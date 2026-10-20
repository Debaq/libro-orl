# Pasar los audiogramas del tomo II a la hoja auditiva

Libro de ORL para tecnólogos médicos, en español de Chile. El autor decidió (2026-10-20) que **todos los casos del tomo II (capítulos 1 a 36) usan la "hoja auditiva"** (`fig.audiosupra()`, generador `figuras/motor/audio_supra.py`). Los capítulos B y H (tomo I) no se tocan. Los vestibulares (20-27, 31, 32) ya están hechos: míralos como modelo (`capitulos/21-vertigo-agudo.md` y `.py`).

## Qué es la hoja auditiva
Una sola figura por caso: el audiograma combinado (frecuencias arriba, ósea completa de 250 a 4.000 Hz si una frecuencia la pide, LDL, Fowler sobre la frecuencia estudiada) y, a la derecha, en datos: diapasones (Weber y Rinne en 500 y 1.000 Hz), logoaudiometría (SDT, SRT, UMD con los tres mejores intentos; con ruido "80 dB/60 dB"; en esta figura se enmascara cuando la voz pasa de 45 dB) y supraliminares cuando hay pérdida sensorioneural (SISI, Carhart en 2 y 4 kHz, Metz, decay del reflejo). Todos los datos salen del caso de LabSim.

## Qué hacer en cada caso de tus capítulos
1. **`.py`**: cambia `fig.audiograma()` por `fig.audiosupra()`. Borra `fig.acumetria()` (los diapasones ya van en la hoja) y `fig.logo(...)` (ver punto 4). Si el caso tiene `fig.audiograma(sin_enmascarar=True)` para enseñar la curva sombra, déjalo como `fig.audiosupra(sin_enmascarar=True)` y pon **primero** en la lista el `fig.audiosupra()` enmascarado: así `<caso>_audiosupra.svg` es el enmascarado y `<caso>_audiosupra_2.svg` el sin enmascarar. No cambies nada más del pedido del caso (od, oi, grados, edad, anamnesis): si el pedido cambia, `solo_figuras.py` se detiene.
2. **`.md`**: cada bloque `:::figura <caso> audiograma[ N]` … `:::` (con notas "- @OD 1000 | …", que son globos) se reemplaza por
   ```
   :::imagen figuras/salida/<caso>_audiosupra.svg ancho=100% Audiometría de <nombre>: <lectura en 1 o 2 frases>.
   :::
   ```
   y lo esencial de las notas pasa a **prosa normal** en el párrafo siguiente (sin listas numeradas, sin "@", sin globos). El autor dijo: los globos "no aportan nada", basta un pie de figura normal. Si había dos audiogramas (sin enmascarar y enmascarado), van dos imágenes: primero `_audiosupra_2.svg` (sin enmascarar, "lo que anota quien no enmascara") y debajo `_audiosupra.svg` (enmascarado).
3. **Diapasones**: borra el bloque `:::figura <caso> acumetria`; si su lectura importa (p. ej. Weber al sano y Rinne falso negativo), queda en una frase del párrafo.
4. **Curvas de logoaudiometría**: el autor pidió **eliminar todas las curvas logoaudiométricas salvo que sean necesarias** ("casi en cualquier caso; quizás en uno de reclutamiento"). Borra los bloques `:::figura <caso> logoaudiometria` y su `fig.logo(...)`. Solo deja la curva si **el caso enseña la forma de la curva** (roll-over, curva que cae con la intensidad) y sin ella no se entiende; en ese caso dilo en tu informe. Lo que decían las notas (SDT, SRT, máximo de discriminación) pasa al texto **con los números de la hoja**.
5. **Números**: después de cambiar el `.py`, rehace las figuras (`cd herramientas && python3 solo_figuras.py ../capitulos/NN-*.py`) y **lee los valores en el SVG** (`grep -o '>[^<]*<' figuras/salida/<caso>_audiosupra.svg`). El texto, el pie y el informe deben decir lo mismo que la hoja: SDT, SRT, UMD (porcentaje e intensidad), umbrales. Si el texto decía otro número, corrige el texto (el caso clínico no cambia; si un dato rompe el caso, avísame en el informe, no inventes).
6. **Supraliminares**: si la hoja muestra supraliminares (pérdida sensorioneural), agrega en el párrafo una frase de lectura con sus datos (p. ej. "SISI de 90 %, Carhart sin deterioro en 2 y 4 kHz y Metz de 40 dB: recluta, es coclear"; con 30 dB de deterioro, "Carhart con deterioro de 30 dB…"). En el informe de la resolución (`#### Informe` o texto equivalente), agrega "**Supraliminares:** …" si hay un informe de audiometría.
7. No dejes frases de "lo que no corresponde" ("no se hicieron supraliminares…"). No agregues pruebas que no estén en la hoja.

## Reglas
- Escribe como el resto del libro: frases cortas, español de Chile, sin relleno. Mantén las remisiones (→ H3, cap. 11).
- No armes el libro ni capítulos en PDF. No hagas commits. No toques capítulos que no son tuyos ni el tomo I.
- Al terminar, verifica: ningún `:::figura <caso> audiograma|acumetria` en tus capítulos; los `:::figura … logoaudiometria` que queden, justificados; todas las rutas de `:::imagen` existen.

## Informe final (corto)
Por capítulo: casos cambiados, curvas de logo que quedaron y por qué, números de texto que corregiste, y cualquier dato de la hoja que contradiga el caso.
