"""Potenciales de latencia media y tardía (MLR, CAEP, P300, MMN) con el
equipo de la app: la misma ventana del ABR, con la prueba cambiada. Cada
nivel se registra dos veces (réplica), como el ABR del libro.

Los componentes se rotulan sobre el promedio de las dos réplicas, en el
extremo (positivo o negativo) dentro de una ventana amplia y en orden: la
ventana es ancha a propósito, para que un componente tardío por patología
o por edad también se marque. El texto del capítulo es el que lo lee.
"""
import os

from . import estilo as E
from .datos import RAIZ, fijar_azar
from .svg import Svg

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

PRUEBAS = ('MLR', 'CAEP', 'P300', 'MMN')

# Barridos de las figuras donde el estándar del equipo deja demasiado ruido
# para un libro: la MMN promedia solo los raros (~20 %).
BARRIDOS_LIBRO = {'MMN': 2000}

# Canales que se dibujan por defecto (los del equipo): el MLR compara
# hemisferios (C3, Cz, C4); los tardíos se leen en un canal.
CANALES = {'MLR': ('C3', 'Cz', 'C4'), 'CAEP': ('Cz',), 'P300': ('Pz',), 'MMN': ('Fz',)}

# Ventanas de búsqueda (ms) y polaridad de cada componente. Anchas: un
# componente alargado por la edad o la lesión tiene que caer dentro.
VENTANAS = {
    'MLR': [('Na', 12, 28, -1), ('Pa', 22, 50, 1), ('Nb', 35, 65, -1), ('Pb', 50, 85, 1)],
    'CAEP': [('P1', 40, 260, 1), ('N1', 70, 300, -1), ('P2', 130, 350, 1), ('N2', 180, 420, -1)],
    'P300': [('N1', 70, 200, -1), ('P2', 130, 280, 1), ('N2', 180, 320, -1), ('P3', 250, 700, 1)],
    'MMN': [('MMN', 80, 320, -1)],
}

# µV de la barra de escala (una fila de trazo mide esto de alto)
ESCALA_UV = {'MLR': 1.0, 'CAEP': 5.0, 'P300': 12.0, 'MMN': 2.0}



def _ventana(caso, prueba, promediaciones, ventana_ms):
    from core.base import context  # noqa: F401  (crea el QApplication)
    from abr.AbrMainWindow import AbrMainWindow
    w = AbrMainWindow({'name': 'Libro', 'user': 'libro', 'permission': 'admin'})
    w.la_super(caso, caso.get('id'))
    w.set_test_silently(prueba)
    # El estándar del docente (protocols.STANDARD_SETUP): tasa, filtros,
    # barridos, montaje al lóbulo, oddball 1 kHz/2 kHz 80/20 y la tarea.
    # El equipo del alumno arranca con tasa y barridos al azar a propósito.
    from abr.protocols import standard_setup
    control, tecnico = standard_setup(prueba)
    w.technical.update(tecnico)
    w.control.set_data(control)
    w.apply_window()
    if ventana_ms:
        w.technical = dict(w.technical, window_ms=float(ventana_ms))
        w.apply_window()
    w.control.sb_prom.setValue(promediaciones or BARRIDOS_LIBRO.get(prueba) or control['average'])
    return w


