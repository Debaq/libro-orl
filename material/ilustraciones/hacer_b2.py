#!/usr/bin/env python3
"""Dibuja los esquemas propios del capítulo B2 (fisiología), SVG a mano, no IA:

    b2-resonancia-cae.svg       ganancia del pabellón y el conducto (curva tipo Shaw, 1974)
    b2-adaptador-oido-medio.svg razón de áreas y palanca de la cadena
    b2-arco-estapedial.svg      arco ipsi y contralateral del reflejo estapedial
    b2-mecanismos-co.svg        caminos de la conducción ósea (Stenfelt y Goode, 2005)
    b2-onda-viajera.svg         onda viajera y tonotopía (von Békésy, 1960; Greenwood, 1990)
    b2-transduccion.svg         transducción mecanoeléctrica en la célula ciliada
    b2-codificacion.svg         código de lugar, bloqueo de fase y frecuencia de disparo
    b2-binaural.svg             diferencias interaurales de tiempo y de nivel
    b2-ewald.svg                las tres leyes de Ewald
    b2-olfaccion.svg            transducción olfatoria y vía hasta la corteza

Son esquemas didácticos, no medidas a escala. Las curvas son aproximadas; las cifras que llevan
salen de la bibliografía del capítulo."""
import math
from hacer_b3 import (L, TINTA, TENUE, GRILLA, AZUL, ROJO, VERDE, NARANJA, VIOLETA, HUESO, HUESO2,
                      ROSA, ROSA2, AMAR, AMAR2, CELE, CELE2, VERD_C, VERD_C2)


def flecha(c, x1, y1, x2, y2, color=TINTA, w=1.6, dash=None, punta=7):
    c.linea(x1, y1, x2, y2, color, w, dash)
    a = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - punta * math.cos(a - 0.4), y2 - punta * math.sin(a - 0.4))
    p2 = (x2 - punta * math.cos(a + 0.4), y2 - punta * math.sin(a + 0.4))
    c.add(f'<polygon points="{x2:.1f},{y2:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{color}"/>')


def caja(c, x, y, w, h, texto, fill='#fff', stroke=TINTA, size=10.5, color=TINTA, peso=400):
    c.rect(x, y, w, h, fill, stroke, 1, 5)
    lineas = texto.split('|')
    y0 = y + h / 2 - (len(lineas) - 1) * 7 + 4
    for i, s in enumerate(lineas):
        c.t(x + w / 2, y0 + i * 14, s, size, color, peso=peso)


def ejes(c, x0, y0, w, h, xlab, ylab):
    c.linea(x0, y0, x0 + w, y0, TINTA, 1)
    c.linea(x0, y0, x0, y0 - h, TINTA, 1)
    c.t(x0 + w / 2, y0 + 34, xlab, 10.5, TENUE)
    c.add(f'<text x="{x0 - 38:.1f}" y="{y0 - h / 2:.1f}" font-family="\'Plus Jakarta Sans\', sans-serif" '
          f'font-size="12.8" fill="{TENUE}" text-anchor="middle" '
          f'transform="rotate(-90 {x0 - 38:.1f} {y0 - h / 2:.1f})">{ylab}</text>')


