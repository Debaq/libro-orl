#!/usr/bin/env python3
"""Renumera las herramientas H14-H25 a H15-H26 en docs/libro (contenido y nombres)."""
import pathlib, re, subprocess, sys, collections
RAIZ = pathlib.Path('/home/nick/Escritorio/Proyectos/LabSim'); LIBRO = RAIZ/'docs/libro'
EXCL = ('fuentes/', 'investigacion/', 'salida/', 'libro.pdf')
TEXTO = {'.md','.py','.mjs','.js','.sh','.json','.svg','.txt','.html','.css','.tsv','.csv','.yml','.yaml'}
INCLUIR_INV = {'investigacion/pasada_contenidos_2026-10-18/PARA_EL_AUTOR.md'}
RE_H = re.compile(r'\bH(1[4-9]|2[0-5])\b'); RE_h = re.compile(r'\bh(1[4-9]|2[0-5])(?=[-_.])')
def sube(m): return m[0][0] + str(int(m[1]) + 1)
def archivos():
    for p in LIBRO.rglob('*'):
        if not p.is_file(): continue
        r = p.relative_to(LIBRO).as_posix()
        if r in INCLUIR_INV: yield p; continue
        if r.startswith(EXCL) or '__pycache__' in r: continue
        if p.suffix.lower() in TEXTO: yield p
def conteo():
    c = collections.Counter()
    for p in archivos():
        t = p.read_text(encoding='utf-8', errors='ignore')
        for m in RE_H.finditer(t): c['H'+m[1]] += 1
        for m in RE_h.finditer(t): c['h'+m[1]] += 1
    return c
modo = sys.argv[1]
if modo == 'contar':
    c = conteo(); print(sorted(c.items())); print('total', sum(c.values()))
elif modo == 'contenido':
    n = 0
    for p in archivos():
        t = p.read_text(encoding='utf-8', errors='ignore')
        u = t.replace('h2425', 'h2526').replace('H2425', 'H2526')
        u = RE_H.sub(sube, u); u = RE_h.sub(sube, u)
        if u != t: p.write_text(u, encoding='utf-8'); n += 1
    print('archivos tocados', n)
elif modo == 'nombres':
    rx = re.compile(r'^(hacer_)?([Hh])(1[4-9]|2[0-5])(?=[-_.])')
    cand = []
    for p in LIBRO.rglob('*'):
        r = p.relative_to(LIBRO).as_posix()
        if not p.is_file() or r.startswith(('fuentes/', 'investigacion/', 'salida/')): continue
        m = rx.match(p.name)
        if m or 'h2425' in p.name: cand.append((p, m))
    cand.sort(key=lambda x: -int(x[1][3]) if x[1] else 0)
    trackeados = set(subprocess.run(['git','ls-files'], cwd=LIBRO, capture_output=True, text=True).stdout.split())
    for p, m in cand:
        nuevo = p.name.replace('h2425','h2526') if not m else rx.sub(lambda k: (k[1] or '') + k[2] + str(int(k[3]) + 1), p.name, count=1)
        dst = p.with_name(nuevo); assert not dst.exists(), dst
        r = p.relative_to(LIBRO).as_posix()
        if r in trackeados: subprocess.run(['git','mv',str(p),str(dst)], cwd=LIBRO, check=True)
        else: p.rename(dst)
        print(r, '->', nuevo)
