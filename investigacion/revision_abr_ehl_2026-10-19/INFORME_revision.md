# Informe: revisión del libro después de la corrección nHL → eHL nueva de LabSim

Fecha: 2026-10-20. Base: commit `0f07349` (figuras ya regeneradas, notas sin revisar). Nada de esto tiene commit todavía.

**Criterio, decidido por él el 2026-10-20:** los casos se ajustan al contenido de cada capítulo, no al revés. El libro tiene **casos propios**. Después se llevan a LabSim o se crean allá.

## 1. Resumen

Se revisaron las 61 figuras de ABR y las 9 de ECochG que había cambiado la corrección nueva. Quedaron en tres grupos.

**A. Casos que quedaron mal: el caso vuelve a como estaba y el texto queda intacto.** Son los casos en que la figura nueva contradecía lo que enseña el capítulo. El libro usa ahora una copia propia del caso, con sus valores anteriores. Sus figuras salieron **idénticas byte a byte** a las originales (`figuras_antes/`), y el texto no se tocó.

- **Pacientes demo:** `casos/pacientes_demo.json`, copia propia de los 10 pacientes de práctica. Antes se leían de LabSim. Los pacientes solo difieren de LabSim en el bloque ABR. Con esto vuelven a como estaban:
  - Patricia (ECochG del caso 9.1 y de H11; cap. 18);
  - Raúl (caso 11.1 y H10);
  - Tomás (H10 y cap. 18, también la ilustración del promedio);
  - Carolina y Hernán (H10);
  - los pacientes 37 y 42 (cap. 18, cap. 19);
  - el paciente 40 (H9, H10, cap. 13).
- **Casos por cuadro:** `casos/propios/`, una copia de 9 casos con sus valores anteriores. Si existe la copia, el motor la usa en vez de la de `casos/generados/`:
  - `cap09_hidrops_retardado`;
  - `cap12_siderosis`;
  - `cap15_colesteatoma_fistula`;
  - `cap17_cmv_congenito`;
  - `cap23_meniere_avanzado`, `cap23_meniere_bilateral`, `cap23_meniere_migrana` y `cap23_migrana_vestibular`;
  - `cap34_hidrops`.

En total, **34 figuras** y las **5 ilustraciones del cap. 18** volvieron a su versión original. Los caps. 9, 11, 18, 23, H10 y H11 quedan **sin cambios de texto**.

**B. Casos que solo cambiaron en el detalle: el caso queda con la corrección nueva y se ajustan las cifras del texto.** El capítulo enseña lo mismo, solo cambian cifras: latencias que se corren 0,1 a 0,3 ms o umbrales 5 dB más bajos. Son **57 líneas en 6 capítulos** (12, 13, 14, 15, 17 y 34), detalladas palabra por palabra en `apendice_cambios.md`.

**C. Sin cambios:** los caps. 10, 19, 27 y H9. Sus notas siguen calzando con la figura.

**Verificación:**
- las **196 anclas** de las notas ABR y ECochG existen en su figura;
- los 14 capítulos tocados se arman sin errores;
- el libro completo y los tomos se regeneraron.

## 2. Cambios en el motor del libro

| Archivo | Cambio |
|---|---|
| `figuras/motor/datos.py` | `CASOS_DEMO` apunta a `casos/pacientes_demo.json` y ya no a LabSim. |
| `figuras/hacer_figuras.py` | Si existe `casos/propios/<caso>.json`, se usa en vez de `casos/generados/<caso>.json`. Así, volver a correr `armar_casos.sh` no pisa un caso ajustado. |
| `ilustraciones/hacer_cap18.py` | Lee los pacientes de la copia del libro. Además se arregló un error: usaba `os` antes de importarlo y no corría. |
| `casos/pacientes_demo.json` | Nuevo: copia de `casos_antes/casos_demo.json`. |
| `casos/propios/*.json` (9) | Nuevos: copias de `casos_antes/generados/`. |

