# Revisión de errores: B05 y H24 (agente 03, 2026-10-22)

Leí completos los dos capítulos. Rehice con python/aritmética todos los cálculos (dosis, LEX,8h, VPP/VPN, incidencia, atenuación). No edité ningún archivo.

## Hallazgos

### GRAVE
Ninguno. No encontré normativa mal citada ni procedimiento que lleve a una decisión errada.

### IMPRECISO

- **[IMPRECISO] H24 l.498** — "un protector que protegería 30 dB, sacado media hora acumulada en un turno de 8, protege solo 15 dB (NIOSH, 1998)" → con la fórmula estándar A = -10·log10(f·10^(-A0/10) + (1-f)), f = 7,5/8 y A0 = 30 dB resultan **12 dB**, no 15. Un estudio de laboratorio alemán da el mismo caso (30 dB, 30 min de 8 h) como 12 dB (resumen de búsqueda; no abrí el original). Con 15 dB el tiempo sin protector sería unos 15 min. No pude abrir NIOSH 98-126 (la descarga devolvió HTML), así que no sé si NIOSH escribe 15 dB; si lo escribe, la cifra está mal en la fuente o mal copiada. Corrección: decir "unos 12 dB" o cambiar el ejemplo (por ejemplo, 10 min sin protector dejan unos 17 dB) y no atribuirlo a NIOSH sin cotejar.
- **[IMPRECISO] H24 l.493** — "NIOSH rebaja 70 % en los demás tapones (en su capítulo 6 el mismo documento dice 75 %)" → el valor de 25/50/70 % está confirmado en fuentes secundarias. La afirmación de que el capítulo 6 dice 75 % no la pude comprobar. Corrección: dejar solo 70 % o verificar la página antes de afirmar la discrepancia.

### DISCUTIBLE

- **[DISCUTIBLE] H24 l.106** — "la de 3 dB ... es la que usan la UE, Chile, Canadá y Australia" → Canadá tiene regulación provincial y federal que varía (algunas provincias usan 85 dB y 3 dB; otras 90 dB y 5 dB). Postura del texto: NIOSH 1998. Matiz: "Canadá" no es uniforme. Corrección: escribir "varias provincias de Canadá".
- **[DISCUTIBLE] H24 l.489-496 y l.503** — el texto aplica la fórmula NIOSH (rebaja por tipo y -7 dB en dB(A)) y presenta la de OSHA (50 %). Ambas son correctas y están bien atribuidas. Anoto que la norma ISO 4869-2 (SNR/HML) se cita en la bibliografía pero el texto no explica HML/SNR ni cómo se calcula con ellos. Es omisión, no error. Los objetivos del encargo mencionaban HML/SNR; el capítulo solo da NRR.

## Verificado con fuente (sin error)

