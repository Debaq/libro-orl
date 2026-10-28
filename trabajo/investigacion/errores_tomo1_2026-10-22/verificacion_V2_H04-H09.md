# Verificación V2: imprecisos de H04 a H09 (2026-10-22)

Verificador V2. Se juzgó el texto ACTUAL de los capítulos (H04 y H05 ya con la regla del habla de 40/60 dB contra el mejor óseo). Fuentes leídas: Katz 7.ª ed. (cap. 6, pp. 77-105; cap. 13, p. 237; cap. 33, p. 622), BSA 2018 (audiometría tonal con enmascaramiento, texto completo), BSA 2022 (LDL, texto completo), BSA 2026 (timpanometría y reflejos, texto completo), BSA 2025 (acústica en clínicas, texto completo), ASHA 1988 (texto completo, asha.org), Moore (cap. 4), Europe PMC y un buscador web. Cuentas rehechas con python3.

Nota: el informe del agente 05 dice "16 imprecisos (H06: 6)", pero lista 15 (H04: 5, H05: 5, H06: 5). Aquí se evalúan los 15 listados.

---

## AGENTE 05

### H04

**05-H04-a. Fórmulas sin margen +10 al mínimo ni −5 al máximo.** CONFIRMADO.
Fuente: Katz cap. 6 (Yacullo), p. 93 ("a safety factor of not less than 10 dB should be added to the calculated minimum masking level", Studebaker 1979; Martin 1974); p. 94 ("M Max = BC Test Ear + IA − 5 dB", fórmula dada para tonos, aérea y ósea); p. 103 (el −5 también en habla; el libro ya lo tiene en habla). Katz agrega que las fórmulas son poco prácticas en umbrales y recomienda el plateau; el libro ya lo hace. Cuentas: aérea OI, mínimo 10 (20 con margen), máximo 65 (60 con −5); ósea OI, mínimo 35 (45), máximo 65 (60).
Correcciones (texto actual → nuevo):
- `- Máximo = UO evaluado + AI` → `- Máximo = UO evaluado + AI − 5`
- `- Máximo = UO evaluado + AI del fono que lleva el ruido` → `- Máximo = UO evaluado + AI del fono que lleva el ruido − 5`
- Después de la línea `UA: umbral aéreo. UO: umbral óseo. AI: ... de una frecuencia.` agregar: `Al mínimo se le suman al menos 10 dB de margen, porque el ruido enmascara distinto en cada persona; al máximo se le restan 5 dB para quedar bajo el sobreenmascaramiento (Yacullo, 2015).`
- `- **Máximo = UO evaluado + AI**: el ruido que pones cruza` → `- **Máximo = UO evaluado + AI − 5**: el ruido que pones cruza`
- `- Aérea del OI: mínimo = 50 − 40 − 0 + 0 = **10 dB**; máximo = 25 + 40 = **65 dB**. Un ruido de unos 40 dB EM en el OD está holgado.` → `- Aérea del OI: mínimo = 50 − 40 − 0 + 0 = **10 dB** (20 con el margen de 10); máximo = 25 + 40 − 5 = **60 dB**. Un ruido de unos 40 dB EM en el OD está holgado.`
- `- Ósea del OI: mínimo = 25 − 0 + 0 + 10 (oclusión, porque el OD es normal) = **35 dB**; máximo = 25 + 40 = **65 dB**. El ruido tiene que ir entre 35 y 65.` → `- Ósea del OI: mínimo = 25 − 0 + 0 + 10 (oclusión, porque el OD es normal) = **35 dB** (45 con el margen); máximo = 25 + 40 − 5 = **60 dB**. El ruido tiene que ir entre 45 y 60.`
Referencia: Yacullo 2015 ya está en la lista del capítulo; no falta nada.

