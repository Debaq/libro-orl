# Informe: revisión del libro después de la corrección nHL → eHL nueva de LabSim

Fecha: 2026-10-20. Nada de esto tiene commit todavía. Se compara contra el commit `51fbdad`, que restauraba datos viejos y quedó descartado (ver más abajo, "Lo que se descartó").

## Criterio, decidido por él

- **El caso clínico no se mueve.** Lo que no puede cambiar es lo que el caso enseña.
- **Los casos se quedan con la corrección nueva.** Nunca se vuelve a los datos viejos: eso reintroduce el error que la corrección arreglaba.
- **Si los datos nuevos sostienen el caso, se quedan** y se actualizan las cifras del texto.
- **Si el caso se cae**, se ajusta un parámetro propio del caso, en una copia del libro, sin tocar la tabla de corrección.

## Qué se hizo

### 1. Tres casos que se caían

Se ajustó un parámetro del caso en cada uno; la corrección queda intacta.

| Caso | Qué se caía | Ajuste | Lo que muestra la figura |
|---|---|---|---|
| 23.2, Ménière bilateral | La ECochG del OI salía normal (0,17 / 1,06) y se caía el "bilateral". | OI `ecochg.sp_ap` de 0,28 a **0,64** (`casos/propios/cap23_meniere_bilateral.json`). | OI con PS/PA 0,45 y áreas 2,43: los dos sobre el límite. |
| Patricia (caso 9.1, H11) | La razón de áreas daba 1,59 y se perdía el PS prolongado del informe de H11. | OI `ecochg.sp_ap` de 0,55 a **0,63** (`casos/pacientes_demo.json`, paciente 38). | OI con PS/PA 0,63, áreas 3,87 y retorno a la base a 8,8 ms. |
| 9.2, OD cofótico | El marcado automático ponía PS y PA sobre ruido (−5,24). | Regla nueva en el motor (`figuras/motor/ecochg.py`), ver abajo. | "Sin respuesta identificable". |

**La regla del motor.** Es la misma que ya se usa en el ABR: no se marca sobre ruido. Si el PA mide menos de 0,1 µV o la razón da negativa, la figura dice "Sin respuesta identificable". Los PA reales de los casos del libro miden de 0,4 a 3 µV. Solo cambia la figura del OD del 9.2.

**Caso 17.2, CMV.** El generador sigue poniendo la V del OD a 60 dB con burst de 500 Hz, pero el ruido la tapaba. No se tocó el caso, sino la figura: niveles de 80 a 20 dB y 3.000 barridos (`casos/cap17_cmv_congenito.json`). Así se ve la V a 80 dB y una V chica a 60.

### 2. Casos propios del libro

- **`casos/pacientes_demo.json`**: copia de los pacientes demo de LabSim, con la corrección nueva. Su único cambio es el OI de Patricia. `figuras/motor/datos.py` e `ilustraciones/hacer_cap18.py` leen esta copia.
- **`casos/propios/<caso>.json`**: si existe, manda sobre `casos/generados/` (`figuras/hacer_figuras.py`). Hoy solo está el Ménière bilateral.
- **Para LabSim:** hay que llevar a LabSim estos dos ajustes de `sp_ap` y la regla de no marcar sobre ruido. Esa regla sería mejor ponerla en `ecochg.auto_marks`.

### 3. Los demás casos

Siguen con la corrección nueva y se actualizaron las cifras del texto. Son **75 líneas en 10 capítulos** (9, 11, 12, 13, 14, 15, 17, 18, 23, 34, H10 y H11), detalladas palabra por palabra en `apendice_cambios.md`.

Los casos donde el texto cambia más que una cifra:

| Caso | Cambio |
|---|---|
| **H10, Raúl** | I-III 2,6 y III-V 2,3, en el borde. El I-V de 5,0 y la diferencia interaural de 0,8 ms sostienen el patrón retrococlear. |
| **Caso 11.1** (el mismo paciente) | Diferencia interaural de 0,8 ms. |
| **Siderosis** | A tasa alta la V se atrasa 0,5 ms en el OD y 1,3 ms en el OI. Las marcas son inestables y la nota lo dice. |
| **Colesteatoma** | Hay una V chica en el OD a 50 dB por vía ósea, en su umbral. |
| **Rubéola** | La V con click aparece a 90 dB. Calza con la regla del cap. 17 de que a esa edad el click no se corrige. |
| **Ismael** | La AMA queda en 3,9 %. |
| **Cap. 18, ilustración del promedio** | El FSP llega a 3,1 con 1.000 barridos. |
| **Caso 23.4, logoaudiometría del OI** | Nota reescrita a pedido suyo: la curva corrida unos 30 dB y el roll-over leve (96 → 83 %, índice 0,14). |

### 4. Verificación

- Las **1.094 anclas** de todas las figuras de los capítulos existen en su SVG.
- Los 14 capítulos tocados se arman sin errores.
- Por pedido suyo, el libro completo **no se volvió a armar**: se arma cuando esté todo resuelto.

## Lo que se descartó

Se descartó el commit `51fbdad`, que devolvía casos y pacientes demo a los datos de antes de la corrección. Eso reproducía las figuras viejas, pero con la tabla de corrección vieja.

## Observaciones que no toqué

1. **El marcado automático de la ECochG de LabSim es caótico.** Cambiar `sp_ap` en 0,01 puede mover la razón medida de 0,15 a 0,55. Los valores elegidos son los que reproducen el caso, pero conviene revisar `ecochg.auto_marks` en LabSim.
2. **El ruido de las figuras cambia con los datos del caso aunque la semilla sea la misma.** Por eso las marcas de ondas chicas saltan hasta 0,5 ms.
3. **Cap. 12, esclerosis múltiple:** el texto dice V/I de 0,5 (amplitud del generador), pero en la figura, medido de pico a valle, se ve de 0,7 a 0,8.
4. **Caso 17.2:** el I-V del OI de 4,0 ms es corto para un lactante de 4 meses.
5. **`figuras/salida/h11_p33_ecochg.svg` está huérfana:** ningún capítulo la usa.

## Cómo verificarlo

Desde la raíz del libro:

```bash
R=investigacion/revision_abr_ehl_2026-10-19
python3 $R/herramientas/ver_capitulo.py capitulos/12-el-tronco.md      # figuras, notas y umbrales de un capítulo
~/micromamba/envs/labsim/bin/python $R/herramientas/ajustar_ecochg.py cap23_meniere_bilateral 'OI.ecochg.sp_ap=0.64'
python3 $R/herramientas/apendice.py 51fbdad                            # cambios de texto palabra por palabra
```

Las mediciones de antes y después están en `mediciones_abr.txt` y `mediciones_ecochg.txt`.
