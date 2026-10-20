# LabSim metido en el cuerpo del texto (2026-10-19)

Búsqueda de párrafos que nombran LabSim o el simulador **fuera** de `## En LabSim`, de los recuadros y de la guía docente. Sin contar comentarios HTML ni preliminares. Total: ~90 párrafos.

Formato propuesto para reemplazarlos:

```
:::simulador
En LabSim: <qué hacer> y mira <qué error / qué cambia>.
:::
```

## A. Pierden el foco: narran reglas, castigos o comportamiento del simulador

Candidatos directos a recuadro de una línea, o a borrar si ya están en `## En LabSim`.

| Dónde | Qué hace | Propuesta |
|---|---|---|
| 01-antes-de-medir-el-conducto.md:29 | Falta grave, aviso en rojo, impedanciómetro bloqueado en los dos oídos. **Repite casi palabra por palabra H07:390** (que ya está en `## En LabSim`) | Quitar. Recuadro: "En LabSim: intenta timpanometría en el oído con otitis externa y mira qué pasa con el equipo." |
| 09-hidrops.md:61 y H11:160 | "un oído con razón 0,55 se mide 0,38 con pasa-alto 100 Hz y 0,08 en 200" | Recuadro: "sube el pasa-alto a 100 y 200 Hz y mira cómo desaparece el PS" |
| 13-oye-pero-no-entiende.md:55 | Casilla *Pinzar tubo* | Recuadro: "pinza el tubo en plena promediación y mira qué queda" |
| B04-fisica.md:356 | "en LabSim, 6 dB de umbral por cada mitad de barridos" | Recuadro: "parte los barridos a la mitad y mira cuánto sube el umbral" |
| 06-ruido.md:21 | TEOAE pasa con 3 de 5, DPOAE 4 de 7 | Recuadro: "con una muesca en 3-4 kHz, mira cómo la TEOAE pasa igual" |
| 04-rigidez.md:41 | "desde 10 dB de gap en el oído de la sonda el reflejo queda ausente" | Recuadro: "sube el gap de a 5 dB y mira cuándo se va el reflejo" |
| H12-vemp.md:250 | El ECM se cansa; "recupera la fuerza al doble de la velocidad" | Mecánica interna del modelo. A `## En LabSim` |
| H12-vemp.md:248 | Banda de EMG 30-150 µV | Dejar la idea clínica; el número a recuadro |
| H07-impedanciometria.md:252 | El recuadro amarillo de la gradiente | Describe la pantalla. A "Conoce tu equipo" o recuadro |
| 02-liquido-detras-del-timpano.md:59 | Gradiente en LabSim: A 0,58, C 0,50, Cs 0,35 | Recuadro: "compara la gradiente de un A, un C y un Cs" |
| 02-liquido-detras-del-timpano.md:82 | "LabSim usa la prueba de Williams…" | Abrir con la prueba, no con LabSim |
| H03-audiometria-tonal.md:276 | Vía ósea al final "porque es el orden que espera LabSim" | Justificar por la clínica o quitar la frase |
| 14-lo-que-mueve-el-abr-sin-ser-el-oido.md:50 | Cómo LabSim elige la fila normativa por edad | Recuadro o `## En LabSim` |
| 09-hidrops.md:102 | SISI "en LabSim, como en el audiómetro, a mano" | Quitar "en LabSim" |
| H11-electrococleografia.md:213 | Con burst "no las pinta en rojo" | Recuadro |
| H11-electrococleografia.md:217 | Límite de tasa 0,20 ms "sale del modelo y no de una serie publicada" | Número inventado en el cuerpo clínico. A recuadro o quitar |

## B. Botones, pestañas y menús de LabSim en el procedimiento

Interrumpen el paso a paso clínico. Juntarlos en "Conoce tu equipo" o en `## En LabSim`.

- H10:184 botón **AB** · H10:215 pestaña *Promediación* · H10:278 transductor en *Parámetros avanzados* · H10:289 pestaña latencia-intensidad
- H11:44 botón para invertir el eje · H11:136 A1/A2 y Fpz en parámetros avanzados
- H05:89 "las palabras se eligen en una ventana aparte" · H06:167 ventana *Comandos de voz*

## C. "LabSim no tiene / no simula" en el cuerpo

Avisos de lo que falta, sueltos entre la clínica. Juntar en un solo recuadro "Lo que el simulador no tiene" (ya existe en algunos capítulos) o al pie del capítulo.

- 08:375 · 09:135 · 09:424 · 19:49 · 24:54 · 33:178 · 34:274
- H01:417 · H08:96 · H11:22 · H11:223 · H13:79 · H21:280
- 26:182 · 26:272 (Rinne positivo "que da el simulador")

Estos explican de dónde sale una figura; sí hacen falta, pero como pie de figura o una línea al inicio de "Casos":
- 18:132 · 25:241 · 30:231 · 35:156 · 36:239 · 34:239 · 10:169 · B01:494

## D. Valores que el texto da como "los de LabSim"

Mezclan la norma clínica con el parámetro del simulador. Menos grave. El cuerpo da la norma con su cita; "LabSim usa X" va al recuadro.

- 04:25 · 04:72 · 04:82 · 02:39 · 03:45 · 12:19 · 17:43 · 18:70
- H07:131 · H07:266 · H07:275 · H09:208
- H10:12 · H10:206 · H10:223 · H10:344
- H11:90 · H11:94 · H11:95 · 09:40
- H12:99 · H12:100 · H12:102 · H24:455 · B04:184

## Bien puestos (no tocar)

- Las 32 secciones `## En LabSim`.
- Las figuras de "Conoce tu equipo" con la pantalla de LabSim (H03:173, H07:76, H09:90): dicen que la figura es de LabSim y siguen con el equipo en general.