**05-H04-b. Dilema con inserto: "hay ventana, angosta".** PARCIAL.
Las cuentas del texto son correctas con la fórmula sin márgenes (inserto 55 dB, 250 Hz: mín 50, máx 55). Con el margen de Katz (+10/−5) queda mín 60 y máx 50: no hay ventana (python3). Pero con la AI de inserto que usa Katz (75 dB hasta 1.000 Hz; p. 80 y p. 84) sale mín 30 (40 con margen) y máx 75 (70): sí hay ventana. El libro usa 55 (BSA 2018, Munro y Agnew 1999), válido. Fuente: Katz pp. 80, 84, 93-94.
Corrección: `hay ventana, angosta. Al subir la atenuación, el mínimo baja y el máximo sube a la vez.` → `en el papel hay ventana, de solo 5 dB; con el margen de 10 dB al mínimo y el −5 al máximo ya no la hay. Con los 75 dB de atenuación que Katz usa con inserto hasta 1.000 Hz (Yacullo, 2015) el mínimo baja a 30 y el máximo sube a 70, y sí hay ventana. Al subir la atenuación, el mínimo baja y el máximo sube a la vez.`

**05-H04-c. "Errores frecuentes": comparar con el aéreo del no evaluado vs. regla 1 aéreo-aéreo.** PARCIAL.
Texto actual: `**Comparar con el aéreo del oído no evaluado** en vez de con su óseo. Se pierde el cruce en los casos de la regla 3.` La regla 1 de la tabla sí compara aéreo con aéreo. Fuente: Katz p. 84 ("a preliminary decision... comparing the air-conduction thresholds of the two ears... it will be necessary to re-evaluate... following the measurement of unmasked bone-conduction"); BSA 2018 §8.6.3 ("Rule 1 is merely a convenient way of anticipating the need to mask"; "it is the sensitivity of the non-test cochlea (b-c)... that is the important factor"). No es contradicción, pero la frase puede confundir.
Corrección: `- **Comparar con el aéreo del oído no evaluado** en vez de con su óseo. Se pierde el cruce en los casos de la regla 3.` → `- **Quedarte con la regla 1** (aéreo contra aéreo). Es solo un atajo para anticipar: el cruce lo decide la cóclea del oído no evaluado, así que hay que revisarla con su óseo (regla 3) (BSA, 2018; Yacullo, 2015).`

**05-H04-d. Fila "Habla" sin inserto; Sklare y Denenberg mal atribuida.** YA CORREGIDO.
La tabla actual tiene la fila "Habla con fono de inserción bien puesto | 68 a 84 dB | 60 dB" (Katz p. 82: 68 a 84 dB, Sklare y Denenberg 1987; estimación conservadora 60). Sobre la atribución: Katz p. 81 cita a Sklare y Denenberg (1987) también dentro del rango de 48 a 76 dB con supraaural, así que citarlo en la fila supraaural no es erróneo. Acción: opcional, agregar a Martin y Blythe (1977) y Snyder (1973) a la línea de fuentes (son los del mínimo de 48 dB; no están en la lista de referencias, habría que agregar la referencia completa si se citan; no se pudo verificar el DOI aquí, por eso no se propone).

**05-H04-e. Técnica por pasos (30 dB aérea, 20 dB ósea, pasos de 20 dB) sin fuente.** CONFIRMADO.
Buscado en Katz cap. 6 (pp. 92-98), BSA 2018 y los libros chilenos locales (González 2015 *Audiología básica para estudiantes*, Cuaderno de Audiología; *Audiología clínica y electrodiagnóstico*): ninguno trae esa técnica. BSA 2018 §8.9 (l. 422-423): "Techniques other than those described here are not recommended". Lo más cercano: Martin (1967, 1974) en Katz p. 91-94, nivel inicial = aéreo del no evaluado + 10 dB (+ efecto de oclusión en ósea); y un texto chileno (*Audiología clínica y electrodiagnóstico*, p. 62) que dice "ensordecer con 30 dB sobre el umbral" para la ósea, sin pasos.
Corrección (el comentario `<!-- verificar -->` sigue vigente; si la sección se mantiene): `Cuando hay que enmascarar varias frecuencias y el tiempo es poco, se usa una versión abreviada que solo mira si el umbral se mueve con saltos grandes de ruido:` → `Cuando hay que enmascarar varias frecuencias y el tiempo es poco, algunas cátedras usan una versión abreviada que solo mira si el umbral se mueve con saltos grandes de ruido. Es un protocolo de cátedra: la BSA (2018) no recomienda técnicas distintas del plateau, y Katz parte de otro nivel inicial (umbral aéreo del no evaluado + 10 dB, más el efecto de oclusión en la ósea; Yacullo, 2015). Si el resultado es dudoso, vuelve al plateau.` Alternativa: reemplazar el paso 1 por el nivel inicial de Martin.

