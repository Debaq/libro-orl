#!/usr/bin/env python3
"""Ilustración 10.1 del capítulo 10 (hipoacusias genéticas). SVG propio, a mano, no IA:

    cap10-potasio.svg    pared lateral de la cóclea en corte: el circuito del potasio (endolinfa, célula
                         ciliada, células de sostén, ligamento espiral, estría vascular, endolinfa)

Esquema didáctico, no a escala. Repite el corte de `coclea_corte()` de `hacer_b3.py` (misma paleta, mismas
coordenadas del órgano de Corti, de las membranas, de las escalas, del ligamento espiral y de la estría),
ampliado y recortado a la pared lateral. Para que se vean las tres capas de la estría y las cadenas de
células, la estría y el ligamento se ensanchan, y se omite la membrana tectoria para que el potasio llegue
a los estereocilios; el resto de las formas es el de B3. Un solo color para el potasio en todo el
recorrido; las uniones gap (conexina 26) van en verde, como "uniones comunicantes" en B3.
Circuito: Wangemann (2006); Kikuchi y cols. (1995, 2000); Zdebik y cols. (2009); Hibino y cols. (2010).
Los rótulos no van en el dibujo, salvo los esenciales: son los globos numerados de la referencia en el capítulo."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
# L (el lienzo SVG) y la paleta salen de hacer_b3.py, que no se modifica.
from hacer_b3 import (AMAR, AMAR2, AZUL, CELE, CELE2, HUESO, HUESO2, ROSA, ROSA2, TENUE,  # noqa: E402
                      TINTA, VERDE, VIOLETA, L)

HAZ = '#a06020'        # estereocilios, como en b3-ciliadas
K = '#c2185b'          # potasio: un solo color en todo el recorrido
W, H = 980, 500
S, TX, TY = 2.0, -550, -220      # del dibujo de B3 a este lienzo: recorta x 300-750, y 110-350


def P(x, y):
    return S * x + TX, S * y + TY


def camino(c, pts, r=6, punta=True):
    """Polilínea de esquinas redondeadas (coordenadas de B3) con halo blanco y punta de flecha al final."""
    q = [P(*p) for p in pts]
    rr = r * S
    d = f'M{q[0][0]:.1f},{q[0][1]:.1f}'
    for i in range(1, len(q) - 1):
        (x0, y0), (x1, y1), (x2, y2) = q[i - 1], q[i], q[i + 1]
        n0 = max(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** .5, 1e-6)
        n1 = max(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5, 1e-6)
        d += (f' L{x1 - (x1 - x0) / n0 * rr:.1f},{y1 - (y1 - y0) / n0 * rr:.1f}'
              f' Q{x1:.1f},{y1:.1f} {x1 + (x2 - x1) / n1 * rr:.1f},{y1 + (y2 - y1) / n1 * rr:.1f}')
    d += f' L{q[-1][0]:.1f},{q[-1][1]:.1f}'
    c.ruta(d, stroke='#fff', w=7, extra='opacity="0.75"')
    c.ruta(d, stroke=K, w=3.2)
    if punta:
        cabeza(c, q[-1], q[-1][0] - q[-2][0], q[-1][1] - q[-2][1])


def cabeza(c, fin, dx, dy):
    """Punta de flecha rellena en `fin` (pantalla), apuntando en la dirección (dx, dy)."""
    n = (dx * dx + dy * dy) ** .5
    ux, uy = dx / n, dy / n
    x, y = fin
    c.ruta(f'M{x:.1f},{y:.1f} L{x - 11 * ux + 6 * uy:.1f},{y - 11 * uy - 6 * ux:.1f} '
           f'L{x - 11 * ux - 6 * uy:.1f},{y - 11 * uy + 6 * ux:.1f} Z', fill=K, stroke=K, w=1)


def chevron(c, x, y, dx, dy):
    """Pequeña flecha abierta a mitad de camino (x, y en coordenadas de B3), para que se lea el sentido."""
    px, py = P(x, y)
    n = (dx * dx + dy * dy) ** .5
    ux, uy = dx / n, dy / n
    c.ruta(f'M{px - 7 * ux + 6 * uy:.1f},{py - 7 * uy - 6 * ux:.1f} L{px + 4 * ux:.1f},{py + 4 * uy:.1f} '
           f'L{px - 7 * ux - 6 * uy:.1f},{py - 7 * uy + 6 * ux:.1f}', stroke=K, w=3)


def union(c, x, y, vertical=False):
    """Unión gap entre dos células vecinas: dos barras cruzadas por el canal (x, y en coord. de B3).
    `vertical` es para un paso hacia arriba o abajo; si no, el paso es de izquierda a derecha."""
    px, py = P(x, y)
    if vertical:
        for dy in (-2.6, 2.6):
            c.linea(px - 8, py + dy, px + 8, py + dy, VERDE, 2.2)
        c.linea(px, py - 2.6, px, py + 2.6, VERDE, 2.2)
    else:
        for dx in (-2.6, 2.6):
            c.linea(px + dx, py - 8, px + dx, py + 8, VERDE, 2.2)
        c.linea(px - 2.6, py, px + 2.6, py, VERDE, 2.2)


def pared(c):
    """Escalas, ligamento, estría y órgano de Corti con las coordenadas de `coclea_corte()` (B3)."""
    c.add(f'<g transform="translate({TX},{TY}) scale({S})">')
    c.ruta('M734,110 L752,110 L752,350 L734,350 Z', HUESO, HUESO2, 1)                              # pared ósea
    c.ruta('M636,150 L734,130 L734,330 L636,330 Z', '#f0d9c4', '#c9a98a', 1)                       # ligamento espiral
    c.ruta('M300,110 L734,110 L734,130 L636,150 L300,215 Z', CELE, CELE2, 1)                       # vestibular
    c.ruta('M300,310 L636,310 L636,330 L734,330 L734,350 L300,350 Z', CELE, CELE2, 1)              # timpánica
    c.ruta('M300,215 L636,150 L636,310 L300,310 Z', '#e9f3d6', '#9ab36a', 1)                       # media
    c.ruta('M300,215 L636,150', fill='none', stroke=VIOLETA, w=2.2)                                # Reissner
    c.ruta('M300,215 L330,240 L330,262 L300,262 Z', '#f0d9c4', '#c9a98a', 1)                       # limbo
    c.ruta('M300,262 L300,300 L330,300 L330,262 Z', '#f0d9c4', '#c9a98a', 1)
    c.ruta('M300,300 L340,300 L340,308 L300,308 Z', HUESO, HUESO2, 1)
    # estría: tres capas (marginal hacia la endolinfa, intermedia con melanocitos, basal hacia el ligamento)
    c.ruta('M636,152 L652,150 L652,290 L636,290 Z', '#e8a87c', '#b5683a', 1.2)
    c.ruta('M652,150 L668,149 L668,290 L652,290 Z', '#d98c5a', '#b5683a', 1.2)
    c.ruta('M668,149 L684,148 L684,290 L668,290 Z', '#f1c7a4', '#b5683a', 1.2)
    for i, (x, y) in enumerate(((657, 166), (662, 186), (656, 206), (663, 226), (657, 272), (662, 160),
                                (658, 296 - 40), (661, 236), (656, 176))):
        c.el(x, y, 2.6, 2.2, '#7a3b1d', '#7a3b1d', 0.5)                                            # melanina
    for yy in (172, 210, 270):
        c.el(676, yy, 5, 8, '#c62f3a', '#8a1d26', 0.8)                                             # capilares
    c.ruta('M300,308 L636,308', fill='none', stroke=AZUL, w=3)                                     # basilar
    # órgano de Corti (como en B3, sin tectoria)
    c.ruta('M340,308 L340,262 L350,254 L372,254 L372,262 L396,262 L396,308 Z', '#f8e8c8', '#c9a56a', 1)
    c.ruta('M356,308 L370,262 L384,308 Z', '#fff', '#c9a56a', 1)                                   # túnel
    c.ruta('M340,262 L340,240 L350,236 L350,262 Z', AMAR, AMAR2, 1)                                # CCI
    for dx, h in ((1, 4), (3.5, 6), (6, 8), (8.5, 6)):
        c.linea(340 + dx, 238, 340 + dx, 238 - h, HAZ, 1.2)
    for x in (405, 428, 451):
        c.ruta(f'M{x},266 L{x},238 L{x+13},238 L{x+13},266 Z', ROSA, ROSA2, 1)                     # CCE
        c.ruta(f'M{x+1},266 L{x-3},308 L{x+14},308 L{x+12},266 Z', '#f0e6d8', '#c9a56a', 1)        # Deiters
        for dx, h in ((1.5, 5), (4.5, 8), (8.5, 8), (11.5, 5)):
            c.linea(x + dx, 238, x + dx * 1.15 - 0.5, 238 - h, HAZ, 1.2)
    c.ruta('M470,308 L470,266 L496,262 L506,308 Z', '#f0e6d8', '#c9a56a', 1)                       # Hensen
    c.ruta('M506,308 L520,292 L560,288 L610,288 L636,292 L636,308 Z', '#f0e6d8', '#c9a56a', 1)     # Claudius y surco externo
    c.linea(590, 288, 590, 308, '#c9a56a', 1)
    # fibrocitos del ligamento: la cadena del potasio y unos pocos más, sin flechas
    for (x, y, rx, ry) in ((649, 300, 12, 10), (673, 300, 12, 10), (697, 300, 12, 10), (720, 300, 10, 13),
                           (720, 274, 10, 13), (720, 248, 10, 13), (698, 248, 12, 11)):
        c.el(x, y, rx, ry, '#e6c4a0', '#b58a60', 1)
    for y in (225, 199, 173):
        c.el(720, y, 10, 13, '#ead3bb', '#c9a98a', 1)
    c.add('</g>')


def cap10_potasio():
    c = L(W, H)
    pared(c)
    # Recorrido del potasio, en coordenadas de B3. Entra por los estereocilios, sale por la base,
    # cruza las células de sostén y el ligamento, sube a la estría y vuelve a la endolinfa.
    camino(c, [(434.5, 250), (434.5, 300), (632, 300)], punta=False)                  # base -> sostén
    camino(c, [(632, 300), (720, 300), (720, 248), (640, 248)], punta=False)          # ligamento -> estría
    # de la estría de vuelta a la endolinfa y a los estereocilios (curva que cierra el circuito)
    x0, y0 = P(636, 248)
    d = (f'M{x0:.1f},{y0:.1f} C{P(600, 248)[0]:.1f},{P(600, 248)[1]:.1f} {P(520, 226)[0]:.1f},{P(520, 226)[1]:.1f} '
         f'{P(468, 214)[0]:.1f},{P(468, 214)[1]:.1f} C{P(450, 210)[0]:.1f},{P(450, 210)[1]:.1f} '
         f'{P(436, 214)[0]:.1f},{P(436, 214)[1]:.1f} {P(434.5, 224)[0]:.1f},{P(434.5, 224)[1]:.1f}')
    c.ruta(d, stroke='#fff', w=7, extra='opacity="0.75"')
    c.ruta(d, stroke=K, w=3.2)
    cabeza(c, P(434.5, 227), 0, 1)
    # sentido del recorrido a mitad de cada tramo
    chevron(c, 434.5, 286, 0, 1)
    chevron(c, 548, 300, 1, 0)
    chevron(c, 616, 300, 1, 0)
    chevron(c, 720, 277, 0, -1)
    chevron(c, 668, 248, -1, 0)
    ax, ay = P(540, 229)
    chevron(c, 540, 229, -1, -0.25)
    # uniones gap: red 1 (epitelio del órgano de Corti) y red 2 (conectivo: ligamento y estría)
    for x in (444, 467, 506, 590):
        union(c, x, 300)
    for x, y, v in ((661, 300, False), (685, 300, False), (710, 300, False), (720, 287, True),
                    (720, 261, True), (710, 248, False), (686, 248, False)):
        union(c, x, y, v)
    # canal KCNQ1/KCNE1 en la cara de la célula marginal que da a la endolinfa
    px, py = P(636, 248)
    c.rect(px - 5, py - 12, 10, 24, '#fff', AZUL, 2, 4)
    c.linea(px - 5, py, px + 5, py, AZUL, 1.5)
    # rótulos esenciales
    c.t(*P(548, 262), '+80 mV', 15, K, peso=700)
    c.t(*P(548, 278), 'endolinfa', 11.5, '#5a7a2a')
    c.t(*P(470, 128), 'perilinfa', 11.5, TENUE)
    c.t(*P(470, 338), 'perilinfa', 11.5, TENUE)
    c.guardar('cap10-potasio.svg')
    return c


if __name__ == '__main__':
    print('dibujando cap. 10...')
    cap10_potasio()
    for nombre, (x, y) in {'ent': (434.5, 224), 'base': (434.5, 285), 'sosten': (506, 300), 'lig': (720, 274),
                           'estria': (660, 230), 'kcnq': (636, 248), 'mv': (548, 262), 'cci': (345, 250)}.items():
        px, py = P(x, y)
        print(f'  {nombre}: @{px / W * 100:.1f},{py / H * 100:.1f}')
