# Revisión de errores: B02 (fisiología) y B04 (física)

Fecha: 2026-10-22. Se leyeron completos ambos capítulos. En B04 se rehicieron con python3 todas las cuentas (ver lista al final). No se editó ningún archivo del libro.

Resultado corto: no encontré errores GRAVES. Los cálculos de B04 salen bien salvo un par de signos cambiados. B02 es un esquema de contenidos (la autora lo escribirá) y no tiene afirmaciones falsas.

## Hallazgos (ordenados por gravedad)

### GRAVE
Ninguno.

### IMPRECISO

- **[IMPRECISO] B04-fisica.md l.373** — "si la cabeza queda a 1 m y se mueve 10 cm, el nivel cambia entre +0,8 y −0,9 dB; a 0,5 m, ... entre +1,6 y −1,9 dB" → los signos están cambiados. Acercarse 10 cm da 20 log(1/0,9) = **+0,92 dB** y alejarse da 20 log(1/1,1) = **−0,83 dB**. A 0,5 m: 20 log(0,5/0,4) = **+1,94 dB** y 20 log(0,5/0,6) = **−1,58 dB**. Fuente: cálculo (la respuesta 10 de las preguntas, l.507, sí da +0,9 y +1,9, así que el texto contradice a su propia respuesta). Corrección: escribir "entre +0,9 y −0,8 dB" y "entre +1,9 y −1,6 dB".

- **[IMPRECISO] B04-fisica.md l.112** — "Un pasa altos de 100 Hz y un pasa bajos de 3.000 Hz dejan adentro el grueso de la respuesta" → el mismo párrafo cita a Hall (1986: picos de energía en 0-200, 500-600 y 900-1.000 Hz) y a Sininger (1995: en el lactante la energía está bajo 100 Hz). Un pasa altos de 100 Hz saca justo esa zona, así que "el grueso" queda adentro solo para las componentes rápidas de las ondas I-V, no por energía. El filtro de 100-3.000 Hz es el estándar clínico, pero la justificación del texto se contradice con sus citas. Fuente: los dos artículos citados (según los comentarios del propio archivo). Corrección: decir que 100-3.000 Hz es un compromiso que conserva las ondas rápidas y saca el EEG lento, a costa de parte de la energía grave (más en el lactante), y remitir a Picton (2010) por la distorsión de latencia.

- **[IMPRECISO] B04-fisica.md l.63** — "el artefacto eléctrico del estímulo, que no se invierte con la respuesta, se cancela al promediarlos" → lo que ocurre es lo contrario de lo que sugiere la redacción: el artefacto (y también la microfónica coclear) **sí invierte su signo** con la polaridad del estímulo, y la respuesta neural **no**. Por eso se cancelan al alternar y la respuesta neural queda. Conviene decir además que la microfónica coclear también se cancela (es relevante para el ANSD y la ECochG, donde se registra por polaridad separada). Fuente: Katz 7.ª ed., capítulos de PEAT (principio estándar de polaridad alternada); Hall 2007. Corrección: "el artefacto y la microfónica invierten su signo con la polaridad del estímulo; la respuesta neural no, y por eso queda al promediar".

- **[IMPRECISO] B04-fisica.md l.96 vs l.106 y la figura de la banda crítica** — el NBN se describe como "de un ancho algo mayor que el de la banda crítica (del orden de un tercio de octava)" → el propio capítulo muestra después que bajo 500 Hz el tercio de octava es **más angosto** que la banda crítica (≈ 58 Hz contra ≈ 100 Hz en 250 Hz; cruce en 500 Hz). Las dos frases no pueden ser ciertas a la vez en graves. Fuente: Zwicker y Terhardt (1980) como cita el capítulo; cuenta: 250 Hz × 0,23 = 58 Hz. Corrección: "ancho de la banda crítica o algo más; en la práctica del orden de un tercio de octava sobre 500 Hz".