### H05

**05-H05-a. "el SRT medido con palabras queda unos 18 dB peor que el PTP" (caso Raúl, demo 39).** CONFIRMADO.
Datos: casos_demo.json, demo 39: SRT OD = 15, SRT OI = 5, SDT OD = 10; PTP OD = (15+20+30)/3 = 21,7 ≈ 22. El SRT (15) concuerda con el PTP (7 dB mejor). Lo que cruza el 50 % a 40 dB es la curva de bisílabos, no el SRT (definido con espondeos, ASHA 1988). Un SRT mucho peor que el PTP tampoco es lo esperable en retrococlear (cae la discriminación, no el umbral). El caso no se mueve; se ajusta el texto.
Corrección: `- @OD 40 | Con un máximo tan bajo, la curva apenas pasa el 50 % a **40 dB**: el SRT medido con palabras queda unos 18 dB peor que el PTP, y no es un error de medición.` → `- @OD 40 | Con un máximo tan bajo, la curva de bisílabos apenas pasa el 50 % a **40 dB**, 18 dB sobre el PTP. El SRT con espondeos sigue concordante (15 dB): lo que falla no es el umbral, es la discriminación (ASHA, 1988).`

**05-H05-b. "Unos 10 dB más abajo detecta la voz" (demo 34, OI).** CONFIRMADO.
Datos demo 34: OI SDT = −5, SRT = 0: 5 dB. En literatura son 8 a 9 dB (ASHA 1988, texto leído: "8-9 dB weaker than the SRT", Chaiklin 1959; Katz p. 81). El texto de la sección (8 a 9) es correcto; la leyenda de la figura no.
Corrección: `Unos 10 dB más abajo detecta la voz sin entender ninguna.` → `Cinco dB más abajo (−5 dB HL) detecta la voz sin entender ninguna; en promedio la diferencia es de 8 a 9 dB (ASHA, 1988).`

**05-H05-c. SRT ascendente "el primer nivel en que repite una de las dos".** CONFIRMADO.
ASHA 1988, nota 6: "In an ascending procedure, start at a level where five out of five or two out of two items are missed and stop the procedure where five out of five or two out of two items are correct. Scoring is identical to the descending procedures." Un criterio de 1 de 2 es más laxo y da un nivel bajo el 50 % (inferencia, no cifra de la fuente).
Correcciones: `El SRT es el primer nivel en que repite una de las dos.` → `El SRT es el primer nivel en que repite las dos (2 de 2), como pide ASHA (1988) en el método ascendente; con una de dos el nivel sale más bajo que el 50 %.` Y en la ayuda memoria: `vale el primero con una de dos.` → `vale el primero con las dos correctas.`

**05-H05-d. Tono "de menos de 1 segundo" vs. BSA 1 segundo.** CONFIRMADO.
BSA 2022 (LDL) §4.3 punto 3: "Present a 1-second-long tone, followed by at least a 1-second quiet period"; pausa de 2 a 5 s para responder (punto 4). La frase "sin cansar ni dejar un acúfeno" no tiene respaldo en la BSA; la BSA justifica limitar frecuencias y nivel máximo por riesgo de exposición.
Correcciones: `2. Presenta **tonos cortos**, de menos de 1 segundo, de 250 a 4.000 Hz.` → `2. Presenta **tonos de 1 segundo**, seguidos de al menos 1 segundo de silencio, de 250 a 4.000 Hz (BSA, 2022).` Y: `El tono corto basta para juzgar la sonoridad sin cansar ni dejar un acúfeno, y los pasos de 5 dB evitan pasarse de golpe.` → `Los pasos de 5 dB evitan pasarse de golpe, y limitar frecuencias y nivel máximo reduce la exposición a sonidos fuertes (BSA, 2022).`

