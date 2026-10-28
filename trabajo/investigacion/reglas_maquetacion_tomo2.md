# Reglas de maquetación del tomo II

Acordadas con el autor el 2026-10-20, sobre el cap. 23. Todas están en el código: este documento dice qué hace cada regla y dónde vive. **Desde el 2026-10-22 el tomo I (B, H) usa las mismas reglas** (`estilo_t2(cap)` en `hacer_libro.py`; `ESTILO_T2_TOMO1=no` las apaga). Los créditos de las imágenes del tomo I (B y H) salen del pie y van al mismo índice "Créditos de las imágenes" del final del tomo II. Falta convertir las figuras de los casos de H a los modelos del tomo II (hoja auditiva, impedanciometría, figuras del motor): hecho en H3 (casos H3.1, H3.3 a H3.6); el resto de las H sigue con `fig.audiograma()` y globos.

## 1. Letra (`herramientas/hacer_libro.py`, `TOMO2_CSS`)

Cada capítulo del tomo II va dentro de `<div class="tomo2">`.

| Elemento | Tamaño |
|---|---|
| Texto corrido | 9 pt (8,5 hasta el 2026-10-21) |
| Título del capítulo / sección / subtítulo | 25 / 14 / 11 pt |
| Recuadros (Sabías que, Ojo clínico, Ayuda memoria, Pasos, guía), tablas, pies de figura, leyenda de los números, rótulos | 7,7 pt (7,2 hasta el 2026-10-21) |
| Bibliografía | 7,2 pt (no sube) |

## 2. Texto a dos columnas (`capitulo()`: `dos_columnas`, `es_ancho`)

- Las secciones de teoría seguidas (Técnica, Fisiología, Patología, Razonamiento) son **un solo texto corrido**: el título de cada sección va dentro de la columna (`h2.en-columna`). No hay bloques de dos columnas cerrados uno sobre otro.
- Las figuras del texto van **dentro de la columna**, a su ancho, salvo las **apaisadas** (1,9 veces más anchas que altas o más, `APAISADA = 1.9`; una que no llega se fuerza con `:::imagen ruta ancho=… completa …`) y **todo dibujo SVG cuya letra, a ancho de columna (~83 mm), quedaría bajo 7 pt** (2026-10-21: "cualquiera con letras muy chicas"; hoy son todos los SVG de teoría): esas cortan las columnas y van a todo el ancho (2026-10-21: la 2.1, la 5.1 y la 8.1 no se leían en la columna). Solo cortan las columnas las fichas de caso y los recuadros `-ancho`.

## 3. Figuras

