# H10. Potenciales evocados auditivos de tronco

:::objetivos En esta herramienta
- Explicar de dónde sale cada onda del ABR y por qué hay que promediar miles de barridos para verla.
- Preparar al paciente, montar los electrodos y configurar el equipo sabiendo para qué sirve cada parámetro.
- Buscar el umbral de la onda V con click y con estímulos por frecuencia, y llevarlo de dB nHL a una estimación en dB HL.
- Medir latencias, interpicos y diferencia interaural, y reconocer los patrones conductivo, coclear, retrococlear y de neuropatía.
- Saber qué puede y qué no puede decir un ABR por vía ósea y un AABR de tamizaje.
- Reconocer los artefactos que se disfrazan de onda, incluida la falsa onda V.
:::

Los potenciales evocados auditivos de tronco (PEAT, PEATC o BERA; en inglés *auditory brainstem response*, **ABR**) son la respuesta eléctrica del nervio auditivo y del tronco cerebral a un sonido breve. No piden nada al paciente: puede estar dormido, sedado o ser un recién nacido. Por eso son el examen que responde cuando la audiometría no puede, y el que mira más allá de la cóclea cuando la audiometría no alcanza. A cambio, exigen técnica: la respuesta es tan chica que, mal registrada, cualquier ruido parece una onda.

## Para qué sirve

El ABR responde tres preguntas distintas, y cada una se hace de otra manera:

1. **¿Hasta qué intensidad responde la vía?** Es la búsqueda del **umbral de la onda V**: la intensidad más baja a la que la onda V aparece y se repite. Se usa para estimar la audición de quien no puede hacer una audiometría confiable: lactantes, niños pequeños, personas con discapacidad cognitiva y quienes exageran o simulan una pérdida (→ cap. 17 y 19).
2. **¿La señal viaja a tiempo?** Es el ABR **neurootológico**: a una intensidad alta se miden las latencias y los intervalos entre ondas para buscar un retraso en el nervio o en el tronco, como el de un schwannoma vestibular o una esclerosis múltiple (→ cap. 11 y 12).
3. **¿Este recién nacido necesita estudio?** Es el **AABR** de tamizaje: un equipo automático estimula a una sola intensidad y contesta PASA o REFIERE (→ cap. 16).

Conviene tener claros sus límites desde el principio:

- El ABR **no es una audiometría**. Mide si un grupo de neuronas descarga **sincronizado**, no si la persona oye. Una neuropatía auditiva puede dejarlo plano con un audiograma casi normal (→ cap. 13), y una lesión por encima del tronco puede dejarlo normal en alguien que no entiende nada.
- El click, que es el estímulo de rutina, informa sobre todo de la zona de **2 a 4 kHz** (Stapells y Oates, 1997). No dice nada de los graves: para eso hacen falta estímulos por frecuencia.
- Un ABR alterado **no dice la causa**. Un tumor del ángulo y un meningioma dan el mismo trazado: el ABR describe un patrón, y la imagen dice qué lo produce.

## Fundamento

### Una respuesta muy chica dentro de mucho ruido

Cuando un sonido breve llega a la cóclea, miles de fibras del nervio auditivo descargan casi al mismo tiempo. Esa descarga, y la de los núcleos que siguen, produce un campo eléctrico que llega hasta la piel. Unos electrodos en el vértex y detrás de la oreja lo recogen como una serie de ondas positivas en los primeros 10 ms. Jewett y Williston (1971) las describieron en el ser humano y les pusieron los números romanos que se usan hasta hoy.

El problema es el tamaño. La onda V de un adulto normal mide alrededor de **0,5 µV** (Sanfins y cols., 2026).<!-- Pasada de fundamentos 2026-10-18: la cita era Da Silva Nunes y Gentile Matas (2005), que no se pudo leer; Sanfins y cols. (2026, tabla de amplitudes, 244 normoyentes) dan 0,50 µV de media para la onda V. --> El EEG de fondo y la actividad de los músculos, en la misma banda, son varias veces más grandes. En un solo barrido la respuesta es invisible.

La solución es **promediar**. Se repite el estímulo miles de veces y se suman los tramos de señal que siguen a cada uno. La respuesta aparece siempre a la misma latencia y se suma; el ruido aparece al azar y se cancela. El ruido que queda (el **ruido residual**) baja con la raíz cuadrada del número de barridos: para dejarlo a la mitad hay que promediar **cuatro veces más** (Picton, 2010). Por eso no basta "un poco más": de 1.000 a 2.000 barridos el ruido baja solo un 30 %.

### Quién genera cada onda

Los registros intracraneales hechos durante cirugías permitieron asignar cada onda a una estación de la vía (Møller y cols., 1981; Møller y Jannetta, 1983):

- **Onda I**: la porción **distal** del nervio auditivo, junto a la cóclea.
- **Onda II**: la porción **proximal** del nervio, donde entra al tronco.
- **Onda III**: el **núcleo coclear**, en la parte baja de la protuberancia.
- **Onda IV**: el **complejo olivar superior**.
- **Onda V**: el **lemnisco lateral** al llegar al **colículo inferior**, en la parte alta del tronco.

Es un mapa útil, pero no literal: cada onda recibe aportes de varias poblaciones de neuronas, y una misma estación contribuye a más de una onda (Melcher y Kiang, 1996). Las ondas VI y VII son inconstantes y no se usan en la clínica.

:::imagen ilustraciones/h10-generadores.svg ancho=100% La vía auditiva y el PEAT de un paciente sano. A: la vía de la cóclea a la corteza, de frente (a la izquierda queda el lado derecho del paciente). B: el PEAT del oído derecho con un clic a 80 dB, con las ondas I a V y los interpicos. Imagen propia hecha con labyrinthus3d (→ Simuladores, en las preliminares).
- @12,84 | **Cóclea y nervio VIII**: la onda I sale de la porción distal del nervio y la II de la proximal, donde entra al tronco.
- @1,68 | **Núcleo coclear**: la onda III.
- @22,57 | **Complejo olivar superior** (MSO, LSO y MNTB): la onda IV. Desde aquí la vía cruza y los dos oídos se comparan.
- @21,40 | **Lemnisco lateral** llegando al **colículo inferior**: la onda V.
- @57,22 | Cada onda aparece cuando la señal llega a su estación, con el retardo de cada tramo.
- @88,16 | La **V** es la más alta y la más estable: es la que se sigue al bajar la intensidad.
- @88,72 | Los **interpicos** miden el viaje dentro de la vía: I-III, III-V e I-V.
:::
<!-- Imagen: hacer_h10_simulador.py (A, esquema de la vía de labyrinthus3d recortado sin interfaz; B, dibujo propio con las latencias y amplitudes del modelo). Desde el 2026-10-16 labyrinthus3d usa la misma asignación de Møller que el texto (I y II nervio, III núcleo coclear, IV olivar, V lemnisco/colículo). -->

De ese mapa sale la lectura clínica de los **interpicos**:

- **I-III**: del nervio a la protuberancia baja. Se alarga en las lesiones del nervio, como el schwannoma vestibular.
- **III-V**: la parte alta del tronco.
- **I-V**: el **tiempo de conducción central**. Como empieza en la onda I, no depende de cuánto sonido llegó a la cóclea: es la medida más robusta del examen.

### Latencia e intensidad

Al bajar la intensidad, las ondas llegan **más tarde** y son **más chicas**. Las primeras en perderse son la I y la III; la V es la que llega más cerca del umbral, y por eso el umbral del ABR es el **umbral de la onda V**. En una serie de adultos normoyentes, la onda V pasa de 5,5 ms a 90 dB nHL a 8,2 ms a 20 dB nHL (Delgado Hernández y cols., 2003).<!-- Pasada de fundamentos 2026-10-18: decía "de unos 5 a 6 ms a 90 dB nHL a unos 8 a 9 ms a 20 dB nHL (ACNS, 2008)". La guía ACNS 9C no trae esas latencias (expresa la intensidad en dB pe SPL). Se corrigió a las medias de Delgado Hernández y cols. (2003, tabla II: V90 5,53 ms; V20 8,19 ms). -->

La razón está en la cóclea. A intensidad alta, el click excita con fuerza la base, que responde primero. A intensidad baja, la respuesta depende de regiones más apicales, donde la onda viajera llega después, y además la descarga tarda más en sincronizarse. Los interpicos, en cambio, casi no cambian con la intensidad: todas las ondas se corren juntas detrás de la I. Por eso son el parámetro neurológico preferido.

La curva que une la latencia de la V con la intensidad es la **función latencia-intensidad**. No es una recta: es plana a intensidad alta y se empina a medida que se acerca al umbral, alrededor de 0,3 ms por cada 10 dB entre 70 y 50 dB nHL (Hood, 1998; Delgado Hernández y cols., 2003). Su forma cambia con el tipo de pérdida, y ahí está buena parte del diagnóstico (ver "Cómo se informa").

### dB nHL: el cero del ABR

Los estímulos del ABR duran microsegundos o milisegundos, y un sonido tan breve se oye peor que un tono continuo. Por eso el ABR no usa dB HL sino **dB nHL** (*normalized hearing level*): **0 dB nHL es el nivel al que un grupo de adultos jóvenes con audición normal detecta ese mismo estímulo**, en ese mismo equipo. Cada estímulo tiene su propio cero.

Un detalle importante: el umbral de la onda V no cae en 0 dB nHL en un oído normal, sino algo más arriba. El sistema nervioso necesita algo de nivel para descargar con la sincronía que el promedio puede detectar. Por eso, para estimar el audiograma, al umbral del ABR se le **resta una corrección** (ver "Umbral por frecuencia").

:::sabias ¿Sabías que?
El ABR no cambia con el sueño, con la sedación habitual ni con la atención del paciente (Hall, 2007). Lo que sí lo cambian son la edad, el sexo, la temperatura y algunos fármacos (→ cap. 14). Por eso puede hacerse a un recién nacido dormido en brazos de su madre.
:::

## Antes de empezar

### Equipo

