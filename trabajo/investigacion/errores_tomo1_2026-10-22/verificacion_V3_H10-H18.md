# Verificación V3: hallazgos IMPRECISO de H10 a H18 (2026-10-22)

Verificador V3. Se contrastó el texto actual de cada capítulo con la fuente primaria. No se editó nada en capitulos/, casos/, figuras/ ni labsim/. Los 4 graves ya corregidos no se revisaron.

Fuentes usadas (todas leídas por mí, no copiadas de los informes):
- Katz, *Handbook of Clinical Audiology* 7.ª ed. (pdftotext). Página impresa = página del PDF menos 18.
- Rosa y cols. 2014 (CoDAS 26:117-21), texto completo con las 4 tablas, vía doi.org (había un grupo de 6 meses que los agentes no vieron).
- Rosengren y cols. 2019 (PMC6430081), Li y cols. 2015 (PMC4514573), Welgampola y Colebatch 2001 (PMID 11682335 y 11698798), Strupp 2017 (PMC9249284), Strupp 2022 (PMC9661346), Blakley y Chan 2015 (PMC4501377), Kattah 2009 (PMID 19762709), Olsen 1976 (PMID 1275814), Matas 2009 (SciELO).
- BSA 2022/2023 ASSR (OD104-115), descargada y leída. AAA 2010 (CAPD), leída.
- Atlas de pruebas vestibulares (Pérez Fernández, SEORL-PCF, 2009), Manual de Consulta Examen Vestibular, Manual de Otoneurología vestibular (PDF con texto).

Convención: el "texto actual" está copiado tal cual del capítulo. "Error de LabSim" = dato del simulador fuera de lo que dice la literatura; se propone ajustar el texto, no el caso.

---

## H10 y H11 (agente 07)

### 07-1 H10 l.425 y l.538: caso Sofía, la V a 81,1/s. **CONFIRMADO**
- La figura `h10_mujer_joven_abr_2.svg` (la vi renderizada) marca solo I y III en el OI; no hay V a 7,37 ms. El pie dice "no se distingue" y el informe da "7,37 (+1,30)". Se contradicen. **Error de LabSim**: la tabla de latencias da una V que la curva no dibuja.
- Fuente: la desaparición de la V con la tasa alta es en sí un hallazgo retrococlear (Musiek y cols., en Katz, p. 235: "a greater than expected latency increase or a disappearance of Wave V during the high rep rate recording"). Ya está en las referencias de H10.
- Corrección (el pie queda igual; se ajusta el informe):
  - Tabla, l.538: `| V a 81,1 estímulos/s | 6,10 (+0,57) | 7,37 (+1,30) ↑ | |` → `| V a 81,1 estímulos/s | 6,10 (+0,57) | no se distingue ↑ | |`
  - Interpretación: `Lo apoyan la diferencia interaural de la onda V (0,54 ms) y el alargamiento de la V con la tasa alta (1,30 ms en el OI frente a 0,57 en el OD).` → `Lo apoyan la diferencia interaural de la onda V (0,54 ms) y la pérdida de la V con la tasa alta en el OI (en el OD la V solo se alarga 0,57 ms; Musiek y cols., 2015).`

### 07-2 H10 l.285 y l.498: Álvaro (12 semanas) contra la fila del recién nacido. **PARCIAL**
- Rosa y cols. (2014) tiene cuatro grupos de 20 niños (40 oídos): 35-36 sem, 37-38 sem, 39-40 sem y **6 meses**. Medias de la V: 7,14 / 7,05 / 6,90 / **6,50** (DE 0,27; límite 7,04). I-V del grupo de 6 meses: 4,81 (DE 0,26; límite 5,33).
- No existe un grupo de 12 semanas. Álvaro (V 6,97; I-V 5,24 y 5,10) cae dentro del límite de los dos grupos, pero "latencias de recién nacido" no es exacto: tiene 3 meses, y su V está 0,47 ms sobre la media de 6 meses. Es válido usar la fila del término como aproximación; no lo es decir que son "de recién nacido".
- Corrección l.285:
  - `Son latencias de recién nacido: la V llega 1,4 ms más tarde que en Sofía y está dentro de su fila (hasta 7,56; Rosa y cols., 2014).` → `Son latencias de lactante pequeño: la V llega 1,4 ms más tarde que en Sofía. Queda bajo el límite del recién nacido de término (7,56) y bajo el de los 6 meses (7,04; Rosa y cols., 2014).`
