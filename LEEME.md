# Evaluación y rehabilitación en otorrinolaringología (libro de casos)

**Los libros armados están en `ediciones/`** (ver `ediciones/LEEME.md`). Ya no se rearman solos:
se trabaja por piezas (capítulo, parte, preliminares, portadas) en `salida/`
y el libro entero se arma solo cuando se pide con `--completo`.

## Qué hay en cada carpeta

| Carpeta | Qué tiene |
|---|---|
| `texto/` | Lo que se escribe: `capitulos/` (un `.md` por capítulo y su `.py`, que declara los casos y las figuras), `preliminares/` (prólogo, presentación, cómo usar, abreviaturas) e `indice.md` (el índice y el plan de cada capítulo). |
| `material/` | Lo que el texto usa: `casos/` (JSON de cada caso; `generados/` es lo que armó LabSim), `figuras/` (motor, `armar_casos.sh`, `hacer_figuras.py`; los SVG en `figuras/salida/`), `ilustraciones/`, `otoscopias/` (fotos y créditos; `bancos/` no se versiona), `rostros/`, `logos/` y `labsim/` (copia de recursos de LabSim). En los `.md`, las rutas de imágenes (`ilustraciones/…`, `figuras/…`) son relativas a esta carpeta. |
| `herramientas/` | Los scripts del libro (abajo). |
| `ediciones/` | Los libros armados: `digital/` (A4, dos tomos), `kdp/` (Amazon: tapa blanda, tapa dura, descripciones) y `entregados/` (copias congeladas). Ver `ediciones/LEEME.md`. |
| `trabajo/` | Lo de apoyo, que no va al libro: `investigacion/`, `revision_colegas/`, `portadas/` (opciones de portada), `notas/` (ROADMAP, checklist, incongruencias con el protocolo) y `png/` (exportaciones PNG de ilustraciones y gráficos). |
| `docs/` | Página web de referencias e imágenes (GitHub Pages; debe quedar en la raíz). |
| `salida/` | PDF de capítulos sueltos para revisar y las cachés del armado. No se versiona. |
| `fuentes/` | Material privado del autor (protocolo 2019). No se versiona. |

En la raíz quedan solo `LEEME.md`, `ESTADO.md` (estado y decisiones) y `pendientes_urgentes.md`.

## Comandos

```bash
# Un capítulo: casos + figuras + su PDF (salida/capitulo-11.pdf)
python3 texto/capitulos/11-asimetria-que-no-cierra.py
python3 texto/capitulos/11-asimetria-que-no-cierra.py --solo-pdf   # sin rehacer figuras

# Piezas sueltas (todo sale a salida/, en segundos)
python3 herramientas/hacer_libro.py 11                 # solo el capítulo 11 (o H4, B2...)
python3 herramientas/hacer_libro.py parte III          # una parte: separador y sus capítulos
python3 herramientas/hacer_libro.py parte nariz        # también por nombre: bases, herramientas...
python3 herramientas/hacer_libro.py prelim             # todas las preliminares
python3 herramientas/hacer_libro.py prelim prologo     # una o varias (prologo, como-usar, 04...)
python3 herramientas/hacer_libro.py portadas           # portada, interior, créditos, autores, contraportada
python3 herramientas/hacer_libro.py portadas --tomo II # las del tomo II
python3 herramientas/hacer_libro.py indice             # el índice, sin números de página
python3 herramientas/hacer_libro.py frente             # preliminares y portadas nuevas en los 3 PDF, sin recomponer capítulos

# El libro entero, solo cuando se pide
python3 herramientas/hacer_libro.py --completo         # ediciones/digital/libro.pdf
python3 herramientas/hacer_libro.py --completo --tomos # ediciones/digital/libro-tomo-I.pdf y -II.pdf
python3 herramientas/hacer_libro.py --completo --tomo I # solo el tomo I

# Edición KDP (Amazon, tres tomos)
python3 herramientas/hacer_kdp.py --tomos              # ediciones/kdp/tapa-blanda/
python3 herramientas/hacer_kdp.py --tomo I --formato dura   # ediciones/kdp/tapa-dura/

# Esqueleto de un capítulo nuevo desde indice.md
python3 herramientas/nuevo_capitulo.py H8
```

**Estado y pendientes: ver `ESTADO.md`.**

Las guías del docente (`:::docente`) van siempre dentro de cada caso: hay
**una sola edición** del libro.
