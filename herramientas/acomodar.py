"""Acomodo de figuras: que el texto suba cuando una figura no cabe.

WeasyPrint no tiene "figuras flotantes": una figura que no cabe en lo que
queda de página salta entera a la siguiente y deja un hueco. Este módulo
compone el documento, busca esos huecos y adelanta el párrafo que sigue a la
figura para que lo llene, como haría un diagramador. Repite hasta que no
quedan huecos grandes o ya no hay qué mover.

Solo mueve párrafos y listas (nunca títulos, recuadros ni casos), y solo los
que vienen inmediatamente después de la figura: el orden del texto no cambia,
solo la figura queda un poco más abajo.

Después parte la guía del docente (el recuadro verde de cada caso) donde la
corta la página: el primer trozo termina en "continúa →" y el segundo repite
el título con "(continuación)". Partirla llena el pie de la página en vez de
mandarla entera a la siguiente.

Al final revisa que ninguna ficha de caso quede con la cabecera (cara y
nombre) sola al pie: si la anamnesis empieza en la página siguiente, la
ficha entera pasa a esa página. Y si el capítulo termina en una página casi
vacía (las últimas líneas de las referencias), aprieta un poco las
referencias para que quepan en la anterior.
"""
import logging

import lxml.html
from weasyprint import HTML

HUECO_MAX = 0.30        # fracción de página vacía al pie que ya se considera hueco
ULTIMA_MIN = 0.25       # la última página con menos de esto lleno se intenta ahorrar
ARRIBA_PX = 40          # la figura "salta" si empieza en los primeros px del contenido
VUELTAS = 20            # 8 dejaba huecos en los capítulos con muchas figuras
MOVIBLES = ('p', 'ul', 'ol')


def _es_figura(el):
    """Bloques que no se parten y por eso pueden dejar hueco: figuras y
    recuadros."""
    clases = (el.get('class') or '').split()
    return ('figobs' in clases or (el.tag == 'figure' and 'ilustracion' in clases)
            or (el.tag == 'aside' and 'caja' in clases))


def _cajas(caja):
    """Las cajas del contenido de la página (sin entrar a los márgenes, donde
    van el número de página y el título corrido)."""
    if type(caja).__name__ == 'MarginBox':
        return
    yield caja
    for hija in getattr(caja, 'children', None) or []:
        yield from _cajas(hija)


def _hueco(pagina):
    """Fracción vacía al pie del área de contenido de una página."""
    pb = pagina._page_box
    arriba, alto = pb.content_box_y(), pb.height
    fondo = arriba
    for c in _cajas(pb):
        nombre = type(c).__name__
        if nombre in ('PageBox', 'MarginBox') or not hasattr(c, 'position_y'):
            continue
        if nombre in ('LineBox', 'InlineReplacedBox', 'BlockReplacedBox', 'TableBox') and c.height:
            fondo = max(fondo, c.position_y + c.height)
    return max(0.0, (arriba + alto - fondo) / alto) if alto else 0.0


def _unidad(el):
    """Lo que se puede subir empezando en `el`: un párrafo o lista, o un
    subtítulo (h3/h4) junto con el párrafo que lo sigue (nunca un subtítulo
    solo, que quedaría huérfano)."""
    if el is None:
        return []
    if el.tag in MOVIBLES:
        return [el]
    if el.tag in ('h3', 'h4'):
        nxt = el.getnext()
        if nxt is not None and nxt.tag in MOVIBLES:
            return [el, nxt]
    return []


def _clases(el):
    return (el.get('class') or '').split() if el is not None else []


