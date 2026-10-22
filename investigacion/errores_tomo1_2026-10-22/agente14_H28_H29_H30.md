# Agente 14: revisión de H28 (olfatometría), H29 (prick test) y H30 (espirometría)

Los tres `.py` (`H28`, `H29`, `H30`) tienen `CASOS = []`: no hay casos que cotejar con el texto.
Los capítulos están en general muy bien: casi todas las cifras citadas coinciden con la fuente primaria. Los hallazgos son pocos y en su mayoría de gravedad baja.

## Hallazgos (ordenados por gravedad)

### GRAVE

- **[GRAVE] H30-espirometria.md l.411 (informe de ejemplo)**
  - Texto: "patrón obstructivo (VEF1/CVF 0,59 …) … **La CVF está sobre el LIN.**"
  - Correcto: en la tabla del propio ejemplo (l.403) la CVF previa es 3,30 L, el LIN es 3,44 L y el z-score es −1,88. Eso es **bajo** el LIN (z < −1,645). Solo después del broncodilatador sube sobre el LIN (3,60 L, z −1,39).
  - Con razón bajo el LIN y CVF bajo el LIN, la tabla de patrones del mismo capítulo (l.315-322) da **mixto** (obstrucción y posible restricción, a confirmar con TLC), no "obstructivo puro". El informe de ejemplo enseña una lectura contraria a su propia tabla.
  - Cálculo: rehecho con GLI-2012 (paquete `pyspiro`, hombre de 55 años, 172 cm, caucásico). Previstos: CVF 4,455 L, VEF1 3,501 L, razón 0,787. LIN: CVF 3,442 L, VEF1 2,690 L, razón 0,672. z pre: CVF −1,88, VEF1 −3,05, razón −2,65. z post: −1,39, −2,30, −1,90.
  - Todos los números de la tabla coinciden con GLI-2012; el error es solo la frase de conclusión.
  - Corrección: escribir "la CVF está bajo el LIN antes del broncodilatador (z −1,88) y sobre el LIN después". Cambiar la conclusión a "patrón mixto/obstructivo con CVF baja", o subir la CVF previa del ejemplo (por ejemplo a 3,50 L) para que quede sobre el LIN.

### IMPRECISO

- **[IMPRECISO] H30-espirometria.md l.229 y l.277 (ayuda memoria)**
  - Texto: "si la FVC es menor que 1 L, la diferencia debe ser menor que 0,100 L (Schönffeldt …; Graham …)".
  - Graham 2019 (AJRCCM 200:e70, PMC6794117, texto en el cuerpo y Tabla 7) fija para mayores de 6 años **≤ 0,150 L** para FVC y FEV1, sin excepción por FVC < 1 L. La regla "≤ 0,100 L si FVC ≤ 1 L" era del estándar de 2005 (Miller 2005) y se eliminó. La Tabla 10 de Graham (grado A y B: 0,150 L) lo confirma.
  - Corrección: citar solo el manual chileno para esa excepción (si la trae), o quitarla de la atribución a Graham.

- **[IMPRECISO] H29-prick-test.md l.51 y l.125 (histamina)**
  - Texto: "histamina diclorhidrato al 0,1 % (10 mg/mL)".
  - 0,1 % equivale a 1 mg/mL, no a 10 mg/mL (10 mg/mL = 1 %). La inconsistencia viene de Heinzerling 2013 (Clin Transl Allergy 3:3, PMC3565910): el texto dice "10 mg/ml or 0.1 %" y la Tabla 1 pone "0,1 %".
  - El libro la copia y además usa "10 mg/mL" en la hoja de registro (l.188). Hay que decidir una sola cifra.
  - Corrección: poner "histamina diclorhidrato 10 mg/mL (la guía europea escribe también 0,1 %, que no equivale a esa concentración; se usa la que trae el fabricante)".

- **[IMPRECISO] H28-olfatometria.md l.190 (Pekala 2016)**
  - Texto: "Un metaanálisis de 10 estudios y 639 pacientes encontró una mejoría del TDI de 3,77 puntos".
  - Pekala (PMID 26624966): la revisión sistemática incluyó 10 estudios y 639 pacientes, pero el **metaanálisis fue de solo 3 estudios**. De él salen TDI +3,77 (IC 2,28-5,26), D +1,92, I +1,61, umbral −0,01.
  - Corrección: "una revisión sistemática de 10 estudios (639 pacientes), con metaanálisis de 3 estudios, mostró +3,77 de TDI…".

