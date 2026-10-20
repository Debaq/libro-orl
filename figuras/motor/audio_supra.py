"""Hoja auditiva de los casos vestibulares (él, 2026-10-20): un generador
aparte, para no tocar los audiogramas del resto del libro.

A la izquierda, el audiograma clínico (audiograma.dibujar con clinico=True):
frecuencias arriba, ósea completa de 250 a 4.000 Hz si una frecuencia la pide,
rótulo "LDL:" y el Fowler sobre la línea de la frecuencia estudiada, con
"Fowler (+)" o "Fowler (−)" arriba. A la derecha, una tabla OD | OI:

- Logoaudiometría: SDT, SRT y UMD (tres mejores intentos). Toda intensidad va
  en el color del oído estimulado; con ruido, "80 dB/60 dB", el ruido en el
  color del otro oído. Aquí se enmascara cuando la voz pasa de 45 dB.
- Supraliminares, solo si algún oído tiene pérdida sensorioneural: SISI,
  Carhart en 2 y 4 kHz desde el umbral ("No det." o "Det. N dB"), Metz y decay
  del reflejo. El Fowler no se repite: está en el audiograma.
"""
import math

from . import audiograma as A
from . import estilo as E
from . import logo, supraliminares as SP
from .datos import por_oido


def _ptp(valores):
    v = [A._num(x) for f, x in zip(A.FRECUENCIAS, valores) if f in (500, 1000, 2000)]
    v = [x for x in v if x is not None]
    return sum(v) / len(v) if v else 0.0


def ruido_logo(caso, lado, voz):
    """Nivel de ruido de habla en el oído contrario para la voz a `voz` dB, o
    None si no hace falta: se enmascara cuando la voz pasa de 45 dB (él,
    2026-10-20).
    Mínimo = voz − 45 − PTP óseo NE + PTP aéreo NE; se usa el mínimo + 10, sin
    pasar el máximo (PTP óseo del evaluado + 45); de 5 en 5."""
    otro = 'OI' if lado == 'OD' else 'OD'
    aerea, osea = por_oido(caso['Aerea']), por_oido(caso['Osea'])
    if voz <= 45:
        return None
    minimo = voz - 45 - _ptp(osea[otro]) + _ptp(aerea[otro])
    maximo = _ptp(osea[lado]) + 45
    return int(round(min(minimo + 10, max(maximo, minimo)) / 5) * 5)


def nivel_logo(lado, voz, ruido, color=False):
    """'60 dB' o '60 dB/20 dB': la voz en el color del oído estimulado y el
    ruido en el del contrario (tspans para meter dentro de un <text>).
    color=True: la voz va en color aunque no haya ruido (todas las intensidades
    de la logo: SDT, SRT y UMD, él, 2026-10-20)."""
    otro = 'OI' if lado == 'OD' else 'OD'
    if ruido is None:
        return (f'<tspan fill="{E.COLOR_LADO[lado]}" font-weight="600">{voz} dB</tspan>' if color
                else f'{voz} dB')
    return (f'<tspan fill="{E.COLOR_LADO[lado]}" font-weight="600">{voz} dB</tspan>'
            f'/<tspan fill="{E.COLOR_LADO[otro]}" font-weight="600">{ruido} dB</tspan>')