- Corrección l.498:
  - `**Referencia**: recién nacido de término, 39 a 40 semanas (Rosa y cols., 2014): media / límite (media + 2 DE).` → `**Referencia**: recién nacido de término, 39 a 40 semanas (Rosa y cols., 2014): media / límite (media + 2 DE). Ese estudio no tiene un grupo de 12 semanas; el de 6 meses tiene la V en 6,50 (límite 7,04) y el I-V en 4,81 (límite 5,33).`

### 07-3 H10 l.506: límite III-V del recién nacido 3,64 ("errata"). **FALSO**
- El 3,64 es fiel a la fuente: Rosa y cols. 2014, tabla 3 (39-40 semanas): III-V media 2,42, mediana 2,30, **DE 0,61, máximo 5,88**. 2,42 + 2 × 0,61 = 3,64. La DE es grande porque la serie trae un valor atípico (5,88), no por un error del libro. La media (2,42) y las DE de I-III (0,21) e I-V (0,31) también coinciden con la tabla.
- Opcional (no es error): agregar bajo la tabla "El límite del III-V es muy amplio porque la serie tiene un valor atípico de 5,88 ms (Rosa y cols., 2014); la mediana es 2,30."

### 07-4 H10 l.290, l.491, l.495: ventana y niveles del burst de 1 kHz. **CONFIRMADO**
- La figura `h10_lactante_abr_2.svg` tiene eje de 0 a 20 ms y tres niveles (40, 20 y 10 dB). El texto dice 12 ms y "40 y 20". H10 l.188 y l.261 ya dicen que con burst en lactantes va 20 a 25 ms, y H11 usa 20 ms con burst.
- **Error de LabSim** adicional: en esa figura el OI trae una V marcada a 10 dB (~11 ms) sobre un trazo que no la sostiene; el OD no tiene nada a 10 dB. El texto dice que 20 dB es el nivel más bajo con respuesta; se mantiene el texto.
- Correcciones:
  - l.290: `cerca del borde de la ventana de 12 ms.` → `en una ventana de 20 ms; con una de 12 ms habría quedado pegada al borde.`
  - l.491: `filtros de 100 a 3.000 Hz, ventana de 12 ms,` → `filtros de 100 a 3.000 Hz, ventana de 12 ms (20 ms para el burst de 1 kHz de Álvaro),`
  - l.495: `tone burst de 1 kHz a 40 y 20, y de 4 kHz` → `tone burst de 1 kHz a 40, 20 y 10 (sin respuesta a 10), y de 4 kHz`

### 07-5 H10 l.416: "una pérdida periférica alarga las latencias absolutas". **CONFIRMADO**
- Contradice la fila "Coclear: casi normales a intensidad alta" de la tabla de arriba. Katz (Musiek, p. 244-245 en el PDF 262-263): una pérdida coclear de agudos puede retrasar la V, "especially if the hearing loss in the 4-kHz region falls within the moderate to moderately severe range"; además el efecto varía mucho entre pacientes.
- Corrección: `Una pérdida periférica (conductiva o coclear) alarga las latencias absolutas y deja normales los interpicos.` → `Una pérdida conductiva alarga todas las latencias. Una coclear de agudos puede atrasar la V cuando el 4 kHz está entre moderado y moderadamente severo, pero deja normales los interpicos (Musiek y cols., 2015). En las dos, los interpicos normales son el dato que separa lo periférico de lo retrococlear.`
  (la frase siguiente, "Ese es el dato que separa lo periférico de lo retrococlear.", se elimina para no repetirla).

