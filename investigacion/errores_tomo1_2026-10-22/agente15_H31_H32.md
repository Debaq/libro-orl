# Agente 15: revisión de H31 y H32 (sueño, CPAP, DAM)

Ambos capítulos se leyeron completos. Los `.py` (H31.py, H32.py) tienen `CASOS = []`: no hay casos que cotejar. Las cuentas se rehicieron (ver al final).

## Hallazgos

### GRAVE
Ninguno.

### IMPRECISO

1. **IMPRECISO H32 l.241** (efectos dentales del DAM): "frente a 0,1 ± 0,6 mm y 0,2 ± 0,7 mm con el CPAP" para sobremordida y resalte. El resumen de Doff 2013 (PMID/DOI 10.1007/s00784-012-0737-x) da en el DAM overbite -1,2 ± 1,1 mm y overjet -1,5 ± 1,5 mm (coincide con el texto). Pero la cifra "-0,1 ± 0,6" del resumen es del **cambio anteroposterior de la oclusión** en el grupo CPAP (en el DAM fue -1,3 ± 1,5), no de la sobremordida. El "0,2 ± 0,7" no aparece en el resumen. → Los valores del CPAP están posiblemente mal asignados. Corrección: comprobar con el texto completo de Doff 2013 (o Ramar 2015) y, si no se puede, citar solo las cifras del DAM, o la cifra de -0,1 como cambio anteroposterior de la oclusión.

2. **IMPRECISO H31 l.277** (cortes de gravedad 5/15/30): se atribuyen a "Lumeng y Chervin, 2008", que es una revisión de epidemiología **pediátrica**. Los cortes del adulto vienen de la AASM Task Force 1999 (Sleep 22:667) y de la ICSD-3. La cifra es correcta (<5, 5-<15, 15-<30, ≥30). → Cambiar la cita por AASM 1999 o ICSD-3.

3. **IMPRECISO H31 l.127** (Epworth): "16 o más indica somnolencia alta (Johns, 1991)". Johns 1991 solo da controles 5,9 ± 2,2 (rango 2-10) y pacientes; la banda 16-24 como "grave" viene de interpretaciones posteriores (Johns 1992/2000), no del artículo de 1991. → Citar la fuente de la banda o quitar la atribución.

4. **IMPRECISO H31 l.126** (STOP-Bang, riesgo con 3-4 puntos): el texto dice que "STOP ≥ 2 más IMC > 35" clasifica como alto. El resumen de Chung 2016 (PMID 26378880) dice exactamente eso como ejemplo; el criterio completo es STOP ≥ 2 más **uno de**: IMC > 35, sexo masculino o cuello > 40 cm. Como está escrito, parece la única vía. Las cifras de sensibilidad (93 % y 100 %), VPN (90 % y 100 %) y probabilidades (18 % a 60 %) coinciden con el resumen. → Agregar "o sexo masculino, o cuello > 40 cm".

5. **IMPRECISO H31 l.115** (Friedman): las definiciones de estadio I/II/III coinciden con Friedman 2002 (resumen PMID 12161725; éxitos 80,6/37,9/8,1 %; n = 134). Pero esa definición deja sin clasificar la combinación paladar 1-2 con amígdalas 0-2; la estadificación posterior de Friedman la ubica en el estadio II y agrega el estadio IV (IMC > 40 o alteración craneofacial grave). El lector puede toparse con pacientes sin estadio. → Una línea: "las combinaciones no listadas (paladar 1-2 con amígdalas 0-2) las ubica la versión posterior en el estadio II" o citar Friedman 2004/2009.

6. **IMPRECISO H31 l.57-58** (N3): "en más del 20 % de la época". La regla AASM dice "≥ 20 %". Mínimo, sin consecuencia. Mismo capítulo: la EMG tibial es un canal por pierna con un par de electrodos (l.173 "uno por pierna"): sin consecuencia.

### DISCUTIBLE
Ninguno hallado.

### Omisión (no es error, a criterio del autor)
- **H32 sección DAM**: el texto no dice nada de la titulación del avance (práctica habitual: llegar al 50-75 % del avance máximo, ajuste progresivo hasta controlar síntomas y ronquido), ni de contraindicaciones relativas (enfermedad periodontal activa, pocos dientes, trastorno temporomandibular grave). El ítem del encargo "avance 50-75 % del máximo" no figura. No lo pude comprobar con una fuente primaria (Ramar 2015 no lo fija como número en el resumen). Si se agrega, citar fuente (p. ej. Ramar 2015 texto completo / AADSM).

