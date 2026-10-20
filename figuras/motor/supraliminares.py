"""Pruebas supraliminares, desde los datos del caso en LabSim.

A la izquierda, la escalera de Fowler (balance binaural de sonoridad) en cada
frecuencia que el caso tiene configurada: los dos oídos en columnas, con el
nivel que suena igual unido por una línea. A la derecha, los datos de cada
oído estudiado: SISI, deterioro tonal de Carhart y Metz (umbral del reflejo
menos umbral tonal), como se anotan en la hoja.

Las reglas son las del simulador:
- Fowler: los patrones de Fowler.FOWLER_PATTERNS (none, partial, complete,
  over), con los cortes en dB sobre el umbral del oído estudiado.
- SISI: un porcentaje por oído (response_sisi).
- Carhart: dB que hay que subir para que el tono se sostenga el minuto, en
  500, 1.000, 2.000 y 4.000 Hz (response.py, 'frequencies': [2, 3, 4, 6]).
- Reflejo ipsilateral en 500, 1.000, 2.000 y 4.000 Hz; 130 = ausente.
"""
from . import estilo as E
from .datos import por_oido
from .svg import Svg

FRECUENCIAS = [125, 250, 500, 1000, 2000, 3000, 4000, 6000, 8000]
CORTES = {'none': (200, 200, 200), 'partial': (15, 200, 200), 'complete': (15, 30, 200), 'over': (15, 30, 50)}
NOMBRE = {'none': 'sin reclutamiento', 'partial': 'reclutamiento parcial',
          'complete': 'reclutamiento completo', 'over': 'sobrerreclutamiento'}
CARHART_F = [500, 1000, 2000, 4000]
REFLEJO_F = [500, 1000, 2000, 4000]
AUSENTE = 130


def _hz(f):
    return f'{f // 1000} kHz' if f >= 1000 else f'{f} Hz'


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def oidos_estudiados(caso):
    """Oídos con pérdida sensorioneural (aérea ≥ 30 dB entre 500 y 4.000 Hz,
    con la ósea a menos de 15 dB): ahí van las supraliminares."""
    aerea, osea = por_oido(caso['Aerea']), por_oido(caso['Osea'])
    out = []
    for lado in ('OD', 'OI'):
        for f, a, o in zip(FRECUENCIAS, aerea[lado], osea[lado]):
            a, o = _num(a), _num(o)
            if 500 <= f <= 4000 and a is not None and a >= 30 and (o is None or a - o < 15):
                out.append(lado)
                break
    return out


def _balance(l_ref, th_ref, th_est, patron):
    """Nivel del oído estudiado que suena igual que l_ref en el oído de
    referencia (la misma lógica de cortes de Fowler.py, en continuo)."""
    c1, c2, c3 = CORTES[patron]
    gap = th_est - th_ref
    igual_sl = l_ref + gap                       # misma sensación sobre el umbral
    if igual_sl < th_est + c1:
        return igual_sl
    if patron == 'partial':                       # se acerca, no cierra: queda la mitad
        return max(l_ref + gap / 2, th_est + c1)
    if c2 >= 200:
        return igual_sl
    # entre c1 y c2 converge; desde c2, misma intensidad; desde c3, 10 dB menos
    a0 = th_ref + c1                             # l_ref donde empieza a reclutar
    a1 = th_est + c2                             # l_ref donde ya iguala
    if l_ref < a1:
        k = (l_ref - a0) / max(a1 - a0, 1)
        return th_est + c1 + k * (c2 - c1)
    if l_ref >= th_est + c3:
        return l_ref - 10
    return l_ref


def _pares(th, lado_est, patron):
    """Pares (nivel OD, nivel OI) que suenan igual, desde el umbral."""
    ref = 'OI' if lado_est == 'OD' else 'OD'
    th_ref, th_est = th[ref], th[lado_est]
    pares, l_ref = [], th_ref
    while l_ref <= 100:
        l_est = th_est if l_ref == th_ref else round(_balance(l_ref, th_ref, th_est, patron) / 5) * 5
        if l_est > 110:
            break
        pares.append({ref: l_ref, lado_est: l_est})
        l_ref += 20                              # el oído sano sube de 20 en 20 desde su umbral
    return [(p['OD'], p['OI']) for p in pares]


