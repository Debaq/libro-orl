"""Audiograma tonal, un panel por oído.

Las reglas clínicas son las de CaseCharts::audiogram (labsim_backend), que es
lo que ve el alumno en la ficha: qué símbolo va enmascarado, dónde se mide
la vía ósea, cómo se dibuja el "no responde" y el LDL. Lo que cambia es solo
el dibujo.
"""
import math

from . import estilo as E
from .datos import por_oido
from .svg import Svg

FRECUENCIAS = [125, 250, 500, 1000, 2000, 3000, 4000, 6000, 8000]
FRECUENCIAS_OSEA = [250, 500, 1000, 2000, 3000, 4000]
ATENUACION_AEREA = [35, 40, 40, 40, 40, 45, 45, 50, 50]   # CaseCharts::ATENUACION_AEREA_POR_FREQ
GAP_ENMASCARA_OSEA = 10
SIN_RESPUESTA = 130
NIVEL_MAXIMO = 120
TOPE_OSEA = 70            # el vibrador no pasa de acá (CaseCharts::TOPE_OSEA_DB)
LIMITE_NORMAL = 20
CORRIMIENTO_OSEA = 9      # px: OD a la izquierda, OI a la derecha
ROTULO = {1000: '1k', 2000: '2k', 3000: '3k', 4000: '4k', 6000: '6k', 8000: '8k'}
OCTAVA_PX = 34            # una octava mide lo mismo que 20 dB (ASHA)
R = 4.0                   # radio de los símbolos


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def sombra(aerea, osea):
    """Lo que mide quien NO enmascara: el oído mejor contesta por el peor.

    Por aérea el tono cruza con la atenuación interaural de la frecuencia
    (ATENUACION_AEREA, la misma regla de enmascaramiento de la ficha) y lo
    oye la cóclea contraria, que se mide por su ósea; por ósea la atenuación
    es casi nula, así que contesta la mejor ósea de las dos."""
    otro = {'OD': 'OI', 'OI': 'OD'}
    a2, o2 = {}, {}
    for lado in ('OD', 'OI'):
        a2[lado], o2[lado] = [], []
        for i in range(len(FRECUENCIAS)):
            a, o, oo = _num(aerea[lado][i]), _num(osea[lado][i]), _num(osea[otro[lado]][i])
            cruce = oo + ATENUACION_AEREA[i] if oo is not None else None
            a2[lado].append(min(a, cruce) if a is not None and cruce is not None else a)
            o2[lado].append(min(o, oo) if o is not None and oo is not None else o)
    return a2, o2


