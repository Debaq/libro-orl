#!/usr/bin/env python3
"""Capítulo 37 (Nariz y pulmón): espirometrías de los dos casos y dos figuras de fisiología.

    cap37-via-unica.svg       la vía aérea de la nariz a los bronquios y qué ve la espirometría
    cap37-donde-limita.svg    curvas flujo-volumen: dónde se limita el flujo (normal, asma, estenosis fija)
    cap37-espiro-asma.svg     informe pre/post broncodilatador del caso 37.1 (formato del manual SER 2024)
    cap37-espiro-estenosis.svg informe del caso 37.2

Todo se CALCULA acá. Los valores previstos, el límite inferior de la normalidad (LIN) y los z-score salen de las
ecuaciones GLI-2012 (grupo caucásico), que es lo que recomienda el manual SER Chile 2024 (hacer_cap37_gli.py:
coeficientes de la tabla spline de GLI; se validan contra dos ejemplos publicados del propio manual). Las curvas
son las del modelo de hacer_h30.py (el flujo depende solo del volumen ya espirado), ajustadas para que el FEV1 y
el PEF de cada caso sean los de abajo; FVC, FEV1 y PEF medidos son DATOS DEL CASO (inventados para el ejemplo),
todo lo demás sale de cuentas. Al correrlo se imprimen todas las cifras que usa el texto."""
import json
import math
import pathlib
import sys

AQUI = pathlib.Path(__file__).parent
sys.path.insert(0, str(AQUI))
from hacer_h30 import Maniobra, Eje, Lienzo, lazo_pts, curva_tiempo  # noqa: E402
from hacer_h26 import TINTA, TENUE, GRILLA, FUERTE, AVISO, RETRO, COCLEAR, IZQ  # noqa: E402
from hacer_cap37_gli import GLI  # noqa: E402

GRIS = '#b9b6ae'
PRE, POST = IZQ, AVISO     # como en el informe del manual: antes en azul, después en rojo


# ------------------------------------------------------------------ GLI-2012
def _lms(sexo, par, edad, talla_cm, etnia=1):
    d = GLI[f'{sexo}_{par}']
    c = d['c']
    i = (edad - 3.0) / 0.25
    i0 = min(int(i), len(d['L']) - 2)
    fr = i - i0
    sp = lambda k: d[k][i0] + (d[k][i0 + 1] - d[k][i0]) * fr
    L = c['q0'] + c['q1'] * math.log(edad) + sp('L')
    M = math.exp(c['a0'] + c['a1'] * math.log(talla_cm) + c['a2'] * math.log(edad) + (c['a6'] if etnia == 5 else 0) + sp('M'))
    S = math.exp(c['p0'] + c['p1'] * math.log(edad) + (c['p5'] if etnia == 5 else 0) + sp('S'))
    return L, M, S


def prev(sexo, par, edad, talla):
    return _lms(sexo, par, edad, talla)[1]


def lin(sexo, par, edad, talla):
    L, M, S = _lms(sexo, par, edad, talla)
    return M * (1 + L * S * -1.645) ** (1 / L)


def zscore(sexo, par, v, edad, talla):
    L, M, S = _lms(sexo, par, edad, talla)
    return ((v / M) ** L - 1) / (L * S)


def verificar_gli():
    """Ejemplos publicados en el manual SER 2024: (1) hombre de 54 años y 160 cm: FEV1 previsto 3,00 L (texto);
    (2) figura 2: mujer de 44 años y 164 cm: CVF 3,67, VEF1 2,97, VEF1/CVF 81,42 %, LIN 2,91, 2,35 y 70,46 %."""
    assert abs(prev('M', 'FEV1', 54, 160) - 3.00) < 0.02
    mujer = ('F', 44, 164)
    for par, t, l in (('FVC', 3.67, 2.91), ('FEV1', 2.97, 2.35), ('FEV1FVC', 0.8142, 0.7046)):
        assert abs(prev(*mujer[:1], par, *mujer[1:]) - t) < 0.006, par
        assert abs(lin(*mujer[:1], par, *mujer[1:]) - l) < 0.006, par
    print('GLI verificado contra los ejemplos del manual SER 2024')