def fowler(caso):
    """[(frecuencia, lado estudiado, patrón, [(nivel OD, nivel OI), ...])] de
    las frecuencias con Fowler configurado en el caso."""
    aerea = por_oido(caso['Aerea'])
    fdata = caso.get('Fowler') or {}
    patrones = fdata.get('patterns') if isinstance(fdata, dict) and fdata.get('enabled') else {}
    out = []
    for k, patron in sorted((patrones or {}).items(), key=lambda kv: int(kv[0])):
        th = {l: _num(aerea[l][int(k)]) for l in ('OD', 'OI')}
        if None in th.values() or patron not in CORTES:
            continue
        lado_est = 'OD' if th['OD'] > th['OI'] else 'OI'
        out.append((FRECUENCIAS[int(k)], lado_est, patron, _pares(th, lado_est, patron)))
    return out


def _escalera(s, x0, y0, alto, f, th, lado_est, patron):
    """Escalera de Fowler: OD a la izquierda, OI a la derecha, 0 dB arriba."""
    ref = 'OI' if lado_est == 'OD' else 'OD'
    ancho = 90

    def Y(db):
        return y0 + db / 120 * alto
    xs = {'OD': x0 + 20, 'OI': x0 + 20 + ancho}
    s.texto(x0 + 20 + ancho / 2, y0 - 22, f'Fowler · {_hz(f)}', E.T_TITULO, E.TINTA, 'middle', 700)
    s.texto(x0 + 20 + ancho / 2, y0 - 9, NOMBRE[patron], E.T_CHICO, E.TENUE)
    for db in range(0, 121, 20):
        s.texto(x0 + 8, Y(db) + 3, db, E.T_EJE, E.TENUE, 'end')
        s.linea(xs['OD'], Y(db), xs['OI'], Y(db), E.GRILLA, 0.8)
    for lado, x in xs.items():
        s.linea(x, Y(0), x, Y(120), E.GRILLA_FUERTE, 1.2)
        s.texto(x, Y(120) + 14, lado, E.T_ROTULO, E.COLOR_LADO[lado], 'middle', 700)
    th_ref, th_est = th[ref], th[lado_est]
    pares = []
    l_ref = th_ref
    while l_ref <= 100:
        l_est = th_est if l_ref == th_ref else round(_balance(l_ref, th_ref, th_est, patron) / 5) * 5
        if l_est > 110:
            break
        pares.append((l_ref, l_est))
        l_ref += 20 if l_ref > th_ref else max(20 - th_ref % 20, 10)
    for l_r, l_e in pares:
        s.linea(xs[ref], Y(l_r), xs[lado_est], Y(l_e), E.TINTA_2, 1.1)
        for lado, db in ((ref, l_r), (lado_est, l_e)):
            col = E.COLOR_LADO[lado]
            if lado == 'OD':
                s.circulo(xs[lado], Y(db), 3.6, col, E.PAPEL, 1.5)
            else:
                s.linea(xs[lado] - 3.4, Y(db) - 3.4, xs[lado] + 3.4, Y(db) + 3.4, col, 1.5)
                s.linea(xs[lado] - 3.4, Y(db) + 3.4, xs[lado] + 3.4, Y(db) - 3.4, col, 1.5)
    s.texto(x0 + 4, y0 + alto / 2, 'dB HL', E.T_CHICO, E.TENUE,
            extra=f'transform="rotate(-90 {x0 - 14} {y0 + alto / 2:.1f})"')
    return ancho + 50


