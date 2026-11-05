# Bitácora B2 (y pendientes de B3)

Fase actual: **producción**. Después: lectura y ajuste de la autora → verificación manual de referencias.

Prioridad de revisión: 🔴 alta (dato o cita escritos de memoria, sin verificar en línea) · 🟡 media (fuente verificada, pero la cifra o el matiz conviene leerlo en el original) · 🟢 baja (verificado en línea: autores, año, doi).

## Avance por sección

| # | Sección | Estado | Fecha |
|---|---|---|---|
| 0 | Apertura (objetivos, tabla de uso) | Redactada | 2026-11-05 |
| 1 | Oído externo y medio | Redactada | 2026-11-05 |
| 2 | Conducción ósea | Redactada | 2026-11-05 |
| 3 | Cóclea | Redactada | 2026-11-05 |
| 4 | Nervio y vía central | Redactada | 2026-11-05 |
| 5 | Desarrollo | Redactada | 2026-11-05 |
| 6 | Sistema vestibular | Redactada | 2026-11-05 |
| 7 | Nariz | Redactada | 2026-11-05 |
| 8 | Cierre (preguntas, respuestas, ayuda memoria final, créditos) | Pendiente | |

## Figuras pendientes (esquemas propios)

| Archivo | Sección | Qué debe mostrar |
|---|---|---|
| `ilustraciones/b2-resonancia-cae.svg` | 1 | Ganancia campo libre → membrana vs frecuencia (curva tipo Shaw 1974), pico ~3 kHz |
| `ilustraciones/b2-adaptador-oido-medio.svg` | 1 | Razón de áreas + palanca martillo/yunque |
| `ilustraciones/b2-arco-estapedial.svg` | 1 | Arco ipsi y contralateral con estímulo derecho |
| `ilustraciones/b2-mecanismos-co.svg` | 2 | Caminos de la vibración del cráneo a la cóclea (5 componentes) |
| `ilustraciones/b2-onda-viajera.svg` | 3 | Cóclea desenrollada, envolvente de la onda para 3 tonos |
| `ilustraciones/b2-transduccion.svg` | 3 | Haz en reposo/excitado/inhibido + célula (K⁺, Ca²⁺, glutamato) |
| `ilustraciones/b2-codificacion.svg` | 4 | Curvas de sintonía, bloqueo de fase, tasa vs intensidad (alta/baja actividad espontánea) |
| `ilustraciones/b2-ewald.svg` | 6 | Tres leyes de Ewald: lateral ampulípeto, vertical ampulífugo, curva asimétrica de disparo |
| `ilustraciones/b2-olfaccion.svg` | 7 | Cascada de transducción en el cilio + vía al bulbo y corteza piriforme |
| `ilustraciones/b2-binaural.svg` | 4 | DIT (graves) y DIN/sombra (agudos) con fuente a la derecha; oliva medial y lateral |

Al final: crear `material/ilustraciones/CREDITOS_B2.md`.

## Qué revisar (autora)

### Sección 1 — Oído externo y medio

| Prio | Qué | Detalle |
|---|---|---|
| 🔴 | Margolis y Goycoolea 1993 | Doi escrito de memoria; confirmar que el rango 800-1.200 Hz sale de ahí |
| 🔴 | Metz 1952 | Doi de memoria; confirmar criterio "< 60 dB entre umbral y reflejo" |
| 🔴 | Anderson, Barr y Wedenberg 1970 | Título, revista y doi de memoria; confirmar criterio de decay (> 50 % en 10 s, 500/1.000 Hz, 10 dB sobre umbral del reflejo) |
| 🔴 | Cerumen y umbral | Frase "el cerumen casi no mueve el umbral mientras queda una rendija" **sin cita**; buscar fuente o suavizar |
| 🔴 | Umbral normal del reflejo 70-100 dB HL | Sin cita |
| 🟡 | Shaw 1974 | Verificado; confirmar cifras (15-20 dB; concha ~5 kHz) en las curvas |
| 🟡 | Aibara 2001 | Verificado; confirmar "≈ 20 dB cerca de 1 kHz" |
| 🟡 | Pickles 2013 | Cifras de manual (99,9 % / 30 dB; 55 mm²; 3,2 mm²; 1,3; ≈ 27 dB): cotejar con la edición |
| 🟡 | Sadé y Ar 1997 | Verificado; "dos décimos de segundo" viene de una fuente secundaria que lo cita |
| 🟢 | Mukerji y cols. 2010 | Verificado |

### Sección 2 — Conducción ósea