### 07-6 H11 l.116, l.168, l.315: "la razón sale chica aunque haya hidrops". **PARCIAL**
- Lo de la **pérdida marcada** sí está en Katz (Santarelli y Arslan, p. 218): "the SP enhancement induced by the endolymphatic hydrops may be masked by the amplitude reduction resulting from hair cell loss particularly in the presence of a high degree of hearing impairment". El agente 07 dijo que no estaba: se equivocó.
- Lo del **nivel bajo** no está en ninguna fuente que pude leer. Katz solo dice que la mayoría de las series usan clicks de 90 dB nHL (p. 218), y que el SP crece de forma no lineal con el nivel (fig. 12.6). Se puede decir que no hay un corte validado a nivel bajo; no que "la razón sale chica".
- Correcciones:
  - l.116: `a 90 dB nHL el nivel sobre el umbral es poco y la razón sale chica, aunque haya hidrops (ver "Errores frecuentes").` → `la pérdida de células ciliadas atenúa el PS y puede enmascarar el hidrops: la razón sale chica aunque lo haya (Santarelli y Arslan, 2015; ver "Errores frecuentes").`
  - l.168: `Una razón medida a nivel bajo sale chica aunque haya hidrops, y el equipo no avisa.` → `Las series publicadas usan clicks de unos 90 dB nHL (Santarelli y Arslan, 2015). A un nivel más bajo no hay un corte validado, y el equipo no avisa.`
  - l.315: `A 60 dB nHL la razón sale chica en un oído con hidrops, y nada lo avisa.` → `A 60 dB nHL no hay un corte validado: una razón normal no descarta hidrops, y nada lo avisa.`
- La referencia de Santarelli y Arslan ya está en H11 (l.358).

### 07-7 H11 l.278-281: razón de áreas 1,94 aplicada a los tres electrodos. **YA CORREGIDO**
- El texto de l.281 ya dice que el 1,94 viene de electrodo timpánico (Devaiah 2003), que con aguja en promontorio no mejoró (Baba 2009) y que el libro aplica el mismo límite a los tres electrodos. Katz (p. 219) solo trata el índice de áreas de pasada. No hay nada que corregir.

---

## H12 y H13 (agente 08)

### 08-1 H12 l.286, 437-446, 459-471: amplitudes corregidas de los casos. **CONFIRMADO (error de LabSim)**
- Rehice la cuenta (amplitud pico a pico / corregida) con los siete valores de cVEMP de los casos: Tomás 295/5,68 = 51,9 µV; 287/5,63 = 51,0; Patricia 350/6,79 = 51,5 y 33/0,66 = 50,0; Carolina 109/2,15 = 50,7 y 340/6,81 = 49,9; Matías 19/0,38 = 50,0 y 290/5,75 = 50,4. El EMG de LabSim es ~50 µV en todos.
- Rosengren y cols. 2019: mínimo ~80 µV de EMG rectificado; su ejemplo da una razón de 2,5 (201/80). Li y cols. 2015 (n = 250): 1,25 (DE 0,72). Los casos (5,6 a 6,8) están 6 DE sobre la media de Li; la razón de asimetría sí es válida.
- Corrección en el pie de Tomás (`h12_p33 vemp`): después de `En estas figuras la contracción es la misma en los dos lados, así que la amplitud cruda y la corregida dicen lo mismo.` agregar: `El EMG de estas figuras es de unos 50 µV, bajo el mínimo de unos 80 µV (Rosengren y cols., 2019); por eso la corregida sale en 5 o 6 y no en 1 a 3 como en la tabla de referencia. Compara un oído con el otro, no con la tabla.`

