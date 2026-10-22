# 18. El ABR que engaña

:::objetivos En este capítulo
- Explicar por qué el promedio mejora con la raíz del número de barridos y qué te dicen el FSP y el ruido residual sobre cuándo parar.
- Reconocer una curva "sin respuesta" que en realidad es un registro con demasiado ruido, y un umbral que sale alto o bajo por pocos barridos o por un artefacto.
- Distinguir una onda auditiva de un artefacto de estímulo, de una respuesta postauricular y de una falsa onda V, con las pruebas que lo permiten.
- Ver cómo los filtros, la polaridad y la ventana de registro cambian lo que se ve, y por qué la norma solo vale con los mismos ajustes.
- Decidir con un orden fijo de preguntas si un trazo es una respuesta antes de marcarla.
:::

El ABR tiene fama de examen objetivo: el paciente no tiene que contestar nada, el equipo dibuja unas ondas y un número dice si hay respuesta. Esa fama es la trampa. La señal que se busca mide una fracción de microvolt y se esconde dentro de un ruido varias veces más grande; lo que llega a la pantalla es el resultado de unas decisiones (cuántos barridos, qué filtros, qué transductor, qué polaridad) y de una última decisión, la tuya, cuando marcas una onda o declaras que no hay ninguna. Este capítulo trata de los registros que parecen decir una cosa y dicen otra: una curva plana que no es una sordera, una "onda I" que es el estímulo, una "onda V" que es un músculo, un umbral demasiado bajo porque una onda falsa cayó en el lugar justo. Todos los pacientes de los casos son pacientes corrientes. Lo que engaña es el registro.

## Técnica en foco

La técnica de rutina del ABR está en H10: montaje, parámetros, búsqueda de umbral y cómo se informa. Aquí no se repite. Este capítulo toma una sola idea de ese capítulo y la lleva hasta el final: **un trazo no es una respuesta mientras no haya pasado cinco controles**.

1. **¿El registro es confiable?** EEG tranquilo, impedancias bajas y parejas, y un ruido residual que permita decidir algo.
2. **¿Se repite?** Una onda que no está en las dos réplicas, o en las dos mitades del mismo promedio, no es una onda.
3. **¿Se comporta como una onda V?** Al bajar la intensidad, la V se achica y se **atrasa**. Lo que no se mueve, no es V.
4. **¿Sobrevive a los controles?** Cambiar la polaridad, pinzar el tubo, relajar al paciente, cambiar la ventana.
5. **¿Calza con lo demás?** Audiograma, timpanometría, emisiones y lo que cuenta el paciente.

:::ayuda Ayuda memoria
Antes de marcar una onda: **ruido bajo, se repite, migra con la intensidad, resiste los controles, calza con el resto**. Antes de decir "no hay respuesta": **¿el ruido residual era lo bastante bajo como para verla?**
:::

## Fisiología

### Qué hay entre los electrodos

Los electrodos recogen la suma de todo lo que genera voltaje bajo la piel de la cabeza. Una pequeña parte es la respuesta de tronco que buscamos. El resto es **ruido**: el EEG de fondo (la actividad eléctrica de la corteza, de decenas de microvoltios), la actividad de los músculos del cuello y la cara, el movimiento de los electrodos y la corriente de la red eléctrica. La onda V de un adulto con audición normal mide entre **0,4 y 0,5 µV** (Da Silva Nunes y Gentile Matas, 2005), de modo que en un solo barrido la respuesta es invisible: está enterrada en un ruido que la supera varias veces (Picton, 2010).

### Por qué el promedio mejora con la raíz de los barridos

Se repite el estímulo muchas veces y se suma, en cada repetición, el tramo de registro que sigue al estímulo. Dos cosas distintas ocurren al sumar:

- **La respuesta** aparece en cada barrido con la misma forma y a la misma latencia. Al sumar N barridos se suma N veces: su tamaño crece **en proporción a N**.
- **El ruido** no tiene relación con el estímulo: en un barrido es positivo, en otro negativo, al azar. Al sumar N barridos, los valores se compensan en parte y el total crece solo **en proporción a la raíz de N**.

Al dividir por N para obtener el promedio, la respuesta conserva su tamaño y el ruido que queda, el **ruido residual**, cae como **1/√N** (Picton y cols., 1983; Picton, 2010). De ahí salen las dos reglas prácticas del capítulo:

- Para dejar el ruido residual a **la mitad** hay que promediar **cuatro veces más** barridos. De 250 a 1.000 el ruido baja a la mitad; de 1.000 a 4.000, otra vez a la mitad.
- Cada mejora cuesta más que la anterior. A 21,1 estímulos por segundo, 2.000 barridos toman unos 95 segundos y 4.000 toman unos 190, sin contar los barridos rechazados, que no cuentan y alargan el examen.

:::imagen ilustraciones/cap18-raiz.svg ancho=80% Cuánto cae el ruido residual al aumentar los barridos, con la regla de 1/√N desde 250 barridos. Mira cómo se aplana la curva: cada mitad de ruido que ganas cuesta cuatro veces más barridos.
:::

El argumento vale mientras el ruido sea **aleatorio y sin relación con el estímulo**. Lo que **sí** guarda relación con cada estímulo (un artefacto eléctrico del transductor, un músculo que se contrae reflejamente con cada click) se suma como la respuesta y no se promedia hacia abajo. Ese es el hilo del resto del capítulo: el promedio limpia el ruido, pero no distingue una respuesta auditiva de cualquier otra cosa que se repita con cada estímulo.

### FSP y ruido residual: lo que mira el equipo

A ojo cerca del umbral es fácil equivocarse, y por eso el equipo calcula dos números. El **ruido residual** estima cuánto ruido queda en el promedio (Don y Elberling, 1994). El **FSP** (*F single point*) compara la variabilidad de la señal promediada, en una ventana donde se espera la respuesta, con el ruido estimado a partir de los mismos barridos (Elberling y Don, 1984): sin respuesta vale alrededor de 1, y un valor de **3,1** o más se toma como detección con 99 % de confianza (→ H10, paso 4). Para decidir cuándo parar se usan los dos juntos (Don y Elberling, 1996): se sigue hasta que el FSP cruza el criterio o hasta que el ruido residual es tan bajo que una respuesta del tamaño esperable ya se habría visto.

Dos precauciones. El criterio es una prueba estadística: con un 99 % de confianza, una de cada cien veces que se mira un registro sin respuesta marcará una detección falsa, y cada nivel de la serie es una oportunidad más. Y la ausencia de respuesta solo se afirma con **ruido residual bajo**: un FSP de 1 con ruido alto no dice "no hay onda", dice "no se alcanza a ver".

:::ayuda-ancho Barridos, ruido y tiempo, a 21,1 estímulos por segundo
| Barridos | Tiempo aproximado | Ruido residual relativo |
|---|---|---|
| 250 | 12 s | 100 % |
| 500 | 24 s | 71 % |
| 1.000 | 47 s | 50 % |
| 2.000 | 95 s | 35 % |
| 4.000 | 190 s | 25 % |
:::

Los tiempos son el cociente entre los barridos y la tasa; el ruido relativo es 1/√N tomando 250 barridos como 100 %.

