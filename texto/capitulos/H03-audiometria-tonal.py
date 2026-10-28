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

AUDIO = fig.audiograma(clinico=True, combinado=True)

CASOS = [
    # Símbolos sobre un audiograma normal, con la ósea a la vista en todo el rango
    demo(33, [fig.audiograma(estudio=False, ldl=False)]),
    # Las tres lecturas del gap: conductiva, sensorioneural y mixta. Solo el audiograma,
    # unido y en la forma clínica (él, 2026-10-28: "si el capítulo está viendo audiometría,
    # solo mostremos eso"; antes la hoja auditiva entera, con logo y supraliminares, que
    # van en H5 y H6). El 33 queda con el audiograma de los símbolos.
    demo(34, [AUDIO]),
    demo(36, [AUDIO]),
    # Luis va primero en el texto (caso H3.1); el audiograma con LDL es el de la radiografía, que no es de ningún paciente; la "radiografía de un audiograma"
    demo(41, [AUDIO]),
    # Sin respuesta y curva sombra (el porqué de H4)
    demo(42, [fig.audiograma(clinico=True, combinado=True, sin_enmascarar=True)]),
    # Ocupacional: la muesca
    demo(37, [AUDIO]),
]

if __name__ == '__main__':
    Capitulo('H3').generar(CASOS)