def dibujar(caso, estudio=True, ldl=True, oidos=('OD', 'OI'), sin_enmascarar=False, combinado=False, fowler=(),
            clinico=False):
    """combinado=True: los dos oídos en una sola grilla, como el audiograma clínico.
    estudio=True: la ósea no aparece donde el aéreo de ese oído es normal
    (como en la ficha de estudio; un examen real no la busca ahí).
    clinico=True: la hoja clínica de los casos vestibulares (audio_supra.py):
    frecuencias arriba, ósea completa de 250 a 4.000 Hz si una frecuencia la
    necesita, rótulo "LDL:" y el Fowler (ver fowler).
    sin_enmascarar=True: lo que anota quien no enmascara (curva sombra).
    fowler: [(frecuencia, lado, patrón, [(nivel OD, nivel OI), ...])] de
    supraliminares.fowler: el balance va sobre la línea de esa frecuencia,
    el OD a la izquierda y el OI a la derecha, unidos por una línea."""
    aerea = por_oido(caso['Aerea'])
    osea = por_oido(caso['Osea'])
    if sin_enmascarar:
        aerea, osea = sombra(aerea, osea)
        ldl = False
    ldl_d = por_oido(caso['LDL']) if ldl and caso.get('LDL') else None
    otro = {'OD': 'OI', 'OI': 'OD'}

    db_px = OCTAVA_PX / 20
    pw, ph = 6 * OCTAVA_PX, 130 * db_px
    # clinico: las frecuencias van arriba, como en la hoja clínica (él, 2026-10-20)
    ml, mt, sep, mb = (36, 58, 34, 14) if clinico else (36, 30, 34, 40)
    paneles = 1 if combinado else len(oidos)
    s = Svg(ml + paneles * pw + (paneles - 1) * sep + 14, mt + ph + mb)

    rotulos_ldl = []
    for k, lado in enumerate(oidos):
        col = E.COLOR_LADO[lado]
        if not combinado:
            rotulos_ldl = []
        x0 = ml + (0 if combinado else k) * (pw + sep)

        def X(f):
            return x0 + math.log2(f / 125) * OCTAVA_PX

        def Y(db):
            return mt + (max(-10.0, min(float(NIVEL_MAXIMO), db)) + 10) * db_px

        # Fondo: zona de audición normal y grilla (una sola vez si va combinado)
        if not (combinado and k):
            s.rect(x0, Y(-10), pw, Y(LIMITE_NORMAL) - Y(-10), E.LAVADO)
            for db in range(-10, 121, 10):
                fuerte = db in (0, LIMITE_NORMAL)
                s.linea(x0, Y(db), x0 + pw, Y(db), E.GRILLA_FUERTE if fuerte else E.GRILLA,
                        1 if (fuerte or db % 20 == 0) else 0.5)
                if k == 0 and db % 20 == 0:
                    s.texto(x0 - 7, Y(db) + 3, db, E.T_EJE, E.TENUE, 'end')
            for f in FRECUENCIAS:
                mayor = f not in (3000, 6000)
                s.linea(X(f), Y(-10), X(f), Y(120), E.GRILLA, 1 if mayor else 0.5)
                s.texto(X(f), Y(-10) - 6 if clinico else Y(120) + 14, ROTULO.get(f, f), E.T_EJE if mayor else E.T_CHICO,
                        E.TENUE if mayor else E.MUY_TENUE)
        if not combinado:   # combinado: sin leyenda, el color y el símbolo ya dicen el oído
            s.texto(x0, 14 if clinico else mt - 12, E.NOMBRE_LADO[lado], E.T_TITULO, E.TINTA, 'start', 600)

        a = [_num(v) for v in aerea[lado]]
        o = [_num(v) for v in osea[lado]]
        o_otro = [_num(v) for v in osea[otro[lado]]]

        # Vía aérea: línea por los tramos con umbral (el "no responde" no se une)
        for tramo in _tramos([(X(f), Y(v)) if v is not None and v < SIN_RESPUESTA else None
                              for f, v in zip(FRECUENCIAS, a)]):
            s.trazo(tramo, col, 1.4)

        # Vía ósea: punteada, solo donde se mide
        # clinico: si la curva necesita una sola ósea, se hacen todas, de 250 a
        # 4.000 Hz (él, 2026-10-20); si ninguna aérea pasa de 20 dB, no se mide.
        necesita = any(f in FRECUENCIAS_OSEA and a[i] is not None and a[i] > LIMITE_NORMAL
                       for i, f in enumerate(FRECUENCIAS))
        idx_osea = [i for i, f in enumerate(FRECUENCIAS) if f in FRECUENCIAS_OSEA
                    and o[i] is not None
                    and (not estudio or (necesita if clinico else (a[i] is not None and a[i] > LIMITE_NORMAL)))]
        desp = -CORRIMIENTO_OSEA if lado == 'OD' else CORRIMIENTO_OSEA
        for tramo in _tramos([(X(FRECUENCIAS[i]) + desp, Y(o[i])) if i in idx_osea and o[i] <= TOPE_OSEA else None
                              for i in range(len(FRECUENCIAS))]):
            s.trazo(tramo, col, 0.9, guiones='1 2.5')

        # LDL: guiones largos, solo si se midió
        if ldl_d and any(_num(v) is not None and _num(v) < SIN_RESPUESTA for v in ldl_d[lado]):
            l = [_num(v) for v in ldl_d[lado]]
            pts = [(X(f), Y(l[i])) if f in FRECUENCIAS_OSEA and l[i] is not None and l[i] < SIN_RESPUESTA else None
                   for i, f in enumerate(FRECUENCIAS)]
            for tramo in _tramos(pts):
                s.trazo(tramo, col, 0.9, guiones='4 3')
            # rótulo "LDL" subrayado a la izquierda del primer LDL (uno solo si
            # los dos oídos quedan a la misma altura en el combinado)
            primero = next(((X(f), Y(min(l[i], NIVEL_MAXIMO))) for i, f in enumerate(FRECUENCIAS)
                            if f in FRECUENCIAS_OSEA and l[i] is not None), None)
            if clinico and primero and all(abs(primero[1] - yy) > 8 for yy in rotulos_ldl):
                rotulos_ldl.append(primero[1])
                s.texto(primero[0] - 12, primero[1] + 3, 'LDL:', E.T_CHICO, E.TINTA_2, 'end', 600,
                        'text-decoration="underline"')
            for i, f in enumerate(FRECUENCIAS):
                if f in FRECUENCIAS_OSEA and l[i] is not None:
                    y = Y(min(l[i], NIVEL_MAXIMO))
                    _ldl(s, X(f), y, col, -1 if lado == 'OD' else 1)
                    if l[i] >= SIN_RESPUESTA:
                        _flecha(s, X(f), y, col, -1 if lado == 'OD' else 1)

        # Símbolos (encima de las líneas)
        for i, f in enumerate(FRECUENCIAS):
            if a[i] is None:
                continue
            sin = a[i] >= SIN_RESPUESTA
            x, y = X(f), Y(NIVEL_MAXIMO if sin else a[i])
            enmascarada = (not sin_enmascarar and o_otro[i] is not None
                           and (a[i] - o_otro[i]) >= ATENUACION_AEREA[i])
            _simbolo_aereo(s, lado, x, y, col, enmascarada)
            s.ancla(f'{lado} {f}', x, y)
            if sin:
                _flecha(s, x, y, col, -1 if lado == 'OD' else 1)
        for i in idx_osea:
            sin = o[i] > TOPE_OSEA
            x, y = X(FRECUENCIAS[i]) + desp, Y(TOPE_OSEA if sin else o[i])
            # Contra la MEJOR ósea: sin enmascarar contesta la mejor cóclea
            # (CaseCharts::audiogram, boneMasked en audiogram.js).
            mejor = o[i] if o_otro[i] is None else min(o[i], o_otro[i])
            enmascarada = not sin_enmascarar and a[i] is not None and (a[i] - mejor) >= GAP_ENMASCARA_OSEA
            _simbolo_oseo(s, lado, x, y, col, enmascarada)
            s.ancla(f'{lado} osea {FRECUENCIAS[i]}', x, y)
            if sin:
                _flecha(s, x, y, col, -1 if lado == 'OD' else 1)

    # Fowler: en la frecuencia estudiada, marcas a los lados de la línea
    rotulos = []
    for f, _l, _, pares in fowler:
        x = ml + math.log2(f / 125) * OCTAVA_PX
        # Las marcas van a los lados de la línea, sin llegar a la línea vecina
        # (3k y 6k están a media octava): cada lado usa su propio espacio.
        i = FRECUENCIAS.index(f)
        izq = math.log2(f / FRECUENCIAS[i - 1]) * OCTAVA_PX if i > 0 else OCTAVA_PX
        der = math.log2(FRECUENCIAS[i + 1] / f) * OCTAVA_PX if i + 1 < len(FRECUENCIAS) else OCTAVA_PX
        dx_od, dx_oi = min(13, 0.45 * izq), min(13, 0.45 * der)
        # Fowler (+): recluta (parcial, completo o sobrerreclutamiento); (−): no recluta
        # dos rótulos cercanos se escalonan para no montarse
        y_rot = mt - 31 if rotulos and x - rotulos[-1] < 55 and len(rotulos) % 2 else mt - 20
        rotulos.append(x)
        s.texto(x, y_rot, f"Fowler ({'−' if _ == 'none' else '+'})", E.T_CHICO, E.TINTA_2, 'middle', 600)
        for l_od, l_oi in pares:
            y_od = mt + (l_od + 10) * db_px
            y_oi = mt + (l_oi + 10) * db_px
            s.linea(x - dx_od, y_od, x + dx_oi, y_oi, E.TINTA_2, 1.0)
            s.circulo(x - dx_od, y_od, 2.6, E.OD, E.PAPEL, 1.2)
            r = 2.3
            xo = x + dx_oi
            s.camino(f'M{xo - r:.2f},{y_oi - r:.2f} L{xo + r:.2f},{y_oi + r:.2f} '
                     f'M{xo - r:.2f},{y_oi + r:.2f} L{xo + r:.2f},{y_oi - r:.2f}', E.OI, 1.2)
    if sin_enmascarar:
        s.texto(s.ancho - 14, 14, 'sin enmascarar', E.T_CHICO, E.TENUE, 'end')
    s.texto(14, mt + ph / 2, 'dB HL', E.T_EJE, E.TENUE,
            extra=f'transform="rotate(-90 14 {mt + ph / 2:.1f})"')
    if clinico:
        s.texto(ml + (s.ancho - ml - 14) / 2 if combinado else s.ancho / 2, 14 if combinado else 30,
                'Frecuencia (Hz)', E.T_EJE, E.TENUE)
    else:
        s.texto(s.ancho / 2, mt + ph + 34, 'Frecuencia (Hz)', E.T_EJE, E.TENUE)
    return s.svg()


