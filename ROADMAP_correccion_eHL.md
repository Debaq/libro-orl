# Roadmap: revisar el libro después del cambio de la corrección nHL → eHL en LabSim

Decidido por él el 2026-10-19: se hace la **opción 1** (revisar todo, capítulo por capítulo) en una conversación nueva. Nada de esto tiene commit todavía, ni en el libro ni en LabSim.

## Qué se cambió (2026-10-19)

**En LabSim** (`labsim_backend/src/CaseProfile.php`):
- `STIM_NHL_CORRECTION` pasó a la tabla de la BSA 2019 (*ABR testing for post-newborn and adult*, OD104-84, Apéndice C, fonos de inserción) y ahora depende de la edad corregida (`nhlCorrection()`):
  - **Mayores de 24 semanas y adultos:** burst 20 / 15 / 10 / **10** (antes el 4 kHz era 5); chirp por frecuencia 15 / 10 / 5 / 5; click **5** (antes 10).
  - **Lactantes de 12 a 24 semanas:** burst de 4 kHz 5, chirp de 4 kHz **0**, click **0**.
  - **Menores de 12 semanas:** se dejó la tabla anterior. Está **pendiente** la guía BSA para recién nacidos (OD100, 2025), que no se pudo descargar. No se tocó para no cambiar el tamizaje: el AABR lee el CE-Chirp.
  - **CE-Chirp de banda ancha:** sin corrección publicada; queda en 5, igual que el click.
- `project()` ahora pasa la edad también a la vía aérea.
- `tests/test_case_profile.php`: se ajustaron las esperas y se agregaron 4 pruebas por edad. `php tests/run.php` da **OK, 6827 asserts** (se saltan las que piden `pdo_sqlite`). Las pruebas de Python del ABR no se corrieron porque falta pytest.
- `docs/manual/capturas/casos_demo.json`: se recalculó el ABR de los 10 pacientes de práctica.

**En el libro:**
- Se recalculó el ABR guardado de los casos (`casos/generados/*.json`) con `CaseProfile::project()`. Antes, con la tabla vieja, el script reprodujo 822 de 822 campos, así que la cuenta es fiel. Cambiaron 130 de 137 casos: click, burst de 4 kHz y NB chirp de 4 kHz, por vía aérea y ósea.
- Se regeneraron las figuras del motor (`figuras/hacer_figuras.py`, con el Python de LabSim: `~/micromamba/envs/labsim/bin/python`, que tiene pyqtgraph). Cambiaron **61 figuras de ABR y 9 de ECochG**; ninguna otra.
- `figuras/motor/ecochg.py`: muestra "—" cuando no hay razón de áreas. Antes se caía con `KeyError: 'area_ratio'` en el caso `cap09_hidrops_retardado`.
- Tablas nuevas en H10 (corrección nHL → eHL, BSA 2019) y en H12 (valores de referencia del VEMP: Rodriguez 2019 y Li 2015).

## Lo que falta: la revisión

Con 5 dB más (o menos) de sensación, las figuras no solo cambian de umbral. **Las latencias se corren entre 0,05 y 0,3 ms**, y algunas ondas aparecen o desaparecen en los niveles bajos. Las notas sobre las figuras (`- @…`) y los textos que citan esas cifras quedaron desactualizados.

- **Capítulos:** 10 (1 figura), 11 (6), 12 (10), 13 (6), 14 (3), 15 (5), 17 (11), 18 (5), 19 (3), 27 (1), 34 (3), H9 (1), H10 (6). Y las ECochG de los caps. 9, 23, 34 y H11.
- **Cuánto:** unas 99 notas con latencias y 97 con niveles en dB, más los "Razonamiento", los informes y las guías del docente que repiten esas cifras.
- **Método, capítulo por capítulo** (empezar por el cap. 11 como muestra y que él lo revise):
  1. Abrir la figura nueva y la anterior (`investigacion/revision_abr_ehl_2026-10-19/figuras_antes/`).
  2. Ajustar cada cifra de las notas, del razonamiento y del informe a la figura nueva: latencias, interpicos, diferencias interaurales, umbrales en dB nHL.
  3. Comprobar que la conclusión del caso siga en pie. Si cambia lo clínico, avisarle antes de reescribir.
  4. Armar el capítulo: si una nota apunta a una onda que ya no está, el armado se detiene y lo dice.

### Casos que hay que mirar con cuidado
- **Caso 9.2 (`cap09_hidrops_retardado`, ECochG):** el OD antes salía "sin respuesta identificable" y ahora muestra PS y PA medibles (PS/PA −5,24, sin razón de áreas). Hay que decidir si el caso sigue enseñando lo mismo.
- **Cap. 34 (Ismael):** el 2026-10-19 se ajustaron a mano la tabla de umbrales estimados y la AMA a 3,0 %, con la figura vieja. Con la nueva, el burst de 4 kHz da 80 / 75 nHL, 80 − 10 = 70 eHL, y **la AMA vuelve a 3,9 %**. También cambian las notas del click.
- **Cap. 17 (lactantes de 4 meses):** las notas del click se ajustaron con la figura vieja. Ahora el umbral del click baja 10 dB y el eHL vuelve a coincidir con la audición. Algunas vías óseas que antes daban "sin respuesta" ahora responden (por ejemplo, `cap17_asfixia_perinatal`: click óseo de "sin respuesta" a 50).
- **H10, caso de Hernán:** la cuenta del click (60 − 5 = 55) se hizo con la figura vieja.
- **`cap13_p40`, `h9_p40`, `h10_p40`:** el burst óseo de 4 kHz pasa a "sin respuesta" y el click óseo aparece a 55.

## Archivos de apoyo

En `investigacion/revision_abr_ehl_2026-10-19/`:
- `revision_abr.txt`: por figura, qué latencias cambiaron (antes → después) y las notas del libro que la acompañan. **Es la lista de trabajo.**
- `lat_cambios.json`: lo mismo, en datos.
- `cambios_por_caso.json`: qué umbrales cambiaron en cada caso.
- `difs_figuras.txt`: textos que cambiaron dentro de cada figura; sirve para la ECochG.
- `figuras_antes/`: las 70 figuras como estaban.
- `casos_antes/`: los casos y `casos_demo.json` como estaban. Sirven para deshacer el cambio: copiar de vuelta, revertir `CaseProfile.php` y regenerar las figuras.
- `recalc_abr.php`: recalcula el ABR de los casos con el código de LabSim. Se usa así: `php recalc_abr.php <labsim_backend> <salida.json> <casos…>`.
- `lat.py`: calcula las latencias desde las anclas de las figuras. Espera `salida_vieja/`; hay que apuntarlo a `figuras_antes/`.

## Después de esto

- **VEMP en LabSim**, el segundo paso que se acordó: cambiar `resources/vemp/normative_data.json` y `src/vemp/protocol.py` (`EMG_REFERENCIA` de 50 / 40 µV) a la tabla nueva de H12 y a un EMG realista, para que la amplitud corregida ronde 1. Arrastra 34 figuras de VEMP en 13 capítulos y el ejemplo de informe de H12, que hoy dice "5,68 corregida".
- **Guía BSA para recién nacidos (OD100, 2025):** conseguirla y completar la fila de menores de 12 semanas, en el libro y en LabSim.
- **Vía ósea:** LabSim suma a la ósea la misma corrección de la aérea más su propia referencia (+15 dB en el adulto, de Stuart y cols., 1993). La BSA 2019 da para la ósea correcciones propias según la edad. Revisar si conviene alinearlo.