# ------------------------------------------------------------------ casos
def ajustar(fvc, fev1, pef, tau=0.05, pif=None):
    """Maniobra (modelo de H30) con la FVC y el PEF dados y la p que da ese FEV1."""
    lo, hi = 0.4, 8.0
    for _ in range(60):
        p = (lo + hi) / 2
        f = Maniobra(fvc, pef, p, tau, pif=pif).fev(1.0)
        if f > fev1:
            lo = p
        else:
            hi = p
    return Maniobra(fvc, pef, (lo + hi) / 2, tau, pif=pif)


def tef(m, F=None):
    t = m.meseta(F=F)
    return t


ASMA = dict(sexo='M', edad=27, talla=176, peso=74, etiqueta='hombre',
            pre=dict(fvc=4.90, fev1=3.20, pef=7.4, cvif=4.93),
            post=dict(fvc=5.10, fev1=3.80, pef=8.8, cvif=5.12),
            calidad_pre='VEF1 A  CVF A', calidad_post='VEF1 A  CVF A')
ESTEN = dict(sexo='F', edad=49, talla=160, peso=68, etiqueta='mujer',
             pre=dict(fvc=3.25, cap_e=3.2, cap_i=3.0, cvif=3.28),
             post=dict(fvc=3.27, cap_e=3.25, cap_i=3.0, cvif=3.30),
             calidad_pre='VEF1 A  CVF A', calidad_post='VEF1 A  CVF A')
BASE_EST = dict(pef=7.4, p=1.5, tau=0.05, pif=5.2)


def maniobras():
    """Devuelve, para cada caso, las maniobras (objeto, F espiratoria, FI inspiratoria) pre y post y sus números."""
    res = {}
    # asma
    for k, par in (('pre', ASMA['pre']), ('post', ASMA['post'])):
        m = ajustar(par['fvc'], par['fev1'], par['pef'], pif=par['pef'] * 0.62)
        res[('asma', k)] = dict(m=m, F=m.F, FI=m.FI, fvc=par['fvc'], fev1=m.fev(1.0), pef=par['pef'],
                                cvif=par['cvif'], tef=m.meseta())
    # estenosis fija: el tope recorta el flujo normal en los dos sentidos
    for k in ('pre', 'post'):
        par = ESTEN[k]
        m = Maniobra(par['fvc'], BASE_EST['pef'], BASE_EST['p'], BASE_EST['tau'], pif=BASE_EST['pif'])
        F = (lambda x, m=m, c=par['cap_e']: min(m.F(x), c))
        FI = (lambda y, m=m, c=par['cap_i']: min(m.FI(y), c))
        res[('esten', k)] = dict(m=m, F=F, FI=FI, fvc=par['fvc'], fev1=m.fev(1.0, F=F),
                                 pef=max(F(i / 400) for i in range(401)), cvif=par['cvif'], tef=m.meseta(F=F))
    return res


def filas(caso, r):
    """Filas de la tabla del informe (CVF, VEF1, VEF1/CVF, FEM, TEF, CVIF) con previstos, LIN y z."""
    s, e, t = caso['sexo'], caso['edad'], caso['talla']
    a, b = r[0], r[1]
    out = {}
    pf, pv = prev(s, 'FVC', e, t), prev(s, 'FEV1', e, t)
    lf, lv = lin(s, 'FVC', e, t), lin(s, 'FEV1', e, t)
    prr, lr = prev(s, 'FEV1FVC', e, t) * 100, lin(s, 'FEV1FVC', e, t) * 100
    for nom, x in (('pre', a), ('post', b)):
        fvc, fev = round(x['fvc'], 2), round(x['fev1'], 2)
        ratio = fev / fvc * 100
        out[nom] = dict(fvc=fvc, fev1=fev, ratio=ratio, pef=round(x['pef'], 1), tef=x['tef'], cvif=x['cvif'],
                        z_fvc=zscore(s, 'FVC', fvc, e, t), z_fev1=zscore(s, 'FEV1', fev, e, t),
                        z_ratio=zscore(s, 'FEV1FVC', fev / fvc, e, t),
                        pc_fvc=fvc / pf * 100, pc_fev1=fev / pv * 100, pc_cvif=x['cvif'] / pf * 100)
    out['prev'] = dict(fvc=pf, fev1=pv, ratio=prr, lin_fvc=lf, lin_fev1=lv, lin_ratio=lr)
    out['cambio'] = dict(fvc_l=out['post']['fvc'] - out['pre']['fvc'], fev1_l=out['post']['fev1'] - out['pre']['fev1'])
    out['cambio']['fvc_pc'] = out['cambio']['fvc_l'] / pf * 100
    out['cambio']['fev1_pc'] = out['cambio']['fev1_l'] / pv * 100
    out['cambio']['fev1_rel'] = out['cambio']['fev1_l'] / out['pre']['fev1'] * 100
    out['cambio']['fvc_rel'] = out['cambio']['fvc_l'] / out['pre']['fvc'] * 100
    out['fev1_pef'] = {k: out[k]['fev1'] * 1000 / (out[k]['pef'] * 60) for k in ('pre', 'post')}
    return out