- **Equipo de potenciales evocados**: un generador de estímulos, un **preamplificador** cerca del paciente y un promediador en el computador.
- **Electrodos** de superficie, **gel abrasivo**, **gel conductor** y cinta adhesiva; alcohol y algodón.
- **Fonos de inserción**, rojo para el oído derecho y azul para el izquierdo, con olivas de varios tamaños. Además del confort, tienen tres ventajas: aíslan mejor del ruido de la sala, el sonido cruza mucho menos al otro oído y el transductor queda lejos de los electrodos, así que produce menos artefacto.
- **Vibrador óseo** para el ABR por vía ósea.
- **Otoscopio**, una **camilla** y una **manta**. Se trabaja con la luz apagada.

Con fonos de inserción el sonido demora cerca de 1 ms en recorrer el tubo. Algunos equipos lo descuentan y otros no. Da lo mismo cómo lo haga el tuyo, siempre que los valores normales que uses se hayan medido con **el mismo transductor**: cada laboratorio debe construir su norma con el mismo equipo y protocolo que usa en la clínica (Sanfins y cols., 2026; ACNS, 2008).

### Conoce tu equipo: el ABR

Todo equipo de ABR tiene la misma lógica: los parámetros a la izquierda, las curvas de cada oído al centro, los valores que mides a la derecha y, abajo, lo que está pasando mientras registras. La figura muestra un examen en curso: el OD ya está registrado de 80 a 20 dB nHL y el OI va en 40.

:::imagen /docs/manual/img/estudiante/abr.png Pantalla de un equipo de ABR durante una búsqueda de umbral Imagen propia: captura de LabSim.
- @-2.5,11 | **Estímulo y polaridad.** *Click*, *CE-Chirp* y *CE-Chirp LS* (de banda ancha), y los de frecuencia: *NB CE-Chirp LS* y *Burst* de 500 Hz a 4 kHz. La polaridad: alternada, condensación o rarefacción.
- @-2.5,17.5 | **Intensidad** en dB nHL y, debajo, el **Masking**: el ruido que va al oído contrario.
- @-2.5,26.5 | **Tasa** (estímulos por segundo) y **filtros**: *Pasa bajo* y *Pasa alto* fijan la banda de registro.
- @-2.5,34.3 | **Pinzar tubo.** Bloquea el tubo del fono de inserción: el sonido no llega, pero el artefacto eléctrico del transductor sigue.
- @-2.5,40.5 | **Promediación** (cuántos barridos va a sumar la curva) y **lado**.
- @63,5.7 | **Línea de estado** de la curva que se registra: nivel y oído, barridos, aceptados, FSP, ruido residual, replicabilidad (*repro*) y el veredicto del equipo.
- @38,12.5 | **Las ondas marcadas.** Se marcan con las banderas **A** y **A'**, que se arrastran sobre el trazo.
- @51.3,21 | **Rótulo de intensidad.** Un clic en él elige la curva con la que vas a trabajar.
- @88.5,5.6 | **Valores.** Latencia y amplitud de cada onda, por oído.
- @95.5,25.8 | **Variables**: los interpicos y la razón V/I se calculan solos. Lo que queda fuera de la norma se pinta en rojo.
- @10,79.5 | **EEG** en vivo de los dos canales. Si está sucio, el promedio va a salir sucio.
- @78.5,88 | **FSP y ruido residual** contra los barridos. La línea roja es el criterio de detección.
:::

Lo demás está en **Archivo → Parámetros avanzados**: el transductor, el montaje, los electrodos y sus impedancias, el rechazo de artefactos y el criterio de detección. El equipo **no viene configurado**: la tasa y las promediaciones arrancan con valores al azar, y dejarlo bien puesto es parte del examen.

### Preparar al paciente

**La quietud es todo.** El ABR no cambia con el sueño, pero el músculo tenso sí ensucia el registro. Por eso aquí el examen se hace con el paciente **dormido**, y si no duerme, no se hace. Las indicaciones se dan al citarlo:

- **Lactantes y niños pequeños**: dormir no más de 5 horas la noche anterior, no dejarlos dormir en el camino ni en la sala de espera y alimentarlos justo antes del examen (hay que traer la comida).
- **Adultos**: dormir no más de 5 horas la noche anterior, venir con ropa cómoda y no tomar café, bebidas estimulantes ni alcohol antes del examen.

El ABR diagnóstico toma alrededor de **una hora**.

Antes de poner un electrodo:

1. **Otoscopía** (→ H1). Un tapón de cerumen que ocluye el conducto suma una pérdida conductiva que no es del paciente y no deja poner el fono: se deriva para extraerlo y se reagenda.
2. **Anamnesis** (→ H1). En lactantes se agrega: semanas de gestación, enfermedades del embarazo, complicaciones del parto, días en UCI neonatal, fármacos y antecedentes familiares de hipoacusia.
3. **Explicar el examen**. Al adulto, o a quien acompaña al niño, se le dice qué se va a hacer y que la limpieza de la piel puede dejar la zona enrojecida, incluso con una costra, que desaparece en pocos días.

### Montaje de electrodos

Con el paciente acostado de espalda:

1. **Limpia la piel** con alcohol y luego con gel abrasivo, frotando en una sola dirección, en cada punto donde va un electrodo. El objetivo es bajar la impedancia entre la piel y el electrodo.
2. **Pon los electrodos** con gel conductor y fíjalos con cinta:
    - **activo** en el **vértex** (Cz; blanco en muchos equipos);
    - **tierra** sobre una ceja o en la frente (negro);
    - **referencias** en cada **mastoides**: rojo en la derecha y azul en la izquierda.
3. **Revisa las impedancias**: todas **bajo 5 kΩ** y **parecidas entre sí**. El preamplificador resta lo que es común a los dos electrodos de cada canal, y esa resta funciona bien solo si los dos tienen una impedancia parecida (Picton, 2010). Una impedancia alta o desbalanceada deja entrar el zumbido de la red eléctrica.
4. **Pon los fonos de inserción**: rojo en el OD, azul en el OI, con la oliva del tamaño del conducto.
5. Apaga la luz, abriga al paciente y espera que se duerma.

:::imagen /docs/manual/img/estudiante/abr-avanzados-2.png ancho=50% Parámetros de registro de un equipo de ABR Imagen propia: captura de LabSim.
- @80,14 | **Transductor**: fono de inserción, supraaural o vibrador óseo. Elegir el vibrador es lo que convierte el examen en un ABR por vía ósea.
- @88,19.7 | **Montaje**: Cz o Fz contra mastoides, o Cz contra lóbulo.
- @75,25.5 | **Ventana**: cuántos milisegundos se registran después del estímulo.
- @78,42.4 | **Filtro de red**: el notch de 50 Hz. Es el último recurso, no el primero: primero se arreglan las impedancias.
- @52,68 | **Electrodo activo** en el vértex (Cz).
- @86,68 | **Impedancia** de cada electrodo. Un número alto acá se paga en ruido.
- @52,76.5 | **Referencias**: A2 a la derecha y A1 a la izquierda (en el sistema 10-20, la zona de la oreja de cada lado).
- @52,85.1 | **Tierra** en la frente (Fpz).
:::

### Los parámetros de rutina

:::ayuda-ancho Configuración del ABR neurootológico y de búsqueda de umbral
| Parámetro | Valor de rutina | Por qué |
|---|---|---|
| Estímulo | Click (o CE-Chirp) | Banda ancha: sincroniza mucho nervio a la vez y da ondas claras |
| Polaridad | Alternada | Cancela el artefacto eléctrico del transductor y la microfónica coclear |
| Intensidad inicial | 80 dB nHL | En un oído normal se ven todas las ondas |
| Tasa | 21,1 estímulos/s | Rápida sin degradar las ondas; el decimal evita que el estímulo quede en fase con la red eléctrica |
| Montaje | Activo en Cz, referencia en el mastoides del oído estudiado, tierra en la frente | Las ondas I a III salen mejor del lado del estímulo; el vértex da la V |
| Filtros | 100 a 3.000 Hz | Deja pasar la energía del ABR; saca el EEG lento y parte del músculo |
| Ventana | 10 a 12 ms | Lo que tarda en llegar la onda V cerca del umbral |
| Barridos | 2.000 por curva | Lo que hace falta para bajar el ruido residual (ver el paso 4) |
| Rechazo de artefactos | ±10 µV o menos | Descarta los barridos sucios antes de que entren al promedio |
| Ganancia | 100.000 a 240.000, y baja si subes el rechazo | Llena el rango del conversor sin saturarlo |
| Filtro de red (notch) | Apagado | Último recurso, después de arreglar impedancias y tierra |
| Impedancias | Bajo 5 kΩ y parecidas entre sí | Una impedancia alta o desbalanceada deja entrar el zumbido de la red |
| Transductor | Fonos de inserción | Más aislación, menos artefacto |
:::

<!-- decide el autor: "Ganancia 10k" y "Ventana 10 s" salen del protocolo ORL 2019 (OtoAccess) y la escala de la ganancia depende del equipo; aquí se dan 100.000 a 240.000 porque BSA (2019) recomienda 240.000 con rechazo de ±10 µV y Burkard y Don (2015) explican la regla. Rechazo ±10 µV: BSA (2019, ABR neurológico: "no más de ±10 µV"; umbral: ±3 a ±10 µV). El protocolo ORL no fija rechazo ni notch; el montaje de mastoides y las impedancias bajo 5 kΩ sí coinciden con el protocolo. -->
<!-- verificar: Hall 2007 y AAA 2020 no se pudieron leer (no hay copia en ~/Escritorio/Libros); no se citan. -->
<!-- Protocolo ORL 2019: "Ventana de tiempo: 10 s". Es una errata: la ventana del ABR se mide en milisegundos (10 a 12 ms; Aguilar-Madrid y cols. 2016 registran 10 ms; Delgado Hernández y cols. 2003, 12 ms). Se corrigió a 10 a 12 ms. -->

La polaridad tiene un costo y hay que conocerlo. El click de **rarefacción** adelanta la onda I y la hace más clara que el de condensación; en la III y la V no hay diferencias constantes (Stockard y cols., 1979). En **condensación** las ondas I y III salen más chicas (Da Silva Nunes y Gentile Matas, 2005). Alternar cancela el artefacto, pero promedia dos respuestas de latencia apenas distinta y ensancha un poco las ondas. La norma que uses tiene que estar hecha con la misma polaridad.

Cada parámetro tiene su razón, y cambiarlo tiene un precio. Esto es lo que pasa cuando lo mueves:

1. **Pasa-alto más alto de 100 Hz.** Saca más músculo y EEG, pero también la parte lenta de la onda V y de las respuestas cerca del umbral. Las ondas se achican y adelantan. La ACNS (2008) lo acepta, hasta 100-200 Hz, solo cuando el músculo no se puede reducir, y no lo aconseja en niños. Hood (2015) dice lo contrario para ellos: en lactantes, bajar de 100 a 30 Hz suele aumentar la amplitud, porque su ABR tiene más energía lenta. La BSA (2019) usa 30 Hz en el umbral y no pasa de 50 Hz si el ruido es del paciente.
2. **Pasa-alto más bajo (30 Hz).** Entra más EEG y más músculo, los picos se redondean y las latencias se alargan (Hood, 2015). Sirve para el umbral. Para medir latencias, los valores normales tienen que haberse hecho con el mismo filtro.
3. **Pasa-bajo más bajo de 3.000 Hz.** Redondea los picos y alarga las latencias, porque se pierde la parte rápida de la respuesta (Hood, 2015). Con 1.500 Hz la BSA (2019) registra tone bursts, pero para las latencias del ABR neurológico exige 3.000 Hz, justo para no "redondear los bordes". Subirlo más no mejora nada: la energía del ABR está bajo unos 3.000 Hz y arriba solo entra ruido (Burkard y Don, 2015).
4. **Ventana corta (menos de 10 ms).** La onda V cerca del umbral llega a los 8 ms, y con fonos de inserción sale casi 1 ms más tarde. Una ventana corta la deja fuera y parece que no hay respuesta. En lactantes menores de 18 meses hace falta al menos 15 ms, y con tone burst de 20 a 25 ms (Hood, 2015; ACNS, 2008). Una ventana demasiado larga no daña la respuesta, pero resta resolución para medir (BSA, 2019).
5. **Pocos barridos.** El ruido baja con la raíz cuadrada del número de barridos: para reducirlo a la mitad hacen falta cuatro veces más (Burkard y Don, 2015). Con pocos barridos cerca del umbral, la onda V no sale del ruido y el umbral queda peor de lo real, o aparece una falsa V. La ACNS (2008) pide de 1.000 a 4.000. No hay un número mágico: manda el FSP y el ruido residual (paso 4).
6. **Intensidad inicial menor de 80 dB nHL.** Con menos nivel las ondas I y III se achican o desaparecen, y sin ellas no hay intervalos I-III ni I-V para informar. La latencia de la V se alarga 0,2 a 0,3 ms por cada 10 dB, más rápido cerca del umbral (Hood, 2015), y esas latencias ya no se pueden comparar con la norma de 80 dB nHL. La BSA (2019) mide los intervalos con 80 dB nHL o más.
7. **Tasa distinta de 21,1/s.** Sobre unos 20 a 30 estímulos por segundo la latencia de todas las ondas aumenta y las primeras (I y III) se achican, así que la onda I se pierde (BSA, 2019; Hood, 2015). Es justo lo que usas a propósito con 81,1/s para buscar fatiga neural (paso 6). Una tasa baja, de 8 a 10/s, resuelve mejor la I, la II y la VI (ACNS, 2008), pero el examen se alarga. Y una tasa que sea múltiplo de 50 Hz deja el estímulo en fase con la red: el zumbido se promedia como si fuera respuesta.
8. **Polaridad.** Alternada cancela el artefacto, pero si el paciente tiene una pérdida aguda de agudos mete en el mismo promedio dos respuestas desfasadas y empeora la resolución. En ese caso, o si no sabes cómo está su audición, la ACNS (2008) y Hood (2015) recomiendan una polaridad sola. Con una sola, aparece la microfónica: no la confundas con la onda I.
9. **Montaje.** El mastoides ipsilateral muestra mejor las ondas I a III, y un canal contralateral separa mejor la IV de la V. El lóbulo da menos músculo y una onda I más grande que el mastoides. Un electrodo en la nuca agranda la V, pero también el ruido (Hood, 2015, citando a Sininger y cols., 2000). Un activo en la frente alta achica la respuesta y baja la relación señal-ruido (BSA, 2019).
10. **Rechazo de artefactos.** Descarta cada barrido cuyo voltaje pasa el límite. Si lo pones muy bajo, rechazas casi todo y el promedio no avanza. Si lo subes o lo apagas, entra el movimiento y el músculo, el ruido residual no baja y el FSP no cruza nunca. La BSA (2019) parte de ±5 µV y sube a 7 solo después de revisar impedancias y filtros. Si duplicas el límite, hacen falta cuatro veces más barridos.
11. **Ganancia.** El conversor analógico-digital tiene un rango fijo, y la ganancia lleva la señal a ocupar casi todo ese rango. Con una ganancia baja, el redondeo del conversor se come una respuesta de 0,5 µV. Con una alta, un barrido ruidoso satura. Por eso la ganancia y el rechazo van juntos: con 240.000 el límite de ±10 µV llena justo el rango, y si subes el límite, hay que bajar la ganancia (BSA, 2019; Burkard y Don, 2015).
12. **Filtro de red.** El notch saca los 50 Hz. En el ABR de recién nacidos no lo deforma, salvo con tone burst de 500 Hz, donde la BSA (2019) pide no usarlo. Si lo usas, déjalo escrito en el informe. Primero arregla impedancias, cables y tierra.
13. **Impedancias.** Entre los dos electrodos de cada canal, una impedancia alta o desigual hace que la resta del preamplificador no cancele lo común y entre la red eléctrica y el músculo. La ACNS (2008) y la BSA (2019) piden menos de 5 kΩ; la BSA prefiere menos de 2 kΩ, o menos de 3 kΩ para el estudio neurológico, y balanceadas. Si saltan, reprepara la piel antes de tocar un filtro.

:::simulador
En Archivo → Parámetros avanzados cambia el pasa-alto, la ventana y el rechazo, y mira cómo se mueve la onda V.
:::

## Paso a paso

### 1. Mira el EEG antes de promediar

Antes de apretar Iniciar, mira el EEG en vivo. Tiene que estar **tranquilo**: sin el serrucho del músculo, sin saltos por movimiento y sin la onda regular de la red eléctrica. Un promedio no limpia un EEG malo; solo tarda más en mostrar que es malo. Si está sucio, revisa las impedancias, acomoda la cabeza o espera que el paciente se duerma.

### 2. Empieza a 80 dB nHL y reconoce las ondas

Registra el primer oído a **80 dB nHL**. Ahí, en un oído normal, se ven las ondas I a V. Antes de marcar nada, **repite la curva**: una onda que no está en las dos curvas no es una onda. Lo mismo dicen los **subpromedios A y B**: el equipo reparte los barridos en dos mitades, y una respuesta real aparece en las dos.

Para reconocer las ondas sirve el **canal contralateral** (el botón **C**), el que registra con la referencia del otro lado. Ahí la onda I falta o es mínima y la V sigue presente. Si dudas cuál es la I, la que desaparece en el contralateral lo es.

### 3. Busca el umbral de la onda V

Desde 80 dB nHL se **baja de 20 en 20** mientras la onda V siga presente. Cuando desaparece, se **sube de 10 en 10** hasta que vuelve. El **umbral** es la intensidad más baja con una onda V que se repite. Se repiten, como mínimo, la curva de intensidad máxima y la del umbral.

Ese esquema deja siempre un **escalón bajo el umbral sin onda V**. No es un registro perdido: es la prueba de que el nivel de arriba es el umbral y no un nivel más.

{{caso h10_mujer_joven}}

:::figura h10_mujer_joven abr
- @OD 80 I | A 80 dB nHL la **onda I** llega a 1,53 ms, la **III** a 3,67 y la **V** a 5,53. Interpicos: I-III 2,14 ms, III-V 1,86 e I-V 4,00. Todo dentro de lo normal para una mujer de su edad.
- @OD 40 V | A 40 dB la V llega a 6,67 ms y es más chica. La I y la III se achicaron más que la V.
- @OD 20 V | A 20 dB queda una III mínima y la **V**, a 7,67 ms.
- @OD 10 V | A 10 dB la V es chica, a 8,20 ms, pero está en las dos réplicas (las líneas finas): es una respuesta.
- @OD 0 | A 0 dB no hay nada que se repita.
- En el OD el orden de registro fue **80, 60, 40, 20, 0** (sin V) y, subiendo 10, **10** (con V). **Umbral de la onda V: 10 dB nHL**. El nivel de 50 dB se registró por el OI.
- Mira cómo se corre la V: 0,44 ms de 80 a 60, pero 1,0 ms de 40 a 20. Esa es la **función latencia-intensidad**: plana arriba y empinada cerca del umbral.
- @OI 80 | El **OI** no se parece al OD. Se lee en *Cómo se informa*.
:::

Si a 80 dB nHL no hay onda V, se sube a **90 o 100 dB nHL** antes de concluir que no hay respuesta. Más arriba los fonos no entregan sin distorsión.

### 4. Cuántos barridos: el FSP y el ruido residual

Decidir "hay onda" a ojo cerca del umbral es la fuente de error más común del examen. Los equipos ayudan con dos números:

- El **ruido residual**: cuánto ruido queda en el promedio, en nanovoltios. Mientras sea comparable con la onda que buscas, no puedes decidir nada.
- El **FSP** (*F single point*): la razón entre la varianza de la señal promediada y la del ruido de fondo (Elberling y Don, 1984). Si no hay respuesta, vale alrededor de 1. Un FSP de **3,1** o más equivale a una detección con un 99 % de confianza.

Los dos sirven para decidir **cuándo parar**: se sigue promediando hasta que el FSP cruza el criterio o hasta que el ruido residual es tan bajo que, si hubiera una respuesta del tamaño esperable, ya se vería (Don y Elberling, 1996). Parar antes es la forma más rápida de inventar una pérdida.

### 5. Enmascara cuando el otro oído puede contestar

El sonido que entra por un oído también llega, más débil, a la cóclea del otro. Con fonos de inserción pierde unos 60 a 70 dB en el camino (sobre 1.000 Hz va de 50 a 95 dB según la persona; Yacullo, 2015); por vía ósea, casi nada. Si el oído que estudias oye mucho peor que el otro, la respuesta que ves puede ser del oído bueno: es la misma **curva sombra** de la audiometría (→ H4). La regla es la misma: si la intensidad del estímulo, menos lo que se pierde al cruzar, alcanza el umbral óseo del otro oído, se enmascara con ruido en el otro oído (el **Masking** del panel).

