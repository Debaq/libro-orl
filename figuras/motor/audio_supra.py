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


def dibujar(caso, diapasones=True, sin_enmascarar=False):
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
    # sin_enmascarar: lo que anota quien no enmascara (curva sombra, logo sin
    # ruido, sin supraliminares), para ponerlo sobre la hoja enmascarada
    if sin_enmascarar:
        fw = []
    aud = A.dibujar(caso, combinado=True, fowler=fw, clinico=True, sin_enmascarar=sin_enmascarar)
    w = float(re.search(r'width="([\d.]+)"', aud)[1])
    h = float(re.search(r'height="([\d.]+)"', aud)[1])
    interior = re.sub(r'^<svg[^>]*>|</svg>\s*$', '', aud.strip())
    interior = re.sub(r'<metadata.*?</metadata>', '', interior, flags=re.S)
    K = 1.3                                       # el audiograma toma más espacio que el panel
    interior = f'<g transform="scale({K})">{interior}</g>'
    w, h = w * K, h * K
    curvas = logo.curvas(caso, not sin_enmascarar)
    aerea, osea = por_oido(caso['Aerea']), por_oido(caso['Osea'])
    otro = {'OD': 'OI', 'OI': 'OD'}
    # Bajo 6 años no se hacen diapasones, logoaudiometría ni supraliminares:
    # la hoja queda con el audiograma (cap. 10, Adrián de 3 años)
    try:
        nino = float(caso.get('edad')) < 6
    except (TypeError, ValueError):
        nino = False
    if nino:
        diapasones = False
    # Un oído que no responde o con pérdida profunda (1 kHz sobre 100 dB) no
    # tiene supraliminares ni logo medible: no se le inventan (cófosis, cap. 7)
    def sin_reserva(lado):
        v = A._num(aerea[lado][A.FRECUENCIAS.index(1000)])
        return v is None or v > 100
    estudiados = [] if (sin_enmascarar or nino) else [l for l in SP.oidos_estudiados(caso) if not sin_reserva(l)]

    def ptp_oseo(lado):
        v = [A._num(x) for f, x in zip(A.FRECUENCIAS, osea[lado]) if f in (500, 1000, 2000)]
        v = [x for x in v if x is not None]
        return sum(v) / len(v) if v else 0.0

    out = []
    TT, TR, TC = 9, 7.6, 6.4               # letra del panel, más chica que la del motor

    def t(x, y, txt, tam=TR, col=E.TINTA, peso=400, ancla='start'):
        out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{tam}" fill="{col}" font-weight="{peso}" '
                   f'text-anchor="{ancla}">{txt}</text>')

    def raya(y):
        out.append(f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x0 + ancho:.1f}" y2="{y:.1f}" stroke="{E.GRILLA_FUERTE}" stroke-width="0.8"/>')

    # Arriba, lado a lado para ahorrar alto (él, 2026-10-20): los diapasones
    # (en espejo: Weber y Rinne al centro, 500 Hz junto al centro y 1 kHz en
    # los extremos) y la logoaudiometría. Abajo, las supraliminares.
    x0, ancho = w + 14, 340
    c_et, c_od, c_oi = x0 + 2, x0 + 86, x0 + 204
    PASO = 24
    y_top = 22
    y = y_top
    if diapasones:
        rinne = caso.get('Rinne') or {}
        weber = caso.get('Weber') or {}
        dcx = x0 + 56
        pos = {('od', '1000'): dcx - 48, ('od', '500'): dcx - 28, ('oi', '500'): dcx + 28, ('oi', '1000'): dcx + 48}
        t(dcx, y, 'Diapasones', TT, E.TINTA, 700, 'middle')
        y += 18
        t(dcx - 38, y, 'OD', TR, E.OD, 700, 'middle')
        t(dcx + 38, y, 'OI', TR, E.OI, 700, 'middle')
        y += 11
        for (lado, f), x in pos.items():
            t(x, y, '1k' if f == '1000' else '500', TC, E.TENUE, 400, 'middle')
        y += 16
        t(dcx, y, 'Weber', TR, E.TENUE, 600, 'middle')
        for (lado, f), x in pos.items():
            if str(weber.get(f, '')).lower() in (lado, 'centrado'):
                signo, col = (-1, E.OD) if lado == 'od' else (1, E.OI)
                ym = y - 4
                x0_, x1_ = x - signo * 6, x + signo * 6
                out.append(f'<path d="M{x0_:.1f},{ym:.1f} L{x1_:.1f},{ym:.1f} M{x1_ - signo * 3.5:.1f},{ym - 3:.1f} '
                           f'L{x1_:.1f},{ym:.1f} L{x1_ - signo * 3.5:.1f},{ym + 3:.1f}" fill="none" stroke="{col}" '
                           f'stroke-width="1.3"/>')
        y += 16
        t(dcx, y, 'Rinne', TR, E.TENUE, 600, 'middle')
        for (lado, f), x in pos.items():
            v = str((rinne.get(f) or {}).get(lado, '')).lower()
            t(x, y, {'positivo': '(+)', 'negativo': '(−)', 'falso_negativo': '(−*)'}.get(v, '—'),
              TR, E.TINTA, 600, 'middle')
    y_dia = y
    # --- logoaudiometría, a la derecha de los diapasones
    lx = x0 + 132 if diapasones else x0
    l_et, l_od, l_oi = lx, lx + 26, lx + 112
    if nino:
        y = y_dia
    else:
        y = y_top
        t(lx, y, 'Logoaudiometría', TT, E.TINTA, 700)
        y += 18
        t(l_od, y, 'OD', TR, E.OD, 700)
        t(l_oi, y, 'OI', TR, E.OI, 700)
        y += 15
        mejores = {}
        for i, lado in enumerate(('OD', 'OI')):
            # solo niveles que se presentan: desde el SDT hacia arriba
            piso = caso['SDT'][0 if lado == 'OD' else 1]
            piso = piso if isinstance(piso, (int, float)) else 0
            pts = {db: p for db, p in curvas[lado] if db % 10 == 0 and db >= piso}
            mejores[lado] = sorted(sorted(pts.items(), key=lambda dp: (-dp[1], dp[0]))[:3])
        for et, k in (('SDT', 'SDT'), ('SRT', 'SRT')):
            t(l_et, y, et, TR, E.TENUE, 600)
            for i, (lado, c) in enumerate((('OD', l_od), ('OI', l_oi))):
                v = caso[k][i]
                if v is None or v >= 120:
                    t(c, y, 'no responde', TR, E.TENUE)
                    continue
                if sin_enmascarar:      # sin ruido, el oído peor contesta por el mejor (45 dB de atenuación)
                    v = min(v, caso[k][1 - i] + 45)
                t(c, y, nivel_logo(lado, v, None if sin_enmascarar else ruido_logo(caso, lado, v), color=True))
            y += 12
        t(l_et, y, 'UMD', TR, E.TENUE, 600)
        for n in range(3):
            for lado, c in (('OD', l_od), ('OI', l_oi)):
                if sin_reserva(lado):
                    if n == 0:
                        t(c, y, '—')
                    continue
                if n < len(mejores[lado]):
                    db, p = mejores[lado][n]
                    t(c, y, f'{p:.0f} % a ' + nivel_logo(lado, db, None if sin_enmascarar else ruido_logo(caso, lado, db),
                                                          color=True))
            y += 11
    y = max(y, y_dia)
    if diapasones:
        out.append(f'<line x1="{lx - 12:.1f}" y1="{y_top - 10:.1f}" x2="{lx - 12:.1f}" y2="{y - 6:.1f}" '
                   f'stroke="{E.GRILLA_FUERTE}" stroke-width="0.8"/>')
    y += 6
    y += 10
    if estudiados:
        # --- supraliminares
        t(x0, y, 'Supraliminares', TT, E.TINTA, 700)
        t(c_od, y, 'OD', TR, E.OD, 700)
        t(c_oi, y, 'OI', TR, E.OI, 700)
        y += 6
        raya(y)
        y += 12
        sisi = caso.get('SISI') or [0, 0]
        carhart = caso.get('Carhart') or []
        reflejo = (caso.get('Reflex') or {}).get('ipsi') or []
        decay = (caso.get('Reflex') or {}).get('decay') or {}
        fowler_lado = {}
        for f, lado, patron, _ in fw:
            fowler_lado.setdefault(lado, {}).setdefault(SP.NOMBRE[patron], []).append(SP._hz(f))

        def celda(lado, valor):
            return valor if lado in estudiados else '—'
        t(c_et, y, 'SISI (1 kHz)', TR, E.TENUE, 600)
        for i, (lado, c) in enumerate((('OD', c_od), ('OI', c_oi))):
            t(c, y, celda(lado, f'{sisi[i]:.0f} %'))
        y += 12
        # El Fowler no se repite aquí: está en el audiograma. Solo la nota de diploacusia.
        diplo = bool((caso.get('Fowler') or {}).get('diplacusia')) if isinstance(caso.get('Fowler'), dict) else False
        if diplo and fowler_lado:
            for lado in fowler_lado:
                t(c_od if lado == 'OD' else c_oi, y, 'Nota: refiere diploacusia en el Fowler.', TC, E.TINTA_2, 600)
            y += 12
        y += 8
        # Carhart en 2 y 4 kHz, desde el umbral (él, 2026-10-20): "No det." si
        # sostiene el tono el minuto al nivel de partida; si no, "Det. N dB", lo
        # que hubo que subir para que lo sostuviera.
        t(c_et, y, 'Carhart', TR, E.TENUE, 600)
        for i, (lado, c) in enumerate((('OD', c_od), ('OI', c_oi))):
            if lado not in estudiados:
                t(c, y, '—')
                continue
            for n, (k, f) in enumerate(((2, 2000), (3, 4000))):
                u = A._num(aerea[lado][A.FRECUENCIAS.index(f)])
                d = carhart[k][i] if k < len(carhart) else 0
                res = 'No det.' if d <= 5 else f'Det. {d:.0f} dB'      # 5 dB o menos: no deteriora (él)
                if u is None or u >= 110:                            # sin margen para presentar el tono
                    t(c, y + n * 12, f'{f // 1000} kHz:', TC, E.TENUE)
                    t(c + 54, y + n * 12, '—', TR, E.TINTA)
                    continue
                t(c, y + n * 12, f'{f // 1000} kHz a {u:.0f} dB:', TC, E.TENUE)
                t(c + 54, y + n * 12, res, TR, E.TINTA, 600 if d > 0 else 400)
        y += 30
        # Metz por frecuencia
        for lado, c in (('OD', c_od), ('OI', c_oi)):
            if lado not in estudiados:
                continue
            for k, f in enumerate(SP.REFLEJO_F):
                t(c + 14 + k * PASO, y, SP._hz(f).replace(' kHz', 'k').replace(' Hz', ''), TC, E.TENUE, 400, 'end')
        y += 11
        t(c_et, y, 'Metz (dB)', TR, E.TENUE, 600)
        hay = {}
        for i, (lado, c) in enumerate((('OD', c_od), ('OI', c_oi))):
            if lado not in estudiados:
                t(c, y, '—')
                continue
            for k, (f, r) in enumerate(zip(SP.REFLEJO_F, reflejo)):
                u = A._num(aerea[lado][A.FRECUENCIAS.index(f)])
                # el reflejo está en dB SPL: se pasa a dB HL con la corrección de la
                # sonda (H7: 5,5, 0, 3 y 5,5 dB) antes de restar el umbral
                corr = {500: 5.5, 1000: 0, 2000: 3, 4000: 5.5}[f]
                v = 'aus.' if r[i] >= SP.AUSENTE or u is None else f'{r[i] - corr - u:g}'.replace('.', ',')
                hay[lado] = hay.get(lado, False) or v != 'aus.'
                t(c + 14 + k * PASO, y, v, TR, E.TINTA, 400, 'end')
        y += 12
        t(c_et, y, 'Decay del reflejo', TR, E.TENUE, 600)
        for lado, c in (('OD', c_od), ('OI', c_oi)):
            if lado not in estudiados or not hay.get(lado):
                t(c, y, '—')
            else:
                t(c, y, 'positivo' if decay.get(lado.lower()) else 'negativo')
        y += 18
    if not nino:
        t(x0, y, 'Sin enmascarar. UMD: tres mejores intentos.' if sin_enmascarar else
          'Voz/ruido de habla en el otro oído. UMD: tres mejores intentos.', TC, E.TENUE)
    if estudiados:
        y += 12
        t(x0, y, 'Carhart desde el umbral, 1 minuto. Metz: reflejo (en dB HL) − umbral.', TC, E.TENUE)
    W, H = x0 + ancho + 6, max(h, y + 10)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'font-family="{E.FUENTE}">{interior}{"".join(out)}</svg>')