# ------------------------------------------------------------------ informe en SVG
def f2(x):
    return f'{x:.2f}'


def informe(nombre_svg, caso, r, d, titulo_extra=''):
    W, H = 640, 548
    c = Lienzo(W, H)
    c.t(10, 20, 'ESPIROMETRÍA PRE/POST BRONCODILATADOR', 10.5, TINTA, 'start', 700)
    c.t(10, 38, f"{caso['etiqueta'].capitalize()}, {caso['edad']} años · {caso['talla']} cm · {caso['peso']} kg · sexo de nacimiento: "
        f"{'masculino' if caso['sexo'] == 'M' else 'femenino'}", 9, TINTA, 'start')
    c.t(10, 54, 'VALORES TEÓRICOS: GLI-2012 (caucásico) · BRONCODILATADOR: salbutamol 400 µg con aerocámara, 15 min', 9, TINTA, 'start')
    c.t(10, 70, f"CALIDAD DE LA PRUEBA   PRE: {caso['calidad_pre']}   POST: {caso['calidad_post']}", 9, TINTA, 'start', 700)
    # gráficos
    ef = Eje(c, 54, 100, 290, 190, 0, 6, -8, 10)
    ef.marco(xt=[0, 2, 4, 6], yt=[-8, -4, 0, 4, 8], xlab='volumen (L)', ylab='flujo (L/s)')
    ev = Eje(c, 418, 100, 200, 190, 0, 10, 0, 6)
    ev.marco(xt=[0, 2, 4, 6, 8, 10], yt=[0, 2, 4, 6], xlab='tiempo (s)', ylab='volumen (L)')
    c.t(54, 94, 'Flujo-volumen', 9, TINTA, 'start', 700)
    c.t(418, 94, 'Volumen-tiempo', 9, TINTA, 'start', 700)
    for nom, col, dash in (('pre', PRE, None), ('post', POST, '5 3')):
        x = r[(nom_caso(caso), nom)]
        m = x['m']
        n = 240
        pe = [(ef.X(x['fvc'] * i / n), ef.Y(x['F'](i / n))) for i in range(n + 1)]
        pi_ = [(ef.X(x['fvc'] * (1 - i / n) * 1.0), ef.Y(-x['FI'](i / n))) for i in range(n + 1)]
        c.poli(pe + pi_, col, 2, dash)
        tt = m.tiempo(tmax=10, F=x['F'])
        c.poli([(ev.X(t), ev.Y(v)) for t, v in tt if t <= 10], col, 2, dash)
        c.punto(ev.X(1), ev.Y(x['fev1']), col, 3.2)
    # leyenda de curvas
    c.l(176, 90, 198, 90, PRE, 2)
    c.t(204, 94, 'Pre', 9, TINTA, 'start')
    c.l(236, 90, 258, 90, POST, 2, '5 3')
    c.t(264, 94, 'Post', 9, TINTA, 'start')
    # tabla
    cols = [('', 10, 'start'), ('Teór.', 108, 'end'), ('Pre', 150, 'end'), ('% Teór.', 200, 'end'), ('LIN', 244, 'end'),
            ('z', 284, 'end'), ('Post', 332, 'end'), ('% Teór.', 384, 'end'), ('z', 422, 'end'), ('Cambio', 520, 'end'),
            ('(% del teór.)', 618, 'end')]
    y = 340
    c.raw(f'<rect x="4" y="{y - 14}" width="{W - 8}" height="20" fill="#f1e9ee"/>')
    for t, x, a in cols[:-2]:
        c.t(x, y, t, 9, TINTA, a, 700)
    c.t(570, y, 'Cambio (% del teór.)', 9, TINTA, 'middle', 700)
    P, A, B = d['prev'], d['pre'], d['post']
    f1 = lambda v: f'{v:.1f}'
    cam = d['cambio']
    rows = [
        ('CVF (L)', f2(P['fvc']), f2(A['fvc']), f'{A["pc_fvc"]:.0f}', f2(P['lin_fvc']), f2(A['z_fvc']), f2(B['fvc']), f'{B["pc_fvc"]:.0f}', f2(B['z_fvc']), f'{cam["fvc_pc"]:+.1f}'),
        ('VEF1 (L)', f2(P['fev1']), f2(A['fev1']), f'{A["pc_fev1"]:.0f}', f2(P['lin_fev1']), f2(A['z_fev1']), f2(B['fev1']), f'{B["pc_fev1"]:.0f}', f2(B['z_fev1']), f'{cam["fev1_pc"]:+.1f}'),
        ('VEF1/CVF (%)', f1(P['ratio']), f1(A['ratio']), '', f1(P['lin_ratio']), f2(A['z_ratio']), f1(B['ratio']), '', f2(B['z_ratio']), ''),
        ('FEM (L/s)', '', f1(A['pef']), '', '', '', f1(B['pef']), '', '', ''),
        ('TEF (s)', '', f1(A['tef']), '', '', '', f1(B['tef']), '', '', ''),
        ('CVIF (L)', f2(P['fvc']), f2(A['cvif']), f'{A["pc_cvif"]:.0f}', f2(P['lin_fvc']), '', f2(B['cvif']), f'{B["pc_cvif"]:.0f}', '', ''),
    ]
    xs = [10, 108, 150, 200, 244, 284, 332, 384, 422, 570]
    for k, row in enumerate(rows):
        yy = y + 22 + k * 19
        if k % 2 == 0:
            c.raw(f'<rect x="4" y="{yy - 13}" width="{W - 8}" height="19" fill="#faf7f4"/>')
        for j, v in enumerate(row):
            a = 'start' if j == 0 else ('middle' if j == 9 else 'end')
            peso = 700 if (j == 0 or (j == 9 and v)) else 400
            col = PRE if j in (2, 3, 5) and v else (POST if j in (6, 7, 8) and v else TINTA)
            c.t(xs[j], yy, v.replace('-', '−') if v else v, 9, col if j else TINTA, a, peso)
    yb = y + 22 + 6 * 19 + 10
    notas = ['LIN: límite inferior de la normalidad (z = −1,645). CVF: capacidad vital forzada.',
             'VEF1: volumen espiratorio forzado en el primer segundo (el punto de la curva volumen-tiempo).',
             'FEM: flujo espiratorio máximo (GLI-2012 no trae valores teóricos del FEM).',
             'TEF: tiempo espiratorio forzado. CVIF: capacidad vital inspiratoria forzada.',
             'El cambio se calcula sobre el valor teórico: (post − pre) × 100 / teórico.']
    for i, t in enumerate(notas):
        c.t(10, yb + i * 14, t, 8.5, TENUE, 'start')
    c.guardar(nombre_svg)