- **[IMPRECISO] H30-espirometria.md l.129 (Roberts 2018)**
  - Texto: "5 por cada 10.000 pruebas … lo ocasional es la tos y el mareo leve, y lo infrecuente el broncoespasmo…".
  - Roberts (Thorax 73:385; PMID 28663340): 119 incidentes en 186 000 pruebas = 0,6 por 1000, es decir cerca de **6** por 10 000. Los que requirieron ingreso o urgencias fueron cerca de 1 por 10 000. El incidente cardiopulmonar más frecuente fue el **síncope**, que el texto no nombra.
  - Corrección: "cerca de 6 por 10 000 (0,6 por 1000); el más frecuente fue el síncope". Si la cifra "5" viene del manual chileno, anotarlo como tal.

- **[IMPRECISO] H29-prick-test.md l.42 (fase tardía)**
  - Texto: la fase tardía "depende de la llegada de otras células y no de la IgE".
  - La reacción de fase tardía **se inicia por IgE y mastocitos** (el infiltrado celular es posterior). Es una fase tardía de la reacción mediada por IgE, no una reacción independiente de ella.
  - Es una simplificación que puede confundir; la fuente citada (Bernstein) no pudo cotejarse (ver más abajo).
  - Corrección: "la fase tardía la inicia la misma reacción IgE-mastocito y se mantiene por la llegada de otras células; no se usa para leer la prueba".

- **[IMPRECISO] H29-prick-test.md l.90 y l.142 (espalda como alternativa)**
  - Heinzerling 2013 advierte que la piel de la espalda es **más reactiva** que la del antebrazo (pápulas mayores y más positivos).
  - El libro propone "otra zona sana (la espalda)" y la espalda en lactantes sin avisar que los tamaños no son comparables con los del antebrazo ni con el criterio de 3 mm.
  - Corrección: agregar una línea: "la espalda reacciona más; anotar la zona".

### DISCUTIBLE

- **[DISCUTIBLE] H30-espirometria.md l.143-145 y tabla l.153-158 (exactitud ±3 % o ±2,5 %)**
  - Comprobado: Graham 2019 exige ISO 26782 con error máximo permitido **±2,5 %** con la jeringa de 3 L. La verificación diaria sigue en **±3 %** (±2,5 % del espirómetro más ±0,5 % de la jeringa). El texto lo dice bien; el cambio de 2019 está correctamente recogido.
  - Solo conviene aclarar que en la tabla "Precisión ±2,5 %" es el error máximo permitido y no la repetibilidad (que ISO fija en ±3 %). No es un error.

- **[DISCUTIBLE] H30-espirometria.md l.166 (preparación del paciente)**
  - El texto atribuye al manual chileno y a Graham: sin fumar 1 h, sin drogas ni alcohol 8 h, sin ejercicio intenso 1 h. Coincide con la Tabla 5 de Graham 2019. No es error.

## Verificado y correcto (con fuente)

### H28

- **Oleszkiewicz 2019** (PMC6411676, texto completo leído):
  - 9139 sanos, de 5 a 96 años.
  - Cortes: ≤16 anosmia funcional (D=8 e I=8, máximo de 90 % de los anósmicos); 16,25-30,5 hiposmia; 30,75-41,25 normosmia; ≥41,5 supersmellers.
  - Hiposmia = percentil 10 del grupo de 21 a 30 años (30,75). Percentil 10 de 31-40 años = 30,5.
  - Mujeres +1,3 puntos; máximo a los 21-30 años; caída marcada a los 60-71 años.
  - 71-80 años: 60 % hipósmicos con el corte joven; 31-40 años: 10,7 %.
  - Pluma de 14 cm con 4 mL; destapada unos 3 s; tríos cada 20 s; 16 pasos 1:2 desde 4 %; n-butanol o PEA; escalera desde la concentración más baja; dos aciertos o un error marcan un punto de giro; umbral = promedio de los últimos 4 giros.
  - Discriminación: 3 s dentro del trío y 20-30 s entre tríos.
  - Umbral: el que más cae con la edad.