def resonancia_cae():
    c = L(780, 440)
    c.t(390, 26, 'Ganancia del pabellón y del conducto', 15, peso=700)
    x0, y0, w, h = 90, 360, 640, 280
    fmin, fmax, gmin, gmax = 0.2, 10, -5, 25

    def X(f):
        return x0 + w * math.log10(f / fmin) / math.log10(fmax / fmin)

    def Y(g):
        return y0 - h * (g - gmin) / (gmax - gmin)

    for g in range(0, 26, 5):
        c.linea(x0, Y(g), x0 + w, Y(g), GRILLA, 1)
        c.t(x0 - 8, Y(g) + 4, str(g), 10, TENUE, 'end')
    for f, s in ((0.25, '0,25'), (0.5, '0,5'), (1, '1'), (2, '2'), (3, '3'), (5, '5'), (8, '8')):
        c.linea(X(f), y0, X(f), y0 - h, GRILLA, 1)
        c.t(X(f), y0 + 16, s, 10, TENUE)
    ejes(c, x0, y0, w, h, 'frecuencia (kHz)', 'ganancia en la membrana (dB)')
    abierto = [(0.2, 0.5), (0.4, 1), (0.7, 2), (1, 3), (1.4, 5), (1.8, 9), (2.2, 14), (2.6, 17),
               (3, 17.5), (3.5, 16), (4, 14.5), (4.7, 15), (5.3, 14), (6.5, 10), (8, 5), (10, 2)]
    c.ruta('M' + ' L'.join(f'{X(f):.1f},{Y(g):.1f}' for f, g in abierto), stroke=AZUL, w=2.6)
    ocl = [(0.2, 0.5), (1, 1), (2, 0.5), (3, 0), (5, -1), (10, -2)]
    c.ruta('M' + ' L'.join(f'{X(f):.1f},{Y(g):.1f}' for f, g in ocl), stroke=NARANJA, w=2, dash='6 4')
    c.rot(X(2.9), Y(17.5), X(1.3), Y(22.5), 'resonancia del conducto (≈ 3 kHz)', 'middle', AZUL)
    c.rot(X(4.8), Y(15), X(6.3), Y(21), 'concha (≈ 5 kHz)', 'middle', AZUL)
    c.t(X(0.6), Y(-2.5), 'conducto ocluido: se pierde la resonancia', 10.5, NARANJA, 'middle')
    c.t(390, 428, 'Curva aproximada, promedio de varias fuentes en campo libre; a partir de Shaw (1974).', 10, TENUE)
    c.guardar('b2-resonancia-cae.svg')


def adaptador():
    c = L(920, 420)
    c.t(460, 26, 'El oído medio como adaptador de impedancia', 15, peso=700)
    c.t(230, 62, 'A. Razón de áreas', 12.5, peso=700)
    c.el(110, 200, 46, 92, CELE, CELE2, 1.4)
    c.t(110, 205, 'membrana', 10.5)
    c.t(110, 312, '≈ 55 mm² útiles', 10.5, TENUE)
    c.rect(330, 186, 16, 30, AMAR, AMAR2, 1.2, 2)
    c.t(338, 250, 'platina', 10.5)
    c.t(338, 266, '≈ 3,2 mm²', 10.5, TENUE)
    for dy in (-60, -30, 0, 30, 60):
        flecha(c, 160, 200 + dy, 326, 200 + dy * 0.18, AZUL, 1.2)
    c.t(240, 130, 'la misma fuerza', 10.5, AZUL)
    c.t(240, 144, 'en menos área', 10.5, AZUL)
    c.t(240, 350, '55 / 3,2 ≈ ×17 en presión', 12, peso=700)
    c.linea(460, 60, 460, 360, GRILLA, 1.2)
    c.t(690, 62, 'B. Palanca de la cadena', 12.5, peso=700)
    c.add('<polygon points="690,214 676,240 704,240" fill="#e8dfc8" stroke="#b5a57a"/>')
    c.linea(540, 214, 800, 214, TINTA, 4)
    c.el(690, 214, 4, 4, TINTA, TINTA)
    c.t(610, 200, 'mango del martillo', 10.5)
    c.t(610, 260, 'brazo largo (1,3)', 10.5, TENUE)
    c.t(750, 200, 'apófisis larga', 10.5)
    c.t(750, 260, 'del yunque (1)', 10.5, TENUE)
    flecha(c, 545, 160, 545, 208, ROJO, 1.8)
    c.t(545, 152, 'fuerza', 10.5, ROJO)
    flecha(c, 795, 222, 795, 280, ROJO, 2.6)
    c.t(795, 298, 'fuerza ×1,3', 10.5, ROJO)
    c.t(690, 350, 'palanca ≈ ×1,3', 12, peso=700)
    c.rect(150, 372, 620, 34, '#f7f5ef', GRILLA, 1, 6)
    c.t(460, 394, '17 × 1,3 ≈ 22 veces → ≈ 27 dB teóricos; medido: ≈ 20 dB cerca de 1 kHz', 11.5, peso=600)
    c.guardar('b2-adaptador-oido-medio.svg')