def nom_caso(caso):
    return 'asma' if caso is ASMA else 'esten'


# ------------------------------------------------------------------ fisiología
def via_unica():
    W, H = 640, 382
    c = Lienzo(W, H)
    segs = [('Nariz', 'mucosa hinchada\n(rinitis)', 'no se ve: la pinza\nnasal la deja fuera'),
            ('Faringe y\nlaringe', 'parálisis de cuerdas\nvocales, tumores', 'meseta inspiratoria\n(si es variable)'),
            ('Tráquea\nextratorácica', 'estenosis tras\nintubación', 'meseta inspiratoria\n(variable) o en las dos\nfases (fija)'),
            ('Tráquea\nintratorácica', 'estenosis tras\nintubación', 'meseta espiratoria\n(variable) o en las dos\nfases (fija)'),
            ('Bronquios', 'asma\n(broncoconstricción)', 'curva cóncava en\nla espiración')]
    x0, w, gap = 20, 112, 10
    ytop = 96
    for k, (nom, que, lim) in enumerate(segs):
        x = x0 + k * (w + gap)
        col = COCLEAR if k < 4 else RETRO
        c.raw(f'<rect x="{x}" y="{ytop}" width="{w}" height="44" rx="8" fill="#fff" stroke="{col}" stroke-width="2"/>')
        l1 = nom.split('\n')
        for i, t in enumerate(l1):
            c.t(x + w / 2, ytop + (19 if len(l1) == 1 else 15) + (i * 14 if len(l1) > 1 else 6), t, 9.5, TINTA, 'middle', 700)
        if k < 4:
            c.l(x + w, ytop + 22, x + w + gap, ytop + 22, TINTA, 1.4)
        for i, t in enumerate(que.split('\n')):
            c.t(x + w / 2, ytop + 76 + i * 14, t, 9, TINTA)
        for i, t in enumerate(lim.split('\n')):
            c.t(x + w / 2, ytop + 146 + i * 14, t, 9, col, 'middle', 700)
    c.t(x0, ytop + 60, 'Se estrecha por:', 9, TENUE, 'start')
    c.t(x0, ytop + 130, 'Dónde se ve en la curva flujo-volumen:', 9, TENUE, 'start')

    def corchete(xa, xb, y, texto, col):
        c.l(xa, y, xb, y, col, 2)
        c.l(xa, y, xa, y + 8, col, 2)
        c.l(xb, y, xb, y + 8, col, 2)
        c.t((xa + xb) / 2, y - 6, texto, 9.5, col, 'middle', 700)
    xb4 = x0 + 4 * (w + gap) - gap
    corchete(x0, xb4, 64, 'Vía aérea superior (de la nariz a la carina)', COCLEAR)
    corchete(x0 + 4 * (w + gap), x0 + 5 * (w + gap) - gap, 64, 'Vía aérea inferior', RETRO)
    c.t(10, 22, 'Una sola vía por donde pasa el aire', 10.5, TINTA, 'start', 700)
    c.t(10, 40, 'De izquierda a derecha, el camino del aire que se inspira.', 9, TENUE, 'start')
    xt = x0 + 3 * (w + gap) - gap / 2
    c.l(xt, ytop - 8, xt, ytop + 52, TENUE, 1.2, '4 3')
    c.l(xt, ytop + 52, xt, ytop + 70, TENUE, 1.2, '4 3')
    c.t(xt, ytop - 12, 'entrada del tórax', 8.5, TENUE, 'middle')
    yb = 322
    xm1 = x0 + (w + gap) + 6
    xm2 = x0 + 5 * (w + gap) - gap
    c.raw(f'<rect x="{xm1}" y="{yb}" width="{xm2 - xm1}" height="22" rx="5" fill="{GRILLA}" stroke="{TENUE}" stroke-width="1.2"/>')
    c.t((xm1 + xm2) / 2, yb + 15, 'Lo que mide la espirometría: el aire que pasa por la boca', 9.5, TINTA, 'middle', 700)
    c.raw(f'<rect x="{x0}" y="{yb}" width="{xm1 - x0 - 6}" height="22" rx="5" fill="#fff" stroke="{TENUE}" stroke-width="1.2" stroke-dasharray="4 3"/>')
    c.t(x0 + (xm1 - x0 - 6) / 2, yb + 15, 'fuera', 9.5, TENUE, 'middle', 700)
    c.t(10, yb + 46, 'Con la pinza nasal puesta, el aire de la maniobra no pasa por la nariz: la espirometría no mide la nariz.', 9, TINTA, 'start')
    c.t(10, yb + 62, 'La nariz se estudia con otros exámenes (→ H25, H26, H27).', 9, TENUE, 'start')
    c.guardar('cap37-via-unica.svg')


