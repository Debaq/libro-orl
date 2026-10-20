# Reglas de maquetación del tomo II

Acordadas con el autor el 2026-10-20, sobre el cap. 23. Todas están en el código: este documento dice qué hace cada regla y dónde vive. El tomo I (B, H) no cambia con ninguna de ellas.

## 1. Letra (`herramientas/hacer_libro.py`, `TOMO2_CSS`)

Cada capítulo del tomo II va dentro de `<div class="tomo2">`.

| Elemento | Tamaño |
|---|---|
| Texto corrido | 8,5 pt |
| Título del capítulo / sección / subtítulo | 25 / 14 / 11 pt |
| Recuadros (Sabías que, Ojo clínico, Ayuda memoria, Pasos, guía), tablas, bibliografía, pies de figura, leyenda de los números, rótulos | 7,2 pt (mínimo) |

## 2. Texto a dos columnas (`capitulo()`: `dos_columnas`, `es_ancho`)

- Las secciones de teoría seguidas (Técnica, Fisiología, Patología, Razonamiento) son **un solo texto corrido**: el título de cada sección va dentro de la columna (`h2.en-columna`). No hay bloques de dos columnas cerrados uno sobre otro.
- Las figuras del texto van **dentro de la columna**, a su ancho. Solo cortan las columnas las fichas de caso y los recuadros `-ancho`.

## 3. Figuras

- **Leyenda de los números** (globos): va en el pie, en letra chica, con su numerito (`leyenda_globos`). No hay cuadros de explicación bajo la figura.
- **Créditos** (fuente, autores, licencia: "Imagen: …", "Imagen propia …"): salen del pie (`separar_credito`) y van al índice **"Créditos de las imágenes"** al final del tomo (`armado_incremental.creditos_html`).
- **Tamaños fijos de los casos:** hoja auditiva (`audiosupra`) e impedanciometría (`impedancia`) al 80 %; hexágonos de nistagmo al 55 %.
- **Calórica y vHIT:** el recuadro lleva la tabla de la calórica y la del vHIT lado a lado (la tabla del vHIT no se quita: trae los canales verticales).
- **Fila** (`:::lado` … `:::`): dos figuras, o una figura y una tabla, lado a lado. Las figuras de una fila van a la misma altura (38 mm), sin el alto propio del SVG. Se usa para la **mariposa con el vHIT** y para el **vHIT con su tabla** cuando no hay calórica.

## 4. Generadores del tomo II (`figuras/motor/`)

- `audio_supra.py` (`fig.audiosupra()`): audiograma clínico (frecuencias arriba, ósea completa de 250 a 4.000 Hz si una frecuencia la pide, "LDL:" en negrita subrayado, Fowler (+)/(−) sobre la frecuencia, el oído sano de 20 en 20 desde su umbral) y, a la derecha, diapasones en espejo y logoaudiometría lado a lado; abajo, supraliminares (SISI, Carhart en 2 y 4 kHz "No det." hasta 5 dB, Metz con el reflejo pasado a dB HL, decay). Sin logo ni supraliminares bajo 6 años ni en un oído sin respuesta. En esta figura se enmascara la voz sobre 45 dB, "80 dB/60 dB" con el ruido en el color del otro oído.
- `impedancia_hoja.py` (`fig.impedancia()`): un timpanograma con las dos curvas ("OD curva A" / "OI curva B" en las esquinas), sus datos, reflejos por sonda (ipsi en el color del oído de la sonda, contra en el del otro; N/D sin reflejo), decay y función tubaria. Va en las pérdidas de transmisión o mixtas y donde el caso necesita el reflejo (asimétricas, retrococleares, Ménière); no donde el caso enseña que no se pone sonda.
- `ecochg.py`: área PS (clara) y área PA (oscura, dentro de la PS) sombreadas con las mismas cuentas de LabSim que la razón de áreas (`ecochg.area_shading`, Devaiah y Ferraro 2003); rótulo PS a la izquierda de su marca sobre la base y PA bajo el valle, para que no se tapen.
- `vestibular.py`: `nistagmo` (hexágonos con (−)), `mariposa`, `vng` (maniobras), `vhit` (dos gráficos, uno por oído; en cada uno la cabeza (gris) y el ojo (color del lado) van en sentidos opuestos: oído derecho, ojo arriba y cabeza abajo; oído izquierdo, cabeza arriba y ojo abajo; ganancia y sacadas en la mitad del ojo).

## 5. Paginador (`herramientas/acomodar.py`)

Se usa en el tomo y también en la prueba de un capítulo (`hacer_libro.py NN`), así la prueba sale como el tomo.

1. **El texto sube a los huecos:** si un bloque salta a la columna o página siguiente y deja un hueco al pie de la columna anterior (≥ 8 %, `HUECO_COL`), sube el párrafo o lista que lo sigue, unidad por unidad (hasta 40 vueltas). Mide el hueco **por columna**.
2. **Achicar para que quepa:** si aún queda hueco, achica la figura que saltó, o la de la página anterior (o todas un poco) para que suba lo que sigue. Mínimos: teoría 60 %, figuras de casos 75 %; la hoja auditiva y la impedanciometría no se achican nunca. Se acepta solo si el bloque sube y el capítulo no gana páginas.
3. **Fichas de caso:** la ficha (cara, nombre, anamnesis) no queda separada de sus Pasos 1-3: si no caben juntos, el caso empieza en la página siguiente.
4. **Guía del docente:** se parte entre páginas con "continúa →".
5. **Última página casi vacía:** aprieta la bibliografía para ahorrarla.