### 08-2 H12 l.215, l.330 y figuras de oVEMP: "corregida por EMG". **CONFIRMADO (error de LabSim)**
- Las figuras `h12_p33_vemp_2` y `h12_p38_vemp_2` rotulan "Corregida por EMG" y "Razón de asimetría (amplitud corregida)". Patricia: 24/0,57 = 42 µV y 24/0,55 = 44 µV. La tabla del capítulo (l.215) dice que en el oVEMP el EMG "No se mide".
- Corrección en el pie de Patricia: `El oVEMP de Patricia: **24 µV**, **0,57** corregidos en un oído...` → `El oVEMP de Patricia: **24 µV** en un oído (LabSim calcula además una amplitud "corregida", 0,57, que para el oVEMP no se mide en la práctica)...` y la segunda línea `...y **24 µV**, **0,55** en el otro.` → `...y **24 µV** (0,55) en el otro.`

### 08-3 H12 l.130: 13,5 dB es para TDH49, el libro usa inserción. **PARCIAL**
- Rosengren 2019 lo dice literal para TDH49 a 500 Hz. Katz cap. 2 (Wilber y Burkard, fig. 2.2, p. 18, ANSI S3.6-1996): TDH-49 a 500 Hz = 13,5 dB SPL; **ER-3A = 6,0 dB** (acoplador HA-1). Con inserción se suman unos 6 dB, no 13,5.
- Corrección: `Con la norma ANSI, para un tono de 500 Hz y fonos TDH49, se suman 13,5 dB al valor en HL para llegar al SPL equivalente (Rosengren y cols., 2019).` → `Con la norma ANSI, para un tono de 500 Hz se suman 13,5 dB al valor en HL con fonos TDH49 (Rosengren y cols., 2019) y unos 6 dB con fonos de inserción ER-3A, que son los de este libro (Wilber y Burkard, 2015), para llegar al SPL equivalente.`
- Referencia nueva: `Wilber LA, Burkard R. Calibration. En: Katz J, Chasin M, English K, Hood LJ, Tillery KL, editores. Handbook of clinical audiology. 7th ed. Philadelphia: Wolters Kluwer; 2015. p. 9-34.` (**verificar las páginas finales del capítulo antes de imprimir**: el inicio, p. 9, sí está en el índice de Katz; el cierre no lo comprobé).

### 08-4 H12 l.392: Welgampola y Colebatch (2001) "con clics". **PARCIAL**
- El **dato está bien**; la **referencia está mal**. Los 35 % (corregida) y 46 % (cruda) vienen de "Vestibulocollic reflexes: normal values and the effect of age" (Clin Neurophysiol 2001;112:1971-9, PMID 11682335): clics a 100 dB nHL, 70 adultos de 25 a 85 años, valores para menores de 60 años. Es lo que cita Rosengren 2019. La referencia de H12 l.518 es otro artículo (tone burst, Otol Neurotol 2001, PMID 11698798), que da el umbral de 114,4 dB SPL y no el 35 %.
- Corrección en las referencias (l.518; ese artículo no se cita en otra parte de H12): `Welgampola MS, Colebatch JG. Characteristics of tone burst-evoked myogenic potentials in the sternocleidomastoid muscles. Otol Neurotol. 2001;22(6):796-802. doi:10.1097/00129492-200111000-00014` → `Welgampola MS, Colebatch JG. Vestibulocollic reflexes: normal values and the effect of age. Clin Neurophysiol. 2001;112(11):1971-9. doi:10.1016/s1388-2457(01)00645-9`
- El texto de l.392 queda como está.

### 08-5 H12 l.397: "5 a 15 % de los mayores de 60 años no tiene cVEMP". **CONFIRMADO**
- Rosengren 2019: 5 a 15 % en mayores de 60, "it can be higher" según la edad y el método. Li y cols. 2015 (BLSA, edad media 72,6; rango 26-92): de 244 sujetos, cVEMP aéreo ausente en **ambos oídos 26 %** (64) y en uno 22 % (54); con algún cVEMP ausente: 29 % bajo 70 años, 45 % a los 70-79 y **69 % desde los 80**. oVEMP por golpe en Fz ausente en ambos: 17 %.
- Corrección: `y entre el 5 y el 15 % de las personas mayores de 60 años no tiene cVEMP aéreo;` → `y entre el 5 y el 15 % de las personas mayores de 60 años no tiene cVEMP aéreo (Rosengren y cols., 2019); en una cohorte de 73 años de media faltó en los dos oídos en el 26 % y en alguno en el 69 % de los mayores de 80 (Li y cols., 2015);`

