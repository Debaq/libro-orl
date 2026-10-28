#!/usr/bin/env python3
"""Herramienta H10 — Potenciales evocados auditivos de tronco.

    python3 docs/libro/capitulos/<este archivo>.py              figuras + PDF
    python3 docs/libro/capitulos/<este archivo>.py --solo-pdf   solo el PDF

Una herramienta no necesita pacientes, pero puede ilustrar con algunos
(demo() o cuadro(), igual que un capítulo clínico; ver libro.py).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'herramientas'))
from libro import Capitulo, cuadro, demo, fig  # noqa: E402,F401


# Pacientes propios del libro (él, 2026-10-21): un bebé, una mujer adulta joven y
# un anciano, para mostrar las diferencias de edad y sexo. Los pacientes de
# práctica de LabSim (33, 34, 36, 39, 40) se guardaron en
# investigacion/del_trazo_al_informe/pacientes_labsim_retirados/.
CASOS = [
    # Bebé de 12 semanas con audición normal: el PEAT de umbral (click y burst de 1 y 4 kHz).
    # Menor de 3 meses para que LabSim use la fila del recién nacido (Rosa 2014): la del
    # "lactante" de 3 meses a 3 años es casi de adulto (aviso en LabSim).
    cuadro('lactante', [fig.abr(niveles=(80, 40, 20)),
                        fig.abr(niveles=(40, 20, 10), estimulo='Burst 1', marcar=('V',), ventana=20),
                        fig.abr(niveles=(40, 20, 10, 0), estimulo='Burst 4 kHz', marcar=('V',))],
           od='normal', oi='normal', sexo='hombre', edad_horas=2050, semilla=31,
           anamnesis="""Tiene 12 semanas y viene con sus papás. Nació de término, con 3.400 g, sin UCI. En el
           tamizaje con emisiones, a las 36 horas, el oído izquierdo refirió; al repetirlo antes del alta volvió a
           referir. La mamá cuenta que se asusta con los portazos y que se calma cuando ella le habla. No hay
           sordera en la familia. Lo derivan para un PEAT de diagnóstico.""",
           historia=[(84, 'Tamizaje con emisiones: OD pasa, OI refiere; se repite antes del alta y vuelve a referir.')]),
    # Mujer de 28 años: OD normal (búsqueda de umbral) y OI retrococlear, con tasa alta
    cuadro('mujer_joven', [fig.abr(niveles=(80, 60, 50, 40, 20, 10, 0)),
                           fig.abr(niveles=(80,), tasa=81.1)],
           od='normal', oi='schwannoma', grado_oi='leve', edad=28, sexo='mujer', semilla=22,
           anamnesis="""Tiene 28 años y es contadora. Hace unos ocho meses empezó con un zumbido agudo y continuo
           en el oído izquierdo, y desde hace poco nota que por ese lado entiende menos por teléfono. Algunas veces
           se siente inestable al darse vuelta rápido. No ha tenido infecciones de oído ni ruido en el trabajo. El
           otorrinolaringólogo vio una audiometría con caída de agudos solo en el oído izquierdo y pide un PEAT.""",
           historia=[(30, 'Audiometría: OI con caída de agudos (35 a 50 dB HL de 2 a 4 kHz); OD normal. Se pide PEAT.')]),
    # Hombre de 76 años con presbiacusia: coclear de agudos, click y burst de 1 kHz
    cuadro('anciano', [fig.abr(niveles=(80, 60, 50, 40)),
                       fig.abr(niveles=(60, 40, 30, 20), estimulo='Burst 1', marcar=('V',))],
           od='presbiacusia', oi='presbiacusia', edad=76, sexo='hombre', semilla=13,
           anamnesis="""Tiene 76 años y es agricultor jubilado. Hace años que le cuesta entender cuando hablan
           varios a la vez, y la familia le sube el volumen a la televisión. Desde hace un año tiene un zumbido en
           los dos oídos, más molesto de noche. Hace dos meses tuvo un mareo breve al levantarse. Usa enalapril para
           la presión. El médico pide un PEAT antes de indicarle audífonos.""",
           antecedentes=['hta'], medicamentos='Enalapril 10 mg al día'),
]

if __name__ == '__main__':
    Capitulo('H10').generar(CASOS)
