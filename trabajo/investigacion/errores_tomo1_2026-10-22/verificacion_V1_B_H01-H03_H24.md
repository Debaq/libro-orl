# Verificación V1: B01-B05, H01-H03, H24 (2026-10-22)

Fuentes usadas: Europe PMC (resúmenes), Katz 7.ª ed. (pdftotext local), BSA 2018 PTA y BSA 2022 Rinne/Weber (texto ya extraído en el scratchpad de otros agentes), Snell 7.ª ed. (local), Ecevit 2021 (PMC8221269, texto completo), cálculos con python3. NIOSH 98-126 no se pudo abrir (CDC devuelve HTML/404).

## Agente 01 (B01, B03)

### 01-a B03 l.311 (resp. 6) vs l.179, Merchant 2005 — FALSO
Texto: "Los 28 casos clásicos de Ménière tenían hidrops, pero también había hidrops en oídos sin los síntomas, y algunos con síntomas no lo tenían (Merchant y cols., 2005)."
Resumen de Merchant 2005 (PMID 15699723): los 28 casos con Ménière tenían hidrops; 19 casos con hidrops sin síntomas; y "a review of the literature revealed ... cases where symptoms of Meniere's syndrome existed during life but no hydrops was observed". El artículo sí dice lo de la respuesta 6 (en su revisión de la literatura). No hay contradicción con l.179. Sin cambio. (Opcional, precisión: "y la literatura revisada describe casos con síntomas sin hidrops".)

### 01-b B01 l.61 "tercio óseo" — CONFIRMADO
Fuente: la tabla de B01 l.54-57 y B03 l.57 (hueso = dos tercios internos).
Actual: `el tercio óseo es estrecho, delgado y sangra con facilidad (→ H1).`
Nuevo: `la parte ósea (los dos tercios internos) es estrecha, delgada y sangra con facilidad (→ H1).`

### 01-c B01 l.397 utrículo/sáculo por rama — CONFIRMADO (menor)
B01 l.300-306 dice que parte del sáculo va por la superior.
Actual: `van el **utrículo** (rama superior) y el **sáculo** (rama inferior).`
Nuevo: `van el **utrículo** (sobre todo por la rama superior) y el **sáculo** (sobre todo por la inferior).`

### 01-d B01 l.379 VOR vertical y FLM — FALSO
Texto: "...el fascículo, que también los lleva, lesionado, altera el VOR vertical". PMID 28879396 (VOR en lesiones del FLM): "the MLF is the final common pathway ... for the vertical-torsional VOR"; mide ganancia reducida de canales anteriores y posteriores en INO. Que otros haces (brachium conjunctivum, tractos tegmentales ventrales) lleven parte del canal anterior no vuelve falsa la frase. Sin cambio.

### 01-e B03 l.259 picazón y parasimpático — CONFIRMADO (menor)
Ecevit 2021 (PMC8221269): la histamina "stimulates the sensory nerve endings of the trigeminal nerve, and causes sneezing, itching"; los nociceptores despolarizados dan la picazón. Los vasos (congestión) y glándulas (secreción) dependen del tono vascular/parasimpático.
Actual: `y eso produce los síntomas de la rinitis: congestión, picazón y secreción (Ecevit y cols., 2021).`
Nuevo: `y eso produce la congestión y la secreción de la rinitis; la picazón y el estornudo vienen de las terminaciones sensitivas del trigémino, que estimula la histamina (Ecevit y cols., 2021).`
(Ecevit ya está en la lista de referencias.)

### 01-f B03 l.175 "mecanismo común es el estrés oxidativo" — PARCIAL
Resumen Henderson 2006 (doi 10.1097/01.aud.0000191942.36672.f3): las especies reactivas de oxígeno "play a significant role in noise-induced hair cell death"; también describe muerte necrótica y apoptótica. "Común" sobrepasa lo que dice.
Actual: `El mecanismo común es el estrés oxidativo (Henderson y cols., 2006).`
Nuevo: `Un mecanismo central es el estrés oxidativo (Henderson y cols., 2006).`

### 01-g (discutible) B01 l.626 neumatización, Adibelli 2011 — FALSO
Resumen (PMID 21711972): "initial signs of pneumatization ... at birth for maxillary and ethmoid, at 9 months for sphenoid, and after the age of 5 years for the frontal". El texto cita bien. Sin cambio.

### 01-h (discutible) B01 l.331 áreas 41 y 42 — FALSO
Snell, Neuroanatomía 7.ª ed. (local): "El área auditiva primaria (áreas de Brodmann 41 y 42)". El texto cita bien. Sin cambio.

## Agente 02 (B02, B04)

