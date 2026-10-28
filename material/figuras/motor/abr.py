"""ABR con el equipo de la app: se abre la ventana ABR sin pantalla, se
captura cada nivel como lo haría el alumno, y se dibuja el resultado.

Las ondas se rotulan donde el generador las puso (metadata 'waves'), sobre
el pico real de la curva promediada: nunca a ojo.
"""
import os

from . import estilo as E
from .datos import RAIZ, fijar_azar
from .svg import Svg

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

_VENTANA = {}

# Nombre corto del libro -> valor del equipo (AbrAdvanceSettings.TRANSDUCERS
# y el combo de polaridad de la ventana).
TRANSDUCTORES = {'insercion': 'insert_earphone', 'copa': 'TDH39_headphone',
                 'oseo': 'bone_vibrator'}
POLARIDADES = {'alternada': 'Alternada', 'condensacion': 'Condensación',
               'rarefaccion': 'Rarefacción'}

# Una onda se rotula si sobresale del ruido residual del promedio (el de la
# diferencia A-B): con el umbral fijo de 0,02 µV se marcaba una "V" donde
# solo había ruido. Y nunca debajo de AMP_MIN_UV, aunque el ruido sea bajo.
SNR_ROTULO = 3.0
AMP_MIN_UV = 0.05


def _ventana(caso, promediaciones, transductor='insercion', tasa=21.1, ventana=12.0):
    from core.base import context  # noqa: F401  (crea el QApplication)
    from abr.AbrMainWindow import AbrMainWindow
    w = AbrMainWindow({'name': 'Libro', 'user': 'libro', 'permission': 'admin'})
    w.la_super(caso, caso.get('id'))
    if transductor not in TRANSDUCTORES:
        raise ValueError(f'Transductor {transductor!r}; hay: ' + ', '.join(TRANSDUCTORES))
    # Lo mismo que hace Aceptar en Parámetros avanzados (active_advance_setting).
    w.technical = dict(w.technical, transducer=TRANSDUCTORES[transductor])
    if ventana and ventana != 12.0:
        w.technical['window_ms'] = float(ventana)   # el burst grave y el lactante piden más
    w.apply_window()
    w.control.sb_prom.setValue(promediaciones)
    w.control.sb_rate.setValue(tasa)
    # Banda de rutina: el equipo arranca abierto a propósito (lo configura
    # el alumno); para el libro se registra ya bien puesto.
    for combo, texto in ((w.control.cb_filter_up, '100'), (w.control.cb_filter_down, '3000')):
        i = combo.findText(texto)
        if i >= 0:
            combo.setCurrentIndex(i)
    return w


def _elegir(combo, texto):
    if texto is None:
        return
    for i in range(combo.count()):
        if texto.lower() in combo.itemText(i).lower():
            combo.setCurrentIndex(i)
            return
    raise ValueError(f'No existe la opción {texto!r}; hay: '
                     + ', '.join(combo.itemText(i) for i in range(combo.count())))


def capturar(caso, lados, niveles, estimulo=None, promediaciones=2000,
             transductor='insercion', polaridad='alternada', tasa=21.1, enmascaramiento=0.0,
             ventana=12.0):
    """Devuelve {lado: [{'db', 'x', 'y', 'a', 'b', 'ondas', 'visibles'}]}.

    transductor: 'insercion', 'copa' u 'oseo' (el vibrador llega a 55 dB nHL);
    polaridad: 'alternada', 'condensacion' o 'rarefaccion'; tasa en estímulos/s;
    enmascaramiento: dB de ruido en el oído contrario (el MKG del panel).
    """
    # La app abre sus recursos (resources/) con rutas relativas a la raíz
    antes = os.getcwd()
    os.chdir(RAIZ)
    try:
        return _capturar(caso, lados, niveles, estimulo, promediaciones,
                         transductor, polaridad, tasa, enmascaramiento, ventana)
    finally:
        os.chdir(antes)


