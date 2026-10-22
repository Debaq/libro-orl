# Agente 13: revisión de H25, H26 y H27 (rinología y función nasal)

Leídos completos: H25, H26 y H27 (.md). Los tres .py (H25, H26, H27) tienen `CASOS = []`, es decir, no tienen casos que contrastar con el texto.
Cuentas rehechas a mano o con python: todas las de H26 (ver "Sin hallazgos").

## Hallazgos

### GRAVE
Ninguno. No encontré en los tres capítulos nada que enseñe algo falso de forma peligrosa.

### IMPRECISO

- **[IMPRECISO] H26 l.291 (tabla "Qué indica la resistencia después del vasoconstrictor")**: la fila "Sube respecto del reposo → Vasomotora, sin descartar un componente mecánico ('efecto rebote')". Un aumento tras UNA dosis medida a los 15 minutos no es rebote. El propio recuadro de l.297 lo reconoce, pero la tabla igual enseña "vasomotora". Lo correcto es tratarlo como resultado a repetir (ciclo nasal, sello, respiración), no como categoría diagnóstica. En H27 (l.226) la misma situación sí se maneja bien ("revisa la técnica antes de interpretar"). Fuente: los textos del propio capítulo; el rebote (rinitis medicamentosa) se describe con uso repetido (Graf 1997, citado en H25). Corrección: cambiar la fila a "Sube: repetir; no interpretar" o igualarla a H27.

- **[IMPRECISO] H25 l.66**: "Ahí [en la válvula, a 1,3 cm de la narina] se genera la mayor parte de la resistencia: ... cerca de dos tercios de ella estaban en la zona de la apertura piriforme y un tercio en el vestíbulo (Haight y Cole, 1983)". Haight y Cole (abstract en Europe PMC) dicen 2/3 de la resistencia en el cavum óseo, junto a la apertura piriforme, y 1/3 en el vestíbulo cartilaginoso. El texto lo presenta como si el 2/3 fuera "la válvula a 1,3 cm" (la válvula interna definida por Rhee 2010). Son dos definiciones de "dónde está la válvula" que no coinciden exactamente. Bloching 2007 (abstract) la describe como "lugar de máxima resistencia (segmento limitante del flujo)". Corrección: decir que la resistencia se concentra en la región de la apertura piriforme y la cabeza del cornete, y que la "válvula" es esa zona completa, sin sugerir que el 2/3 está exactamente a 1,3 cm.

- **[IMPRECISO] H26 l.182 y figura h26-rs-equipo**: el pie dice que la izquierda (R150 = 0,38) "no necesitaba la prueba", pero da un total con vasoconstrictor de 0,18. Con la derecha en 0,46: 1/(1/0,46 + 1/0,38) = 0,208, no 0,18. Para 0,18 la izquierda tendría que ser ~0,30 con vasoconstrictor (es decir, se la midió también). Comprobado con python. Revisar si el pie o el valor mostrado en la imagen están desfasados. No pude ver el PNG, solo el pie.
  Las otras cuentas del pie sí cuadran: reposo 1/(1/0,81+1/0,38) = 0,26; descenso 0,81 a 0,46 = −43 %.

- **[IMPRECISO] H26 l.72 y l.93-96 (Cottle: presiones 75/100/150/300 Pa, velocidad de papel, tabla de patrones)**: ya marcado `verificar` por los autores. No pude comprobarlo (ver "No comprobado"). La tabla de patrones es de material de clase; "pausa espiratoria > 1 s = obstrucción posterior" y "descanso a mitad del ciclo = enfermedad cardiopulmonar crónica" no tienen respaldo primario. No lo reporto como falso, pero conviene que figure como orientación débil. El capítulo ya lo dice.

- **[IMPRECISO] H27 caption h27-rs-curva (l.49-50) y tabla de equipo (l.138-139)**: MCA1 "1,3 cm" y MCA2 "unos 1,5 cm² a 3,1 cm" en un "paciente sano en reposo". El consenso (Clement y Gordts 2005, citado en el propio capítulo) dice que el paso más estrecho suele estar dentro de 3 cm y que la cabeza del cornete está a unos 3,3 cm. Los valores son coherentes con eso. Pero un MCA2 de 1,5 cm² en reposo sin descongestión es amplio para una referencia, y las cifras vienen de RinoSim (no es fuente). Como el texto dice "los valores de referencia de verdad son los de la tabla de tu servicio", no es un error. Corrección opcional: en el pie, decir "valores ilustrativos de un simulador".

### DISCUTIBLE