### 6. Si sospechas compromiso neural, sube la tasa

Al aumentar la tasa, las neuronas tienen menos tiempo para recuperarse entre estímulos: las latencias se alargan y las amplitudes bajan. En la serie de Jiang y cols. (1991), de 10 a 90 estímulos por segundo la onda I se alarga un 4 a 10 %, la III un 9 a 13 % y la V un 12 a 15 %. Un nervio o un tronco con la conducción comprometida se "fatiga" más que uno sano, y la tasa alta puede destapar un retraso que a 21,1 no se veía.

Por eso, cuando la historia o el primer registro sugieren una lesión neural, se repite el registro a **81,1 estímulos por segundo** y se compara con el de 21,1. Para comparar se miden las mismas ondas en las dos curvas: el alargamiento normal es el de la serie de Jiang; uno bastante mayor es el hallazgo.

<!-- Protocolo ORL 2019: "En el caso de sospecha de neuropatía, es necesario aumentar la tasa a 81,1". La tasa alta busca la fatiga de conducción de una lesión neural (retrococlear); en la neuropatía auditiva, con el ABR ausente, la maniobra que define el cuadro es registrar en rarefacción y en condensación por separado para ver la microfónica coclear (Berlin y cols., 1998; BSA, 2019). Se redactó como "compromiso neural" y la polaridad se agregó en el caso H10.5 y en el cap. 13. -->

### 7. Umbral por frecuencia: tone burst y NB chirp

El click estima la audición entre 2 y 4 kHz. Para un audiograma completo, sobre todo en un lactante que se va a equipar con audífonos, hacen falta **estímulos por frecuencia**:

- **Tone burst**: un tono breve de una frecuencia, con subida y bajada suaves (por ejemplo, 2 ciclos de subida, 1 de meseta y 2 de bajada). Excita una zona acotada de la cóclea, pero sincroniza peor que el click: a intensidad alta prácticamente **solo se identifica la onda V**, más ancha y más tardía (Pinto y Matas, 2007). Con un burst grave la V llega tarde: en Álvaro (caso H10.2), con burst de 1 kHz, la V de 20 dB nHL llega a 10,6 a 10,9 ms. Con una ventana de 10 ms se habría salido de la pantalla, y con un burst de 500 Hz llega todavía más tarde.
- **Chirp**: un estímulo que manda primero los graves y después los agudos, para que todos lleguen a su lugar de la cóclea al mismo tiempo. Compensa el retraso de la onda viajera y sincroniza mejor: con el CE-Chirp LS de banda ancha la onda V sale más grande que con el click, sin cambiar su latencia a intensidad alta (Cargnelutti y cols., 2017). El **NB CE-Chirp LS** hace lo mismo dentro de una banda de frecuencia: mira la misma zona que el tone burst, con una V más clara.

#### De dB nHL a dB HL

El umbral del ABR queda por encima del umbral tonal del mismo oído. Para estimar el audiograma se le **resta una corrección** por estímulo y frecuencia, y el resultado se escribe en **dB eHL** (*estimated hearing level*). Las correcciones salen de comparar umbrales de ABR con audiometrías en los mismos sujetos (Stapells, 2000), y cada programa las publica en su propia tabla, con valores algo distintos según el equipo y la edad del niño (BSA, 2025; Ontario Infant Hearing Program, 2020; Hatton y cols., 2022).

:::ayuda Corrección nHL → eHL (BSA, 2019)
Valores en dB que se **restan** al umbral en dB nHL, con fonos de inserción, en 500 / 1.000 / 2.000 / 4.000 Hz.

| Estímulo | Mayores de 2 años y adultos | Lactantes de 12 a 24 semanas |
|---|---|---|
| Burst | 20 / 15 / 10 / 10 | 20 / 15 / 10 / 5 |
| Chirp por frecuencia | 15 / 10 / 5 / 5 | 15 / 10 / 5 / 0 |
| Click | 5 | 0 |

Un estímulo de banda ancha (click o CE-Chirp) no estima el umbral por frecuencia, y para el CE-Chirp de banda ancha no hay corrección publicada. Cada corrección vale para el protocolo con que se obtuvo: los programas de Ontario y de Columbia Británica, con sus propios estímulos, restan menos (→ cap. 17). En adultos chilenos con NB CE-Chirp, Fuentes y cols. (2024) obtuvieron 15 / 10 / 10 / 5.

En Álvaro, de 12 semanas: 10 dB nHL con burst de 4 kHz − 5 = **5 dB eHL**.
:::

{{caso h10_lactante}}

:::figura h10_lactante abr
- @OD 80 V | A 80 dB nHL: en el OD, I a 1,73 ms, III a 4,67 y V a 6,97 (I-V 5,24); en el OI, I a 1,87, III a 4,53 y V a 6,97 (I-V 5,10). Son latencias de lactante pequeño: la V llega 1,4 ms más tarde que en Sofía. Queda bajo el límite del recién nacido de término (7,56) y bajo el de los 6 meses (7,04; Rosa y cols., 2014).
- @OD 20 V | A 20 dB nHL la V sigue (9,27 ms en el OD, 9,30 en el OI). Es el nivel más bajo que se registró con click: alcanza para decir que de 2 a 4 kHz oye normal.
:::

:::figura h10_lactante abr 2
- @OD 20 V | Con **burst de 1 kHz** la V aparece a 20 dB nHL, a 10,87 ms en el OD y 10,63 en el OI, en una ventana de 20 ms; con una de 12 ms habría quedado pegada al borde.
- @OD 10 | A 10 dB ya no hay V en ningún oído: **umbral con burst de 1 kHz, 20 dB nHL**. 20 − 15 (corrección de la BSA para su edad) = **5 dB eHL**.
:::

:::figura h10_lactante abr 3
- @OD 10 V | Con **burst de 4 kHz** la V llega hasta 10 dB nHL (9,67 ms en el OD, 9,90 en el OI).
- @OD 0 | A 0 dB no hay V: **umbral con burst de 4 kHz, 10 dB nHL** en los dos oídos; 10 − 5 = **5 dB eHL**.
- El OI, el que refirió en el tamizaje, oye igual que el OD: un "refiere" de las primeras horas no es una sordera (→ cap. 16).
:::

{{caso h10_anciano}}

:::figura h10_anciano abr
- Juan Joaquín tiene una pérdida sensorioneural de agudos: 20 dB HL en 1 kHz, 35 en 2 kHz, 45 en 3 kHz y 60 (OD) o 55 (OI) en 4 kHz.
- @OD 80 I | En el OD la **onda I** es chica y llega tarde, a 2,10 ms: la genera la base de la cóclea, que es justo la zona dañada.
- @OI 80 III | En el OI **no hay onda I**: es la primera onda que se pierde en una pérdida de agudos.
- @OD 80 V | Pero la **V** llega a 6,00 ms en el OD y a 6,17 en el OI, dentro de lo normal para un hombre de 50 años o más (hasta 6,16 y 6,24; Sanfins y cols., 2026). El I-V del OD, 3,90 ms, es incluso corto.
- @OD 50 V | Con click la V se repite hasta 50 dB nHL; a 40 ya no: **umbral con click, 50 dB nHL** en los dos oídos. 50 − 5 = **45 dB eHL**: un promedio de 2 a 4 kHz, donde el audiograma marca 35 a 60 dB HL.
:::

:::figura h10_anciano abr 2
- @OD 40 V | Con **burst de 1 kHz** la V llega hasta 40 dB nHL (9,07 ms); a 30 y a 20 no hay V: **umbral, 40 dB nHL** en los dos oídos.
- 40 dB nHL − 15 = **25 dB eHL**, cerca de su audiograma en 1 kHz (20 dB HL). El click solo habría dicho "45 dB" y habría escondido que los graves están casi normales.
:::

### 8. ABR por vía ósea

Cuando el ABR por vía aérea sale elevado, la vía ósea responde lo mismo que en la audiometría: **¿es transmisión o es la cóclea?** Es clave en el lactante con otitis media o con una malformación del oído (→ cap. 15 y 17).

- **Cómo**: el **vibrador** en la mastoides, el mismo montaje. El cráneo vibra entero, así que en el adulto el estímulo llega casi igual a las dos cócleas: hay que **enmascarar** el oído contrario. En el lactante el cráneo transmite peor de un lado al otro y el enmascaramiento pesa menos (Yang y cols., 1987).
- **Hasta dónde**: el vibrador entrega poco. Los equipos llegan a unos **45 a 55 dB nHL** (Seo y cols., 2018). Y cada vía tiene su propia referencia: en el adulto normoyente el umbral del click por vía ósea queda unos **15 dB más arriba** que por vía aérea, mientras que en el lactante quedan casi iguales (Stuart y cols., 1993).<!-- Pasada de fundamentos 2026-10-18: la cita era Cobb y Stuart (2016). Esos trabajos usan CE-Chirp, no click, y en el de umbrales (J Speech Lang Hear Res 2016;59(4):853-9) la diferencia ósea-aérea del adulto es de 4 dB (13,8 contra 9,8 dB nHL). Los 15 dB con click salen de Stuart y cols. (1993): adultos 3,75 dB nHL aérea y 18,75 ósea; neonatos 3,75 y 1,25. --> Al adulto le sobra poco margen: con una pérdida sensorioneural de 35 dB HL, la respuesta ósea ya se sale del alcance del vibrador.
- **Qué se lee**: **solo la onda V**. La I y la III rara vez se identifican por vía ósea (Seo y cols., 2018): el estímulo trae poca energía aguda y el artefacto del vibrador, apoyado a centímetros del electrodo, tapa los primeros milisegundos. Buscar interpicos en un registro óseo es un error.
- **El lactante es distinto**: su onda V por vía ósea llega **antes** que por vía aérea, al revés que en el adulto (Seo y cols., 2018).

### 9. Mide y revisa la función latencia-intensidad

Con todas las curvas registradas, marca en cada una las ondas que se repiten: la latencia en el pico y la amplitud del pico al valle que lo sigue. Revisa la tabla de latencias e interpicos y el gráfico **latencia-intensidad** de las ondas I, III y V sobre la banda normal para la edad del paciente.