**05-H05-e. LDL "Parte en 80 dB HL ... hasta la salida máxima del equipo".** PARCIAL.
BSA 2022 §4.3 punto 2: parte en 60 dB HL o en el umbral, el que sea mayor (en acúfeno o hiperacusia, en el umbral); §4.4: en pérdida leve a moderada no pasar de 90 dB HL (sobre eso, justificar). El recuadro de normas del capítulo lo dice, pero el paso numerado y la ayuda memoria enseñan 80 dB y tope del equipo. Los casos (demo 34 y 39, LDL 120 "tope del equipo") no se mueven: se ajusta el texto.
Correcciones: `3. Parte en **80 dB HL** y sube de 5 en 5 hasta que avise o hasta la salida máxima del equipo.` → `3. Parte en **60 dB HL** o en el umbral de esa frecuencia, el que sea mayor, y sube de 5 en 5 hasta que avise. En pérdida leve a moderada no pases de 90 dB HL sin una razón clínica anotada (BSA, 2022).` Ayuda memoria: `**LDL:** tonos cortos desde 80 dB HL, de a 5.` → `**LDL:** tonos de 1 segundo desde 60 dB HL (o el umbral), de a 5.` Caso Raúl (figura del audiograma): `El LDL del OD llega a **120 dB** en 3 y 4 kHz, el tope del equipo:` → `El LDL del OD llega a **120 dB** en 3 y 4 kHz, el tope del equipo (sobre los 90 dB HL de la BSA, que en la práctica exigen justificar):`. En el recuadro de normas, borrar `Partir en 80 dB acorta la prueba;` (ya no calza).

### H06

**05-H06-a. Rosenberg atribuido a Olsen y Noffsinger 1974.** PARCIAL.
El artículo (PMID 4809949, Arch Otolaryngol 1974;99:94-9, "Comparison of one new and three old tests of auditory adaptation") compara varias pruebas, entre ellas el Rosenberg y el Carhart (resumen de JAMA Otolaryngology según la búsqueda web: compara Carhart y Rosenberg con Békésy y un test a 20 dB SL propio). No es la fuente original del Rosenberg. No se pudo abrir el texto ni el trabajo original de Rosenberg (1958, presentación en congreso); no se propone referencia sin comprobarla. Partida a 5 dB SL: solo un fabricante (Interacoustics) en la búsqueda; sigue sin fuente primaria (el `<!-- verificar -->` se mantiene).
Corrección: `y se informa **cuántos dB hubo que subir en ese minuto** (Olsen y Noffsinger, 1974).` → `y se informa **cuántos dB hubo que subir en ese minuto**. Es la prueba de Rosenberg, que Olsen y Noffsinger (1974) compararon con el Carhart y otras.`

**05-H06-b. Faltan Békésy, Green, Olsen-Noffsinger.** FALSO como error.
Es una omisión, no un dato falso. Katz (cap. 5/cap. 6, índice y p. 44 citan el audiómetro de Békésy; en el cap. 33 dice "Békésy audiometry has decreased in medical settings" y "has not been practiced...") confirma su desuso. El capítulo no promete esas pruebas. Sin acción; opcional una frase de vigencia.

**05-H06-c. "un oído muerto responde por el otro alrededor de los 40 a 60 dB".** CONFIRMADO.
Katz p. 79: la atenuación interaural con supraaural va de "about 40 to 85 dB"; con inserto sobre 50 dB. El propio H04 dice 40 a 80. Lo que responde un oído sin audición es AI + óseo del mejor oído.
Corrección: `Sin enmascarar, un oído "muerto" responde por el otro alrededor de los 40 a 60 dB (→ H3, H4).` → `Sin enmascarar, un oído "muerto" responde por el otro desde unos 40 dB con fono supraaural (la atenuación va de 40 a 80 dB según la persona) y desde unos 55 dB con inserto (→ H3, H4).`

