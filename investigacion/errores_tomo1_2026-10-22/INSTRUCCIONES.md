# Verificación de errores del tomo I (2026-10-22): instrucciones comunes

Libro de ORL para tecnología médica (Chile). Tomo I: bases (B) y herramientas (H). Todo en español.

## Qué buscar: errores de procedimiento y de conocimiento

- **Conocimiento**: datos anatómicos, fisiológicos, físicos o clínicos falsos o desactualizados; valores normales, latencias, umbrales, criterios diagnósticos, sensibilidad/especificidad; normas (ISO, ANSI, IEC, BSA, ASHA, JCIH, ATS/ERS, AASM...) mal citadas; mecanismos mal explicados; terminología incorrecta; contradicciones internas del capítulo o con otros capítulos del tomo I.
- **Procedimiento**: pasos de una prueba en orden incorrecto; parámetros de estímulo, registro, filtros, calibración equivocados; contraindicaciones o precauciones de seguridad omitidas; interpretaciones que llevarían a un diagnóstico equivocado.
- **Cálculos**: rehacer con python3 toda cuenta o ejemplo resuelto.
- **Casos**: cada capítulo H tiene un `.py` del mismo nombre con sus casos; revisa que los datos de los casos digan lo que el texto dice de ellos.
- **Citas**: afirmación atribuida a una referencia que esa referencia no dice (si se puede comprobar).

No reportar: estilo, redacción, ortografía, maquetación. Las marcas `<!-- verificar -->` ya se trabajaron en otra pasada: no reportarlas salvo que lo marcado sea claramente falso. Lo que haga LabSim (simulador) NO es fuente: se juzga contra la literatura.

## Cómo trabajar

1. Leer los capítulos COMPLETOS con Read (por partes). No muestrear.
2. **Es obligatorio consultar los libros locales** antes de dar algo por no verificable:
   - Katz, *Handbook of Clinical Audiology* 7.ª ed.: `~/Escritorio/Libros/Auditivo/Handbook of Clinical Audiology 7th Edition_booksmedicos.org.pdf`. Busca con `pdftotext -layout ARCHIVO - | grep -n -i "término"` para ubicar, luego `pdftotext -f N -l M` para leer páginas concretas. No vuelques libros enteros a la salida.
   - Otros en `~/Escritorio/Libros/Auditivo/` (Moore, *Cochlear Hearing Loss*; *Neuropathies of the Auditory and Vestibular Eighth Nerve*; *Handbook of CAPD*...) y en `~/Escritorio/Libros/` (manuales vestibulares, *El sistema vestibular y sus alteraciones* tomos I y II, manuales de electrofisiología y PEAT en .docx — usa `pandoc` o `python3 -c` con zipfile para leerlos —, libros chilenos de audiología, Netter, Snell).
   - Web: WebSearch / WebFetch (cárgalas con ToolSearch `select:WebSearch,WebFetch`) para PubMed, guías y normas.
3. Si los autores discrepan, no es error: anotarlo como DISCUTIBLE con las dos posturas y sus citas.
4. Archivos temporales (PDF bajados, extractos): solo en tu propia subcarpeta `/tmp/claude-1000/-home-nick-Escritorio-Proyectos-libro-orl/9be7d93a-3e93-47a2-bc58-26b89924e345/scratchpad/aNN/` (NN = tu número de agente). Otros agentes trabajan en paralelo.
5. **NO editar** nada en `capitulos/`, `casos/`, `figuras/`, `labsim/`. NO ejecutar `herramientas/hacer_libro.py` ni scripts de armado. No hacer commits. Solo escribir tu informe.

## Formato del informe

Por hallazgo:

- **[GRAVE | IMPRECISO | DISCUTIBLE] archivo l.N** — qué dice el texto (cita corta) → qué es lo correcto → fuente (libro y página, o PMID/DOI/URL, o el cálculo) → corrección propuesta en una frase.

GRAVE = enseña algo falso o un procedimiento que daña o lleva a diagnóstico errado. IMPRECISO = cifra o matiz incorrecto sin consecuencia mayor. DISCUTIBLE = fuentes discrepan.

Ordenar por gravedad. Al final: conteo por categoría; lista de secciones revisadas sin hallazgos; lista de lo que NO se pudo comprobar con fuente (y dónde se buscó). Honestidad: no inventar hallazgos ni fuentes; si una sección está bien, decirlo.

Respuesta final al coordinador: máximo 15 líneas con los GRAVES y los conteos.
