#!/usr/bin/env python3
"""Libro completo por partes, con caché: solo se compone lo que cambió.
También arma una parte suelta (armar(caps=..., con_frente=False)), que es lo
que usa hacer_libro.py parte III.

    python3 docs/libro/herramientas/armado_incremental.py          # libro.pdf
    python3 docs/libro/herramientas/armado_incremental.py --todo   # ignora la caché
    python3 docs/libro/herramientas/armado_incremental.py --tomo I # libro-tomo-I.pdf (o II)
    ... --solo-frente     # solo portada, índice y contraportada (ver armar)

Antes, cada armado componía las ~490 páginas dos veces (la primera solo para
saber en qué página cae cada capítulo). Ahora:

1. Cada capítulo (con el separador de su parte, si la abre) es un SEGMENTO
   que se compone solo y se guarda en salida/cache/ con su huella: el HTML
   del segmento, el CSS y los bytes de cada imagen que usa. Si la huella no
   cambió, se reutiliza. Los que cambiaron se componen en paralelo.
2. Los segmentos se pegan con pypdf. Cada uno empieza en página derecha: si
   el anterior terminó en derecha, va una hoja en blanco (lo que hacía
   break-before: right en el libro de una pieza).
3. Los números de página del cuerpo se estampan después, con una capa que
   compone WeasyPrint con el mismo @page (mismos márgenes, letra y lado). Las
   hojas en blanco y los separadores de parte quedan sin número, como antes.
4. Las páginas iniciales (portada, índice, preliminares) y la contraportada
   se componen de nuevo cada vez, en una sola pasada: los números del índice
   ya se conocen.
5. El índice del PDF (parte > capítulo > sección) y los enlaces del índice
   impreso se rehacen sobre el PDF pegado.

Tocar un capítulo recompone ese capítulo y las páginas iniciales; tocar el
CSS recompone todo (en paralelo).

Un tomo (H.TOMOS) pega solo sus segmentos, que son los mismos del libro en
un tomo: comparten la caché y no se recompone nada para sacarlos.
"""
import concurrent.futures as cf
import hashlib
import html as html_mod
import json
import os
import pathlib
import re
import sys
import time
import urllib.parse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import acomodar  # noqa: E402
import hacer_libro as H  # noqa: E402

CACHE = H.SALIDA / 'cache'
BASE_URL = str(H.LIBRO) + '/'

# En los segmentos el número de página no va: lo estampa la capa de números.
# (El título del libro, en el pie del otro lado, sí.)
SIN_NUMERO = """
@page :right { @bottom-right { content: none; } }
@page :left { @bottom-left { content: none; } }
"""


def documento(cuerpo, css_extra=''):
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{H.TITULO}</title>'
            f'<style>{H.css()}{css_extra}</style></head><body>{cuerpo}</body></html>')


def huella(doc):
    """El HTML completo (CSS incluido), los bytes de cada archivo local que pide
    y el código del acomodo (que cambia cómo se compone)."""
    h = hashlib.sha256(doc.encode('utf-8'))
    h.update(pathlib.Path(acomodar.__file__).read_bytes())
    for uri in sorted(set(re.findall(r'file://([^"\')\s]+)', doc))):
        ruta = pathlib.Path(urllib.parse.unquote(uri))
        h.update(uri.encode())
        h.update(ruta.read_bytes() if ruta.exists() else b'(falta)')
    return h.hexdigest()


def componer(clave, doc, destino):
    """Compone un segmento (en otro proceso) y devuelve lo que el pegado
    necesita saber de sus páginas."""
    import logging
    logging.getLogger('weasyprint').setLevel(logging.ERROR)
    # acomodo de figuras y guías partidas (acomodar.py): la pasada de huecos
    render = acomodar.componer(doc, BASE_URL)
    paginas, anclas = [], {}
    for i, pag in enumerate(render.pages):
        tipo = pag._page_box.page_type
        paginas.append({'blanca': bool(tipo.blank), 'nombre': tipo.name})
        for ancla in pag.anchors:
            anclas.setdefault(ancla, i)
    temporal = destino.with_name(f'.{destino.name}.{os.getpid()}')
    render.write_pdf(str(temporal))
    os.replace(temporal, destino)
    return clave, {'paginas': paginas, 'anclas': anclas}


ARCHIVO = {}      # clave del capítulo -> su .md (lo llena segmentos())


def cambio_real(clave, doc, info):
    """Archivos del capítulo (su .md y las imágenes que pide) más nuevos que su
    caché: un cambio de verdad, que solo_frente no debe tapar."""
    t = info.stat().st_mtime
    rutas = [ARCHIVO.get(clave)] + [pathlib.Path(urllib.parse.unquote(u))
                                    for u in set(re.findall(r'file://([^"\')\s]+)', doc))]
    return [r.name for r in rutas if r and r.exists() and r.stat().st_mtime > t]


