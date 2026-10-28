# Emisiones retiradas del tomo II (2026-10-21)

El autor pidió dejar las emisiones solo en los casos donde son obligatorias o indicadas, sin perder sus generadores.
Aquí está, por caso, cómo se pedían (el .py) y el bloque del texto tal como estaba. Los SVG siguen en `figuras/salida/` y la especificación de cada caso en `casos/<caso>.json` del commit ffd9dca.

Para devolverlas: agregar `fig.teoae(), fig.dpoae()` a la lista de figuras del caso en su .py y pegar el bloque `:::lado` en el Paso 4.

## cap05_p36

Figuras: `[{"tipo": "teoae"}, {"tipo": "dpoae"}]` (en el .py: `fig.teoae(), fig.dpoae()`)

Bloque del texto:

```
:::lado
:::figura cap05_p36 teoae
- OD: ausentes, con reproducibilidad de 15 %.
- OI: ausentes, con reproducibilidad de 4 %.
:::
:::figura cap05_p36 dpoae
- @OD 1000 | En el OD quedan productos de distorsión en 1, 1,5 y 2 kHz, donde la audición todavía es leve.
- @OD 4000 | Desde 3 kHz el DP se confunde con el ruido: quedan sin función las células ciliadas externas de la base.
- @OI 1000 | En el OI, 5 dB peor, no pasa ninguna frecuencia. Las emisiones confirman que el problema es **coclear** (→ H9).
:::
:::
```

## cap05_metabolica

Figuras: `[{"tipo": "teoae"}, {"tipo": "dpoae"}]` (en el .py: `fig.teoae(), fig.dpoae()`)

Bloque del texto:

```
:::lado
:::figura cap05_metabolica teoae
- OD: presentes en 2 de 5 bandas, con reproducibilidad de 60 %.
- OI: ausentes, con reproducibilidad de 7 %.
:::
:::figura cap05_metabolica dpoae
- @OD 2000 | En el OD pasan 1, 1,5 y 2 kHz; desde 3 kHz, nada.
- @OI 1000 | En el OI solo pasa 1 kHz. Como en Hernán, las emisiones se apagan donde empieza la pérdida: **coclear**.
:::
:::
```

## cap07_conmocion_laberintica

Figuras: `[{"tipo": "teoae"}, {"tipo": "dpoae"}]` (en el .py: `fig.teoae(), fig.dpoae()`)

Bloque del texto:

```
:::lado
:::figura cap07_conmocion_laberintica teoae
- OD: ausentes, con reproducibilidad de 6 %.
- OI: presentes en 2 de 5 bandas, con reproducibilidad de 36 %.
:::
:::figura cap07_conmocion_laberintica dpoae
- @OD 1000 | En los dos oídos el DP pasa solo en 1 kHz.
- @OD 2000 | Desde 1,5 kHz queda pegado al ruido: **1 de 7** en cada oído. La lesión está en las células ciliadas externas, donde está la pérdida.
- @OI 8000 | En 8 kHz el umbral se recupera hasta 50 dB, pero no tanto como para que vuelva la emisión.
:::
:::
```

## cap07_autoinmune

Figuras: `[{"tipo": "teoae"}, {"tipo": "dpoae"}]` (en el .py: `fig.teoae(), fig.dpoae()`)

Bloque del texto:

```
:::lado
:::figura cap07_autoinmune teoae
- OD: ausentes, con reproducibilidad de 0 %.
- OI: ausentes, con reproducibilidad de 0 %.
:::
:::figura cap07_autoinmune dpoae
- @OD 2000 | En el OD no hay DP en ninguna frecuencia: **0 de 7**.
- @OI 1000 | En el OI los puntos quedan apenas sobre el ruido y ninguno alcanza el criterio: también **0 de 7**. Con 25 a 45 dB de pérdida coclear, las emisiones ya se apagaron en el oído "bueno".
:::
:::
```

## cap08_post_radioterapia

Figuras: `[{"tipo": "teoae"}, {"tipo": "dpoae"}]` (en el .py: `fig.teoae(), fig.dpoae()`)

Bloque del texto:

```
:::lado
:::figura cap08_post_radioterapia teoae
- OD: ausentes, con reproducibilidad de 9 %.
- OI: presentes en 4 de 5 bandas, con reproducibilidad de 86 %.
:::
:::figura cap08_post_radioterapia dpoae
- @OD 2000 | En el OD no hay DP en ninguna frecuencia: **0 de 7**. Con la caja ocupada, el estímulo entra mal y la emisión no sale: esta DPOAE no dice nada de la cóclea.
- @OI 2000 | En el OI el DP está presente de 1 a 4 kHz, entre 0 y 10 dB SPL, y se pierde en 6 y 8 kHz, acorde a su edad: **5 de 7**.
:::
:::
```

## cap09_p38

Figuras: `[{"tipo": "teoae"}, {"tipo": "dpoae"}]` (en el .py: `fig.teoae(), fig.dpoae()`)

Bloque del texto:

```
:::lado
:::figura cap09_p38 teoae
- OD: presentes en los 5 bandas, con reproducibilidad de 94 %.
- OI: ausentes, con reproducibilidad de 11 %.
:::
:::figura cap09_p38 dpoae
- @OI 1000 | En el OI el DP está ausente en 1 y 1,5 kHz, donde el umbral está en 40 dB o peor.
- @OI 3000 | Desde 2 kHz aparece, con su máximo en 3 kHz, donde la audiometría es casi normal.
- Con **4 de 7** el equipo dice "pasa", pero el DP-grama dibuja la curva ascendente: las células ciliadas externas de los graves dejaron de amplificar.
:::
:::
```

## cap10_alport

Figuras: `[{"tipo": "teoae"}, {"tipo": "dpoae"}]` (en el .py: `fig.teoae(), fig.dpoae()`)

Bloque del texto:

```
:::lado
:::figura cap10_alport teoae
- OD: ausentes, con reproducibilidad de 0 %.
- OI: ausentes, con reproducibilidad de 0 %.
:::
:::figura cap10_alport dpoae
- @OD 2000 | Sin DP en ninguna frecuencia del OD (0 de 7).
- @OI 1000 | Tampoco en el OI, ni siquiera en 1 kHz, donde la pérdida es de 55 dB. La lesión está en la cóclea.
:::
:::
```

## cap30_mayor_ruido

Figuras: `[{"tipo": "teoae"}, {"tipo": "dpoae"}]` (en el .py: `fig.teoae(), fig.dpoae()`)

Bloque del texto:

```
:::lado
:::figura cap30_mayor_ruido teoae
- OD: presentes en 1 de 5 bandas, con reproducibilidad de 34 %.
- OI: presentes en 3 de 5 bandas, con reproducibilidad de 45 %.
:::
:::figura cap30_mayor_ruido dpoae
- @OD 4000 | Las emisiones bajan donde baja el audiograma: la cóclea explica la caída de agudos y no hace falta otra causa para ella.
:::
:::
```

## cap34_hidrops

Figuras: `[{"tipo": "teoae"}, {"tipo": "dpoae"}]` (en el .py: `fig.teoae(), fig.dpoae()`)

Bloque del texto:

```
:::lado
:::figura cap34_hidrops teoae
- @OD 1000 | El OD tiene emisiones en las cinco bandas.
- @OI 1000 | El OI no pasa ninguna: con 40 a 75 dB de pérdida en el rango de 500 a 4.000 Hz, las células ciliadas externas no funcionan. Coclear.
:::
:::figura cap34_hidrops dpoae
- OD: presentes en los 7 frecuencias, con L1/L2 de 65/55 dB SPL.
- OI: ausentes.
:::
:::
```

## cap34_honesto

Figuras: `[{"tipo": "teoae"}, {"tipo": "dpoae"}]` (en el .py: `fig.teoae(), fig.dpoae()`)

Bloque del texto:

```
:::lado
:::figura cap34_honesto teoae
- @OD 1000 | En el OD pasan 1.000 y 1.500 Hz y no 2.000 a 4.000; en el OI, solo 1.500 Hz. La reproducibilidad es baja (35 % y 24 %): vale la forma por banda, igual que el audiograma.
:::
:::figura cap34_honesto dpoae
- @OD 2000 | Los productos pasan hasta 2 kHz y no más allá: 3 de 7. Coincide con la caída del umbral.
:::
:::
```
