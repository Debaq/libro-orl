# Agente 07: revisión de H10 (PEAT) y H11 (electrococleografía), 2026-10-22

Leídos completos: capitulos/H10-...md (679 l.), H10-....py, H11-electrococleografia.md (389 l.), H11-....py. Comprobado contra: Katz 7.ª ed. cap. 12 (Santarelli y Arslan, p. 207-220) y cap. 13 (Musiek, p. 231-248; texto extraído en el scratchpad), guía BSA OD104-84 (2019, PDF descargado y leído, Apéndice C y secciones de parámetros), búsqueda web para vía ósea. Cálculos rehechos a mano (aritmética de latencias e interpicos, filtro pasa-alto de primer orden, ruido residual).

Resultado general: capítulos sólidos. No encontré errores de conocimiento GRAVES. Los hallazgos son de coherencia de casos y de cifras puntuales.

## GRAVE

Ninguno.

## IMPRECISO

- **[IMPRECISO] H10 l.422-425 vs l.538 y l.543 (caso Sofía, 81,1/s)** — el pie de figura dice "En el OI, a esta tasa, la **V no se distingue**: queda la I, la III muy aplanada y nada más", pero la tabla del informe da "V a 81,1 estímulos/s: OI 7,37 (+1,30) ↑" y la interpretación usa "el alargamiento de la V con la tasa alta (1,30 ms en el OI frente a 0,57 en el OD)". Las dos cosas no pueden ser ciertas. La figura (figuras/salida/h10_mujer_joven_abr_2.svg) solo marca I y III en el OI, así que el modelo sí tiene una V en 7,37 (7,37 − 6,07 = 1,30) pero el trazo no la muestra. → Decidir una versión: o la V se ve y se marca a 7,37 (y el pie se corrige), o no se ve y el informe debe decir "V no identificable a 81,1/s" (también es hallazgo retrococlear, Katz p. 235: "disappearance of Wave V during the high rep rate recording"). → Alinear pie e informe.

- **[IMPRECISO] H10 l.285, l.498-507 (Álvaro, 12 semanas, referencia de recién nacido)** — se compara a un lactante de 12 semanas (85 días) con la fila "recién nacido de término, 39 a 40 semanas" de Rosa y cols. (2014) y se dice "Son latencias de recién nacido". A los 3 meses la V ya se acortó claramente (Gorga y cols., 1989, que el propio capítulo cita en l.391: la V se acorta rápido hasta los 18 meses). Una V de 6,97 ms y un I-V de 5,24 a las 12 semanas serían largos para su edad, no normales. El .py (l.22-24) reconoce que es un artificio para que LabSim use esa fila. Es un error de procedimiento didáctico: se enseña a usar la norma de otra edad. → Cambiar la edad del caso a un recién nacido real (días a pocas semanas) y mantener la fila de Rosa, o buscar una norma de 3 meses; las correcciones BSA de 12-24 semanas (que sí calzan con la edad) se pueden mantener si se rehace con latencias de 3 meses. No pude abrir Rosa y cols. (2014) para ver sus grupos de edad (scielo no respondió).

- **[IMPRECISO] H10 l.506 (tabla de Álvaro), límite III-V del recién nacido 3,64** — media 2,42 y límite 3,64 implican DE ≈ 0,61, mientras I-III (2,77 / 3,19) tiene DE 0,21 e I-V (5,08 / 5,70) tiene DE 0,31. Si I-V = I-III + III-V, una DE de 0,61 en el III-V es incompatible con 0,31 en el I-V. Parece una errata (¿3,04?). Cálculo: (3,64 − 2,42)/2 = 0,61; (5,70 − 5,08)/2 = 0,31. → Revisar contra Rosa y cols. (2014, tabla); no pude abrirla.

- **[IMPRECISO] H10 l.261-262 y l.290 vs .py l.26 (ventana del burst de 1 kHz)** — el .py registra el burst de 1 kHz con `ventana=20`, el pie de figura dice "cerca del borde de la ventana de 12 ms" y el informe (l.491) dice "ventana de 12 ms" para los tres casos. Además el .py pide niveles (40, 20, 10) pero el pie y el informe hablan de 40 y 20. → Alinear texto con el .py (ventana de 20 ms con burst, como dice H11 l.153 y l.227, y niveles realmente registrados).

