#!/usr/bin/env python3
"""Ilustración del capítulo 4 (rigidez). SVG propio, no IA:

    04-formas-reflejo.svg  las cuatro formas de la curva del reflejo estapedial en el tiempo
                           (normal, ON-OFF, OFF e invertido), una bajo la otra, con el tono marcado

Esquema. Las formas son las del impedanciómetro de LabSim (Reflex_curve en
src/impedanciometria/z_generator.py), para que el dibujo calce con lo que el alumno ve en el equipo:
traza de 2 s, tono de 1 s desde los 0,5 s, flancos de 50 ms en la meseta normal e invertida, picos
de 150 ms en el ON-OFF (con el leve abombamiento del medio) y pico de 150 ms tras apagar el tono en
el OFF. La amplitud es la de LabSim a 10 dB sobre el umbral (0,055 mL). Deflexión hacia abajo = baja
la admitancia; la mínima que cuenta es 0,02 mL (BSA, 2024), como dice el capítulo."""
import math
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from hacer_h13 import AVISO, COCLEAR, FUERTE, GRILLA, RETRO, TENUE, TINTA, Lienzo  # noqa: E402
import hacer_h13  # noqa: E402

hacer_h13.ESCALA = 1.55   # letra más grande: el dibujo va casi a todo el ancho de la página

FRANJA = '#f4efe4'        # sombreado del tiempo en que suena el tono

# tiempos de la traza (s), los de LabSim
DURACION, INICIO, LARGO_TONO = 2.0, 0.5, 1.0
FIN = INICIO + LARGO_TONO


def amplitud(exceso_db=10):
    """Deflexión en mL según cuántos dB sobre el umbral se estimula (fórmula de LabSim)."""
    return 0.1 * min(1.0, 0.3 + exceso_db / 40)


def forma(t, tipo, amp):
    """Cambio de admitancia (mL) en el instante t para cada forma de curva."""
    tt = (t - INICIO) / LARGO_TONO          # 0 a 1 mientras suena el tono
    if tipo == 'off':
        # plana todo el tono; recién al apagarlo cae y vuelve sola a la base en 150 ms
        tp = (t - FIN) / (0.15 * LARGO_TONO)
        return -amp * (1 - tp) if 0 < tp <= 1 else 0.0
    if not 0 <= tt <= 1:
        return 0.0
    if tipo == 'on-off':
        # un pico al encender y otro al apagar; entre ambos, un leve abombamiento hacia arriba
        borde = 0.15
        pico = max(min(max(1 - tt / borde, 0), 1), min(max(1 - (1 - tt) / borde, 0), 1))
        medio = min(max((tt - borde) / (1 - 2 * borde), 0), 1)
        return -amp * pico + 0.24 * amp * math.sin(math.pi * medio) ** 2
    # normal e invertido: flancos rápidos (50 ms) y meseta sostenida
    meseta = min(max(min(tt / 0.05, (1 - tt) / 0.05), 0), 1)
    return (amp if tipo == 'invertido' else -amp) * meseta


def ruido(n, semilla):
    """Ruido de base suave (σ ~1 μL), fijo para que el dibujo no cambie al rearmarlo."""
    random.seed(semilla)
    crudo = [random.gauss(0, 0.0016) for _ in range(n + 6)]
    return [sum(crudo[i:i + 7]) / 7 for i in range(n)]