def _capturar(caso, lados, niveles, estimulo, promediaciones, transductor, polaridad, tasa,
              enmascaramiento=0.0, ventana=12.0):
    if polaridad not in POLARIDADES:
        raise ValueError(f'Polaridad {polaridad!r}; hay: ' + ', '.join(POLARIDADES))
    w = _ventana(caso, promediaciones, transductor, tasa, ventana)
    _elegir(w.control.cb_stim, estimulo)
    _elegir(w.control.cb_pol, POLARIDADES[polaridad])
    w.control.sb_mskg.setValue(enmascaramiento)
    umbrales = _umbrales(caso, estimulo, transductor)
    out = {}
    for lado in lados:
        g = w.graph_r if lado == 'OD' else w.graph_l
        out[lado] = []
        for db in niveles:
            # Cada nivel se registra dos veces, como en la clínica: la réplica
            # es lo que dice que una onda es respuesta y no ruido (él, 2026-10-22).
            # La primera conserva la semilla de siempre, así sus latencias no cambian.
            registros = []
            for rep in (1, 2):
                fijar_azar('abr', caso.get('id'), lado, db, estimulo,
                           *(() if (transductor, polaridad, tasa) == ('insercion', 'alternada', 21.1)
                             else (transductor, polaridad, tasa)),
                           *((enmascaramiento,) if enmascaramiento else ()),
                           *(('replica',) if rep == 2 else ()))
                i = w.control.cb_side.findText(lado)
                if i >= 0:
                    w.control.cb_side.setCurrentIndex(i)
                w.control.sb_intencity.setValue(db)
                w.control.start_capture()
                for _ in range(2000):
                    w.capture()
                    if w.state_capture != 'record':
                        break
                else:
                    raise RuntimeError('la captura no terminó')
                v = g.data[list(g.data)[-1]]
                meta = w.last_metadata or {}
                registros.append((v, meta))
            (v, meta), (v2, _) = registros
            out[lado].append({
                'db': v['intencity'],
                'x': [float(t) for t in v['ipsi_xy'][0]],
                'y': [float(t) for t in v['ipsi_xy'][1]],
                'x2': [float(t) for t in v2['ipsi_xy'][0]],
                'y2': [float(t) for t in v2['ipsi_xy'][1]],
                'a': [float(t) for t in v['sub_a'][1]],
                'b': [float(t) for t in v['sub_b'][1]],
                'ondas': meta.get('waves') or {},
                'visibles': bool(meta.get('waves_visible')),
                'umbral': umbrales.get(lado, 'sin dato'),
            })
    w.close()
    return out


def dibujar(curvas, marcar=('I', 'III', 'V'), ms_max=12.0, uv_px=80):
    lados = [l for l in ('OD', 'OI') if l in curvas]
    n = max(len(curvas[l]) for l in lados)
    # Separación entre trazos según la amplitud real: que no se pisen
    # y aire fijo para el rótulo de la onda, que no choque con la de arriba
    p2p = max((max(c['y']) - min(c['y'])) for l in lados for c in curvas[l])
    amp_px = min(1.4, max(0.45, p2p)) * uv_px
    # La réplica va pegada bajo su registro; entre niveles, aire para los rótulos
    rep_px = max(10.0, 0.3 * amp_px)
    sep_px = amp_px + rep_px + (18 if marcar else 6)
    ms_px = 22
    pw = ms_max * ms_px
    ml, mt, gap = 70, 58, 40
    ph = (n - 1) * sep_px + rep_px + 50
    s = Svg(ml + len(lados) * pw + (len(lados) - 1) * gap + 64, mt + ph + 40)

    for k, lado in enumerate(lados):
        col = E.COLOR_LADO[lado]
        x0 = ml + k * (pw + gap)

        def X(t):
            return x0 + t * ms_px

        s.texto(x0, mt - 40, E.NOMBRE_LADO[lado], E.T_TITULO, E.TINTA, 'start', 600)
        for t in range(0, int(ms_max) + 1):
            s.linea(X(t), mt - 8, X(t), mt + ph, E.GRILLA, 1 if t % 2 == 0 else 0.5)
            if t % 2 == 0:
                s.texto(X(t), mt + ph + 14, t, E.T_EJE, E.TENUE)
        for j, c in enumerate(sorted(curvas[lado], key=lambda c: -c['db'])):
            base = mt + 14 + j * sep_px
            dentro = [(t, y) for t, y in zip(c['x'], c['y']) if t <= ms_max]
            m = sum(y for _, y in dentro) / len(dentro)

            def P(xs, ys, b=base):
                return [(X(t), b - (y - m) * uv_px) for t, y in zip(xs, ys) if t <= ms_max]

            s.trazo(P(c['x'], c['y']), col, E.LINEA)
            if c.get('y2'):
                d2 = [y for t, y in zip(c['x2'], c['y2']) if t <= ms_max]
                m2 = sum(d2) / len(d2)
                s.trazo(P(c['x2'], [y - m2 + m for y in c['y2']], base + rep_px), col, E.LINEA)
            s.ancla(f"{lado} {c['db']:g}", X(ms_max) - 4, base)
            if k == 0:
                s.texto(ml - 12, base + 3, f"{c['db']:g} dB", E.T_ROTULO, E.TINTA_2, 'end')
            # El umbral del caso decide: bajo él no se rotula nada (lo que se
            # vea ahí es ruido, aunque se parezca a una V); sobre él, la onda
            # que puso el generador. Sin dato del umbral, manda la réplica.
            u = c.get('umbral', 'sin dato')
            bajo_umbral = u is None or (u != 'sin dato' and c['db'] < u)
            if c['visibles'] and not bajo_umbral:
                for onda in marcar:
                    pico = _pico(c, onda)
                    if pico is None or (u == 'sin dato' and not _se_repite(c, *pico)):
                        continue
                    t, y = pico
                    px, py = X(t), base - (y - m) * uv_px
                    s.ancla(f"{lado} {c['db']:g} {onda}", px, py)
                    s.linea(px, py - 4, px, py - 10, E.TINTA_2, 0.8)
                    s.texto(px, py - 13, onda, E.T_CHICO, E.TINTA, peso=600)

    # Barra de escala: 0,5 µV
    xb, yb = s.ancho - 44, mt + ph
    s.linea(xb, yb, xb, yb - 0.5 * uv_px, E.TINTA_2, 1.2)
    s.texto(xb + 5, yb - 0.25 * uv_px + 3, '0,5 µV', E.T_CHICO, E.TENUE, 'start')
    s.texto(ml + (s.ancho - ml) / 2 - 8, mt + ph + 30, 'Latencia (ms)', E.T_EJE, E.TENUE)
    return s.svg()