def _subir_siguiente(fig):
    """Pone antes de la figura el texto que la sigue (saltando hasta dos
    figuras seguidas). Devuelve False si no hay nada movible."""
    sig, saltadas = fig.getnext(), 0
    while sig is not None and _es_figura(sig) and saltadas < 2:
        sig, saltadas = sig.getnext(), saltadas + 1
    origen_col = None
    if sig is not None and 'dos-col' in _clases(sig):
        origen_col = sig
        sig = sig[0] if len(sig) else None
    unidad = _unidad(sig)
    if not unidad:
        return False
    for el in unidad:
        el.getparent().remove(el)
    previo = fig.getprevious()
    if origen_col is not None:
        # venía de una sección a dos columnas: se suma a la columna anterior
        # a la figura, o abre una nueva
        if previo is not None and 'dos-col' in _clases(previo):
            destino = previo
        else:
            destino = lxml.html.Element('div', {'class': 'dos-col'})
            fig.addprevious(destino)
        for el in unidad:
            destino.append(el)
        if not len(origen_col) and not (origen_col.text or '').strip():
            origen_col.getparent().remove(origen_col)
    else:
        for el in unidad:
            fig.addprevious(el)
    return True


def _puntaje(render):
    """Cuánto hueco grande hay (sin contar la última página, que termina el
    capítulo donde le toca)."""
    return sum(h for h in (_hueco(p) for p in render.pages[:-1]) if h >= HUECO_MAX)


def componer(doc, base_url):
    """Compone `doc` (HTML completo) acomodando figuras y recuadros. Devuelve
    el documento de WeasyPrint ya compuesto (para write_pdf o leer páginas).
    Cada movida se acepta solo si baja el total de huecos; si no, se deshace."""
    import copy
    logging.getLogger('weasyprint').setLevel(logging.ERROR)
    raiz = lxml.html.document_fromstring(doc)
    for i, caso in enumerate(raiz.find_class('caso')):
        if caso.tag == 'section':
            caso.set('id', caso.get('id') or f'ficha-{i}')
            for hijo in caso:
                if 'anamnesis' in _clases(hijo):
                    hijo.set('id', f'ficha-{i}-a')
    bloques = [el for el in raiz.iter() if isinstance(el.tag, str) and _es_figura(el)]
    if not bloques and not raiz.find_class('caso'):
        return HTML(string=doc, base_url=base_url).render()
    for i, el in enumerate(bloques):
        el.set('id', el.get('id') or f'acomodo-{i}')
        if 'caja-docente' in _clases(el):          # para ubicar el corte de la guía
            for k, u in enumerate(_unidades(el)):
                u.set('id', f'acomodo-{i}-u{k}')

    def render_de(r):
        return HTML(string=lxml.html.tostring(r, encoding='unicode', doctype='<!doctype html>'),
                    base_url=base_url).render()

    mejor = render_de(raiz)
    puntaje = _puntaje(mejor)
    intentadas = set()
    for _ in range(VUELTAS):
        if puntaje == 0:
            break
        candidata = None
        for p, pagina in enumerate(mejor.pages[1:], start=1):
            if _hueco(mejor.pages[p - 1]) < HUECO_MAX:
                continue
            arriba = pagina._page_box.content_box_y()
            for ancla, (x, y, *_r) in pagina.anchors.items():
                if ancla.startswith('acomodo-') and ancla not in intentadas and y - arriba <= ARRIBA_PX:
                    candidata = ancla
                    break
            if candidata:
                break
        if not candidata:
            break
        prueba = copy.deepcopy(raiz)
        intentadas.add(candidata)
        if not _subir_siguiente(prueba.get_element_by_id(candidata)):
            continue
        render = render_de(prueba)
        nuevo = _puntaje(render)
        if nuevo < puntaje:
            raiz, mejor, puntaje = prueba, render, nuevo
            intentadas.discard(candidata)      # puede necesitar otro párrafo más
    raiz, mejor = _fichas_enteras(raiz, mejor, render_de)
    raiz, mejor = _partir_guias(raiz, mejor, render_de)
    raiz, mejor = _fichas_enteras(raiz, mejor, render_de)
    return _ahorrar_ultima(raiz, mejor, render_de)


def _ahorrar_ultima(raiz, render, render_de):
    """Si la última página casi no tiene nada, aprieta las referencias
    (.referencias.apretada) y se queda con eso solo si el capítulo pierde
    una página."""
    if len(render.pages) < 2 or 1 - _hueco(render.pages[-1]) >= ULTIMA_MIN:
        return render
    import copy
    prueba = copy.deepcopy(raiz)
    refs = [d for d in prueba.find_class('referencias') if d.tag == 'div']
    if not refs:
        return render
    for d in refs:
        d.set('class', d.get('class') + ' apretada')
    nuevo = render_de(prueba)
    return nuevo if len(nuevo.pages) < len(render.pages) else render


