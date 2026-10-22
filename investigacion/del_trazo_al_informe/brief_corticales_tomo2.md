# Latencia media, tardía y estado estable en el tomo II (brief común, 2026-10-22)

Meta del autor: que el tomo II enseñe también los potenciales de latencia media (MLR), tardía (P1-N1-P2, P300, MMN) y de estado estable (ASSR), con casos, figuras e informe, como ya se hizo con el PEAT. Lee también `investigacion/del_trazo_al_informe/brief_peat_tomo2.md` (reglas de informe, referencias del PEAT, réplicas, nivel bajo el umbral, nada de pacientes de práctica de LabSim) y `herramientas/brief_agentes.md` (sintaxis).

## Reglas duras

- **El tomo I (capítulos H y B) NO se toca.** Ni siquiera para arreglar una errata: el autor lo está editando aparte. H13 (estado estable) y H14 (latencia media y tardía) se LEEN para remitir (→ H13, → H14) y para no contradecirlas; si algo choca, va en tu informe final.
- No hagas commit. No armes el libro completo. Solo tus capítulos (sus .md y .py, sus casos, sus figuras y las ilustraciones nuevas que crees).
- Prosa del libro: frases cortas, español de Chile, "tú", sin relleno. Nunca "el laboratorio". Cuando los autores no coinciden, las dos posturas con cita. El caso manda: el texto calza con los datos.
- Toda cifra normativa con fuente verificada (DOI/PMID). Las cifras que usa LabSim tienen su cita en `/home/nick/Escritorio/Proyectos/LabSim/labsim_backend/src/CentralReferences.php`: úsalo como punto de partida, pero cita la fuente original y verifica lo que puedas. No cites a LabSim.

## Cómo se arma (LabSim)

- Cuadro central del paciente: `cuadro(..., central='<clave>')`. Claves (CaseProfile::CENTRAL_SCENARIOS) y edades permitidas:
  `central_normal` (cualquiera), `nino_dormido` (0-9 años), `acv_temporal` (40 o más; MLR con efecto electrodo de un hemisferio, N1-P2 y MMN reducidas), `tpac` (7 o más; MLR reducido, MMN reducida, P300 retardada 20-50 ms), `privacion_implante_tardio` (2-17; P1 retardada 60-140 ms, N1-P2 reducida), `deterioro_cognitivo`.
  Los casos armados desde el 2026-10-21 ya traen bloque Central normal; los anteriores no. Agregar `central=` cambia el pedido y REARMA el caso: con la misma semilla los datos periféricos no cambian, pero revisa nombre, umbrales y figuras y ajusta el texto si algo se movió.
- Figura: `fig.cortical(prueba='MLR'|'CAEP'|'P300'|'MMN', niveles=(70,), estimulo=None, canales=None, marcar=True, promediaciones=None, ventana=None, oidos=None)`. El motor aplica el estándar del equipo (MLR: click, 7,1/s, 10-300 Hz, 1.000 barridos, ventana 100 ms; CAEP: burst 1 kHz, 1/s, 1-30 Hz, 150; P300: burst 1 kHz frecuente / 2 kHz raro 80/20, 1/s, 0,5-30 Hz, 250, paciente contando los raros; MMN: igual, 1,5/s, 1-30 Hz, 2.000, video sin sonido), con referencia en el lóbulo. Cada nivel sale con réplica. Canales por defecto: C3/Cz/C4 en el MLR (para el efecto electrodo), Cz en el CAEP, Pz en la P300 (con el frecuente en gris detrás) y Fz en la MMN (la diferencia raro − frecuente, con los dos promedios en gris).
- Los rótulos (Na, Pa, Nb, Pb; P1, N1, P2, N2; P3; MMN) los pone el motor en el extremo dentro de la ventana normativa de la edad. NO son la lectura: lee tú la figura (pásala a PNG y mírala) y, si un rótulo no corresponde, dilo en el globo o usa `marcar=False` y explica en los globos. Las anclas para globos son "OD Cz 70", "OD Cz 70 P1", etc.
- Latencias: del SVG. El eje va de 0 a la ventana; px por ms = 290 / ventana (MLR 100 ms, CAEP 500, P300 800, MMN 500); el origen x es el del "0" del eje de ese oído. Escribe un script chico que las lea.
- Un umbral cortical (CAEP) se busca como el del PEAT: baja de 20 en 20, sube 10, y siempre se muestra el nivel de abajo sin respuesta.

## Informe

Mismo formato que el PEAT (recuadro `:::comentario-ancho Informe de <nombre>, <edad> (caso N)`): Motivo, Registro (prueba, estímulo, tasa, filtros, barridos, montaje, estado del paciente y tarea), Referencia (con fuente, por edad), tabla (latencias y amplitudes por oído/canal contra su referencia, ↑ lo que pasa el límite), Morfología y replicabilidad, Interpretación (en qué se basa: p. ej., efecto electrodo frente a efecto oído en el MLR), Conclusión y Recomendación. Mira el ejemplo de informe de H14 (sección "Cómo se informa") sin editarla.

## Informe final (corto, en español)

Por capítulo: pacientes tocados (rearmados o no), figuras agregadas, informes escritos, cifras normativas con su fuente, choques entre LabSim y la literatura (para avisar a LabSim), lo que no se pudo mostrar y por qué, rostros pedidos si hay casos nuevos.