### 02-a B04 l.373 signos de la distancia — CONFIRMADO
Cálculo: 20 log(1/0,9) = +0,92; 20 log(1/1,1) = −0,83; a 0,5 m: +1,94 y −1,58 (coincide con la resp. 10).
Actual: `el nivel cambia entre +0,8 y −0,9 dB; a 0,5 m, la misma desviación cambia entre +1,6 y −1,9 dB.`
Nuevo: `el nivel cambia entre +0,9 y −0,8 dB; a 0,5 m, la misma desviación cambia entre +1,9 y −1,6 dB.`

### 02-b B04 l.112 filtro 100-3.000 Hz — PARCIAL
Las citas del propio párrafo (Hall 1986: picos en 0-200, 500-600, 900-1.000 Hz; Sininger 1995: lactante bajo 100 Hz) dejan fuera bajo 100 Hz parte de la energía; "el grueso" no es exacto. El filtro es el estándar clínico.
Actual: `Un pasa altos de 100 Hz y un pasa bajos de 3.000 Hz dejan adentro el grueso de la respuesta y sacan buena parte de lo demás,`
Nuevo: `Un pasa altos de 100 Hz y un pasa bajos de 3.000 Hz son un compromiso: conservan las ondas rápidas, sacan buena parte del EEG lento y del ruido, y pierden algo de la energía más grave (más en el lactante),`

### 02-c B04 l.63 artefacto y polaridad — CONFIRMADO
Katz 7.ª ed., cap. 11 (ABR, ~p. 236 del libro; líneas 16370-16380 del texto): "alternating polarity reduces stimulus artifact"; al invertir la polaridad "the waves also invert, consistent with ... the CM". Es decir: artefacto y microfónica invierten con el estímulo; la respuesta neural no.
Actual: `y el artefacto eléctrico del estímulo, que no se invierte con la respuesta, se cancela al promediarlos (→ H10).`
Nuevo: `y el artefacto eléctrico del estímulo (y la microfónica coclear) invierte su signo con la polaridad, la respuesta neural no, así que lo primero se cancela al promediar y lo segundo queda (Katz, 2015; → H10).`

### 02-d B04 l.96 NBN "algo mayor que la banda crítica ... un tercio de octava" — CONFIRMADO
Cálculo: ancho de tercio de octava = 0,2316 f: 58 Hz en 250, 116 en 500, 232 en 1.000. Banda crítica (Zwicker–Terhardt) 105, 117, 162 Hz. Bajo 500 Hz el tercio es más angosto (lo dice el propio capítulo en l.106).
Actual: `de un ancho algo mayor que el de la banda crítica (del orden de un tercio de octava, según el equipo;`
Nuevo: `de un ancho algo mayor que el de la banda crítica (sobre 500 Hz, del orden de un tercio de octava; bajo 500 Hz el tercio de octava es más angosto que la banda crítica, → Banda crítica; según el equipo,`

### 02-e B04 l.404 acoplador 2 cm³ e IEC 60118-0 — PARCIAL
Katz 7.ª ed. cap. 39: el acoplador de 2 cm³ lo define ANSI S3.7 (1995) y "the parallel IEC standard is IEC 60118-0" para la medida del audífono. La parte IEC del acoplador es IEC 60318-5 (de memoria, no está en Katz). No está mal citar 60118-0, pero falta la norma del acoplador.
Actual: `no un modelo del oído de nadie (IEC 60118-0, 2022).`
Nuevo: `no un modelo del oído de nadie (ANSI S3.7, 1995, según Katz, 2015; IEC 60118-0, 2022).`
(Katz 2015 ya está en la lista de B04 l.594. ANSI S3.7 se cita "según Katz" para no agregar referencia.) Si el autor quiere IEC 60318-5, hay que agregarla y comprobarla (no la pude abrir).

### 02-f B04 l.303 "amplitudes se suman como las varianzas" — CONFIRMADO
Actual: `sus amplitudes se suman como las varianzas, es decir, crecen con √*N* al sumar,`
Nuevo: `sus varianzas se suman, es decir, su amplitud crece con √*N* al sumar,`

### 02-g (discutible) B04 l.223 IA con inserción 55 dB — PARCIAL (discrepancia, no error)
BSA 2018 (l.282 del texto): "transmission loss of 55 dB if the earphones are inserted correctly (Munro y Agnew)": el libro cita bien. Katz cap. 6 (p. 79-80): con ER-3A de inserción profunda, valores conservadores 75 dB en ≤1.000 Hz y 50 dB sobre 1.000 Hz. Con 50 en agudos, el 55 del libro es menos conservador que Katz sobre 1 kHz.
Actual: `**55 dB** o más con inserción y casi 0 con el vibrador óseo (BSA, 2018; Munro y Agnew, 1999; Stenfelt, 2012).`
Nuevo: `**55 dB** o más con inserción bien colocada (BSA, 2018; Munro y Agnew, 1999); Katz usa 75 dB hasta 1.000 Hz y 50 dB sobre 1.000 Hz con inserción profunda (Katz, 2015, cap. 6), y casi 0 con el vibrador óseo (Stenfelt, 2012).`