- OSHA Apéndice F, tabla F-1 (hombres): 25 años = 3/5/7; 27 = 4/6/7; 32 = 5/7/10; 45 = 7/13/18; 47 = 8/14/19 dB (2, 3 y 4 kHz). Coincide con las tablas de H24 y con la pregunta 7. El ejemplo oficial (32 años, base a los 27, 4 kHz de 5 a 25, corregido 17 dB) coincide con el texto. Promedios del ejercicio de Jorge (38,3 / 8,7 / 29,7) correctos.
- Lie y cols. 2015 (PMC4415960): 12.055 trabajadores ferroviarios; en no expuestos, muesca de Coles 53 %, índice de muesca 51 %, muesca de 4 kHz 21 %. "Cerca de la mitad" es correcto para Coles e índice de muesca, pero no para la muesca de 4 kHz (21 %). Conviene precisar qué definición de muesca se usa (matiz menor).
- GES problema 77 (Superintendencia de Salud): 90 días de confirmación, audífono 90 días, implante 180 días, copago 0 % FONASA A-D y 20 % ISAPRE. Coincide con B05. No abrí las fichas 56 y 59.
- Cálculos B05: VPP 40 % y VPN 98,7 %; con 2 %, VPP 10,9 % (11 %); incidencia 300/7.600 = 3,9 %; índice de envejecimiento 83; AVAD 700; respuestas de las preguntas (33 %, 99,7 %, 15 %, 3,0 %, 50). Todo correcto.
- Cálculos H24: 4 h a 88 + 4 h a 82 = 125 % y 85,97 dB (86); 1.000 % = 95 dB(A); 82 dB = dosis de 50 %; 115 dB(A) = 28 s con 3 dB; 100 dB(A) = 15 min; 2,79 s a 135 dB(C) desde 95 dB(C) con 3 dB; 100 dB(A) con tapón NRR 30 derrateado = 92 dB(A); orejera NRR 25 = 88,25 dB(A); 80 dB(A) x 40 h = 1,6 Pa²h; pregunta 1 = 225 % y 88,5 dB(A).
- Cifras que coinciden con lo que conozco de las fuentes originales (de memoria, no abrí cada fuente): GBD 2019 (1,57 mil millones, 20,3 %, 2,45 mil millones en 2050, +56,1 %), OMS (430 millones, 34 millones de niños, 60 % evitable, retorno de casi 16 dólares por dólar), Neuhauser 2005 (7,4 %, 4,9 %, 1,4 %), Benjafield 2019 (936 y 425 millones, 17 estudios en 16 países), Lin y Ferrucci 2012 (1,4 por 10 dB, IC 1,3-1,5), NIOSH 1998 (riesgo excesivo 8 % a 85 y 25 % a 90 dB(A); derrateo 25/50/70 %; STS 15 dB en 500-6.000 Hz), OSHA (STS 10 dB promedio en 2-3-4 kHz, 14 h, aviso en 21 días, (g)(9), (j)(2) y (j)(3)), Directiva 2003/10/CE (80/85/87 dB(A); 135/137/140 dB(C)), Ley 16.744 art. 5 (fuerza mayor y carga de la prueba) y art. 71 (traslado), Ley 20.949 (25 kg y 20 kg), Doran 1981 (SMART original).

## No pude comprobar con fuente

- PREXOR: periodicidad por nivel (3 años, 2 años, anual, 6 meses), plazos de 1 año y 6 meses, dosis de 1.000 %, informe al mes, chequeo cada 3 años por debajo del criterio, cambios de nivel (45 dB HL), definición de incremento de 15 dB HL "que implique hipoacusia". La búsqueda web no entregó el texto. Matemáticamente 1.000 % = 95 dB(A) con 3 dB es coherente.
- Guía ISP 2026 (sensibilidad y especificidad, 80 % de oclusión por cerumen, reposo de 12 h, calibración semanal y semestral, método Carhart-Jerger modificado).
- D.S. 594: numeración exacta de artículos (arts. 71-81, 83-84, 110 a) y tabla de tiempos permitidos; el 2,79 s es coherente por cálculo.
- D.S. 44 (arts. 2, 7, 9, 67), D.S. 109 (arts. 16, 18, 19 n.° 12), Ley 4.055 de 1924 (incorporación de enfermedades profesionales), Circular 3G/40 (25 dB; 23,07 % de daño auditivo = 15 % de incapacidad), Circular B33/47, PEECCA.
- D.S. 14/2024 del MMA (publicado 27-02-2026) y D.S. 38/2011: solo el cálculo de fecha (30 meses desde 27-02-2026 = 27-08-2028) es coherente.
- TMERT v3 (Res. Ex. 1697), guía de manejo manual de carga (3 kg, 90/120 cm, 19-25 °C).
- Rink 1989 ("más de 70 %" menos STS con retest inmediato): no se leyó el original y no pude abrir NIOSH.
- NIOSH: reposo de 12 h, 6 meses sobre 100 dB(A), doble protección sobre 100 dB(A), rango 140-2.000 % de sobrestimación del NRR. No pude abrir el PDF.
- B05: fichas GES 56 y 59 (plazos de 45/30 días y 120/90/180 días), ENS 2016-17 (ya marcada), Ley 21.168 (fecha 27-07-2019), Ley 21.303 ("lengua oficial"), 65,8 % del Índice HAQ (GBD), cifra de ARIA 10-40 %, H.870 modo niños 75 dB(A), estudios de metales/solventes/estireno (Choi, Morata, Śliwińska-Kowalska), Pettersson 2012, Waters 2007 (35 lb).

## Conteo

- GRAVE: 0
- IMPRECISO: 2 (más un matiz menor sobre Lie 2015)
- DISCUTIBLE: 2 (una es omisión de HML/SNR)

B05: sin errores de conocimiento ni de cálculo hallados. H24: sin errores de procedimiento ni de normativa hallados con las fuentes que pude abrir; las dos imprecisiones están en la sección de protección auditiva.
