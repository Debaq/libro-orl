"""Para un capítulo: cada figura ABR cambiada con sus latencias y amplitudes
antes → después (lat ms / amplitud µV pico-depresión), sus notas, los
umbrales que cambiaron en sus casos y las líneas del texto con cifras de PEAT.

Uso (desde la raíz del libro): python3 .../ver_capitulo.py capitulos/12-el-tronco.md
"""
import glob
import json
import os
import re
import sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R, 'herramientas'))
from medir_abr import tabla  # noqa: E402

md = sys.argv[1]
t = open(md).read()
antes = set(os.listdir(os.path.join(R, 'figuras_antes')))
casos = sorted(set(re.findall(r'\{\{caso (\S+)\}\}', t)) | set(re.findall(r':::figura (\S+) ', t)))
for m in re.finditer(r'\n:::figura (\S+) (abr|ecochg) ?(\d*)\n(.*?)\n:::', t, re.S):
    caso, tipo, n, cuerpo = m.groups()
    f = f'{caso}_{tipo}' + (f'_{n}' if n and n != '1' else '') + '.svg'
    if f not in antes:
        continue
    linea = t[:m.start()].count('\n') + 2
    print(f'\n## {f}  (línea {linea})')
    if tipo == 'abr':
        tabla(f'figuras/salida/{f}', os.path.join(R, 'figuras_antes', f))
    for l in cuerpo.split('\n'):
        print('    ' + l)
cpc = json.load(open(os.path.join(R, 'cambios_por_caso.json')))
print('\n## Umbrales que cambiaron en los casos del capítulo')
for c in casos:
    k = f'casos/generados/{c}.json'
    if k in cpc:
        print(f'  {c}: ' + '; '.join(cpc[k]))
print('\n## Líneas con cifras de PEAT fuera de las notas')
dentro = False
for i, l in enumerate(t.split('\n'), 1):
    if l.startswith(':::figura'):
        dentro = True
    elif l.startswith(':::') and dentro:
        dentro = False
        continue
    if not dentro and re.search(r'nHL|eHL|\d ms\b|onda V|interpico|I-V|I-III|III-V|PEAT|ABR', l):
        print(f'  {i}: {l[:300]}')