**05-H06-d. Stenger "sirve cuando la pérdida es de un solo oído o muy asimétrica".** CONFIRMADO.
Katz cap. 33 (Martin y Clark), p. 622: la prueba de tamizaje identifica la presencia de pérdida no orgánica "if there is a difference in admitted threshold between the ears of at least 20 dB"; es más probable que sea positiva con diferencias mayores de 40 dB. El procedimiento del capítulo (bueno +10, malo −10) coincide.
Corrección: `Sirve cuando la pérdida que se informa es de un solo oído o muy asimétrica.` → `Sirve cuando la pérdida que se informa es de un solo oído o muy asimétrica, con al menos 20 dB de diferencia entre los oídos; mientras mayor la diferencia, mejor funciona (Martin y Clark, 2015, p. 622).`
Referencia a agregar: `Martin FN, Clark JG. Nonorganic hearing loss. En: Katz J, Chasin M, English K, Hood LJ, Tillery KL, editores. Handbook of clinical audiology. 7.ª ed. Filadelfia: Wolters Kluwer; 2015. p. 617-29.` (páginas del capítulo: 617-629 según el índice y la numeración vista).

**05-H06-e. SISI: falta duración del incremento; puntaje alto en frecuencias altas.** PARCIAL.
Moore, *Cochlear Hearing Loss*, cap. 4: el SISI mide "brief (200-ms) 1-dB increments in level of a continuous tone presented at 20 dB SL"; también dice que la ventaja coclear existe a igual SL y desaparece a igual SPL (el libro ya lo dice). La afirmación sobre puntajes altos en normales a 4 kHz o más (Buus 1982): NO VERIFICABLE (no se pudo abrir Buus y cols.; no está en Moore ni en Katz).
Corrección (opcional, mejora): `3. **Prueba.** Veinte incrementos de **1 dB**, breves, más o menos uno cada cinco segundos` → `3. **Prueba.** Veinte incrementos de **1 dB** y 200 ms (Moore, 2007), más o menos uno cada cinco segundos`. Verificar que Moore esté en las referencias de H06 (el agente 05 dice que se usó como fuente); si no, agregarla en el formato de la lista.

### DISCUTIBLES del agente 05 (observaciones técnicas)

- **05-D1 AI inserto (55 vs 75/50).** CONFIRMADO como discrepancia real. Katz p. 80: 75 dB hasta 1.000 Hz y 50 dB sobre 1.000 Hz (conservador, espuma profunda); BSA 2018: 55. En agudos Katz es menor que el libro. Sin error; opcional una frase en la nota de fuentes.
- **05-D2 Oclusión (15/15/10/0 vs Yacullo 30/20/10).** CONFIRMADO. Katz p. 94: supraaural 30/20/10 (250/500/1.000 Hz), inserto profundo 10/10/0, y no se suma la oclusión si el no evaluado tiene gap potencial de 20 dB o más. El libro lo declara como valores de la cátedra. Opcional: en `el oído no evaluado **no tiene componente conductivo**` agregar `(Katz: gap potencial menor de 20 dB)`.
- **05-D3 Regla 2 (10 vs 15 dB).** CONFIRMADO. Katz p. 85: ASHA 2005 usa 10 dB, pero Katz considera 10 "too stringent" y usa 15 dB. BSA 2018: 10. Sin error.
- **05-D4 Plateau (10 vs 5 dB).** CONFIRMADO, compatible. Katz p. 97: 5 o 10 dB aceptables, 5 recomendado con plateau angosto; plateau = 15-20 dB sin cambio. BSA: 10 dB, 3 seguidas.
- **05-D5 Habla: PTP vs mejor óseo.** YA CORREGIDO (regla de 40/60 contra el mejor óseo de 250 a 4.000 Hz; Katz pp. 86, 103).
- **05-D6 UMD a SRT+20 y tope de 3 listas.** CONFIRMADO como discrepancia. Katz cap. 5: lo habitual es 30 a 40 dB SL; Kamm y cols. 1983: a 40 dB SL el 40 % de 25 sujetos con pérdida no alcanza el máximo; Wilson sugiere dos niveles de 25 palabras (50 y 70 dB HL si PTA ≤35). Carlo y cols. 2020 NO VERIFICABLE. El libro mitiga con el recuadro "Si la curva sigue subiendo".
- **05-D7 Corte de roll-over 0,45 / 0,35.** NO VERIFICABLE: Katz (cap. 5) menciona el roll-over (Bess 1979; Dirks 1977) sin índice; Jerger y Jerger 1971, Meyer y Mishler 1985 y Gang 1976 sin acceso.