def arco_estapedial():
    c = L(920, 470)
    c.t(460, 26, 'Arco del reflejo estapedial (estímulo en el oído derecho)', 15, peso=700)
    c.linea(460, 50, 460, 430, TENUE, 1, '5 5')
    c.t(230, 56, 'lado derecho', 11, TENUE)
    c.t(690, 56, 'lado izquierdo', 11, TENUE)
    W, H = 170, 40
    pos = {'coc': (60, 380, 'cóclea + VIII'), 'ncv': (60, 270, 'núcleo coclear|ventral'),
           'cos_d': (270, 180, 'complejo olivar|superior'), 'cos_i': (480, 180, 'complejo olivar|superior'),
           'vii_d': (60, 90, 'núcleo motor|del facial'), 'vii_i': (690, 90, 'núcleo motor|del facial'),
           'mus_d': (270, 90, 'VII → músculo|del estribo'), 'mus_i': (690, 380, 'VII → músculo|del estribo')}
    for k, (x, y, s) in pos.items():
        fill = ROSA if k.startswith('mus') else (AMAR if k == 'coc' else '#fff')
        caja(c, x, y, W, H, s, fill, TINTA, 10.5)

    def cx(k, lado='c'):
        x, y, _ = pos[k]
        return {'c': (x + W / 2, y + H / 2), 't': (x + W / 2, y), 'b': (x + W / 2, y + H),
                'l': (x, y + H / 2), 'r': (x + W, y + H / 2)}[lado]
    flecha(c, *cx('coc', 't'), *cx('ncv', 'b'), TINTA, 1.8)
    flecha(c, *cx('ncv', 't'), *cx('vii_d', 'b'), ROJO, 2.2)
    flecha(c, *cx('ncv', 'r'), *cx('cos_d', 'l'), ROJO, 1.8)
    flecha(c, *cx('cos_d', 't'), *cx('vii_d', 'r'), ROJO, 1.8)
    flecha(c, *cx('vii_d', 'r'), *cx('mus_d', 'l'), ROJO, 2.2)
    xr, yr = cx('ncv', 'r')
    flecha(c, xr, yr + 10, *cx('cos_i', 'l'), AZUL, 1.8)
    flecha(c, *cx('cos_i', 'r'), *cx('vii_i', 'b'), AZUL, 1.8)
    xb, yb = cx('vii_i', 'r')
    c.ruta(f'M{xb},{yb} L{xb + 30},{yb} L{xb + 30},{400}', stroke=AZUL, w=2.2)
    flecha(c, xb + 30, 400, xb + 2, 400, AZUL, 2.2)
    c.linea(560, 440, 590, 440, ROJO, 2.5)
    c.t(596, 444, 'ipsilateral (no cruza)', 10.5, ROJO, 'start')
    c.linea(560, 458, 590, 458, AZUL, 2.5)
    c.t(596, 462, 'contralateral (cruza la línea media)', 10.5, AZUL, 'start')
    c.t(250, 455, 'Esquema simplificado a partir de Mukerji y cols. (2010).', 10, TENUE)
    c.guardar('b2-arco-estapedial.svg')