def _fichas_enteras(raiz, render, render_de):
    """La ficha cuya anamnesis empieza en la página siguiente a su cabecera
    pasa entera a esa página."""
    for _ in range(3):
        pagina = _pagina_de(render)
        huerfanas = [c for c in raiz.find_class('caso') if c.tag == 'section' and c.get('id') in pagina
                     and pagina.get(c.get('id') + '-a', pagina[c.get('id')]) > pagina[c.get('id')]]
        if not huerfanas:
            break
        for c in huerfanas:
            c.set('style', 'break-before: page')
        render = render_de(raiz)
    return raiz, render


def _pagina_de(render):
    """{id: página} de cada elemento con id, en la página donde empieza."""
    out = {}
    for i, pag in enumerate(render.pages):
        for ancla in pag.anchors:
            out.setdefault(ancla, i)
    return out


def _unidades(guia):
    """Lo que se puede dejar de un lado o del otro del corte: cada viñeta de
    las listas y cada bloque suelto (sin el título)."""
    out = []
    for hijo in guia:
        if 'caja-titulo' in _clases(hijo) or 'continua' in _clases(hijo):
            continue
        if hijo.tag in ('ul', 'ol'):
            out += list(hijo)
        else:
            out.append(hijo)
    return out


def _partir(guia, k):
    """Deja en `guia` las primeras k unidades y pone el resto en una guía
    nueva, a continuación. Devuelve la nueva."""
    import copy
    unidades = _unidades(guia)
    nueva = lxml.html.Element('aside', {'class': guia.get('class'), 'id': guia.get('id') + 'c'})
    titulo = next((h for h in guia if 'caja-titulo' in _clases(h)), None)
    if titulo is not None:
        t = copy.deepcopy(titulo)
        t.text = (t.text or '').strip() + ' (continuación)'
        nueva.append(t)
    lista_nueva, lista_origen = None, None
    for el in unidades[k:]:
        padre = el.getparent()
        padre.remove(el)
        if el.tag == 'li':
            if padre is not lista_origen:
                lista_origen = padre
                lista_nueva = lxml.html.Element(padre.tag)
                nueva.append(lista_nueva)
            lista_nueva.append(el)
        else:
            lista_origen = None
            nueva.append(el)
    for lista in guia.findall('.//ul') + guia.findall('.//ol'):
        if not len(lista):
            lista.getparent().remove(lista)
    sigue = lxml.html.Element('p', {'class': 'continua', 'id': guia.get('id') + '-sigue'})
    sigue.text = 'continúa →'
    guia.append(sigue)
    guia.addnext(nueva)
    return nueva


def _partir_guias(raiz, render, render_de):
    """Parte cada guía del docente que cruza de página (ver arriba). Si el
    "continúa" no cabe y se va a la página siguiente, deja una viñeta menos
    en el primer trozo."""
    import copy
    for _ in range(VUELTAS):
        pagina = _pagina_de(render)
        cambio = False
        for guia in raiz.iter('aside'):
            if 'caja-docente' not in _clases(guia) or not guia.get('id'):
                continue
            unidades = _unidades(guia)
            if guia.get('id') not in pagina or any(el.get('id') not in pagina for el in unidades):
                continue
            inicio = pagina[guia.get('id')]
            k = next((k for k, el in enumerate(unidades) if pagina[el.get('id')] > inicio), None)
            if not k:                         # no cruza, o el título quedó solo (lo evita el CSS)
                continue
            for atras in range(min(3, k)):
                prueba = copy.deepcopy(raiz)
                _partir(prueba.get_element_by_id(guia.get('id')), k - atras)
                nuevo = render_de(prueba)
                if _pagina_de(nuevo).get(guia.get('id') + '-sigue') == inicio:
                    raiz, render, cambio = prueba, nuevo, True
                    break
            if cambio:
                break                         # el árbol cambió: se recorre de nuevo
        if not cambio:
            break
    return raiz, render