:::ayuda Ayuda memoria
- Paciente dormido, piel bien limpia, impedancias **bajo 5 kΩ** y parecidas.
- Click alternado, 21,1/s, 100-3.000 Hz, ventana de 10-12 ms, fonos de inserción. Lo que sigue a la onda V, con otra ventana, otra tasa y otros filtros, está en H14.
- **80 dB nHL**: ondas I a V, repetidas.
- Baja **20 en 20**; sin V, sube **10 en 10**. Umbral = la V más baja que se repite.
- Repite siempre el máximo y el umbral.
- Promedia hasta FSP ≥ 3,1 o ruido residual bajo; nunca menos por apuro.
- Sospecha neural: **tasa a 81,1/s**. Frecuencias: **burst o NB chirp** y corrección a dB eHL.
- Vía ósea: tope de **45 a 55 dB nHL**, **solo la V**.
:::

### El AABR de tamizaje

El **ABR automatizado** (AABR) es otro equipo, aunque use el mismo principio. No busca umbrales ni deja leer ondas: estimula cada oído a un **nivel fijo**, típicamente **35 dB nHL**, y un algoritmo estadístico decide si hay respuesta. Contesta **PASA** o **REFIERE**.

Se hace en el recién nacido antes del alta, dormido en la cuna o en brazos, en unos 15 minutos:

1. Otoscopía y anamnesis del parto.
2. Limpieza de la piel y electrodos: vértex y ambas mastoides, más la tierra en la frente si el equipo la usa.
3. Impedancias parecidas y bajo el límite del equipo, que en tamizaje es más amplio que en el ABR diagnóstico.
4. La sonda u oliva en el primer oído.
5. Iniciar. El equipo revisa solo las impedancias, el sello de la sonda y el estímulo, y promedia hasta llegar al criterio o hasta agotar el tiempo (en algunos equipos, 120 segundos).
6. El otro oído.

Leer bien el resultado es la mitad del examen:

- **PASA** quiere decir que ese oído tuvo una respuesta a 35 dB nHL **ese día**. No descarta una pérdida leve, ni una que aparezca después.
- **REFIERE no es hipoacusia.** En las primeras horas de vida, el vérnix en el conducto y el líquido en el oído medio hacen referir a muchos oídos sanos (→ cap. 16). Refiere también el bebé que se movió. Lo que sigue es un nuevo tamizaje o un ABR diagnóstico.
- El AABR **detecta la neuropatía auditiva** y las emisiones otoacústicas no: en la neuropatía las emisiones pasan y el AABR refiere. Por eso a los recién nacidos con más de 5 días en UCI neonatal se les tamiza con AABR (JCIH, 2019).

:::imagen /docs/manual/img/estudiante/aabr.png ancho=75% Pantalla de un AABR después de tamizar el OD Imagen propia: captura de LabSim.
- @25,21.8 | **Estímulo**: CE-Chirp, el de fábrica.
- @29,26.5 | **Nivel**: 35 dB nHL.
- @25,31.1 | **Tasa**: los equipos de tamizaje estimulan rápido para terminar antes.
- @29,40.2 | **Criterio FSP** (3,1) y, arriba, los barridos máximos (6.000): lo que el equipo exige antes de decir PASA.
- @29.5,63 | **Restaurar valores de fábrica** devuelve el protocolo de tamizaje.
- @97.5,9.7 | Los **cuatro pasos** que el equipo hace solo: sonda, impedancias, registro y resultado.
- @89.5,32.3 | **Impedancias**: en el tamizaje el límite es más amplio que en el diagnóstico.
- @80,36.8 | **Barridos**: 1.882 de 6.000. Se detuvo antes porque cruzó el criterio.
- @41,45 | **FSP 3,13**: sobre 3,1.
- @80,53 | **PASA**.
- @59,68.7 | En el **informe**, el resultado de cada oído viene precargado, pero se puede cambiar.
- @88,80 | **Observaciones** del registro y **conducta**: rescreening, ABR diagnóstico o alta.
:::

:::ojo Subir el nivel para conseguir un PASA
El nivel del tamizaje es fijo por una razón: 35 dB nHL separa un oído que oye de uno que necesita estudio. Un oído con umbral de 45 dB refiere a 35 y pasa a 60. Subir el nivel "para que pase" no cambia el oído, solo esconde la pérdida. Lo mismo vale para cortar el registro antes de que el equipo termine: con pocos barridos, hasta un oído sano refiere.
:::

## Cómo se informa

### Qué se mide

- **Latencias absolutas** de las ondas I, III y V a 80 dB nHL, por oído.
- **Interpicos** I-III, III-V e I-V.
- **Diferencia interaural de la onda V** al mismo nivel, cuando los dos oídos oyen parecido: es anormal sobre 0,2 a 0,4 ms (Hood, 1998; Selters y Brackmann, 1977); Musiek y cols. (2015) toman 0,3 a 0,4 ms. Con una pérdida de agudos asimétrica o un gap, la diferencia aparece sola.
- **Razón de amplitudes V/I**. En un oído normal la V es más grande que la I. Musiek y cols. (1984) toman como anormal una V/I menor que 1; en la revisión de Musiek y cols. (2015), menor que 0,75. No es frecuente, pero cuando la V es mucho más chica que la I es un hallazgo retrococlear.
- **Morfología y replicabilidad**: a 75 u 80 dB nHL, un ABR normal tiene picos bien definidos y **al menos las ondas I, III y V en cada oído**; la IV y la V pueden venir fundidas sin que eso sea anormal (Hood, 1998). Cada curva se repite.
- **La V con tasa alta**, si se registró (paso 6).
- **Umbral de la onda V** por estímulo, en dB nHL, y su estimación en dB eHL.

### Contra qué se compara

Cada laboratorio debe tener su propia norma, medida con su equipo, su transductor y su protocolo, estratificada por sexo y edad (Sanfins y cols., 2026; ACNS, 2008). En las mujeres las ondas III y V llegan 0,08 a 0,19 ms antes que en los hombres, y los interpicos son 0,07 a 0,15 ms más cortos (Jerger y Hall, 1980; Sanfins y cols., 2026). Con la edad adulta la V se alarga unos 0,2 ms entre los 25 y los 55 años y su amplitud cae cerca de un 10 % (Jerger y Hall, 1980). El recién nacido tiene la onda I algo más tardía que la del adulto y un I-V largo (Rosa y cols., 2014). La onda V, y con ella los interpicos, se acorta rápido hasta los 18 meses mientras la I casi no cambia (Gorga y cols., 1989), y después de los 3 años sigue acortándose más lento (Sharma y cols., 2016).<!-- Pasada de fundamentos 2026-10-18: decía "la onda I casi de adulto" y que el I-V llega "a valores de adulto entre los 9 meses y los 3 años". Rosa y cols. (2014) dan la onda I del término en 1,79 ms (adulto ~1,47); Gorga y cols. (1989) ven acortarse la V al menos hasta los 18 meses, y Sharma y cols. (2016) la ven madurar del todo recién a los 12 años. --> La temperatura también cuenta: la hipotermia alarga el I-V (→ cap. 14).

:::ayuda-ancho Límites del adulto (click a 80 dB nHL, oído derecho, en ms)
| Límite superior | Hombre, 18 a 49 años | Mujer, 18 a 49 años | Hombre, 50 o más | Mujer, 50 o más |
|---|---|---|---|---|
| Onda I | 1,80 | 1,80 | 1,90 | 1,87 |
| Onda III | 4,05 | 3,94 | 4,16 | 4,17 |
| Onda V | 6,03 | 5,89 | 6,16 | 6,08 |
| I-III | 2,45 | 2,42 | 2,54 | 2,71 |
| III-V | 2,33 | 2,11 | 2,17 | 2,16 |
| I-V | 4,49 | 4,33 | 4,53 | 4,51 |

Media más 2 desviaciones estándar, con fonos de inserción, en 244 personas de 3 a 79 años con audición normal (Sanfins y cols., 2026, tabla 7). La serie da también el oído izquierdo, que difiere en centésimas o décimas: en el informe se usa la columna de cada oído. El recién nacido tiene su propia tabla (Rosa y cols., 2014; → cap. 14).
:::

### Cuatro patrones

:::ayuda-ancho Cómo se lee un ABR alterado
| | Latencias absolutas | Interpicos | Latencia-intensidad | Umbral |
|---|---|---|---|---|
| **Conductivo** | Todas largas, incluida la I | Normales | Corrida en paralelo, tanto como el gap | Elevado |
| **Coclear** | Casi normales a intensidad alta; la I puede faltar | Normales | Empinada: converge con la normal a intensidad alta | Elevado |
| **Retrococlear** | La I normal; III y V largas | **Largos** (I-III, I-V) | Corrida desde la I; empeora con tasa alta | Normal o elevado |
| **Neuropatía auditiva** | Sin ondas, o desorganizadas | No medibles | No medible | No estima la audición |

Una pérdida conductiva alarga todas las latencias. Una coclear de agudos puede atrasar la V cuando el 4 kHz está entre moderado y moderadamente severo, pero deja normales los interpicos (Musiek y cols., 2015). En las dos, los interpicos normales son el dato que separa lo periférico de lo retrococlear.
:::

El oído izquierdo de Sofía (caso H10.1) es el patrón retrococlear. Los patrones conductivo y de neuropatía están en los caps. 15 y 13.

:::figura h10_mujer_joven abr 2
- @OI 80 I | En el registro de rutina (21,1 estímulos/s, figura del caso H10.1), el OI tiene la **I a tiempo**, a 1,40 ms, pero la III llega a 4,03 y la V a 6,07. El I-III (2,63 ms) y el I-V (4,67) pasan los límites de una mujer de su edad en ese oído (2,49 y 4,41). La diferencia interaural de la V es de 0,54 ms.
- Esta figura es el mismo examen a **81,1 estímulos/s**.
- @OD 80 V | En el OD la V pasa de 5,53 a 6,10 ms: se alarga 0,57 ms.
- @OI 80 V | En el OI, a esta tasa, todo se aplana y la **V llega a 7,37 ms**: se alarga 1,30 ms, más del doble que en el OD. En el registro de rutina estaba en 6,07. Una onda que se atrasa y se achata con la tasa alta es la fatiga de conducción: la vía del OI conduce mal.
- Sofía tiene 35 a 50 dB HL de 2 a 4 kHz en el OI. Una pérdida coclear así puede atrasar algo la V, pero con la I a tiempo **no alarga los interpicos**: el retraso está entre la I y la V, en el nervio (→ cap. 11).
:::

