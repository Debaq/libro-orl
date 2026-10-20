# Evaluación y rehabilitación en otorrinolaringología (libro de casos)

**El compilado es `libro.pdf`** (en esta carpeta). Ya no se rearma solo:
se trabaja por piezas (capítulo, parte, preliminares, portadas) en `salida/`
y el libro entero se arma solo cuando se pide con `--completo`.

## Qué hay en cada carpeta

| Carpeta | Qué tiene |
|---|---|
| `capitulos/` | El texto: un `.md` por capítulo (B, H1-H30, 1-36) y su `.py`, que declara los casos y las figuras. |
| `preliminares/` | Prólogo, presentación, cómo usar el libro y abreviaturas. |
| `indice.md` | El índice y el plan de cada capítulo. |
| `casos/` | Un JSON por caso pedido por cuadro; `casos/generados/` es lo que armó el editor real de LabSim. |
| `figuras/` | Motor de figuras (`motor/`), `armar_casos.sh` y `hacer_figuras.py`. Los SVG salen a `figuras/salida/`. |
| `otoscopias/` | Fotos usadas en las fichas y sus créditos (`CREDITOS*.md`). Los bancos completos (`bancos/`) no se versionan. |
| `ilustraciones/`, `logos/` | Dibujos y logos de la portada. |
| `investigacion/` | La revisión bibliográfica de base. |
| `herramientas/` | Los scripts del libro (abajo). |
| `salida/` | PDF de capítulos sueltos para revisar. No se versiona. |
| `fuentes/` | Material privado del autor (protocolo 2019). No se versiona. |

## Comandos

```bash
# Un capítulo: casos + figuras + su PDF (salida/capitulo-11.pdf)
python3 capitulos/11-asimetria-que-no-cierra.py
python3 capitulos/11-asimetria-que-no-cierra.py --solo-pdf   # sin rehacer figuras

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
python3 herramientas/hacer_libro.py --completo         # libro.pdf
python3 herramientas/hacer_libro.py --completo --tomos # libro-tomo-I.pdf y -II.pdf

# Esqueleto de un capítulo nuevo desde indice.md
python3 herramientas/nuevo_capitulo.py H8
```

**Estado y pendientes: ver `ESTADO.md`.**

Las guías del docente (`:::docente`) van siempre dentro de cada caso: hay
**una sola edición** del libro.
