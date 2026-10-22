# PEAT del tomo II: informe completo y técnica completa (brief común, 2026-10-21)

Meta del autor: que el libro enseñe TODO el PEAT, más completo y actual que Hood (1998), que es su autora central. Cada paciente con PEAT del tomo II termina con un informe completo, y entre todos los casos se ven todas las técnicas que un tecnólogo usa hoy.

## Modelo único: H10

Lee en `capitulos/H10-potenciales-evocados-auditivos-de-tronco.md` las secciones *Cómo se informa* (Qué se mide, Contra qué se compara, Cuatro patrones, Lo que hay que saber de memoria, Del trazo a la conclusión, Las frases de la conclusión, Qué lleva el informe, Informes de ejemplo). El formato de informe es ESE: un recuadro `:::comentario-ancho Informe de <nombre>, <edad> (caso <N>)` con Motivo, Registro, Referencia, la tabla (OD | OI | referencia o límite, con ↑ en lo que pasa el límite; umbrales en dB nHL → dB eHL), Morfología, Interpretación (en qué se basa), Conclusión (frases de la tabla de H10) y Recomendación. No repitas la teoría de H10: remite (→ H10).

Dónde va el informe: en la *Resolución de los casos* de cada caso con PEAT, dentro de "Diagnóstico y qué sigue" (reemplaza el informe corto que haya). Si el caso ya tiene un informe de ECochG, VEMP o emisiones, déjalo.

## Referencias (valores verificados; no uses otras cifras sin fuente)

- **Adulto, por sexo, edad y oído**: Sanfins y cols. (2026), tabla 7 (media ± 2 DE, click 80 dB nHL, inserción). Límite superior (ms):

| Oído | Sexo | Edad | I | III | V | I-III | III-V | I-V |
|---|---|---|---|---|---|---|---|---|
| D | H | 3-17 | 1,71 | 4,08 | 6,20 | 2,61 | 2,25 | 4,69 |
| D | H | 18-49 | 1,80 | 4,05 | 6,03 | 2,45 | 2,33 | 4,49 |
| D | H | 50+ | 1,90 | 4,16 | 6,16 | 2,54 | 2,17 | 4,53 |
| D | M | 3-17 | 1,74 | 4,39 | 6,42 | 2,89 | 2,27 | 4,91 |
| D | M | 18-49 | 1,80 | 3,94 | 5,89 | 2,42 | 2,11 | 4,33 |
| D | M | 50+ | 1,87 | 4,17 | 6,08 | 2,71 | 2,16 | 4,51 |
| I | H | 3-17 | 1,70 | 4,13 | 6,37 | 3,06 | 2,96 | 5,31 |
| I | H | 18-49 | 1,80 | 4,14 | 6,05 | 2,61 | 2,11 | 4,52 |
| I | H | 50+ | 1,91 | 4,22 | 6,24 | 2,53 | 2,33 | 4,54 |
| I | M | 3-17 | 1,74 | 4,10 | 6,32 | 2,56 | 2,44 | 4,88 |
| I | M | 18-49 | 1,80 | 4,01 | 5,92 | 2,49 | 2,12 | 4,41 |
| I | M | 50+ | 2,06 | 4,18 | 6,22 | 2,63 | 2,27 | 4,41 |

  Cita: Sanfins MD, Santillo MEA, Martins MFP, Silva DLdS, Gos E, Skarzynski PH, Hall JW III. The influence of sex, ear, and age on auditory brainstem responses recorded with the NeuroAudio system. Diagnostics. 2026;16(7):971. doi:10.3390/diagnostics16070971
- **Recién nacido y lactante**: Rosa y cols. (2014), media (DE): 39-40 semanas: I 1,79 (0,09), III 4,56 (0,22), V 6,90 (0,33), I-III 2,77 (0,21), III-V 2,42 (0,61), I-V 5,08 (0,31). 37-38 sem.: V 7,05. 35-36 sem.: I 1,81 (0,09), III 4,74 (0,20), V 7,14 (0,34), I-III 2,89, III-V 2,41, I-V 5,33. 6 meses: I 1,70 (0,12), III 4,37 (0,19), V 6,50 (0,27), I-III 2,65 (0,20), III-V 2,16 (0,18), I-V 4,81 (0,26). Límite = media + 2 DE. Cita como en el cap. 14.
- **Diferencia interaural de la V**: anormal sobre 0,2 a 0,4 ms (Hood, 1998); 0,3 a 0,4 (Musiek y cols., 2015, en Katz 7.ª ed.).
- **V/I**: anormal bajo 1 (Musiek y cols., 1984) o bajo 0,75 (Musiek y cols., 2015).
- **Morfología** (Hood, 1998, p. 24): a 75-80 dB nHL, picos claros y al menos I, III y V en cada oído.
- **nHL → eHL**: tabla de la BSA (2019) que está en H10 (adultos y lactantes de 12 a 24 semanas). Click adulto −5.
- **Tasa**: Jiang y cols. (1991): de 10 a 90 estímulos/s la V se alarga 12 a 15 %.
- Textos completos para leer lo que necesites (privados, no se citan las páginas de este archivo, sino el libro): `/tmp/claude-1000/-home-nick-Escritorio-Proyectos-libro-orl/b1d6046a-432d-419e-92b3-44c94a49154c/scratchpad/fuentes_peat/hood.txt` (Hood 1998; cap. 9 = informes modelo, cap. 5 neurológico, cap. 6 estimar audición, cap. 7 niños) y `katz.txt` (Katz 7.ª ed., 2015; cap. 13 Musiek diagnóstico diferencial, cap. 14 Hood estimación de audición, cap. 15 ASSR). Lo que cites de ellos va como Hood (1998) o como capítulo del Katz (formato de las referencias de H10).

