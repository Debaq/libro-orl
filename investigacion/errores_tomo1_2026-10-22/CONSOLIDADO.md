# Errores de procedimiento y conocimiento del tomo I: consolidado (2026-10-22)

15 agentes Sonnet leyeron completos B01-B05 y H01-H32 (~320 mil palabras) y contrastaron con Katz 7.ª ed., guías (BSA, ASHA, AAA, AAO-HNS, APTA, ATS/ERS, AASM, EAACI, NICE) y PubMed. Solo informe: no se tocó ningún capítulo. Detalle, fuentes y líneas en `agenteNN_*.md`; instrucciones en `INSTRUCCIONES.md`.

**Totales: 4 GRAVES (corregidos el 2026-10-22, ver abajo), ~100 IMPRECISOS, ~45 DISCUTIBLES.** Los graves se verificaron contra la fuente primaria; los imprecisos son lo que informó cada agente: el coordinador solo rehízo las cuentas de B04 l.373 y del pie de H26, y no ha verificado el resto.

### Verificación de los imprecisos (2026-10-22)

4 verificadores Sonnet volvieron a comprobar cada impreciso contra el texto actual y la fuente primaria (`verificacion_V1` a `V4`; cada entrada trae "texto actual → texto nuevo" y su fuente).

| | V1 (B, H1-3, H24) | V2 (H4-9) | V3 (H10-18) | V4 (H19-32) | Total |
|---|---|---|---|---|---|
| Confirmado | 12 | 14 | 11 | 17 | 54 |
| Parcial | 9 | 5 | 12 | 6 | 32 |
| Falso (descartar) | 4 | 1 | 3 | 11 | 19 |
| No verificable | 2 | 0 | 0 | 9 | 11 |
| Ya corregido | 0 | 1 | 2 | 0 | 3 |

Falsos que importan: los 4 de B01/B03 del agente 01 (FLM, Adibelli, áreas 41-42, Merchant), H10 III-V 3,64 (es de Rosa 2014), H16 muestreo 30-60 Hz (literal de Blakley y Chan), H14 postauricular (fiel a Matas), H25 Haight y Cole, H32 Doff 2013 (bien en la tabla). **H26, pie de `h26-rs-equipo`**: la cuenta 0,21 del coordinador era correcta con 0,38, pero la figura muestra la fosa izquierda con vasoconstrictor en 0,29 y con eso el total 0,18 cuadra; el error real es que el pie dice que la izquierda "no necesitaba la prueba".

### Aplicación (2026-10-22)

4 aplicadores Sonnet (`aplicado_A1` a `A4`) aplicaron 82 entradas confirmadas o parciales (A1 21, A2 19, A3 23, A4 22, algunas solo en parte) en los .md del tomo I; solo un comentario en H03.py. Casos, figuras y LabSim sin tocar. Referencias nuevas: Martin y Clark 2015 (H06), Welgampola y Colebatch 2001 corregida (H12), Atlas Vestibular 2009 (H17, año por confirmar con el impreso), Cole y Chasin 2015 e IEC 60318-5 (H22), Galli y Tsai 2012 (H29), AASM 1999 (H31).

Quedan abiertos:
- **Margen de +10 dB al mínimo** (Katz), agregado en H04: en la logoaudiometría deja sin ventana al paciente 41 de H5 (50-55 dB → 60-55) y a Clara del cap. 5 (40-45 → 50-45). Hay que decidir cómo se enseña: punto medio con la ventana conservadora, o confirmar con plateau.
- H31 STOP-Bang (falta sexo masculino o cuello > 40 cm) y Friedman 2004: aplicados solo en parte.
- H12: amplificación de 6 dB con ER-3A sin cita (falta la paginación de Wilber y Burkard 2015). H16: "HINTS plus" no agregado.
- H07: Carolina, el informe de ejemplo sigue diciendo 120 dB SPL en 4 kHz (solo se corrigió la anotación de la figura).

### Corrección de los graves (2026-10-22)

