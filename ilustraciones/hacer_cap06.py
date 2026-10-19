#!/usr/bin/env python3
"""Ilustración 6.1 del capítulo 6 (ruido). SVG propio, a mano, no IA:

    cap06-electromotilidad.svg   órgano de Corti en corte (izquierda) y una célula ciliada externa
                                 ampliada, acortada y alargada, con la prestina en su pared lateral (derecha)

Esquema didáctico, no a escala. El órgano de Corti repite el dibujo de `coclea_corte()` de
`hacer_b3.py` (misma paleta, grosores y forma de las células), ampliado, para que el capítulo 6 y B3
muestren las mismas células. El cambio de largo está exagerado: la célula real se mueve una fracción
de su largo (electromotilidad: Brownell y cols., 1985; prestina: Zheng y cols., 2000).
Los rótulos no van en el dibujo: son los globos numerados de la referencia en el capítulo."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
# L (el lienzo SVG) y la paleta salen de hacer_b3.py, que no se modifica.
from hacer_b3 import (AMAR, AMAR2, AZUL, HUESO, HUESO2, ROSA, ROSA2, TENUE, TINTA, VERDE,  # noqa: E402
                      VIOLETA, ROJO, L)

HAZ = '#a06020'        # estereocilios y placa cuticular, como en b3-ciliadas
PREST = '#6b3fa0'      # prestina (el violeta del libro)


def corti(c, S, TX, TY):
    """Órgano de Corti de `coclea_corte()` (mismas coordenadas), con los estereocilios dibujados."""
    c.add(f'<g transform="translate({TX},{TY}) scale({S})">')
    c.ruta('M300,215 L330,240 L330,262 L300,262 Z', '#f0d9c4', '#c9a98a', 1)                       # limbo
    c.ruta('M300,262 L300,300 L330,300 L330,262 Z', '#f0d9c4', '#c9a98a', 1)
    c.ruta('M300,300 L340,300 L340,308 L300,308 Z', HUESO, HUESO2, 1)
    c.ruta('M300,225 Q380,205 470,232 L474,244 Q400,228 330,248 L330,236 Z', '#d9d2e8', '#8a7fb0', 1.2)  # tectoria
    c.ruta('M300,308 L565,308', fill='none', stroke=AZUL, w=3)                                   # basilar
    c.ruta('M340,308 L340,262 L350,254 L372,254 L372,262 L396,262 L396,308 Z', '#f8e8c8', '#c9a56a', 1)
    c.ruta('M356,308 L370,262 L384,308 Z', '#fff', '#c9a56a', 1)                                 # túnel
    c.ruta('M340,262 L340,240 L350,236 L350,262 Z', AMAR, AMAR2, 1)                              # CCI
    c.ruta('M470,308 L470,266 L496,262 L506,308 Z', '#f0e6d8', '#c9a56a', 1)
    c.ruta('M506,308 L520,300 L550,297 L565,308 Z', '#f0e6d8', '#c9a56a', 1)
    for x in (405, 428, 451):
        c.ruta(f'M{x},266 L{x},238 L{x+13},238 L{x+13},266 Z', ROSA, ROSA2, 1)                   # CCE
        c.ruta(f'M{x+1},266 L{x-3},308 L{x+14},308 L{x+12},266 Z', '#f0e6d8', '#c9a56a', 1)      # Deiters
        for dx, h in ((1.5, 5), (4.5, 8), (8.5, 8), (11.5, 5)):                                  # haz en V
            c.linea(x + dx, 238, x + dx * 1.15 - 0.5, 238 - h, HAZ, 1.2)
    for dx, h in ((1, 4), (3.5, 6), (6, 8), (8.5, 6)):                                           # haz de la CCI
        c.linea(340 + dx, 238, 340 + dx, 238 - h, HAZ, 1.2)
    c.add('</g>')


def celula(c, cx, base, alto, nitido=True):
    """Una CCE ampliada: cilindro con su base fija (sobre la célula de Deiters) y el extremo libre
    arriba. `alto` es el largo del cilindro; la base queda fija y el que se mueve es el extremo."""
    top = base - alto
    ancho = 30
    dash = None if nitido else '5 4'
    c.ruta(f'M{cx-ancho},{top} L{cx-ancho},{base-26} Q{cx-ancho},{base} {cx},{base} '
           f'Q{cx+ancho},{base} {cx+ancho},{base-26} L{cx+ancho},{top} Z',
           ROSA if nitido else 'none', ROSA2, 2 if nitido else 1.4, dash)
    return top


def derecha(c, base):
    """Dos momentos de la misma CCE: acortada (izquierda) y alargada (derecha)."""
    cx1, cx2 = 735, 880
    largo, corto = 250, 205
    # la línea punteada marca hasta dónde llega la célula alargada
    t_largo = base - largo
    for cx, alto, nombre in ((cx1, corto, 'corta'), (cx2, largo, 'larga')):
        top = celula(c, cx, base, alto)
        c.el(cx, base - 34, 15, 18, '#d98a78', ROSA2, 1.2)                                # núcleo
        c.ruta(f'M{cx-30},{top} L{cx+30},{top}', stroke=HAZ, w=4)                         # placa cuticular
        for dx, h in ((-22, 22), (-7, 36), (7, 36), (22, 22)):                           # estereocilios en V
            c.linea(cx + dx, top, cx + dx * 1.35, top - h, HAZ, 3)
        # prestina en la pared lateral: puntos violeta a lo largo de las dos paredes
        n = 9 if nombre == 'larga' else 7
        paso = (alto - 90) / (n - 1)
        for i in range(n):
            y = top + 22 + i * paso
            for lado in (-1, 1):
                c.el(cx + lado * 30, y, 4.2, 6.5, PREST, '#fff', 0.8)
    # nivel de la célula alargada, marcado sobre la corta
    c.linea(cx1 - 60, t_largo, cx1 + 60, t_largo, TENUE, 1, '4 4')
    # flecha doble entre las dos posiciones del extremo libre
    xa = 808
    ya, yb = t_largo + 2, base - corto - 2
    c.linea(xa, ya, xa, yb, TINTA, 2)
    for y, s in ((ya, 1), (yb, -1)):
        c.ruta(f'M{xa-6},{y+s*10} L{xa},{y} L{xa+6},{y+s*10}', stroke=TINTA, w=2)
    return cx1, cx2, t_largo, ya, yb


def cap06_electromotilidad():
    c = L(980, 380)
    S, TX, TY = 1.9, -520, -190
    c.t(290, 30, 'Órgano de Corti', 15, peso=700)
    c.t(808, 30, 'Célula ciliada externa', 15, peso=700)
    c.add('<g transform="translate(0,-70)">')     # sube el dibujo: debajo de los títulos no sobra aire
    corti(c, S, TX, TY)
    # la CCE central del corte (x 428-441) se amplía a la derecha
    x0, y0 = S * 428 + TX, S * 238 + TY
    x1, y1 = S * 441 + TX, S * 308 + TY
    base = 420
    derecha(c, base)
    c.linea(x1 + 4, y0, 700, base - 250, TENUE, 1, '3 4')
    c.linea(x1 + 4, y1, 700, base, TENUE, 1, '3 4')
    c.add('</g>')
    c.guardar('cap06-electromotilidad.svg')
    return c, (x0, y0, x1, y1)


if __name__ == '__main__':
    print('dibujando cap. 6...')
    cap06_electromotilidad()