- **Leyenda de los números** (globos): va en el pie, en letra chica, con su numerito (`leyenda_globos`). No hay cuadros de explicación bajo la figura.
- **Créditos** (fuente, autores, licencia: "Imagen: …", "Imagen propia …"): salen del pie (`separar_credito`) y van al índice **"Créditos de las imágenes"** al final del tomo (`armado_incremental.creditos_html`).
- **Tamaños fijos de los casos:** hoja auditiva (`audiosupra`) e impedanciometría (`impedancia`) al 100 % (antes 80 %; ver más abajo); hexágonos de nistagmo al 55 %.
- **Calórica y vHIT:** el recuadro lleva la tabla de la calórica y la del vHIT lado a lado (la tabla del vHIT no se quita: trae los canales verticales).
- **Figuras del motor de los casos** (ABR, reflejos, VEMP, ECochG, emisiones): solas y centradas al 80 % (`div.tomo2 .figobs-motor`); en una fila van al ancho de su celda, pasadas a `<img>` (`caja('lado')`), porque el SVG en línea guardaba su alto y dejaba un hueco.
- **Emisiones:** solo en los casos donde son obligatorias o indicadas (tamizaje, lactante, neuropatía, cap. 14, pseudohipoacusia y simulación, ototoxicidad, niños que no responden, p39 retrococlear, TPA; y todo el cap. 6 y el cap. 29). Donde van, van las dos, TEOAE y DPOAE, **una debajo de la otra, cada una a todo el ancho** (2026-10-21: en una fila no se leían; probado en el caso 6.1, aprobado y llevado a todo el tomo): arriba la TEOAE (OD y OI) y abajo el DP-grama (OD y OI), 4 gráficos. El generador las hace compactas en el tomo II (`oae.dibujar_teoae/dibujar_dpoae(compacto=True)`): más bajas, letra en negro, ~9 pt impresa. Se probó el DP de los dos oídos en un solo gráfico y no gustó. `libro._figuras` no repite ninguna. Las retiradas están en `investigacion/emisiones_retiradas.md`, con su generador y su texto.
- **Logoaudiometría** (2026-10-21): el libro también se imprime, así que la letra de la figura impresa no baja de 7 pt. En el tomo II la curva sale compacta (`logo.dibujar(compacto=True)`, que `hacer_figuras.py` activa en los casos `cap*`): gráfico más chico y letra más grande (7,4 a 8,4 pt a media página). Dos curvas del mismo caso van en `:::lado ancho` (cada una a la mitad del ancho, con su alto proporcional); una sola, al 50 % (también la `:::figura … logoaudiometria` con globos, por CSS `fig-logoaudiometria`). Bajo 6 años la hoja auditiva queda sin panel: el audiograma centrado, del mismo tamaño.
- **Hoja auditiva para impreso** (aprobada el 2026-10-21 en el cap. 5 y propagada a todo el tomo el mismo día): `audiosupra` al 100 % del ancho; el audiograma clínico con toda la letra en negro (sin gris) y sin rótulos más chicos (3k, 6k, Fowler, LDL a 8); margen arriba más bajo si no hay Fowler; el panel de la derecha con ancho fijo (`ANCHO_PANEL = 400`), letra única para datos y notas, columnas juntas, medido con la fuente real (`svg.borde_derecho`) y escalado hasta llenar el ancho o el alto del audiograma (si sobra alto, crecen los espacios entre líneas). Impreso: audiograma de 76 × 85 mm y toda la letra ≥ 7 pt.
- **Impedanciometría para impreso** (aprobada y propagada el 2026-10-21): `impedancia` al 100 %, la misma idea: timpanograma con letra en negro a 7, panel a la derecha (`ANCHO_PANEL = 225`) escalado hasta el alto del timpanograma.
- **Citar figuras** (2026-10-21): `:::imagen ruta ancho=80% id=nombre Pie…` y en el texto `({{fig nombre}})`; el armado pone el número ("figura 7.1"), que no se desfasa si se mueve una figura, y avisa si se cita una que no existe. Toda figura se cita donde se usa.
- **Pies**: qué es y qué mirar. Nada de "otra persona, no el paciente", "la pide y la informa el médico" ni "se muestra para que se vea". Si la imagen ya trae letras (a, b, A…) o flechas, la explicación va en el pie por esas letras y no se le ponen globos encima.
- **Fila** (`:::lado` … `:::`): dos figuras, o una figura y una tabla, lado a lado (ya no las emisiones). Las figuras de una fila van a la misma altura (38 mm), sin el alto propio del SVG. Se usa para la **mariposa con el vHIT** y para el **vHIT con su tabla** cuando no hay calórica.

- **Tomo I: los tamaños del tomo II** (él, 2026-10-27, revisando el digital: "de aquí en adelante usar los tamaños del tomo 2"). Las figuras del motor que van en la columna de una H van a todo el ancho de la columna (~83 mm; `div.tomo2.tomo1 .dos-col .figobs-motor:not(.apaisada)`), no al 80 %: así el audiograma mide lo que el de la hoja auditiva (76 mm) y la logo compacta lo que la del tomo II a media página. Los audiogramas de los casos desde H4 van **unidos** (`fig.audiograma(combinado=True)`: los dos oídos en una grilla, como se hace una audiometría); los globos siguen funcionando. La logo y las emisiones de los casos de las H salen compactas, como en el tomo II (`hacer_figuras.py`, `tomo2` también para `h*`). Una figura del motor que debe ir a todo el ancho sin ser apaisada: `:::figura nombre tipo [n] completa` (H3.1).