### Rechazo de artefactos

Algunos barridos son tan ruidosos (el paciente tragó, se movió, se tensó) que llevan el promedio al desastre. Por eso el equipo **rechaza** cualquier barrido cuyo voltaje supera un límite y no lo suma. El límite es un parámetro del equipo. Si es muy estricto, casi ningún barrido entra y el examen no avanza; si es muy laxo, entran barridos sucios y el promedio se contamina. Rechazar protege, pero no hace milagros: un paciente que se mueve sigue siendo un registro lento. El remedio es antes del examen: dormido, acostado, con el cuello suelto (→ H10).

### Filtros, polaridad y ventana: lo que el equipo hace antes de dibujar

Tres decisiones del equipo modifican lo que se ve, y cada una tiene un costo.

- **Los filtros** dejan pasar la banda donde está la energía del ABR y sacan el resto: el pasa alto elimina el EEG lento y la deriva; el pasa bajo, el ruido eléctrico y muscular de frecuencia alta. La rutina del libro es **100 a 3.000 Hz**. Un pasa alto demasiado alto le quita parte de la energía a la respuesta misma y la achica; uno demasiado bajo deja pasar la deriva y el ruido lento; un pasa bajo muy bajo redondea y funde las ondas (Picton, 2010). Con **filtros analógicos o causales** de un equipo real, el filtrado además **corre las latencias**: frente a un filtro de fase cero, el pasa alto convencional achica más las ondas y adelanta la V, con más variabilidad entre registros (Kavanagh y Franks, 1989). Las figuras de este libro usan filtros de fase cero, que no las corren.
- **La polaridad** del estímulo (rarefacción, condensación o alternada) cambia el sentido en que se mueve el tímpano. El artefacto eléctrico del transductor y la microfónica coclear **invierten su signo** con la polaridad; la respuesta neural, en lo esencial, no. Al **alternar**, esas dos cancelan al promediar y la respuesta neural queda. El precio: se promedian dos respuestas de latencia apenas distinta y las ondas se ensanchan un poco. En rarefacción la onda I sale antes y más clara (Stockard y cols., 1979; → H10).
- **La ventana** es el tramo de tiempo que se registra después de cada estímulo. La rutina del libro es de 10 a 12 ms. Hay que cubrir la V incluso cuando está atrasada: cerca del umbral, en un oído con pérdida, en un lactante. Una ventana corta la deja afuera. Una ventana larga muestra componentes tardíos que la rutina no ve, entre ellos el que sigue.

### Un músculo que contesta al sonido

Detrás de la oreja está el músculo auricular posterior. Con sonidos intensos se contrae de forma refleja y da una respuesta que los electrodos del mastoides o del lóbulo recogen sin querer: la **respuesta postauricular** (PAMR), una onda ancha de latencia cercana a **12 a 15 ms** (O'Beirne y Patuzzi, 1999). Es una respuesta real al sonido, pero no es auditiva de tronco: es muscular. Su amplitud varía con la tensión del paciente y con la posición de los ojos (Patuzzi y O'Beirne, 1999a), y por eso aparece y desaparece entre registros. En una ventana de rutina de 12 ms solo asoma su comienzo; si se abre la ventana, se ve entera. El PAMR se ha estudiado también como una respuesta útil por sí misma (Purdy y cols., 2005), pero en un ABR es un contaminante.

