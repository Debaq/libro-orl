#!/usr/bin/env python3
"""Herramienta H3 — Audiometría tonal.

    python3 docs/libro/capitulos/<este archivo>.py              figuras + PDF
    python3 docs/libro/capitulos/<este archivo>.py --solo-pdf   solo el PDF

Una herramienta no necesita pacientes, pero puede ilustrar con algunos
(demo() o cuadro(), igual que un capítulo clínico; ver libro.py).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'herramientas'))
from libro import Capitulo, cuadro, demo, fig  # noqa: E402,F401

CASOS = [
    # Símbolos sobre un audiograma normal, con la ósea a la vista en todo el rango
    demo(33, [fig.audiograma(estudio=False, ldl=False)]),
    # Las tres lecturas del gap: conductiva, sensorioneural y mixta. Desde acá la hoja
    # auditiva del tomo II (él, 2026-10-22); el 33 queda con el audiograma de los símbolos.
    demo(34, [fig.audiosupra()]),
    demo(36, [fig.audiosupra()]),
    # Luis va primero en el texto (caso H3.1); el audiograma con LDL es el de la radiografía, que no es de ningún paciente; la "radiografía de un audiograma"
    demo(41, [fig.audiosupra()]),
    # Sin respuesta y curva sombra (el porqué de H4)
    demo(42, [fig.audiosupra(sin_enmascarar=True)]),
    # Ocupacional: la muesca
    demo(37, [fig.audiosupra()]),
]

if __name__ == '__main__':
    Capitulo('H3').generar(CASOS)
