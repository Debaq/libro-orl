# Errores de procedimiento y de conocimiento: H01, H02, H03 (agente 04, 2026-10-22)

Leídos completos: H01, H02, H03 (.md y .py) y los datos de los pacientes (labsim/docs/manual/capturas/casos_demo.json, casos 33 a 42, e ilustraciones/hacer_h03_radiografia.py).
Fuentes contrastadas: BSA 2018 (pura tonal, leída entera en lo pertinente), BSA 2022 (Rinne y Weber; examen del oído, leídos), Katz Handbook 7.ª ed. cap. 3 (Schlauch y Nelson), resumen de Kelly 2018 y Golabek y Stephens 1979 (Europe PMC), AAA 2009 (ototoxicidad), resumen de Swan y Browning 1989, Watson y Gengel 1969 (resumen).

Resultado general: no encontré errores GRAVES. Los datos de los casos coinciden con el texto en H01 y H02; en H03 hay una contradicción interna (hallazgo 3). Lo demás son imprecisiones y puntos donde las guías discrepan.

## GRAVES

Ninguno.

## IMPRECISOS (ordenados por peso)

1. **[IMPRECISO] H03 l.434 (y comentario de H03.py l.23)** — "El OI de Luis, el paciente de la radiografía del comienzo (caso H3.1)" → la radiografía NO es de Luis ni de ningún paciente: ilustraciones/hacer_h03_radiografia.py dice "No es de un paciente". En la radiografía el mixto es el OD (aérea 55-70, ósea 20; OI aérea 10-20 en graves y sin gap), mientras que Luis (demo 41) tiene OD normal y OI mixto (aérea 50-55 en 500-2k, ósea 25) → fuente: casos_demo.json caso 41 vs. hacer_h03_radiografia.py; el propio texto l.46 dice "en el OD la pérdida es mixta" → corrección: decir "el mismo tipo de pérdida que aparece en el OD de la radiografía" o quitar "el paciente de la radiografía"; en H03.py l.23 el comentario dice que el 2.º audiograma de Luis es la radiografía, y no lo es.

2. **[IMPRECISO] H03 l.134** — "Esa suma se completa en unos 30 a 70 ms en los agudos y en 125 a 175 ms en los graves (Watson y Gengel, 1969)" → esas cifras son las *constantes de tiempo* de la integración (resumen de Watson y Gengel 1969), no el tiempo en que se completa la suma; Katz cap. 3 (Schlauch y Nelson 2015, sección de procedimiento): duraciones de ~200 ms a 1 s o más dan umbrales casi idénticos, y menores de 200 ms los elevan (de ahí el pulso nominal de 225 ms de la norma) → corrección: decir "constante de tiempo de 30-70 ms (agudos) a 125-175 ms (graves); la suma se completa hacia los 200-300 ms" o citar el criterio de Katz de ≥200 ms.

3. **[IMPRECISO] H03 l.458** — "Dos oídos casi iguales quedan en grados distintos por un decibel" (OD 36 dB leve, OI 41 dB moderada) → entre 36,25 y 41,25 hay 5 dB; lo que es "un decibel" es cuánto pasa el OI del corte de 40 dB. Datos del caso (demo 36) correctos: (20+25+40+60)/4 y (25+30+45+65)/4 → corrección: "quedan en grados distintos porque el OI pasa por un decibel el corte de 40".

4. **[IMPRECISO] H03 l.226 y l.228 (instrucción al paciente)** — la instrucción modelo dice solo "aprieta el botón ... altiro" → BSA 2018 §6.1 exige que el paciente mantenga el botón mientras oye el tono y lo suelte al dejar de oírlo ("Release the button as soon as you no longer hear"), y §7.4 que en vía ósea se enfatice que responda "no importa en qué lado oiga el sonido". Sin la segunda frase, el paciente puede no responder a un tono óseo que percibe en el oído contrario → corrección: agregar "mientras lo oigas" y, en la ósea, "aunque lo oigas en el otro oído". (El propio texto, l.547, evalúa "responde mientras suena", así que la instrucción debería pedirlo.)

5. **[IMPRECISO] H03 l.115** — "0 dB HL es el nivel que detecta un adulto joven ... entre 18 y 25 años (ISO 389-7, 2019)" → la ISO 389-7 es el umbral de referencia en campo libre y campo difuso; el cero de los fonos supra-aurales está en ISO 389-1 (que el mismo capítulo cita en l.113), el de inserción en 389-2 y el del vibrador en 389-3 → corrección: citar ISO 389-1/-2/-3 para el cero de cada transductor y dejar 389-7 solo para campo libre. (El marcador "verificar" ya trata el rango 18-25 años; esto es sobre la elección de la norma.)