def mecanismos_co():
    c = L(920, 450)
    c.t(460, 26, 'Cómo llega a la cóclea la vibración del cráneo', 15, peso=700)
    caja(c, 30, 190, 180, 60, 'vibrador en la mastoides:|vibra el cráneo', HUESO, HUESO2, 10.5)
    caja(c, 720, 175, 170, 90, 'cóclea:|se mueve la|membrana basilar', CELE, CELE2, 11, peso=600)
    vias = [('1. Radiación al conducto', 'el conducto suena; pesa en graves', 70, NARANJA),
            ('2. Inercia de la cadena', 'el estribo queda atrás; pesa en medios', 140, NARANJA),
            ('3. Inercia de los líquidos', 'la más importante', 210, AZUL),
            ('4. Compresión de la cápsula', 'pesa en agudos', 280, AZUL),
            ('5. Presión del LCR', 'por el acueducto', 350, AZUL)]
    for tit, sub, y, col in vias:
        caja(c, 330, y - 23, 270, 46, f'{tit}|{sub}', '#fff', col, 10.5, col)
        flecha(c, 210, 220, 328, y, TENUE, 1.2)
        flecha(c, 600, y, 718, 220, col, 1.6)
    c.linea(30, 410, 60, 410, NARANJA, 2.5)
    c.t(66, 414, 'dependen del oído externo y medio: cambian con el conducto tapado o la platina fija', 10.5, NARANJA, 'start')
    c.t(460, 440, 'A partir de Stenfelt y Goode (2005); 1, 2 y 4 son los tres mecanismos clásicos (Tonndorf, 1966).', 10, TENUE)
    c.guardar('b2-mecanismos-co.svg')


def onda_viajera():
    c = L(960, 430)
    c.t(480, 26, 'La onda viajera en la cóclea desenrollada', 15, peso=700)
    x0, x1, yc = 130, 830, 210
    c.ruta(f'M{x0},{yc-8} L{x1},{yc-26} L{x1},{yc+26} L{x0},{yc+8} Z', '#e9f3d6', '#9ab36a', 1.2)
    c.t(x0 - 8, yc - 4, 'base', 11.5, peso=700, anchor='end')
    c.t(x0 - 8, yc + 12, 'angosta, rígida', 10, TENUE, 'end')
    c.t(x1 + 8, yc - 4, 'ápice', 11.5, peso=700, anchor='start')
    c.t(x1 + 8, yc + 12, 'ancha, flexible', 10, TENUE, 'start')

    def env(p, amp, col, nombre):
        pts = []
        for i in range(0, 201):
            u = i / 200
            x = x0 + (x1 - x0) * u
            if u <= p:
                a = amp * math.exp(-2.2 * ((p - u) / (0.32 * p + 0.02)) ** 2)
            else:
                a = amp * math.exp(-((u - p) / 0.035) ** 2)
            pts.append((x, a))
        d = 'M' + ' L'.join(f'{x:.1f},{yc - a:.1f}' for x, a in pts)
        d += ' L' + ' L'.join(f'{x:.1f},{yc + a:.1f}' for x, a in reversed(pts)) + ' Z'
        c.ruta(d, col, col, 1.2, extra='fill-opacity="0.18"')
        c.t(x0 + (x1 - x0) * p, yc - amp - 10, nombre, 11, col, peso=700)
    env(0.18, 70, ROJO, '8 kHz')
    env(0.50, 85, VIOLETA, '1 kHz')
    env(0.86, 95, AZUL, '125 Hz')
    c.linea(x0, 340, x1, 340, TENUE, 1)
    for u, s in ((0.0, '20 kHz'), (0.18, '8 kHz'), (0.35, '3 kHz'), (0.5, '1 kHz'), (0.7, '400 Hz'), (0.86, '125 Hz'), (1.0, '20 Hz')):
        x = x0 + (x1 - x0) * u
        c.linea(x, 340, x, 348, TENUE, 1)
        c.t(x, 364, s, 10, TENUE)
    c.t(480, 386, 'tonotopía: frecuencia característica a lo largo de la membrana basilar (aproximada)', 10.5, TENUE)
    c.t(480, 412, 'Toda onda pasa por la base antes de llegar a su lugar: la base trabaja más y se daña primero.', 11, ROJO, peso=600)
    c.guardar('b2-onda-viajera.svg')