def dibujar(caso):
    aerea = por_oido(caso['Aerea'])
    estudiados = oidos_estudiados(caso)
    fdata = caso.get('Fowler') or {}
    patrones = fdata.get('patterns') if isinstance(fdata, dict) and fdata.get('enabled') else {}
    patrones = patrones if isinstance(patrones, dict) else {}
    escaleras = []
    for k, patron in sorted(patrones.items(), key=lambda kv: int(kv[0])):
        f = FRECUENCIAS[int(k)]
        th = {l: _num(aerea[l][int(k)]) for l in ('OD', 'OI')}
        if None in th.values() or patron not in CORTES:
            continue
        lado_est = 'OD' if th['OD'] > th['OI'] else 'OI'
        escaleras.append((f, th, lado_est, patron))
    escaleras = escaleras[:2]
    alto, y0 = 150, 40
    s = Svg(800, y0 + alto + 30)
    x = 20
    for f, th, lado_est, patron in escaleras:
        x += _escalera(s, x, y0, alto, f, th, lado_est, patron)
    # datos por oído
    x0 = x + 20
    y = 20
    s.texto(x0, y, 'Supraliminares', E.T_TITULO, E.TINTA, 'start', 700)
    y += 20
    sisi = caso.get('SISI') or [0, 0]
    carhart = caso.get('Carhart') or []
    reflejo = (caso.get('Reflex') or {}).get('ipsi') or []
    decay = ((caso.get('Reflex') or {}).get('decay') or {})
    cols = [x0 + 150 + k * 44 for k in range(4)]
    lado_a_lado = not escaleras and len(estudiados) == 2
    y_ini, base = y, x0
    for n_oido, lado in enumerate(estudiados):
        i = 0 if lado == 'OD' else 1
        if lado_a_lado and n_oido == 1:
            x0, y = base + 420, y_ini
        cols = [x0 + 150 + k * 44 for k in range(4)]
        s.texto(x0, y, lado, E.T_TITULO + 1, E.COLOR_LADO[lado], 'start', 700)
        y += 17
        s.texto(x0 + 6, y, 'SISI (1 kHz)', E.T_TITULO, E.TENUE, 'start', 600)
        s.texto(cols[0], y, f'{sisi[i]:.0f} %', E.T_TITULO, E.TINTA, 'end')
        y += 16
        for k, f in enumerate(CARHART_F):
            s.texto(cols[k], y, _hz(f).replace(' kHz', ' k').replace(' Hz', ''), E.T_CHICO, E.TENUE, 'end')
        y += 13
        s.texto(x0 + 6, y, 'Carhart', E.T_TITULO, E.TENUE, 'start', 600)
        for k, c in enumerate(carhart[:4]):
            s.texto(cols[k], y, f'{c[i]:.0f}', E.T_TITULO, E.TINTA, 'end')
        s.texto(cols[3] + 10, y, 'dB de deterioro en 60 s', E.T_CHICO, E.TENUE, 'start')
        y += 16
        s.texto(x0 + 6, y, 'Metz', E.T_TITULO, E.TENUE, 'start', 600)
        hay_reflejo = False
        for k, (f, r) in enumerate(zip(REFLEJO_F, reflejo)):
            umbral = _num(aerea[lado][FRECUENCIAS.index(f)])
            if r[i] >= AUSENTE or umbral is None:
                val = 'aus.'
            else:
                val, hay_reflejo = f'{r[i] - umbral:.0f}', True
            s.texto(cols[k], y, val, E.T_TITULO, E.TINTA, 'end')
        s.texto(cols[3] + 10, y, 'reflejo − umbral (dB)', E.T_CHICO, E.TENUE, 'start')
        y += 16
        s.texto(x0 + 6, y, 'Decay del reflejo', E.T_TITULO, E.TENUE, 'start', 600)
        s.texto(cols[1], y, ('positivo' if decay.get(lado.lower()) else 'negativo') if hay_reflejo else '—',
                E.T_TITULO, E.TINTA, 'start')
        y += 20
    s.alto = max(y0 + alto + 30, y + 4) if escaleras else y + 4
    s.ancho = cols[3] + 150
    return s.svg()
