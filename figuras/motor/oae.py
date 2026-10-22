"""Emisiones otoacústicas con los generadores de la app (src/oae/generators).

Se llaman con los parámetros del protocolo (TEOAE no lineal a 80 dB SPL,
barridos y L1/L2 de la normativa) y con cases.data['EOAS'][oído]: la
semilla es la de la app (stable_seed + huella del caso), así que el libro
muestra lo mismo que el equipo con ese paciente.
"""
from . import estilo as E
from .datos import en_raiz
from .svg import Svg

F_MIN, F_MAX = 500, 8000


def teoae(caso, lado):
    from oae.generators.teoae import TeoaeGenerator
    with en_raiz():
        g = TeoaeGenerator()
        n = g.normative
        # Como manda el protocolo: click no lineal a 80 dB SPL.
        return g.generate(level_db=n.get('reference_level_db_spl', g.REFERENCE_LEVEL_DB_SPL),
                          n_sweeps=n['default_n_sweeps'], ear=lado,
                          case=caso['EOAS'][lado], mode='no_lineal')


def dpoae(caso, lado):
    from oae.generators.dpoae import DpoaeGenerator
    with en_raiz():
        g = DpoaeGenerator()
        n = g.normative
        return g.generate(l1_db=n['default_l1_db_spl'], l2_db=n['default_l2_db_spl'],
                          ear=lado, case=caso['EOAS'][lado])


# Letra y medidas: las de siempre y, en el tomo II, la compacta (él, 2026-10-21:
# a media página no se veían). Va a todo el ancho, más baja y con letra que
# impresa no baja de 8 pt, en negro como las hojas del tomo II.
NORMAL = dict(eje=E.T_EJE, chico=E.T_CHICO, rotulo=E.T_ROTULO, titulo=E.T_TITULO,
              tenue=E.TENUE, tinta_2=E.TINTA_2, ph=150, mt=30, f_y=14, eje_y=28, r1=42, r2=54, mb=66)
COMPACTO = dict(eje=10, chico=9.5, rotulo=10, titulo=11, tenue=E.TINTA, tinta_2=E.TINTA,
                ph=100, mt=32, f_y=15, eje_y=30, r1=46, r2=59, mb=66)


def _ejes(s, x0, mt, pw, ph, y_min, y_max, titulo, con_numeros, m=NORMAL):
    import math

    def X(f):
        return x0 + math.log2(f / F_MIN) / math.log2(F_MAX / F_MIN) * pw

    def Y(db):
        return mt + ph - (max(y_min, min(y_max, db)) - y_min) / (y_max - y_min) * ph

    for f in (500, 1000, 2000, 4000, 8000):
        s.linea(X(f), mt, X(f), mt + ph, E.GRILLA, 1)
        s.texto(X(f), mt + ph + m['f_y'], {1000: '1k', 2000: '2k', 4000: '4k', 8000: '8k'}.get(f, f), m['eje'], m['tenue'])
    for db in range(y_min, y_max + 1, 10):
        s.linea(x0, Y(db), x0 + pw, Y(db), E.GRILLA_FUERTE if db == 0 else E.GRILLA, 1)
        if con_numeros:
            s.texto(x0 - 7, Y(db) + m['eje'] * 0.375, db, m['eje'], m['tenue'], 'end')
    s.texto(x0, mt - 12, titulo, m['titulo'], E.TINTA, 'start', 600)
    return X, Y