**Para llevar a LabSim:** los casos propios usan los umbrales ABR de antes del cambio. Es decir, los del adulto con la corrección vieja: click 10 y burst de 4 kHz 5. Llevarlos tal cual a LabSim significa cargarlos como casos fijos y no recalcularlos con `CaseProfile::project()`. Si se recalculan, vuelven a dar las figuras que no calzaban.

## 3. Grupo B: qué cambió en el texto y por qué

Las cifras son las de la marca de la figura (latencias) o las del caso (umbrales). Antes → ahora.

**Cap. 12.**
- **Esclerosis múltiple.** OD: I 1,20, III 3,33, V 5,90, que dan I-III 2,1, III-V 2,6 (antes 2,4) e I-V 4,7, ahora sobre el límite (antes "en el límite"). OI: III-V 2,6. A 81,1/s, la V del OD es 7,2 y se atrasa 1,3 ms.
- **AICA.** III del OD 4,0, V del OD 6,1, III-V 2,1; diferencia interaural 0,2. A 81,1/s, los dos oídos se atrasan 0,6 ms.
- **Glioma.** I-V del OD 4,6. A 40 dB aparece una V a 7,7 ms. A 81,1/s: OD 7,1 y OI 6,9.
- **Hipertensión intracraneal.** Amplitud de la I del generador 0,44. A 81,1/s, la V del OD es 6,9 (+0,6, 10 %).

**Cap. 13.**
- Neuropatía hereditaria: I 1,4, III 4,2, V 6,7.
- Kernicterus: el equipo rotula una III sobre un trazo plano. La nota aclara que no se separa del ruido.
- Leucodistrofia: la V es 6,7 y el I-V "llega a 5 ms" (antes "pasa de 5"); OI 4,9.

**Cap. 14.**
- **Tóxico-metabólico.** Umbral del click del caso 50 → **45 dB nHL**. III del OI 3,5, I-III 2,3. OD a 80 dB: V 5,8, III 3,7. OD a 60 dB: 6,4. Diferencia interaural 0,2 a 90 dB. El informe dice ahora que a 90 dB hay I en los dos oídos.
- **Hipotermia.** III 4,7, I-III 2,7, III-V 2,5, I-V 5,3. La regla de Markand da 5,1. A 40 dB: V 8,5, I 3,3.
- **Bloqueo proximal.** I a 1,4, 2,0 y 3,1 ms.

**Cap. 15, otitis crónica mixta.** Umbral del click del OD 70 → **65 dB nHL**, en la nota y en el razonamiento. Umbral óseo del OI cerca de 25 (antes 30).

**Cap. 17.**
- **Efusión.** I 2,17, III 4,23, V 6,37; 7,07 a 60 dB y 8,13 a 40 dB. El OI ahora también responde a 40 dB, así que el umbral queda en 40 en los dos oídos (antes "cerca de 60 en el OI"). Vía ósea: 6,53, 7,33, 8,47 y 8,63.
- **Rubéola.** Con click, la V aparece a 90 dB nHL y no solo a 100. Se dejó así a propósito: el cap. 17 dice que a esta edad **el click no se corrige**, y el texto anterior ("V solo a 100… con el click, unos 90") se contradecía con eso. Ahora calza: V a 90, 90 dB eHL. El burst de 500 Hz sigue solo a 100 (9,17 y 9,03 ms).

**Cap. 34, Ismael.** El burst de 4 kHz pasa a 80 / 75 nHL, que dan 70 / 65 eHL. La interpolación de 3 kHz da 52,5 / 50, los promedios 28 / 27,5, los porcentajes monoaurales 4,7 / 3,8 y la **AMA binaural 3,9 %**, con un rango de 0 a 12 %. Cuenta: (5 × 3,75 + 4,69) / 6 = 3,91. Esta tabla no es una figura, son datos del caso. Es lo que el roadmap ya preveía.

## 4. Observaciones que no toqué

