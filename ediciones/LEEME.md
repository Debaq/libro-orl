# Ediciones del libro

Todo lo que sale para leer, revisar o subir. Los PDF no se versionan.

| Carpeta | Qué tiene | Cómo se arma |
|---|---|---|
| `digital/` | Versión digital A4: `libro-tomo-I.pdf` (B y H), `libro-tomo-II.pdf` (capítulos 1-38) y `libro.pdf` (un solo tomo, del 2026-10-20, no se ha vuelto a armar). | `herramientas/hacer_libro.py --completo --tomos` (o `--tomo I`, `--tomo II`) |
| `kdp/tapa-blanda/` | Amazon KDP, 8,5 × 11", tres tomos: interior y portada completa de cada uno (`-guias.pdf` solo para revisar, no se sube). | `herramientas/hacer_kdp.py --tomos` |
| `kdp/tapa-dura/` | Amazon KDP, 8,25 × 11". Vacía: la portada de tapa dura está pendiente. | `herramientas/hacer_kdp.py --tomos --formato dura` |
| `kdp/descripciones/` | Textos de la ficha de Amazon (serie y cada tomo). | a mano |
| `kdp/pruebas/` | Pruebas sueltas de portada y muestras. | — |
| `entregados/` | Copias congeladas de lo que se entregó, una carpeta por fecha. No se rearman ni se tocan. | se copian a mano |

Las cachés del armado están en `salida/cache/` (A4) y `salida/cache-kdp/` (KDP).