def donde_limita():
    W, H = 640, 480
    c = Lienzo(W, H)
    base = Maniobra(4.8, 9.0, 1.5, 0.05, pif=5.6)
    asma = ajustar(4.6, 2.9, 5.4, pif=3.4)
    pan = [('Normal', TINTA, base.F, base.FI, 4.8),
           ('Obstrucción bronquial (asma)', AVISO, asma.F, asma.FI, 4.6),
           ('Estenosis fija (vía aérea alta)', IZQ, (lambda x: min(base.F(x), 3.3)), (lambda y: min(base.FI(y), 2.9)), 4.8)]
    aw, sep, x_ini = 168, 36, 52
    for k, (nom, col, F, FI, fvc) in enumerate(pan):
        x0 = x_ini + k * (aw + sep)
        c.t(x0 + aw / 2, 22, nom, 9.5, col if col != TINTA else TINTA, 'middle', 700)
        ej = Eje(c, x0, 36, aw, 190, 0, 5, -8, 10)
        ej.marco(xt=[0, 1, 2, 3, 4, 5], yt=[-6, -3, 0, 3, 6, 9], xlab='volumen (L)', ylab='flujo (L/s)' if k == 0 else '')
        n = 240
        pe = [(ej.X(fvc * i / n), ej.Y(F(i / n))) for i in range(n + 1)]
        pi_ = [(ej.X(fvc * (1 - i / n)), ej.Y(-FI(i / n))) for i in range(n + 1)]
        if k:
            pb, pbi = lazo_pts(base, ej)
            c.poli(pb + pbi, GRIS, 1.4, '4 3')
        c.poli(pe + pi_, col, 2.4)
    # marcadores numerados
    def num(n, x, y):
        c.raw(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8.5" fill="#fff" stroke="{TINTA}" stroke-width="1.2"/>')
        c.t(x, y + 3.6, str(n), 9, TINTA, 'middle', 700)
    ejs = [Eje(c, x_ini + k * (aw + sep), 36, aw, 190, 0, 5, -8, 10) for k in range(3)]
    num(1, ejs[0].X(0.75), ejs[0].Y(base.F(0.75 / 4.8)) - 14)
    num(2, ejs[0].X(3.2), ejs[0].Y(base.F(3.2 / 4.8)) - 14)
    num(3, ejs[0].X(2.4), ejs[0].Y(-base.FI(.5)) + 16)
    num(2, ejs[1].X(2.2), ejs[1].Y(asma.F(2.2 / 4.6)) - 14)
    num(4, ejs[2].X(1.0), ejs[2].Y(3.3) - 14)
    num(5, ejs[2].X(2.4), ejs[2].Y(-2.9) + 16)
    ly = 290
    leyenda = [('1', 'Pico (PEF): depende del esfuerzo; ahí se ve lo que pasa en la vía aérea ancha: laringe y tráquea.'),
               ('2', 'Tramo medio y final: no depende del esfuerzo; depende del calibre de los bronquios (en el asma, cóncavo).'),
               ('3', 'Inspiración forzada: depende del esfuerzo; la vía extratorácica se estrecha cuando la presión interna baja.'),
               ('4', 'Meseta espiratoria: el aire no sale más rápido que lo que deja pasar el estrechamiento.'),
               ('5', 'Meseta inspiratoria: lo mismo al inspirar; una estenosis rígida (fija) limita los dos sentidos.')]
    for i, (n, t) in enumerate(leyenda):
        num(n, 18, ly + i * 24)
        c.t(34, ly + i * 24 + 3.5, t, 9, TINTA, 'start')
    c.t(10, ly + 5 * 24 + 8, 'Línea gris punteada: la curva normal del primer panel. Curvas calculadas con un modelo sencillo; los valores son de ejemplo.', 8.5, TENUE, 'start')
    c.guardar('cap37-donde-limita.svg')


def main():
    verificar_gli()
    res = maniobras()
    out = {}
    for nombre, caso, svg in (('asma', ASMA, 'cap37-espiro-asma.svg'), ('esten', ESTEN, 'cap37-espiro-estenosis.svg')):
        d = filas(caso, (res[(nombre, 'pre')], res[(nombre, 'post')]))
        informe(svg, caso, res, d)
        out[nombre] = d
        print('\n###', nombre, caso['sexo'], caso['edad'], 'años', caso['talla'], 'cm')
        print(json.dumps(d, ensure_ascii=False, indent=1, default=float))
    via_unica()
    donde_limita()


if __name__ == '__main__':
    main()