- **G1 H30**: conclusión del informe rehecha (CVF bajo el LIN; sin TLC no se descarta patrón mixto; la CVF que se normaliza tras el broncodilatador apunta a aire atrapado). Stanojevic 2022, coherente con la regla del propio capítulo (l.326).
- **G2 B01**: reclutamiento por pérdida de la compresión de las CCE. Fuente: Moore, *Cochlear Hearing Loss* 2.ª ed. (2007), pp. 109-110 (libro local); referencia agregada.
- **G3 H12**: título de la tabla y nota corregidos; el oVEMP de Li fue con golpe en Fz y filtro de 3-500 Hz. Comprobado en el texto completo (PMC4514573): n = 250 (cVEMP), 72,6 años, P13 13,8 (0,95), amplitud 1,25 (0,72), n10 7,70 (0,64), 13,86 (8,87) µV, hombres +0,38 ms.
- **G4 H04/H05 (+ cap. 5 del tomo II)**: 40 dB con supraaural y 60 con inserto, contra el mejor óseo de 250 a 4.000 Hz; mínimo = voz − AI + mayor gap; máximo = mejor óseo del evaluado + AI − 5. Yacullo 2015 (Katz cap. 6, pp. 81-82, 89-90, 103-105); se agregaron Konkle y Berry 1983 y Lidén 1959 a H05. Los 45 dB del protocolo quedan dichos como valor del SRT. Recalculados: H4 (paciente 42: mínimo 40), H5 (paciente 41: 50 a 55 dB), cap. 5 (Clara: enmascarar desde 50 dB; 40 a 45 dB). La pasada de la madrugada no se equivocó para el SRT: el 45 es correcto ahí; no lo es para el SDT ni la discriminación. No hay ningún procedimiento peligroso para el paciente. Las direcciones de giro y de nistagmo de H19 están todas bien (contra la guía AAO-HNS 2017 completa). Las cuentas de B04, H17, H26 y H31 salen bien salvo las señaladas.

## 1. Graves (confirmados en el texto por el coordinador)

| # | Dónde | Error | Corrección |
|---|---|---|---|
| G1 | H30 l.411 (informe de ejemplo) | "La CVF está sobre el LIN", pero la tabla (l.403) da CVF 3,30 L con LIN 3,44 L (z −1,88): bajo el LIN. Con razón y CVF bajo el LIN, la tabla de patrones del mismo capítulo da **mixto/posible restricción**, no obstructivo puro. | Corregir la frase y la conclusión (o cambiar los datos para que la CVF quede sobre el LIN). Los números de la tabla están bien (GLI-2012 recalculado). |
| G2 | B01 l.242 | "Las rampas llenas de líquido explican también el reclutamiento y la compresión". Los explica el amplificador coclear (CCE) y su pérdida; además contradice B03 l.127. | "La amplificación de las CCE explica la compresión; su pérdida, el reclutamiento (→ B2, B3, H6)". |
| G3 | H12 l.399-407 (tabla de referencia, fila Li 2015) | El título dice "tone burst 500 Hz, vía aérea", pero el oVEMP de Li se evocó con golpe en Fz (solo el cVEMP fue aéreo). Por eso su n10 es 7,7 ms (con sonido ~12,5 ms, Piker 2011). | Sacar la columna oVEMP de Li o rotularla "golpe en Fz". |
| G4 | H05 l.146-154; H04 l.51, 143, 167-169 | AI del habla = 45 dB contra el **promedio** óseo para decidir enmascarar la discriminación. Katz cap. 6 / ASHA 1988: 40 dB (supraaural) contra el **mejor** óseo 500-4000 Hz; con 45 queda una franja de 5-10 dB con curva sombra posible. | **Decide el autor**: la pasada de la madrugada (`verificar_tomo1_2026-10-22/agente7`) aceptó 45 como "48 de Yacullo redondeado, conservador". Si se cambia, rehacer H4.1, el caso Luis y la tabla. |

## 2. Imprecisos que conviene corregir primero