| Prio | Qué | Detalle |
|---|---|---|
| 🔴 | Carhart: valores 5/10/15/5 dB | Una fuente secundaria los atribuye a **Carhart 1971** (capítulo de libro), no a 1950. Confirmar y ajustar la cita |
| 🔴 | Tonndorf 1966 | Asignación de cada mecanismo a graves/medios/agudos escrita de memoria |
| 🔴 | Tabla de atenuación interaural | Cifras de uso clínico sin cita primaria (ósea ≈ 0-15 dB; supraural ≈ 40; inserción ≈ 55-70). Sugerencia: citar un manual (p. ej. Gelfand, Essentials of Audiology) |
| 🔴 | Doi de memoria | Stenfelt y Reinfeldt 2007; Stenfelt 2012; Carhart 1950 |
| 🟢 | Stenfelt y Goode 2005 | Verificado (5 componentes; inercia de los líquidos la más importante) |

### Sección 3 — Cóclea

| Prio | Qué | Detalle |
|---|---|---|
| 🔴 | "CCE de la base más sensibles al estrés oxidativo" | Sin cita. Posible fuente: Sha y cols. 2001, Hear Res (vulnerabilidad basal vs apical a radicales libres) |
| 🔴 | "EOA desaparecen sobre unos 30-40 dB HL" | Sin cita específica |
| 🔴 | Hidrops: desplazamiento de la basilar hacia la rampa timpánica → PS grande | Mecanismo escrito de memoria, sin cita propia |
| 🟡 | Doi de memoria (alta confianza) | Greenwood 1990; Robles y Ruggero 2001; Glowatzki y Fuchs 2002; Wangemann 2006; Kemp 1978 |
| 🟡 | Detalles de transducción | Canales en la punta de los estereocilios cortos; ≈ 150 mV de fuerza impulsora (citado a Fettiplace 2017) |
| 🟡 | Eferente lateral: ACh, GABA, dopamina | Citado a Guinan 2006 |
| 🟡 | Moore 2007 | ISBN de memoria |
| 🟢 | Liberman 2002 | Verificado (40-60 dB sin prestina) |
| 🟢 | Fettiplace 2017; Guinan 2006 | Verificados |

### Sección 4 — Nervio y vía central

| Prio | Qué | Detalle |
|---|---|---|
| 🔴 | Generadores del PEAT | Tabla según Møller y cols. 1981 (título y doi de memoria). Coherente con B1 (onda IV = olivar). Confirmar en el original |
| 🔴 | "I-V ≈ 4 ms en el adulto" | Sin cita; remite a H10 para normas |
| 🔴 | Roll-over: Jerger y Jerger 1971 | Doi de memoria |
| 🔴 | Doi de memoria | Zatorre 2002; Litovsky 1999; ASHA 2005 |
| 🔴 | "Pérdida auditiva oculta" y fibras de baja actividad espontánea | Afirmación sin cita propia en B2 (sugerencia: Furman y cols. 2013, J Neurophysiol; Wu y cols. 2019 ya está en B3) |
| 🔴 | Tabla de estaciones (núcleo coclear dorsal = muescas espectrales; geniculado = atención) | Escrita de memoria, sin cita por fila; sugerencia: citar Pickles 2013 |
| 🟡 | DIT máxima ≈ 0,7 ms; teoría dúplex | Citado a Grothe 2010; confirmar la cifra |
| 🟡 | Lateralización hemisférica y ventaja del oído derecho | Citado a Zatorre 2002; la ventaja del oído derecho no tiene cita propia (Kimura 1961) |
| 🟢 | Liberman 1978; Johnson 1980; Grothe 2010 | Verificados |

### Sección 5 — Desarrollo

| Prio | Qué | Detalle |
|---|---|---|
| 🔴 | "PEAT adulto hacia los 2 años"; onda I casi adulta al nacer | Citado a Eggermont y Salamy 1988 (doi de memoria); confirmar cifras |
| 🔴 | Kei y cols. 2003 (1.000 Hz) | Autores y doi de memoria |
| 🔴 | "Intervención antes de los 6 meses" | Sin cita (JCIH); probablemente ya citado en cap. 16 |
| 🔴 | "Repetir EOA días después baja falsos positivos" | Sin cita en B2 (cap. 16 debería tenerla) |
| 🟢 | Moore y Linthicum 2007 | Verificado (ya en B3) |

### Sección 6 — Sistema vestibular

