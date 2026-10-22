"""Hoja de impedanciometría de los casos del tomo II (él, 2026-10-20).

A la izquierda, un solo timpanograma con las dos curvas (OD rojo, OI azul) y,
debajo, sus datos en dos columnas: tipo, volumen, compliancia, presión y
gradiente. A la derecha, la tabla de reflejos (ipsilateral y contralateral por
sonda, 500 a 4.000 Hz y NBN, en dB SPL), el decay del reflejo y la función
tubaria. Los datos son los del caso de LabSim (impedancia._curva y Reflex).
"""
from . import estilo as E
from .impedancia import FRECS_REFLEJO, NO_REALIZABLE, ROTULO_FRECS, SIN_REFLEJO, _curva, _dapa, _dec, _f, _ml
from .svg import Svg, borde_derecho

# Letra (él, 2026-10-21): todo en negro y sin rótulos más chicos, para que
# impresa no baje de 7 pt; el panel de la derecha crece hasta el alto del
# timpanograma, como en la hoja auditiva (audio_supra.py).
TT, TR = 8.4, 7
ANCHO_PANEL = 225


def dibujar(caso, escala_ml=2.0, sonda=226):
    pw, ph = 190, 160
    ml, mt, md, mb = 34, 26, 10, 26
    x_min, x_max = -400, 200
    s = Svg(ml + pw + md, mt + ph + mb)

    def X(p):
        return ml + (p - x_min) / (x_max - x_min) * pw

    def Y(v):
        return mt + ph - max(0.0, min(escala_ml, v)) / escala_ml * ph

    # --- timpanograma: una grilla, las dos curvas
    s.texto(ml, 14, f"Timpanograma {'1.000' if str(sonda) == '1000' else '226'} Hz", TT, E.TINTA, 'start', 700)
    for p in range(x_min, x_max + 1, 100):
        s.linea(X(p), mt, X(p), mt + ph, E.GRILLA_FUERTE if p == 0 else E.GRILLA, 1)
        s.texto(X(p), mt + ph + 11, p, TR, E.TINTA)
    s.texto(ml + pw / 2, mt + ph + 23, 'Presión (daPa)', TR, E.TINTA)
    for i in range(0, int(escala_ml * 10) + 1, 5):
        v = i / 10
        s.linea(ml, Y(v), ml + pw, Y(v), E.GRILLA, 1 if i % 10 == 0 else 0.5)
        s.texto(ml - 5, Y(v) + 3, f'{v:.1f}'.replace('.', ','), TR, E.TINTA, 'end')
    s.texto(9, mt + ph / 2, 'mL', TR, E.TINTA, extra=f'transform="rotate(-90 9 {mt + ph / 2:.1f})"')
    datos = {}
    for lado in ('OD', 'OI'):
        col = E.COLOR_LADO[lado]
        if caso.get(f'Z_{lado}') == NO_REALIZABLE:
            datos[lado] = None
            continue
        d = _curva(caso, lado, sonda)
        datos[lado] = d
        if d is None:
            continue
        pts = [(X(px), Y(py)) for px, py in sorted(zip(d['x'], d['y'])) if x_min <= px <= x_max]
        s.trazo(pts, col, E.LINEA)
    # en cada esquina, el oído y su curva: OD arriba a la izquierda, OI a la derecha
    for lado, x, ancla in (('OD', ml + 5, 'start'), ('OI', ml + pw - 5, 'end')):
        # la letra de la sonda que se usó (con 1.000 Hz no es la de 226)
        letra = (datos.get(lado) or {}).get('letra') or caso.get(f'Z_{lado}')
        txt = f'{lado} no realizable' if letra == NO_REALIZABLE else f'{lado} curva {letra}' if letra else lado
        s.texto(x, mt + 11, txt, TR, E.COLOR_LADO[lado], ancla, 700)

    # --- a la derecha, en su propio sistema (x desde 0): datos, reflejos y
    # otras pruebas. G multiplica los saltos de línea, para llenar el alto.
    def panel(G=1.0):
        q = Svg(0, 0)
        x0 = 0
        y = 14
        c_et, c_od, c_oi = x0, x0 + 90, x0 + 168
        q.texto(c_od, y, 'OD', TR, E.OD, 'start', 700)
        q.texto(c_oi, y, 'OI', TR, E.OI, 'start', 700)
        filas = [('Volumen', lambda l, d: _ml(d['volumen'])),
                 ('Compliancia', lambda l, d: _ml(d['compliancia'])),
                 ('Presión', lambda l, d: 'sin pico' if (_f(d['compliancia']) or 0) < 0.05 else _dapa(d['presion'])),
                 ('Gradiente', lambda l, d: '—' if (_f(d['compliancia']) or 0) < 0.05 else _dec(d['gradiente']))]
        for et, fn in filas:
            y += 12 * G
            q.texto(c_et, y, et, TR, E.TINTA, 'start', 600)
            for lado, c in (('OD', c_od), ('OI', c_oi)):
                d = datos.get(lado)
                if caso.get(f'Z_{lado}') == NO_REALIZABLE:
                    # la sonda no va en ese oído (H7): se dice una vez, en la primera fila
                    val = 'no realizable' if et == filas[0][0] else ''
                else:
                    val = fn(lado, d) if (d or et == 'Tipo') else '—'
                q.texto(c, y, val, TR, E.TINTA, 'start', 600 if et == 'Tipo' else 400)

        # --- reflejos: por sonda; en el contralateral el tono entra por el otro oído
        y += 24 * G
        q.texto(x0, y, 'Reflejo estapedial (dB SPL)', TT, E.TINTA, 'start', 700)
        cw = 27
        xc = [x0 + 92 + k * cw for k in range(len(FRECS_REFLEJO))]
        y += 16 * G
        for x, f in zip(xc, ROTULO_FRECS):
            q.texto(x, y, f, TR, E.TINTA, 'middle')
        r = caso.get('Reflex') if isinstance(caso.get('Reflex'), dict) else {}
        # Por sonda (él, 2026-10-20): con la sonda en un oído se mide su ipsi y,
        # sin moverla, su contra (el tono entra por el otro oído). La sonda va sin
        # color; cada fila, en el color del oído que recibe el tono: el ipsi de la
        # sonda OD en rojo y su contra en azul. Sin reflejo, N/D.
        for j, lado in enumerate(('OD', 'OI')):
            otro = 'OI' if lado == 'OD' else 'OD'
            q.linea(x0, y + 4, xc[-1] + 14, y + 4, E.GRILLA, 0.8)
            for modo, nombre in (('ipsi', 'Ipsi'), ('contra', 'Contra')):
                datos_r = r.get(modo) or []
                y += 14 * G
                col = E.COLOR_LADO[lado if modo == 'ipsi' else otro]
                q.texto(x0, y, f'Sonda {lado}' if modo == 'ipsi' else '', TR, E.TINTA, 'start', 700)
                q.texto(x0 + 50, y, nombre, TR, col, 'start', 600)
                nr = NO_REALIZABLE in (caso.get(f'Z_{lado}'), caso.get(f'Z_{lado if modo == "ipsi" else otro}'))
                for k, x in enumerate(xc):
                    try:
                        v = float(datos_r[k][j])
                    except (IndexError, TypeError, ValueError):
                        v = None
                    if nr:
                        txt, peso = 'NR', 400
                    elif v is None:
                        txt, peso = '·', 400
                    elif v >= SIN_REFLEJO:
                        txt, peso = 'N/D', 400
                    else:
                        txt, peso = f'{v:g}', 600
                    q.texto(x, y, txt, TR, col, 'middle', peso)
        # --- otras pruebas
        y += 10 * G
        decay = r.get('decay') or {}
        etf = caso.get('ETF') or ['', '']

        def hay_reflejo(i):
            # el decay se mide con el ipsilateral de esa sonda; sin reflejo no hay decay
            try:
                return any(float(v[i]) < SIN_REFLEJO for v in (r.get('ipsi') or []))
            except (TypeError, ValueError, IndexError):
                return False
        otras = [('Decay del reflejo', lambda i, l: ('positivo' if decay.get(l.lower()) else 'negativo')
                  if hay_reflejo(i) else '—'),
                 ('Función tubaria', lambda i, l: str(etf[i]) if i < len(etf) and etf[i] else '—')]
        for et, fn in otras:
            y += 13 * G
            q.texto(x0, y, et, TR, E.TINTA, 'start', 600)
            for i, (lado, c) in enumerate((('OD', c_od), ('OI', c_oi))):
                nr = caso.get(f'Z_{lado}') == NO_REALIZABLE
                q.texto(c, y, 'no realizable' if nr else fn(i, lado), TR, E.TINTA)
        return q.partes, y

    # El panel llena el alto del timpanograma con ancho fijo (como en la hoja
    # auditiva): la letra crece hasta ese ancho o ese alto y, si sobra alto,
    # crecen los espacios entre líneas.
    ARRIBA, MARGEN = 14 - TT * 0.8, 3
    alto_util = s.alto - 2 * MARGEN
    partes, y1 = panel(1.0)
    ancho_nat = max(borde_derecho(partes), 1)
    k = min(ANCHO_PANEL / ancho_nat, alto_util / (y1 + 3 - ARRIBA))
    _, y2 = panel(2.0)
    a, b = (y1 + 3 - ARRIBA) - (y2 - y1), (y2 - y1)
    G = max(1.0, min(1.8, (alto_util / k - a) / b)) if b > 0 else 1.0
    partes, _ = panel(G)
    x_panel = s.ancho + 8
    s.crudo(f'<g transform="translate({x_panel:.1f},{MARGEN - ARRIBA * k:.1f}) scale({k:.3f})">'
            + ''.join(partes) + '</g>')
    s.ancho = x_panel + ANCHO_PANEL + 2
    return s.svg()