6. **[IMPRECISO] H03 l.585** — "La fiabilidad cae después de unos 20 minutos sin pausa (ISO 8253-1, 2010)" → lo que pude comprobar es BSA 2018 §5.2: "Si el examen supera los 20 minutos, el sujeto puede beneficiarse de una pausa breve"; no dice que la fiabilidad "caiga" a esa hora, y no pude leer la ISO (de pago) → corrección: citar BSA 2018 §5.2 y decir "conviene una pausa si el examen pasa de 20 minutos".

7. **[IMPRECISO] H02 l.140 y fila "Mixta" de la tabla (l.138)** — la tabla se rotula "Según la BSA (2022)" y agrega "con una sensorioneural de larga data en un oído, el Weber puede salir centrado" → BSA 2022 §4.1.3 y §4.2.3 solo sostienen las filas simétrica, sensorioneural asimétrica, conductiva asimétrica y el falso negativo; la fila mixta y lo del Weber centrado no están en BSA (la nota de H02 l.153 ya advierte esto para Schwabach/Bing pero no para esta tabla) → corrección: decir "Según la BSA (2022), salvo la fila mixta y la nota final, que son deducción del libro".

## DISCUTIBLES (las fuentes discrepan; no es error del libro)

8. **[DISCUTIBLE] H03 l.135 (tono pulsado)** — el libro presenta el pulsado como equivalente y preferido por 2 de cada 3 pacientes (Burk y Wiley 2004: 67 % lo prefiere, umbrales y confiabilidad comparables; Katz cap. 3 lo recomienda, y por reducir falsos positivos con acúfeno, Mineau y Schlauch 1997). BSA 2018 §6.8 dice lo contrario: "El uso de tonos pulsados y de ruido de banda angosta no se aconseja por problemas de calibración y percepción". Postura A: Katz/Burk y Wiley. Postura B: BSA 2018. Sugerencia: decir las dos, porque el libro cita a BSA 2018 en la misma sección.

9. **[DISCUTIBLE] H03 l.298 (frecuencias de la vía ósea)** — el libro: 250 a 4.000 Hz (ASHA 2005; ISP 2012). BSA 2018 §7.2 y §7.7: "normalmente solo de 500 a 2.000 Hz" y no se recomienda bajo 500 Hz por distorsión del B71 (el libro explica la distorsión en l.305 pero concluye lo contrario sobre 250 Hz). Katz cap. 3 usa 250-4000 Hz. Postura A: ASHA/Katz. Postura B: BSA.

10. **[DISCUTIBLE] H03 l.240 (familiarización)** — el libro: 1 kHz a 40 dB HL y subida de 10 en 10 si no responde (BSA 2018 §6.6, ISO). ASHA 2005 según Katz cap. 3: 30 dB HL y subida de 20 en 20. Ambas son válidas; el texto cita a ASHA para el oído de partida pero a BSA para esta parte, lo cual es correcto, solo conviene saber que ASHA es distinta.

11. **[DISCUTIBLE] H03 l.265 y l.267 (cuándo repetir 1 kHz)** — el libro repite 1 kHz tras 8 kHz y antes de 500 Hz y cita "ASHA 2005; BSA 2018". ASHA 2005 (Katz): 1k, 2k, 4k, 8k, repetir 1k, luego 500 y 250. BSA 2018 §6.4: 1k, 2k, 4k, 8k, 500, 250 y *después* repetir 1k. Además BSA toma 3 y 6 kHz solo "cuando se necesiten", mientras Katz y el libro los miden de rutina en diagnóstico. Tolerancia de 5 dB: coincide en ASHA y BSA.

12. **[DISCUTIBLE] H03 l.274-293 (vía ósea al final de la batería)** — el libro lo declara y lo justifica ("un solo cambio de transductor"); ISO 8253-1:2010, ISP 2012, INSST 1992, ASHA y BSA la ponen justo después de la aérea. La regla de enmascarar la aérea comparando con la aérea del otro oído (l.290) es correcta: subestima la necesidad, nunca la sobreestima, y el libro manda revisar al final. Sin error lógico; es una decisión de método que se aparta de todas las guías.

13. **[DISCUTIBLE] H03 l.506 (asimetría)** — "diferencia de 15 dB o más en una o más frecuencias" es criterio propio del libro y sin cita; las definiciones clínicas de asimetría varían (p. ej. ≥15 dB en dos o más frecuencias, o por promedio). No pude contrastarlo con una guía concreta.

## Sin errores en H01