## Latencias: se leen de la figura, no se inventan

Toda latencia o umbral que escribas sale de los datos del caso (`casos/generados/<caso>.json`, `ABR.<oído>.umbral_por_estimulo`) y de la figura SVG (`figuras/salida/<caso>_abr*.svg`). En el SVG cada rótulo de onda (`<text>` I, III, V) está en el pico: latencia (ms) = (x del rótulo − x del "0" del eje de ese oído) / 22. El nivel de cada rótulo es la fila cuyo rótulo "NN dB" está justo debajo. Escribe un script chico que lo calcule (ver cómo se hizo en el informe de H10). Usa dos decimales en la tabla del informe y uno en los globos si basta. Si una onda marcada por el motor no se ve clara en el trazo, míralo (rsvg-convert a PNG y Read) y no la informes como presente.

## Técnicas: que se vean todas en el tomo II

`fig.abr(niveles=(...), estimulo=..., marcar=('I','III','V'), transductor='insercion'|'oseo'|'copa', polaridad='alternada'|'condensacion'|'rarefaccion', tasa=21.1, promediaciones=None, ventana=12, enmascaramiento=None)`.
- `estimulo`: 'Click', 'CE-Chirp', 'CE-Chirp LS', 'NB CE-Chirp LS 500 Hz' / '1 kHz' / '2 kHz' / '4 kHz', 'Burst 500 Hz', 'Burst 1 kHz', 'Burst 2 kHz', 'Burst 4 kHz'.
- `ventana` en ms (nuevo): 15 a 20 para burst de 500 Hz y lactantes; con 12 la V grave cerca del umbral se sale.
- `enmascaramiento` en dB (nuevo): ruido en el oído contrario (MKG).
- `tasa=81.1` para la prueba de esfuerzo neural.
- La búsqueda de umbral se muestra entera: baja de 20 en 20, sube 10. **Siempre** incluye el nivel de abajo sin V, para demostrar que no había respuesta más abajo (él, 2026-10-22).
- **Réplicas** (él, 2026-10-22): cada nivel se registra dos veces y la figura muestra los dos trazos juntos (80, 80, 60, 60...). Lo hace el motor solo. Una onda es respuesta si está en los dos trazos; ya no hay "líneas finas" de subpromedios.
Cambiar las figuras de un caso NO lo rearma (los datos quedan iguales). Cambiar edad, cuadro, semilla o anamnesis SÍ lo rearma.

## Pacientes de práctica de LabSim: fuera

Los casos `capNN_pXX` (demo(33..42)) se reemplazan por casos propios con `cuadro()` que enseñen lo mismo o algo mejor ("cámbialos, no aumentes"). Antes de sacar uno, copia su .md (el bloque del caso), su JSON y sus SVG a `investigacion/del_trazo_al_informe/pacientes_labsim_retirados/`. Flujo de un cuadro nuevo: armar sin anamnesis, mirar datos y figuras, escribir anamnesis/historia coherente, rearmar (con la misma semilla los datos no cambian). Pide rostros para los casos nuevos en tu informe final (no los generes).

## Cuidado con LabSim (y avísalo, no lo parches)

- La fila del lactante de LabSim (3 meses a 3 años) es casi de adulto (V 5,78 ms); Rosa a los 6 meses da V 6,50. Un bebé de 3 meses o más sale con latencias de adulto. Si un caso tuyo está en esa edad, compara con Rosa: si no calza, rearma al bebé con `edad_horas=2050` (12 semanas, fila del recién nacido) y ajusta el texto (edad, anamnesis), o dímelo si cambia el sentido del caso.
- Cualquier otra cifra de LabSim sin fuente que choque con la referencia: gana la referencia, y lo anotas en tu informe final (yo lo paso a `LabSim/docs/limites_desde_el_libro.md`). No edites LabSim.

## Reglas del autor

- Prosa: frases cortas, claras, tono del libro, sin relleno de narrador. Español de Chile, "tú".
- El caso clínico manda: el texto calza con los datos; nunca vuelvas a datos viejos.
- Cuando los autores no coinciden, se dicen las dos posturas con cita.
- Pies de figura: qué es y qué mirar.
- Nunca "el laboratorio" ni instituciones en texto visible. No cites ni nombres el protocolo como documento: "en este libro".
- No hagas commit. No armes el libro completo. Solo tus capítulos (sus .md y .py, sus casos y figuras) y lo que se te diga.
- Arma cada capítulo con `PUERTO=<tu puerto> python3 capitulos/<archivo>.py`, renderiza las páginas (pdftoppm -r 60) a tu scratch y MÍRALAS. Arregla lo que se vea mal (recuadros partidos, tablas aplastadas, globos sobre valores).

## Informe final (corto, en español)

Por capítulo: pacientes cambiados (antes → después), técnicas agregadas (qué figura, qué estímulo), informes escritos, cifras de LabSim que chocaron con la referencia, rostros pedidos, problemas del armador, y cualquier cosa que deba decidir el autor.