def formas_reflejo():
    c = Lienzo(760, 478)
    c.t(14, 20, 'Las cuatro formas de la curva del reflejo estapedial', 10.5, TINTA, 'start', 700)

    x0, x1 = 226, 740
    X = lambda t: x0 + t / DURACION * (x1 - x0)
    esc = 800                                 # px por mL: 0,05 mL = 40 px
    amp = amplitud()
    alto = 88                                 # alto de cada fila
    y_tono, y_filas = 62, 86
    filas = [('Normal', 'meseta mientras suena', 'normal'),
             ('ON-OFF', 'al encender y al apagar', 'on-off'),
             ('OFF', 'solo al apagar', 'off'),
             ('Invertido', 'sube en vez de bajar', 'invertido')]
    y_eje = y_filas + alto * len(filas) + 6

    # franja del tono, de la barra al eje del tiempo
    c.out.append(f'<rect x="{X(INICIO):.1f}" y="{y_tono + 6}" width="{X(FIN) - X(INICIO):.1f}" '
                 f'height="{y_eje - y_tono - 6}" fill="{FRANJA}"/>')
    # barra del tono
    c.out.append(f'<rect x="{X(INICIO):.1f}" y="{y_tono - 5}" width="{X(FIN) - X(INICIO):.1f}" '
                 f'height="10" rx="2" fill="{RETRO}"/>')
    c.t((X(INICIO) + X(FIN)) / 2, y_tono - 11, 'tono (1 s)', 8.4, RETRO, 'middle', 700)
    c.t(X(INICIO) - 6, y_tono + 4, 'enciende', 7.6, RETRO, 'end', 600)
    c.t(X(FIN) + 6, y_tono + 4, 'apaga', 7.6, RETRO, 'start', 600)

    for k, (nombre, detalle, tipo) in enumerate(filas):
        top = y_filas + k * alto
        sube = tipo == 'invertido'
        yb = top + (alto - 18 if sube else 18)          # línea base de la fila
        signo = -1 if sube else 1                        # hacia dónde se dibuja la deflexión
        if k:
            c.l(14, top, x1, top, GRILLA, 1)
        # nombre y qué mirar
        c.t(14, top + alto / 2 - 2, nombre, 9.6, TINTA, 'start', 700)
        c.t(14, top + alto / 2 + 14, detalle, 7.8, TENUE, 'start', 600)
        # eje de la admitancia: 0 y 0,05 mL hacia el lado en que va la deflexión
        xa = x0 - 10
        y5 = yb + signo * 0.05 * esc
        c.l(xa, yb, xa, y5, FUERTE, 1)
        for y, s in ((yb, '0'), (y5, '+0,05' if sube else '−0,05')):
            c.l(xa - 3, y, xa, y, FUERTE, 1)
            c.t(xa - 5, y + 3, s, 7.2, TENUE, 'end')
        # línea base y nivel de 0,02 mL (lo mínimo que cuenta como deflexión)
        c.l(x0, yb, x1, yb, FUERTE, 0.8, '4 3')
        y2 = yb + signo * 0.02 * esc
        c.l(x0, y2, x1, y2, AVISO, 1.1, '2 3')
        if k == 0:
            c.t(x0 + 4, y2 + 12, 'mínimo: 0,02 mL', 7.4, AVISO, 'start', 600)
        # la traza
        n = 600
        rr = ruido(n + 1, 40 + k)
        pts = []
        for i in range(n + 1):
            t = i / n * DURACION
            pts.append((X(t), yb - (forma(t, tipo, amp) + rr[i]) * esc))
        c.poli(pts, COCLEAR, 1.9)

    c.t(x0 - 10, y_filas - 4, 'mL', 7.6, TENUE, 'end', 600)

    # eje del tiempo
    c.l(x0, y_eje, x1, y_eje, FUERTE, 1)
    for t in (0, 0.5, 1, 1.5, 2):
        c.l(X(t), y_eje, X(t), y_eje + 4, FUERTE, 1)
        c.t(X(t), y_eje + 15, f'{t:g}'.replace('.', ','), 8, TENUE)
    c.t(x1, y_eje + 28, 'tiempo (s)', 8.2, TENUE, 'end')
    c.t(14, y_eje + 28, 'Hacia abajo, baja la admitancia.', 7.8, TENUE, 'start')
    c.guardar('04-formas-reflejo.svg')


if __name__ == '__main__':
    formas_reflejo()