### 08-6 H12 l.215 / l.311: banda de EMG de 30 a 150 µV. **YA CORREGIDO**
- Ya está dicho como decisión del autor (comentario l.220) y con el mínimo de 80 µV de Rosengren (l.311). La consecuencia en los casos se trata en 08-1.

### 08-7 H13 l.226: conducto pequeño sube el fono "hasta 10 a 20 dB". **PARCIAL**
- BSA 2023, sec. 5.2: "10-20 dB higher", "greatest at high frequencies"; y apéndice de exactitud: +24 dB en 4 kHz y menos de 10 dB en graves (Sininger y cols. 1997). El texto no está mal; falta la dependencia de la frecuencia.
- Corrección: `(que sube el nivel real del fono hasta 10 a 20 dB)` → `(que sube el nivel real del fono entre 10 y 20 dB, más en agudos: unos 24 dB en 4.000 Hz y menos de 10 dB en graves)`

### 08-8 H13 l.290: artefacto con el vibrador desde ~40 dB nHL. **CONFIRMADO**
- BSA 2023, sec. 7.4: "air conduction tests above 100 dB nHL or bone conduction tests above 40 dB nHL". Además, nota de la tabla de umbrales: "ASSR BC testing at 500 Hz is not recommended because there is an unacceptably high risk of the BC stimulus artefact being erroneously detected as a physiological response". Eso resuelve la pregunta 7 del capítulo (vía ósea, 500 Hz, 40 dB).
- Corrección: `a más de 100 dB nHL por vía aérea las respuestas pueden ser vestibulares o del estímulo (BSA, 2023).` → `a más de 100 dB nHL por vía aérea las respuestas pueden ser vestibulares o del estímulo; por vía ósea el artefacto del vibrador puede aparecer desde unos 40 dB nHL, y en 500 Hz la BSA no recomienda el ASSR óseo (BSA, 2023).`

### 08-9 H13 l.336: el control con estímulo bloqueado. **PARCIAL**
- BSA 7.4: "If response is still present, then it is artefactual" (el texto está bien). BSA, preguntas frecuentes (P9): el bloqueo "would stop both a cochlear and vestibular response so that doesn't help distinguish them". El capítulo no dice lo segundo.
- Corrección: `Si la respuesta persiste, es artefacto (BSA, 2023).` → `Si la respuesta persiste, es artefacto. Si desaparece, no queda descartada una respuesta vestibular sobre 100 dB nHL: el bloqueo corta la respuesta del oído y la vestibular por igual (BSA, 2023).`

### 08-10 H13 l.210 vs l.331: "ABR antes que ASSR" y Rance 1998. **PARCIAL**
- BSA 2.5: "An ABR (either threshold or suprathreshold) must be carried out prior to ASSR testing". El texto de l.210 es fiel. Rance 1998 (niños sin ABR a click máximo) es evidencia de que el ASSR a nivel alto detecta restos, pero la BSA igual exige el ABR primero. El lector ve dos reglas.
- Corrección l.331: `los modulados pueden mostrar que hay resto auditivo (Rance y cols., 1998).` → `los modulados pueden mostrar que hay resto auditivo (Rance y cols., 1998). Aun así, la BSA (2023) exige un ABR antes del ASSR; el ASSR de nivel alto es un complemento, no un reemplazo.`

### 08-11 H13 l.20: candidatos a implante coclear. **PARCIAL**
- BSA 2.5 lo lista ("alternative to ABR") pero remite a las limitaciones del nivel alto (sec. 7.7) y en P9 dice: "For cochlear implant candidate assessment, use ABR in young children and CAEP in older children and adults".
- Corrección: `- **Candidatos a implante coclear**, como alternativa al ABR para estimar cuánta audición residual queda.` → `- **Candidatos a implante coclear**, como alternativa al ABR para estimar cuánta audición residual queda, con cautela: a nivel alto aumentan los artefactos, y la BSA (2023) prefiere ABR en niños pequeños y CAEP en mayores.`