def transduccion():
    c = L(960, 630)
    c.t(480, 26, 'Transducción mecanoeléctrica en una célula ciliada', 15, peso=700)
    c.rect(20, 44, 920, 196, '#eef6e2', '#c6dba6', 1, 8)
    c.t(40, 66, 'endolinfa: K⁺ alto, +80 mV', 11, '#5a7a2a', 'start', 600)

    def haz(cx, incl, titulo, estado, color, sub):
        alturas = (54, 78, 102)
        bases = (cx - 26, cx, cx + 26)
        tops = []
        for b, hgt in zip(bases, alturas):
            tx = b + incl * hgt / 100
            c.linea(b, 222, tx, 222 - hgt, '#7a6a3a', 9)
            tops.append((tx, 222 - hgt))
        for (ax, ay), (bx, by) in zip(tops[:-1], tops[1:]):
            tenso = incl > 0
            c.linea(ax, ay, bx - 4, by + 18, VIOLETA if tenso else TENUE, 1.8 if tenso else 1, None if tenso else '3 3')
            c.el(ax, ay, 4.5, 4.5, '#bbb' if estado == 'cerrado' else VERDE, '#333', 0.8)
        if estado == 'abierto':
            for ax, ay in tops[:-1]:
                flecha(c, ax, ay - 26, ax, ay - 7, ROJO, 1.4, punta=5)
            c.t(cx + 60, 110, 'entra K⁺', 10.5, ROJO, peso=600)
        c.t(cx, 256, titulo, 11, color, peso=700)
        c.t(cx, 272, sub, 10, TENUE)
    haz(160, 0, 'en reposo', 'parcial', TINTA, 'algunos canales abiertos')
    haz(480, 35, 'hacia el más alto', 'abierto', ROJO, 'enlaces tensos: excita')
    haz(800, -35, 'hacia el más corto', 'cerrado', AZUL, 'enlaces flojos: inhibe')
    c.t(480, 294, 'enlaces apicales (violeta) · canal de transducción (verde: abierto; gris: cerrado)', 10, TENUE)
    c.ruta('M380,320 L580,320 Q610,320 610,350 L610,520 Q610,560 570,560 L390,560 Q350,560 350,520 L350,350 Q350,320 380,320 Z',
           AMAR, AMAR2, 1.4)
    for x, y, s in ((372, 350, '1-4. entra K⁺ por arriba'), (372, 384, '5. despolarización'),
                    (372, 470, '6. entra Ca²⁺ por la base'), (372, 504, '→ vesículas con glutamato')):
        c.t(x, y, s, 10.5, TINTA, 'start')
    flecha(c, 480, 302, 480, 330, ROJO, 2)
    for i in range(4):
        c.el(500 + i * 18, 540, 6, 6, '#fff', VIOLETA, 1.2)
    c.ruta('M470,562 Q520,600 600,600', stroke=VERDE, w=3)
    c.t(606, 604, 'fibra del nervio (tipo I)', 10.5, VERDE, 'start')
    flecha(c, 612, 430, 700, 430, AZUL, 2)
    c.t(706, 425, '7. sale K⁺ a la perilinfa', 10.5, AZUL, 'start')
    c.t(706, 441, '→ vuelve a la estría (conexina 26)', 10, TENUE, 'start')
    c.t(706, 480, '8. adaptación: el Ca²⁺ cierra', 10.5, TINTA, 'start')
    c.t(706, 496, 'en parte los canales', 10.5, TINTA, 'start')
    c.t(170, 440, 'perilinfa: K⁺ bajo', 11, AZUL, peso=600)
    c.t(480, 624, 'A partir de Fettiplace (2017). En el vestíbulo, la célula se excita al doblar el haz hacia el kinocilio.', 10, TENUE)
    c.guardar('b2-transduccion.svg')


