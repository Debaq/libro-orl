"""Electrococleografía con el generador y la marcación automática de la app.

ECochG_Curve con el protocolo estándar del equipo (abr.protocols:
click alternado, 90 dB, electrodo timpánico) y el mismo capture_id que usa
la ventana ("R1"/"L1"), que entra en la semilla. Las marcas y la razón PS/PA
salen de ecochg.auto_marks + measure_complex, el botón "marcar" del equipo:
el libro no mide nada por su cuenta.
"""
from . import estilo as E
from .datos import en_raiz
from .svg import Svg

# Como en el ABR (abr.SNR_ROTULO): no se marca sobre ruido. El marcado
# automático de la app encuentra un "PA" en casi cualquier trazo plano; un
# PA de menos de 0,1 µV o una razón negativa no son un complejo. Los PA
# reales de los casos del libro miden de 0,4 a 3 µV.
PA_MIN_UV = 0.1


def _hay_complejo(m):
    return (m.get('ap_amp') or 0) >= PA_MIN_UV and (m.get('sp_ap') or 0) >= 0


def registrar(caso, lado, nivel=90):
    import numpy as np
    from abr import ecochg
    from abr.ABR_generator import default_settings
    from abr.ECochG_generator import ECochG_Curve
    from abr.protocols import standard_setup
    with en_raiz():
        ctrl, tec = standard_setup('ECochG')
        tecnica = default_settings('ECochG')
        tecnica.update(tec)
        cs = dict(ctrl, side=lado, mkg=0, clamp=False)
        t, y, meta = ECochG_Curve(nivel, cs, caso['ABR'][lado], [1.0, ctrl['average']], done=True,
                                  patient=caso, capture_id='R1' if lado == 'OD' else 'L1', technical=tecnica)
        if meta.get('ecochg_sin_datos'):
            return None
        t, y = np.asarray(t, float), np.asarray(y, float)
        marcas = ecochg.auto_marks(t, y)
        con_y = {k: (v, float(np.interp(v, t, y))) for k, v in marcas.items()}
        medida = ecochg.measure_complex(t, y, con_y)
        # lo que se integra en cada área, de las mismas cuentas que la razón
        # de áreas (ecochg.area_shading): el área PS y, dentro, el área PA
        zonas = None
        try:
            sh = ecochg.area_shading(t, y, con_y)
            if sh:
                zonas = {k: (list(map(float, x)), list(map(float, yt))) for k, (x, _b, yt) in sh.items()}
        except Exception:
            zonas = None
    return {'t': t.tolist(), 'y': y.tolist(), 'marcas': marcas, 'medida': medida, 'nivel': nivel, 'zonas': zonas}


