#!/usr/bin/env python3
"""Capítulo 18 — El ABR que engaña.

    python3 docs/libro/capitulos/18-el-abr-que-engana.py              casos + figuras + PDF
    python3 docs/libro/capitulos/18-el-abr-que-engana.py --solo-pdf   solo el PDF (cambió el texto)
    python3 docs/libro/capitulos/18-el-abr-que-engana.py --rearmar    vuelve a armar los casos por cuadro

Acá se deciden los pacientes y las figuras del capítulo; el texto está en
18-el-abr-que-engana.md (cada caso se nombra ahí como cap18_<nombre>).
Cuadros y grados: claves de CaseProfile::SCENARIOS. Un cuadro() acepta
od=, oi=, grado_od=, grado_oi=, edad=, sexo='hombre'|'mujer', semilla=.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'herramientas'))
from libro import Capitulo, cuadro, demo, fig  # noqa: E402,F401

# Lo que engaña no es el oído, es el registro. Cada paciente es de un cuadro corriente y sus figuras del
# motor son el ABR limpio (la referencia); los registros mal tomados están en ilustraciones/hacer_cap18.py,
# calculados con el generador de LabSim sobre los datos de cada caso (casos/generados/cap18_*.json).
CASOS = [
    cuadro('barridos', [fig.audiosupra(), fig.impedancia(), fig.abr(niveles=(80, 40, 20, 10, 0))],
           od='normal', oi='normal', edad=23, sexo='hombre',
           anamnesis="""Tiene 23 años y se tituló este año de técnico en refrigeración. No tiene ningún síntoma: oye
           bien, no tiene pitidos, mareos ni secreción y nunca ha tenido infecciones de oído. No ha trabajado con
           ruido fuerte ni toma medicamentos. Nadie en su familia tiene problemas de audición. Se ofreció de
           voluntario para que un alumno de electrofisiología practicara con él un ABR.""",
           historia=[(14, 'Audiometría de práctica en la universidad: umbrales normales en los dos oídos.')]),
    cuadro('supraaural', [fig.audiosupra(), fig.abr(niveles=(100, 80, 60, 50, 40))],
           od='nihl_cronica', oi='nihl_cronica', grado_od='leve', grado_oi='leve', edad=47, sexo='hombre',
           anamnesis="""Tiene 47 años y hace 20 opera un chancador en una planta de áridos. Usó protección auditiva solo
           a ratos. Desde hace unos años tiene un siseo permanente en los dos oídos y le cuesta entender cuando hay
           ruido de fondo; en silencio conversa sin problema. No tiene mareos, dolor ni secreción de oídos. En la
           mutual le hicieron una audiometría con caída en los agudos y lo derivaron a un ABR para completar el
           estudio.""",
           historia=[(60, 'Audiometría de vigilancia: caída bilateral en agudos compatible con ruido; se pide un estudio con ABR.')],
           antecedentes=['trauma_acustico']),
    cuadro('postauricular', [fig.audiosupra(), fig.abr(niveles=(90, 70, 60, 50))],
           od='presbiacusia', oi='presbiacusia', edad=74, sexo='hombre',
           anamnesis="""Tiene 74 años; fue carpintero hasta que se jubiló hace diez. Hace años oye menos: le cuesta
           entender la televisión y las conversaciones con ruido, y dice que "todos murmuran". Tiene un pitido agudo
           permanente en los dos oídos. No tiene mareos, dolor ni secreción. Se hizo la audiometría por consejo de
           su hija y, por curiosidad, también un ABR.""",
           historia=[(30, 'Control con su médico general: hipoacusia bilateral lentamente progresiva; se pide audiometría.')]),
    cuadro('cofosis', [fig.audiosupra(), fig.impedancia(), fig.abr(niveles=(100, 80))],
           od='parotiditis', grado_od='profunda', edad=22, sexo='hombre',
           anamnesis="""Tiene 22 años y trabaja de garzón en un restaurante del centro. No oye por el oído derecho desde
           que tiene memoria: se lo encontraron en el control de salud del colegio, a los 7 años, y a su mamá le dijeron
           que era "de nacimiento" y que no había nada que hacer. Nunca le hicieron otro estudio. En el restaurante se
           acomoda para que los clientes le hablen por la izquierda, y con el local lleno no sabe de dónde lo llaman.
           No tiene pitido, mareos, dolor ni secreción. Del oído izquierdo no tiene ninguna queja.""",
           historia=[(5475, 'Control de salud escolar: no oye por el oído derecho; se informa como sordera de nacimiento. Sin estudios.'),
                     (20, 'Médico general: sordera derecha de larga data; pide audiometría y ABR.')]),
    cuadro('configuracion', [fig.audiosupra(), fig.impedancia(), fig.abr(niveles=(80, 50, 30, 20, 10, 0))],
           od='normal', oi='meniere', grado_oi='leve', edad=46, sexo='mujer',
           anamnesis="""Tiene 46 años y es profesora de básica. Desde hace unos ocho meses tiene crisis de vértigo
           giratorio con náuseas que duran un par de horas, con el oído izquierdo "tapado" y un zumbido grave que viene
           y va con las crisis. Entre una crisis y otra, la audición de ese lado sube y baja. El oído derecho está
           bien. No tiene dolor ni secreción.""",
           historia=[(240, 'Primera crisis de vértigo con náuseas y plenitud del oído izquierdo.'),
                     (20, 'Otorrinolaringología: sospecha de enfermedad de Ménière; se pide audiometría y ABR.')]),
]

if __name__ == '__main__':
    Capitulo(18).generar(CASOS)