### Lo que hay que saber de memoria

:::ayuda-ancho Los números del PEAT (adulto, click a 80 dB nHL, fonos de inserción)
| Qué | Valor | Para qué sirve |
|---|---|---|
| Morfología | A 75 u 80 dB nHL, picos claros y al menos las ondas I, III y V en cada oído (Hood, 1998) | Si falta una onda, el informe dice cuál |
| Ondas I, III y V | I ≈ 1,5 ms; III ≈ 3,7; V ≈ 5,6 en el adulto. Límite de la V: 5,9 a 6,0 ms de 18 a 49 años y 6,1 a 6,2 ms desde los 50, según el sexo (Sanfins y cols., 2026) | Una latencia absoluta larga dice que algo atrasa la señal, pero no dónde |
| Interpicos | I-III ≈ 2,2 ms; III-V ≈ 1,9; I-V ≈ 4,1. Límite del I-V: 4,3 a 4,5 ms según la edad y el sexo (Sanfins y cols., 2026) | Separan lo periférico (interpicos normales) de lo retrococlear (interpicos largos) |
| Diferencia interaural de la V | Anormal sobre 0,2 a 0,4 ms (Hood, 1998); 0,3 a 0,4 ms para Musiek y cols. (2015) | Solo vale si los dos oídos tienen una audición parecida en agudos y sin gap |
| Razón V/I | La V es más grande que la I; anormal bajo 1 (Musiek y cols., 1984) o bajo 0,75 (Musiek y cols., 2015) | Sirve cuando las latencias están en el límite |
| Latencia-intensidad | La V pasa de unos 5,5 ms a 90 dB nHL a unos 8,2 ms a 20 dB nHL (Delgado Hernández y cols., 2003) | Una V tardía cerca del umbral es normal; a 80 dB, no |
| Tasa de 81,1/s | De 10 a 90 estímulos/s la V se alarga un 12 a 15 % en un oído normal (Jiang y cols., 1991) | Más que eso es fatiga de una vía comprometida |
| Umbral | Click: mira de 2 a 4 kHz. dB eHL = umbral en dB nHL menos la corrección (click: 5 dB en adultos; BSA, 2019). Hasta 20 dB eHL es audición normal (→ H3) | Da el "aproximadamente XX dB HL" de la conclusión |
:::

Los niños y los recién nacidos tienen otras latencias. Un recién nacido de término tiene la V a 6,90 ms, con límite de 7,56 (Rosa y cols., 2014): en un adulto eso sería un hallazgo, en él es lo normal (→ cap. 14).

### Del trazo a la conclusión

Se piensa siempre en el mismo orden. Cada paso descarta algo antes de pasar al siguiente.

1. **¿Hay ondas que se repiten a 80 dB nHL?** Si no, se sube a 90 o 100 dB nHL. Si sigue sin haber ondas, se miran las emisiones: presentes, es un patrón de neuropatía (→ cap. 13); ausentes, es una pérdida severa a profunda en la zona del click. Una ausencia de ABR puede ser cualquiera de las dos cosas, y las emisiones son las que las separan (Hood, 2015).
2. **¿Los interpicos son normales?** Si la I está a tiempo y el I-III o el I-V se alargan, el retraso está después de la cóclea: es un **patrón retrococlear**. La diferencia interaural de la V y una V/I menor que 1 lo apoyan, y la tasa alta puede destaparlo (→ cap. 11).
3. **Si los interpicos son normales, el problema es periférico.** ¿La I llega tarde y todas las ondas se corren juntas? Es **transmisión**: se mira la impedanciometría y, si hace falta, el ABR por vía ósea (→ cap. 15). ¿La I falta o es chica, y la V llega a tiempo a intensidad alta? Es **coclear**.
4. **¿Dónde está el umbral de la V?** Se pasa a dB eHL. Ese número es el grado aproximado de la conclusión, y vale para la zona de 2 a 4 kHz. Si se midió con tone burst o NB chirp, se informa cada frecuencia.
5. **¿Calza con el audiograma, si lo hay?** Si no calza, el informe lo dice: un ABR mejor que el audiograma es un hallazgo (→ cap. 19).

### Las frases de la conclusión

En este libro la conclusión dice qué audición **sugiere** el examen, en qué oído y de qué grado aproximado. Cuando el hallazgo no es un tipo de hipoacusia, la conclusión lo describe y no le pone nombre de enfermedad: eso lo hace el médico con la imagen y la clínica.

:::ayuda-ancho Qué se escribe en la conclusión
| Patrón | Conclusión |
|---|---|
| Normal | Examen sugiere audición normal en ambos oídos, para el rango frecuencial estudiado de 2 a 4 kHz. |
| Transmisión | Examen sugiere hipoacusia de transmisión en OD, de aproximadamente 45 dB HL, para el rango frecuencial estudiado de 2 a 4 kHz. Se adjunta impedanciometría. |
| Sensorioneural | Examen sugiere hipoacusia sensorioneural en ambos oídos, de aproximadamente 55 dB HL en OD y 60 dB HL en OI, para el rango frecuencial estudiado de 2 a 4 kHz. |
| Mixta | Examen sugiere hipoacusia mixta en OI, de aproximadamente 65 dB HL, con umbral de onda V por vía ósea elevado (XX dB nHL), para el rango de 2 a 4 kHz (→ cap. 15). |
| Retrococlear | Interpicos I-III e I-V prolongados en OD, con onda I de latencia normal y diferencia interaural de la onda V de 0,8 ms: patrón retrococlear en OD. Se sugiere correlación clínica e imagenológica. |
| Neuropatía | Ausencia de ondas con emisiones otoacústicas presentes: patrón de neuropatía auditiva bilateral. En este patrón el PEAT no estima el umbral auditivo (→ cap. 13). |
| Sin respuesta | OD sin ondas reconocibles hasta 100 dB nHL, con emisiones ausentes: examen sugiere hipoacusia de grado severo a profundo en OD, para el rango de 2 a 4 kHz. |
| Por frecuencia | Umbrales estimados con tone burst, en dB eHL: OD 500 Hz XX, 1.000 Hz XX, 2.000 Hz XX, 4.000 Hz XX (corrección de la BSA, 2019). |
:::

Las cifras de la tabla son de ejemplo. El grado sale siempre del umbral en dB eHL del paciente.

### Qué lleva el informe

El informe del protocolo de este libro describe cada oído y concluye. Hood (1998, cap. 9) agrega lo que le permite a otro profesional revisar el examen: los parámetros, los valores medidos y los trazos con las ondas marcadas. Un informe completo lleva:

1. **Motivo** y la historia que importa.
2. **Lo que se hizo antes**: audiometría, impedanciometría y emisiones, si las hay. El PEAT se interpreta junto a ellos.
3. **Registro**: estímulos, transductor, polaridad, tasa, intensidad, filtros, ventana, barridos y réplica, montaje, impedancias, enmascaramiento y estado del paciente.
4. **Referencia**: con qué tabla se compara (edad, sexo, oído y fuente).
5. **Tabla de valores**: latencias, interpicos, diferencia interaural, la V con tasa alta si se hizo, y los umbrales en dB nHL y en dB eHL. Lo que sale del límite se marca.
6. **Interpretación**: qué es normal y qué no, y en qué se basa.
7. **Conclusión**, con las frases de la tabla de arriba.
8. **Recomendación**. En un niño, Hood agrega siempre una nota: si el lenguaje no se desarrolla como se espera, hay que volver a evaluarlo, porque un ABR normal no descarta un problema central.
9. **Los trazos**, con las ondas marcadas.

### Informes de ejemplo

Los tres pacientes de este capítulo, informados de principio a fin. En los tres: polaridad alternada, 21,1 estímulos/s, filtros de 100 a 3.000 Hz, ventana de 12 ms (20 ms para el burst de 1 kHz de Álvaro), 2.000 barridos por curva con réplica, fonos de inserción, montaje Cz-mastoides con impedancias bajo 5 kΩ y sin enmascaramiento contralateral. Los trazos marcados son las figuras de cada caso. En las tablas, ↑ marca lo que pasa el límite.

:::comentario-ancho Informe de Álvaro, 12 semanas (caso H10.2)
**Motivo**: refirió dos veces en el tamizaje con emisiones del OI.

**Registro**: click a 80, 40 y 20 dB nHL; tone burst de 1 kHz a 40, 20 y 10 (sin respuesta a 10), y de 4 kHz a 40, 20, 10 y 0 dB nHL. En sueño fisiológico.

**Referencia**: recién nacido de término, 39 a 40 semanas (Rosa y cols., 2014): media / límite (media + 2 DE). Ese estudio no tiene un grupo de 12 semanas; el de 6 meses tiene la V en 6,50 (límite 7,04) y el I-V en 4,81 (límite 5,33).

| | OD | OI | Referencia |
|---|---|---|---|
| Onda I | 1,73 | 1,87 | 1,79 / 1,97 |
| Onda III | 4,67 | 4,53 | 4,56 / 5,00 |
| Onda V | 6,97 | 6,97 | 6,90 / 7,56 |
| I-III | 2,94 | 2,66 | 2,77 / 3,19 |
| III-V | 2,30 | 2,44 | 2,42 / 3,64 |
| I-V | 5,24 | 5,10 | 5,08 / 5,70 |
| Diferencia interaural de la V | 0,00 | | hasta 0,4 |
| Umbral con click (dB nHL → dB eHL) | 20 o menos → 20 o menos | 20 o menos → 20 o menos | hasta 20 dB eHL |
| Umbral con burst de 1 kHz | 20 → 5 | 20 → 5 | |
| Umbral con burst de 4 kHz | 10 → 5 | 10 → 5 | |

**Morfología**: ondas I, III y V bien definidas y replicables en ambos oídos.

**Interpretación**: latencias absolutas e interpicos dentro de lo esperado para la edad, sin diferencia interaural. Onda V presente hasta 20 dB nHL con click (el nivel más bajo registrado), hasta 20 dB nHL con burst de 1 kHz (sin respuesta a 10) y hasta 10 dB nHL con burst de 4 kHz (sin respuesta a 0). Correcciones a dB eHL de la BSA (2019) para lactantes de 12 a 24 semanas.