def _tramos(puntos):
    tramo = []
    for p in puntos:
        if p is None:
            if len(tramo) > 1:
                yield tramo
            tramo = []
        else:
            tramo.append(p)
    if len(tramo) > 1:
        yield tramo


def _simbolo_aereo(s, lado, x, y, col, enmascarada):
    if lado == 'OD':
        if enmascarada:      # triángulo
            s.camino(f'M{x:.2f},{y - R:.2f} L{x - R:.2f},{y + R * .8:.2f} L{x + R:.2f},{y + R * .8:.2f} Z',
                     col, E.LINEA, E.PAPEL)
        else:                # círculo
            s.circulo(x, y, R, col)
    else:
        if enmascarada:      # cuadrado
            s.rect(x - R * .85, y - R * .85, R * 1.7, R * 1.7, E.PAPEL, col, E.LINEA)
        else:                # cruz
            r = R * .85
            s.camino(f'M{x - r:.2f},{y - r:.2f} L{x + r:.2f},{y + r:.2f} M{x - r:.2f},{y + r:.2f} L{x + r:.2f},{y - r:.2f}',
                     col)


def _simbolo_oseo(s, lado, x, y, col, enmascarada):
    r = R
    d = -1 if lado == 'OD' else 1      # OD abre a la derecha: "<" y "["
    if enmascarada:
        d_ = (f'M{x - d * r * .6:.2f},{y - r:.2f} L{x + d * r:.2f},{y - r:.2f} '
              f'L{x + d * r:.2f},{y + r:.2f} L{x - d * r * .6:.2f},{y + r:.2f}')
    else:
        d_ = f'M{x - d * r * .7:.2f},{y - r:.2f} L{x + d * r * .7:.2f},{y:.2f} L{x - d * r * .7:.2f},{y + r:.2f}'
    s.camino(d_, col)