---

## AGENTE 06

**06-a. H07 reflejo contralateral con ruido "en 95 es el mismo reflejo de unos 85 dB HL".** CONFIRMADO.
Texto actual (H07, sección umbral y Metz): `y el ruido contralateral en 95: es el mismo reflejo de unos 85 dB HL, con la corrección de cada transductor y redondeado a 5 dB, el paso del dial.` Contradice la línea de las normas del mismo capítulo ("el ruido de banda ancha unos 20 dB más bajo que los tonos"). BSA 2026, Tabla 2 (Wiley y cols. 1987): ruido de banda ancha contralateral media 66,3 dB HL (límite del 95 %: 80), DE 8,8; ipsilateral 64,6 (75); §10.3: "BBN ARTs are approximately 20 dB lower than tonal ARTs"; "broadband stimuli should be limited to 95 dB SPL" (Arriaga y Luxford 1993). 95 dB SPL queda en el tope y por sobre el 95 % de los oídos normales.
Corrección: `y el ruido contralateral en 95: es el mismo reflejo de unos 85 dB HL, con la corrección de cada transductor y redondeado a 5 dB, el paso del dial.` → `. El ruido de banda ancha da el reflejo unos 20 dB más abajo que los tonos: 66 dB HL de media y hasta 80 dB HL en el 95 % de los oídos normales, y la BSA limita los estímulos de banda ancha a 95 dB SPL (BSA, 2026; Wiley y cols., 1987). Los valores en dB SPL se redondean a 5 dB, el paso del dial.` (cuidar la puntuación al pegar: el texto anterior termina `...95, 90, 95 y 95 dB SPL`). Además, en `**Tope**` (viñeta de la técnica) agregar: `El ruido de banda ancha, no más de 95 dB SPL.` Los datos del paciente 38 no se tocan (la ficha del simulador no es fuente).

**06-b. H07 caso Carolina: reflejo contra en 4 kHz a 120 dB SPL, sobre el tope.** CONFIRMADO.
Datos demo 34: contra [130,110] en 2 kHz y [130,120] en 4 kHz; Aérea OD 40 y óseo OD 15 en 4 kHz (gap 25). Tope del capítulo 105 dB HL = 105 + 9,5 = 114,5 dB SPL en 4 kHz contra (python3); 120 dB SPL = 110,5 dB HL, sobre el tope (BSA 2026: "not recommended that presentation levels go above 105 dB HL"). En 2 kHz, 110 dB SPL = 101 dB HL, dentro del tope. 500 y 1.000 Hz ausentes: 1 kHz, tope 112 dB SPL contra, coherente. El caso no se mueve; se ajusta el texto.
Correcciones: figura: `110 dB SPL en 2 kHz, 120 en 4 kHz, y ausente en 500 y 1000 Hz, donde el gap es de 40 y 30 dB.` → `110 dB SPL en 2 kHz (101 dB HL) y ausente en 500 y 1000 Hz, donde el gap es de 40 y 30 dB. En 4 kHz aparece en 120 dB SPL, 110,5 dB HL, sobre el tope de 105 dB HL: en la clínica la prueba se habría detenido antes, y se deja para ver cuánto sube el reflejo.` Informe de ejemplo: `presentes a 110 dB SPL en 2 kHz y 120 dB SPL en 4 kHz.` → `presentes a 110 dB SPL en 2 kHz; en 4 kHz no se registra dentro del tope de 105 dB HL.` (esto último solo si el autor acepta que el informe diga distinto a la ficha; si no, dejar el informe y solo corregir la leyenda).

