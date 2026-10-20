"""Hoja de impedanciometría de los casos del tomo II (él, 2026-10-20).

A la izquierda, un solo timpanograma con las dos curvas (OD rojo, OI azul) y,
debajo, sus datos en dos columnas: tipo, volumen, compliancia, presión y
gradiente. A la derecha, la tabla de reflejos (ipsilateral y contralateral por
sonda, 500 a 4.000 Hz y NBN, en dB SPL), el decay del reflejo y la función
tubaria. Los datos son los del caso de LabSim (impedancia._curva y Reflex).
"""
from . import estilo as E
from .impedancia import FRECS_REFLEJO, NO_REALIZABLE, ROTULO_FRECS, SIN_REFLEJO, _curva, _dapa, _dec, _f, _ml
from .svg import Svg

TT, TR, TC = 8.4, 7, 6


def dibujar(caso, escala_ml=2.0, sonda=226):
    pw, ph = 190, 160
    ml, mt = 40, 26
    x_min, x_max = -400, 200
    s = Svg(800, 300)

    def X(p):
        return ml + (p - x_min) / (x_max - x_min) * pw

    def Y(v):
        return mt + ph - max(0.0, min(escala_ml, v)) / escala_ml * ph

    # --- timpanograma: una grilla, las dos curvas
    s.texto(ml, 14, f"Timpanograma {'1.000' if str(sonda) == '1000' else '226'} Hz", TT, E.TINTA, 'start', 700)
    for p in range(x_min, x_max + 1, 100):
        s.linea(X(p), mt, X(p), mt + ph, E.GRILLA_FUERTE if p == 0 else E.GRILLA, 1)
        s.texto(X(p), mt + ph + 12, p, TC, E.TENUE)
    s.texto(ml + pw / 2, mt + ph + 23, 'Presión (daPa)', TC, E.TENUE)
    for i in range(0, int(escala_ml * 10) + 1, 5):
        v = i / 10
        s.linea(ml, Y(v), ml + pw, Y(v), E.GRILLA, 1 if i % 10 == 0 else 0.5)
        s.texto(ml - 6, Y(v) + 3, f'{v:.1f}'.replace('.', ','), TC, E.TENUE, 'end')
    s.texto(12, mt + ph / 2, 'mL', TC, E.TENUE, extra=f'transform="rotate(-90 12 {mt + ph / 2:.1f})"')
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
    # datos del timpanograma, a la derecha del gráfico, en dos columnas
    x0 = ml + pw + 24
    y = 14
    c_et, c_od, c_oi = x0, x0 + 100, x0 + 170
    s.texto(c_od, y, 'OD', TR, E.OD, 'start', 700)
    s.texto(c_oi, y, 'OI', TR, E.OI, 'start', 700)
    filas = [('Volumen', lambda l, d: _ml(d['volumen'])),
             ('Compliancia', lambda l, d: _ml(d['compliancia'])),
             ('Presión', lambda l, d: 'sin pico' if (_f(d['compliancia']) or 0) < 0.05 else _dapa(d['presion'])),
             ('Gradiente', lambda l, d: '—' if (_f(d['compliancia']) or 0) < 0.05 else _dec(d['gradiente']))]
    for et, fn in filas:
        y += 12
        s.texto(c_et, y, et, TR, E.TENUE, 'start', 600)
        for lado, c in (('OD', c_od), ('OI', c_oi)):
            d = datos.get(lado)
            if caso.get(f'Z_{lado}') == NO_REALIZABLE:
                val = 'no realizable' if et == 'Tipo' else ''
            else:
                val = fn(lado, d) if (d or et == 'Tipo') else '—'
            s.texto(c, y, val, TR, E.TINTA, 'start', 600 if et == 'Tipo' else 400)
    y_izq = mt + ph + 26

    # --- reflejos: por sonda; en el contralateral el tono entra por el otro oído
    y += 24
    s.texto(x0, y, 'Reflejo estapedial (dB SPL)', TT, E.TINTA, 'start', 700)
    cw = 27
    xc = [x0 + 100 + k * cw for k in range(len(FRECS_REFLEJO))]
    y += 16
    for x, f in zip(xc, ROTULO_FRECS):
        s.texto(x, y, f, TC, E.TENUE, 'middle')
    r = caso.get('Reflex') if isinstance(caso.get('Reflex'), dict) else {}
    # Por sonda (él, 2026-10-20): con la sonda en un oído se mide su ipsi y,
    # sin moverla, su contra (el tono entra por el otro oído). La sonda va sin
    # color; cada fila, en el color del oído que recibe el tono: el ipsi de la
    # sonda OD en rojo y su contra en azul. Sin reflejo, N/D.
    for j, lado in enumerate(('OD', 'OI')):
        otro = 'OI' if lado == 'OD' else 'OD'
        col = E.COLOR_LADO[lado]
        s.linea(x0, y + 4, xc[-1] + 18, y + 4, E.GRILLA, 0.8)
        for modo, nombre in (('ipsi', 'Ipsi'), ('contra', 'Contra')):
            datos_r = r.get(modo) or []
            y += 14
            col = E.COLOR_LADO[lado if modo == 'ipsi' else otro]
            s.texto(x0, y, f'Sonda {lado}' if modo == 'ipsi' else '', TR, E.TINTA, 'start', 700)
            s.texto(x0 + 52, y, nombre, TR, col, 'start', 600)
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
                s.texto(x, y, txt, TR, col, 'middle', peso)
    # --- otras pruebas
    y += 10
    decay = r.get('decay') or {}
    etf = caso.get('ETF') or ['', '']
    c1, c2 = c_od, c_oi

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
        y += 13
        s.texto(x0, y, et, TR, E.TENUE, 'start', 600)
        for i, (lado, c) in enumerate((('OD', c1), ('OI', c2))):
            s.texto(c, y, fn(i, lado), TR, E.TINTA)
    s.alto = max(y_izq, y) + 10
    s.ancho = xc[-1] + 30
    return s.svg()
