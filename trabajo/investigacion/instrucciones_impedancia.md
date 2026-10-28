# Impedanciometría en los casos del tomo II

Libro de ORL para tecnólogos médicos, español de Chile. Desde 2026-10-20 los casos del tomo II (caps. 1-36) usan la **hoja de impedanciometría** `fig.impedancia()` (generador `figuras/motor/impedancia_hoja.py`): un timpanograma con las dos curvas (en las esquinas "OD curva A", "OI curva B"), sus datos (volumen, compliancia, presión, gradiente), los reflejos **por sonda** (sonda OD: ipsi en rojo y contra en azul; sonda OI: ipsi en azul y contra en rojo; en dB SPL; N/D si no hay reflejo), el decay del reflejo y la función tubaria. Con lactantes se pide `fig.impedancia(sonda=1000)`. El tomo I (B, H) no se toca.

## Tarea 1: agregar la hoja donde falta y corresponde
Regla del autor: **"solo transmisión y reflejos"**. Lleva hoja de impedanciometría todo caso con audiometría que:
1. tenga una pérdida **de transmisión o mixta** (gap aéreo-óseo), o
2. **necesite el reflejo**: pérdida asimétrica o unilateral (descartar lo retrococlear con reflejo y decay), sospecha retrococlear, Ménière/hidrops (Metz), o el texto del caso discute reflejo, Metz, decay u oído medio.
No la lleva una pérdida simétrica (presbiacusia, ruido) ni una audición normal si el caso no discute el reflejo.

En los casos de tus capítulos que hoy **no** tienen `fig.impedancia()` (lista abajo), decide con esa regla. Si va:
- En el `.py`, agrega `fig.impedancia()` a la lista de figuras del caso (después de `fig.audiosupra()`). No cambies nada más del pedido del caso.
- En el `.md`, agrega en el Paso 4 (resultados), después del bloque de la audiometría:
  ```
  :::imagen figuras/salida/<caso>_impedancia.svg ancho=100% Impedanciometría de <nombre>.
  :::

  <1 o 2 frases que leen la hoja con sus números>
  ```
- Rehace las figuras (`cd herramientas && python3 solo_figuras.py ../capitulos/NN-*.py`) y **lee los valores del SVG** (`grep -o '>[^<]*<' figuras/salida/<caso>_impedancia.svg`). El texto dice lo mismo que la hoja. Si la hoja contradice el caso (p. ej. curva B en un oído que el caso describe sano), no inventes: avísame en el informe.
- Si hay un informe de la resolución con audiometría, agrega "**Impedanciometría:** …" en una frase.

## Tarea 2: pulir los párrafos de impedancia que ya están
Los timpanogramas y reflejos que ya estaban se pasaron a la hoja con un script: el texto bajo cada `:::imagen …_impedancia.svg` viene de las notas de los globos y quedó con frases forzadas ("En el OD, …", "Con la sonda en el OI, en el contralateral, …" pegado a frases que no hablan de esa celda). Reescríbelos en prosa natural, frases cortas, sin perder datos ni conclusiones, y verifica que digan lo que muestra la hoja: con la sonda en un oído se mide su ipsi y su contra (el contra estimula el otro oído). Sin "@", sin listas numeradas, sin globos.

## Reglas
- Español de Chile, frases cortas, como el resto del libro. Mantén las remisiones (→ H7).
- No armes PDF, no hagas commits, no toques capítulos ajenos ni el tomo I.
- Al terminar: todas las rutas `:::imagen` existen.

## Informe final (corto)
Por capítulo: casos a los que agregaste la hoja y por qué; casos que dejaste sin hoja y por qué; párrafos pulidos; contradicciones entre la hoja y el caso.