---

## H14 y H15 (agente 09)

### 09-1 H15 l.391: el criterio de "2 DE". **CONFIRMADO**
- AAA 2010, "Interpretation of (C)APD Test Results": "a score two standard deviations or more below the mean for at least one ear on at least two different behavioral central auditory tests" (también recomendado por ASHA 2005).
- Corrección: `se toma como anormal un rendimiento a unas **2 desviaciones estándar bajo la media** de la norma, para equilibrar sensibilidad y especificidad (AAA, 2010).` → `se toma como anormal un rendimiento a **2 desviaciones estándar o más bajo la media** de la norma, en al menos un oído y en al menos dos pruebas centrales distintas, para equilibrar sensibilidad y especificidad (AAA, 2010).`

### 09-2 H15 l.115 y referencia: Cranford 1990 "citado en AAA". **CONFIRMADO**
- La AAA cita "Cranford, Boose & Moore (1990). Effects of aging on the precedence effect in sound localization. J Speech Hear Res 33(4):654-659". La referencia del libro (l.490) es otro artículo del mismo grupo y año (Ear Hear 1990;11:282-8, esclerosis múltiple). Ese sí respalda la frase.
- Corrección: `(Cranford y cols., 1990, citado en AAA, 2010)` → `(Cranford y cols., 1990, en esclerosis múltiple; la AAA, 2010, cita otro trabajo del mismo grupo y año)`

### 09-3 H15 l.107: MLD "bajo la corteza". **PARCIAL**
- Olsen y cols. 1976 (resumen): MLD no afectado por lesiones corticales; "very often abnormally small" en tumor del VIII par, Ménière y esclerosis múltiple; poco confiable con pérdida auditiva o diferencias interaurales de umbral. El texto es correcto, pero "lesiones bajo la corteza" omite que el MLD también baja con lesión retrococlear y de laberinto. La advertencia sobre la pérdida asimétrica ya está al final de l.107.
- Corrección: `como la esclerosis múltiple, y no se altera en las lesiones corticales (Olsen y cols., 1976)` → `como la esclerosis múltiple, y también con un tumor del VIII par o un Ménière; no se altera en las lesiones corticales (Olsen y cols., 1976)`

### 09-4 H14 l.26: indicaciones de la electrofisiología según la AAA. **CONFIRMADO**
- AAA 2010 lista cinco: conducta incompleta o contaminada, niño muy pequeño, sospecha neurológica, ubicar el sitio, y "behavioral measures of (C)APD are not available in the individual's native language". Falta la última.
- Corrección: `para cuando se sospecha una enfermedad neurológica y para cuando hace falta ubicar el sitio de la disfunción.` → `para cuando se sospecha una enfermedad neurológica, para cuando hace falta ubicar el sitio de la disfunción y para cuando no hay pruebas conductuales en el idioma del paciente.`

### 09-5 H14 l.119: reflejo postauricular "entre 14 y 19 ms". **FALSO**
- Matas y cols. 2009 (SciELO, leído): el reflejo postauricular "happens between 14 and 19 ms after the acoustic stimulus", y su media con electrodo en mastoides fue ~14 ms. El libro es fiel a su cita. Katz (p. 319, tabla 17.1, de Picton 1974) da otros valores (negativo 11,8 ± 0,8 y positivo 16,4 ± 0,7 ms): diferencia entre fuentes, no error. No se cambia.

---

## H16, H17 y H18 (agente 10)