- **[DISCUTIBLE] H25 l.66, ángulo de la válvula**: el texto da 10-20° (Bloching 2007, que cita a Mink). La enseñanza habitual en rinología dice 10-15° (esa fue la redacción anterior y la del encargo). Ambas cifras circulan; la corrección de la pasada anterior es defendible. Dejar con las dos citas si se quiere ser explícito.

- **[DISCUTIBLE] Tiempo de adaptación: 15 min (H25, H26, H27) vs 20-30 min** del consenso (Clement y Gordts 2005, texto completo según la nota de los autores). Los tres capítulos lo reconocen, H26 y H25 en recuadro "Lo que dicen las normas", H27 solo con `verificar`. H27 no tiene el recuadro de la norma para la aclimatación (sí lo tiene H25/H26). Sugiero copiar la frase.

- **[DISCUTIBLE] H26 l.238**: la crítica de Vogt 2016 (flujo a 150 Pa es "estimación" obsoleta) está bien resumida (abstract: "reject the further use of these parameters as obsolete"). Sí corresponde marcarla como postura de un grupo, como ya está. Sin cambios.

- **[DISCUTIBLE] H26 l.36 y l.38 "nariz ~ la mitad de la resistencia" (Ferris 1964)**: ya con `verificar`. Fuentes secundarias dan entre la mitad y dos tercios. No es error.

### Omisiones frente al encargo (no son errores del texto)
H25 no contiene: Lund-Kennedy, clasificaciones de pólipos (Lildholdt, Meltzer, tamaño endoscópico 0-4), maniobra de Cottle con ángulo cuantificado (sí describe la maniobra), rinosinusitis crónica con los criterios endoscópicos o de TAC de EPOS (sí da el criterio por síntomas y duración, que es correcto), NSAID, clasificación de hipertrofia de cornetes, grados de desviación septal. Si el libro quiere cubrir endoscopía, falta contenido; el capítulo dice explícitamente que la endoscopía "no es parte de esta herramienta".
H27 no da valores normales numéricos (decisión declarada del capítulo). H26 sí da una referencia (0,4 por fosa) con matiz.

## Sin hallazgos (revisado y correcto)

H25
- NOSE: 5 ítems 0-4, suma ×5, 0-100. Correcto (Stewart 2004).
- SNOT-22: 22 ítems 0-5, total 0-110, MCID 8,9 (Hopkins 2009) y estratificación leve 8-20, moderado >20-50, grave >50 (Toma y Hopkins 2016; confirmado en abstract de Europe PMC, 65 pacientes). Correcto. Los cinco dominios agrupados: correcto.
- EVA 0-10 de obstrucción (Bousquet PJ 2007): ok.
- Definición de rinosinusitis aguda <12 sem / crónica ≥12 sem con ≥2 síntomas, uno de ellos obstrucción o secreción: coincide con EPOS 2020. AAO-HNS aguda hasta 4 semanas: correcto.
- Señales de alarma EPOS 2020 (unilateralidad, sangrado, costras, cacosmia, signos orbitarios, cefalea intensa, tumefacción frontal, signos neurológicos): coincide.
- ARIA (intermitente <4 días/sem o <4 sem; leve vs moderada-grave): correcto.
- Cottle: descrita como tracción de la mejilla; distinguida de la "rinomanometría de Cottle". Correcto.
- Anatomía de meatos y drenaje: correcta.
- Poiseuille r^-4 (radio a la mitad = ×16): correcto. Bernoulli y colapso valvular en inspiración forzada: correcto.
- Ciclo nasal 72 % vs 21 %, resistencia total más estable: coherente con H26.
- Clasificación de la limpieza del espéculo como semicrítico con desinfección de alto nivel mínima (Rutala y Weber): correcto.
- Diferenciación de términos del olfato y causas (Hummel 2017): sin objeciones.

