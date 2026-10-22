#!/usr/bin/env python3
"""Capítulo 37 — Nariz y pulmón.

    python3 docs/libro/capitulos/37-nariz-y-pulmon.py              casos + figuras + PDF
    python3 docs/libro/capitulos/37-nariz-y-pulmon.py --solo-pdf   solo el PDF (cambió el texto)
    python3 docs/libro/capitulos/37-nariz-y-pulmon.py --rearmar    vuelve a armar los casos por cuadro

Acá se deciden los pacientes; el texto está en 37-nariz-y-pulmon.md (cada caso se nombra
ahí como cap37_<nombre>). Los dos pacientes son de audición normal ('normal'): un cuadro nasal
o pulmonar no existe en LabSim y solo se necesitan la ficha, la anamnesis y el rostro.
La espirometría (curvas, tablas y z-score) NO sale de LabSim: la calcula
ilustraciones/hacer_cap37.py (GLI-2012, grupo caucásico, como el manual SER Chile 2024).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'herramientas'))
from libro import Capitulo, cuadro, demo, fig  # noqa: E402,F401

CASOS = [
    cuadro('asma', [], edad=27, sexo='hombre', semilla=107,
           anamnesis="""Tiene 27 años y es diseñador gráfico. Desde la adolescencia se le tapa la nariz casi todo el año y
           peor en primavera: estornuda en salvas, le pica la nariz y los ojos, le gotea agua clara y siente la garganta
           "con moco que baja". Hace dos años adoptó un gato y desde entonces está peor. En los últimos meses se le suma
           tos seca de madrugada, un silbido en el pecho al subir escaleras o al jugar fútbol, y a veces "no me llega el
           aire" al reírse mucho. Hace un año un médico le dio un inhalador de salbutamol: lo usa dos o tres veces por
           semana y le alivia. Toma un antihistamínico cuando está muy mal; lo dejó hace tres días, como le pidieron para
           el examen, y no usó el salbutamol en las últimas 24 horas. No fuma. Su madre tiene rinitis y "bronquitis
           alérgica". Un alergólogo le hizo pruebas en la piel hace un año; le dijo que reaccionaba a los ácaros y al gato.""",
           historia=[(2500, 'Control por estornudos y picazón en primavera; antihistamínico oral cuando hay síntomas.'),
                     (365, 'Pruebas cutáneas con alérgenos inhalantes: reacciona a ácaros y a epitelio de gato (según relata; no trajo el informe). Se indica salbutamol en inhalador a demanda.'),
                     (30, 'Médico general: rinitis alérgica y sospecha de asma; se solicita espirometría con prueba broncodilatadora.')],
           medicamentos='Salbutamol en inhalador a demanda, dos o tres veces por semana (última dosis hace más de 24 horas); antihistamínico oral cuando hay síntomas (lo dejó hace tres días)'),
    cuadro('estenosis', [], edad=49, sexo='mujer', semilla=214,
           anamnesis="""Tiene 49 años y trabaja como secretaria. Hace catorce meses estuvo hospitalizada 16 días por una
           neumonía grave, y 12 de esos días con ventilación mecánica por un tubo en la tráquea. Salió ronca y la voz se
           le normalizó en un mes. Desde hace ocho meses se agita al subir una escalera y al caminar rápido, y desde hace
           unos tres meses "hace ruido" al respirar: lo oyen los demás, sobre todo al inspirar y cuando camina apurada.
           Un médico pensó en asma y le dio un inhalador con corticoide y formoterol, que usa dos veces al día desde hace
           cinco meses sin notar cambio. No ha tenido silbidos de pecho antes, ni estornudos, ni picazón; su nariz "respira
           bien" y no hay alergia en la familia. Nunca ha fumado. Para el examen dejó el formoterol 24 horas, como le indicaron.""",
           historia=[(425, 'Neumonía grave; ventilación mecánica invasiva durante 12 días; alta a los 16 días.'),
                     (240, 'Disnea de esfuerzo progresiva.'),
                     (150, 'Se diagnostica asma; corticoide inhalado con formoterol, sin mejoría.'),
                     (30, 'Médico general: disnea que no responde al tratamiento del asma; se solicita espirometría con prueba broncodilatadora.')],
           medicamentos='Budesonida con formoterol en inhalador, dos veces al día (el formoterol se suspendió 24 horas antes del examen)'),
]

if __name__ == '__main__':
    Capitulo(37).generar(CASOS)