### 10-1 H17 l.206 y l.203: límites de 25/30 % sin exigir suma de VFL. **CONFIRMADO**
- Atlas de pruebas vestibulares (Pérez Fernández, 2009, cap. 7, PDF p. 60): paresia > 20 %, preponderancia > 28 %, "siempre que la suma total de la VFL máxima en todas las exploraciones sea igual o superior a 15°/s". El capítulo solo trata la suma baja en la arreflexia (< 6 °/s, criterio de Strupp 2017, verificado).
- Corrección l.206, al final del primer párrafo, después de `Cada centro debería fijar los suyos con sus propios sanos.` agregar: `Los porcentajes solo valen con respuestas suficientes: el Atlas (Pérez Fernández, 2009) los acepta si la suma de las VFL máximas es de al menos 15 °/s; con menos, se describe una hipofunción bilateral y no una asimetría.`
- Referencia nueva (formato de la lista): `Pérez Fernández N, editor. Atlas de pruebas vestibulares para especialistas en otorrinolaringología. Barcelona: SEORL-PCF; 2009. Cap. 7.` (El año 2009 sale del depósito legal del PDF; verificar con el original impreso).
- Las discrepancias de límites con los manuales chilenos (15 %: Manual de Consulta, líneas 1123-1134; Manual de Otoneurología, líneas 857-868) también están confirmadas; el capítulo ya dice que no hay un límite único.

### 10-2 H17 l.163: calórica del canal posterior (15 s) enseñada y a la vez sin respaldo. **PARCIAL**
- La inconsistencia es real, pero el capítulo ya la reconoce en l.166 ("no tiene respaldo en la literatura revisada... se informa como dato complementario"). Basta ordenar el mensaje en el pasaje donde se enseña.
- Corrección: `Una diferencia de duración de **15 segundos o más** entre los dos oídos se toma como una hipofunción del lado más corto.` → `Una diferencia de duración de **15 segundos o más** entre los dos oídos es el criterio del protocolo para hablar de hipofunción del lado más corto; no tiene respaldo en la literatura y se informa solo como dato complementario (ver más abajo).`

### 10-3 H16 l.191: "muestreo típico de 30 a 60 Hz" en VNG. **FALSO**
- Blakley y Chan 2015 (PMC4501377, tabla de métodos): "Video sampling rates are usually 30–60 Hz. Sampling rates of 100 Hz requires specialized equipment"; "most commercial units sample calorics at 30 Hz"; en su estudio 30 Hz (EOG) y 60 Hz (VOG). El libro es fiel a la fuente que cita. H18 ya explica que el vHIT usa cámaras más rápidas. Opcional: `muestreo típico de 30 a 60 Hz` → `muestreo típico de 30 a 60 Hz (el vHIT usa cámaras más rápidas, → H18)`.

### 10-4 H16 l.433 y l.453: HINTS sin condiciones de uso. **PARCIAL**
- Kattah 2009 (resumen): pacientes con síndrome vestibular agudo (vértigo, **nistagmo**, náuseas, intolerancia al movimiento, marcha inestable) y al menos un factor de riesgo vascular; 101 pacientes, sensibilidad 100 %, especificidad 96 %. Sin nistagmo no se aplica. El "plus" (hipoacusia unilateral aguda nueva) se propuso para el infarto de la AICA, donde HINTS es menos sensible; la revisión sistemática (Anburajan y cols., 2026, PMID 41665728; HINTS 92,7 % de sensibilidad, 91,1 % de especificidad; con hipoacusia 95,7 % y 80,7 %) lo respalda.
- Corrección l.433: `Entre los pacientes con vértigo agudo continuo y un factor de riesgo vascular,` → `Entre los pacientes con vértigo agudo continuo, nistagmo y un factor de riesgo vascular,` y al final de la viñeta agregar: `Sin nistagmo no se aplica. Una hipoacusia nueva en el mismo lado se suma como un cuarto signo central ("HINTS plus"), porque el infarto de la arteria cerebelosa anteroinferior puede dar un impulso normal.` → es un dato de la revisión de Anburajan y cols. (2026); si se agrega, incluir: `Anburajan G, Kattah J, Wang Z, Mantokoudis G, Newman-Toker DE, Tarnutzer AA. HINTS+ to diagnose AICA stroke: systematic review of the diagnostic impact of acute unilateral hearing loss in the acute vestibular syndrome. J Neurol. 2026;273:131. doi:10.1007/s00415-026-13641-3` (revista y volumen tomados de la ficha de Europe PMC; confirmar).

