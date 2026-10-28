# Agente 3: H12 (VEMP) y H13 (ASSR), parámetros de configuración

## H13 (nueva sección "Los parámetros de configuración", antes de "Paso a paso")
- Tabla `:::ayuda-ancho Configuración de un ASSR` (Parámetro | Valor de rutina | ¿Lo cambias tú? | Por qué) y lista numerada de 10 puntos con lo que pasa al cambiar cada uno: portadoras, ritmo de modulación, tipo/profundidad, nivel de partida y pasos, criterio de detección (95/99 %), ruido residual, filtros, rechazo de artefactos, tiempo máximo, dB nHL/eHL. Recuadro "Lo que dicen las normas".
- Hallazgo: la BSA (2023, §4.1) dice que el estímulo no se modifica salvo la familia 40/90 Hz. Lo que sí se ajusta: pasos de nivel, criterio 95/99 %, rechazo, tiempo máximo, tabla de corrección. Filtros: no hay control; Katz dice que el corte importa poco porque la FFT actúa como filtro angosto.
- Paso 1 retocado (una frase) para que no contradiga la sección.
- Fuentes leídas: BSA 2023 (§4, 7.1-7.3, 7.7, preguntas A3, A4, A6, apéndice E); Dimitrijevic y Cone, cap. 15 de Katz 7.ª ed. (nueva entrada en Referencias, p. 267-93, páginas finales por confirmar); manual de instrucciones de un fabricante (2011, solo para el tiempo de 6 min).
- `decide el autor`: tabla sale de BSA y Katz, el protocolo ORL solo nombra los 3 protocolos; "unos 6 min" de tiempo máximo sale de un manual de fabricante.
- `verificar`: frecuencias de corte exactas de filtros por equipo; ASHA, Hall 2007 y Picton 2003 no se leyeron para esta sección.

## H12
- Tabla existente: se agregaron 4 filas (duración del burst, contracción/EMG, rechazo de artefactos, impedancia máxima).
- Lista numerada de 12 puntos "Cada parámetro tiene su razón": nivel, frecuencia del burst, duración y subida, tasa, filtros, ganancia, ventana, barridos, contracción y su banda, rechazo, impedancia, polaridad.
- Fuente: Rosengren y cols. 2019 (texto completo leído en PMC): rutinas de filtro, ganancia, pre-estímulo, duración hasta 6 ms, nivel 95 dB nHL, contracción mínima 80 µV, tasa >10/s.
- `decide el autor`: banda de EMG 30-150 µV es de LabSim; polaridad (punto 12) es inferencia.
- `verificar`: el consenso no da nivel de rechazo en µV para VEMP ni efecto de la polaridad; no se inventó cifra. Frases sobre saturación del convertidor y filtros cerca de la frecuencia de la respuesta son razonamiento, no cita. Ganancias del protocolo (5.000/10.000) difieren de Rosengren (2.000/20.000).
- Sin referencias nuevas en H12 (todo lo citado ya estaba).

No se tocaron casos, figuras, otros capítulos, ni se hizo commit ni PDF.