**Conclusión**: examen sugiere audición normal en ambos oídos, de 1 a 4 kHz. No se confirma el resultado del tamizaje en el OI.

**Recomendación**: control del desarrollo del lenguaje; si no avanza como se espera, volver a evaluar.
:::

:::comentario-ancho Informe de Sofía, 28 años (caso H10.1)
**Motivo**: zumbido y menor audición en el OI; audiometría con caída de agudos en el OI.

**Registro**: click a 80, 60, 50, 40, 20, 10 y 0 dB nHL, y a 80 dB nHL con 81,1 estímulos/s. En reposo, con los ojos cerrados.

**Referencia**: mujer de 18 a 49 años, por oído (Sanfins y cols., 2026): límite superior (media + 2 DE).

| | OD | OI | Límite OD / OI |
|---|---|---|---|
| Onda I | 1,53 | 1,40 | 1,80 / 1,80 |
| Onda III | 3,67 | 4,03 ↑ | 3,94 / 4,01 |
| Onda V | 5,53 | 6,07 ↑ | 5,89 / 5,92 |
| I-III | 2,14 | 2,63 ↑ | 2,42 / 2,49 |
| III-V | 1,86 | 2,04 | 2,11 / 2,12 |
| I-V | 4,00 | 4,67 ↑ | 4,33 / 4,41 |
| Diferencia interaural de la V | 0,54 ↑ | | hasta 0,4 |
| V a 81,1 estímulos/s | 6,10 (+0,57) | 7,37 (+1,30) ↑ | |
| Umbral con click (dB nHL → dB eHL) | 10 → 5 | 50 → 45 | hasta 20 dB eHL |

**Morfología**: OD con ondas I, III y V bien definidas y replicables. OI con ondas I, III y V replicables, de menor amplitud.

**Interpretación**: OD normal. OI anormal: onda I de latencia normal con ondas III y V prolongadas e interpicos I-III e I-V prolongados. Lo apoyan la diferencia interaural de la onda V (0,54 ms) y el alargamiento de la V con la tasa alta (1,30 ms en el OI frente a 0,57 en el OD).

**Conclusión**: patrón retrococlear en OI. El umbral sugiere una pérdida de aproximadamente 45 dB HL en OI y audición normal en OD, para el rango de 2 a 4 kHz. Se adjunta audiometría.

**Recomendación**: se sugiere correlación clínica e imagenológica.
:::

:::comentario-ancho Informe de Juan Joaquín, 76 años (caso H10.3)
**Motivo**: dificultad para entender y zumbido bilateral; PEAT antes de indicar audífonos.

**Registro**: click a 80, 60, 50 y 40 dB nHL, y tone burst de 1 kHz a 60, 40, 30 y 20 dB nHL. En reposo.

**Referencia**: hombre de 50 años o más, por oído (Sanfins y cols., 2026): límite superior (media + 2 DE).

| | OD | OI | Límite OD / OI |
|---|---|---|---|
| Onda I | 2,10 ↑ | no se identifica | 1,90 / 1,91 |
| Onda III | 4,23 ↑ | 4,20 | 4,16 / 4,22 |
| Onda V | 6,00 | 6,17 | 6,16 / 6,24 |
| I-III | 2,13 | | 2,54 / 2,53 |
| III-V | 1,77 | 1,97 | 2,17 / 2,33 |
| I-V | 3,90 | | 4,53 / 4,54 |
| Diferencia interaural de la V | 0,17 | | hasta 0,4 |
| Umbral con click (dB nHL → dB eHL) | 50 → 45 | 50 → 45 | hasta 20 dB eHL |
| Umbral con burst de 1 kHz | 40 → 25 | 40 → 25 | |

**Morfología**: OD con ondas I, III y V replicables; la I es de baja amplitud. OI con ondas III y V replicables; la onda I no se identifica.

**Interpretación**: onda I tardía en OD y ausente en OI, con onda V de latencia normal, interpicos normales y diferencia interaural normal: patrón de pérdida coclear de agudos. Sin signos de alteración retrococlear.

**Conclusión**: examen sugiere hipoacusia sensorioneural en ambos oídos, de aproximadamente 45 dB HL para el rango de 2 a 4 kHz, con umbral estimado de 25 dB eHL en 1 kHz: la pérdida predomina en agudos. Se adjunta audiometría.

**Recomendación**: evaluación para audífonos.
:::

<!-- Protocolo ORL 2019, ejemplo de informe: entre las conclusiones ofrece "Hipofunción sensorioneural". El término para el tipo de pérdida es "hipoacusia sensorioneural" (ASHA y BIAP); se dejó así. -->

## Errores frecuentes

- **Promediar poco.** Con pocos barridos la V cercana al umbral no sale del ruido y el umbral queda más alto de lo real. Es el error que más pérdidas inventa.
- **Marcar una onda que no se repite.** Si no está en las dos curvas, o en los subpromedios A y B, no es una onda.
- **Leer la latencia sin el audiograma.** Una conductiva o una pérdida de agudos alargan las latencias absolutas y la diferencia interaural. El retrococlear se decide con los **interpicos**.
- **Electrodos mal puestos.** Una impedancia alta o desbalanceada deja entrar la red eléctrica; un electrodo suelto deja la curva plana o llena de ruido.
- **Equipo sin configurar.** Filtros abiertos, tasa al azar o una ventana corta para el tone burst grave cambian las ondas o las dejan fuera.
- **Normas de otro protocolo.** Comparar contra valores medidos con otro transductor, otra polaridad u otra tasa.
- **Llamar "sordo" a un ABR plano.** Sin ABR y con emisiones presentes, puede ser una neuropatía.

### Lo que parece onda y no es

El promedio cancela lo que es aleatorio. Lo que **no** es aleatorio, lo que se repite con cada estímulo o se cuela en una parte de los barridos, sobrevive al promedio y puede parecer una onda.