### 02-h B02 l.44 olivococlear lateral "sobre las CCE" — NO VERIFICABLE (menor; conocimiento estándar: el lateral actúa sobre dendritos de fibras aferentes tipo I, el medial sobre las CCE)
Actual: `qué hace sobre las CCE, protección y escucha en ruido`
Nuevo: `qué hace el medial sobre las CCE (el lateral actúa sobre las fibras aferentes), protección y escucha en ruido`
Estado: NO VERIFICABLE con fuente primaria en esta pasada (conocimiento estándar, Pickles).

## Agente 03 (H24)

### 03-a H24 l.498 protector 30 dB, media hora → 15 dB — CONFIRMADO (cuenta)
A = −10 log10[f·10^(−A0/10) + (1−f)], f = 7,5/8: 30 min → 11,98 dB; 15 min → 14,92 dB. NIOSH 98-126 no se pudo abrir (CDC 404; búsqueda web sin el pasaje). El 15 dB corresponde a un cuarto de hora, no a media.
Actual: `un protector que protegería 30 dB, sacado media hora acumulada en un turno de 8, protege solo 15 dB (NIOSH, 1998).`
Nuevo: `un protector que protegería 30 dB, sacado un cuarto de hora acumulado en un turno de 8, protege solo unos 15 dB (cálculo con la fórmula de atenuación efectiva; la idea, en NIOSH, 1998). Sacado media hora, unos 12 dB.`
(Si el autor puede abrir NIOSH y el pasaje dice media hora y 15 dB, el error es de la fuente; en ese caso conviene decirlo con la cuenta.)

### 03-b H24 l.493 NIOSH 70 % vs 75 % en cap. 6 — NO VERIFICABLE
No pude abrir NIOSH 98-126 (CDC 404/HTML). La búsqueda web confirma 25/50/70 % y menciona una versión multiplicativa (conservar 75 % para orejeras) que podría explicar un "75" en otro punto del documento. Recomendación: abrir el PDF antes de afirmar una discrepancia; si no se puede, dejar `y **70 %** en los demás tapones (NIOSH, 1998)` y quitar el paréntesis `(en su capítulo 6 ... no se explica)`.

### 03-c H24 l.106 "UE, Chile, Canadá y Australia" — PARCIAL
Canadá regula por provincia (la mayoría 85 dB(A)/3 dB; Quebec ha usado 90 dB(A)/5 dB; de memoria, sin fuente abierta).
Actual: `es la que usan la Unión Europea, Chile, Canadá y Australia, entre otros;`
Nuevo: `es la que usan la Unión Europea, Chile, Australia y varias provincias de Canadá, entre otros;`

### 03-d H24 l.183 Lie 2015 "cerca de la mitad" — PARCIAL
Resumen (doi 10.1097/AUD.0000000000000129): en hombres no expuestos (controladores de tráfico), muesca de Coles 53 %, índice de muesca 51 %, muesca de 4 kHz 21 %.
Actual: `cerca de la mitad de los no expuestos tenía una (Lie y cols., 2015; → cap. 6).`
Nuevo: `cerca de la mitad de los hombres no expuestos tenía una muesca según la definición de Coles o el índice de muesca (53 y 51 %; con la muesca de 4 kHz, 21 %) (Lie y cols., 2015; → cap. 6).`

### 03-e (discutible) H24 l.489-503, HML/SNR no explicado — NO ES ERROR (omisión; fuera del alcance de esta verificación)

## Agente 04 (H01-H03)

### 04-1 H03 l.434 Luis no es el paciente de la radiografía — CONFIRMADO
`ilustraciones/hacer_h03_radiografia.py`: "No es de un paciente"; su mixto es el OD, el de Luis (demo 41) es el OI. (El comentario de H03.py l.23 también lo dice mal.)
Actual: `El OI de Luis, el paciente de la radiografía del comienzo (caso H3.1), es el ejemplo de mixta:`
Nuevo: `El OI de Luis (caso H3.1) es el ejemplo de mixta:`
Y en H03.py l.23 el comentario: `# Luis va primero en el texto (caso H3.1); el audiograma con LDL es el de la radiografía, que no es de ningún paciente` (esto no lo edito yo).