def codificacion():
    c = L(1000, 410)
    c.t(500, 26, 'Cómo codifica el nervio coclear', 15, peso=700)
    x0, y0, w, h = 70, 320, 250, 220
    ejes(c, x0, y0, w, h, 'frecuencia (escala log)', 'umbral (dB)')
    c.t(x0 + w / 2, 66, 'A. Lugar: curvas de sintonía', 12, peso=700)
    for cf, col in ((0.22, AZUL), (0.5, VIOLETA), (0.8, ROJO)):
        pts = []
        for i in range(101):
            u = i / 100
            d = u - cf
            thr = 20 + (130 * (-d) ** 1.1 if d < 0 else 520 * d ** 1.3)
            pts.append((x0 + w * u, y0 - min(thr, 200) * h / 200))
        c.ruta('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts), stroke=col, w=2)
    c.t(x0 + w / 2, y0 + 52, 'la punta marca la frecuencia característica', 10, TENUE)
    bx = 380
    c.t(bx + 130, 66, 'B. Tiempo: bloqueo de fase', 12, peso=700)
    pts = [(bx + i * 2.6, 170 - 40 * math.sin(i / 100 * 4 * 2 * math.pi)) for i in range(101)]
    c.ruta('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts), stroke=AZUL, w=2)
    c.t(bx + 130, 236, 'tono grave', 10, AZUL)
    for ciclo in (0, 1, 3):
        x = bx + (ciclo + 0.25) * 65
        c.linea(x, 128, x, 290, GRILLA, 1, '2 3')
        c.linea(x, 260, x, 290, ROJO, 2.4)
    c.linea(bx, 290, bx + 260, 290, TENUE, 1)
    c.t(bx + 130, 312, 'disparos (rojo): siempre en la misma fase,', 10, TENUE)
    c.t(bx + 130, 326, 'aunque no en cada ciclo', 10, TENUE)
    x0, y0, w, h = 720, 320, 250, 220
    ejes(c, x0, y0, w, h, 'intensidad (dB)', 'disparos/s')
    c.t(x0 + w / 2, 66, 'C. Intensidad', 12, peso=700)

    def sig(mid, lo, hi, col, nombre, ty):
        pts = []
        for i in range(101):
            r = lo + (hi - lo) / (1 + math.exp(-(i - mid) / 4.5))
            pts.append((x0 + w * i / 100, y0 - h * r / 300))
        c.ruta('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts), stroke=col, w=2.2)
        c.t(x0 + w - 4, ty, nombre, 10, col, 'end', 600)
    sig(20, 60, 250, ROJO, 'alta actividad espontánea', y0 - h * 270 / 300)
    sig(60, 2, 200, AZUL, 'baja actividad espontánea', y0 - h * 120 / 300)
    c.t(x0 + w / 2, y0 + 52, 'cada fibra cubre solo 20-30 dB', 10, TENUE)
    c.t(500, 400, 'Esquema a partir de Liberman (1978) y Johnson (1980); curvas aproximadas.', 10, TENUE)
    c.guardar('b2-codificacion.svg')


def binaural():
    c = L(940, 470)
    c.t(470, 26, 'Las dos pistas de la localización (fuente a la derecha)', 15, peso=700)

    def cabeza(cx, cy, titulo):
        c.t(cx + 60, 66, titulo, 12, peso=700)
        c.el(cx, cy, 70, 78, '#f7efe6', '#b89a80', 1.4)
        c.el(cx - 72, cy, 8, 16, '#f7efe6', '#b89a80', 1.2)
        c.el(cx + 72, cy, 8, 16, '#f7efe6', '#b89a80', 1.2)
        c.add(f'<polygon points="{cx-10},{cy-76} {cx+10},{cy-76} {cx},{cy-94}" fill="#f7efe6" stroke="#b89a80"/>')
        c.t(cx - 72, cy + 36, 'izq.', 10, TENUE)
        c.t(cx + 72, cy + 36, 'der.', 10, TENUE)
        c.el(cx + 190, cy, 9, 9, NARANJA, NARANJA)
        c.t(cx + 190, cy - 16, 'fuente', 10, NARANJA)
    cabeza(170, 200, 'A. Grave (&lt; 1,5 kHz): tiempo')
    for r in (30, 65, 100, 135):
        c.ruta(f'M{360},{200 - r} A {r} {r} 0 0 0 {360},{200 + r}', stroke=AZUL, w=1, dash='4 4')
    c.t(170, 320, 'la onda rodea la cabeza y llega', 10.5, AZUL)
    c.t(170, 334, 'antes al oído derecho (≤ 0,7 ms)', 10.5, AZUL)
    cabeza(620, 200, 'B. Agudo (&gt; 1,5 kHz): nivel')
    c.ruta('M548,160 L470,140 L470,260 L548,240 Z', '#d9d6e6', '#d9d6e6', 0.5, extra='fill-opacity="0.8"')
    c.t(505, 205, 'sombra', 10.5, VIOLETA, peso=600)
    for i in range(5):
        flecha(c, 800, 160 + i * 20, 700, 160 + i * 20, ROJO, 1.2, punta=5)
    c.t(620, 320, 'la cabeza hace sombra: el oído', 10.5, ROJO)
    c.t(620, 334, 'izquierdo recibe menos sonido', 10.5, ROJO)
    caja(c, 70, 362, 230, 56, 'oliva superior medial|compara el tiempo', CELE, CELE2, 11)
    caja(c, 520, 362, 230, 56, 'oliva superior lateral|compara el nivel', ROSA, ROSA2, 11)
    c.t(470, 456, 'Teoría dúplex: tiempo para los graves, nivel para los agudos. A partir de Grothe y cols. (2010).', 10, TENUE)
    c.guardar('b2-binaural.svg')


def ewald():
    c = L(1000, 430)
    c.t(500, 26, 'Las tres leyes de Ewald', 15, peso=700)

    def canal(cx, cy, titulo, sub, hacia_ampolla):
        c.t(cx, 64, titulo, 12, peso=700)
        c.el(cx, cy, 80, 80, 'none', CELE2, 14)
        c.el(cx + 80, cy, 18, 26, '#e9f3d6', '#9ab36a', 1.4)
        c.t(cx + 80, cy + 44, 'ampolla', 10, TENUE)
        c.linea(cx + 64, cy, cx + 96, cy, '#7a6a3a', 3)
        if hacia_ampolla:
            c.ruta(f'M{cx},{cy - 80} A 80 80 0 0 1 {cx + 66},{cy - 45}', stroke=ROJO, w=3)
            flecha(c, cx + 56, cy - 55, cx + 70, cy - 38, ROJO, 3)
        else:
            c.ruta(f'M{cx + 66},{cy + 45} A 80 80 0 0 1 {cx},{cy + 80}', stroke=ROJO, w=3)
            flecha(c, cx + 14, cy + 79, cx - 2, cy + 80, ROJO, 3)
        c.t(cx, cy + 4, 'excita', 11.5, ROJO, peso=700)
        c.t(cx, 290, sub, 10.5, TENUE)
    canal(140, 180, 'A. Canal lateral', 'flujo hacia la ampolla (ampulípeto)', True)
    canal(440, 180, 'B. Canal vertical', 'flujo que se aleja (ampulífugo)', False)
    x0, y0, w, h = 650, 290, 300, 210
    c.t(800, 64, 'C. Excitación &gt; inhibición', 12, peso=700)
    c.linea(x0, y0, x0 + w, y0, TINTA, 1)
    c.linea(x0 + w / 2, y0, x0 + w / 2, y0 - h, TINTA, 1)
    c.t(x0 + 20, y0 + 18, '← inhibe', 10, AZUL, 'start')
    c.t(x0 + w - 20, y0 + 18, 'excita →', 10, ROJO, 'end')
    c.t(x0 + w / 2, y0 + 36, 'velocidad de la cabeza', 10.5, TENUE)
    c.t(x0 + w / 2 + 6, y0 - h + 10, 'disparos/s', 10, TENUE, 'start')
    base = y0 - 80
    c.ruta(f'M{x0},{y0} L{x0 + 70},{y0} L{x0 + w / 2},{base} L{x0 + w},{y0 - h + 10}', stroke=VIOLETA, w=2.6)
    c.t(x0 + w / 2 - 8, base - 6, 'reposo', 10, TENUE, 'end')
    c.t(x0 + 10, y0 - 12, 'tope en 0', 10, AZUL, 'start')
    c.t(500, 346, '1. Los ojos se mueven en el plano del canal estimulado.', 11)
    c.t(500, 366, '2. Lateral: excita el flujo hacia la ampolla; verticales: el que se aleja.', 11)
    c.t(500, 386, '3. La excitación puede crecer mucho; la inhibición, solo hasta cero.', 11)
    c.t(500, 418, 'Esquema didáctico; las leyes, según Baloh y cols. (2011).', 10, TENUE)
    c.guardar('b2-ewald.svg')


def olfaccion():
    c = L(1000, 480)
    c.t(500, 26, 'Transducción olfatoria y vía hasta la corteza', 15, peso=700)
    c.t(500, 56, 'En el cilio de la neurona olfatoria', 12, peso=700)
    pasos = [('odorante', AMAR), ('receptor|olfatorio', CELE), ('proteína G|olfatoria', CELE),
             ('adenilato|ciclasa', CELE), ('AMP cíclico', CELE), ('canal catiónico|entra Na⁺, Ca²⁺', ROSA),
             ('canal de Cl⁻|sale Cl⁻', ROSA)]
    w, gap, x = 118, 22, 20
    for i, (s, col) in enumerate(pasos):
        caja(c, x, 76, w, 54, s, col, TINTA, 10)
        if i < len(pasos) - 1:
            flecha(c, x + w, 103, x + w + gap - 2, 103, TINTA, 1.4, punta=5)
        x += w + gap
    c.t(500, 156, 'despolarización → potencial de acción · el Ca²⁺ también produce adaptación', 11, ROJO, peso=600)
    c.linea(30, 180, 970, 180, GRILLA, 1.2)
    c.t(500, 206, 'La vía', 12, peso=700)
    via = [('neurona|olfatoria', VERD_C), ('lámina|cribosa', HUESO), ('glomérulo|(bulbo)', AMAR),
           ('célula|mitral', AMAR), ('tracto|olfatorio', '#fff')]
    x = 30
    for i, (s, col) in enumerate(via):
        caja(c, x, 226, 120, 54, s, col, TINTA, 10.5)
        if i < len(via) - 1:
            flecha(c, x + 120, 253, x + 148, 253, TINTA, 1.4, punta=5)
        x += 150
    for s, y in (('corteza piriforme', 300), ('amígdala', 360), ('corteza entorrinal', 420)):
        caja(c, 770, y - 20, 200, 40, s, ROSA, TINTA, 10.5)
        flecha(c, 720, 280, 768, y, TINTA, 1.2, punta=5)
    caja(c, 480, 380, 210, 46, 'corteza orbitofrontal|identifica el olor', '#fff', TINTA, 10.5)
    flecha(c, 768, 306, 692, 396, TENUE, 1.2, punta=5)
    c.t(220, 340, 'sin relevo obligatorio en el tálamo,', 11, VIOLETA, peso=600)
    c.t(220, 356, 'a diferencia de los demás sentidos', 11, VIOLETA, peso=600)
    c.t(500, 470, 'Esquema a partir de Buck y Axel (1991) y Kleene (2008).', 10, TENUE)
    c.guardar('b2-olfaccion.svg')


if __name__ == '__main__':
    print('dibujando B2...')
    resonancia_cae()
    adaptador()
    arco_estapedial()
    mecanismos_co()
    onda_viajera()
    transduccion()
    codificacion()
    binaural()
    ewald()
    olfaccion()