| Prio | Qué | Detalle |
|---|---|---|
| 🔴 | "≈ 90 potenciales/s en reposo" | Citado a Goldberg y Fernández 1971 (verificado el artículo, no la cifra) |
| 🔴 | Latencia del RVO ≈ 10 ms | Sin cita |
| 🔴 | Polarización: utrículo hacia la estriola, sáculo hacia afuera | De memoria; confirmar (Baloh 2011 o B3) |
| 🔴 | Tabla de VEMP (vías, músculo, inhibitorio/excitatorio) | Citada a Rosengren 2010 (verificado); confirmar detalle de vías |
| 🔴 | Ganancia normal del RVO "cercana a 1" | Sin cifra de corte; H17 debería tener normas |
| 🔴 | Doi de memoria | Raphan 1979; Halmagyi y Curthoys 1988; Angelaki 1999; Lopez y Blanke 2011; Baloh 2011 (ISBN) |
| 🔴 | "Sedantes vestibulares retrasan la compensación" | Sin cita propia (Lacour 2016 lo menciona en general) |
| 🟡 | Leyes de Ewald | Citadas a Baloh 2011 (manual, no verificado en línea) |
| 🟢 | Rosengren 2010; Lacour 2016; Goldberg y Fernández 1971 | Verificados (artículo) |

### Sección 7 — Nariz

| Prio | Qué | Detalle |
|---|---|---|
| 🔴 | "La nariz es la parte de la vía aérea que más se opone al paso del aire" | Sin cita |
| 🔴 | Válvula nasal (límites, colapso inspiratorio) | Sin cita; sugerencia: citar texto de rinología o B1 |
| 🔴 | Tabla de acondicionamiento del aire | Sin cita por fila |
| 🔴 | Vía olfatoria sin tálamo; corteza orbitofrontal | De memoria, sin cita; sugerencia: citar un manual de neurociencia |
| 🟢 | Pendolino 2018; Kahana-Zweig 2016; Kleene 2008; Buck y Axel 1991 | Verificados |

### B3 (de la revisión del 2026-11-05)

| Prio | Qué | Detalle |
|---|---|---|
| 🔴 | Lindsay y cols. 1953 | Sin resumen en línea; ver en fuente impresa (adherencias de Reissner en rubéola) |
| 🟡 | Lim 1968b | Estudio en animales; confirmar redacción "más gruesa que la parte tensa" |

## Pauta original de B2 (de Nicolás; se borra cuando todo esté cubierto)

### Para la autora: lo que pide el checklist de la carrera

> ✍ **Fernanda: el libro se cotejó contra el checklist de contenidos de las 14 asignaturas (2026-10-18/19). Lo que sigue lo pide la carrera y hoy solo lo cubre este capítulo**; el resto del libro lo usa y remite acá:
> - Transducción mecanoeléctrica en las células ciliadas (Morfofisiopatología; Otoneurología, "mecanismos de transducción").
> - Neurotransmisores e integración de señales bioeléctricas (Otoneurología).
> - Codificación de frecuencia, intensidad y tiempo en el nervio coclear y los núcleos cocleares (Otoneurología).
> - Procesamiento de la aceleración lineal (otolitos) además de la angular (Morfofisiopatología).
> - Fisiología de la olfacción (Morfofisiopatología); H28 trae la técnica y una base, pero la transducción olfatoria va acá.
> La anatomía de las vías ya está en B1 con las láminas de labyrinthus3d: conviene remitir a ellas en vez de dibujarlas de nuevo.

### Qué tiene que tener

#### Oído externo y medio
- Resonancia del conducto y del pabellón; qué pasa cuando el conducto se ocluye (→ cap. 1).
- Adaptación de impedancia del oído medio: razón de áreas, palanca de la cadena; por qué la rigidez pesa en los graves y la masa en los agudos (→ H7, cap. 3, cap. 4; la física, en B4).
- Función de la trompa: ventilación, drenaje, protección; qué pasa con la presión cuando no abre (→ cap. 2, H7).
- Reflejo estapedial: arco ipsi y contralateral, umbral, decay (→ H7, cap. 11).

#### Conducción ósea
- Los tres mecanismos (compresión, inercia de la cadena, radiación al conducto) y el efecto de oclusión (→ H2, H3, H4).
- Atenuación interaural y por qué la ósea cruza casi entera (→ H4, cap. 7).
- Por qué la ósea cae en la otoesclerosis sin daño coclear (muesca de Carhart) (→ cap. 4, cap. 15).