def segmentos(tomo=None, caps=None):
    """[(clave, html del segmento, tiene_separador)] en el orden del libro
    (solo los del tomo o los de caps, si se piden), y la lista (cap, título,
    parte) de la obra entera para el índice."""
    archivos = sorted(H.CAPITULOS.glob('*.md'),
                      key=lambda a: ({'B': 0, 'H': 1}.get(a.name[:1].upper(), 2), a.name))
    partes = H.partes_del_indice()
    out, capitulos, parte_actual = [], [], None
    for a in archivos:
        md = a.read_text(encoding='utf-8')
        m = re.match(r'#\s+([A-Z]?\d+)\.\s*(.+)', md)
        cap, titulo = (m[1], m[2].strip()) if m else (a.stem, a.stem)
        ARCHIVO[cap] = a
        parte = partes.get(cap)
        capitulos.append((cap, titulo, parte))
        if (tomo and H.tomo_de(cap) != tomo) or (caps and cap not in caps):
            continue
        sep = ''
        if parte and parte != parte_actual:
            sep = H.separador(parte)
            parte_actual = parte
        out.append((cap, f'<div class="cuerpo">{sep}{H.capitulo(md)}</div>', bool(sep)))
    # Créditos de las imágenes del tomo II, al final (H.CREDITOS lo llenó capitulo())
    if (tomo in (None, 'II')) and not caps:
        creditos = creditos_html()
        if creditos:
            out.append(('creditos', f'<div class="cuerpo">{creditos}</div>', False))
    return out, capitulos


def creditos_html():
    """Índice de créditos de las imágenes del tomo II: por capítulo, el número
    de la figura y su fuente, autores y licencia (sacados del pie)."""
    import html as html_mod
    bloques = []
    for cap in sorted((c for c in H.CREDITOS if H.CREDITOS[c] and H.tomo_de(c) == 'II'), key=lambda c: int(c)):
        filas = ''.join(f'<p><strong>Figura {html_mod.escape(n)}.</strong> '
                        f'{html_mod.escape(re.sub(r"^Imagen:[ ]*", "", cr))}</p>'
                        for n, cr in H.CREDITOS[cap])
        bloques.append(f'<h3>Capítulo {cap}</h3>{filas}')
    if not bloques:
        return ''
    return ('<section class="creditos" id="creditos-imagenes"><h1 class="prelim">Créditos de las imágenes</h1>'
            '<p class="creditos-intro">Fuente, autores y licencia de cada imagen, por capítulo y número de figura.</p>'
            f'<div class="referencias">{"".join(bloques)}</div></section>')


def capa_de_numeros(numerada, destino):
    """Un PDF con solo los números de página del cuerpo, uno por página."""
    from weasyprint import HTML
    f = H.FORMATO
    numero = "font: 8pt 'Plus Jakarta Sans'; color: #8f7a83;"
    fuentes = '\n'.join(l for l in H.css().splitlines() if l.startswith('@font-face'))
    css = (fuentes + f"""
@page {{ size: {f['tamano']}; margin: {f['arriba']} {f['exterior']} {f['abajo']} {f['interior']};
        @bottom-right {{ content: counter(page); {numero} }} }}
@page :left {{ margin-left: {f['exterior']}; margin-right: {f['interior']};
        @bottom-right {{ content: none; }} @bottom-left {{ content: counter(page); {numero} }} }}
@page sin {{ @bottom-left {{ content: none; }} @bottom-right {{ content: none; }} }}
body {{ margin: 0; }} div {{ height: 1px; }} .sin {{ page: sin; }} .salto {{ break-before: page; }}""")
    divs = ''.join(f'<div class="{"" if n else "sin"}{" salto" if i else ""}"></div>' for i, n in enumerate(numerada))
    HTML(string=f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head>'
                f'<body>{divs}</body></html>').write_pdf(str(destino))


def copiar_marcadores(writer, reader, desplazamiento, padre=None, raices=None):
    """Copia el índice del PDF de `reader` (anidado) desplazando las páginas.
    Devuelve los ítems de primer nivel creados."""
    from pypdf.generic import Destination
    creados, ultimo = [], None
    for item in (reader.outline if raices is None else raices):
        if isinstance(item, list):
            copiar_marcadores(writer, reader, desplazamiento, ultimo, item)
        elif isinstance(item, Destination):
            pag = reader.get_destination_page_number(item)
            ultimo = writer.add_outline_item(item.title, pag + desplazamiento, parent=padre)
            creados.append(ultimo)
    return creados