Errores de dato o contradicciones internas, fáciles de arreglar:

- **B04 l.373**: signos cambiados al mover la cabeza (a 1 m: acercarse 10 cm = +0,9 dB, alejarse = −0,8; el texto los invierte; igual a 0,5 m). Recalculado.
- **H26, pie de `h26-rs-equipo`**: total con vasoconstrictor 0,18; con 0,46 y 0,38 en paralelo da **0,21**. Recalculado.
- **H24 l.498**: protector de 30 dB sacado 30 min en 8 h → texto 15 dB, la cuenta da **12 dB** (falta confirmar si el 15 es de NIOSH).
- **H10, caso Sofía**: el pie dice que a 81,1/s no se ve la V en OI, pero el informe da V = 7,37 ms.
- **H10, tabla de Álvaro**: III-V límite 3,64 ms parece errata; Álvaro (12 semanas) comparado con norma de recién nacido.
- **H10, tone burst**: el .py usa ventana 20 ms y niveles 40/20/10; el texto dice 12 ms y 40/20.
- **H10**: una frase dice que la pérdida coclear alarga las latencias absolutas; la tabla del mismo capítulo dice "casi normales".
- **H07 l.263**: el contra con ruido a 95 dB SPL se equipara a "85 dB HL"; contradice l.248 (BSA: ~66 dB HL). Viene de LabSim.
- **H07 l.305 (Carolina)**: reflejo contra presente en 4 kHz a 120 dB SPL, sobre el tope del libro (114,5).
- **H07 l.320 / H09 l.327 (Benjamín)**: volumen OD 0,42 mL llamado normal; rango del capítulo para 5-7 años 0,7-1,3.
- **H08 l.88**: 3,8/√3 = ±2,2 dB, no ±2,7 (error heredado del ejemplo BSA).
- **H09 l.34, 256, 356**: neuropatía = "OEA + ABR ausente" sin exigir microfónica coclear.
- **H12, casos normales**: amplitud corregida 5,6-6,8 y EMG ~52 µV, fuera de la tabla del capítulo (1,25) y bajo el mínimo de 80 µV. Vienen de LabSim. Figuras de oVEMP con "corregida por EMG" cuando el texto dice que no se mide.
- **H12**: Welgampola y Colebatch 2001 citado con "clics"; la referencia es de tone burst.
- **H13**: falta que el artefacto del vibrador óseo aparece desde ~40 dB nHL; tensión entre "ABR ausente → no ASSR" y Rance 1998.
- **H03 l.434**: Luis no es "el paciente de la radiografía" (y el lado mixto no coincide); repetido en H03.py l.23.
- **H03 l.115**: ISO 389-7 (campo libre) citada para el cero de los fonos → ISO 389-1/-2/-3.
- **H03 l.226**: faltan en la instrucción "suelta cuando deje de sonar" y, en VO, "responde aunque lo oigas en el otro oído" (BSA 2018).
- **H04**: fórmulas sin el margen +10 dB al mínimo y −5 al máximo (Katz/Studebaker); con ellos el dilema con inserto queda **sin ventana** y el texto dice que hay.
- **H05 l.232**: llama SRT al 50 % de la curva de bisílabos (40 dB); el SRT de Raúl es 15. **H05 l.51**: detección 10 dB bajo el SRT vs 5 en los casos y 8-9 en l.42.
- **H06**: Rosenberg citado a Olsen-Noffsinger (falta Rosenberg 1958); Stenger sin el requisito de 20 dB de diferencia.
- **H15 l.391**: criterio "2 DE" sin "en al menos dos pruebas" (AAA 2010); Cranford 1990 es otro artículo.
- **H17 l.206**: límites 25/30 % sin exigir suma de VFL suficiente. **H17 l.163**: enseña calórica del canal posterior que el mismo capítulo dice sin respaldo.
- **H16 l.433**: HINTS sin la condición de nistagmo espontáneo ni el "plus" auditivo. **H18 l.95**: contraindicaciones sin patología cervical.
- **H19 l.122**: faltan estenosis carotídea y desprendimiento de retina. **H19 l.176**: supine roll 30 s vs "hasta que cese". **H19 l.138 vs l.57**: contradicción sobre el canal anterior.
- **H22 l.172, 185**: tubo HA-2 es rígido, 2 mm × 25 mm, no "flexible 1,5 cm" (Katz cap. 39; resuelve el `verificar`). **H22 l.48**: tubo fino con gancho estándar → HA-2. **B04 l.404 / H22 l.45**: el acoplador de 2 cm³ es IEC 60318-5.
- **H23 l.34**: faltan disparadores NICE y "considerar derivar" ≠ "derivar". **H23 l.44**: el pulsátil no es "casi siempre vascular".
- **H29 l.51, 125**: "histamina 0,1 % (10 mg/mL)": 10 mg/mL es 1 % (error que viene de Heinzerling). **H29 l.42**: la fase tardía no es independiente de IgE.
- **H30 l.229, 277**: regla "<0,100 L si FVC <1 L" es de 2005, no de Graham 2019.
- **H31 l.126**: STOP-Bang 3-4 incompleto (falta sexo masculino o cuello >40 cm). **H31 l.277**: cortes 5/15/30 citados a un artículo pediátrico. **H31 l.127**: Epworth ≥16 no está en Johns 1991.
- **H32 l.241**: cifras del grupo CPAP de Doff 2013 mal asignadas.