def dibujar_teoae(caso, oidos=('OD', 'OI'), compacto=False):
    """Respuesta y ruido por frecuencia; bandas que pasan = punto lleno."""
    m = COMPACTO if compacto else NORMAL
    pw, ph, ml, mt, sep = 230, m['ph'], 40, m['mt'], 34
    s = Svg(ml + len(oidos) * pw + (len(oidos) - 1) * sep + 12, mt + ph + m['mb'])
    y_min, y_max = -30, 30
    for k, lado in enumerate(oidos):
        col = E.COLOR_LADO[lado]
        r = teoae(caso, lado)
        x0 = ml + k * (pw + sep)
        X, Y = _ejes(s, x0, mt, pw, ph, y_min, y_max, E.NOMBRE_LADO[lado], k == 0, m)
        fs = [(f, rd, nd) for f, rd, nd in zip(r['freqs'], r['spectrum_db'], r['noise_db']) if F_MIN <= f <= F_MAX]
        # ruido: lavado gris desde el piso; respuesta: línea del oído
        piso = [(X(f), Y(y_min)) for f, _, _ in fs]
        ruido = [(X(f), Y(nd)) for f, _, nd in fs]
        d = 'M' + ' L'.join(f'{x:.2f},{y:.2f}' for x, y in ruido + piso[::-1]) + ' Z'
        s.crudo(f'<path d="{d}" fill="{E.GRILLA}" stroke="none"/>')
        s.trazo([(X(f), Y(rd)) for f, rd, _ in fs], col, E.LINEA)
        for banda, snr in r['snr_per_band'].items():
            f = float(banda)
            pasa = bool(r['pass_per_band'].get(banda, False))
            y = Y(min(y_max, max(y_min, _interp(f, [q[0] for q in fs], [q[1] for q in fs]))))
            s.circulo(X(f), y, 3.8, col, col if pasa else E.PAPEL, 1.4)
            s.ancla(f'{lado} {int(f)}', X(f), y)
        res = [('Reproducibilidad', f"{r['reproducibility_pct']:.0f} %"),
               ('Bandas que pasan', f"{r['n_pass']} de {len(r['snr_per_band'])}")]
        for i, (rot, val) in enumerate(res):
            s.texto(x0 + i * pw / 2, mt + ph + m['r1'], rot, m['chico'], m['tenue'], 'start')
            s.texto(x0 + i * pw / 2, mt + ph + m['r2'], val, m['rotulo'], m['tinta_2'], 'start', 600)
    s.texto(s.ancho / 2, mt + ph + m['eje_y'], 'Frecuencia (Hz)', m['eje'], m['tenue'])
    s.texto(12, mt + ph / 2, 'dB SPL', m['eje'], m['tenue'], extra=f'transform="rotate(-90 12 {mt + ph / 2:.1f})"')
    return s.svg()


def dibujar_dpoae(caso, oidos=('OD', 'OI'), compacto=False):
    """DP-grama: nivel del producto de distorsión sobre el piso de ruido."""
    m = COMPACTO if compacto else NORMAL
    pw, ph, ml, mt, sep = 230, m['ph'], 40, m['mt'], 34
    s = Svg(ml + len(oidos) * pw + (len(oidos) - 1) * sep + 12, mt + ph + m['mb'])
    y_min, y_max = -30, 20
    for k, lado in enumerate(oidos):
        col = E.COLOR_LADO[lado]
        r = dpoae(caso, lado)
        x0 = ml + k * (pw + sep)
        X, Y = _ejes(s, x0, mt, pw, ph, y_min, y_max, E.NOMBRE_LADO[lado], k == 0, m)
        f2 = [float(f) for f in r['f2_list']]
        piso = [(X(f), Y(nf)) for f, nf in zip(f2, r['noise_floors_db_spl'])]
        d = ('M' + ' L'.join(f'{x:.2f},{y:.2f}' for x, y in piso)
             + f' L{piso[-1][0]:.2f},{Y(y_min):.2f} L{piso[0][0]:.2f},{Y(y_min):.2f} Z')
        s.crudo(f'<path d="{d}" fill="{E.GRILLA}" stroke="none"/>')
        s.trazo([(X(f), Y(dp)) for f, dp in zip(f2, r['dp_levels_db_spl'])], col, E.LINEA)
        for p in r['points']:
            s.circulo(X(float(p['f2_hz'])), Y(p['dp_db']), 3.8, col, col if p['passed'] else E.PAPEL, 1.4)
            s.ancla(f"{lado} {int(float(p['f2_hz']))}", X(float(p['f2_hz'])), Y(p['dp_db']))
        s.texto(x0, mt + ph + m['r1'], 'Frecuencias que pasan', m['chico'], m['tenue'], 'start')
        s.texto(x0, mt + ph + m['r2'], f"{r['n_pass']} de {r['n_total']}  ·  L1/L2 {r['l1_db']:g}/{r['l2_db']:g} dB SPL",
                m['rotulo'], m['tinta_2'], 'start', 600)
    s.texto(s.ancho / 2, mt + ph + m['eje_y'], 'f2 (Hz)', m['eje'], m['tenue'])
    s.texto(12, mt + ph / 2, 'dB SPL', m['eje'], m['tenue'], extra=f'transform="rotate(-90 12 {mt + ph / 2:.1f})"')
    return s.svg()


def _interp(x, xs, ys):
    for i in range(1, len(xs)):
        if xs[i] >= x:
            t = (x - xs[i - 1]) / ((xs[i] - xs[i - 1]) or 1)
            return ys[i - 1] + t * (ys[i] - ys[i - 1])
    return ys[-1]