def dibujar(caso):
    """Audiograma combinado con el Fowler sobre la frecuencia estudiada y, a la
    derecha, una tabla con las dos columnas de oídos: logoaudiometría (SDT,
    SRT, UMD con los tres mejores intentos) y supraliminares (SISI, Carhart,
    Metz y decay del reflejo; el Fowler va en el audiograma) de los oídos con pérdida
    sensorioneural. Lo que no se hace en un oído queda en "—"."""
    import re
    fw = SP.fowler(caso)
    # en el audiograma, hasta dos frecuencias a dos octavas o más (si no, las escaleras se montan)
    en_audio = []
    for item in fw:
        if len(en_audio) < 2 and all(abs(math.log2(item[0] / otro_[0])) >= 2 for otro_ in en_audio):
            en_audio.append(item)
    fw = en_audio
    aud = A.dibujar(caso, combinado=True, fowler=fw, clinico=True)
    w = float(re.search(r'width="([\d.]+)"', aud)[1])
    h = float(re.search(r'height="([\d.]+)"', aud)[1])
    interior = re.sub(r'^<svg[^>]*>|</svg>\s*$', '', aud.strip())
    interior = re.sub(r'<metadata.*?</metadata>', '', interior, flags=re.S)
    curvas = logo.curvas(caso, True)
    aerea, osea = por_oido(caso['Aerea']), por_oido(caso['Osea'])
    otro = {'OD': 'OI', 'OI': 'OD'}
    estudiados = SP.oidos_estudiados(caso)

    def ptp_oseo(lado):
        v = [A._num(x) for f, x in zip(A.FRECUENCIAS, osea[lado]) if f in (500, 1000, 2000)]
        v = [x for x in v if x is not None]
        return sum(v) / len(v) if v else 0.0

    out = []

    def t(x, y, txt, tam=E.T_ROTULO, col=E.TINTA, peso=400, ancla='start'):
        out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{tam}" fill="{col}" font-weight="{peso}" '
                   f'text-anchor="{ancla}">{txt}</text>')

    def raya(y):
        out.append(f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x0 + ancho:.1f}" y2="{y:.1f}" stroke="{E.GRILLA_FUERTE}" stroke-width="0.8"/>')

    x0, ancho = w + 20, 360
    c_et, c_od, c_oi = x0 + 4, x0 + 112, x0 + 240
    PASO = 30
    y = 22
    t(c_od, y, 'OD', E.T_TITULO, E.OD, 700)
    t(c_oi, y, 'OI', E.T_TITULO, E.OI, 700)
    # --- logoaudiometría
    y += 20
    t(x0, y, 'Logoaudiometría', E.T_TITULO, E.TINTA, 700)
    y += 6
    raya(y)
    y += 14
    mejores = {}
    for i, lado in enumerate(('OD', 'OI')):
        pts = {db: p for db, p in curvas[lado] if db % 10 == 0}
        mejores[lado] = sorted(sorted(pts.items(), key=lambda dp: (-dp[1], dp[0]))[:3])
    for et, k in (('SDT', 'SDT'), ('SRT', 'SRT')):
        t(c_et, y, et, E.T_ROTULO, E.TENUE, 600)
        for i, (lado, c) in enumerate((('OD', c_od), ('OI', c_oi))):
            v = caso[k][i]
            t(c, y, nivel_logo(lado, v, ruido_logo(caso, lado, v), color=True))
        y += 14
    t(c_et, y, 'UMD', E.T_ROTULO, E.TENUE, 600)
    for n in range(3):
        for lado, c in (('OD', c_od), ('OI', c_oi)):
            if n < len(mejores[lado]):
                db, p = mejores[lado][n]
                t(c, y, f'{p:.0f} % a ' + nivel_logo(lado, db, ruido_logo(caso, lado, db), color=True))
        y += 13
    y += 10
    if estudiados:
        # --- supraliminares
        t(x0, y, 'Supraliminares', E.T_TITULO, E.TINTA, 700)
        y += 6
        raya(y)
        y += 14
        sisi = caso.get('SISI') or [0, 0]
        carhart = caso.get('Carhart') or []
        reflejo = (caso.get('Reflex') or {}).get('ipsi') or []
        decay = (caso.get('Reflex') or {}).get('decay') or {}
        fowler_lado = {}
        for f, lado, patron, _ in fw:
            fowler_lado.setdefault(lado, {}).setdefault(SP.NOMBRE[patron], []).append(SP._hz(f))

        def celda(lado, valor):
            return valor if lado in estudiados else '—'
        t(c_et, y, 'SISI (1 kHz)', E.T_ROTULO, E.TENUE, 600)
        for i, (lado, c) in enumerate((('OD', c_od), ('OI', c_oi))):
            t(c, y, celda(lado, f'{sisi[i]:.0f} %'))
        y += 14
        # El Fowler no se repite aquí: está en el audiograma. Solo la nota de diploacusia.
        diplo = bool((caso.get('Fowler') or {}).get('diplacusia')) if isinstance(caso.get('Fowler'), dict) else False
        if diplo and fowler_lado:
            for lado in fowler_lado:
                t(c_od if lado == 'OD' else c_oi, y, 'Nota: refiere diploacusia en el Fowler.', E.T_CHICO, E.TINTA_2, 600)
            y += 14
        y += 8
        # Carhart en 2 y 4 kHz, desde el umbral (él, 2026-10-20): "No det." si
        # sostiene el tono el minuto al nivel de partida; si no, "Det. N dB", lo
        # que hubo que subir para que lo sostuviera.
        t(c_et, y, 'Carhart', E.T_ROTULO, E.TENUE, 600)
        for i, (lado, c) in enumerate((('OD', c_od), ('OI', c_oi))):
            if lado not in estudiados:
                t(c, y, '—')
                continue
            for n, (k, f) in enumerate(((2, 2000), (3, 4000))):
                u = A._num(aerea[lado][A.FRECUENCIAS.index(f)])
                d = carhart[k][i] if k < len(carhart) else 0
                res = 'No det.' if d <= 5 else f'Det. {d:.0f} dB'      # 5 dB o menos: no deteriora (él)
                t(c, y + n * 13, f'{f // 1000} kHz a {u:.0f} dB:', E.T_CHICO, E.TENUE)
                t(c + 66, y + n * 13, res, E.T_ROTULO, E.TINTA, 600 if d > 0 else 400)
        y += 30
        # Metz por frecuencia
        for lado, c in (('OD', c_od), ('OI', c_oi)):
            if lado not in estudiados:
                continue
            for k, f in enumerate(SP.REFLEJO_F):
                t(c + 14 + k * PASO, y, SP._hz(f).replace(' kHz', 'k').replace(' Hz', ''), E.T_CHICO, E.TENUE, 400, 'end')
        y += 13
        t(c_et, y, 'Metz (dB)', E.T_ROTULO, E.TENUE, 600)
        hay = {}
        for i, (lado, c) in enumerate((('OD', c_od), ('OI', c_oi))):
            if lado not in estudiados:
                t(c, y, '—')
                continue
            for k, (f, r) in enumerate(zip(SP.REFLEJO_F, reflejo)):
                u = A._num(aerea[lado][A.FRECUENCIAS.index(f)])
                v = 'aus.' if r[i] >= SP.AUSENTE or u is None else f'{r[i] - u:.0f}'
                hay[lado] = hay.get(lado, False) or v != 'aus.'
                t(c + 14 + k * PASO, y, v, E.T_ROTULO, E.TINTA, 400, 'end')
        y += 14
        t(c_et, y, 'Decay del reflejo', E.T_ROTULO, E.TENUE, 600)
        for lado, c in (('OD', c_od), ('OI', c_oi)):
            if lado not in estudiados or not hay.get(lado):
                t(c, y, '—')
            else:
                t(c, y, 'positivo' if decay.get(lado.lower()) else 'negativo')
        y += 18
    t(x0, y, 'Voz/ruido de habla en el otro oído. UMD: tres mejores intentos.', E.T_CHICO, E.TENUE)
    if estudiados:
        y += 12
        t(x0, y, 'Carhart desde el umbral, 1 minuto. Metz: reflejo − umbral.', E.T_CHICO, E.TENUE)
    W, H = x0 + ancho + 6, max(h, y + 10)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'font-family="{E.FUENTE}">{interior}{"".join(out)}</svg>')