# Rótulo del combo -> clave de umbral_por_estimulo del caso
CLAVES_ESTIMULO = [('nb ce-chirp ls 500', 'nb_ce_chirp_ls_500Hz'), ('nb ce-chirp ls 1', 'nb_ce_chirp_ls_1000Hz'),
                   ('nb ce-chirp ls 2', 'nb_ce_chirp_ls_2000Hz'), ('nb ce-chirp ls 4', 'nb_ce_chirp_ls_4000Hz'),
                   ('ce-chirp ls', 'ce_chirp_ls'), ('ce-chirp', 'ce_chirp'),
                   ('burst 500', 'tone_burst_500Hz'), ('burst 1', 'tone_burst_1000Hz'),
                   ('burst 2', 'tone_burst_2000Hz'), ('burst 4', 'tone_burst_4000Hz'), ('click', 'click')]


def _umbrales(caso, estimulo, transductor):
    """Umbral de la V del caso por oído para este estímulo y vía ({} si no hay dato).
    None = sin respuesta a ninguna intensidad."""
    texto = (estimulo or 'Click').lower()
    clave = next((k for patron, k in CLAVES_ESTIMULO if texto.startswith(patron)), None)
    campo = 'umbral_por_estimulo_oseo' if transductor == 'oseo' else 'umbral_por_estimulo'
    out = {}
    for lado in ('OD', 'OI'):
        tabla = ((caso.get('ABR') or {}).get(lado) or {}).get(campo) or {}
        if clave and clave in tabla:
            out[lado] = tabla[clave]
    return out


def _se_repite(c, t0, y0, ventana_ms=0.35, fraccion=0.5):
    """Una onda se rotula solo si la réplica también la tiene: un máximo local
    cerca de la misma latencia, con al menos la mitad de su altura sobre la
    media del trazo. Lo que está en un registro y no en el otro es ruido."""
    if not c.get('y2'):
        return True
    m1 = sum(c['y']) / len(c['y'])
    m2 = sum(c['y2']) / len(c['y2'])
    alto = y0 - m1
    xs, ys = c['x2'], c['y2']
    for i in range(1, len(xs) - 1):
        if abs(xs[i] - t0) <= ventana_ms and ys[i] >= ys[i - 1] and ys[i] >= ys[i + 1] \
                and ys[i] - m2 >= fraccion * alto:
            return True
    return False


def _ruido(c):
    """Ruido residual del promedio (µV RMS): la mitad de la diferencia A-B."""
    d = [(a - b) / 2 for a, b in zip(c['a'], c['b'])]
    if not d:
        return 0.0
    m = sum(d) / len(d)
    return (sum((v - m) ** 2 for v in d) / len(d)) ** 0.5


def _pico(c, onda, ventana_ms=0.35):
    """Máximo de la curva promediada cerca de la latencia que usó el generador."""
    o = c['ondas'].get(onda)
    if not o or o.get('amp', 0) < max(AMP_MIN_UV, SNR_ROTULO * _ruido(c)):
        return None
    lat, xs, ys = o['lat'], c['x'], c['y']
    # Solo un máximo local de verdad: el borde de la ventana sobre una
    # pendiente no es un pico, y ahí se deja la onda sin rotular.
    picos = [(xs[i], ys[i]) for i in range(1, len(xs) - 1)
             if abs(xs[i] - lat) <= ventana_ms and ys[i] >= ys[i - 1] and ys[i] >= ys[i + 1]]
    if not picos:
        return None
    return max(picos, key=lambda p: p[1])