- **[IMPRECISO] B04-fisica.md l.404** — "El acoplador de 2 cm³ es una convención repetible... (IEC 60118-0, 2022)" → el acoplador de 2 cm³ se define en la serie IEC 60318 (parte 5) y en ANSI S3.7; IEC 60118-0 es el método de medida de las características del audífono que lo usa. Fuente: memoria del autor de esta revisión; no pude abrir las normas (de pago). Corrección: citar también IEC 60318-5 o decir "según IEC 60118-0 con el acoplador de la IEC 60318-5". Confianza media.

- **[IMPRECISO] B04-fisica.md l.303** — "sus amplitudes se suman como las varianzas" → se suman las **varianzas**; la amplitud (desviación estándar) crece con √N. La conclusión que sigue (σ/√N) es correcta. Corrección: "sus varianzas se suman, así que su amplitud crece con √N".

### DISCUTIBLE

- **[DISCUTIBLE] B04-fisica.md l.223** — "55 dB o más con inserción" → Postura A (el libro): 55 dB como mínimo conservador para inserción. Postura B (Katz 7.ª ed., cap. 6 "Clinical Masking", ~p. 79-81): con ER-3A de inserción profunda los valores publicados van de 75 a 110 dB en ≤1.000 Hz y de 50 a 95 dB sobre 1.000 Hz, y se usa el mínimo, o sea **75 dB en ≤1.000 Hz y 50 dB sobre 1.000 Hz**. Otras guías (BSA 2018) usan un valor único mayor para inserción (de memoria, 60 dB; no pude comprobarlo). El ejemplo resuelto (80 − 55 = 25 dB) es coherente con el 55 del libro. No es error, pero conviene decir que el valor depende de la frecuencia y de la profundidad de inserción, o citar la fuente exacta del 55.

## Revisado y correcto (sin hallazgos)

### B02
Todo el esquema es correcto: transducción (enlaces apicales, K+, glutamato, polarización hacia el cinocilio), neurotransmisores (ACh y GABA en eferentes; glutamato, GABA y glicina en núcleos vestibulares), ITD en oliva superior medial e ILD en lateral, muesca de Carhart, estriola con polarización opuesta, cVEMP sáculo y oVEMP utrículo, "el nistagmo bate hacia el lado más activo", canal como integrador de aceleración, flóculo y nódulo, corteza vestibular insular posterior. Observación menor (no es error): la línea 44 pone "qué hace sobre las CCE" para el sistema olivococlear medial **y lateral**; solo el medial actúa sobre las CCE (el lateral, sobre los dendritos de las fibras tipo I).

