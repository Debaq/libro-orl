#!/usr/bin/env python3
"""Capítulo 38 — El que ronca.

    python3 docs/libro/capitulos/38-el-que-ronca.py              casos + figuras + PDF
    python3 docs/libro/capitulos/38-el-que-ronca.py --solo-pdf   solo el PDF (cambió el texto)
    python3 docs/libro/capitulos/38-el-que-ronca.py --rearmar    vuelve a armar los casos por cuadro

Acá se deciden los pacientes y las figuras del capítulo; el texto está en
38-el-que-ronca.md (cada caso se nombra ahí como cap38_<nombre>).
Cuadros y grados: claves de CaseProfile::SCENARIOS. Un cuadro() acepta
od=, oi=, grado_od=, grado_oi=, edad=, sexo='hombre'|'mujer', semilla=.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'herramientas'))
from libro import Capitulo, cuadro, demo, fig  # noqa: E402,F401

# Un cuadro de sueño no existe en LabSim: los cuatro pacientes son de audición normal
# ('normal') y sirven para que existan la ficha, la anamnesis y el rostro.
# Los registros de sueño (hipnogramas, trazos, índices) salen de ilustraciones/hacer_cap38.py:
# son noches simuladas con semilla fija, y todo índice que dice el texto sale de ahí.
CASOS = [
    cuadro('roncador', [], edad=44, sexo='hombre',
           anamnesis="""Tiene 44 años y es jefe de bodega. Su pareja se queja de que ronca "como motosierra" desde
           hace unos cinco años y hace dos meses se cambió de pieza. Dice que a veces se calla un rato y vuelve con un
           resoplido, pero que no lo ha visto ahogarse. Él duerme de corrido, se levanta descansado y no se queda
           dormido de día: ni en el auto, ni viendo televisión. Su peso está estable desde hace años. En primavera
           se le tapa la nariz y el ronquido empeora; el resto del año respira bien. No toma alcohol de noche ni
           sedantes, no fuma y no tiene la presión alta. Quiere saber si hay algún aparato o una operación que lo
           haga dejar de roncar.""",
           historia=[(1800, 'Su pareja empieza a notar el ronquido.'),
                     (60, 'Médico general: ronquido habitual sin somnolencia; se deriva a otorrinolaringología y se pide una poligrafía respiratoria.')],
           medicamentos='Ninguno'),
    cuadro('moderado', [], edad=52, sexo='hombre',
           anamnesis="""Tiene 52 años y maneja un colectivo. Ronca desde hace años y desde hace dos "se me va la
           cabeza" en los semáforos; el mes pasado se salió un poco de la pista y se asustó. Su señora cuenta que se
           ahoga y que despierta a veces con un sobresalto. Se levanta con dolor de cabeza y la boca seca, porque
           duerme con la boca abierta. La nariz derecha no le pasa desde que se la quebró jugando a la pelota a los
           20 años y la izquierda se le tapa en primavera, con estornudos y picazón. Para poder dormir usa un spray
           descongestionante casi todas las noches. Tiene la presión alta, en tratamiento, y ha subido unos ocho
           kilos en cinco años.""",
           historia=[(7300, 'Fractura nasal jugando a la pelota; no consultó.'),
                     (730, 'Empieza con somnolencia al manejar y ronquido más fuerte.'),
                     (90, 'Médico general: sospecha de apnea del sueño; se pide una poligrafía respiratoria y evaluación otorrinolaringológica.')],
           antecedentes=['hta'],
           medicamentos='Antihipertensivo; oximetazolina en spray nasal casi todas las noches'),
    cuadro('grave', [], edad=61, sexo='mujer', semilla=22,
           anamnesis="""Tiene 61 años y es dueña de una panadería. Hace dos años tuvo un accidente cerebrovascular
           isquémico y, desde entonces, su hija la vigila de noche: dice que "se queda sin respirar" y que a veces
           parece que se asfixia. Se levanta con dolor de cabeza y no se siente descansada aunque duerma ocho horas.
           Se duerme sentada en la caja, esperando a los clientes, y una vez se quedó dormida en el semáforo. Ha subido
           de peso desde la menopausia. Es hipertensa y diabética, y le cuesta controlarse la presión pese a tres
           remedios. Nunca se ha hecho un estudio del sueño.""",
           historia=[(730, 'Accidente cerebrovascular isquémico sin secuelas importantes.'),
                     (120, 'Neurología: sospecha de apnea del sueño como factor de riesgo; se pide un estudio del sueño.')],
           antecedentes=['hta', 'diabetes'],
           medicamentos='Tres antihipertensivos, metformina y un antiagregante'),
    cuadro('dudosa', [], edad=41, sexo='mujer', semilla=123,
           anamnesis="""Tiene 41 años y es ingeniera. Duerme mal hace años: se acuesta rendida, despierta varias veces en
           la noche y a veces se queda despierta una o dos horas. Se levanta cansada, con dolor de cabeza y la
           mandíbula apretada, y en las reuniones de la tarde le cuesta no cabecear. Ronca poco, solo cuando está
           resfriada, y su pareja no ha visto pausas. Le diagnosticaron hipertensión hace seis meses, a pesar de tener
           un peso normal y hacer deporte. Hace un mes se hizo una poligrafía en la casa y le dijeron que "salió
           normal", pero ella sigue igual de cansada. Pregunta si la apnea del sueño se puede tener sin roncar.""",
           historia=[(2000, 'Insomnio de mantención y bruxismo, sin tratamiento.'),
                     (180, 'Diagnóstico de hipertensión arterial; inicia tratamiento.'),
                     (30, 'Poligrafía respiratoria domiciliaria: índice de eventos respiratorios bajo 5 por hora. El médico mantiene la sospecha y pide una polisomnografía.')],
           antecedentes=['hta'],
           medicamentos='Antihipertensivo'),
]

if __name__ == '__main__':
    Capitulo(38).generar(CASOS)
