#!/usr/bin/env python3
"""Escribe los casos de un capítulo y rehace sus figuras, sin armar el PDF.

    python3 herramientas/solo_figuras.py capitulos/21-vertigo-agudo.py [cap21_neuritis ...]

Igual que Capitulo.generar, pero sin rearmar casos con LabSim (si el pedido
cambió, avisa y no sigue) y sin componer el capítulo: sirve para trabajar las
figuras mientras el libro no se arma. Con nombres, rehace solo esos casos.
"""
import json
import os
import runpy
import subprocess
import sys

import libro

ruta = sys.argv[1]
solo = set(sys.argv[2:])
mod = runpy.run_path(ruta, run_name='solo_figuras')
cap = mod.get('CAP') or libro.Capitulo(int(os.path.basename(ruta).split('-')[0])
                                       if os.path.basename(ruta)[0].isdigit()
                                       else os.path.basename(ruta).split('-')[0])
nombres = []
for c in mod['CASOS']:
    n = cap.nombre(c)
    if solo and n not in solo:
        continue
    spec = {'caso': c['caso'], 'figuras': c['figuras']}
    (libro.CASOS / f'{n}.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if isinstance(c['caso'], dict):
        gen = libro.GENERADOS / f'{n}.json'
        previo = json.loads(gen.read_text(encoding='utf-8')).get('pedido') if gen.exists() else None
        if previo != c['caso']:
            sys.exit(f'{n}: el pedido del caso cambió y habría que rearmarlo con LabSim (Capitulo.generar).')
    nombres.append(n)
subprocess.run([*libro.python_figuras(), str(libro.LIBRO / 'figuras' / 'hacer_figuras.py'), *nombres],
               check=True, cwd=libro.RAIZ, env=dict(os.environ, QT_QPA_PLATFORM='offscreen'))
