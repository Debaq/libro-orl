#!/usr/bin/env python3
"""Herramienta H13 — Potenciales de estado estable.

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
    # Gabriela: GJB2 severa bilateral confirmada con click; el ASSR da los
    # umbrales por frecuencia para adaptar audífonos a los 7 meses
    cuadro('lactante', [fig.abr(), fig.timpanograma(sonda=1000), fig.teoae()],
           od='gjb2', oi='gjb2', grado_od='severa', grado_oi='severa', edad_meses=7, sexo='mujer',
           semilla=1481668643,
           anamnesis="""Tiene 7 meses y viene con su mamá y su papá. Nació de término, sin complicaciones, y no pasó el
           tamizaje auditivo en ninguno de los dos oídos. A los 3 meses le hicieron un PEAT con click que mostró una
           hipoacusia severa en los dos lados y el estudio genético salió positivo para GJB2. Los papás dicen que no se
           asusta con los portazos, pero que sí se ríe cuando le hablan mirándola. Balbucea poco. Un tío por el lado
           de la mamá es sordo desde chico. No ha tenido otitis ni hospitalizaciones.""",
           historia=[(120, 'Maternidad: tamizaje con emisiones refiere OD y OI; se repite antes del alta y vuelve a referir.'),
                     (100, 'Otorrinolaringólogo: PEAT con click, onda V hasta 85 dB nHL en OD y 90 dB nHL en OI. Solicita estudio genético.'),
                     (30, 'Genetista: dos variantes patogénicas en GJB2. Consejo genético a los padres.'),
                     (7, 'Otorrinolaringólogo: indica audífonos bilaterales. Solicita potenciales de estado estable para estimar los umbrales por frecuencia.')],
           antecedentes=['hipoacusia_familiar']),
    # César: TEA, no colabora con la audiometría conductual; CMV congénito con
    # pérdida moderada del OD que el ASSR muestra por frecuencia
    cuadro('nino_tea', [fig.abr(), fig.timpanograma(), fig.teoae()],
           od='cmv_congenito', oi='normal', grado_od='moderada', edad=4, sexo='hombre',
           semilla=1153267858,
           anamnesis="""Tiene 4 años y viene con su mamá. Tiene diagnóstico de trastorno del espectro autista desde los 2
           años y va a un jardín con apoyo. Habla poco, con frases cortas, y no tolera los audífonos de la audiometría:
           se los saca y llora. Al nacer le encontraron CMV en la orina por un examen que le pidieron por bajo peso;
           pasó el tamizaje de los dos oídos. La educadora notó que cuando lo llaman por la derecha no se da vuelta.
           En la casa sube el volumen de la tableta. No ha tenido otitis.""",
           historia=[(400, 'Neuropediatra: trastorno del espectro autista. Antecedente de CMV congénito sin tratamiento. Seguimiento auditivo anual.'),
                     (60, 'Fonoaudióloga del jardín: no gira al llamado por la derecha. Sugiere evaluación auditiva.'),
                     (20, 'Otorrinolaringólogo: otoscopía normal. Audiometría por juego no lograda: no tolera los fonos. Solicita PEAT y potenciales de estado estable.')]),
]

if __name__ == '__main__':
    Capitulo('H13').generar(CASOS)