H26
- Rehechas con python y a mano: R = ΔP/V̇; 1 Pa/(cm³/s) ≈ 10,2 cmH₂O/L/s; 0,30 → 3,06 ≈ 3,1; 600 cm³/s = 36 L/min.
- Ejercicio 1: 0,60 y 0,30. Ejercicio 2: 1/RT = 1,667+3,333 = 5,0, RT = 0,20; suma de flujos 750, 150/750 = 0,20. Correcto.
- Ejercicio 3: 150/400 = 0,375 (−37,5 %); total 1/0,375+1/0,30 = 6,0, RT = 0,167 ≈ 0,17. Correcto.
- Ejercicio 4: 150/330 = 0,4545 (−24,2 %); 150/255 = 0,588 (−2 %). Correcto.
- Ejercicio 5: 110/300 = 0,367. Correcto.
- Promedio 0,45 vs total 0,20. Correcto. Figura de curvas: total de 0,35 y 0,29 en paralelo = 0,159 ≈ 0,16. Correcto.
- Ecuación de Rohrer ΔP = k₁V̇ + k₂V̇², R = k₁ + k₂V̇: correcta.
- Resistencias en paralelo y su precisión (misma presión): correcto.
- Técnica anterior activa (presión de la nasofaringe por la fosa ocluida, flujo en la otra; contraindicación por perforación septal y atresia coanal): correcto.
- Ren 2018 (Europe PMC): 505 sanos; unilateral 150 Pa media 0,511 (IC 0,086-0,936), total 0,243 (0,112-0,374). Coincide con lo citado.
- Vogt 2016 (abstract): 36.563 mediciones; 20.069 sin tratamiento; percentiles de 20 % (cinco grados); xilometazolina 0,1 %. Coincide.
- Flanagan y Eccles (11 de 52 ≈ 21 %) coherente con H25.
- Descongestión en dos pasos (2 sprays de 50 µg, otro a los 5 min; medir a 15-30 min): citada del texto completo del consenso según nota de los autores.
- Contraindicaciones para la prueba de provocación y umbrales ≥40 %/≥20 % del flujo: ver "No comprobado".

H27
- Principio de reflexión acústica; eco más fuerte y del mismo signo ante estrechamiento, invertido ante ensanchamiento: correcto.
- Hilberg 1989 (abstract en Europe PMC): CV <2 % del método acústico vs 15 % en rinomanometría. Coincide.
- Hilberg y Pedersen 2000 (abstract): informar volumen 0-5 cm (2-5 cm para cambios de mucosa), las dos primeras áreas mínimas con sus distancias, control de temperatura y ruido, atención al adaptador. Coincide.
- Subestimación detrás de estrechez marcada y sobreestimación pasados 5-6,5 cm por senos y rinofaringe (Hilberg y Pedersen 1996, Cakmak 2003 y 2005): coherente con lo que dicen los resúmenes citados.
- MCA2 correspondiente a la cabeza del cornete a 3,3 cm: coincide con la cita literal del consenso.
- Contraindicaciones listadas del vasoconstrictor (IMAO, glaucoma de ángulo cerrado): coherentes con las fichas.
- Tabla de lectura tras vasoconstrictor y el recuadro con Corey 1997 (cambios de 15,6 %/24,6 % y 40 %/36 %): prudente y sin sobreafirmar.
- Coherencia entre capítulos (H25, H26 y H27): válvula a 1,3 cm, 15 min de aclimatación, 48 h y 24 h, dos puff y 15 min: consistente. El valor 0,4 de H26 se discute en el recuadro.

## No comprobado con fuente (y dónde se buscó)
- Que Clement y Gordts (2005) pidan promediar 3-5 ciclos (H26 l.219), el criterio de "3 a 5 respiraciones". Se buscó en Europe PMC (solo abstract) y PubMed (bloqueado por cookies). No hay copia local de ese artículo.
- Porcentajes 4,5-8,6 % de pacientes que no llegan a 150 Pa (Vogt 2016, H26 l.66): el abstract no lo trae; el texto completo no se pudo abrir.
- Umbrales de respuesta de la provocación nasal (flujo a 150 Pa −40 % fuerte, −20 % moderada), 0,1 mL por fosa, esperas de 4 semanas y 6-8 semanas (Augé 2018, H26 l.337-339). El abstract confirma solo "0,1 mL por narina" y que existe un catálogo de criterios. Texto completo no abierto.
- Radio 2 del consenso / "radio 200" de Broms, y la escala (H26 l.104, 109): ya marcado `verificar`; no hay fuente local.
- Que el criterio de repetibilidad sea 0,03 cm² entre registros (H27 l.168, 173): ya `verificar`; el abstract de Hilberg y Pedersen 2000 no da ese número.
- Hopkins 2009 (n = 3.128, MCID 8,9): la búsqueda por título devolvió otro artículo (SNOT-22 en fibrosis quística). Lo di por correcto por conocimiento propio, no verificado en esta pasada.
- Ferris 1964 ("~la mitad"), Keck 2000a/b, Sun 2002, Hasegawa y Kern: no abiertos; ya con notas de los autores.
- Libros locales de ~/Escritorio/Libros no tratan rinología (son de audiología, vestibular y neuroanatomía), por lo que no hubo qué consultar allí. No los reviso uno por uno.

## Conteo
GRAVE: 0. IMPRECISO: 5 (de ellos 1 de cuentas/figura H26, 1 de interpretación H26, 1 de anatomía-fisiología H25, 2 de datos de figuras y material de clase). DISCUTIBLE: 4. Omisiones de contenido: 1 (H25: endoscopía/pólipos).