:::comentario Lo que dicen las normas
En personas reales el primer pico de la PAMR está entre 12,5 y 15 ms según la intensidad y el tono del músculo, y puede registrarse a menos de 20 dB del umbral subjetivo (O'Beirne y Patuzzi, 1999); al bajar el estímulo su amplitud cae y su latencia se alarga (Purdy y cols., 2005). En un registro real lo que la separa de la V es la latencia absoluta, el tamaño, el ancho y su dependencia del tono muscular y de la mirada.
:::

## Patología

No hay un cuadro clínico en este capítulo, sino **un catálogo de errores del registro**: de qué manera un trazo puede mentir, qué conclusión falsa produce y qué lo delata.

:::ayuda-ancho Lo que engaña, el error que provoca y cómo se descubre
| El registro | La conclusión equivocada | Lo que lo delata |
|---|---|---|
| **Pocos barridos** o ruido alto | "No hay respuesta"; umbral demasiado alto; una pérdida que no existe | FSP bajo **con ruido residual alto**; seguir promediando lo cambia |
| **Artefacto de estímulo** (supraaural, vibrador, nivel alto) | Una onda I que no es de la cóclea; latencias y amplitudes sin sentido | Está desde 0 ms, crece con el nivel, **sigue con el tubo pinzado**, se cancela alternando |
| **Respuesta postauricular** | Una "V" tardía; un retrococlear que no existe | Tarda 12 a 15 ms, es más grande que el ABR, **no migra** con la intensidad y se va al relajar al paciente |
| **Falsa onda V** | Un umbral demasiado bajo; audición donde no hay | Está en **una sola mitad** del promedio, **no migra**, el FSP no la confirma |
| **Filtros, polaridad o ventana mal puestos** | Ondas que faltan o se deforman; latencias contra una norma que no corresponde | Las ondas cambian al cambiar el ajuste; se compara con la norma del mismo ajuste |
| **Red eléctrica** | Una onda regular cada 20 ms (50 Hz) que parece respuesta | Es periódica y no cambia con el nivel (→ H10) |
:::

:::sabias ¿Sabías que?
Una de las razones de usar una tasa decimal como 21,1 estímulos por segundo es que ese número no es un divisor de la frecuencia de la red eléctrica, de modo que el ruido de red no cae siempre en la misma fase respecto del estímulo y el promedio lo cancela mejor (→ H10).
:::

## Razonamiento

### Un orden fijo para dudar de un trazo

Cuando algo se ve distinto de lo esperado, el reflejo es dudar del paciente. El orden de este capítulo es dudar primero del registro:

1. **¿El registro es confiable?** Mira el EEG, las impedancias, los barridos aceptados y rechazados, el ruido residual. Si el ruido es del tamaño de la onda que buscas, no puedes decidir nada, ni a favor ni en contra.
2. **¿Se repite?** Mira las réplicas y las dos mitades del promedio. Una onda real está en todas.
3. **¿Migra?** Compara con el nivel siguiente. La V verdadera se achica y se atrasa al bajar. Lo que se queda quieto, sea una onda perfecta o no, no es V.
4. **¿Resiste los controles?** Alterna la polaridad, pinza el tubo, relaja al paciente, abre la ventana.
5. **¿Calza con lo demás?** Un ABR peor que el audiograma hace sospechar un registro malo antes que una pérdida; uno mejor que lo que el paciente da por voluntad hace sospechar una pérdida no orgánica (→ cap. 19).

### Lo que más se equivoca

- **Parar por apuro.** Es el error que más pérdidas inventa: con pocos barridos la onda de la zona del umbral no sale del ruido y el umbral queda más alto de lo real.
- **Marcar una onda sin mirar el nivel de abajo.** Si no hay nada que migre, no hay V.
- **Creer en la réplica como prueba única.** Replicar es necesario, pero no suficiente: el artefacto de estímulo y el postauricular también se repiten. La falsa onda V es la que falla en replicar, y por eso es la más fácil de descubrir si se mira.
- **Comparar con una norma que no es del registro.** Otro transductor, otra polaridad, otros filtros, otra ventana.

:::pregunta Pregunta abierta
Obtienes un trazo con una onda perfecta a 5,6 ms a 40 dB nHL en un oído que el audiograma da como sordo. ¿Qué tres cosas pedirías mirar antes de dudar de la audiometría?
:::

## Casos

Los pacientes son corrientes: sus oídos son los de siempre. En cada caso hay dos tipos de figura. El **ABR limpio** del paciente, tal como lo toma el equipo bien puesto, es la referencia. El **registro que engaña** es el mismo oído con el artefacto o el ajuste equivocado, simulado: no es el registro de un paciente real.

{{caso cap18_barridos}}

:::pregunta Paso 1 · ¿Qué datos importan?
Un técnico recién titulado de 23 años, sin síntomas, con audiometría normal. Un alumno en práctica le hace un ABR "para completar", promedia **250 barridos por curva** para no demorar y concluye: "V presente hasta 40 dB nHL; a 20 dB no hay respuesta; **umbral 40 dB nHL**". ¿Qué dato de la historia no calza con ese umbral?
:::

:::pregunta Paso 2 · Tus hipótesis
Plantea tres explicaciones para que un oído con audiograma normal tenga un umbral de ABR de 40 dB nHL. ¿Cuál es la menos probable y cuál es la primera que descartarías?
:::

:::pregunta Paso 3 · ¿Qué pedirías y por qué?
Antes de repetir nada, ¿qué dos números del equipo te dirían si el registro de 20 dB sirve para decidir que "no hay respuesta"?
:::

#### Paso 4 · Los resultados

:::imagen figuras/salida/cap18_barridos_impedancia.svg ancho=100% Impedanciometría del técnico.
:::

Timpanograma A en los dos oídos, con compliancia de 0,76 mL en el OD y de 0,51 mL en el OI. Los reflejos están presentes de 85 a 95 dB SPL, ipsi y contra, y el decay es negativo. La audiometría tiene 0 dB en todas las frecuencias. El oído medio está sano: lo que falló fue el registro.

:::figura cap18_barridos abr
- @OD 80 V | La V llega a 5,6 ms. Con el equipo bien puesto el paciente tiene todas las ondas a 80 dB.
- @OD 40 V | A 40 dB la V está a 6,7 ms: ahí coincide con lo que anotó el alumno.
- @OD 20 V | A 20 dB la V existe y se ve, a 7,7 ms. Es la curva que el alumno declaró "sin respuesta".
- @OD 10 V | A 10 dB la V sigue ahí, a 8,3 ms, en las dos réplicas: el **umbral del paciente está en 10 dB nHL o más abajo**, como dice su audiometría.
:::

:::imagen ilustraciones/cap18-promedio.svg ancho=92% El mismo oído a 20 dB nHL, de 250 a 4.000 barridos, con la mitad A del promedio en azul y la mitad B en rojo. Mira en qué fila empiezan a coincidir las dos mitades: recién ahí se puede decir que hay respuesta, y antes tampoco se podía decir que no la había.
- @92,13 | **250 barridos:** FSP de 2,4, bajo el criterio de 3,1, y las dos mitades no se parecen. Los picos de ruido son del tamaño de lo que se busca: aquí no se puede decir ni que hay ni que no hay respuesta.
- @92,40 | **1.000 barridos:** el ruido residual bajó de 96 a 55 nV y el FSP (5,1) ya pasa el criterio de 3,1, pero las mitades todavía no se pegan del todo.
- @92,77 | **4.000 barridos:** el ruido residual es de 28 nV y el FSP, de 15,3. La onda de 7,5 ms está en las dos mitades.
:::

:::docente Guía del caso
- **Datos clave:** audiograma normal, sin síntomas, examen preocupacional; el alumno dio por cerrada una curva con ruido alto.
- **Hipótesis:** pérdida leve oculta, oído medio (descartado por la timpanometría), **registro insuficiente**. La tercera es la más probable y la que más veces se comete.
- **Qué pedir:** los barridos aceptados, el FSP y el **ruido residual** de la curva de 20 dB; y, sobre todo, seguir promediando.
- **Errores esperables:** pasar de "sin respuesta" a "umbral 40" sin mirar el ruido; contentarse con el FSP bajo sin mirar el ruido residual.
- **Para discutir:** Repetir el ejercicio con 500, 1.000 y 2.000 barridos y ver cómo sube el umbral (→ H10, paso 4).
:::

{{caso cap18_supraaural}}

:::pregunta Paso 1 · ¿Qué datos importan?
Un operador de chancador de 47 años, con acúfeno bilateral y una audiometría con caída en 4 kHz. Su ABR lo hizo un colega en otro centro, **con fonos supraaurales** (los de inserción no estaban), a **100 dB nHL en condensación**. El informe dice: "onda I a 0,6 ms, muy grande, y V a 4,7 ms: intervalo I-V acortado". ¿Qué te llama la atención de esa onda I?
:::

:::pregunta Paso 2 · Tus hipótesis
¿Qué dos explicaciones hay para una "onda I" que aparece antes de que el sonido haya tenido tiempo de llegar a la cóclea? ¿Cuál está en la configuración del examen?
:::

:::pregunta Paso 3 · ¿Qué pedirías y por qué?
¿Qué dos maniobras sencillas, sin cambiar de paciente, te dirían si esa deflexión es una respuesta?
:::

#### Paso 4 · Los resultados

:::imagen figuras/salida/cap18_supraaural_audiosupra.svg ancho=100% Audiometría del paciente de este caso: caída de agudos con recuperación en 8 kHz en los dos oídos y la voz casi normal.
:::

Caída en 3 a 6 kHz, de daño por ruido, con 70 dB en 4 kHz en los dos oídos, 75 dB en 6 kHz en el OI y recuperación en 8 kHz (50 y 55 dB). SDT de 5 y 10 dB, SRT de 10 y 15 dB; discriminación de 92 % a 50 dB en el OD y 84 % a 55 dB en el OI. SISI de 90 %, Carhart sin deterioro en 2 y 4 kHz y Metz de 24,5 dB en 4 kHz: recluta, es coclear. No hay nada en la audiometría que acorte los intervalos del ABR.

:::figura cap18_supraaural abr
- @OI 100 I | Con fono de inserción y polaridad alternada, la I del OI llega a 1,2 ms.
- @OI 100 V | Y la V, a 5,6 ms. Interpico I-V de 4,4 ms.
- @OD 60 V | En el OD la V pasa de 5,5 ms a 100 dB a 6,0 a 80 y a 6,6 a 60 dB: la V migra.
:::

:::imagen ilustraciones/cap18-estimulo.svg ancho=92% El mismo oído a 100 dB nHL con distintas condiciones del estímulo. Arriba, la referencia: inserción y polaridad alternada. Segunda fila: fono supraaural en condensación. Tercera: supraaural alternada. Abajo: inserción con el tubo pinzado. Compara el primer milisegundo de cada fila: lo que aparece antes de que el sonido pueda llegar a la cóclea es el estímulo, no una onda.
- @92,19 | **Referencia.** Inserción y alternada: el primer milisegundo está limpio; la V cae cerca de 5,5 ms.
- @92,42 | **Supraaural, condensación.** Una deflexión grande **desde 0 ms**, antes de que el sonido pueda llegar a la cóclea: es el estímulo, no una onda. Se lee como una "I" temprana y enorme.
- @92,65 | **Supraaural, alternada.** El artefacto casi desaparece, pero la V llega unos 0,8 ms antes que con inserción: sin el tubo, el sonido llega antes.
- @92,86 | **Inserción con tubo pinzado.** No llega sonido y no hay ondas; lo que queda en el primer milisegundo es el artefacto. Esta es la maniobra que separa estímulo de respuesta.
:::

:::docente Guía del caso
- **Datos clave:** transductor supraaural, nivel alto, una sola polaridad, onda "I" a menos de 1 ms.
- **Hipótesis:** onda I con latencia anormal (no existe una I a 0,6 ms con ese estímulo), **artefacto de estímulo**.
- **Qué pedir:** repetir con **fono de inserción** y polaridad **alternada**; si no hay otro transductor, **pinzar el tubo** (con inserción) o comparar polaridades; mirar si la deflexión crece con la intensidad.
- **Errores esperables:** medir interpicos sobre una onda que es el estímulo; comparar las latencias absolutas con una norma hecha con fonos de inserción.
- **Para discutir:** El artefacto del transductor se ve con claridad con el supraaural y el vibrador.
:::

{{caso cap18_postauricular}}

:::pregunta Paso 1 · ¿Qué datos importan?
Un carpintero jubilado de 74 años con una presbiacusia clásica. Se hizo un ABR por curiosidad, a 100 dB nHL, con la **ventana abierta a 25 ms** "para ver todo". El informe: "onda V con latencia de 13 ms; I-V muy prolongado: sospecha de lesión retrococlear". ¿Qué te dice la edad y el audiograma sobre las ondas que esperarías?
:::

:::pregunta Paso 2 · Tus hipótesis
Una onda grande y ancha a 13 ms en un anciano con una pérdida simétrica: ¿lesión retrococlear, o algo que no es nervio?
:::

:::pregunta Paso 3 · ¿Qué pedirías y por qué?
Sin cambiar de paciente, ¿qué mirarías al bajar la intensidad para saber si esa onda es la V?
:::

#### Paso 4 · Los resultados

:::figura cap18_postauricular abr
- @OD 90 V | Con la ventana de rutina, a 90 dB la V del OD llega a 5,9 ms. Esa es la onda V de este paciente; es chica porque tiene 74 años.
- @OD 70 V | A 70 dB la V se atrasa a 6,3 ms, y a 60 dB, a 6,9. A 50 dB ya no hay V.
:::

:::imagen ilustraciones/cap18-pam.svg ancho=92% El oído derecho con una respuesta postauricular y la ventana abierta a 25 ms, de 100 a 60 dB nHL. Las dos mitades del promedio coinciden en todo el trazo, así que replicar no basta: lo que delata a la onda muscular es que no se atrasa al bajar la intensidad, como sí lo hace la V.
- @92,11 | **100 dB.** Una onda grande y ancha a 13 ms, mucho más que cualquier onda del ABR. Con una ventana de 12 ms solo se vería su comienzo.
- @92,27 | **90 dB.** La V verdadera (verde, a 5,9 ms) es chica; la de 13 ms es varias veces mayor. Y las dos mitades **coinciden**: replicar no la descarta.
- @92,66 | **70 dB.** La onda tardía ya casi no está; la V de 6,3 ms está atrasada y chica, como corresponde.
- @92,88 | **60 dB.** Sin respuesta tardía. La V verdadera se achica de a poco y se atrasa; la onda muscular no se atrasa: cambia de tamaño o desaparece.
:::

:::docente Guía del caso
- **Datos clave:** 74 años, pérdida simétrica, ventana de 25 ms, onda ancha a 13 ms.
- **Hipótesis:** lesión retrococlear (no: la pérdida es simétrica y no hay otros signos), **respuesta postauricular** de un paciente tenso con sonido intenso.
- **Qué pedir:** volver a la ventana de rutina; registrar a un nivel menor y comparar: la V se achica y se atrasa; la onda muscular no se atrasa, cambia de tamaño o desaparece <!-- Pasada de fundamentos 2026-10-18: decía "la respuesta muscular suele caer antes que la V" con un verificar. O'Beirne y Patuzzi 1999 la registran a menos de 20 dB del umbral subjetivo y Purdy 2005 la obtuvo con clicks de 20 dB nHL en la mitad de los normoyentes en la condición menos favorable: no cae de forma fiable antes que la V; la literatura sobre su latencia está en el recuadro de Fisiología. -->; relajar al paciente, **cuello suelto y cabeza apoyada**; revisar la posición de los electrodos.
- **Errores esperables:** marcar V en el máximo más grande de la pantalla; "interpretar" interpicos con un componente muscular.
- **Para discutir:** Con la ventana de 12 ms asoma solo el comienzo de la respuesta postauricular; se ve entera al abrir la ventana.
:::

{{caso cap18_cofosis}}

:::pregunta Paso 1 · ¿Qué datos importan?
Un garzón de 22 años que no oye por el oído derecho desde que tiene memoria: se lo encontraron en el control de salud del colegio y nunca le hicieron otro estudio. Un ABR del oído derecho, hecho con fonos de inserción, informa: "V presente a 5,6 ms entre 70 y 40 dB nHL; **umbral de 40 dB**, audición residual". ¿Con qué dato de su historia choca?
:::

:::pregunta Paso 2 · Tus hipótesis
¿Qué tres explicaciones tendría una onda "V" en un oído con una pérdida profunda desde la infancia? ¿Qué cambiaría si el estímulo fuera de 100 dB en lugar de 70?
:::

:::pregunta Paso 3 · ¿Qué pedirías y por qué?
Mira solo la latencia de esa onda en cuatro niveles seguidos. ¿Qué esperarías de una V verdadera?
:::

#### Paso 4 · Los resultados

:::imagen figuras/salida/cap18_cofosis_audiosupra.svg ancho=100% Audiometría del paciente de este caso: oído derecho con pérdida profunda, oído izquierdo normal.
:::

El oído derecho tiene de 90 a 100 dB HL en todas las frecuencias, con el OI enmascarado; SDT de 90 dB y SRT de 95, y solo discrimina 36 % a 110 dB: es una **pérdida profunda**, casi una cofosis, y coincide con lo que cuenta el paciente. El OI tiene SDT de −5 dB, SRT de 0 dB y discrimina 100 % a 30 dB.

:::imagen figuras/salida/cap18_cofosis_impedancia.svg ancho=100% Impedanciometría del garzón.
:::

Timpanograma A en los dos oídos, con compliancia de 0,54 mL en el OD y de 1,51 mL en el OI. Cuando el sonido va al OD no hay reflejo, ni ipsi ni contra, porque ese oído no lo recibe. Cuando va al OI aparece en los dos oídos, de 85 a 95 dB SPL, y el decay es negativo.

:::figura cap18_cofosis abr
- @OI 100 V | El oído izquierdo es normal: I, III y V a lo esperable (V a 5,4 ms).
- @OD 100 | A 100 dB el trazo del **oído derecho** muestra una onda con réplicas, hacia los 7 ms (sin V propia hasta ese nivel): es real, pero **no es del derecho**. Es la respuesta del oído izquierdo, que el estímulo alcanza por vía ósea a través del cráneo (la curva sombra; → H10 y H4). Se enmascara y desaparece.
:::

:::imagen ilustraciones/cap18-falsa-v.svg ancho=92% El oído derecho con pérdida profunda, de 70 a 40 dB nHL, con una falsa onda V. En azul la mitad A del promedio, en rojo la mitad B. Dos cosas la delatan: vive en una sola mitad y no se mueve al bajar la intensidad.
- @92,19 | **70 dB.** Una "V" perfecta a 5,6 ms, pero solo en la **mitad A**; la B está plana. El FSP no la confirma.
- @92,42 | **60 dB.** Misma latencia, misma altura: bajó 10 dB y la onda no se movió. Una V verdadera se atrasa y se achica.
- @92,64 | **50 dB.** Idéntica otra vez. Un artefacto se queda quieto.
- @92,86 | **40 dB.** La "V" sigue a 5,6 ms, en un oído que casi no oye. El ruido residual es el de siempre y el FSP no pasa de 1,3.
:::

:::docente Guía del caso
- **Datos clave:** pérdida profunda del OD desde la infancia, de causa nunca estudiada (detectada en el control escolar), audición normal en el OI, ninguna prueba previa.
- **Dos trampas distintas:** a nivel **alto** (100 dB) lo que aparece en el oído sordo es la **curva sombra**, una respuesta real del oído sano; a nivel **bajo** (70 a 40 dB) lo que aparece es una **falsa onda V**, un artefacto que quedó en una parte de los barridos y no se mueve con la intensidad.
- **Qué pedir:** enmascarar el oído sano; mirar las dos mitades del promedio; comparar latencias entre niveles; contrastar con el audiograma y la historia.
- **Errores esperables:** concluir audición residual por una sola onda bonita; no preguntar qué dicen las otras pruebas.
- **Para discutir:** Es el ejercicio para aprender a pedir los subpromedios A y B.
:::

{{caso cap18_configuracion}}

:::pregunta Paso 1 · ¿Qué datos importan?
Una profesora de 46 años con crisis de vértigo y plenitud del oído izquierdo, con una pérdida de graves en ese oído. Un ABR del oído izquierdo se tomó con el equipo "como estaba": **ventana de 6 ms**, pasa alto en 300 Hz y pasa bajo en 1.000 Hz, polaridad al azar. El informe: "sin respuesta a 50 dB; V solo a 80 dB; umbral **80 dB nHL**". ¿Qué tiene de raro un umbral de 80 en un oído que da 20 dB en agudos?
:::

:::pregunta Paso 2 · Tus hipótesis
Sin cambiar de oído, ¿qué parámetros del equipo pudieron esconder una onda que está presente? ¿Cuál es el más sencillo de revisar?
:::

:::pregunta Paso 3 · ¿Qué pedirías y por qué?
¿A qué latencia esperas la V a 50 dB en este oído? ¿Cabe en una ventana de 6 ms?
:::

#### Paso 4 · Los resultados

:::imagen figuras/salida/cap18_configuracion_impedancia.svg ancho=100% Impedanciometría de la profesora.
:::

Timpanograma A en los dos oídos, con compliancia de 0,45 mL en el OD y de 0,58 mL en el OI. Los reflejos están presentes de 85 a 95 dB SPL, ipsi y contra, y el decay es negativo. Ni el oído medio ni el reflejo explican un umbral de 80 dB.

:::figura cap18_configuracion abr
- @OI 80 V | A 80 dB la V del oído izquierdo llega a 5,6 ms.
- @OI 50 V | A 50 dB está a 6,4 ms. Con una ventana de 6 ms **queda afuera**.
- @OI 30 V | A 30 dB, a 7,7 ms, cerca del umbral. A 10 dB ya no hay V. Un umbral buscado con la ventana corta se detiene en el nivel donde la V todavía cabe.
:::

:::imagen ilustraciones/cap18-polaridad.svg ancho=92% El oído izquierdo con distintas polaridades a 80 dB nHL y con ventana de 12 y de 6 ms a 50 dB nHL. Arriba, otra polaridad cambia la forma y deja de valer la norma de rutina; abajo, la ventana corta deja la V afuera y el oído parece no responder.
- @92,19 | **Alternada.** Es la referencia de rutina: V clara cerca de 5,6 ms.
- @92,33 | **Rarefacción.** La forma cambia un poco (las ondas tempranas salen antes y más claras en rarefacción; Stockard y cols., 1979); la V se mantiene.
- @92,47 | **Condensación.** Más chica la onda I y distinta la forma. Con otra polaridad, la norma de rutina no vale.
- @92,64 | **Ventana de 12 ms, 50 dB.** La V está, a 6,7 ms.
- @92,84 | **Ventana de 6 ms, 50 dB.** El mismo oído: aquí no hay nada. La onda no se fue; se cortó.
:::

:::imagen ilustraciones/cap18-filtros.svg ancho=92% El mismo oído a 80 dB nHL con cuatro bandas de filtro. Solo la de rutina deja las ondas como las espera la norma: las otras achican, ensucian o redondean el trazo.
- @92,17 | **100-3.000 Hz**, la rutina.
- @92,38 | **Pasa alto de 300 Hz.** El trazo se aplana y se achica: se le quitó parte de la energía de la respuesta, y con un equipo real, además, se correrían las latencias.
- @92,60 | **Pasa alto de 30 Hz.** Entra la deriva lenta y las mitades A y B se separan: hay más ruido y el promedio tarda más en ser confiable.
- @92,82 | **Pasa bajo de 1.000 Hz.** Las ondas se redondean y se funden: lo que eran I, III y V se ve como lomas.
:::

:::docente Guía del caso
- **Datos clave:** ventana de 6 ms, filtros angostos, polaridad distinta a la de la norma; umbral que no calza con la audiometría.
- **Hipótesis:** pérdida del oído medio o neural (no: no hay datos), **registro mal configurado**. Se revisa antes que el paciente.
- **Qué pedir:** ventana de 10 a 12 ms, filtros de 100 a 3.000 Hz, polaridad alternada y repetir la serie.
- **Errores esperables:** informar un umbral que sale de la ventana y no del oído; comparar con la norma de rutina sin igualar los ajustes.
- **Para discutir:** El equipo viene sin configurar (tasa, filtros y ventana) y nada avisa qué está mal.
:::

## Resolución de los casos

Intenta resolver cada caso con los pasos del aprendizaje basado en problemas antes de leer esta sección.

### Caso 18.1

#### Razonamiento

El audiograma es normal y el paciente no tiene síntomas: un umbral de 40 dB nHL no calza con nada. Antes de pensar en una pérdida, se piensa en el registro, y el registro tiene lo que lo delata: **250 barridos** por curva. Con tan pocos barridos el ruido residual es del tamaño de lo que se busca, el FSP queda bajo y las dos mitades del promedio no se parecen. "Sin respuesta" con ese ruido no significa nada. Al seguir promediando, la onda que estaba tapada aparece, en las dos mitades, y el umbral baja a 10 dB nHL.

#### Diagnóstico y qué sigue

ABR normal con onda V presente hasta 10 dB nHL, el nivel más bajo registrado. El registro anterior no se informa como pérdida: se rehace con más barridos.

Informe del registro bien hecho:

:::comentario-ancho Informe de Enrique, 23 años (caso 18.1)
**Motivo**: práctica de ABR en un voluntario sin síntomas, con audiometría normal.

**Registro**: click a 80, 40, 20, 10 y 0 dB nHL. Polaridad alternada, 21,1 estímulos/s, filtros de 100 a 3.000 Hz, ventana de 12 ms, fonos de inserción, montaje Cz-mastoides con impedancias bajo 5 kΩ. 4.000 barridos por curva con réplica cerca del umbral. En reposo.

**Referencia**: hombre de 18 a 49 años, por oído (Sanfins y cols., 2026): límite superior (media + 2 DE).

| | OD | OI | Límite OD / OI |
|---|---|---|---|
| Onda I | 1,47 | 1,67 | 1,80 / 1,80 |
| Onda III | 3,77 | 3,77 | 4,05 / 4,14 |
| Onda V | 5,63 | 5,67 | 6,03 / 6,05 |
| I-III | 2,30 | 2,10 | 2,45 / 2,61 |
| III-V | 1,86 | 1,90 | 2,33 / 2,11 |
| I-V | 4,16 | 4,00 | 4,49 / 4,52 |
| Diferencia interaural de la V | 0,04 | | hasta 0,4 |
| Umbral con click (dB nHL → dB eHL) | 10 → 5 | 10 → 5 | hasta 20 dB eHL |

**Morfología**: ondas I, III y V bien definidas y replicables en los dos oídos a 80 dB nHL.

**Interpretación**: latencias, interpicos y diferencia interaural dentro de la norma. Onda V presente hasta 10 dB nHL y ausente a 0, con ruido residual bajo.

**Conclusión**: examen sugiere audición normal en ambos oídos, para el rango frecuencial estudiado de 2 a 4 kHz.

**Recomendación**: ninguna.
:::

:::ayuda Ayuda memoria
Un "no hay respuesta" solo vale si el **ruido residual** era lo bastante bajo como para verla. Con ruido alto, lo único que se puede decir es "no se ve".
:::

### Caso 18.2

#### Razonamiento

Una "onda I" a 0,6 ms no puede ser neural con ese estímulo: el sonido ni siquiera ha tenido tiempo de llegar a la cóclea y generar un potencial del nervio. Lo que hay ahí es el **artefacto electromagnético del transductor**, que es peor con el fono supraaural y con intensidad alta, y que con una sola polaridad no se cancela. Alternar lo cancela, y con fonos de inserción, pinzar el tubo lo demuestra: el sonido deja de llegar, las ondas desaparecen y el artefacto sigue (BSA, 2019). Además, la V de un supraaural llega antes que la de la inserción, porque no hay tubo que retrase el sonido: las latencias de la norma, medidas con inserción, no valen.

#### Diagnóstico y qué sigue

El intervalo I-V "acortado" no es un hallazgo: se midió sobre un artefacto. Se repite con fonos de inserción y polaridad alternada. Con el registro limpio, la I llega a 1,2 ms (OI) y la V a 5,5 ms, sin alteración neural.

Informe del registro bien hecho:

:::comentario-ancho Informe de Roberto, 47 años (caso 18.2)
**Motivo**: acúfeno bilateral y audiometría con caída en agudos; operador de chancador.

**Registro**: click a 100, 80, 60, 50 y 40 dB nHL. Polaridad alternada, 21,1 estímulos/s, filtros de 100 a 3.000 Hz, ventana de 12 ms, fonos de inserción, montaje Cz-mastoides con impedancias bajo 5 kΩ. Sin artefacto en el primer milisegundo. En reposo.

**Referencia**: hombre de 18 a 49 años, por oído (Sanfins y cols., 2026): límite superior.

| | OD | OI | Límite OD / OI |
|---|---|---|---|
| Onda I (100 dB nHL) | no se identifica | 1,20 | 1,80 / 1,80 |
| Onda III (100 dB nHL) | 3,63 | 3,53 | 4,05 / 4,14 |
| Onda V (100 dB nHL) | 5,53 | 5,57 | 6,03 / 6,05 |
| I-III | | 2,33 | / 2,61 |
| III-V | 1,90 | 2,04 | 2,33 / 2,11 |
| I-V | | 4,37 | / 4,52 |
| Onda V (80 dB nHL) | 5,97 | 6,17 ↑ | 6,03 / 6,05 |
| Umbral con click (dB nHL → dB eHL) | 60 → 55 | 60 → 55 | hasta 20 dB eHL |

**Morfología**: ondas III y V replicables en los dos oídos; la I solo se identifica en el OI a 100 dB nHL.

**Interpretación**: a 100 dB nHL, interpicos y latencias dentro de la norma. A 80 dB la V del OI pasa el límite por 0,12 ms, lo esperable en una pérdida de agudos de 70 dB, sin interpicos largos. Umbral de 60 dB nHL (55 dB eHL), que corresponde a la zona de 2 a 4 kHz de la audiometría.

**Conclusión**: examen sugiere hipoacusia sensorioneural bilateral, de aproximadamente 55 dB HL para el rango de 2 a 4 kHz. Se adjunta audiometría.

**Recomendación**: control con la audiometría de vigilancia y protección auditiva (→ cap. 33).
:::

:::ojo Ojo clínico
Replicar no descarta un artefacto de estímulo: **se repite en cada barrido, y por eso sobrevive al promedio**. Las pruebas son otras: cambia con la polaridad, no desaparece al pinzar el tubo, crece con la intensidad y empieza en el instante cero.
:::

### Caso 18.3

#### Razonamiento

Una latencia de 13 ms no corresponde a la V de un adulto con una pérdida simétrica: la V de este paciente llega cerca de los 6 ms. La onda de 13 ms es ancha, mucho mayor que cualquier onda del ABR y **se achica al bajar, casi no está a 70 dB y a 60 ya no hay nada, mientras la V verdadera sigue ahí, achicada y atrasada**. Es la respuesta postauricular, un reflejo muscular a sonido intenso. Se repite en las dos mitades del promedio, así que la replicación no la delata; lo que la delata es **dónde está** y **cómo se comporta con la intensidad**. Y la pérdida simétrica de 74 años no aporta ningún motivo para pensar en un retrococlear.

#### Diagnóstico y qué sigue

ABR con onda V de latencia acorde a la edad y a la pérdida, sin signos retrococleares. La onda tardía se atribuye a una respuesta muscular: se repite el registro con el paciente relajado, el cuello suelto y la ventana de rutina.

Informe del registro bien hecho:

:::comentario-ancho Informe de Alberto, 74 años (caso 18.3)
**Motivo**: hipoacusia progresiva y pitido bilateral; ABR por curiosidad.

**Registro**: click a 90, 70, 60 y 50 dB nHL. Polaridad alternada, 21,1 estímulos/s, filtros de 100 a 3.000 Hz, ventana de 12 ms, fonos de inserción, montaje Cz-mastoides con impedancias bajo 5 kΩ. Paciente relajado, cuello suelto y cabeza apoyada.

**Referencia**: hombre de 50 años o más, por oído (Sanfins y cols., 2026): límite superior.

| | OD | OI | Límite OD / OI |
|---|---|---|---|
| Onda I | no se identifica | no se identifica | 1,90 / 1,91 |
| Onda III | 3,97 | 4,03 | 4,16 / 4,22 |
| Onda V | 5,90 | 5,93 | 6,16 / 6,24 |
| III-V | 1,93 | 1,90 | 2,17 / 2,33 |
| Diferencia interaural de la V | 0,03 | | hasta 0,4 |
| Umbral con click (dB nHL → dB eHL) | 60 → 55 | 60 → 55 | hasta 20 dB eHL |

**Morfología**: ondas III y V replicables; sin componente tardío en la ventana de 12 ms.

**Interpretación**: latencias dentro de la norma, interpico III-V normal y sin diferencia entre oídos: sin signos retrococleares. La V se atrasa al bajar el nivel (5,9 ms a 90 dB, 6,3 a 70 y 6,9 a 60).

**Conclusión**: examen sugiere hipoacusia sensorioneural bilateral, de aproximadamente 55 dB HL para el rango de 2 a 4 kHz. Se adjunta audiometría.

**Recomendación**: evaluación para audífonos.
:::

:::sabias ¿Sabías que?
El mismo músculo ha sido estudiado como una respuesta útil: la respuesta postauricular se ha propuesto como una forma de estimar la sensibilidad auditiva (Purdy y cols., 2005). En un ABR, en cambio, es un contaminante que hay que reconocer.
:::

### Caso 18.4

#### Razonamiento

Una pérdida profunda desde la infancia (90 a 100 dB HL) y una V con latencia exacta a 70, 60, 50 y 40 dB nHL son incompatibles: si bajó 30 dB, la V verdadera se habría **atrasado y achicado**. Esa onda no se movió, y el FSP y las mitades lo confirman: vive solo en la mitad A del promedio. Es una **falsa onda V**, un artefacto que quedó en una parte de los barridos y que por casualidad cayó donde se espera la V. A nivel alto, el trazo del oído sordo muestra además una onda que se repite pero que viene del oído sano: es la **curva sombra**, y se descarta enmascarando. Con 90 a 100 dB HL no hay audición que explique una respuesta a 40 dB nHL.

#### Diagnóstico y qué sigue

Pérdida profunda derecha. El ABR del oído derecho no muestra respuesta propia con el oído izquierdo enmascarado. La "V" de 70 a 40 dB es un artefacto; se informa **sin respuesta** y se contrasta con el audiograma.

Informe del registro bien hecho:

:::comentario-ancho Informe de Sergio, 22 años (caso 18.4)
**Motivo**: pérdida de audición derecha desde la infancia, detectada en el control de salud escolar. Sin estudios previos.

**Registro**: click a 100 y 80 dB nHL en el OI, y a 100 dB nHL en el OD con ruido de enmascaramiento en el OI. Polaridad alternada, 21,1 estímulos/s, filtros de 100 a 3.000 Hz, ventana de 12 ms, fonos de inserción, montaje Cz-mastoides con impedancias bajo 5 kΩ. En reposo.

**Referencia**: hombre de 18 a 49 años, OI (Sanfins y cols., 2026): límite superior.

| | OD | OI | Límite OI |
|---|---|---|---|
| Onda I | sin ondas | 1,50 | 1,80 |
| Onda III | sin ondas | 3,77 | 4,14 |
| Onda V | sin ondas | 5,60 | 6,05 |
| I-III | | 2,27 | 2,61 |
| III-V | | 1,83 | 2,11 |
| I-V | | 4,10 | 4,52 |
| Umbral con click (dB nHL → dB eHL) | sin respuesta a 100 → mayor que 95 | no se buscó | |

**Morfología**: OI con ondas I, III y V bien definidas y replicables. OD sin ondas reconocibles, con el OI enmascarado.

**Interpretación**: OI normal. En el OD, la única onda que aparece sin enmascarar es la respuesta del OI por vía ósea (curva sombra); enmascarada desaparece. Ninguna onda de los registros anteriores sobrevive al pedir que se repita en las dos curvas y que migre con el nivel.

**Conclusión**: OD sin ondas reconocibles hasta 100 dB nHL, con enmascaramiento: examen sugiere hipoacusia de grado profundo en OD, para el rango de 2 a 4 kHz. OI normal. Se adjunta audiometría.

**Recomendación**: correlación con la audiometría; evaluación otorrinolaringológica.
:::

:::pregunta Para discutir
¿Y si el audiograma no hubiera existido? ¿Qué te habría dicho la onda a 40 dB si solo hubieras tenido ese registro? ¿Qué habría pasado con ese umbral en un lactante, donde no hay otra prueba que lo desmienta?
:::

### Caso 18.5

#### Razonamiento

El oído de la paciente tiene los graves caídos (45 dB en 125 y 250 Hz, 25 en 1 kHz) y los agudos en 20 dB; no hay razón para un umbral de 80 dB. Lo que hay son tres ajustes inadecuados: una **ventana de 6 ms**, una banda de **300 a 1.000 Hz** y una polaridad que no es la de la norma. La ventana corta es la que más pesa: la V a 50 dB llega a 6,4 ms y a 30 dB, a casi 8 ms, de modo que **no cabe** y el equipo no la registra. Los filtros angostos, además, achican y redondean las ondas.

#### Diagnóstico y qué sigue

ABR del oído izquierdo con onda V hasta 30 dB nHL y sin respuesta a 10 dB, con la configuración de rutina. El registro anterior no se usa para informar: se repite con ventana de 10 a 12 ms, filtros de 100 a 3.000 Hz y polaridad alternada.

Informe del registro bien hecho:

:::comentario-ancho Informe de Noelia, 46 años (caso 18.5)
**Motivo**: crisis de vértigo y plenitud del oído izquierdo, con pérdida de graves.

**Registro**: click a 80, 50, 30, 20, 10 y 0 dB nHL. Polaridad alternada, 21,1 estímulos/s, filtros de 100 a 3.000 Hz, ventana de 12 ms, fonos de inserción, montaje Cz-mastoides con impedancias bajo 5 kΩ. En reposo.

**Referencia**: mujer de 18 a 49 años, por oído (Sanfins y cols., 2026): límite superior.

| | OD | OI | Límite OD / OI |
|---|---|---|---|
| Onda I | 1,43 | 1,43 | 1,80 / 1,80 |
| Onda III | 3,57 | 3,70 | 3,94 / 4,01 |
| Onda V | 5,53 | 5,57 | 5,89 / 5,92 |
| I-III | 2,14 | 2,27 | 2,42 / 2,49 |
| III-V | 1,96 | 1,87 | 2,11 / 2,12 |
| I-V | 4,10 | 4,14 | 4,33 / 4,41 |
| Diferencia interaural de la V | 0,04 | | hasta 0,4 |
| Umbral con click (dB nHL → dB eHL) | 10 → 5 | 30 → 25 | hasta 20 dB eHL |

**Morfología**: ondas I, III y V bien definidas y replicables a 80 dB nHL en los dos oídos.

**Interpretación**: latencias e interpicos normales: sin signos retrococleares. El umbral del OI, 25 dB eHL, queda apenas sobre el límite normal en 2 a 4 kHz; el click no estima los graves, donde está la pérdida mayor de la audiometría.

**Conclusión**: examen sugiere audición normal en OD y, en OI, umbral de 25 dB eHL para el rango frecuencial estudiado de 2 a 4 kHz, sin signos retrococleares. Se adjunta audiometría.

**Recomendación**: umbral por frecuencia con burst o NB chirp si se necesita estimar los graves (→ H10).
:::

:::comentario Comentario
El oído estaba bien: lo que estaba mal era el equipo. Por eso la configuración se revisa antes de registrar, y la norma que uses tiene que estar medida con los mismos filtros, polaridad, tasa y transductor (→ H10).
:::

:::comentario Prevención
- **Cuaternaria:** seguir promediando hasta tener ruido residual bajo antes de informar "sin respuesta", y exigir que la onda migre con el nivel, evita inventar una pérdida o un retrococlear que no existen (→ H10).
- **Para el paciente:** "Quédate quieto, con los ojos cerrados y sin tensar el cuello ni la mandíbula: la tensión del músculo ensucia el registro."
<!-- Recuadro sin citas nuevas: reutiliza lo que el capítulo ya trae (ruido residual, migración de la V, respuesta postauricular que cambia con la tensión del paciente). -->

Niveles de prevención y su marco: → B5.
:::

## Para cerrar

:::pregunta Preguntas para discutir
1. ¿Por qué replicar la curva es necesario pero no suficiente? Da un ejemplo de un artefacto que replica y otro que no.
2. Con 250 barridos el FSP vale 2,4 y el ruido residual es alto; con 4.000, el FSP llega a 15,3. ¿Qué le dirías a quien dice que "con 250 ya se ve que no hay respuesta"?
3. Un ABR sale con umbral de 20 dB nHL y el audiograma del mismo oído da 60 dB HL de promedio. ¿Qué tres cosas revisarías antes de decir que el paciente tiene una pérdida no orgánica?
4. ¿Qué diferencia hay entre una onda V que se queda quieta al bajar la intensidad y una V que se atrasa? ¿Qué te dice cada una?
5. ¿Cuándo preferirías **no** pinzar el tubo, y qué otra maniobra usarías para separar estímulo de respuesta?
:::

:::ayuda Ayuda memoria del capítulo
- El promedio mejora con la **raíz** de los barridos: la mitad del ruido cuesta **cuatro veces** más.
- Un "no hay respuesta" vale solo con **ruido residual bajo**; un FSP bajo con ruido alto es "no se ve".
- Lo que se repite en cada estímulo (artefacto, músculo) **sobrevive al promedio**: la replicación no lo descarta.
- Una V verdadera **migra**: se achica y se atrasa al bajar. Lo que no se mueve no es V.
- El artefacto de estímulo está **desde 0 ms**, no se va al alternar del todo con el vibrador y **sigue con el tubo pinzado**.
- La respuesta postauricular está a **12 a 15 ms**, es ancha, grande, no se atrasa al bajar el nivel y cambia con la tensión del paciente.
- La falsa V vive en **una sola mitad** del promedio.
- Filtros, polaridad, transductor, tasa y ventana: la norma vale solo con **los mismos ajustes**.
- Antes de dudar del paciente, duda del registro.
:::

## Referencias

### Técnica

1. Sanfins MD, Santillo MEA, Martins MFP, Silva DLdS, Gos E, Skarzynski PH, Hall JW III. The influence of sex, ear, and age on auditory brainstem responses recorded with the NeuroAudio system. Diagnostics. 2026;16(7):971. doi:10.3390/diagnostics16070971
1. Picton TW. Human auditory evoked potentials. San Diego: Plural Publishing; 2010 (el editor la fecha en 2011).
1. Picton TW, Linden RD, Hamel G, Maru JT. Aspects of averaging. Semin Hear. 1983;4(4):327-40. doi:10.1055/s-0028-1094195
1. Don M, Elberling C. Evaluating residual background noise in human auditory brain-stem responses. J Acoust Soc Am. 1994;96(5 Pt 1):2746-57. doi:10.1121/1.411281
1. Don M, Elberling C. Use of quantitative measures of auditory brain-stem response peak amplitude and residual background noise in the decision to stop averaging. J Acoust Soc Am. 1996;99(1):491-9. doi:10.1121/1.414560
1. Stockard JE, Stockard JJ, Westmoreland BF, Corfits JL. Brainstem auditory-evoked responses: normal variation as a function of stimulus and subject characteristics. Arch Neurol. 1979;36(13):823-31. doi:10.1001/archneur.1979.00500490037006.
1. British Society of Audiology. Recommended procedure: cochlear microphonic testing (OD104-87). BSA; 2019 (describe la prueba de pinzar el tubo). Disponible en: https://www.thebsa.org.uk/wp-content/uploads/2023/10/OD104-87-Recommended-Procedure-for-Cochlear-Microphonic-Testing.pdf
1. Small SA, Stapells DR. Artifactual responses when recording auditory steady-state responses. Ear Hear. 2004;25(6):611-23. doi:10.1097/00003446-200412000-00009
1. Kavanagh KT, Franks R. Analog and digital filtering of the brain stem auditory evoked response. Ann Otol Rhinol Laryngol. 1989;98(7 Pt 1):508-14. doi:10.1177/000348948909800704

### Respuesta postauricular

1. O'Beirne GA, Patuzzi RB. Basic properties of the sound-evoked post-auricular muscle response (PAMR). Hear Res. 1999;138(1-2):115-32. doi:10.1016/s0378-5955(99)00159-8
1. Patuzzi RB, O'Beirne GA. Effects of eye rotation on the sound-evoked post-auricular muscle response (PAMR). Hear Res. 1999;138(1-2):133-46. doi:10.1016/s0378-5955(99)00160-4
1. Purdy SC, Agung KB, Hartley D, Patuzzi RB, O'Beirne GA. The post-auricular muscle response: an objective electrophysiological method for evaluating hearing sensitivity. Int J Audiol. 2005;44(11):625-30. doi:10.1080/14992020500266639

### Fisiología

1. Elberling C, Don M. Quality estimation of averaged auditory brainstem responses. Scand Audiol. 1984;13(3):187-97. doi:10.3109/01050398409043059
1. Da Silva Nunes C, Gentile Matas C. Audiometría de tronco encefálico utilizando diferentes polaridades de presentación del estímulo. Rev Chil Fonoaudiol. 2005;6(2):7-16. doi:10.5354/0719-4692.2005.48433.
