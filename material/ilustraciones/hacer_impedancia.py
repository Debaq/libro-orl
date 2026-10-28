#!/usr/bin/env python3
"""Ilustraciones de impedanciometría (caps. 2 y 3, H7). SVG propios, no IA:

    h7-etf-integra.svg     función tubaria con membrana íntegra: los tres timpanogramas
                           (reposo, tras tragar con +400 y con −400 daPa); A, la trompa abre; B, no abre
    h7-etf-perforada.svg   función tubaria con membrana perforada: la presión del conducto en 10 s,
                           con tres degluciones; la trompa que abre y la que no
    h7-decay.svg           deterioro del reflejo: contracción sostenida (negativo) y la que cae
                           a menos de la mitad (positivo)

Reemplazan las capturas de LabSim (2026-10-19): para mostrar la curva no hace falta el equipo.
Las curvas son esquemas. Las cifras de A del primero (−18, −23 y −11 daPa) y la subida de −200 a −10
daPa del segundo son las de las capturas que reemplazan."""
import math
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from hacer_h13 import AVISO, COCLEAR, FUERTE, GRILLA, RETRO, TENUE, TINTA, Lienzo  # noqa: E402
import hacer_h13  # noqa: E402

hacer_h13.ESCALA = 1.45

AZUL = '#2c5cb0'
FRANJA = '#f4efe4'


def ruido(n, semilla, sigma):
    random.seed(semilla)
    crudo = [random.gauss(0, sigma) for _ in range(n + 6)]
    return [sum(crudo[i:i + 7]) / 7 for i in range(n)]


def ejes(c, x0, x1, ytop, ybot, xs, ys, fx, fy, rot_x, rot_y):
    """Grilla, marcas y rótulos de un panel."""
    for v in xs:
        c.l(fx(v), ytop, fx(v), ybot, GRILLA, 1)
        c.t(fx(v), ybot + 14, f'{v:g}'.replace('-', '−').replace('.', ','), 7.6, TENUE)
    for v in ys:
        c.l(x0, fy(v), x1, fy(v), GRILLA, 1)
        c.t(x0 - 5, fy(v) + 3, f'{v:g}'.replace('-', '−').replace('.', ','), 7.6, TENUE, 'end')
    c.l(x0, ybot, x1, ybot, FUERTE, 1)
    c.l(x0, ytop, x0, ybot, FUERTE, 1)
    c.t(x1, ybot + 29, rot_x, 8, TENUE, 'end')
    c.t(x0 - 5, ytop - 7, rot_y, 8, TENUE, 'end', 600)


def timpanograma(p, pico, alto=0.4, ancho=55):
    return alto * math.exp(-((p - pico) / ancho) ** 2)


def etf_integra():
    """Con el dibujo del timpanograma de la hoja de impedanciometría del tomo II
    (figuras/motor/impedancia_hoja.py: misma grilla de -400 a 200 daPa, letra en
    negro), en vez del esquema propio (él, 2026-10-21). Letra grande: la figura
    va a todo el ancho y así impresa no baja de 7 pt."""
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / 'figuras'))
    from motor import estilo as E
    from motor.svg import Svg
    TT, TR = 11, 10
    pw, ph, ml, mt, sep = 250, 150, 40, 44, 56
    escala = 0.6
    x_min, x_max = -400, 200
    curvas = (('reposo', E.TINTA), ('tras +400', COCLEAR), ('tras −400', RETRO))
    paneles = (('A · La trompa abre', (-18, -23, -11), 'el pico se corre al lado contrario'),
               ('B · La trompa no abre', (-150, -151, -149), 'los tres picos quedan juntos'))
    s = Svg(ml + 2 * pw + sep + 14, mt + ph + 74)
    for k, (titulo, picos, nota) in enumerate(paneles):
        x0 = ml + k * (pw + sep)

        def X(p, x0=x0):
            return x0 + (p - x_min) / (x_max - x_min) * pw

        def Y(v):
            return mt + ph - max(0.0, min(escala, v)) / escala * ph
        s.texto(x0, mt - 26, titulo, TT, E.TINTA, 'start', 700)
        for p in range(x_min, x_max + 1, 100):
            s.linea(X(p), mt, X(p), mt + ph, E.GRILLA_FUERTE if p == 0 else E.GRILLA, 1)
            s.texto(X(p), mt + ph + 13, f'{p}'.replace('-', '−'), TR, E.TINTA)
        for i in range(0, int(escala * 10) + 1, 2):
            v = i / 10
            s.linea(x0, Y(v), x0 + pw, Y(v), E.GRILLA, 1)
            s.texto(x0 - 5, Y(v) + 3.5, f'{v:.1f}'.replace('.', ','), TR, E.TINTA, 'end')
        s.texto(x0 + pw / 2, mt + ph + 27, 'Presión (daPa)', TR, E.TINTA)
        s.texto(x0 - 30, mt + ph / 2, 'mL', TR, E.TINTA, extra=f'transform="rotate(-90 {x0 - 30} {mt + ph / 2:.1f})"')
        for j, ((nombre, color), pico) in enumerate(zip(curvas, picos)):
            rr = ruido(301, 10 * k + j, 0.004)
            pts = [(X(-400 + i * 2), Y(timpanograma(-400 + i * 2, pico) + rr[i])) for i in range(301)]
            s.trazo(pts, color, E.LINEA)
            # la presión de cada pico, escalonada para que no se monten
            y = Y(0.4) - 6 - 13 * j
            s.linea(X(pico), Y(0.4) - 3, X(pico), y + 2, color, 0.8)
            s.texto(X(pico) + (6 if j != 1 else -6), y, f'{pico}'.replace('-', '−'), TR, color,
                    'start' if j != 1 else 'end', 700)
        s.texto(x0 + pw / 2, mt + ph + 45, nota, TR, E.TINTA, 'middle', 600)
    xl = ml + 60
    for j, (nombre, color) in enumerate(curvas):
        s.linea(xl + j * 130, mt + ph + 64, xl + j * 130 + 22, mt + ph + 64, color, 2.2)
        s.texto(xl + j * 130 + 28, mt + ph + 68, nombre, TR, E.TINTA, 'start', 600)
    (pathlib.Path(__file__).resolve().parent / 'h7-etf-integra.svg').write_text(s.svg(), encoding='utf-8')