## 4. Generadores del tomo II (`figuras/motor/`)

- `audio_supra.py` (`fig.audiosupra()`): audiograma clínico (frecuencias arriba, ósea completa de 250 a 4.000 Hz si una frecuencia la pide, "LDL:" en negrita subrayado y una sola vez por audiograma, Fowler (+)/(−) sobre la frecuencia, el oído sano de 20 en 20 desde su umbral) y, a la derecha, diapasones en espejo y logoaudiometría lado a lado; abajo, supraliminares (SISI, Carhart en 2 y 4 kHz "No det." hasta 5 dB, Metz con el reflejo pasado a dB HL, decay). Sin logo ni supraliminares bajo 6 años ni en un oído sin respuesta. En esta figura se enmascara la voz sobre 45 dB, "80 dB/60 dB" con el ruido en el color del otro oído.
- `impedancia_hoja.py` (`fig.impedancia()`): un timpanograma con las dos curvas ("OD curva A" / "OI curva B" en las esquinas), sus datos, reflejos por sonda (ipsi en el color del oído de la sonda, contra en el del otro; N/D sin reflejo), decay y función tubaria. Va en las pérdidas de transmisión o mixtas y donde el caso necesita el reflejo (asimétricas, retrococleares, Ménière); no donde el caso enseña que no se pone sonda.
- `ecochg.py`: área PS (clara) y área PA (oscura, dentro de la PS) sombreadas con las mismas cuentas de LabSim que la razón de áreas (`ecochg.area_shading`, Devaiah y Ferraro 2003); rótulo PS a la izquierda de su marca sobre la base y PA bajo el valle, para que no se tapen.
- `vestibular.py`: `nistagmo` (hexágonos con (−)), `mariposa`, `vng` (maniobras), `vhit` (dos gráficos, uno por oído; en cada uno la cabeza (gris) y el ojo (color del lado) van en sentidos opuestos: oído derecho, ojo arriba y cabeza abajo; oído izquierdo, cabeza arriba y ojo abajo; ganancia y sacadas en la mitad del ojo).

## 5. Paginador (`herramientas/acomodar.py`)

Se usa en el tomo y también en la prueba de un capítulo (`hacer_libro.py NN`), así la prueba sale como el tomo.

1. **El texto sube a los huecos:** si un bloque salta a la columna o página siguiente y deja un hueco al pie de la columna anterior (≥ 8 %, `HUECO_COL`), sube el párrafo o lista que lo sigue, unidad por unidad (hasta 40 vueltas). Mide el hueco **por columna**.
2. **Achicar para que quepa:** si aún queda hueco, achica la figura que saltó, o la de la página anterior (o todas un poco) para que suba lo que sigue. Mínimos: teoría 60 %, figuras de casos 75 %; la hoja auditiva y la impedanciometría no se achican nunca. Se acepta solo si el bloque sube y el capítulo no gana páginas.
3. **Fichas de caso:** la ficha (cara, nombre, anamnesis) no queda separada de sus Pasos 1-3: si no caben juntos, el caso empieza en la página siguiente. Salvo el **primer caso después de un título** ("Casos", 2026-10-21): ahí basta que la cabecera y la anamnesis queden juntas, así el caso empieza bajo el título y llena la página; si ni eso cabe, el título baja con el caso. El título nunca queda solo al pie.
4. **Guía del docente:** se parte entre páginas con "continúa →".
5. **Última página casi vacía:** aprieta la bibliografía para ahorrarla.

## 6. Cómo se trabaja

- Cada cambio se prueba primero en UN capítulo (`hacer_libro.py NN`, que ya pasa por el paginador) y la prueba se deja en `investigacion/prueba_paginas/`. Solo cuando el autor lo aprueba se lleva al resto del tomo.
- El tomo se arma (`hacer_libro.py --completo --tomo II`) solo cuando el autor lo pide.
- Antes de borrar algo del libro (figuras, generadores, texto), se guarda en `investigacion/`.