#### Cóclea
- Onda viajera y tonotopía; por qué la base (agudos) se daña primero (→ cap. 5, cap. 6, cap. 8).
- Células ciliadas externas: electromotilidad y amplificador coclear; sensibilidad y sintonía fina (→ H9, cap. 6).
- Transducción mecanoeléctrica, paso a paso: deflexión de los estereocilios, enlaces apicales, canal de transducción, entrada de K+, despolarización, liberación de glutamato; adaptación del canal; lo mismo en las células del vestíbulo (polarización hacia el cinocilio). Hoy cap. 10 ("el detalle de la transducción está en B2") y cap. 9 remiten acá (→ cap. 6, cap. 9, cap. 10).
- Células ciliadas internas: sinapsis en cinta y fibras del nervio (tipo I y II); sincronía neural (→ cap. 13).
- Neurotransmisión: glutamato en la sinapsis aferente; acetilcolina y GABA en las eferentes; glutamato, GABA y glicina en los núcleos vestibulares; potencial de acción, mielina y velocidad de conducción (→ cap. 12, cap. 13, cap. 30).
- Sistema eferente olivococlear medial y lateral: qué hace sobre las CCE, protección y escucha en ruido (→ H9, que trae la supresión contralateral de las EOA; B1 da la vía).
- Potencial endococlear y estría vascular; homeostasis del potasio y conexina 26 (→ cap. 9, cap. 10; la histología, en B3).
- Potenciales cocleares: microfónica, potencial de sumación, potencial de acción (→ H11, cap. 9).
- Emisiones otoacústicas: de dónde salen y qué dicen (→ H9).
- Reclutamiento y campo dinámico; adaptación (→ H5, H6).

#### Nervio y vía central
- Codificación de frecuencia, intensidad y tiempo en el nervio: código de lugar y de ritmo, bloqueo de fase y su límite en frecuencia, fibras de alta y baja actividad espontánea y rango dinámico, sumación por población; adaptación neural (→ H6, cap. 11, cap. 13, cap. 30).
- Núcleos cocleares ventral y dorsal, complejo olivar, lemnisco, colículo, geniculado y corteza: qué hace cada estación (tonotopía conservada, áreas secundarias, lateralización hemisférica) (→ H15, cap. 12; la anatomía, en B1).
- Audición binaural y localización: diferencias interaurales de tiempo (oliva superior medial) y de nivel (oliva superior lateral), rango de frecuencias de cada pista, sombra de la cabeza, efecto de precedencia, análisis de la escena auditiva y efecto cóctel (→ H15, cap. 30).
- Generadores de las ondas I a V del PEAT; latencias e interpicos; maduración y mielinización en el lactante (→ H10, cap. 14, cap. 17).
- Procesamiento central del habla; por qué la discriminación cae más en lo retrococlear (→ H5, cap. 13).
- Procesamiento auditivo central: resolución y ordenamiento temporal, interacción binaural, escucha dicótica, separación figura-fondo; maduración hasta la adolescencia (→ H15).

#### Desarrollo
- Oído del recién nacido: vérnix, mesénquima y líquido en el oído medio las primeras horas (→ cap. 16); maduración del oído medio y del tronco (→ cap. 17).

#### Sistema vestibular
- Canales semicirculares (aceleraciones angulares) y otolitos (lineales y gravedad); actividad de reposo y asimetría (→ H16).
- Dinámica de la cúpula: por qué el canal se comporta como integrador de la aceleración (modelo de péndulo de torsión), constante de tiempo y almacenamiento de velocidad; leyes de Ewald (→ H17, H18, H19).
- Fisiología macular: estriola y polarización opuesta de las células, inclinación frente a traslación, reflejos otolíticos (contrarrotación ocular, vertical visual subjetiva), integración canal-otolito (→ H12, cap. 20, cap. 22).
- Reflejo vestíbulo-ocular: ganancia, fase; por qué el nistagmo bate hacia el lado más activo (→ H16, H17, H18).
- Vías vestíbulo-cólica (cVEMP) y vestíbulo-ocular (oVEMP); sáculo y utrículo (→ H12, cap. 20).
- Mecanismo del VPPB: canalitiasis y cupulolitiasis (→ H19).
- Reflejos vestíbulo-espinal y vestíbulo-cólico: vías lateral y medial, control postural (→ H20, cap. 32).
- Vías vestibulares centrales: núcleos, cerebelo (flóculo y nódulo), tálamo y corteza vestibular (región insular posterior); percepción de la vertical y del movimiento propio, integración multisensorial (→ cap. 25, cap. 27).
- Compensación central, adaptación y sustitución: la base de la rehabilitación (→ H20).

#### Nariz
- Ciclo nasal, resistencia al flujo y válvula nasal; mucosa y respuesta al vasoconstrictor (→ H25-H27).
- Acondicionamiento del aire: calentamiento, humidificación, filtrado y depuración mucociliar; papel de los cornetes y del flujo sanguíneo de la mucosa (→ H25, cap. 36).
- Olfacción: hendidura olfatoria, transducción en la neurona receptora, bulbo, vía y corteza olfatoria; por qué la obstrucción nasal quita el olfato (→ H25, cap. 35).