def capturar(caso, lados, niveles, prueba='MLR', estimulo=None, promediaciones=None,
             ventana_ms=None):
    """{lado: [{'db', 'x', 'canales': {canal: (y1, y2)}, 'extra': {nombre: {canal: y}}}]}"""
    if prueba not in PRUEBAS:
        raise ValueError(f'Prueba {prueba!r}; hay: ' + ', '.join(PRUEBAS))
    if caso.get('Central') is None:
        raise ValueError('El caso no tiene bloque Central: armarlo con cuadro(..., central=...)')
    antes = os.getcwd()
    os.chdir(RAIZ)
    try:
        w = _ventana(caso, prueba, promediaciones, ventana_ms)
        if estimulo:
            from .abr import _elegir
            _elegir(w.control.cb_stim, estimulo)
        from abr import cortical as C
        edad = C.age_years(w.data_current)
        out = {}
        for lado in lados:
            g = w.graph_r if lado == 'OD' else w.graph_l
            out[lado] = []
            for db in niveles:
                registros = []
                for rep in (1, 2):
                    fijar_azar('cortical', prueba, caso.get('id'), lado, db, estimulo,
                               *(('replica',) if rep == 2 else ()))
                    i = w.control.cb_side.findText(lado)
                    if i >= 0:
                        w.control.cb_side.setCurrentIndex(i)
                    w.control.sb_intencity.setValue(db)
                    w.control.start_capture()
                    for _ in range(4000):
                        w.capture()
                        if w.state_capture != 'record':
                            break
                    else:
                        raise RuntimeError('la captura no terminó')
                    grupo = w.current_capture_curve
                    lineas = {k.split('.', 1)[1]: v for k, v in g.data.items()
                              if k.startswith(grupo + '.')}
                    registros.append((lineas, dict(w.last_metadata or {})))
                (r1, meta), (r2, _) = registros
                x = [float(t) for t in next(iter(r1.values()))['ipsi_xy'][0]]
                canales = {c: ([float(v) for v in r1[c]['ipsi_xy'][1]],
                               [float(v) for v in r2[c]['ipsi_xy'][1]]) for c in r1}
                extra = {}
                for c, v in r1.items():
                    for nombre, (_, y) in (v.get('overlays') or {}).items():
                        extra.setdefault(nombre, {})[c] = [float(t) for t in y]
                # Sobre el umbral del paciente para ese estímulo: lo dice el
                # generador (nivel de sensación > 0 y registro visible).
                sobre = bool(meta.get('waves_visible')) and float(meta.get('sl') or 0) > 0
                out[lado].append({'db': db, 'x': x, 'canales': canales, 'extra': extra,
                                  'edad': edad, 'sobre_umbral': sobre})
        w.close()
        return out
    finally:
        os.chdir(antes)


def _ventanas(prueba, edad):
    """Ventanas de búsqueda: las normativas de la edad (las del equipo,
    cortical.normative), ensanchadas un 25 % para que un componente alargado
    por la lesión también caiga; si la edad no trae norma, la ancha fija."""
    norma = {}
    if edad is not None:
        from abr import cortical as C
        norma = C.normative(prueba, edad).get('lat', {})
    out = []
    for nombre, lo, hi, signo in VENTANAS[prueba]:
        # Bajo los 10 años la cortical es P1 y N2 (N250): la N1 y la P2 de
        # adulto todavía no se separan (Sharma y cols., 1997; Ponton y cols., 2000).
        if prueba == 'CAEP' and edad is not None and edad < 10 and nombre in ('N1', 'P2'):
            continue
        if nombre in norma:
            a, b = norma[nombre]
            ancho = (b - a) * 0.25
            lo, hi = max(lo * 0.6, a - ancho), b + ancho
        out.append((nombre, lo, hi, signo))
    return out


def _marcas(prueba, x, y, edad=None):
    """Componentes en orden, cada uno en el extremo de su ventana."""
    out, desde = {}, 0.0
    for nombre, lo, hi, signo in _ventanas(prueba, edad):
        pts = [(t, v) for t, v in zip(x, y) if max(lo, desde) <= t <= hi]
        if len(pts) < 3:
            continue
        t, v = (max if signo > 0 else min)(pts, key=lambda p: p[1])
        out[nombre] = (t, v)
        desde = t + 5
    return out


def _relacion(x, y1, y2, t0, signo, ventana_ms):
    """Cuánto sobresale el componente del ruido en la PEOR de las dos réplicas:
    el extremo del signo esperado a ±ventana_ms, sobre la mitad de la
    diferencia entre réplicas. Bajo 1, no está en las dos."""
    import statistics
    ruido = statistics.pstdev([(a - b) / 2 for a, b in zip(y1, y2)]) or 1e-9
    peor = None
    for y in (y1, y2):
        m = sum(y) / len(y)
        cerca = [v for t, v in zip(x, y) if abs(t - t0) <= ventana_ms]
        if not cerca:
            return 0.0
        pico = (max(cerca) - m) if signo > 0 else (m - min(cerca))
        peor = pico / ruido if peor is None else min(peor, pico / ruido)
    return peor


def _hay_respuesta(prueba, relaciones, edad):
    """Criterio de presencia del potencial en ese nivel. En la cortical manda
    el complejo: N1 y P2 en las dos réplicas desde los 10 años, y la P1 antes,
    cuando la N1 todavía no está (los umbrales salen de medir los casos del
    libro: con ellos los niveles sin respuesta quedan sin rótulos)."""
    if prueba != 'CAEP':
        return True
    if edad is not None and edad < 10:
        return relaciones.get('P1', 0) >= 1.5
    return relaciones.get('N1', 0) >= 2.5 and relaciones.get('P2', 0) >= 2.0


