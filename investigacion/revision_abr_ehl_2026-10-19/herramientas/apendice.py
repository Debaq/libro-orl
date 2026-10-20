"""Apéndice del informe: cada línea de capitulos/*.md que cambió respecto
de un commit, con el cambio palabra por palabra ([-antes-]{+después+}).

Uso (desde la raíz del libro): python3 .../apendice.py [commit] > apendice.md
"""
import difflib
import re
import subprocess
import sys

base = sys.argv[1] if len(sys.argv) > 1 else 'HEAD'
archivos = subprocess.run(['git', 'diff', '--name-only', base, '--', 'capitulos/'],
                          capture_output=True, text=True, check=True).stdout.split()
total = 0
for f in archivos:
    viejo = subprocess.run(['git', 'show', f'{base}:{f}'], capture_output=True, text=True, check=True).stdout.split('\n')
    nuevo = open(f).read().split('\n')
    print(f'\n### `{f}`\n')
    sm = difflib.SequenceMatcher(None, viejo, nuevo, autojunk=False)
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op == 'equal':
            continue
        for k in range(max(a2 - a1, b2 - b1)):
            a = viejo[a1 + k] if a1 + k < a2 else ''
            b = nuevo[b1 + k] if b1 + k < b2 else ''
            ta, tb = re.findall(r'\S+|\s+', a), re.findall(r'\S+|\s+', b)
            partes = []
            for o, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ta, tb, autojunk=False).get_opcodes():
                if o == 'equal':
                    seg = ''.join(ta[i1:i2])
                    partes.append(seg if len(seg) < 90 else seg[:40] + ' … ' + seg[-40:])
                else:
                    if i2 > i1:
                        partes.append('[-' + ''.join(ta[i1:i2]).strip() + '-]')
                    if j2 > j1:
                        partes.append('{+' + ''.join(tb[j1:j2]).strip() + '+}')
            total += 1
            print(f'- **L{b1 + k + 1}**: ' + ''.join(partes).replace('|', '\\|'))
print(f'\n_{total} líneas cambiadas en {len(archivos)} archivos._')