## Verificado y correcto (con fuente)
H31:
- Apnea ≥ 90 % con sensor térmico, ≥ 10 s; hipopnea ≥ 30 % con presión nasal, ≥ 10 s, desaturación ≥ 3 % o despertar (regla 1A); 4 % como alternativa (1B); toda la porción con apnea se puntúa apnea; sensor térmico "no proporcional al flujo y suele sobrestimar el flujo cuando baja"; presión nasal proporcional al cuadrado del flujo; manometría esofágica o RIP como sensores de esfuerzo; carboxihemoglobina sube la SpO2 (Berry 2012, PMC3459210).
- Definición de mixta (sin esfuerzo y luego con esfuerzo): el artículo de 2012 no la redefine ("sin cambios"); la marca `verificar` del capítulo ya lo señala. No es error.
- Kapur 2017 (PMC5337595 y resumen): riesgo aumentado, no usar cuestionarios, PSG tras HSAT negativa o inadecuada, contraindicaciones de HSAT, split-night (≥ 2 h de registro con apnea moderada-grave y ≥ 3 h para titular), HSAT adecuada con ≥ 4 h de oximetría y flujo, criterios ICSD-3 (≥ 5 con síntomas o ≥ 15 sin síntomas).
- Eckert 2013 (PMID 23721582): 75 sujetos; 36 %, 37 %, 36 %, 28 %, 19 %; Pcrit 0,3 (-1,5 a 1,9) frente a -6,2 (-12,4 a -3,6): todo coincide con el resumen.
- Saldías 2020 (PMID 33399673): 205 personas, 49 % (62 % hombres, 31 % mujeres) con IAH ≥ 5, 16 % con IAH ≥ 15; sin asociación con somnolencia. Coincide.
- Young 1993, Peppard 2013, Benjafield 2019, Peppard 2000, Marin 2005, Netzer 1999: cifras coinciden con lo que conozco; no releí los PDF.
- Reglas de etapas (W, N1, N2, N3, R), derivaciones EEG/EOG, ciclos de ~90 min, IAH 20,5 y clase "moderada".
- Reglas pediátricas (apnea obstructiva ≥ 2 respiraciones, central 20 s o 2 respiraciones con despertar/desaturación ≥ 3 %, hipopnea ≥ 2 respiraciones).

H32:
- Patil 2019 (resumen y PMC6374094): recomendaciones 1-9 con su fuerza coinciden (PAP vs nada: fuerte en somnolencia, condicional en calidad de vida e hipertensión; APAP en casa o titulación: fuerte; CPAP/APAP sobre BPAP: condicional; educación: fuerte; conductual y telemonitorización: condicional); lista de comorbilidades correcta; "interfaces nasales sobre oronasales por menos efectos adversos" figura en la sección de selección de mascarilla (el texto la presenta como recomendación de la guía; no está en las 9 recomendaciones numeradas, pero sí en el cuerpo de la guía); efectos adversos (sequedad, boca seca, dolor de garganta, sinusitis) correctos.
- Kushida 2008: valores de la tabla de titulación (inicio 4 cmH2O; BPAP 8/4; máximos 20 y 30; diferencia 4-10; ≥ 1 cmH2O cada ≥ 5 min; umbrales 2 AO / 3 H / 5 RERA / 3 min de ronquido; paso a BPAP con 15 cmH2O) y los cuatro grados (óptima RDI < 5 por ≥ 15 min con REM supino, buena ≤ 10 o 50 % si basal < 15, adecuada 75 %): concuerdan con mi conocimiento de la guía; no se pudo abrir el texto completo (ver "no comprobado").
- Kribbs 1993 (PMID 8466125): 35 pacientes, 16 (46 %) con ≥ 4 h en 70 % de los días, sobreestimación de 69 min, uso del mes 1 predice el mes 3. Coincide.
- Deshpande 2016 (PMID 27448430): n = 358, 46/35/19 %, presiones 12/10/11, OR 4,5, IAH residual 11,3/6,4/6,7. Coincide.
- Ng 2003 (PMID 12724125): 10 pacientes, IAH 25,0 a 13,2, presión de cierre -1,6 a -3,9 y -2,5 a -4,7. Coincide.
- Ha 2014 (PMID 23831268): diferencia de 4,28 eventos/h. Rotenberg 2016 (34,1 % sobre 7 h, ~1 h por intervención conductual). SAVE (3,3 h/noche). Coinciden con sus resúmenes.
- Medicare L33718 (4 h en 70 % de las noches en 30 días consecutivos dentro de los primeros 3 meses): correcto según mi conocimiento; no abrí el documento.

## Cuentas rehechas
- H31: 100/5 h = 20; 100/8 h = 12,5. Informe de ejemplo: (47+9+6+88)/(440/60) = 150/7,333 = 20,45 (20,5); IDR (150+26)/7,333 = 24,0; eficiencia 440/480 = 91,7 %; 14 + 26 + 440 = 480; REM+NREM suman ~150 eventos (47,2 y 13,2 por hora). Porcentajes de etapas suman 100,1 (redondeo).
- H32: descarga de ejemplo 23/30 = 76,7 % (77 %). Pregunta 5: (18x6 + 6x2)/30 = 4,0 h; noches con ≥ 4 h = 18/30 = 60 % (no cumple 70 %). Presión: 10 cmH2O ≈ 0,98 kPa.

## No se pudo comprobar con fuente
- Texto completo de Kushida 2008 (grados y reglas de titulación), Ramar 2015 (recomendaciones y fuerza), Morgenthaler 2008, Manual AASM v3 (acceso restringido; buscado en PubMed/Europe PMC/PMC). Los valores se contrastaron con mi conocimiento, no con el texto.
- Ip 2012 (11 min y 0,5 de Epworth), Zhu 2016 (3 de 7 funciones), Soudorn 2016, Ravesloot 2017 (11,3/h, 54 %, 84 %), Camacho 2015 (2,7 cmH2O; 89 %), Lebret 2017 (25 %), Nigro 2015 (3,5/h), Strollo 2014, Caples 2010: no se abrieron los resúmenes por tiempo; verosímiles.
- Cifras de Johns 1991, Netzer 1999 y Friedman 1999 no se releyeron. No se buscaron en los libros locales de ~/Escritorio/Libros (no contienen medicina del sueño relevante que yo conozca; no los exploré).

## Conteo
GRAVE 0 | IMPRECISO 6 | DISCUTIBLE 0 | Omisión 1.
