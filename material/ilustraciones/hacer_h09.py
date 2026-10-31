#!/usr/bin/env python3
"""Esquema de la herramienta H9 (emisiones otoacústicas). SVG propio, no IA:

    h09-sonda.svg  la sonda de OEA puesta: la oliva sella el conducto; dos parlantes (f1 y f2)
                   y un micrófono abren frente al tímpano; el estímulo entra hasta la cóclea y
                   la emisión vuelve, más débil, por el mismo camino

Corte longitudinal del conducto, de afuera (izquierda) hacia la cóclea (derecha). Esquema, no a
escala. TEOAE usa un parlante y DPOAE los dos (f1 y f2), como dice el capítulo."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from hacer_h02_esquemas import HUESO, HUESO_CLARO, TINTA_2, camino, espiral, rect  # noqa: E402
from hacer_h04_esquemas import GRIS_FONO, flecha, punta  # noqa: E402
from hacer_h13 import COCLEAR, RETRO, TENUE, TINTA, Lienzo  # noqa: E402

OLIVA = '#f1d9a6'


def sonda():
    c = Lienzo(820, 300)
    defs = punta('p-c', COCLEAR, 10) + punta('p-r', RETRO, 7) + punta('p-t', TENUE, 6)
    c.t(14, 20, 'La sonda de OEA puesta (corte del conducto, de afuera hacia la cóclea)', 10.5, TINTA, 'start', 700)
    yc = 170
    x_ent, x_tim, x_ve = 300, 520, 616       # entrada del conducto, tímpano, ventana oval
    # hueso y piel alrededor del conducto y del oído medio
    rect(c, x_ent, yc - 110, 400, 220, HUESO_CLARO, HUESO, 1.2, 12)
    c.l(x_ent, yc - 110, x_ent, yc + 110, TINTA_2, 1.4)
    # luz del conducto, que se angosta hacia el tímpano
    camino(c, f'M{x_ent - 1},{yc - 34} L{x_tim},{yc - 26} L{x_tim},{yc + 26} L{x_ent - 1},{yc + 34} Z',
           '#ffffff', 'none', 0)
    c.l(x_ent, yc - 34, x_tim, yc - 26, TINTA_2, 1.1)
    c.l(x_ent, yc + 34, x_tim, yc + 26, TINTA_2, 1.1)
    # oído medio y cóclea
    rect(c, x_tim, yc - 62, x_ve - x_tim, 112, '#ffffff', 'none', 0, 8)
    c.l(x_tim - 6, yc - 30, x_tim + 6, yc + 30, TINTA, 2.4)                       # tímpano
    c.poli([(x_tim + 2, yc + 4), (x_tim + 16, yc - 34), (x_tim + 36, yc - 40)], TINTA_2, 3)   # martillo
    c.poli([(x_tim + 36, yc - 40), (x_tim + 56, yc - 36), (x_tim + 62, yc - 14)], TINTA_2, 3)  # yunque
    c.poli([(x_tim + 62, yc - 14), (x_ve - 8, yc - 14)], TINTA_2, 3)                            # estribo
    c.l(x_ve - 6, yc - 26, x_ve - 6, yc - 2, TINTA_2, 3)                                         # platina
    espiral(c, x_ve + 44, yc - 14, 30, COCLEAR, '#fbe9dc')
    # la sonda: cuerpo, cable y oliva
    rect(c, 150, yc - 22, 120, 44, '#ffffff', GRIS_FONO, 1.6, 6)
    camino(c, f'M150,{yc + 14} C110,{yc + 14} 110,{yc + 80} 60,{yc + 80}', 'none', GRIS_FONO, 4)
    # la oliva llena la entrada: toca las dos paredes
    camino(c, f'M262,{yc - 38} L{x_ent},{yc - 34} L{x_ent + 46},{yc - 32} Q{x_ent + 56},{yc} {x_ent + 46},{yc + 32} '
              f'L{x_ent},{yc + 34} L262,{yc + 38} Z', OLIVA, '#b8954f', 1.4)
    # los tres tubos: dos parlantes y el micrófono
    for y, col in ((yc - 14, COCLEAR), (yc, COCLEAR), (yc + 14, RETRO)):
        c.l(170, y, x_ent + 52, y, col, 3.4)
    c.t(210, yc - 48, 'parlante 1 (f1)', 8.2, COCLEAR, 'middle', 700)
    c.l(210, yc - 42, 210, yc - 15, TENUE, 0.8)
    c.t(142, yc + 4, 'parlante 2 (f2)', 8.2, COCLEAR, 'end', 700)
    c.l(144, yc, 168, yc, TENUE, 0.8)
    c.t(222, yc + 56, 'micrófono', 8.2, RETRO, 'middle', 700)
    c.l(222, yc + 45, 222, yc + 15, TENUE, 0.8)
    # ida: el estímulo cruza el conducto, el tímpano y la cadena hasta la cóclea
    flecha(c, f'M{x_ent + 62},{yc - 8} L{x_tim - 12},{yc - 8}', COCLEAR, 5, 'p-c')
    flecha(c, f'M{x_tim + 10},{yc - 56} L{x_ve + 8},{yc - 56} Q{x_ve + 44},{yc - 56} {x_ve + 44},{yc - 50}',
           COCLEAR, 3.4, 'p-c')
    # vuelta: la emisión sale de la cóclea, cruza la cadena y el tímpano y llega al micrófono
    flecha(c, f'M{x_ve + 10},{yc + 28} L{x_tim + 12},{yc + 28}', RETRO, 1.6, 'p-r')
    flecha(c, f'M{x_tim - 12},{yc + 12} L{x_ent + 62},{yc + 12}', RETRO, 1.6, 'p-r')
    # rótulos
    c.t(x_ent + 152, yc - 48, 'estímulo (f1 y f2)', 8.2, COCLEAR, 'middle', 700)
    c.t(x_ent + 152, yc + 52, 'emisión: vuelve más débil', 8.2, RETRO, 'middle', 700)
    c.t(x_tim + 48, yc + 66, 'la emisión cruza', 8.2, TINTA, 'middle', 700)
    c.t(x_tim + 48, yc + 78, 'aquí dos veces', 8.2, TINTA, 'middle', 700)
    c.t(x_tim, yc - 118, 'tímpano', 8, TINTA_2, 'middle', 600)
    c.l(x_tim, yc - 112, x_tim - 2, yc - 32, TENUE, 0.8)
    c.t(x_tim + 48, yc - 72, 'oído medio', 8, TENUE, 'middle', 600)
    c.t(x_ve + 44, yc + 34, 'cóclea', 8, COCLEAR, 'middle', 700)
    c.t(x_ent + 110, yc + 88, 'conducto auditivo externo', 8, TENUE, 'middle', 600)
    c.l(x_ent + 110, yc + 76, x_ent + 110, yc + 33, TENUE, 0.8)
    c.t(x_ent + 22, yc - 130, 'oliva: sella la entrada', 8.2, '#8a6a2c', 'middle', 700)
    c.l(x_ent + 22, yc - 124, x_ent + 20, yc - 30, TENUE, 0.8)
    c.t(60, yc + 98, 'al equipo', 8, TENUE, 'middle', 600)
    c.guardar('h09-sonda.svg', defs)


if __name__ == '__main__':
    sonda()