## 3. Decisiones del autor (fuentes que discrepan)

- AI con inserto: 55 dB (BSA, B04 y H04) vs 75 hasta 1 kHz y 50 sobre 1 kHz (Katz).
- Efecto de oclusión 15/15/10/0 vs 30/20/10 de Yacullo (ya anotado en la pasada anterior).
- ASHA vs BSA en audiometría: tono pulsado, frecuencias de VO, familiarización, repetir 1 kHz; VO al final de la batería.
- Tasa del ABR neurodiagnóstico: 21,1/s (libro) vs 11,1/s (BSA, Katz).
- Límites calóricos: 25/30 % (libro), 20/28 % (Atlas), 15 % (manuales chilenos). Arreflexia: agua helada (libro) vs 17 °C (protocolo del servicio).
- H08: parlantes a 45° vs 90° o frontal (BSA). H09: TEOAE pasa con 3/5 bandas vs "mayoría"/75 % (AAA).
- H14: filtro de la MLR, montaje, nº de desviantes en MMN, latencia de P300 (Katz vs texto).
- H19: lado del canal anterior por la torsión. H20: DVA a 2 o 3 Hz y 1 o 2 líneas.
- B01: edades de neumatización; áreas 41-42.

## 4. Problemas transversales

- **Pacientes de práctica de LabSim (demo 33-42) siguen en el tomo I**: H03, H11 (`demo(38)`), H21 (demo 36). Según la regla del autor deben salir del libro.
- **Errores que vienen de LabSim**: H07 (ruido contra), H12 (amplitudes y EMG de los normales), H27 (curvas de RinoSim). Corregir en el simulador, no solo en el texto (`LabSim/docs/limites_desde_el_libro.md`).
- **Muchos capítulos sin casos** (`CASOS = []`): H14-H20, H25-H32.
- **Libros locales escaneados sin texto** (no se pudieron buscar): *El sistema vestibular y sus alteraciones* I y II y *Handbook of CAPD*. Con OCR (`ocrmypdf`) servirían para una segunda pasada.
- **Sin comprobar contra el texto completo** (acceso cerrado): normativa chilena (PREXOR, ISP, D.S. 594/109, GES), ISO 389/8253 vigentes, ANSI S3.22 actual, Kushida 2008, Ramar 2015, Manual AASM v3, Stanojevic 2022, Sanfins 2026, Whitcroft 2023, entre otros (lista en cada informe).
- **Calidad dispar**: el agente 01 (B01, B03) no abrió los libros locales; sus 9 citas sin comprobar merecen otra vuelta.