**06-c. H07 / H09 caso Benjamín: volumen OD 0,42 mL llamado normal.** CONFIRMADO.
Benjamín tiene 5 años (casos_demo 35: edad 5; volumen [0,42; 0,70]). BSA 2026 §11.1.4: rango del 90 % del ECV a los 5-7 años = 0,7-1,3 cm³ (Swanepoel y cols. 2014); un plano con ECV pequeño puede indicar sonda ocluida (l. 646). El capítulo (H07) da 0,7 a 1,3 y dice que "volumen muy bajo" es sonda tapada o apoyada.
Correcciones: H07: `- Los volúmenes son de 0,42 y 0,70 mL, pequeños y propios de un conducto infantil: la sonda está frente a un tímpano cerrado. Plano con volumen normal es **efusión**,` → `- Los volúmenes son de 0,42 mL (OD) y 0,70 mL (OI). El del OI está en el límite inferior del rango de 5 a 7 años (0,7 a 1,3 mL) y el del OD bajo él: se repite con la sonda bien sellada para descartar que esté apoyada en la pared (BSA, 2026). Con la sonda bien puesta, plano con volumen normal es **efusión**,` (el resto de la frase sigue). H09: `Benjamín tiene timpanogramas tipo B en los dos oídos, con volumen normal: efusión (→ H7).` → `Benjamín tiene timpanogramas tipo B en los dos oídos, con volumen en el límite bajo (0,42 y 0,70 mL; se repite con la sonda bien sellada) y los tímpanos con nivel líquido: efusión (→ H7).`

**06-d. H08 "3,8 dB dividido por la raíz de 3, unos ±2,7 dB".** CONFIRMADO.
python3: 3,8/√3 = 2,194. El ejemplo de la guía BSA (acústica en clínicas 2025, l. 1264-1266) trae "(3.8)/√3 = ± 2.7 dB", error aritmético de la guía.
Corrección: `la contribución es 3,8 dB dividido por la raíz de 3, unos ±2,7 dB (BSA, 2025b).` → `la contribución es 3,8 dB dividido por la raíz de 3, unos ±2,2 dB (la guía de la BSA, 2025b, escribe ±2,7 en este ejemplo, pero la cuenta da 2,2).`

**06-e. H07 "Se parte en 80 dB y se sube de 5 en 5".** CONFIRMADO.
BSA 2026 §10.3: "The intensity should start from 60-70 dB HL (60 dB HL for BBN and 70 dB for pure tone stimuli)"; si hay reflejo en la primera presentación, bajar 10 dB y empezar otra vez (puede ser artefacto de sonda). Tabla 2: umbral ipsi medio en 500 Hz = 79,9 dB HL, por lo que partir en 80 hace que la mitad de los oídos normales responda en la primera presentación.
Correcciones: `- Se parte en **80 dB** y se sube de **5 en 5** hasta ver la deflexión.` → `- Se parte en **70 dB HL** con tonos y **60 dB HL** con ruido, y se sube de **5 en 5** hasta ver la deflexión. Si ya responde en la primera presentación, se baja 10 dB y se reinicia (BSA, 2026).` Y en el resumen del procedimiento: `desde 80 dB de 5 en 5` → `desde 70 dB HL (tonos) o 60 dB HL (ruido), de 5 en 5`.