- **[IMPRECISO] H10 l.416 vs tabla de l.409-415** — la frase "Una pérdida periférica (conductiva o coclear) alarga las latencias absolutas" contradice la fila "Coclear: casi normales a intensidad alta" de la tabla. En pérdida coclear de agudos la V a intensidad alta solo se atrasa si la pérdida es importante (Katz p. 234-235, y el propio caso Juan Joaquín, V normal). → "una pérdida conductiva alarga todas las latencias; una coclear de agudos puede atrasar la V y hacer faltar la I, pero deja normales los interpicos".

- **[IMPRECISO] H11 l.116 y l.168, l.315 (pérdida marcada y nivel bajo hacen que "la razón salga chica")** — se afirma sin cita que con pérdida marcada o a 60 dB nHL la razón PS/PA "sale chica aunque haya hidrops". No lo encontré en Katz (Santarelli y Arslan, p. 218-219), que solo muestra que un oído coclear sin hidrops con PTA 45 tiene razón 0,14 y dos Ménière con PTA 30 y 45 tienen 0,46-0,48; no trata el efecto del nivel. En la práctica con pérdida severa el PA falta y la razón no es interpretable (no "chica"). → Citar fuente (Ferraro y Durrant 2006, que no pude leer) o reformular: "con pérdida marcada el PA es pequeño o falta y la razón deja de ser interpretable".

- **[IMPRECISO] H11 l.278-281 (razón de áreas 1,94 aplicada a los tres electrodos)** — el propio capítulo admite que 1,94 se publicó con electrodo timpánico y que con promontorio no mejoró (Baba 2009). Además Katz (p. 219) presenta el índice de áreas de Ferraro y Tibbils (1999) para estímulo tone burst y dice que no está claro que aporte ventaja sobre SP/CAP. Está advertido en el texto; solo falta decir que con conducto y promontorio el 1,94 no tiene respaldo propio. Sin corrección obligatoria.

## DISCUTIBLE

- **[DISCUTIBLE] H10 l.165, l.191 y tabla de rutina (tasa 21,1/s para el ABR neurootológico)** — el capítulo enseña 21,1/s como rutina y, en el mismo capítulo (l.191), dice que sobre ~20 a 30/s la latencia aumenta y la onda I se achica (BSA, 2019). La BSA OD104-84 (l.899-904) usa para el ABR neurodiagnóstico una tasa **bajo 20/s, comúnmente 11,1/s**, justo "para preservar la onda I"; Katz cap. 13 (p. 234) reporta casos a 11-17/s. Hood (1998) y la ACNS aceptan ~21/s. Postura A: 21,1/s (protocolo ORL, ACNS). Postura B: 11,1/s (BSA 2019, Katz cap. 13). Sugerencia: decir las dos.

- **[DISCUTIBLE] H10 l.322 (V por vía ósea en el lactante llega antes que por aérea)** — se afirma sin matiz, citando a Seo y cols. (2018), que no pude abrir. La literatura discrepa: algunos trabajos reportan latencia ósea más corta que la aérea en lactantes (Yang y cols. 1987; Foxe y Stapells 1993, para tonos de 500 Hz), otro estudio brasileño en menores de 2 meses halló la latencia ósea mayor que la aérea. Katz p. 260-261 solo dice que las latencias óseas "varían ligeramente" por las diferencias espectrales del vibrador. → Matizar ("suele"/"en varias series").

- **[DISCUTIBLE] H10 l.383 y l.437 (diferencia interaural de V "0,2 a 0,4 ms")** — Katz cap. 13 (p. 235) dice "most would agree ... greater than 0.3 to 0.4 ms". El libro lo cubre al citar las dos posturas (Hood 1998 y Musiek 2015). Katz agrega que la corrección de Selters y Brackmann (0,1 ms por cada 10 dB de pérdida a 4 kHz sobre 50 dB HL) puede ser inútil, y la BSA (l.1038-1039) la describe. El capítulo solo dice que "con pérdida de agudos asimétrica la diferencia aparece sola"; vale mencionar esta corrección. Sofía (35-50 dB a 2-4 kHz) queda bajo el umbral de 50 dB, así que el caso no se afecta.

## Revisado sin hallazgos (según la fuente que pude consultar)

