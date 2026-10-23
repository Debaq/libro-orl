#!/usr/bin/env python3
"""Página web de las referencias y de los créditos de las imágenes del libro,
con buscador y botón de copiar (él, 2026-10-22). Se publica con GitHub Pages
desde la carpeta docs/ de la rama main.

    python3 herramientas/hacer_referencias_web.py   -> docs/referencias/ (index.html + datos.js)

Referencias: la sección "## Referencias" de cada capítulo (con sus ### de
tema), una fila por referencia distinta, con los capítulos que la citan.
Imágenes: lo que el libro junta en H.CREDITOS al componer cada capítulo (el
"Imagen: ..." del pie y las otoscopías de las fichas), con el título de la
figura.
"""
import collections
import json
import pathlib
import re
import sys

AQUI = pathlib.Path(__file__).resolve().parent
LIBRO = AQUI.parent
sys.path.insert(0, str(AQUI))
import hacer_libro as H  # noqa: E402

DESTINO = LIBRO / 'docs' / 'referencias'
PLANTILLA = AQUI / 'referencias_web.html'


def orden_cap(cap):
    return ({'B': 0, 'H': 1}.get(cap[:1], 2), int(re.sub(r'\D', '', cap) or 0))


def capitulos():
    """[(cap, título, tomo, md)] en el orden del libro."""
    out = []
    for f in H.CAPITULOS.glob('*.md'):
        md = f.read_text(encoding='utf-8')
        m = re.match(r'#\s+([A-Z]?\d+)\.\s*(.+)', md)
        if m:
            out.append((m[1], m[2].strip(), H.tomo_de(m[1]), md))
    return sorted(out, key=lambda c: orden_cap(c[0]))


def sin_md(texto):
    """Quita las marcas de cursiva y negrita del markdown (*Class*, **OD**)."""
    return re.sub(r'\*{1,2}([^*]+?)\*{1,2}', r'\1', texto)


def enlaces(texto):
    doi = re.search(r'doi:\s*(10\.\S+?)(?=[.,;]?(?:\s|$))', texto, re.I)
    pmid = re.search(r'PMID:?\s*(\d+)', texto)
    url = re.search(r'https?://\S+?(?=[.,;)]?(?:\s|$))', texto)
    return dict(doi=doi[1] if doi else '', pmid=pmid[1] if pmid else '', url=url[0] if url else '')


def referencias(caps):
    filas = {}
    for cap, _, _, md in caps:
        m = re.search(r'\n## Referencias\s*\n(.*?)(?=\n## |\Z)', md, re.S)
        if not m:
            continue
        seccion = ''
        for linea in m[1].splitlines():
            if linea.startswith('### '):
                seccion = linea[4:].strip()
            elif linea.startswith('1. '):
                texto = sin_md(linea[3:].strip())
                r = filas.setdefault(texto, dict(t=texto, c=[], s=[], **enlaces(texto)))
                if cap not in r['c']:
                    r['c'].append(cap)
                if seccion and seccion not in r['s']:
                    r['s'].append(seccion)
    return sorted(filas.values(), key=lambda r: r['t'].lower())


def imagenes(caps):
    """Compone cada capítulo como lo hace el armado del tomo II, para que el
    libro llene H.CREDITOS; de paso guarda el título de cada figura."""
    titulos = {}
    original = H.separar_credito

    def espia(cap, numero, titulo):
        t, c = original(cap, numero, titulo)
        if c:
            titulos[(cap, numero)] = t
        return t, c
    H.separar_credito = espia
    for cap, _, _, md in caps:
        try:
            H.capitulo(md)
        except BaseException as e:  # un capítulo que falla no frena la página
            print(f'  aviso: créditos de {cap} sin leer ({e})', file=sys.stderr)
    H.separar_credito = original
    out = []
    for cap in sorted(H.CREDITOS, key=orden_cap):
        for n, cr in H.CREDITOS[cap]:
            texto = re.sub(r'^Imagen:\s*', '', cr)
            tipo = ('ia' if 'inteligencia artificial' in cr.lower()
                    else 'propia' if cr.startswith('Imagen propia') else 'terceros')
            out.append(dict(c=cap, n=n, f=sin_md(titulos.get((cap, n), '')), t=sin_md(texto), k=tipo, **enlaces(texto)))
    return out


def main():
    caps = capitulos()
    refs = referencias(caps)
    imgs = imagenes(caps)
    indice = [dict(c=c, t=t, v=v) for c, t, v, _ in caps]
    DESTINO.mkdir(parents=True, exist_ok=True)
    datos = dict(caps=indice, refs=refs, imgs=imgs)
    (DESTINO / 'datos.js').write_text('window.LIBRO = ' + json.dumps(datos, ensure_ascii=False, separators=(',', ':'))
                                      + ';\n', encoding='utf-8')
    (DESTINO / 'index.html').write_text(PLANTILLA.read_text(encoding='utf-8'), encoding='utf-8')
    raiz = LIBRO / 'docs'
    (raiz / '.nojekyll').write_text('', encoding='utf-8')
    (raiz / 'index.html').write_text(
        '<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=referencias/">'
        '<title>Libro ORL</title><a href="referencias/">Referencias e imágenes del libro</a>\n', encoding='utf-8')
    tipos = collections.Counter(i['k'] for i in imgs)
    print(f'{DESTINO} · {len(refs)} referencias · {len(imgs)} imágenes {dict(tipos)}')


if __name__ == '__main__':
    main()