**06-f. H09 neuropatía auditiva: "OEA presentes con ABR ausente" sin microfónica coclear.** CONFIRMADO.
Katz cap. 13, p. 237: en el ANSD la ABR no tiene ondas medibles, pero "a cochlear microphonic should be present... ABR tracings which lack the cochlear microphonic are likely the result of instrumental or clinician error". Además las OEA pueden estar presentes o ausentes según la cóclea (p. 238, hipoplasia del nervio); en el ANSD pueden desaparecer con el tiempo (clínica; no se contrastó en una cita aquí, por eso la frase propuesta usa "suelen"). El capítulo H10 ya trata la microfónica (cap. 13 del libro).
Correcciones (texto actual → nuevo): `Una neuropatía auditiva tiene OEA normales y un ABR ausente (Starr y cols., 1996).` → `Una neuropatía auditiva suele tener OEA presentes, microfónica coclear presente y un ABR ausente o muy alterado (Starr y cols., 1996; Katz, cap. 13, p. 237).` Y: `- OEA presentes con ABR ausente: **neuropatía auditiva**. Las células ciliadas externas funcionan;` → `- OEA presentes con ABR ausente y microfónica coclear presente: **neuropatía auditiva** (si no hay microfónica, primero se revisa el equipo y el estímulo). Las células ciliadas externas funcionan;`. Y: `Presentes con ABR ausente: después de la cóclea.` → `Presentes con ABR ausente y microfónica presente: después de la cóclea.`
Referencia, si no está en la lista de H09: la del cap. 13 de Katz en el mismo formato que la de Prieve (el autor del capítulo no se leyó en el índice; completar con el nombre): `... Auditory brainstem response: differential diagnosis. En: Katz J, Chasin M, English K, Hood LJ, Tillery KL, editores. Handbook of clinical audiology. 7.ª ed. Filadelfia: Wolters Kluwer; 2015. p. 233-45.` (p. final aproximado).

### DISCUTIBLES del agente 06

- **06-D1 H08: parlantes a 45° con cero de campo libre frontal.** PARCIAL. BSA 2025 (acústica, l. 714-719): el RETSPL (ISO 389-7:2019) se derivó con fuente frontal (0°); hay correcciones de ISO 8253-2 para 45° y 90°, "two loudspeakers at 90° is the recommended layout", y no se recomienda usarlas en la clínica. El libro ya lo dice en el recuadro (H08 l. 211). Opcional: en el paso 1 (`con los parlantes a **45°** a cada lado de la línea de la nariz`) agregar `; a 45° el nivel puede diferir unos dB del dial, por eso se calibra en el punto y con la geometría de uso (BSA, 2025b)`.
- **06-D2 H09: TEOAE "pasa" con 3 de 5 bandas.** NO VERIFICABLE aquí (AAA 2020 no se abrió; el archivo local de AAA es la guía de TPA, no la de evaluación infantil). Nota: 3 de 5 es una mayoría, así que no contradice por sí mismo "la mayoría de las bandas"; la categoría "presente pero no normal" (menos de 75 %) no se pudo comprobar. Decisión del autor ya marcada en el .md.

---

## Conteo por veredicto

Imprecisos (15 listados del agente 05 + 6 del agente 06 = 21):
- CONFIRMADO: 14 (05: H04-a, H04-e, H05-a, H05-b, H05-c, H05-d, H06-c, H06-d; 06: a, b, c, d, e, f)
- PARCIAL: 5 (05: H04-b, H04-c, H05-e, H06-a, H06-e)
- FALSO: 1 (05-H06-b, omisión, no error)
- YA CORREGIDO: 1 (05-H04-d)
- NO VERIFICABLE: 0

Observaciones DISCUTIBLES (9): CONFIRMADO como discrepancia sin error 5 (05-D1, D2, D3, D4, D6); YA CORREGIDO 1 (05-D5); PARCIAL 1 (06-D1); NO VERIFICABLE 2 (05-D7, 06-D2).

Partes no verificables dentro de entradas: puntajes altos del SISI a frecuencias altas (Buus 1982), referencia original de Rosenberg 1958, autor/páginas del cap. 13 de Katz, Carlo y cols. 2020, Meyer y Mishler 1985, Gang 1976, AAA 2020 (criterio de bandas TEOAE).