1. **La ECochG de LabSim es muy sensible a 5 dB.** Con 5 dB más de sensación, las razones saltaban mucho: 0,43 → 0,17, 3,61 → 1,59, 0,24 → 0,43 y 1,98 → 4,64. En `mediciones_ecochg.txt` se ve por qué:
   - el PS se marca siempre 0,5 ms antes del PA;
   - la línea de base y el retorno se mueven mucho.

   En el libro ya no afecta, porque esos casos son propios. Pero conviene revisar `ecochg.auto_marks` en LabSim antes de crear allá casos de ECochG.
2. **El ruido de las figuras cambia con los datos del caso aunque la semilla sea la misma.** Por eso las marcas de ondas chicas saltaban hasta 0,5 ms.
3. **Cap. 12, esclerosis múltiple, V/I.** El texto dice 0,5, con la amplitud del generador. Medida en la figura, de pico a valle, da 0,7 a 0,8. Ya pasaba antes del cambio.
4. **Caso 17.2, CMV: I-V del OI de 4,2 ms "normal para su edad".** Para un lactante de 4 meses es corto, y el cap. 14 no tiene fila de 4 meses.
5. **Caso 15.3: ABR óseo del OD a 50 dB.** Hay una onda grande, sin rótulo, cerca de 6,8 ms, quizás la respuesta cruzada del OI. El texto no la comenta.
6. **Caso 11.5, microvascular.** El I-III del OD da 2,43 ms (antes 2,37) y la nota dice "alargado". Queda en el borde.
7. **`figuras/salida/h11_p33_ecochg.svg` está huérfana:** ningún capítulo la usa.

## 5. Cómo verificarlo

Desde la raíz del libro:

```bash
R=investigacion/revision_abr_ehl_2026-10-19

# Las figuras de los casos propios son las de antes, byte a byte
for f in $R/figuras_antes/*.svg; do cmp -s $f figuras/salida/$(basename $f) && echo "= $(basename $f)" || echo "≠ $(basename $f)"; done

# Latencias (y amplitud pico-valle) de una figura, antes → ahora, leídas del SVG
python3 $R/herramientas/medir_abr.py figuras/salida/cap12_glioma_tronco_abr.svg $R/figuras_antes/cap12_glioma_tronco_abr.svg

# Un capítulo: figuras cambiadas, notas, umbrales del caso y líneas con cifras de PEAT
python3 $R/herramientas/ver_capitulo.py capitulos/12-el-tronco.md

# Apéndice de cambios palabra por palabra contra el commit base
python3 $R/herramientas/apendice.py 0f07349
```

**Lo que debería dar la comparación byte a byte:** `=` en las 34 figuras de los casos propios, y `≠` en las del grupo B, que se quedan con la corrección nueva.

Las latencias y amplitudes del generador, con el caso de antes y el de LabSim, están en `mediciones_abr.txt`, y las de la ECochG en `mediciones_ecochg.txt`. Se sacan con `herramientas/ondas_abr.py` y `herramientas/marcas_ecochg.py`, usando el Python de LabSim.

**Ojo con la columna "ahora" si se vuelven a correr:** para los pacientes demo, `ondas_abr.py` usa ahora la copia del libro, que tiene los datos viejos.

## 6. Archivos de esta revisión

En `investigacion/revision_abr_ehl_2026-10-19/`:

| Archivo | Qué es |
|---|---|
| `INFORME_revision.md` | este informe |
| `apendice_cambios.md` | las 57 líneas cambiadas, con `[-antes-]{+después+}` |
| `mediciones_abr.txt` | marca y generador, por onda, antes → ahora, de las 61 figuras ABR (con los datos de LabSim) |
| `mediciones_ecochg.txt` | marcas y medidas de la ECochG, antes y ahora |
| `herramientas/` | `medir_abr.py`, `ver_capitulo.py`, `ondas_abr.py`, `marcas_ecochg.py`, `apendice.py` |
| `figuras_antes/`, `casos_antes/` | el respaldo del 2026-10-19, sin tocar |