def _ldl(s, x, y, col, lado, algiacusia=False):
    # Umbral de molestia: triángulo VACÍO. El relleno es el umbral de
    # algiacusia (dolor), otro símbolo; LabSim no lo mide.
    xc, xp = x + lado * 1.8, x + lado * 6.6
    s.camino(f'M{xc:.2f},{y - 3:.2f} L{xc:.2f},{y + 3:.2f} L{xp:.2f},{y + 3:.2f} Z', col, 1.1,
             col if algiacusia else E.PAPEL)


def _flecha(s, x, y, col, lado):
    x1, y1 = x + lado * 3, y + 4
    x2, y2 = x1 + lado * 5, y1 + 7
    s.camino(f'M{x1:.2f},{y1:.2f} L{x2:.2f},{y2:.2f} M{x2:.2f},{y2:.2f} L{x2 - lado * 3.4:.2f},{y2 - .6:.2f} '
             f'M{x2:.2f},{y2:.2f} L{x2 - lado * .6:.2f},{y2 - 3.4:.2f}', col, 1.2)


def con_logo(caso):
    """Audiograma combinado y, a su lado, la logoaudiometría en datos: SDT,
    SRT y UMD con los tres mejores intentos (de la curva de 10 en 10 dB) y el
    enmascaramiento solo si corresponde (voz − PTP óseo del otro oído ≥ 45 dB,
    regla del H5)."""
    import re
    from . import logo
    aud = dibujar(caso, combinado=True)
    w = float(re.search(r'width="([\d.]+)"', aud)[1])
    h = float(re.search(r'height="([\d.]+)"', aud)[1])
    interior = re.sub(r'^<svg[^>]*>|</svg>\s*$', '', aud.strip())
    interior = re.sub(r'<metadata.*?</metadata>', '', interior, flags=re.S)
    curvas = logo.curvas(caso, True)
    osea = por_oido(caso['Osea'])
    otro = {'OD': 'OI', 'OI': 'OD'}

    def ptp_oseo(lado):
        v = [_num(x) for f, x in zip(FRECUENCIAS, osea[lado]) if f in (500, 1000, 2000)]
        v = [x for x in v if x is not None]
        return sum(v) / len(v) if v else 0.0

    x0, y, out = w + 26, 34, []

    def t(x, y, txt, tam=E.T_ROTULO, col=E.TINTA, peso=400):
        out.append(f'<text x="{x}" y="{y}" font-size="{tam}" fill="{col}" font-weight="{peso}">{txt}</text>')

    t(x0, y, 'Logoaudiometría', E.T_TITULO, E.TINTA, 700)
    y += 20
    for i, lado in enumerate(('OD', 'OI')):
        pts = {db: p for db, p in curvas[lado] if db % 10 == 0}
        mejores = sorted(sorted(pts.items(), key=lambda dp: (-dp[1], dp[0]))[:3])
        enmasc = [db for db, _ in mejores if db - ptp_oseo(otro[lado]) >= 45]
        t(x0, y, lado, E.T_ROTULO + 1, E.COLOR_LADO[lado], 700)
        y += 16
        for et, val in (('SDT', caso['SDT'][i]), ('SRT', caso['SRT'][i])):
            t(x0 + 6, y, et, E.T_ROTULO, E.TENUE, 600)
            t(x0 + 52, y, f'{val} dB')
            y += 14
        t(x0 + 6, y, 'UMD', E.T_ROTULO, E.TENUE, 600)
        for db, p in mejores:
            t(x0 + 52, y, f'{p:.0f} % a {db} dB')
            y += 14
        if enmasc:
            t(x0 + 52, y, f'con ruido de habla al {otro[lado]}', E.T_CHICO, E.TENUE)
            y += 14
        y += 8
    t(x0, y + 4, 'UMD: los tres mejores intentos.', E.T_CHICO, E.TENUE)
    W, H = x0 + 170, max(h, y + 12)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'font-family="{E.FUENTE}">{interior}{"".join(out)}</svg>')