- **Hummel 2007**: percentil 10 de 16-35 años = 30,3 (PMID 17021776).
- **Gudziol 2006**: más de 60 % notó mejoría con +5,5 de TDI (PMID 17003712).
- **Hummel 2001**: ninguno de 112 anósmicos superó 8 puntos (PMID 11642433).
- **Doty 1984** (UPSIT): test-retest a 6 meses r = 0,918; detecta simulación de anosmia (PMID 6463130).
- **Hummel 2009**: 40 entrenados y 16 controles, 12 semanas, dos veces al día, rosa, eucalipto, limón y clavo (PMID 19235739).
- **Doty 2012**: ~90 % de olfato alterado en Parkinson temprano (PMID 22584158).
- **Hannum 2020**: 77 % con pruebas contra 44 % con preguntas (PMID 33245136).
- **Frasnelli y Hummel 2005**: 205 pacientes y 25 controles; parosmia con más molestias (PMID 15133691).
- **Cuentas del capítulo**: ejemplo de umbral (promedio de 5, 4, 5, 4 = 4,5); 4,5 + 10 + 9 = 23,5; 6 + 12 + 11 = 29,0; diferencia 5,5; azar 16/3 ≈ 5 y 16/4 = 4; TDI 1-48. Todas correctas.

### H29

- **Heinzerling 2013** (PMC3565910, texto leído):
  - Lectura a 15-20 min; positivo con pápula ≥3 mm.
  - Histamina con máximo a los 8-10 min; control negativo NaCl 0,9 %.
  - Distancia ≥2 cm entre punciones; antebrazo volar a 2-3 cm de la muñeca y el codo; lanceta sostenida ≥1 s.
  - El sangrado puede dar falsos positivos (esto resuelve el `verificar` de l.214).
  - Asma: "peak flow <70 %" es contraindicación relativa.
  - Esperar 4-6 semanas tras una reacción sistémica; embarazo y betabloqueantes (con IECA "menos a menudo").
  - Tabla de fármacos: antihistamínicos de 1.ª generación >2 días; de 2.ª generación 7 días; ketotifeno >5 días; H2 sin efecto; corticoide tópico en la zona >1 semana; omalizumab >4 semanas; doxepina 7 días y desipramina 3 días; corticoide oral prolongado >10 mg/día >3 semanas.
  - Sin efecto: corticoides nasales e inhalados, antileucotrienos, ciclosporina, teofilina, ISRS, β2. UV-B reduce la pápula.
- **Nevis 2016**: sensibilidad 85 % y especificidad 77 % contra la provocación nasal (7 estudios, 430 pacientes).
- **Sellaturay 2015**: ~31 000 pacientes, 24 reacciones sistémicas (0,077 %), 18 por alimentos y 4 por aeroalérgenos, pápula >8 mm en 75 %, todas tratadas en la consulta.
- **Grossman 1997**: 60-78 % de los asmáticos tienen rinitis (usado en H30 l.40).
- **Adrenalina** (WAO 2020, de memoria; el PMC no se abrió): 0,01 mg/kg, máximo 0,5 mg, muslo anterolateral, repetir cada 5-15 min. Coincide con lo que recuerdo de la guía; no se comprobó en el texto.
- **Conteo de ejemplos**: 3 × 3 mm es positivo (criterio ≥3 mm); lo demás de la hoja de registro es coherente con el informe de ejemplo.

### H30

- **Graham 2019** (PMC6794117, texto completo leído):
  - Criterios de aceptabilidad: BEV <5 % FVC o 0,100 L, el mayor; meseta ≤0,025 L en el último segundo; tiempo espiratorio ≥15 s; FIVC − FVC ≤0,100 L o 5 %.
  - Tablas de aceptabilidad, utilizable y grados A-F (Tablas 7 y 10): la tabla del libro (l.208-220) y la de grados (l.233-243) coinciden **fila por fila**.
  - Terminar la prueba si el FEV1 cae por debajo del 80 % del valor inicial.
  - Tiempos de suspensión de broncodilatadores (SABA 4-6 h, SAMA 12 h, LABA 24 h, ultra-LABA 36 h, LAMA 36-48 h).
  - Contraindicación relativa: cirugía o infección de senos y oído medio, 1 semana. El libro lo contrasta bien con las 4 semanas del manual chileno.
  - Alerta del factor de calibración: ±2 DE o 6 %.
  - Menores de 6 años: ≤0,100 L o 10 %.
- **Cuentas rehechas** (GLI-2012, ver el GRAVE): 13,3 % de respuesta del ejemplo del manual; 11,4 % del ejemplo propio; los z-scores y LIN del ejemplo coinciden con GLI-2012 caucásico. La ecuación "otros" da previstos 6,8 % más bajos en FEV1 y 7,9 % más bajos en FVC (el texto dice ~7 % y ~8 %).
- **Pregunta 5**: (2,28 − 2,00) × 100 / 3,00 = 9,3 %, no significativa con el criterio de 2022. Con 12 % y 200 mL sí lo sería (+14 % y +280 mL). Coherente con el comentario del capítulo.
- **Miller 1990** (bocio): sensibilidad 100 % y especificidad 78 % por curva; FEV1/PEF >8 con sensibilidad 64 % y especificidad 94 %. Coincide con el texto.
- **Severidad por z-score** (leve −1,65 a −2,4; moderada −2,5 a −4; grave < −4): coincide con mi conocimiento del estándar 2022. No se pudo abrir el texto de Stanojevic (ver más abajo).

