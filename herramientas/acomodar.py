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

Después achica figuras para cerrar huecos (él, 2026-10-20): si un bloque
salta a la página siguiente y deja un hueco, prueba achicar la figura que
saltó para que quepa en la anterior o, si el que saltó es una tabla o un
recuadro, achicar la figura de la página anterior para que suba. Nunca bajo
FACTOR_MIN del tamaño que tenía, y solo si el capítulo no gana páginas.

Al final revisa que ninguna ficha de caso quede con la cabecera (cara y
nombre) sola al pie: si la anamnesis empieza en la página siguiente, la
ficha entera pasa a esa página. El primer caso después de un título
("Casos") empieza en la misma página que el título si caben su cabecera y su
anamnesis; si no, el título baja con él (nunca queda solo al pie). Y si el capítulo termina en una página casi
vacía (las últimas líneas de las referencias), aprieta un poco las
referencias para que quepan en la anterior.
"""
import logging

import lxml.html
from weasyprint import HTML

HUECO_MAX = 0.30        # fracción de página vacía al pie que ya se considera hueco
ULTIMA_MIN = 0.25       # la última página con menos de esto lleno se intenta ahorrar
ARRIBA_PX = 40          # la figura "salta" si empieza en los primeros px del contenido
VUELTAS = 40            # el texto sube unidad a unidad hasta llenar los huecos de las columnas
MOVIBLES = ('p', 'ul', 'ol')
HUECO_COL = 0.08       # hueco al pie de una columna que se intenta llenar con el texto que sigue
HUECO_ACHICAR = 0.06    # hueco mínimo (fracción de página) que vale la pena cerrar achicando
FACTOR_MIN = 0.6        # una figura no queda bajo este factor de su tamaño (él: "estás exagerando")


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


def _fondos(pagina):
    """Fondo (y más baja ocupada) de cada columna de la página: (izquierda,
    derecha). En una página a una columna, las dos son iguales."""
    pb = pagina._page_box
    x0, ancho = pb.content_box_x(), pb.width
    mitad = x0 + ancho / 2
    arriba = pb.content_box_y()
    izq = der = arriba
    hay_der = False
    for c in _cajas(pb):
        nombre = type(c).__name__
        if nombre in ('PageBox', 'MarginBox') or not hasattr(c, 'position_y'):
            continue
        if nombre in ('LineBox', 'InlineReplacedBox', 'BlockReplacedBox', 'TableBox') and c.height:
            fondo = c.position_y + c.height
            if c.position_x >= mitad - 2:
                der, hay_der = max(der, fondo), True
            elif c.position_x + c.width > mitad + 20:       # algo a todo el ancho
                izq, der = max(izq, fondo), max(der, fondo)
            else:
                izq = max(izq, fondo)
    return izq, (der if hay_der else izq)


def _hueco_columna(render, p, x):
    """Hueco al pie de la columna que viene ANTES de un bloque que empieza
    arriba en la página p, en la posición x: si el bloque está en la columna
    derecha, la izquierda de la misma página; si está en la izquierda, la
    última columna de la página anterior. En fracción del alto."""
    pag = render.pages[p]
    pb = pag._page_box
    alto, fondo_pag = pb.height, pb.content_box_y() + pb.height
    if x >= pb.content_box_x() + pb.width / 2 - 2:
        izq, _ = _fondos(pag)
        return max(0.0, (fondo_pag - izq) / alto)
    if p == 0:
        return 0.0
    prev = render.pages[p - 1]._page_box
    _, der = _fondos(render.pages[p - 1])
    return max(0.0, (prev.content_box_y() + prev.height - der) / prev.height)


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
    """Cuánto hueco hay al pie de las columnas (sin contar la última página,
    que termina el capítulo donde le toca): el de la columna derecha (o de la
    página, si va a una columna) y el de la izquierda cuando quedó corta y la
    derecha sigue."""
    total = 0.0
    for pag in render.pages[:-1]:
        pb = pag._page_box
        fondo = pb.content_box_y() + pb.height
        izq, der = _fondos(pag)
        gr = (fondo - der) / pb.height
        gl = (fondo - izq) / pb.height if der > izq + 5 else 0.0
        total += sum(g for g in (gl, gr) if g >= HUECO_COL)
    return total


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
            # los Pasos 1-3 que siguen a la ficha: la ficha no queda sola sin ellos
            sig = caso.getnext()
            if sig is not None and 'pasos' in _clases(sig):
                sig.set('id', f'ficha-{i}-p')
            # el título que la precede ("Casos"): no queda solo al pie
            ant = caso.getprevious()
            if ant is not None and ant.tag in ('h2', 'h3'):
                ant.set('id', ant.get('id') or f'ficha-{i}-t')
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
        for p, pagina in enumerate(mejor.pages):
            arriba = pagina._page_box.content_box_y()
            for ancla, (x, y, *_r) in pagina.anchors.items():
                if not ancla.startswith('acomodo-') or ancla in intentadas or y - arriba > ARRIBA_PX:
                    continue
                # hueco de la página anterior o, con texto a dos columnas, de la columna anterior
                h = max(_hueco(mejor.pages[p - 1]) if p else 0.0, _hueco_columna(mejor, p, x))
                if h >= HUECO_COL:
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
    raiz, mejor = _achicar_figuras(raiz, mejor, render_de)
    raiz, mejor = _fichas_enteras(raiz, mejor, render_de)
    raiz, mejor = _partir_guias(raiz, mejor, render_de)
    raiz, mejor = _fichas_enteras(raiz, mejor, render_de)
    raiz, mejor = _saltos_de_mas(raiz, mejor, render_de)
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


def _titulo_de(caso):
    """El título que precede a la ficha (el "Casos" de la sección), o None."""
    ant = caso.getprevious()
    return ant if ant is not None and ant.tag in ('h2', 'h3') else None


def _fichas_enteras(raiz, render, render_de):
    """La ficha cuya anamnesis o cuyos Pasos empiezan en la página siguiente a
    su cabecera pasa entera a esa página.

    El primer caso después de un título ("Casos") es distinto (él, 2026-10-21:
    el título quedaba solo al pie con media página en blanco): ahí basta que
    la cabecera y la anamnesis queden juntas, así el caso empieza en esa
    página y llena el hueco aunque sus Pasos pasen a la siguiente; y si ni eso
    cabe, el título baja con el caso."""
    for _ in range(3):
        pagina = _pagina_de(render)
        cambios = 0
        for c in raiz.find_class('caso'):
            ident = c.get('id')
            if c.tag != 'section' or ident not in pagina:
                continue
            h = pagina[ident]
            a = pagina.get(ident + '-a', h)
            p = pagina.get(ident + '-p', h)
            titulo = _titulo_de(c)
            if titulo is not None:
                if a > h and 'break-before' not in (titulo.get('style') or ''):
                    titulo.set('style', 'break-before: page')
                    cambios += 1
            elif max(a, p) > h and 'break-before' not in (c.get('style') or ''):
                c.set('style', 'break-before: page')
                cambios += 1
        if not cambios:
            break
        render = render_de(raiz)
    return raiz, render


def _saltos_de_mas(raiz, render, render_de):
    """Quita el salto de página que _fichas_enteras le puso a una ficha si
    dejó la página anterior con un hueco grande y sin él la cabecera y la
    anamnesis (y los Pasos) ya quedan juntas: el salto se decidió en una
    composición anterior y después el texto se movió (él, 2026-10-27: la
    ficha de Álvaro del cap. H10 dejaba la página 10 casi en blanco)."""
    import copy
    for c in raiz.find_class('caso'):
        ident = c.get('id')
        if c.tag != 'section' or 'break-before' not in (c.get('style') or ''):
            continue
        pagina = _pagina_de(render)
        h = pagina.get(ident)
        if not h or _hueco(render.pages[h - 1]) < HUECO_MAX:
            continue
        prueba = copy.deepcopy(raiz)
        f = prueba.get_element_by_id(ident)
        del f.attrib['style']
        nuevo = render_de(prueba)
        pag = _pagina_de(nuevo)
        h2 = pag.get(ident)
        if max(pag.get(ident + '-a', h2), pag.get(ident + '-p', h2)) == h2 and len(nuevo.pages) <= len(render.pages):
            raiz, render = prueba, nuevo
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


FIJAS = ('_audiosupra', '_impedancia')    # audiometría e impedanciometría: tamaño acordado, no se tocan
FACTOR_MIN_CASO = 0.75                    # las demás figuras de los casos, poco


def _es_imagen(el):
    """Figura que se puede achicar: un bloque .figobs con una imagen, salvo la
    audiometría y la impedanciometría de los casos, que tienen su tamaño
    acordado (él, 2026-10-20)."""
    if el is None or 'figobs' not in _clases(el):
        return False
    img = el.find('.//img')
    return img is not None and not any(f in (img.get('src') or '') for f in FIJAS)


def _factor_min(el):
    """Cuánto se puede achicar: las figuras del texto de teoría, hasta
    FACTOR_MIN; las de los casos, solo hasta FACTOR_MIN_CASO."""
    return FACTOR_MIN if any('dos-col' in _clases(a) for a in el.iterancestors()) else FACTOR_MIN_CASO


def _medidas(render):
    """{id: [página, alto, ancho de la imagen, ancho del contenido, alto de la imagen]} de los
    bloques acomodables, desde las cajas de la composición."""
    out = {}
    for i, pag in enumerate(render.pages):
        pb = pag._page_box
        for c in _cajas(pb):
            el = getattr(c, 'element', None)
            ident = el.get('id') if el is not None and hasattr(el, 'get') else None
            if not ident or not ident.startswith('acomodo-') or ident in out:
                continue
            img = next((h for h in _cajas(c) if type(h).__name__ in ('InlineReplacedBox', 'BlockReplacedBox')), None)
            out[ident] = [i, c.margin_height(), img.width if img is not None else None, pb.width,
                          img.height if img is not None else None]
    return out


def _achicar(el, factor, medidas):
    """Pone la imagen del bloque al `factor` de su ancho compuesto."""
    _, _, ancho_img, ancho_contenido, _ = medidas
    caja = el.find('.//div[@class="img-globos"]')
    if caja is None or not ancho_img or not ancho_contenido:
        return False
    pct = 100 * ancho_img / ancho_contenido * factor
    caja.set('style', f'width:{pct:.1f}%')
    return True


def _achicar_figuras(raiz, render, render_de):
    import copy
    intentadas = set()
    for _ in range(VUELTAS):
        med = _medidas(render)
        cambio = False
        for p in range(1, len(render.pages)):
            hueco_px = _hueco(render.pages[p - 1]) * render.pages[p - 1]._page_box.height
            if hueco_px < HUECO_ACHICAR * render.pages[p - 1]._page_box.height:
                continue
            pagina = render.pages[p]
            arriba = pagina._page_box.content_box_y()
            saltos = [a for a, (x, y, *_r) in pagina.anchors.items()
                      if a.startswith('acomodo-') and y - arriba <= ARRIBA_PX and a not in intentadas
                      and a in med and med[a][0] == p]
            logging.getLogger('acomodar').debug('pág %d hueco %.0f px, saltan %s', p, hueco_px, saltos)
            for ancla in saltos:
                intentadas.add(ancla)
                el = raiz.get_element_by_id(ancla)
                alto = med[ancla][1]
                faltan = alto - hueco_px + 6
                objetivos = []
                # lo que se achica es la imagen (el pie no cambia): el factor sale de su alto
                if _es_imagen(el) and med[ancla][2]:
                    objetivos.append(([ancla], 1 - faltan / med[ancla][4]))
                previas = sorted((a for a, m in med.items() if m[0] == p - 1 and m[2]
                                  and _es_imagen(raiz.get_element_by_id(a))), key=lambda a: -med[a][4])
                for a in previas:
                    objetivos.append(([a], 1 - faltan / med[a][4]))
                if len(previas) > 1:            # todas las de la página anterior, un poco cada una
                    objetivos.append((previas, 1 - faltan / sum(med[a][4] for a in previas)))
                logging.getLogger('acomodar').debug('  %s alto %.0f faltan %.0f objetivos %s', ancla, alto, faltan,
                                                    [(o, round(f, 2)) for o, f in objetivos])
                for objetivo, factor in objetivos:
                    minimo = max(_factor_min(raiz.get_element_by_id(o)) for o in objetivo)
                    for f in (factor, factor - 0.04):
                        if f < minimo or f >= 0.995:
                            continue
                        prueba = copy.deepcopy(raiz)
                        if not all(_achicar(prueba.get_element_by_id(o), f, med[o]) for o in objetivo):
                            continue
                        nuevo = render_de(prueba)
                        if (len(nuevo.pages) <= len(render.pages)
                                and _pagina_de(nuevo).get(ancla, p) <= p - 1):
                            raiz, render, cambio = prueba, nuevo, True
                            logging.getLogger('acomodar').info('achicada %s al %.0f %% (sube %s)', objetivo, f * 100, ancla)
                            break
                    if cambio:
                        break
                if cambio:
                    break
            if cambio:
                break
        if not cambio:
            break
    return raiz, render