:::ayuda-ancho Artefactos del ABR
| Artefacto | Cómo se ve | Cómo se reconoce o se resuelve |
|---|---|---|
| **Artefacto de estímulo** | Una deflexión grande en el primer milisegundo, que crece con la intensidad. Peor con fono supraaural y con vibrador | Polaridad alternada lo cancela (por vía ósea, no del todo). Con fono de inserción, **pinzar el tubo**: el sonido deja de llegar y el artefacto sigue (BSA, 2019) |
| **Microfónica coclear** | Ondas desde el inicio que se **invierten** al cambiar de polaridad | Registrar en rarefacción y condensación por separado. Clave en la neuropatía (→ cap. 13) |
| **Respuesta postauricular** | Una onda grande hacia los 12 a 15 ms, a intensidad alta, en un paciente tenso (O'Beirne y Patuzzi, 1999) | Se **repite** en los subpromedios: replicar no la descarta. Se va relajando al paciente |
| **Red eléctrica** | Una onda regular cada 20 ms (50 Hz) en el EEG y en el promedio | Revisar impedancias y la tierra; el notch es el último recurso |
| **Movimiento y músculo** | EEG lleno de ruido; el rechazo descarta muchos barridos y el promedio no avanza | Esperar que duerma, acomodar la cabeza. Sin rechazo, esos barridos entran y arruinan el promedio |
| **Falsa onda V** | Una onda con forma y latencia de V en el promedio | **No se repite**: está en uno de los subpromedios y no en el otro. Repetir la curva la hace desaparecer |
:::

La **falsa onda V** merece una mención aparte porque engaña justo donde más importa, cerca del umbral. Es un artefacto que se metió en una parte de los barridos y que, por casualidad, cae donde se espera la V. El promedio la muestra; el FSP no la confirma, y el ruido residual sube. Lo que la delata son los **subpromedios A y B**: una respuesta real está en las dos mitades; la falsa V, solo en una. La respuesta postauricular es el contraejemplo: es real, se repite en las dos mitades, y aun así no es auditiva de tronco. Por eso la replicación es necesaria pero no suficiente: también hay que mirar **dónde** está la onda y **cómo** se comporta con la intensidad (→ cap. 18).

:::ojo Ojo clínico
Antes de informar un ABR, pregúntate si **calza con lo demás**: con el audiograma, con la timpanometría, con las emisiones y con cómo conversó el paciente. Un umbral de ABR peor que la audiometría hace sospechar un registro malo antes que una pérdida; uno mucho mejor hace sospechar una pérdida no orgánica (→ cap. 19). Y un ABR plano con emisiones presentes no es una sordera: es una neuropatía hasta que se demuestre lo contrario.
:::

## Para practicar

:::pregunta Preguntas para practicar
1. En el OD de Sofía, ¿qué intensidades registrarías si a 20 dB nHL **no** hubiera onda V? ¿Cuál sería su umbral si a 30 sí la hay?
2. Promedias 500 barridos en un oído con umbral real de 30 dB nHL y encuentras la V hasta 45. ¿El oído empeoró? ¿Qué harías para saberlo?
3. Sofía tiene en el OI una diferencia interaural de la onda V de 0,54 ms. ¿Qué otro número de su registro dice que no es una pérdida coclear? ¿Qué agrega la tasa de 81,1?
4. Álvaro tiene la onda V a 6,97 ms. ¿Es normal? ¿Lo sería en Sofía?
5. Con los umbrales de Juan Joaquín (click 50 y burst de 1 kHz 40 dB nHL), estima su audición en dB eHL. ¿Qué le habría dicho a un médico un ABR solo con click?
6. Un lactante tiene un ABR por vía aérea con umbral de 50 dB nHL y por vía ósea no responde a 55. ¿Puedes concluir que la pérdida es sensorioneural? ¿Qué cambia si es un adulto?
7. En un AABR, un oído refiere dos veces. La enfermera propone subir el nivel a 60 dB "para que pase". ¿Qué le contestas?
:::

## Referencias

### Técnica

1. Hood LJ. Auditory brainstem response: estimation of hearing sensitivity. En: Katz J, Chasin M, English K, Hood LJ, Tillery KL, editores. Handbook of clinical audiology. 7th ed. Philadelphia: Wolters Kluwer; 2015. p. 249-66.
1. Yacullo WS. Clinical masking. En: Katz J, Chasin M, English K, Hood LJ, Tillery KL, editores. Handbook of clinical audiology. 7th ed. Philadelphia: Wolters Kluwer; 2015. p. 77-111.
1. Burkard R, Don M. Introduction to auditory evoked potentials. En: Katz J, Chasin M, English K, Hood LJ, Tillery KL, editores. Handbook of clinical audiology. 7th ed. Philadelphia: Wolters Kluwer; 2015. p. 187-205.
1. Picton TW. Human auditory evoked potentials. San Diego: Plural Publishing; 2010 (el editor la fecha en 2011).
1. Hall JW 3rd. New handbook of auditory evoked responses. Boston: Pearson; 2007.
1. American Clinical Neurophysiology Society. Guideline 9C: Guidelines on short-latency auditory evoked potentials. ACNS; 2008. Disponible en: https://www.acns.org/pdf/guidelines/Guideline-9C.pdf
1. Elberling C, Don M. Quality estimation of averaged auditory brainstem responses. Scand Audiol. 1984;13(3):187-97. doi:10.3109/01050398409043059
1. Don M, Elberling C. Evaluating residual background noise in human auditory brain-stem responses. J Acoust Soc Am. 1994;96(5 Pt 1):2746-57. doi:10.1121/1.411281
1. Don M, Elberling C. Use of quantitative measures of auditory brain-stem response peak amplitude and residual background noise in the decision to stop averaging. J Acoust Soc Am. 1996;99(1):491-9. doi:10.1121/1.414560
1. Stockard JE, Stockard JJ, Westmoreland BF, Corfits JL. Brainstem auditory-evoked responses: normal variation as a function of stimulus and subject characteristics. Arch Neurol. 1979;36(13):823-31. doi:10.1001/archneur.1979.00500490037006
1. Da Silva Nunes C, Gentile Matas C. Audiometría de tronco encefálico utilizando diferentes polaridades de presentación del estímulo. Rev Chil Fonoaudiol. 2005;6(2):7-16. doi:10.5354/0719-4692.2005.48433
1. Jiang ZD, Wu YY, Zheng WS, Sun DK, Feng LY, Liu XY. The effect of click rate on latency and interpeak interval of the brain-stem auditory evoked potentials in children from birth to 6 years. Electroencephalogr Clin Neurophysiol. 1991;80(1):60-4. doi:10.1016/0168-5597(91)90044-x
1. Cargnelutti M, Coser PL, Biaggio EP. LS CE-Chirp vs. click in the neuroaudiological diagnosis by ABR. Braz J Otorhinolaryngol. 2017;83(3):313-7. doi:10.1016/j.bjorl.2016.04.018
1. Pinto FR, Matas CG. A comparison between hearing and tone burst electrophysiological thresholds. Braz J Otorhinolaryngol. 2007;73(4):513-22. doi:10.1016/S1808-8694(15)30103-8
1. Stapells DR, Oates P. Estimation of the pure-tone audiogram by the auditory brainstem response: a review. Audiol Neurootol. 1997;2(5):257-80. doi:10.1159/000259252
1. Stapells DR. Threshold estimation by the tone-evoked auditory brainstem response: a literature meta-analysis. J Speech Lang Pathol Audiol. 2000;24(2):74-83.
1. Seo YJ, Kwak C, Kim S, Park YA, Park KH, Han W. Update on bone-conduction auditory brainstem responses: a review. J Audiol Otol. 2018;22(2):53-8. doi:10.7874/jao.2017.00346 PMID 29471611.
1. Stuart A, Yang EY, Stenstrom R, Reindorp AG. Auditory brainstem response thresholds to air and bone conducted clicks in neonates and adults. Am J Otol. 1993;14(2):176-82. PMID 8503493.
1. Yang EY, Rupert AL, Moushegian G. A developmental study of bone conduction auditory brain stem response in infants. Ear Hear. 1987;8(4):244-51. doi:10.1097/00003446-198708000-00009
1. British Society of Audiology. Recommended procedure: cochlear microphonic testing (OD104-87). BSA; 2019. Disponible en: https://www.thebsa.org.uk/wp-content/uploads/2023/10/OD104-87-Recommended-Procedure-for-Cochlear-Microphonic-Testing.pdf
1. O'Beirne GA, Patuzzi RB. Basic properties of the sound-evoked post-auricular muscle response (PAMR). Hear Res. 1999;138(1-2):115-32. doi:10.1016/s0378-5955(99)00159-8

### Valores normales

1. Sanfins MD, Santillo MEA, Martins MFP, Silva DLdS, Gos E, Skarzynski PH, Hall JW III. The influence of sex, ear, and age on auditory brainstem responses recorded with the NeuroAudio system. Diagnostics. 2026;16(7):971. doi:10.3390/diagnostics16070971
1. Jerger J, Hall J. Effects of age and sex on auditory brainstem response. Arch Otolaryngol. 1980;106(7):387-91. doi:10.1001/archotol.1980.00790310011003
1. Hood LJ. Clinical applications of the auditory brainstem response. San Diego: Singular Publishing Group; 1998.
1. Delgado Hernández J, Zenker Castro F, Barajas del Prat JJ. Normalización de los potenciales evocados auditivos del tronco cerebral I: resultados en una muestra de adultos normoyentes. Auditio. 2003;2(1):13-8. doi:10.51445/sja.auditio.vol2.2003.0020
1. Aguilar-Madrid G, Torres-Valenzuela A, Hinojos-Escobar W, Cabello-López A, Gopar-Nieto R, Ravelo-Cortés PE, et al. Latencias de los potenciales evocados auditivos del tallo cerebral, por edad y sexo, en población adulta mexicana. Rev Med Inst Mex Seguro Soc. 2016;54(2):203-10. PMID 26960049.
1. Gorga MP, Kaminski JR, Beauchaine KL, Jesteadt W, Neely ST. Auditory brainstem responses from children three months to three years of age: normal patterns of response II. J Speech Hear Res. 1989;32(2):281-8. doi:10.1044/jshr.3202.281
1. Rosa LAC, Suzuki MR, Angrisani RG, Azevedo MF. Auditory brainstem response: reference-values for age. CoDAS. 2014;26(2):117-21. doi:10.1590/2317-1782/2014469in
1. Sharma M, Bist SS, Kumar S. Age-related maturation of wave V latency of auditory brainstem response in children. J Audiol Otol. 2016;20(2):97-101. doi:10.7874/jao.2016.20.2.97
1. Selters WA, Brackmann DE. Acoustic tumor detection with brain stem electric response audiometry. Arch Otolaryngol. 1977;103(4):181-7. doi:10.1001/archotol.1977.00780210037001
1. Musiek FE, Gonzalez JE, Baran JA. Auditory brainstem response: differential diagnosis. En: Katz J, Chasin M, English K, Hood LJ, Tillery KL, editores. Handbook of clinical audiology. 7th ed. Philadelphia: Wolters Kluwer; 2015. p. 231-48.
1. Musiek FE, Kibbe K, Rackliffe L, Weider DJ. The auditory brain stem response I-V amplitude ratio in normal, cochlear, and retrocochlear ears. Ear Hear. 1984;5(1):52-5. doi:10.1097/00003446-198401000-00011

### Umbral por frecuencia y tamizaje

1. British Society of Audiology. Recommended procedure: auditory brainstem response (ABR) testing for post-newborn and adult (OD104-84). BSA; 2019. Disponible en: https://www.thebsa.org.uk/wp-content/uploads/2022/09/ABR-post-newborn-and-Adult.pdf
1. Fuentes M, Barrientos R, Bravo S. Estimated thresholds (est dBHL) for auditory evoked potentials with narrowband CE-Chirp® stimuli. Rev CEFAC. 2024;26(6). doi:10.1590/1982-0216/202426614423
1. British Society of Audiology. Recommended procedure: auditory brainstem response (ABR) testing in newborns (OD100). BSA; 2025, enmienda 2026. Disponible en: https://www.thebsa.org.uk/wp-content/uploads/2026/06/OD100-Auditory-Brainstem-Response-ABR-Testing-in-Newborns-March-2026.pdf
1. Ontario Infant Hearing Program. Protocol for auditory brainstem response-based audiological assessment (ABRA). Version 2018.02. Toronto; 2020. Disponible en: https://www.uwo.ca/nca/pdfs/clinical_protocols/2018.02%20ABRA%20Protocol_Oct%202020.pdf
1. Hatton JL, Van Maanen A, Stapells DR. British Columbia Early Hearing Program: auditory brainstem response protocol. Vancouver: BC Early Hearing Program; 2022. Disponible en: https://ehdi-pals.org/HostedMaterials/British%20Columbia%20ABR%20Protocol.pdf
1. Joint Committee on Infant Hearing. Year 2019 position statement: principles and guidelines for early hearing detection and intervention programs. J Early Hear Detect Interv. 2019;4(2):1-44. doi:10.15142/fptk-b748

### Fisiología

1. Jewett DL, Williston JS. Auditory-evoked far fields averaged from the scalp of humans. Brain. 1971;94(4):681-96. doi:10.1093/brain/94.4.681
1. Møller AR, Jannetta P, Bennett M, Møller MB. Intracranially recorded responses from the human auditory nerve: new insights into the origin of brain stem evoked potentials (BSEPs). Electroencephalogr Clin Neurophysiol. 1981;52(1):18-27. doi:10.1016/0013-4694(81)90184-x
1. Møller AR, Jannetta PJ. Interpretation of brainstem auditory evoked potentials: results from intracranial recordings in humans. Scand Audiol. 1983;12(2):125-33. doi:10.3109/01050398309076235
1. Melcher JR, Kiang NY. Generators of the brainstem auditory evoked potential in cat. III: Identified cell populations. Hear Res. 1996;93(1-2):52-71. doi:10.1016/0378-5955(95)00200-6
1. Starr A, Picton TW, Sininger Y, Hood LJ, Berlin CI. Auditory neuropathy. Brain. 1996;119(Pt 3):741-53. doi:10.1093/brain/119.3.741
1. Berlin CI, Bordelon J, St John P, Wilensky D, Hurley A, Kluka E, et al. Reversing click polarity may uncover auditory neuropathy in infants. Ear Hear. 1998;19(1):37-47. doi:10.1097/00003446-199802000-00002