## Secciones revisadas sin hallazgos

- **H28**:
  - Fundamento (epitelio, transducción, vía, ortonasal/retronasal, trigémino).
  - Pasos 1-6 del paso a paso, tabla de baterías y comentarios de normas.
  - Clasificación del TDI, cambio mínimo importante (5,5 / 3 / 2,5) e informe de ejemplo.
  - Errores frecuentes y preguntas.
- **H29**:
  - Mecanismo y controles; tabla de falsos positivos y negativos.
  - Contraindicaciones; tabla de fármacos; técnica 1-11.
  - Hoja de registro; reacciones adversas y manejo de la anafilaxia.
- **H30**:
  - Volúmenes y capacidades; compresión dinámica; punto de igual presión.
  - Maniobra y criterios; broncodilatador.
  - GLI y LIN; patrones; gravedad.
  - OVAS (según el manual y la discusión del recuadro); errores frecuentes.

## Lo que NO se pudo comprobar con fuente

- **Whitcroft 2023** (Rhinology 61 Suppl 33, PMID 37454287; no es de acceso abierto; el PDF no se pudo descargar). Quedan sin comprobar las cifras de H28:
  - Autorreporte: especificidad 87 %, sensibilidad 31 % (l.13).
  - 30-40 % de los pacientes con rinosinusitis crónica y olfato alterado que se describen como normales (l.13).
  - 98 pacientes evaluados a los 18 meses (37 %, 60 %) (l.22).
  - 1 226 pacientes con patrón de subpruebas (l.72).
  - 2 178 participantes con sensibilidad de umbral 64 %, D 56 % e I 47 % (l.72).
  - Desiato: 25 estudios, 175 073 personas, 22,2 / 28,8 / 9,5 % (l.27).
  - 479 / 765 / 53 casos con diferencia de ≥3 puntos entre lados (l.132).
  - Cortes unilaterales 2,5 / 3 y "70 % de acuerdo".
  - Recomendaciones de corticoides, entrenamiento ≥3 meses y pronóstico postraumático ~30 %.
  - Se buscó en PubMed/Europe PMC (solo resumen) y en la web (la búsqueda no devolvió estas cifras).
- **H28**:
  - Hummel 2017: ~un tercio de 262 pacientes posinfecciosos mejoró en 14 meses (l.192); solo se leyó el resumen.
  - "6 a 30 millones de neuronas" (l.37).
  - BAST-24 y BOT-8: no localicé la referencia de la sigla BOT-8.
  - PEA en propilenglicol como equivalente del butanol: confirmado en Oleszkiewicz 2019 (cita [17]); no se vio el estudio original.
  - Séptima inversión como fin de la escalera (l.108, ya marcada `verificar`): coincide con el procedimiento estándar de Hummel 1997/2007; no pude abrir el manual del fabricante.
- **H29**:
  - Bernstein 2008 (diluciones, embarazo, ≥3 mm sobre el negativo, plazos de la hidroxizina de 96 h, tricíclicos 7-14 d) y Powrie 2015 (SOP BSACI; "cerca de la mitad de las pruebas positivas…"): no consultados. Las afirmaciones que se atribuyen a Heinzerling sí se confirmaron.
  - Panel de alérgenos para Chile: sigue sin fuente chilena (verificar ya marcado).
- **H30**:
  - Stanojevic 2022: PDF no accesible (bloqueo 403; solo página de resumen). Sin comprobar en el texto: respuesta al broncodilatador >10 % del previsto, gravedad por z-score y la clasificación de OVAS (FIF50/FEF50). Coincide con el estándar tal como lo recuerdo, no verificado en el texto.
  - Manual SER 2024 (control biológico con CV <10 %, ±3 % de linealidad, FIF50 >72 % del teórico, FEF50/FIF50 0,9-1,1, FEV1/PEF <8): no hay copia local. La razón FEV1/PEF >8 sí está respaldada por Miller 1990.
  - GINA 2024 y GOLD/Singh 2025: se asumen según el texto del libro.

## Conteo

- GRAVE: 1.
- IMPRECISO: 6.
- DISCUTIBLE: 2 (ambos sin error; se dejan como notas de contraste).