def etf_perforada():
    c = Lienzo(760, 290)
    x0, x1, ytop, ybot = 70, 600, 40, 230
    fx = lambda t: x0 + t / 10 * (x1 - x0)
    fy = lambda p: ytop + (100 - p) / 350 * (ybot - ytop)
    ejes(c, x0, x1, ytop, ybot, (0, 2, 4, 6, 8, 10), (100, 0, -100, -200), fx, fy, 'segundos', 'daPa')
    tragos = (2.5, 5, 7.5)
    for t in tragos:
        c.l(fx(t), ytop, fx(t), ybot, TENUE, 1, '4 3')
        c.t(fx(t) + 4, ytop + 11, 'traga', 7.6, TENUE, 'start', 600)
    niveles = (-200, -75, -30, -10)

    def abre(t):
        p = niveles[0]
        for i, tt in enumerate(tragos):
            if t >= tt:
                p = niveles[i + 1] + (niveles[i] - niveles[i + 1]) * math.exp(-(t - tt) / 0.15)
        return p
    n = 500
    rr = ruido(n + 1, 3, 2.2)
    c.poli([(fx(i / n * 10), fy(abre(i / n * 10) + rr[i])) for i in range(n + 1)], RETRO, 1.9)
    rr = ruido(n + 1, 4, 2.2)
    c.poli([(fx(i / n * 10), fy(-200 + rr[i])) for i in range(n + 1)], AVISO, 1.9)
    c.t(x1 + 10, fy(-10) + 4, 'abre: sube', 8.4, RETRO, 'start', 700)
    c.t(x1 + 10, fy(-10) + 18, 'por escalones', 8.4, RETRO, 'start', 700)
    c.t(x1 + 10, fy(-200) + 4, 'no abre: plana', 8.4, AVISO, 'start', 700)
    c.t(x0, 280, 'El conducto y la caja, una sola cavidad, parten en −200 daPa.', 8, TENUE, 'start')
    c.guardar('h7-etf-perforada.svg')


def decay():
    c = Lienzo(760, 330)
    x0, x1 = 150, 690
    fx = lambda t: x0 + t / 12 * (x1 - x0)
    alto, top0 = 118, 40
    filas = (('Negativo', 'se sostiene: 94 % a los 10 s', lambda u: 1 - 0.006 * u, RETRO),
             ('Positivo', 'cae a menos de la mitad', lambda u: math.exp(-u / 3.2), AVISO))
    amp = 70
    for k, (nombre, detalle, env, color) in enumerate(filas):
        top = top0 + k * alto
        yb = top + 14
        if k:
            c.l(14, top - 8, x1, top - 8, GRILLA, 1)
        c.out.append(f'<rect x="{fx(1):.1f}" y="{top}" width="{fx(11) - fx(1):.1f}" height="{amp + 24}" fill="{FRANJA}"/>')
        c.t(14, top + 38, nombre, 9.6, color, 'start', 700)
        c.t(14, top + 54, detalle, 7.8, TENUE, 'start', 600)
        c.l(x0, yb, x1, yb, FUERTE, 0.8, '4 3')
        # la mitad de la amplitud inicial: el corte del positivo
        c.l(fx(1), yb + amp / 2, fx(11), yb + amp / 2, AVISO, 1, '2 3')
        if k == 0:
            c.t(fx(11) - 4, yb + amp / 2 - 4, '50 %', 7.4, AVISO, 'end', 600)
        for t in (6, 11):
            c.l(fx(t), top, fx(t), top + amp + 24, TENUE, 0.8, '4 3')
        n = 600
        rr = ruido(n + 1, 20 + k, 1.6)
        pts = []
        for i in range(n + 1):
            t = i / n * 12
            if 1 <= t <= 11:
                flanco = min(1, (t - 1) / 0.06, (11 - t) / 0.06)
                d = amp * env(t - 1) * flanco
            else:
                d = 0
            pts.append((fx(t), yb + d + rr[i]))
        c.poli(pts, color, 1.8)
    y_eje = top0 + 2 * alto
    c.l(x0, y_eje, x1, y_eje, FUERTE, 1)
    for t, s in ((0, '0'), (1, '1'), (6, '6 · 5 s de tono'), (11, '11 · 10 s'), (12, '12')):
        c.l(fx(t), y_eje, fx(t), y_eje + 4, FUERTE, 1)
        c.t(fx(t), y_eje + 15, s, 7.6, TENUE)
    c.t(x1, y_eje + 30, 'segundos (el tono suena de 1 a 11)', 8, TENUE, 'end')
    c.guardar('h7-decay.svg')


if __name__ == '__main__':
    etf_integra()
    etf_perforada()
    decay()
