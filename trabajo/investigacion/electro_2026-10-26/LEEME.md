# Figuras de ASSR, MLR, corticales y ECochG con los motores de LabSim (clases de Electro, 2026-10-26)

Scripts que generaron las figuras de los decks C08, C10b, C11b y C13b del curso ETMP196, a partir de los casos del libro.
Cada uno tiene dos modos: `capture` (env `labsim`: `micromamba run -n labsim python fig_X.py capture`) escribe el JSON;
sin argumento (python del sistema, con matplotlib) dibuja los PNG. Las rutas de salida apuntan al scratchpad del curso: cambiarlas.

- `fig_assr.py` — `abr.assr.Recording` con la búsqueda automática (`auto_step`) sobre `data['ABR']` del caso: grilla de detección por nivel (p de la prueba F), espectro con las ocho líneas, audiograma nHL → eHL contra `data['Aerea']`. Casos: rubéola (17.3), CMV (17.2), efusión neonatal (17.1), asfixia (17.4), cap19_sobre_real, cap19_nina. Para la rubéola hay que partir en 90 y subir `assr.MAX_EPOCHS`.
- `fig_cortical.py` — `motor.cortical._ventana` con el bloque `Central` modificado en memoria: ACV (efecto electrodo en C4), schwannoma (efecto oído), niña dormida/despierta, reflejo postauricular (tensión cervical + montaje mastoides/lóbulo), P1 retrasada en implante (6 → 7 años), P300 lenta con error de conteo.
- `fig_ecochg.py` — `AbrMainWindow` en prueba ECochG, con montaje/filtros/nivel/polaridad/ventana/tasa variados; marcas de `abr.ecochg.auto_marks` + `measure_complex`.