def armar(forzar=False, destino=None, tomo=None, solo_frente=False, caps=None, con_frente=True, sufijo=None,
          solo_cache=False):
    """solo_frente: el cambio fue solo de las páginas iniciales o la
    contraportada (p. ej. el color de una portada). Como la huella lleva el
    CSS entero, eso recompondría todos los capítulos: así se dan por buenos
    los que están en caché y se les pone la huella nueva.
    caps y con_frente=False: una parte suelta (hacer_libro.py parte III),
    solo esos capítulos, sin portada ni contraportada, numerada desde 1.
    solo_cache: no compone ningún capítulo; pega los de la caché tal como
    están, aunque hayan cambiado (hacer_libro.py frente: solo preliminares y
    portadas, para no mezclar con lo que se está maquetando). No toca las
    huellas, así que el próximo armado normal compone lo pendiente."""
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import ArrayObject, DictionaryObject, NameObject
    t0 = time.time()
    CACHE.mkdir(parents=True, exist_ok=True)
    segs, capitulos = segmentos(tomo, caps)
    if not segs:
        sys.exit('No hay capítulos que armar')

    # 1. Segmentos: los que cambiaron, en paralelo
    meta, pendientes, desfasados = {}, [], []
    for clave, cuerpo, _ in segs:
        doc = documento(cuerpo, SIN_NUMERO)
        h = huella(doc)
        # huella del capítulo sin el CSS: distingue "cambió el estilo de las
        # portadas" (solo_frente lo deja pasar) de "cambió el capítulo" (firma,
        # texto, imágenes), que siempre se recompone
        hc = huella(cuerpo)
        info = CACHE / f'{clave}.json'
        pdf = CACHE / f'{clave}.pdf'
        if solo_cache and info.exists() and pdf.exists():
            guardado = json.loads(info.read_text(encoding='utf-8'))
            meta[clave] = guardado
            if guardado.get('huella_cuerpo') != hc:
                desfasados.append(clave)
            continue
        if not forzar and info.exists() and pdf.exists():
            guardado = json.loads(info.read_text(encoding='utf-8'))
            if guardado.get('huella') == h and guardado.get('huella_cuerpo') != hc:
                guardado['huella_cuerpo'] = hc          # cachés de antes de la huella_cuerpo
                info.write_text(json.dumps(guardado), encoding='utf-8')
            if solo_frente and guardado.get('huella') != h:
                if guardado.get('huella_cuerpo', hc) != hc or cambio_real(clave, doc, info):
                    print(f'{clave} cambió: se recompone', flush=True)
                    pendientes.append((clave, doc, pdf, h, hc))
                    continue
                guardado['huella'] = h
                guardado['huella_cuerpo'] = hc
                info.write_text(json.dumps(guardado), encoding='utf-8')
            if guardado.get('huella') == h:
                meta[clave] = guardado
                continue
        pendientes.append((clave, doc, pdf, h, hc))
    if desfasados:
        print(f'{len(desfasados)} capítulos con cambios quedan como estaban (sin componer): '
              + ', '.join(desfasados), flush=True)
    if pendientes:
        print(f'Componiendo {len(pendientes)} de {len(segs)} capítulos: '
              + ', '.join(p[0] for p in pendientes), flush=True)
        with cf.ProcessPoolExecutor(max_workers=min(len(pendientes), os.cpu_count() or 4, 8)) as ex:
            futuros = {ex.submit(componer, c, d, p): (c, h, hc) for c, d, p, h, hc in pendientes}
            for fut in cf.as_completed(futuros):
                c, h, hc = futuros[fut]
                _, m = fut.result()
                m['huella'], m['huella_cuerpo'] = h, hc
                (CACHE / f'{c}.json').write_text(json.dumps(m), encoding='utf-8')
                meta[c] = m
    elif not desfasados:
        print('Ningún capítulo cambió', flush=True)

    # 2. Paginado del cuerpo: cada segmento empieza en página derecha (impar)
    inicio, numerada, total = {}, [], 0
    for clave, _, _ in segs:
        if total % 2 == 1:
            numerada.append(False)       # hoja en blanco
            total += 1
        inicio[clave] = total
        for p in meta[clave]['paginas']:
            numerada.append(not p['blanca'] and p['nombre'] != 'parte')
        total += len(meta[clave]['paginas'])
    pagina_cap = {}
    for clave, _, _ in segs:
        ancla = meta[clave]['anclas'].get(f'cap-{clave}')
        if ancla is not None:
            pagina_cap[clave] = inicio[clave] + ancla + 1      # el cuerpo empieza en 1

    # 3. Páginas iniciales con el índice ya numerado, y la contraportada
    from weasyprint import HTML
    if sufijo is None:
        sufijo = f'-tomo-{tomo}' if tomo else ''  # dos armados a la vez no se pisan
    frente_pdf, contra_pdf, capa_pdf = (CACHE / f'_frente{sufijo}.pdf', CACHE / f'_contraportada{sufijo}.pdf',
                                        CACHE / f'_numeros{sufijo}.pdf')
    if con_frente:
        iniciales = H.paginas_iniciales(capitulos, tomo)
        iniciales = re.sub(r'@@PAG-([A-Z]?\d+)@@', lambda m: str(pagina_cap.get(m[1], '')), iniciales)
        iniciales = re.sub(r'href="#cap-([A-Z]?\d+)"', r'href="libro://cap-\1"', iniciales)
        HTML(string=documento(iniciales), base_url=BASE_URL).write_pdf(str(frente_pdf))
        HTML(string=documento(H.contraportada(tomo)), base_url=BASE_URL).write_pdf(str(contra_pdf))
    capa_de_numeros(numerada, capa_pdf)

    # 4. Pegado
    writer = PdfWriter()
    if con_frente:
        frente = PdfReader(str(frente_pdf))
        for pag in frente.pages:
            writer.add_page(pag)
        ancho, alto = frente.pages[0].mediabox.width, frente.pages[0].mediabox.height
        if len(writer.pages) % 2 == 1:
            writer.add_blank_page(ancho, alto)       # el cuerpo empieza en derecha
        copiar_marcadores(writer, frente, 0)
    else:
        caja = PdfReader(str(CACHE / f'{segs[0][0]}.pdf')).pages[0].mediabox
        ancho, alto = caja.width, caja.height
    base_cuerpo = len(writer.pages)

    capa = PdfReader(str(capa_pdf))
    k = 0                                           # página del cuerpo
    padre_parte = None
    for clave, _, con_sep in segs:
        while k < inicio[clave]:                    # hojas en blanco entre segmentos
            writer.add_blank_page(ancho, alto)
            k += 1
        lector = PdfReader(str(CACHE / f'{clave}.pdf'))
        for pag in lector.pages:
            if numerada[k]:
                pag.merge_page(capa.pages[k])
            writer.add_page(pag)
            k += 1
        # índice del PDF: el separador abre una parte; los capítulos cuelgan de ella
        if con_sep:
            creados = copiar_marcadores(writer, lector, base_cuerpo + inicio[clave])
            padre_parte = creados[0] if creados else padre_parte
        else:
            copiar_marcadores(writer, lector, base_cuerpo + inicio[clave], padre_parte)

    if con_frente:
        if len(writer.pages) % 2 == 0:
            writer.add_blank_page(ancho, alto)       # la contraportada va en izquierda
        for pag in PdfReader(str(contra_pdf)).pages:
            writer.add_page(pag)

    # 5. Enlaces del índice impreso -> página del capítulo
    for pag in writer.pages[:base_cuerpo]:
        for anot in pag.get('/Annots', []) or []:
            a = anot.get_object()
            uri = (a.get('/A') or {}).get('/URI')
            if uri and str(uri).startswith('libro://cap-'):
                clave = str(uri)[len('libro://cap-'):]
                if clave in pagina_cap:
                    objetivo = writer.pages[base_cuerpo + pagina_cap[clave] - 1]
                    a[NameObject('/A')] = DictionaryObject({
                        NameObject('/S'): NameObject('/GoTo'),
                        NameObject('/D'): ArrayObject([objetivo.indirect_reference, NameObject('/Fit')])})

    writer.add_metadata({'/Title': H.TITULO + (f'. Tomo {tomo}' if tomo else '')})
    writer.page_mode = '/UseOutlines'
    destino = pathlib.Path(destino) if destino else H.LIBRO / f'libro{sufijo}.pdf'
    temporal = destino.with_name(f'.{destino.stem}.{os.getpid()}.pdf')
    with open(temporal, 'wb') as f:
        writer.write(f)
    os.replace(temporal, destino)
    print(f'{destino} · {len(writer.pages)} págs. · {time.time() - t0:.0f} s')
    return destino


if __name__ == '__main__':
    a = sys.argv[1:]
    armar(forzar='--todo' in a, destino=a[a.index('--salida') + 1] if '--salida' in a else None,
          tomo=a[a.index('--tomo') + 1].upper() if '--tomo' in a else None, solo_frente='--solo-frente' in a)