### B04: cuentas rehechas con python3 (todas coinciden con el texto)
Período y longitud de onda de la tabla (125 a 8.000 Hz y 226 Hz); c = 331,3 + 0,606 T (343 y 352 m/s); suma de fases (×2, ×1,41, ×1 con 120°); click 100 µs (−3 dB en 4,4 kHz, nulo en 10 kHz); anchos del burst de 5 ciclos (tiempo exacto; ancho a −6 dB 180/370/1.470 Hz es coherente con una ventana tipo Hann, que da 200/400/1.600); banda crítica de Zwicker y ERB 133 Hz en 1 kHz; 20 + 10 log 160 = 42 dB; tablas de 3/6/10 dB; todos los ejemplos de suma, resta y promedio de niveles; RETSPL de TDH-39 y ER-3A (coinciden con ISO 389-1 e ISO 389-2 de memoria y con los comentarios del archivo); ejemplo de calibración cruzada (27 y 39 dB HL, errores de 7 y 19 dB); fuga del tapón (19,6 dB); sonos (2, 4, 8, 16); admitancia 1,00 mmho y 4,43 mmho; λ/4 del conducto 3.430 Hz; daPa (1 daPa = 1,02 mmH₂O, +2 % y −4 %); ejemplo de compliancia 0,7 mL; toda la tabla de promediación (ruido residual, SNR, tiempos a 21,1/s); ejemplo del FSP (4,2; 1,8; 4,2); reproducibilidad → SNR (−12,8; 3,7; 10,0 dB); 9,5/15,1/19,1/25,6 dB de la onda estacionaria; modos de una sala de 3 m (57, 114, 172 Hz); las cifras de la figura de la sala (15,1 dB tono puro, 2,0 dB warble ±5 % con FM sinusoidal, 1,8 dB tercio de octava; mi cálculo da 15,07; 1,97; 1,77); sombra de cabeza 1.900 Hz; 10 log 3 = 4,8 dB; ejemplo del ruido de fondo (1,3 y 19 dB SPL, sube 12 dB); compresión 2:1 (ganancia 7,5 dB); THD (9 %, 8 % de tercer y 3,5 % de quinto armónico al recortar al 80 %: mi cálculo da 9,0 %, 8,2 % y 3,5 %); EIN; 10,5 dB del acoplador; lazo del silbido; ponderación A (los siete valores coinciden con IEC 61672-1) y el ejemplo (93,4 dB y 87,4 dB(A)); tabla de tiempos de 3 dB, OSHA 5 dB, dosis 2,25 y 88,5 dB(A), segunda dosis 2,375 y 88,8; Reynolds (2.430 y 4.180); ejemplo laminar/turbulento (288 y 429 cm³/s, k₂ = 6,4×10⁻⁴, k₁ = 0,075, 29 % y 21 %), que coincide con los 0,26/0,35/0,29/0,16 de H26; paralelo 0,16; Poiseuille ×2,4 y ×16; 1 Pa/(cm³/s) = 10,2 cmH₂O/L/s; reflexión acústica (0,43; 18 %; 76 µs; 0,60 cm²; 181 µs; −0,35; 67 %; 11 %; 0,6 %); 1,8 % por 10 °C. Las 14 respuestas de las preguntas para practicar están bien (salvo el comentario de l.373, que no afecta a la respuesta 10).

Coherencia con otros capítulos: la tasa de 21,1/s, el criterio de reproducibilidad ≥ 70 % y los valores 0,26/0,35/0,29/0,16 de H26 coinciden con H9, H10 y H26.

## Conteo
- GRAVE: 0
- IMPRECISO: 6 (l.373, l.112, l.63, l.96, l.404, l.303)
- DISCUTIBLE: 1 (l.223)

## Revisado y NO comprobado con fuente
- ISO 389-4 (diferencia entre nivel de detección y de enmascaramiento efectivo, "5 a 10 dB"; 4 y 6 dB de las correcciones) y el valor en peSPL del 0 dB nHL del click (30 a 40 dB): ambos ya llevan marca verificar; no los reporté. Katz solo confirma que el peSPL de la norma es de pico a pico.
- Razón crítica de 18 dB en 1.000 Hz (Hawkins y Stevens 1950; marca verificar): plausible, no abierta.
- Hall (1986) y Sininger (1995): usados solo a través de las citas textuales que el archivo trae en sus comentarios.
- Margolis y Goycoolea / Ogut (resonancia 935 y 1.190 Hz), Keck (34 °C en la rinofaringe), Ferris (1964, la nariz como parte más resistente), Sek y Moore (0,6 %), Holte, Kei y Alaerts (sonda de 1.000 Hz bajo 6 meses): consistentes con lo que conozco, no abiertos.
- Correcciones eHL (−20 dB para burst de 500 Hz): coherentes con los protocolos de uso habitual, no comprobadas contra H10/H13.
- NIOSH 1998: 8 % a 85 dB(A) y 25 % a 90, y los descuentos de 25/50/70 %: coinciden con lo que conozco; no abrí el documento.
- Año y edición de normas: ANSI/ASA S3.6-2025 (no pude confirmar que exista esa edición), ANSI S3.1-1999 (R2018), IEC 60645-3:2020, ISO 226:2023, ISO 389-7:2019. Plausibles; no verificadas.
- El 55 dB y el valor de BSA 2018 para la atenuación interaural con inserción (ver DISCUTIBLE).
- Sección de licencias de B02 (CC BY-SA "sin modificar", etc.): es un tema legal, no lo evalué.
