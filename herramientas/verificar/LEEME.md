# Herramientas de verificación (de las pasadas de 2026-10-18/19)

- `cotejar_dois.py archivo.md ...`: coteja contra Crossref y PubMed los DOI y PMID de las líneas de referencia **agregadas** (git diff) en esos capítulos. Para un archivo nuevo, antes `git add -N`.
- `renumerar_herramientas.py contar|contenido|nombres`: corre un número las herramientas de un rango (editar el rango en `RE_H`, `RE_h` y `rx`). Ojo: no toca los `import hacer_hNN` entre scripts de figuras ni `hacer_hNN.py` dentro de textos (revisar a mano, ver decisiones de 2026-10-19), y en otro repo hay que ajustar `RAIZ`/`LIBRO`.
- El checklist se regenera desde `investigacion/pasada_contenidos_2026-10-18/checklist_original.md` + `marcas_checklist.tsv` (número de línea del original, marca x/~/espacio, dónde está).