### 10-5 H18 l.95: contraindicaciones sin patología cervical. **PARCIAL**
- No encontré una fuente específica de vHIT. Respaldo indirecto: el Atlas (cap. 1, PDF p. 14): "las limitaciones para la movilización cervical deben ser valoradas antes de comenzar el estudio, con el objeto de evitar ciertas maniobras" (nistagmo de agitación cefálica y Dix-Hallpike). Es criterio clínico razonable para un giro brusco.
- Corrección: `fractura de nariz o traumatismo de cara, cabeza o cuello, cirugía ocular reciente,` → `fractura de nariz o traumatismo de cara, cabeza o cuello, patología cervical que limite o haga peligroso el giro (inestabilidad, estenosis, dolor intenso, cirugía de columna reciente), cirugía ocular reciente,`

---

## Otros puntos de los informes que comprobé

- **Rosengren 2019, asimetría 6,7 % (H12 l.390). FALSO como error del libro.** 109/46 = 2,370 y 320/156 = 2,051 dan 7,2 %, pero las cifras de la fuente están redondeadas; el 6,7 % es el que publica Rosengren. El libro copia la fuente. No cambiar.
- **Strupp 2017, "fe de erratas" de la silla (agente 10). NO VERIFICABLE.** La versión de PMC (PMC9249284) trae: ganancia < 0,1, avance de fase > 68° (constante de tiempo < 5 s), suma calórica < 6 °/s, 53 % de respuestas anormales en la silla y "menos de ~1000 °/s²". Eso coincide con H17 l.83 y l.87. No encontré los números "≤ 0,1, ≥ 15°, ≤ 6 s" que cita el agente. Se buscó en el texto completo; no pude abrir la fe de erratas (DOI 10.3233/VES-229002). H17 no cita esas cifras: el cap. 24 es el que debe contrastarse.
- **Strupp 2022 vHIT "bajo 0,7 o diferencia > 0,3" (H18 l.228). Comprobado, sin error.** Texto completo (PMC9661346): "reduction of gain < 0.7 for vHIT and or a side difference of > 0.3 and/or a caloric side difference of > 25 %"; ganancia > 0,8 suele darse como normal.
- **Sininger 2018 "hasta 14 dB más bajo" (H13 l.313). Comprobado, sin error.** Umbrales corregidos del ASSR menores que los del ABR: 14,39 dB (500 Hz), 10,12 (1 kHz), 3,73 (2 kHz). La BSA lee la misma figura en dB nHL sin corregir como "equivalente"; las dos posturas ya están en el capítulo.
- Los DISCUTIBLE de los cuatro informes no se revisaron salvo los dos anteriores (fuera del encargo).

---

## Conteo por veredicto (28 hallazgos IMPRECISO)

| Veredicto | N | Ids |
|---|---|---|
| CONFIRMADO | 11 | 07-1, 07-4, 07-5, 08-1, 08-2, 08-5, 08-8, 09-1, 09-2, 09-4, 10-1 |
| PARCIAL | 12 | 07-2, 07-6, 08-3, 08-4, 08-7, 08-9, 08-10, 08-11, 09-3, 10-2, 10-4, 10-5 |
| FALSO | 3 | 07-3, 09-5, 10-3 |
| YA CORREGIDO | 2 | 07-7, 08-6 |
| NO VERIFICABLE | 0 | |

Fuera de la lista: 1 FALSO (Rosengren 6,7 %), 1 NO VERIFICABLE (erratum de Strupp 2017), 2 observaciones comprobadas sin error (Strupp 2022, Sininger 2018).

Errores de LabSim (se ajusta el texto): 07-1 (V a 81,1/s en el OI de Sofía), 07-4 (V marcada a 10 dB en el OI de Álvaro), 08-1 (EMG ~50 µV en todos los casos de H12), 08-2 (amplitud corregida en el oVEMP).