def dibujar(curvas, prueba='MLR', canales=None, marcar=True):
    canales = tuple(canales or CANALES[prueba])
    lados = [l for l in ('OD', 'OI') if l in curvas]
    filas = [(c, n) for n in range(max(len(curvas[l]) for l in lados)) for c in canales]
    x_max = max(max(n['x']) for l in lados for n in curvas[l])
    uv_px = 34.0 / ESCALA_UV[prueba]          # px por µV
    amp_px = 34.0
    rep_px = 26.0
    sep_px = amp_px + rep_px + (22 if marcar else 10)
    pw = 290.0
    ms_px = pw / x_max
    ml, mt, gap = 92, 58, 40
    ph = (len(filas) - 1) * sep_px + rep_px + 50
    s = Svg(ml + len(lados) * pw + (len(lados) - 1) * gap + 70, mt + ph + 40)
    paso = {12: 2, 100: 10, 300: 50, 1000: 100}
    tick = next(v for k, v in sorted(paso.items()) if x_max <= k)

    for k, lado in enumerate(lados):
        col = E.COLOR_LADO[lado]
        x0 = ml + k * (pw + gap)

        def X(t):
            return x0 + t * ms_px

        s.texto(x0, mt - 40, E.NOMBRE_LADO[lado], E.T_TITULO, E.TINTA, 'start', 600)
        t = 0
        while t <= x_max + 1e-6:
            s.linea(X(t), mt - 8, X(t), mt + ph, E.GRILLA, 1 if (t / tick) % 2 == 0 else 0.5)
            if (t / tick) % 2 == 0:
                s.texto(X(t), mt + ph + 14, f'{t:g}', E.T_EJE, E.TENUE)
            t += tick
        for j, (canal, n) in enumerate(filas):
            c = curvas[lado][n]
            base = mt + 14 + j * sep_px
            y1, y2 = c['canales'][canal]

            def P(ys, b):
                m = sum(ys) / len(ys)
                return [(X(t), b - (v - m) * uv_px) for t, v in zip(c['x'], ys)]

            for nombre, porcanal in c['extra'].items():
                if canal in porcanal:
                    s.trazo(P(porcanal[canal], base), E.TENUE, E.LINEA_FINA, E.OPACIDAD_SECUNDARIA)
            s.trazo(P(y1, base), col, E.LINEA)
            s.trazo(P(y2, base + rep_px), col, E.LINEA)
            s.ancla(f"{lado} {canal} {c['db']:g}", X(x_max) - 4, base)
            if k == 0:
                s.texto(ml - 12, base + 3, f"{canal} · {c['db']:g} dB", E.T_ROTULO, E.TINTA_2, 'end')
            if marcar and c.get('sobre_umbral', True):
                prom = [(a + b) / 2 for a, b in zip(y1, y2)]
                m = sum(y1) / len(y1)
                signos = {n: s for n, _, _, s in VENTANAS[prueba]}
                from abr import cortical as C
                snap = C.SNAP_MS[prueba]
                marcas = _marcas(prueba, c['x'], prom, c.get('edad'))
                rel = {n: _relacion(c['x'], y1, y2, t, signos[n], snap) for n, (t, _) in marcas.items()}
                # Un nivel sin respuesta queda sin rótulos; en uno con
                # respuesta, solo lo que está en las dos réplicas.
                if not _hay_respuesta(prueba, rel, c.get('edad')):
                    marcas = {}
                for nombre, (t, _) in marcas.items():
                    if rel[nombre] < 1.0:
                        continue
                    i = min(range(len(c['x'])), key=lambda i: abs(c['x'][i] - t))
                    v = y1[i]
                    px, py = X(t), base - (v - m) * uv_px
                    arriba = v >= m
                    s.ancla(f"{lado} {canal} {c['db']:g} {nombre}", px, py)
                    if arriba:
                        s.linea(px, py - 4, px, py - 10, E.TINTA_2, 0.8)
                        s.texto(px, py - 13, nombre, E.T_CHICO, E.TINTA, peso=600)
                    else:
                        s.linea(px, py + 4, px, py + 10, E.TINTA_2, 0.8)
                        s.texto(px, py + 19, nombre, E.T_CHICO, E.TINTA, peso=600)

    xb, yb = s.ancho - 50, mt + ph
    barra = ESCALA_UV[prueba]
    s.linea(xb, yb, xb, yb - barra * uv_px, E.TINTA_2, 1.2)
    s.texto(xb + 5, yb - barra * uv_px / 2 + 3, f'{barra:g} µV', E.T_CHICO, E.TENUE, 'start')
    s.texto(ml + (s.ancho - ml) / 2 - 8, mt + ph + 30, 'Latencia (ms)', E.T_EJE, E.TENUE)
    return s.svg()