def dibujar(caso, oidos=('OD', 'OI'), nivel=90, ms_max=5.0):
    regs = {l: registrar(caso, l, nivel) for l in oidos}
    pw, ph, ml, mt, sep = 230, 150, 40, 30, 34
    s = Svg(ml + len(oidos) * pw + (len(oidos) - 1) * sep + 12, mt + ph + 66)
    todos = [v for r in regs.values() if r for t, v in zip(r['t'], r['y']) if t <= ms_max]
    lim = max(abs(min(todos)), abs(max(todos))) * 1.15 if todos else 1.0
    for k, lado in enumerate(oidos):
        col = E.COLOR_LADO[lado]
        x0 = ml + k * (pw + sep)

        def X(t):
            return x0 + t / ms_max * pw

        def Y(v):
            return mt + ph / 2 - v / lim * (ph / 2)

        for t in range(0, int(ms_max) + 1):
            s.linea(X(t), mt, X(t), mt + ph, E.GRILLA, 1)
            s.texto(X(t), mt + ph + 14, t, E.T_EJE, E.TENUE)
        s.texto(x0, mt - 12, E.NOMBRE_LADO[lado], E.T_TITULO, E.TINTA, 'start', 600)
        r = regs[lado]
        if r is None:
            s.texto(x0 + pw / 2, mt + ph / 2, 'Sin ECochG en el caso', E.T_ROTULO, E.TENUE)
            continue
        m = r['medida']
        if 'base' not in m or not _hay_complejo(m):
            # Cófosis: hay trazo, pero no complejo que medir (measure_complex devuelve solo 'faltan')
            s.trazo([(X(t), Y(v)) for t, v in zip(r['t'], r['y']) if t <= ms_max], col, E.LINEA)
            s.texto(x0 + pw / 2, mt + ph + 48, 'Sin respuesta identificable', E.T_ROTULO, E.TENUE)
            continue
        base = m['base']
        # áreas (él, 2026-10-20): el área PS, clara, y dentro el área PA, más oscura
        for clave, opac in (('ps', 0.16), ('pa', 0.38)):
            z = (r.get('zonas') or {}).get(clave)
            if not z:
                continue
            xs, ys = z
            pts = [(X(a), Y(b)) for a, b in zip(xs, ys) if a <= ms_max]
            if len(pts) < 2:
                continue
            borde = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
            s.crudo(f'<polygon points="{pts[0][0]:.1f},{Y(base):.1f} {borde} {pts[-1][0]:.1f},{Y(base):.1f}" '
                    f'fill="{col}" fill-opacity="{opac}" stroke="none"/>')
        s.linea(x0, Y(base), x0 + pw, Y(base), E.TINTA_2, 0.8, 'stroke-dasharray="3 3"')
        s.trazo([(X(t), Y(v)) for t, v in zip(r['t'], r['y']) if t <= ms_max], col, E.LINEA)
        # rótulos que no se tapen: el PS a la izquierda de su marca, el PA bajo el valle
        for clave, rot in (('PS', 'PS'), ('PA', 'PA')):
            lat = r['marcas'].get(clave)
            if lat is None or lat > ms_max:
                continue
            v = _interp(lat, r['t'], r['y'])
            s.linea(X(lat), Y(base), X(lat), Y(v), E.TINTA_2, 0.8)
            s.ancla(f'{lado} {clave}', X(lat), Y(v))
            if clave == 'PS':
                s.texto(X(lat) - 4, Y(base) - 5, rot, E.T_CHICO, E.TINTA, 'end', 700)
            else:
                s.texto(X(lat), Y(v) + 12, rot, E.T_CHICO, E.TINTA, 'middle', 700)
        if r.get('zonas'):
            yl = mt + 10
            s.rect(x0 + pw - 74, yl - 7, 9, 7, col, extra=f'fill-opacity="0.16"')
            s.texto(x0 + pw - 62, yl, 'área PS', E.T_CHICO, E.TINTA_2, 'start')
            s.rect(x0 + pw - 74, yl + 4, 9, 7, col, extra=f'fill-opacity="0.38"')
            s.texto(x0 + pw - 62, yl + 11, 'área PA', E.T_CHICO, E.TINTA_2, 'start')
        def num(v):
            # sin FIN (el marcado automático no encontró el retorno) no hay área
            return '—' if v is None else f'{v:.2f}'.replace('.', ',')
        res = [('PS/PA', num(m.get('sp_ap'))),
               ('Razón de áreas', num(m.get('area_ratio'))),
               ('Latencia PA', f"{m['ap_lat']:.2f} ms".replace('.', ','))]
        for i, (rot, val) in enumerate(res):
            s.texto(x0 + i * pw / 3, mt + ph + 42, rot, E.T_CHICO, E.TENUE, 'start')
            s.texto(x0 + i * pw / 3, mt + ph + 54, val, E.T_ROTULO, E.TINTA_2, 'start', 600)
    s.texto(s.ancho / 2, mt + ph + 28, 'Latencia (ms)', E.T_EJE, E.TENUE)
    return s.svg()


def _interp(x, xs, ys):
    for i in range(1, len(xs)):
        if xs[i] >= x:
            t = (x - xs[i - 1]) / ((xs[i] - xs[i - 1]) or 1)
            return ys[i - 1] + t * (ys[i] - ys[i - 1])
    return ys[-1]