H01 coincide con BSA 2022 (examen del oído) y con las guías citadas en: tracción del pabellón (adulto arriba y atrás; niño atrás y a veces abajo), espéculo más grande que entre cómodo, examinador sentado, apoyo de la mano, empezar por el oído menos probable de estar alterado, cambio de espéculo, consentimiento verbal, niño en el regazo, detener ante dolor, sangre o mareo. También coinciden la definición de impactación de cerumen y el rechazo de velas (Schwartz 2017), la definición de OMA con abombamiento leve más dolor menor de 48 h o eritema intenso (Lieberthal 2013), los factores de riesgo JCIH (UCI más de 5 días), el triángulo luminoso a las 5 h (OD) y 7 h (OI), la agudeza de anterior/posterior en cada oído, el agua a 36-37 °C y la dirección posterosuperior. El caso de Benjamín (demo 35) concuerda con el ejemplo de anamnesis (5 años, otitis, ronca, primo con audífono, Rinne negativo bilateral, aérea 25-30 y ósea 0-10, tipo B).

## Datos de los casos contra el texto

- H02: demo 34 (aérea OD 500=50, 1k=45; ósea 10 y 15; ósea 2k=25; Rinne OD negativo, Weber OD) coincide con el texto (gap 40 y 30 dB, muesca de Carhart). Demo 39 (OD 15/20, OI 5/5, ósea=aérea, Weber OI, Rinne positivos) y demo 42 (OD sin respuesta, OI 0, Rinne falso negativo, Weber OI) coinciden.
- H03: demo 34 (gap 45 dB en 250, promedio BIAP 44, configuración ascendente, gap 30-45 entre 250 y 1k) correcto. Demo 36 (OD 4k aérea 60 y ósea 55; OI 1k 30/30; promedios 36 y 41) correcto. Demo 41 (OI aérea 50 y ósea 25 en 1k; ósea 4k=45) correcto. Demo 37 (OD 4k=55, OI 4k=60, 8k OD=30; BIAP OD 21; promedio 1-2-3-4-6 kHz = 33 y 38) correcto. Demo 33 todo 0, correcto.
- Cuentas del "promedio a ojo" (37,5; 38,33; tabla de 1,67/3,33/1,25/2,5/3,75): verificadas, correctas.
- Valores TDH-39 (45; 25,5; 7 dB SPL), grados BIAP, cortes OMS 2021, criterios ASHA 1994 de cambio por ototóxicos, 25/55/70 dB de umbral vibrotáctil (BSA 2018 §7.6), 17,5-30 dB del Rinne (BSA 2022), 5 dB de resolución del Weber, 13-40 dB y 2,5-4 dB de Kelly 2018, 16-87 % de sensibilidad, Bing negativo con gap de ~9 dB (Golabek y Stephens), "casi 90 %" del SRO (AAA 2009), 0,13 y 0,42 mm de membrana basilar y la quinta parte basal (cálculo con la función de Greenwood): coinciden con las fuentes.

## Conteo

- GRAVE: 0
- IMPRECISO: 7 (hallazgos 1 a 7)
- DISCUTIBLE: 6 (hallazgos 8 a 13)

## Revisado y NO comprobado con fuente

- H01: Ley 20.584 (artículos, 15 años de ficha); la inclusión de radioterapia entre los factores que modifican el manejo del cerumen (no pude abrir Schwartz 2017); "punta sin ocluir el conducto" y Ward 2023 (ya marcados con verificar).
- H02: Ungar 2021 (sinusitis y Weber: "la mayoría hacia el lado de la sinusitis, nunca hacia el seno sano"; no pude abrir el resumen); Miltenburg 1994; "Schwabach confirmó en 1885" (Huizing); el mecanismo de oclusión del Weber (Fagelson y Martin; Sichel) solo por la bitácora del libro; Swan y Browning solo por resumen.
- H03: PREXOR (plazos y rangos de frecuencia de las cuatro audiometrías), guía ISP v1.0, v2.0, v3.0 (reposo de 12 h, verificación semanal, criterio 2 de 3), criterio SUSESO (promedio 1-2-3-4-6 kHz y umbral de 25 dB; la búsqueda web no devolvió documento chileno), ISO 8253-1 (ruido ambiente, método de horquilla, "3 de 5", dispersión de más de 10 dB), IEC 60645-1 (solo vía Katz), definición de muesca de Coles 2000, Shaw 1974, Aibara y Merchant (20 dB de ganancia del oído medio), Stenfelt 2012 (0-10 dB de atenuación transcraneal ósea), Collier 2023 (techo de 60 dB), Mahomed 2013 (dispersión de 6 dB), Mehrparvar 2011 y Mkwanazi 2025, Konrad-Martin 2010, SIOP Boston, Fernandez 2025.