H10: generadores de ondas I-V (Møller), reducción de ruido por raíz de N (1.000→2.000 = 29 %), orden de pasos del umbral (80, de 20 en 20 hacia abajo, 10 en 10 hacia arriba, escalón sin onda V), FSP 3,1 y 1 sin respuesta, montaje y electrodos (Cz, mastoides, tierra en frente, A1/A2), impedancias (<5 kΩ, BSA prefiere <2 kΩ, l.381), filtros 100-3.000 y rechazo ±10 µV para ABR neurológico (BSA l.909-922), retardo de fono de inserción ≈ 0,9-1 ms (Katz p. 234 "subtract 0.9 ms"), tabla de corrección nHL→eHL (coincide exactamente con la BSA 2019, Apéndice C, tablas para 12-24 semanas y >2 años, click, tone pip y chirp), AABR 35 dB nHL, JCIH 2019 (AABR si UCI >5 días), umbral de ABR óseo en adulto vs lactante (Stuart 1993), razón V/I <0,75 (Katz p. 235 y 240), I-V >4,4 ms (Katz p. 234), patrón retrococlear (Katz p. 235: I presente y resto ausente), tasa alta 11 vs 81/s (Katz p. 235, el libro usa 21,1 vs 81,1), artefactos y falsa onda V, aritmética de todos los interpicos de los tres casos (Sofía, Álvaro, Juan Joaquín: restas verificadas), diferencia interaural de Sofía (6,07 − 5,53 = 0,54) y de Juan Joaquín (0,17), conclusiones de los informes, eHL de los tres casos (10−5, 20−15, 50−5, 40−15, 40−15).

H11: MC (origen en células ciliadas externas sobre todo, Katz p. 208), PS (origen mixto, Katz p. 208), PA = onda I, mecanismo del punto de trabajo del hidrops (presentado como hipótesis), ganancia de 50.000 con aguja y 500 barridos por polaridad transtimpánico, al menos 1.000 extratimpánico, filtro 5-8.000 Hz (Santarelli y Arslan en Katz p. 211), umbral SP/CAP 0,3-0,4 (Katz p. 218), duración prolongada y diferencia de latencia entre polaridades como índices adicionales (Katz p. 219), cálculo del pasa-alto de primer orden sobre la meseta de 12 ms (5 Hz: 1−e^(−2π·5·0,012) = 31 %, "cerca de un tercio"; 10 Hz: 53 %, "más de la mitad"; 100 Hz: 99,9 %, "desaparece"), tiempo de 1.500 barridos a 11,1/s (135 s, "algo más de dos minutos"), la figura de Patricia (razones 0,25 / 1,17 / 0,63 / 3,87 y latencias 1,37 / 1,50 coinciden con el SVG figuras/salida/h11_p38_ecochg.svg), ejemplo del conducto con razón 0,45 (alterada en promontorio y tímpano, normal en conducto: consistente con la tabla).

## No se pudo comprobar con fuente

- Sanfins y cols. (2026): todos los límites de la tabla de adultos (l.393-403) y la afirmación de las mujeres 0,08-0,19 ms antes (artículo no disponible; no se buscó en la web). Se verificó solo consistencia interna.
- Rosa y cols. (2014), valores de recién nacido (l.498-507): scielo no cargó.
- Delgado Hernández y cols. (2003), Jerger y Hall (1980), Gorga (1989), Sharma (2016), Jiang (1991, 4-15 % de alargamiento con la tasa), Stockard (1979), Pinto y Matas (2007), Cargnelutti (2017, V más grande con CE-Chirp), Fuentes y cols. (2024), Seo (2018): no hay copia local ni se buscaron.
- ACNS 2008 (recomendaciones de pasa-alto, 1.000-4.000 barridos, ventana de 15 ms en menores de 18 meses), Hall 2007, Hood 1998 (cap. 9) y Hood 2015 de tasa/polaridad: Hood 2015 está en Katz p. 249-266 pero no se leyó completo.
- H11: Ferraro y Durrant 2006, Wuyts 1997 (0,35 / 0,42), Margolis 1995, Devaiah 2003 (1,94), Satar 2003 (0,38 ms y 0,32; artículo en turco), Ge y Shea 2002 (62 %), Lamounier 2014 (25-50 % normales en Ménière), Roland 1993 (0,50), Moffat 1978: no consultados. Santarelli y Arslan (Katz) no los reproduce.
- MANUAL-DE-PEAT.docx y MANUAL-Electrofisiologia.docx: no se abrieron (la verificación con Katz y BSA cubrió lo esencial).

## Nota de política (no es error de conocimiento)

H11-electrococleografia.py usa `demo(38)` (paciente de práctica de LabSim, "Patricia"); según la nota de la memoria del proyecto, los pacientes demo 33-42 salen del libro y los casos propios usan `cuadro()`. H10 ya lo hizo; H11 queda pendiente.

## Conteo

GRAVE 0 · IMPRECISO 7 · DISCUTIBLE 3