### 04-2 H03 l.134 Watson y Gengel, "se completa en 30-70 y 125-175 ms" — CONFIRMADO
Katz cap. 3 (Schlauch y Nelson, p. 37; texto línea ~2764): "tonal durations between roughly 200 ms and 1 second or more yield nearly identical thresholds (Watson and Gengel, 1969) ... durations less than 200 ms result in higher thresholds ... nominal pulse duration of 225 ms". Las cifras de 30-70/125-175 ms (no verificadas en el original, resumen no disponible) serían constantes de tiempo, no el momento en que la suma se completa.
Actual: `Esa suma se completa en unos 30 a 70 ms en los agudos y en 125 a 175 ms en los graves (Watson y Gengel, 1969). Un tono de 1 a 2 s la supera con holgura,`
Nuevo: `Con duraciones de unos 200 ms a 1 s o más el umbral casi no cambia; bajo 200 ms sube (Watson y Gengel, 1969, según Schlauch y Nelson, 2015). Un tono de 1 a 2 s la supera con holgura,`
(Schlauch y Nelson 2015 ya está en la lista, l.652.)

### 04-3 H03 l.458 "por un decibel" — CONFIRMADO (menor)
Cuenta: 36,25 y 41,25 → entre ambos hay 5 dB; lo que pasa por 1,25 dB es el corte de 40.
Actual: `Dos oídos casi iguales quedan en grados distintos por un decibel.`
Nuevo: `Dos oídos casi iguales quedan en grados distintos porque el OI pasa por poco (1 dB) el corte de 40 dB.`

### 04-4 H03 l.226-228 instrucción al paciente — CONFIRMADO
BSA 2018 §6.1 (l.100-105 del texto): "Keep it pressed for as long as you hear the sound (tone), no matter which ear you hear it in. Release the button as soon as you no longer hear the sound". (Está en la instrucción de aérea y se repite para ósea.) El propio H03 l.547 evalúa "responde mientras suena".
Actual: `Cada vez que escuches uno, aunque sea apenas, aprieta el botón (o levanta la mano) altiro."`
Nuevo: `Cada vez que escuches uno, aunque sea apenas, aprieta el botón altiro y mantenlo apretado mientras lo oigas; suéltalo apenas deje de sonar. No importa en qué oído lo escuches."`
Y l.228, añadir al final: ` Y soltar el botón cuando el tono se va es lo que permite saber si el paciente responde al tono o a la pausa (BSA, 2018).`

### 04-5 H03 l.115 ISO 389-7 para el cero de los fonos — PARCIAL
ISO 389-7 es campo libre y difuso (el título de la propia referencia l.625 lo dice). El rango 18-25 años solo estaba confirmado en la edición 1996 de 389-7.
Actual: `entre 18 y 25 años (ISO 389-7, 2019).`
Nuevo: `entre 18 y 25 años (ISO 389-7, 2019, en campo libre; para los fonos, ISO 389-1, 2017).`

### 04-6 H03 l.585 fatiga a los 20 minutos — PARCIAL
BSA 2018 §5.2 (l.93-96): "Care should be taken not to fatigue the subject as this can affect the reliability of the test results. If the test time exceeds 20 minutes, subjects may benefit from a short break". ISO 8253-1 no pude abrirla.
Actual: `La fiabilidad cae después de unos 20 minutos sin pausa (ISO 8253-1, 2010).`
Nuevo: `El cansancio afecta la fiabilidad: si el examen pasa de 20 minutos, conviene una pausa breve (BSA, 2018).`

### 04-7 H02 l.140 tabla "Según la BSA (2022)" — PARCIAL
BSA 2022 (texto extraído): ejemplos 1-5, y la nota "with longstanding SNHL in one ear, the Weber response can be central": esa nota SÍ es de BSA. La fila "Mixta" no está en BSA (solo menciona lo mixto como causa del Rinne falso negativo, ejemplo 5).
Actual: `Según la BSA (2022). Con una sensorioneural de larga data en un oído, el Weber puede salir centrado.`
Nuevo: `Según la BSA (2022). Con una sensorioneural de larga data en un oído, el Weber puede salir centrado. La fila de la pérdida mixta es una deducción de este libro.`

### 04-8 a 13 (discutibles: pulsado, VO 250 Hz, familiarización, repetir 1 kHz, VO al final, asimetría 15 dB)
No son errores; verifiqué los dos de BSA: pulsado "not advised" (BSA l.209-210) y 20 min (l.95), coherentes con lo que el agente informó. El libro cita a Katz en el pulsado; conviene decir las dos posturas (decisión del autor). Sin propuesta de reemplazo.

## Conteo por veredicto (24 hallazgos evaluados)
- CONFIRMADO: 12 (01-b, 01-c, 01-e, 02-a, 02-c, 02-d, 02-f, 03-a, 04-1, 04-2, 04-3, 04-4)
- PARCIAL: 9 (01-f, 02-b, 02-e, 02-g, 03-c, 03-d, 04-5, 04-6, 04-7)
- FALSO: 4 (01-a, 01-d, 01-g, 01-h)
- NO VERIFICABLE: 2 (02-h, 03-b)
- YA CORREGIDO: 0
Fuera del conteo: 03-e y 04-8 a 04-13 (omisión o discrepancia entre guías, no error).
