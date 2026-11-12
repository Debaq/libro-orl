#!/usr/bin/env python3
"""Capítulos en Word para un coautor que solo usa Office, y vuelta al .md.

    python3 herramientas/word_autor.py exportar 21 [--autor poza]
        -> trabajo/Poza/21-vertigo-agudo/   (y trabajo/Poza.zip para enviar, sin los .mapa.json)
             21-vertigo-agudo.docx   el texto, con recuadros, tablas y marcas de figura y caso
             21-figuras.pdf          las figuras numeradas F21-01, F21-02… (solo para mirar)
             21-figuras.xlsx         planilla: qué es cada figura, ¿sirve?, qué cambiar, figuras nuevas
             .mapa.json              lo que el Word no muestra (rutas, anchos, globos, notas)

    python3 herramientas/word_autor.py importar <docx devuelto> [--mapa .mapa.json]
        -> junto al docx:
             <cap>.desde_word.md     el capítulo con sus cambios, para revisar y copiar a texto/
             <cap>.cambios.md        control de cambios, comentarios, casos y figuras a pasar a mano
             <cap>.diff              diff contra el .md original

Idea: el .md se parte en unidades (párrafo, ítem, título, tabla, recuadro,
figura, caso). Cada unidad es un párrafo o una tabla en el Word. Al volver,
se alinean las unidades del Word con las del .md (difflib): las que no
cambiaron se copian tal cual del .md (con sus notas <!-- -->, anchos y
globos) y las que cambiaron se reescriben desde el Word. Nunca se toca
texto/capitulos: el resultado queda al lado del docx.
"""
import copy
import datetime
import difflib
import html
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import zipfile

from docx import Document
from docx.enum.section import WD_ORIENT  # noqa: F401
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

AQUI = pathlib.Path(__file__).resolve().parent
LIBRO = AQUI.parent
CAPITULOS = LIBRO / 'texto' / 'capitulos'
MATERIAL = LIBRO / 'material'
TRABAJO = LIBRO / 'trabajo'

SEP = ' ▸ '
COLORES = {   # relleno de cada recuadro en el Word
    'objetivos': 'E8EEF7', 'ojo': 'FBE5E1', 'ayuda': 'E6F2E6', 'comentario': 'E3EEF8',
    'pregunta': 'FFF6D9', 'docente': 'DDEFE3', 'sabias': 'EEE6F5', 'lado': 'FFFFFF',
    'truco': 'FFF6D9', 'figura': 'EFEFEF', 'caso': 'F5EBDD',
}
ROTULO_FIG = re.compile(r'^\s*FIGURA\s+(F[\w-]+)\s*(?:▸\s*(.*))?$')
ROTULO_CASO = re.compile(r'^\s*CASO\s+([\w.]+)\s*▸\s*([a-z0-9_]+)')
ROTULO_CAJA = re.compile(r'^\s*([A-ZÁÉÍÓÚ-]+)\s*▸\s*(.*)$')
COMENT = re.compile(r'<!--.*?-->', re.S)


# ───────────────────────── el .md en unidades ─────────────────────────

class Nodo:
    """kind: h1..h4, p, li, ol, quote, tabla, caja, img, ilus, fig, caso, res.
    src: texto exacto en el .md (sin salto final)."""

    def __init__(self, kind, src, **kw):
        self.kind, self.src = kind, src
        self.hijos = kw.pop('hijos', None)     # caja: [gap, nodo, gap, nodo, ..., gap]
        self.__dict__.update(kw)

    def nodos(self):
        return self.hijos[1::2] if self.hijos else []


def es_gap(linea):
    s = linea.strip()
    return s == '' or s == '>' or bool(re.fullmatch(r'<!--.*?-->', s))


def parsear(lineas, i=0, dentro=False):
    """Devuelve ([gap, nodo, gap, ...], i) hasta el ':::' que cierra (si dentro)."""
    seq, gap = [], []

    def cerrar_gap():
        seq.append(list(gap))
        gap.clear()

    while i < len(lineas):
        l = lineas[i]
        if dentro and l.strip() == ':::':
            break
        if es_gap(l):
            gap.append(l)
            i += 1
            continue
        cerrar_gap()
        m = re.match(r'^:::([a-z-]+)(?:[ \t]+(.*))?$', l)
        if m:
            tipo, resto = m[1], (m[2] or '').strip()
            if tipo == 'imagen' or tipo == 'figura':
                j = i + 1
                while j < len(lineas) and lineas[j].strip() != ':::':
                    j += 1
                cuerpo = lineas[i + 1:j]
                seq.append(Nodo('img' if tipo == 'imagen' else 'fig', '\n'.join(lineas[i:j + 1]),
                                cabeza=l, cuerpo=cuerpo, resto=resto))
                i = j + 1
            else:
                hijos, j = parsear(lineas, i + 1, True)
                seq.append(Nodo('caja', '\n'.join(lineas[i:j + 1]), tipo=tipo, titulo=resto, hijos=hijos))
                i = j + 1
            continue
        m = re.match(r'^\{\{(caso|resultados)\s+([a-z0-9_]+)\}\}\s*$', l)
        if m:
            seq.append(Nodo('caso' if m[1] == 'caso' else 'res', l, nombre=m[2]))
            i += 1
            continue
        m = re.match(r'^!\[(.*)\]\((\S+)\)\s*$', l)
        if m:
            seq.append(Nodo('ilus', l, alt=m[1], ruta=m[2]))
            i += 1
            continue
        if l.startswith('|'):
            j = i
            while j < len(lineas) and lineas[j].startswith('|'):
                j += 1
            seq.append(Nodo('tabla', '\n'.join(lineas[i:j])))
            i = j
            continue
        m = re.match(r'^(#{1,6}) (.*)$', l)
        if m:
            seq.append(Nodo(f'h{len(m[1])}', l, texto=m[2]))
        elif re.match(r'^\s*[-*] ', l):
            seq.append(Nodo('li', l, texto=re.sub(r'^\s*[-*] ', '', l)))
        elif re.match(r'^\s*\d+\. ', l):
            seq.append(Nodo('ol', l, texto=re.sub(r'^\s*\d+\. ', '', l)))
        elif l.startswith('>'):
            seq.append(Nodo('quote', l, texto=re.sub(r'^>\s?', '', l)))
        else:
            seq.append(Nodo('p', l, texto=l))
        i += 1
    cerrar_gap()
    return seq, i


def filas_tabla(src):
    filas = []
    for l in src.splitlines():
        celdas = [c.strip() for c in l.strip().strip('|').split('|')]
        if all(re.fullmatch(r':?-{3,}:?', c) for c in celdas if c):
            continue
        filas.append(celdas)
    return filas


def partir_imagen(nodo):
    """:::imagen ruta [ancho=..] [completa] [id=..] pie / - @x,y | globo."""
    m = re.match(r'^(\S+)\s*((?:(?:ancho=\S+|completa|id=[a-z0-9-]+)\s+)*)(.*)$', nodo.resto, re.S)
    ruta, attrs, pie = (m[1], m[2], m[3]) if m else (nodo.resto, '', '')
    if nodo.kind == 'fig':      # :::figura nombre tipo [n] [completa]: no hay pie en la cabeza
        ruta, attrs, pie = nodo.resto, '', ''
    globos = []
    otras = []
    for l in nodo.cuerpo:
        g = re.match(r'^-\s*(?:(@[^|]*?)\s*\|\s*)?(.*)$', l)
        if g:
            globos.append((g[1], g[2]))
        elif l.strip():
            otras.append(l)
    idm = re.search(r'id=([a-z0-9-]+)', attrs)
    return dict(ruta=ruta, attrs=attrs, pie=pie, globos=globos, otras=otras, id=idm[1] if idm else None)


# ───────────────────────── inline: md <-> runs ─────────────────────────

def runs_md(texto):
    """'**a** *b*' -> [(texto, negrita, cursiva)]; quita las notas <!-- -->."""
    texto = COMENT.sub('', texto)
    out, b, it = [], False, False
    for tok in re.split(r'(\*\*\*|\*\*|\*)', texto):
        if tok == '***':
            b, it = not b, not it
        elif tok == '**':
            b = not b
        elif tok == '*':
            it = not it
        elif tok:
            out.append((tok, b, it))
    return out


def md_de_runs(runs):
    """[(texto, negrita, cursiva)] -> md, con negrita y cursiva anidadas como en el .md."""
    junt = []
    for t, b, i in runs:
        if not t:
            continue
        if junt and junt[-1][1] == b and junt[-1][2] == i:
            junt[-1][0] += t
        else:
            junt.append([t, b, i])
    out, pila = '', []

    def cerrar(m):
        nonlocal out
        ws = out[len(out.rstrip()):]
        out = out[:len(out) - len(ws)] + m + ws

    for t, b, i in junt:
        if not t.strip():
            out += t
            continue
        quiero = [m for m, si in (('**', b), ('*', i)) if si]
        while any(m not in quiero for m in pila):
            cerrar(pila.pop())
        lead = t[:len(t) - len(t.lstrip())]
        out += lead
        for m in quiero:
            if m not in pila:
                out += m
                pila.append(m)
        out += t.lstrip()
    while pila:
        cerrar(pila.pop())
    return out


def plano(md):
    return re.sub(r'\*+', '', COMENT.sub('', md)).strip()


# ───────────────────────── exportar ─────────────────────────

class Exportador:
    def __init__(self, cap, md_path, salida):
        self.cap, self.md_path, self.salida = cap, md_path, salida
        self.nfig = 0
        self.figuras = []          # dicts para el pdf y la planilla
        self.fig_por_id = {}       # id= -> código
        self.casos = {}
        self.ncaso = 0
        self.seccion = ''
        self.doc = Document()
        self._estilos()
        self.mapa = {'capitulo': cap, 'md': str(md_path.relative_to(LIBRO)),
                     'exportado': datetime.date.today().isoformat(), 'figuras': {}, 'casos': {}}

    # estilos y formato
    def _estilos(self):
        d = self.doc
        sec = d.sections[0]
        sec.page_width, sec.page_height = Cm(21), Cm(29.7)
        for m in ('left_margin', 'right_margin'):
            setattr(sec, m, Cm(2.2))
        normal = d.styles['Normal']
        normal.font.name = 'Calibri'
        normal.font.size = Pt(11)
        normal.paragraph_format.space_after = Pt(6)
        for n, tam, col in ((1, 18, '1F3864'), (2, 15, '2E5597'), (3, 13, '2E5597'), (4, 11.5, '404040')):
            st = d.styles[f'Heading {n}']
            st.font.size = Pt(tam)
            st.font.color.rgb = RGBColor.from_string(col)
            st.font.name = 'Calibri'
        from docx.enum.style import WD_STYLE_TYPE
        for nombre, tam, col in (('Rótulo', 9, '5A5A5A'),):
            st = d.styles.add_style(nombre, WD_STYLE_TYPE.PARAGRAPH)
            st.base_style = normal
            st.font.size = Pt(tam)
            st.font.bold = True
            st.font.color.rgb = RGBColor.from_string(col)
            st.next_paragraph_style = normal

    @staticmethod
    def sombrear(celda, color):
        tcPr = celda._tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), color)
        tcPr.append(shd)

    @staticmethod
    def bordes(tabla, color='A6A6A6'):
        tblPr = tabla._tbl.tblPr
        b = OxmlElement('w:tblBorders')
        for lado in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
            e = OxmlElement(f'w:{lado}')
            e.set(qn('w:val'), 'single')
            e.set(qn('w:sz'), '4')
            e.set(qn('w:color'), color)
            b.append(e)
        look = tblPr.find(qn('w:tblLook'))
        if look is not None:
            look.addprevious(b)
        else:
            tblPr.append(b)

    def escribir_runs(self, par, md, gris=False):
        md = re.sub(r'\{\{fig ([a-z0-9-]+)\}\}', lambda m: f'[{self.fig_por_id.get(m[1], "F?")}]', md)
        for t, b, i in runs_md(md):
            r = par.add_run(t)
            r.bold, r.italic = b or None, i or None
            if gris:
                r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

    def parrafo(self, cont, md='', estilo=None, primero=None):
        p = primero if primero is not None else cont.add_paragraph()
        if estilo:
            p.style = self.doc.styles[estilo]
        self.escribir_runs(p, md)
        return p

    def lista_numerada(self, par, num_id):
        pPr = par._p.get_or_add_pPr()
        numPr = OxmlElement('w:numPr')
        il = OxmlElement('w:ilvl')
        il.set(qn('w:val'), '0')
        ni = OxmlElement('w:numId')
        ni.set(qn('w:val'), str(num_id))
        numPr.extend([il, ni])
        pPr.append(numPr)

    def nueva_numeracion(self):
        """Una numeración nueva (parte en 1) basada en la de 'List Number'."""
        numbering = self.doc.part.numbering_part.element
        st = self.doc.styles['List Number']
        num_id_estilo = st.element.pPr.numPr.numId.val
        abs_id = None
        for num in numbering.findall(qn('w:num')):
            if num.get(qn('w:numId')) == str(num_id_estilo):
                abs_id = num.find(qn('w:abstractNumId')).get(qn('w:val'))
        nuevo = max(int(n.get(qn('w:numId'))) for n in numbering.findall(qn('w:num'))) + 1
        num = OxmlElement('w:num')
        num.set(qn('w:numId'), str(nuevo))
        a = OxmlElement('w:abstractNumId')
        a.set(qn('w:val'), abs_id)
        num.append(a)
        ov = OxmlElement('w:lvlOverride')
        ov.set(qn('w:ilvl'), '0')
        so = OxmlElement('w:startOverride')
        so.set(qn('w:val'), '1')
        ov.append(so)
        num.append(ov)
        numbering.append(num)
        return nuevo

    # recorrido
    def secuencia(self, cont, seq, primero=None):
        """Escribe los nodos de [gap, nodo, gap, ...] en cont (documento o celda)."""
        num_id, previo = None, None
        for nodo in seq[1::2]:
            p = primero
            primero = None
            if nodo.kind == 'ol':
                if previo != 'ol':
                    num_id = self.nueva_numeracion()
                par = self.parrafo(cont, nodo.texto, 'List Number', p)
                self.lista_numerada(par, num_id)
            else:
                self.nodo(cont, nodo, p)
            previo = nodo.kind

    def nodo(self, cont, n, primero=None):
        k = n.kind
        if k[0] == 'h':
            nivel = int(k[1])
            if nivel == 2:
                self.seccion = plano(n.texto)
            if primero is not None:      # título dentro de una celda: va en negrita
                self.parrafo(cont, f'**{n.texto}**', None, primero)
            elif hasattr(cont, 'add_heading'):
                h = cont.add_heading(level=min(nivel, 4))
                self.escribir_runs(h, n.texto)
            else:
                self.parrafo(cont, f'**{n.texto}**')
        elif k == 'p':
            self.parrafo(cont, n.texto, None, primero)
        elif k == 'li':
            self.parrafo(cont, n.texto, 'List Bullet', primero)
        elif k == 'quote':
            self.parrafo(cont, n.texto, 'Quote', primero)
        elif k == 'tabla':
            self.tabla(cont, filas_tabla(n.src), primero)
        elif k == 'caja':
            self.caja(cont, n, primero)
        elif k in ('img', 'fig', 'ilus'):
            self.figura(cont, n, primero)
        elif k in ('caso', 'res'):
            self.caso(cont, n, primero)

    def celda_unica(self, cont, color, primero=None):
        if primero is not None:          # dentro de una celda, el primer párrafo vacío se queda
            pass
        t = cont.add_table(rows=1, cols=1)
        self.bordes(t)
        c = t.cell(0, 0)
        self.sombrear(c, color)
        if primero is not None:
            # que la tabla no quede antes de un párrafo vacío sobrante
            primero._p.addnext(t._tbl)
            primero._p.getparent().remove(primero._p)
        return c

    def caja(self, cont, n, primero=None):
        base = n.tipo.replace('-ancho', '')
        c = self.celda_unica(cont, COLORES.get(base, 'F2F2F2'), primero)
        tit = c.paragraphs[0]
        tit.style = self.doc.styles['Rótulo']
        tit.add_run(f'{n.tipo.upper()}{SEP}')
        r = tit.add_run(COMENT.sub('', n.titulo))
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(0, 0, 0)
        self.secuencia(c, n.hijos)
        # un párrafo vacío después de la tabla, para que dos recuadros no se peguen
        if hasattr(cont, 'add_heading'):
            cont.add_paragraph()

    def tabla(self, cont, filas, primero=None):
        ncol = max(len(f) for f in filas)
        t = cont.add_table(rows=len(filas), cols=ncol)
        self.bordes(t)
        if primero is not None:
            primero._p.addnext(t._tbl)
            primero._p.getparent().remove(primero._p)
        for i, fila in enumerate(filas):
            for j in range(ncol):
                c = t.cell(i, j)
                md = fila[j] if j < len(fila) else ''
                self.escribir_runs(c.paragraphs[0], md)
                if i == 0:
                    self.sombrear(c, 'D9D9D9')
        if hasattr(cont, 'add_heading'):
            cont.add_paragraph()

    def figura(self, cont, n, primero=None):
        self.nfig += 1
        cod = f'F{self.cap}-{self.nfig:02d}'
        if n.kind == 'ilus':
            datos = dict(ruta=n.ruta, attrs='', pie=n.alt, globos=[], otras=[], id=None)
        else:
            datos = partir_imagen(n)
        if datos['id']:
            self.fig_por_id[datos['id']] = cod
        self.mapa['figuras'][cod] = {'kind': n.kind, 'src': n.src, 'id': datos['id'],
                                     'globos': [g for g, _ in datos['globos']]}
        archivo = (f'figura del motor: {datos["ruta"]}' if n.kind == 'fig'
                   else pathlib.Path(datos['ruta']).name)
        self.figuras.append(dict(cod=cod, ruta=datos['ruta'], kind=n.kind, pie=plano(datos['pie']),
                                 globos=[plano(t) for _, t in datos['globos']], seccion=self.seccion))
        c = self.celda_unica(cont, COLORES['figura'], primero)
        tit = c.paragraphs[0]
        tit.style = self.doc.styles['Rótulo']
        tit.add_run(f'FIGURA {cod}{SEP}{archivo}')
        if datos['pie']:
            self.parrafo(c, datos['pie'])
        for _, texto in datos['globos']:
            self.parrafo(c, texto, 'List Bullet')
        if hasattr(cont, 'add_heading'):
            cont.add_paragraph()

    def caso(self, cont, n, primero=None):
        self.ncaso += 1
        num = f'{self.cap}.{self.ncaso}'
        texto = ficha_texto(n.nombre, self.ncaso, self.cap) if n.kind == 'caso' else []
        self.mapa['casos'][n.nombre] = {'numero': num, 'ficha': texto}
        c = self.celda_unica(cont, COLORES['caso'], primero)
        tit = c.paragraphs[0]
        tit.style = self.doc.styles['Rótulo']
        tit.add_run(f'CASO {num}{SEP}{n.nombre}' if n.kind == 'caso' else f'CASO {num}{SEP}{n.nombre} (resultados)')
        nota = c.add_paragraph()
        r = nota.add_run('Datos del paciente: salen del generador del capítulo. Si cambias algo aquí, '
                         'lo pasamos a mano.')
        r.italic = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
        for linea in texto:
            self.parrafo(c, linea)
        if hasattr(cont, 'add_heading'):
            cont.add_paragraph()

    def correr(self):
        lineas = self.md_path.read_text(encoding='utf-8').split('\n')
        seq, _ = parsear(lineas)
        # primero los id= de las figuras, para que {{fig x}} se resuelva aunque la cita vaya antes
        n = 0
        def ids(s):
            nonlocal n
            for x in s[1::2]:
                if x.kind in ('img', 'fig', 'ilus'):
                    n += 1
                    if x.kind == 'img':
                        d = partir_imagen(x)
                        if d['id']:
                            self.fig_por_id[d['id']] = f'F{self.cap}-{n:02d}'
                elif x.kind == 'caja':
                    ids(x.hijos)
        ids(seq)
        sec = self.doc.sections[0]
        cab = sec.header.paragraphs[0]
        cab.text = (f'{self.md_path.stem} · versión para revisión del {self.mapa["exportado"]} · '
                    'trabajar con Control de cambios')
        cab.runs[0].font.size = Pt(8)
        cab.runs[0].font.color.rgb = RGBColor(0x80, 0x80, 0x80)
        self.secuencia(self.doc, seq)
        # Control de cambios encendido al abrir
        settings = self.doc.settings.element
        tr = OxmlElement('w:trackRevisions')
        despues = ('doNotTrackMoves', 'doNotTrackFormatting', 'documentProtection', 'autoFormatOverride',
                   'styleLockTheme', 'styleLockQFSet', 'defaultTabStop', 'autoHyphenation',
                   'consecutiveHyphenLimit', 'hyphenationZone', 'doNotHyphenateCaps', 'showEnvelope',
                   'summaryLength', 'clickAndTypeStyle', 'defaultTableStyle', 'evenAndOddHeaders',
                   'bookFoldRevPrinting', 'bookFoldPrinting', 'bookFoldPrintingSheets',
                   'drawingGridHorizontalSpacing', 'drawingGridVerticalSpacing', 'displayHorizontalDrawingGridEvery',
                   'displayVerticalDrawingGridEvery', 'doNotUseMarginsForDrawingGridOrigin',
                   'drawingGridHorizontalOrigin', 'drawingGridVerticalOrigin', 'doNotShadeFormData',
                   'noPunctuationKerning', 'characterSpacingControl', 'compat', 'rsids', 'mathPr',
                   'themeFontLang', 'clrSchemeMapping', 'decimalSymbol', 'listSeparator')
        sig = next((e for e in settings if e.tag.split('}')[1] in despues), None)
        if sig is not None:
            sig.addprevious(tr)
        else:
            settings.append(tr)
        self.salida.mkdir(parents=True, exist_ok=True)
        nombre = self.md_path.stem
        self.doc.save(self.salida / f'{nombre}.docx')
        (self.salida / '.mapa.json').write_text(json.dumps(self.mapa, ensure_ascii=False, indent=1),
                                               encoding='utf-8')
        return nombre


def ficha_texto(nombre, numero, cap):
    """La ficha del caso como la arma el libro, en párrafos de texto."""
    sys.path.insert(0, str(AQUI))
    try:
        import hacer_libro as h
        h_ = h.ficha(nombre, numero, str(cap), False)
    except Exception as e:  # noqa: BLE001
        return [f'(no se pudo armar la ficha: {e})']
    h_ = re.sub(r'<img[^>]*>', '', h_)
    h_ = re.sub(r'<p class="caso-num">.*?</p>', '', h_)
    h_ = h_.replace('<strong class="od">OD</strong>', '**Otoscopía OD:**').replace(
        '<strong class="oi">OI</strong>', '**Otoscopía OI:**')
    h_ = re.sub(r'<strong>(.*?)</strong>', r'**\1**', h_)
    h_ = re.sub(r'<span class="cuando">(.*?)</span>', r'\1:', h_)
    h_ = re.sub(r'</?(p|li|figcaption|div|section|ul|figure)[^>]*>', '\n', h_)
    h_ = re.sub(r'<[^>]+>', '', h_)
    lineas = [html.unescape(re.sub(r'\s+', ' ', l)).strip() for l in h_.split('\n')]
    lineas = [l for l in lineas if l]
    # nombre y edad en una línea
    if len(lineas) >= 2 and '·' in lineas[1]:
        lineas[0:2] = [f'**{lineas[0]}**, {lineas[1]}']
    return lineas


def png_de(ruta, destino):
    """Una figura a PNG para el PDF y la planilla. Devuelve la ruta o None."""
    if ruta.startswith('/'):
        archivo = MATERIAL / 'labsim' / ruta.lstrip('/')
    else:
        archivo = MATERIAL / ruta
    if not archivo.exists():
        return None
    if archivo.suffix.lower() == '.svg':
        subprocess.run(['rsvg-convert', '-w', '1400', '-b', 'white', '-o', str(destino), str(archivo)],
                       check=False, capture_output=True)
    else:
        subprocess.run(['magick', str(archivo), '-resize', '1400x1400>', str(destino)],
                       check=False, capture_output=True)
    return destino if destino.exists() else None


def figuras_motor(nombre, tipo, n):
    """:::figura nombre tipo [n] -> figuras/salida/<nombre>_<tipo>[ _n].svg (si existe)."""
    # como el libro: las del motor en figuras/salida y las hechas a mano en ilustraciones/
    for carpeta in ('figuras/salida', 'ilustraciones'):
        for cand in (f'{nombre}_{tipo}_{n}.svg', f'{nombre}_{tipo}{n}.svg', f'{nombre}_{tipo}.svg'):
            if (MATERIAL / carpeta / cand).exists() and (n in ('', '1') or cand != f'{nombre}_{tipo}.svg'):
                return f'{carpeta}/{cand}'
    return None


def pdf_y_planilla(exp, salida, nombre):
    tmp = pathlib.Path(tempfile.mkdtemp(dir=salida))
    try:
        doc = Document()
        sec = doc.sections[0]
        sec.page_width, sec.page_height = Cm(21), Cm(29.7)
        for m in ('left_margin', 'right_margin', 'top_margin', 'bottom_margin'):
            setattr(sec, m, Cm(1.8))
        doc.styles['Normal'].font.name = 'Calibri'
        doc.add_heading(f'Figuras del capítulo {exp.cap}', level=1)
        doc.add_paragraph('Cada figura lleva el código con que aparece en el Word del capítulo. '
                          'Las observaciones van en la planilla ' + f'{exp.cap}-figuras.xlsx.')
        pngs = {}
        for f in exp.figuras:
            ruta = f['ruta']
            if f['kind'] == 'fig':
                partes = ruta.split()
                ruta = figuras_motor(partes[0], partes[1] if len(partes) > 1 else '',
                                     partes[2] if len(partes) > 2 and partes[2].isdigit() else '') or ruta
            png = png_de(ruta, tmp / f'{f["cod"]}.png')
            pngs[f['cod']] = png
            if f is not exp.figuras[0]:
                doc.add_page_break()
            p = doc.add_paragraph()
            r = p.add_run(f'{f["cod"]}   ')
            r.bold = True
            r.font.size = Pt(16)
            r2 = p.add_run(f'{f["seccion"]} · {pathlib.Path(ruta).name}')
            r2.font.size = Pt(9)
            r2.font.color.rgb = RGBColor(0x70, 0x70, 0x70)
            if png:
                from PIL import Image
                with Image.open(png) as im:
                    w, h = im.size
                ancho = 17.0
                if h / w * ancho > 17:
                    ancho = 17 * w / h
                doc.add_picture(str(png), width=Cm(ancho))
                doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                doc.add_paragraph(f'(no está el archivo de la imagen: {ruta})')
            if f['pie']:
                doc.add_paragraph(f['pie']).runs[0].font.size = Pt(10)
            for g in f['globos']:
                doc.add_paragraph(g, style='List Bullet').runs[0].font.size = Pt(9)
        docx_fig = tmp / f'{exp.cap}-figuras.docx'
        doc.save(docx_fig)
        subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', str(salida), str(docx_fig)],
                       check=False, capture_output=True, timeout=300)

        # planilla
        from openpyxl import Workbook
        from openpyxl.drawing.image import Image as XLImage
        from openpyxl.styles import Alignment, Font, PatternFill
        from openpyxl.worksheet.datavalidation import DataValidation
        wb = Workbook()
        ws = wb.active
        ws.title = 'Figuras'
        cab = ['Código', 'Miniatura', 'Sección', 'Archivo', 'Pie actual (se cambia en el Word)',
               '¿Sirve?', 'Qué cambiar']
        ws.append(cab)
        for i, ancho in enumerate((10, 24, 16, 26, 60, 12, 50), start=1):
            ws.column_dimensions[chr(64 + i)].width = ancho
        dv = DataValidation(type='list', formula1='"Sí,Cambiar,Sacar"', allow_blank=True)
        ws.add_data_validation(dv)
        for k, f in enumerate(exp.figuras, start=2):
            ws.append([f['cod'], '', f['seccion'], pathlib.Path(f['ruta']).name, f['pie'], '', ''])
            dv.add(f'F{k}')
            ws.row_dimensions[k].height = 95
            png = pngs.get(f['cod'])
            if png:
                from PIL import Image
                mini = tmp / f'{f["cod"]}-mini.png'
                with Image.open(png) as im:
                    im.thumbnail((170, 120))
                    im.save(mini)
                ws.add_image(XLImage(str(mini)), f'B{k}')
        for fila in ws.iter_rows():
            for c in fila:
                c.alignment = Alignment(wrap_text=True, vertical='top')
        for c in ws[1]:
            c.font = Font(bold=True)
            c.fill = PatternFill('solid', fgColor='D9D9D9')
        ws.freeze_panes = 'A2'
        ws2 = wb.create_sheet('Figuras nuevas')
        ws2.append(['Código', 'Dónde va (sección o párrafo)', 'Qué debe mostrar', 'Fuente o referencia, si hay'])
        for i, ancho in enumerate((12, 40, 70, 40), start=1):
            ws2.column_dimensions[chr(64 + i)].width = ancho
        for j in range(1, 11):
            ws2.append([f'F{exp.cap}-N{j}', '', '', ''])
        for c in ws2[1]:
            c.font = Font(bold=True)
            c.fill = PatternFill('solid', fgColor='D9D9D9')
        for fila in ws2.iter_rows(min_row=2):
            for c in fila:
                c.alignment = Alignment(wrap_text=True, vertical='top')
        wb.save(salida / f'{exp.cap}-figuras.xlsx')
    finally:
        # el temporal dentro de la carpeta, para que soffice lo lea; se borra al final
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


LEEME = [
    ('h', 'Cómo revisar los capítulos'),
    ('p', 'Cada capítulo viene en una carpeta con tres archivos: el Word con el texto, un PDF con las figuras '
          'y una planilla Excel para las figuras.'),
    ('p', 'El libro no se arma a mano: lo arma un **sistema de maquetado automático con reglas fijas**. '
          'Ese sistema lee la estructura del Word (títulos, recuadros, rótulos, códigos de figura y de caso) '
          'para saber qué es cada cosa y dónde va. Por eso el archivo es **sensible a esa estructura**: si se '
          'borra un rótulo, se cambia un código o se desarma un recuadro, el sistema no lo reconoce y ese trozo '
          'hay que rehacerlo a mano.'),
    ('p', 'El contenido lo puedes cambiar todo lo que quieras. Lo que hay que respetar es **la forma**. Las reglas '
          'de abajo son para eso.'),
    ('h2', 'El texto (el Word)'),
    ('n', 'El **Control de cambios** viene encendido (Revisar → Control de cambios). **No lo apagues**: así '
          'vemos exactamente qué cambiaste.'),
    ('n', 'Corrige y escribe directo en el texto. Para dudas o propuestas usa **comentarios** '
          '(Revisar → Nuevo comentario).'),
    ('n', 'Los **recuadros de color** empiezan con un rótulo en mayúsculas antes de ▸ (OJO, AYUDA, PREGUNTA, '
          'COMENTARIO…). **No borres ese rótulo.** El título que va después de ▸ sí lo puedes cambiar. '
          'Para un recuadro nuevo, copia uno del mismo tipo y cambia su contenido.'),
    ('n', 'Los recuadros **CASO** (color beige) son los datos del paciente. Puedes corregirlos; nosotros los '
          'pasamos a mano.'),
    ('n', 'Usa negrita y cursiva como quieras. Otros formatos (colores, tamaños de letra, subrayado) se pierden '
          'al volver al libro.'),
    ('h2', 'Las figuras'),
    ('n', 'En el Word, cada figura es un recuadro gris: **FIGURA F21-03 ▸ archivo**. La imagen está en el PDF '
          'con el mismo código. En el recuadro puedes corregir el **pie** y los puntos de la figura.'),
    ('n', 'Para **cambiar o sacar** una figura, anótalo en la planilla (columnas «¿Sirve?» y «Qué cambiar»).'),
    ('n', 'Para **pedir una figura nueva**: copia un recuadro FIGURA donde debe ir, cambia el código por '
          '**F21-N1** (después N2, N3…), escribe el pie y descríbela en la planilla, hoja «Figuras nuevas».'),
    ('n', 'Para nombrar una figura en el texto, escribe su código entre corchetes: **[F21-03]**.'),
    ('h2', 'Al terminar'),
    ('n', 'Devuelve el **Word y la planilla** con el mismo nombre. No hace falta aceptar los cambios.'),
]


def escribir_leeme(destino):
    d = Document()
    d.styles['Normal'].font.name = 'Calibri'
    d.styles['Normal'].font.size = Pt(11.5)
    exp = Exportador.__new__(Exportador)
    exp.doc, exp.fig_por_id = d, {}
    num = None
    for tipo, texto in LEEME:
        if tipo == 'h':
            d.add_heading(texto, level=1)
        elif tipo == 'h2':
            d.add_heading(texto, level=2)
            num = None
        elif tipo == 'n':
            if num is None:
                num = exp.nueva_numeracion()
            par = d.add_paragraph(style='List Number')
            exp.escribir_runs(par, texto)
            exp.lista_numerada(par, num)
        else:
            exp.escribir_runs(d.add_paragraph(), texto)
    d.save(destino)


def carpeta_autor(autor):
    """trabajo/Poza: el nombre que ve el coautor al recibir el zip (él, 2026-11-12: 'para_poza'
    es feo para enviárselo)."""
    return TRABAJO / autor.capitalize()


def empaquetar(autor):
    """trabajo/Poza.zip con la carpeta del autor, sin los .mapa.json (son nuestros)."""
    carpeta = carpeta_autor(autor)
    destino = carpeta.with_suffix('.zip')
    with zipfile.ZipFile(destino, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(carpeta.rglob('*')):
            if f.is_file() and f.name != '.mapa.json':
                z.write(f, f.relative_to(TRABAJO))
    print(f'{destino.relative_to(LIBRO)} listo para enviar')


def exportar(cap, autor):
    m = re.fullmatch(r'([BH]?)0*(\d+)', cap)
    if not m:
        raise SystemExit(f'capítulo no válido: {cap}')
    cap = f'{m[1]}{int(m[2])}'                                   # B05 -> B5, 01 -> 1
    nombres = {f'{m[1]}{int(m[2]):02d}', f'{m[1]}{int(m[2])}'}  # el archivo es B05-…, H01-…, 01-…, H12-…
    md = next((x for x in sorted(CAPITULOS.glob('*.md')) if x.stem.split('-')[0] in nombres), None)
    if md is None:
        raise SystemExit(f'no encontré el .md del capítulo {cap}')
    salida = carpeta_autor(autor) / md.stem
    salida.mkdir(parents=True, exist_ok=True)
    escribir_leeme(salida.parent / 'LEEME.docx')
    exp = Exportador(cap, md, salida)
    nombre = exp.correr()
    pdf_y_planilla(exp, salida, nombre)
    if (salida / f'{cap}-figuras.pdf').exists() is False:
        print('  ojo: no salió el PDF de figuras (soffice)')
    print(f'{salida.relative_to(LIBRO)}/: {nombre}.docx, {cap}-figuras.pdf, {cap}-figuras.xlsx '
          f'({exp.nfig} figuras, {exp.ncaso} casos)')


# ───────────────────────── importar ─────────────────────────

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def _on(rpr, tag):
    if rpr is None:
        return False
    e = rpr.find(W + tag)
    return e is not None and e.get(W + 'val') not in ('0', 'false', 'none')


class Lector:
    """Lee el docx con los cambios aceptados y anota lo que hizo el control de cambios."""

    def __init__(self, ruta):
        self.doc = Document(ruta)
        self.estilos = {s.style_id: s.name for s in self.doc.styles}
        self.revisiones = []   # (tipo, autor, texto, contexto)
        self.comentarios = {}  # id -> (autor, texto)
        self.anclas = {}       # id -> texto marcado
        self._comentarios(ruta)

    def _comentarios(self, ruta):
        with zipfile.ZipFile(ruta) as z:
            if 'word/comments.xml' not in z.namelist():
                return
            from lxml import etree
            raiz = etree.fromstring(z.read('word/comments.xml'))
            for c in raiz.findall(W + 'comment'):
                texto = '\n'.join(''.join(t.text or '' for t in p.iter(W + 't')) for p in c.findall(W + 'p'))
                self.comentarios[c.get(W + 'id')] = (c.get(W + 'author') or '', texto.strip())

    def runs(self, p_el, abiertos):
        """Runs de un párrafo (cambios aceptados): [(texto, b, i)]; anota ins/del."""
        out, antes, autores = [], [], set()
        for el in p_el.iter():
            tag = el.tag
            if tag == W + 'commentRangeStart':
                abiertos[el.get(W + 'id')] = []
            elif tag == W + 'commentRangeEnd':
                pass
            elif tag == W + 'commentReference':
                abiertos.setdefault(el.get(W + 'id'), [])
            elif tag == W + 'r':
                anc = [a.tag for a in el.iterancestors() if a.tag in (W + 'ins', W + 'del', W + 'moveFrom', W + 'moveTo')]
                borrado = bool(anc) and anc[0] in (W + 'del', W + 'moveFrom')
                texto = ''
                for t in el:
                    if t.tag in (W + 't', W + 'delText'):
                        texto += t.text or ''
                    elif t.tag == W + 'tab':
                        texto += '\t'
                    elif t.tag in (W + 'br', W + 'cr'):
                        texto += ' '
                if not texto:
                    continue
                if anc:
                    autores.add(next(a for a in el.iterancestors() if a.tag == anc[0]).get(W + 'author') or '')
                if not (anc and anc[0] in (W + 'ins', W + 'moveTo')):
                    antes.append(texto)
                if borrado:
                    continue
                for v in abiertos.values():
                    v.append(texto)
                rpr = el.find(W + 'rPr')
                out.append((texto, _on(rpr, 'b'), _on(rpr, 'i')))
        for k, v in abiertos.items():
            self.anclas[k] = self.anclas.get(k, '') + ''.join(v)
        abiertos.clear()
        if autores:
            self.revisiones.append((', '.join(sorted(a for a in autores if a)) or '?', ''.join(antes),
                                    ''.join(t for t, _, _ in out)))
        return out

    def estilo(self, p_el):
        ps = p_el.find(f'{W}pPr/{W}pStyle')
        sid = ps.get(W + 'val') if ps is not None else 'Normal'
        return (self.estilos.get(sid) or sid).lower()

    @staticmethod
    def marca_borrada(p_el):
        return p_el.find(f'{W}pPr/{W}rPr/{W}del') is not None

    def numerado(self, p_el):
        """None, 'li' o 'ol' según la numeración del párrafo (o de su estilo)."""
        n = p_el.find(f'{W}pPr/{W}numPr/{W}numId')
        if n is None:
            return None
        num_id = n.get(W + 'val')
        if num_id == '0':
            return None
        try:
            numbering = self.doc.part.numbering_part.element
        except Exception:  # noqa: BLE001
            return 'li'
        for num in numbering.findall(W + 'num'):
            if num.get(W + 'numId') == num_id:
                abs_id = num.find(W + 'abstractNumId').get(W + 'val')
                for a in numbering.findall(W + 'abstractNum'):
                    if a.get(W + 'abstractNumId') == abs_id:
                        fmt = a.find(f'{W}lvl/{W}numFmt')
                        return 'li' if fmt is not None and fmt.get(W + 'val') == 'bullet' else 'ol'
        return 'li'

    def bloques(self, cont_el):
        """Elementos de un contenedor (body o celda) en orden: ('p', estilo, runs, num) | ('tbl', el)."""
        out = []
        pegar = False
        for el in cont_el:
            if el.tag == W + 'p':
                rs = self.runs(el, {})
                est = self.estilo(el)
                if pegar and out and out[-1][0] == 'p':
                    out[-1] = ('p', out[-1][1], out[-1][2] + rs, out[-1][3])
                else:
                    out.append(('p', est, rs, self.numerado(el)))
                pegar = self.marca_borrada(el)
            elif el.tag == W + 'tbl':
                out.append(('tbl', el))
                pegar = False
            elif el.tag == W + 'sdt':
                c = el.find(W + 'sdtContent')
                if c is not None:
                    out.extend(self.bloques(c))
        return out

    def filas(self, tbl):
        filas = []
        for tr in tbl.findall(W + 'tr'):
            if tr.find(f'{W}trPr/{W}del') is not None:
                continue
            fila = []
            for tc in tr.findall(W + 'tc'):
                fila.append(self.bloques(tc))
            filas.append(fila)
        return filas


def texto_bloque(b):
    return md_de_runs(b[2]).strip()


def unidades(lector, bloques):
    """Bloques del Word -> nodos 'nuevos' (sin src) con lo que el autor dejó."""
    out = []
    for b in bloques:
        if b[0] == 'p':
            est, md = b[1], texto_bloque(b)
            if not md:
                continue
            m = re.match(r'(?:heading|título|titulo)\s*(\d)', est)
            if m:
                out.append(Nodo(f'h{m[1]}', None, texto=md))
            elif b[3]:
                out.append(Nodo(b[3], None, texto=md))
            elif 'list bullet' in est or 'viñeta' in est:
                out.append(Nodo('li', None, texto=md))
            elif 'list number' in est or 'número' in est:
                out.append(Nodo('ol', None, texto=md))
            elif 'quote' in est or 'cita' in est:
                out.append(Nodo('quote', None, texto=md))
            else:
                out.append(Nodo('p', None, texto=md))
            continue
        filas = lector.filas(b[1])
        if not filas:
            continue
        # un recuadro es una tabla de una celda; si Word juntó dos recuadros pegados,
        # queda una tabla de varias filas de una celda, cada una con su rótulo
        if all(len(f) == 1 for f in filas):
            cajas = [caja_de_celda(lector, f[0]) for f in filas]
            if all(cajas):
                out.extend(cajas)
                continue
        # tabla de datos
        celdas = [[' '.join(texto_bloque(x) for x in celda if x[0] == 'p' and texto_bloque(x)) for celda in fila]
                  for fila in filas]
        out.append(Nodo('tabla', None, filas=celdas))
    return out


def caja_de_celda(lector, dentro):
    """Una celda con rótulo (FIGURA, CASO o TIPO ▸ título) -> nodo; si no tiene rótulo, None."""
    primero = next((x for x in dentro if x[0] == 'p' and texto_bloque(x)), None)
    if primero is None:
        return None
    cab = plano(texto_bloque(primero))
    resto = dentro[dentro.index(primero) + 1:]
    m = ROTULO_FIG.match(cab)
    if m:
        pars = [texto_bloque(x) for x in resto if x[0] == 'p' and texto_bloque(x)]
        vinetas = [texto_bloque(x) for x in resto
                   if x[0] == 'p' and texto_bloque(x) and ('list' in x[1] or 'viñeta' in x[1] or x[3])]
        pie = [t for t in pars if t not in vinetas]
        return Nodo('img?', None, cod=m[1], cabeza=(m[2] or '').strip(), pie=' '.join(pie), globos=vinetas)
    m = ROTULO_CASO.match(cab)
    if m:
        texto = [texto_bloque(x) for x in resto if x[0] == 'p' and texto_bloque(x)]
        texto = [t for t in texto if not plano(t).startswith('Datos del paciente: salen')]
        return Nodo('caso?', None, nombre=m[2], ficha=texto)
    m = ROTULO_CAJA.match(cab)
    if m:
        titulo = texto_bloque(primero).split('▸', 1)[1].strip()
        titulo = re.sub(r'^\*+\s*|\s*\*+$', '', titulo) if titulo.count('*') % 2 else titulo
        seq = [[]]
        for h in unidades(lector, resto):
            seq += [h, []]
        return Nodo('caja', None, tipo=m[1].lower(), titulo=titulo, hijos=seq)
    return None


def clave(n, mapa):
    """Lo que se compara para saber si una unidad cambió (texto como lo ve el autor)."""
    k = n.kind
    if n.src is not None:            # nodo del .md
        if k in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'ol', 'quote'):
            return (k, norm(n.texto))
        if k == 'tabla':
            return (k, tuple(tuple(norm(c) for c in f) for f in filas_tabla(n.src)))
        if k == 'caja':
            return (k, n.tipo, norm(n.titulo), tuple(clave(h, mapa) for h in n.nodos()))
        if k in ('img', 'fig', 'ilus'):
            d = (dict(pie=n.alt, globos=[]) if k == 'ilus' else partir_imagen(n))
            return ('img', n.cod, norm(d['pie']), tuple(norm(t) for _, t in d['globos']))
        if k in ('caso', 'res'):
            return ('caso', n.nombre)
    if k == 'tabla':
        return (k, tuple(tuple(norm(c) for c in f) for f in n.filas))
    if k == 'caja':
        return (k, n.tipo, norm(n.titulo), tuple(clave(h, mapa) for h in n.nodos()))
    if k == 'img?':
        return ('img', n.cod, norm(n.pie), tuple(norm(g) for g in n.globos))
    if k == 'caso?':
        return ('caso', n.nombre)
    return (k, norm(n.texto))


def norm(md):
    """Texto comparable: sin notas, con {{fig x}} como [Fnn-mm] y espacios uniformes."""
    md = COMENT.sub('', md or '')
    md = re.sub(r'\{\{fig ([a-z0-9-]+)\}\}', lambda m: f'[{NORM_IDS.get(m[1], "F?")}]', md)
    md = md.replace(' ', ' ')
    md = md_de_runs(runs_md(md))     # '**a.** **b**' = '**a. b**', como en Word
    return re.sub(r'\s+', ' ', md).strip()


NORM_IDS = {}


class Importador:
    def __init__(self, docx, mapa_path):
        self.mapa = json.loads(mapa_path.read_text(encoding='utf-8'))
        self.md_path = LIBRO / self.mapa['md']
        self.original = self.md_path.read_text(encoding='utf-8')
        self.lector = Lector(docx)
        self.notas = []        # cosas a pasar a mano
        self.cod_de_id = {v['id']: k for k, v in self.mapa['figuras'].items() if v.get('id')}
        NORM_IDS.update(self.cod_de_id)
        self.id_de_cod = {v: k for k, v in self.cod_de_id.items()}

    def numerar(self, seq):
        """Pone a cada figura del .md su código, en el mismo orden que al exportar."""
        n = 0
        def rec(s):
            nonlocal n
            for x in s[1::2]:
                if x.kind in ('img', 'fig', 'ilus'):
                    n += 1
                    x.cod = f'F{self.mapa["capitulo"]}-{n:02d}'
                elif x.kind == 'caja':
                    rec(x.hijos)
        rec(seq)

    # md de un nodo nuevo (o cambiado), usando el original emparejado para lo que no se ve
    def md_inline(self, md):
        md = re.sub(r'\[(F[\w]+-\d+)\]', lambda m: ('{{fig ' + self.id_de_cod[m[1]] + '}}')
                    if m[1] in self.id_de_cod else m[0], md)
        for m in re.finditer(r'\[(F[\w]+-[\w]+)\]', md):
            self.notas.append(f'El texto cita **{m[1]}**, que no tiene `id=`: poner el id en la figura y '
                              f'cambiar la cita por `{{{{fig <id>}}}}`.')
        return md

    def emitir(self, nuevo, orig, num_previo):
        md = self._emitir(nuevo, orig, num_previo)
        if (orig is not None and orig.src and '<!--' in orig.src
                and orig.kind not in ('caja', 'img', 'fig', 'tabla') and nuevo.kind in ('p', 'li', 'ol', 'quote')
                or (orig is not None and orig.kind[0] == 'h' and '<!--' in orig.src)):
            md = self.reponer_notas(orig.src, md)
        return md

    def reponer_notas(self, src, md):
        """Vuelve a poner cada <!-- nota --> del párrafo original detrás del mismo texto, si sigue ahí."""
        partes = re.split(r'(<!--.*?-->)', src, flags=re.S)
        desde = 0
        for i, parte in enumerate(partes):
            if not parte.startswith('<!--'):
                continue
            previo = ''.join(x for x in partes[:i] if not x.startswith('<!--'))
            puesto = False
            for largo in (40, 20, 10):
                ancla = previo[-largo:]
                if len(ancla.strip()) < 5:
                    break
                k = md.find(ancla, desde)
                if k >= 0:
                    corte = k + len(ancla)
                    md = md[:corte] + parte + md[corte:]
                    desde = corte + len(parte)
                    puesto = True
                    break
            if not puesto:
                md += parte
                self.notas.append(f'Párrafo con nota interna que cambió donde estaba la nota; quedó al final: '
                                  f'«{plano(md)[:80]}…»')
        return md

    def _emitir(self, nuevo, orig, num_previo):
        k = nuevo.kind
        coment = ''
        if k[0] == 'h':
            return '#' * int(k[1]) + ' ' + self.md_inline(nuevo.texto)
        if k == 'p':
            return self.md_inline(nuevo.texto)
        if k == 'li':
            pre = re.match(r'^\s*[-*] ', orig.src)[0] if orig is not None and orig.kind == 'li' else '- '
            return pre + self.md_inline(nuevo.texto)
        if k == 'ol':
            if orig is not None and orig.kind == 'ol':
                pre = re.match(r'^\s*\d+\. ', orig.src)[0]
            else:
                pre = '1. ' if num_previo in (None, '1') else f'{int(num_previo) + 1}. '
            return pre + self.md_inline(nuevo.texto)
        if k == 'quote':
            return '> ' + self.md_inline(nuevo.texto)
        if k == 'tabla':
            filas = [[self.md_inline(c) for c in f] for f in nuevo.filas]
            ncol = max(len(f) for f in filas)
            sep = None
            if orig is not None and orig.kind == 'tabla':
                sep = next((l for l in orig.src.splitlines() if re.fullmatch(r'\|?(\s*:?-{3,}:?\s*\|)+\s*', l)), None)
            sep = sep if sep and sep.count('|') - 1 == ncol else '|' + '---|' * ncol
            ls = ['| ' + ' | '.join(f + [''] * (ncol - len(f))) + ' |' for f in filas]
            return '\n'.join([ls[0], sep] + ls[1:])
        if k == 'caja':
            hijos_o = orig.hijos if orig is not None and orig.kind == 'caja' else [[]]
            cuerpo = self.alinear(hijos_o, nuevo.nodos(), dentro=True)
            tit = self.md_inline(nuevo.titulo)
            if orig is not None and orig.kind == 'caja' and norm(orig.titulo) == norm(tit):
                tit = orig.titulo
            return f':::{nuevo.tipo}{(" " + tit) if tit else ""}\n{cuerpo}\n:::'
        if k == 'img?':
            return self.emitir_figura(nuevo, orig)
        if k == 'caso?':
            return self.emitir_caso(nuevo)
        raise ValueError(k)

    def emitir_figura(self, nuevo, orig):
        info = self.mapa['figuras'].get(nuevo.cod)
        if info is None:     # figura nueva que pidió el autor
            self.notas.append(f'Figura nueva **{nuevo.cod}**: «{plano(nuevo.pie)[:100]}». Ver la planilla, hoja '
                              '"Figuras nuevas". En el .md quedó como imagen pendiente.')
            globos = ''.join(f'\n- {self.md_inline(g)}' for g in nuevo.globos)
            return f':::imagen ilustraciones/PENDIENTE-{nuevo.cod}.svg {self.md_inline(nuevo.pie)}{globos}\n:::'
        src = info['src']
        o = Nodo(info['kind'], src)
        if info['kind'] == 'ilus':
            m = re.match(r'^!\[(.*)\]\((\S+)\)\s*$', src)
            return f'![{self.md_inline(nuevo.pie)}]({m[2]})'
        lineas = src.split('\n')
        m = re.match(r'^:::([a-z-]+)(?:[ \t]+(.*))?$', lineas[0])
        o.resto, o.cuerpo = (m[2] or '').strip(), lineas[1:-1]
        d = partir_imagen(o)
        globos_o = d['globos']
        pie = self.md_inline(nuevo.pie)
        if norm(pie) == norm(d['pie']):
            pie = d['pie']
        if info['kind'] == 'fig':
            cabeza = lineas[0]
            if pie:
                self.notas.append(f'{nuevo.cod} (figura del motor) recibió un pie que el formato no tiene: '
                                  f'«{plano(pie)[:100]}»')
        else:
            cabeza = f':::imagen {d["ruta"]} {d["attrs"]}{pie}'.rstrip()
        cuerpo = []
        for j, g in enumerate(nuevo.globos):
            g = self.md_inline(g)
            if j < len(globos_o):
                marca, texto_o = globos_o[j]
                if norm(texto_o) == norm(g):
                    g = texto_o
                cuerpo.append(f'- {marca} | {g}' if marca else f'- {g}')
            else:
                cuerpo.append(f'- {g}')
                self.notas.append(f'{nuevo.cod}: punto nuevo en la figura, sin ubicación: «{plano(g)[:80]}»')
        if len(nuevo.globos) < len(globos_o):
            self.notas.append(f'{nuevo.cod}: el autor sacó {len(globos_o) - len(nuevo.globos)} globo(s); '
                              'revisar que los que quedan calcen con su ubicación (se emparejaron por orden).')
        cuerpo += d['otras']
        return '\n'.join([cabeza] + cuerpo + [':::'])

    def emitir_caso(self, nuevo):
        if nuevo.nombre not in self.mapa['casos']:
            self.notas.append(f'Caso desconocido en el Word: {nuevo.nombre}')
        return '{{caso ' + nuevo.nombre + '}}'

    def revisar_fichas(self, nodos):
        for n in nodos:
            if n.kind == 'caja':
                self.revisar_fichas(n.nodos())
            if n.kind != 'caso?' or n.nombre not in self.mapa['casos']:
                continue
            info = self.mapa['casos'][n.nombre]
            antes = [plano(x) for x in info['ficha']]
            ahora = [plano(x) for x in n.ficha]
            if antes != ahora:
                d = '\n'.join(difflib.unified_diff(antes, ahora, 'antes', 'ahora', lineterm='', n=0)
                              ).split('\n', 2)[-1]
                self.notas.append(f'**Caso {info["numero"]} ({n.nombre})**: cambió la ficha; pasarlo al '
                                  f'`.py` del capítulo:\n\n  ```diff\n' + '\n'.join('  ' + x for x in d.split('\n'))
                                  + '\n  ```')

    def alinear(self, seq_o, nuevos, dentro=False):
        """seq_o: [gap, nodo, gap, ...] del .md; nuevos: nodos del Word -> texto md."""
        orig = seq_o[1::2]
        gaps = seq_o[0::2]
        ko = [clave(n, self.mapa) for n in orig]
        kn = [clave(n, self.mapa) for n in nuevos]
        sm = difflib.SequenceMatcher(None, ko, kn, autojunk=False)
        piezas = []      # (texto, índice original o None)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == 'equal':
                for d in range(i2 - i1):
                    piezas.append((orig[i1 + d].src, i1 + d))
                continue
            os_, ns = orig[i1:i2], nuevos[j1:j2]
            pares = emparejar(os_, ns)
            usados = set()
            for j, n in enumerate(ns):
                o = pares.get(j)
                if o is not None:
                    usados.add(o)
                prev = None
                if piezas and re.match(r'^\s*(\d+)\. ', piezas[-1][0] or ''):
                    prev = re.match(r'^\s*(\d+)\. ', piezas[-1][0])[1]
                piezas.append((self.emitir(n, os_[o] if o is not None else None, prev),
                               (i1 + o) if o is not None else None))
            for o, nodo in enumerate(os_):
                if o not in usados:
                    if nodo.kind in ('caso', 'res'):
                        self.notas.append(f'El autor borró el caso **{nodo.nombre}**: se dejó en el .md; decidir.')
                        piezas.append((nodo.src, i1 + o))
                    for c in COMENT.findall(nodo.src):
                        self.notas.append(f'Se borró un párrafo con nota interna; la nota se conserva: {c[:120]}')
                        piezas.append((c, None))
        # pegar con los espacios del original cuando los vecinos son consecutivos en el .md
        def pegar(g):
            return '\n' + ''.join(x + '\n' for x in g)
        tiene_nota = lambda g: any('<!--' in x for x in g)
        out = ''.join(x + '\n' for x in gaps[0])
        puestos = {0}
        for k, (texto, io) in enumerate(piezas):
            if k:
                pi = piezas[k - 1][1]
                if io is not None and (pi is not None and io == pi + 1 or tiene_nota(gaps[io])):
                    out += pegar(gaps[io])
                    puestos.add(io)
                else:
                    out += self.gap_por_omision(piezas[k - 1][0], texto)
            out += texto
        for gi, g in enumerate(gaps[:-1]):
            if gi not in puestos and tiene_nota(g):
                self.notas.append('Se perdió una nota suelta entre párrafos que cambiaron: '
                                  + ' '.join(x for x in g if '<!--' in x)[:200])
        out += ''.join('\n' + x for x in gaps[-1])
        return out

    @staticmethod
    def gap_por_omision(a, b):
        ta, tb = tipo_linea(a), tipo_linea(b)
        if ta == tb and ta in ('li', 'ol'):
            return '\n'
        if ta == tb == 'quote':
            return '\n>\n'
        return '\n\n'

    def correr(self, docx):
        seq, _ = parsear(self.original.split('\n'))
        self.numerar(seq)
        nuevos = unidades(self.lector, self.lector.bloques(self.lector.doc.element.body))
        self.revisar_fichas(nuevos)
        texto = self.alinear(seq, nuevos)
        base = docx.with_suffix('')
        stem = pathlib.Path(self.mapa['md']).stem
        destino = docx.parent / f'{stem}.desde_word.md'
        destino.write_text(texto, encoding='utf-8')
        diff = ''.join(difflib.unified_diff(self.original.splitlines(True), texto.splitlines(True),
                                            self.mapa['md'], destino.name))
        (docx.parent / f'{stem}.diff').write_text(diff, encoding='utf-8')
        self.informe(docx.parent / f'{stem}.cambios.md', diff)
        print(f'{destino}  ({diff.count(chr(10) + "+") } líneas nuevas o cambiadas; '
              f'{len(self.lector.comentarios)} comentarios; {len(self.notas)} notas a mano)')
        return base

    def informe(self, ruta, diff):
        L = [f'# Cambios de vuelta del Word: {pathlib.Path(self.mapa["md"]).name}', '',
             f'Exportado el {self.mapa["exportado"]}; leído el {datetime.date.today().isoformat()}.', '']
        L += ['## A pasar a mano', '']
        L += [f'- {n}' for n in self.notas] or ['- Nada.']
        L += ['', '## Comentarios del autor', '']
        if self.lector.comentarios:
            for k, (autor, texto) in self.lector.comentarios.items():
                ancla = self.lector.anclas.get(k, '').strip()
                L.append(f'- **{autor}** sobre «{ancla[:120]}»: {texto}')
        else:
            L.append('- No dejó comentarios.')
        L += ['', '## Control de cambios (lo que marcó Word)', '']
        if self.lector.revisiones:
            for autor, antes, despues in self.lector.revisiones:
                L.append(f'- **{autor}**: {trozo_cambiado(antes, despues)}')
        else:
            L.append('- El documento volvió sin cambios marcados (o ya aceptados): ver el diff.')
        L += ['', '## Diff contra el .md', '', '```diff', diff.rstrip(), '```', '']
        ruta.write_text('\n'.join(L), encoding='utf-8')


def trozo_cambiado(antes, despues, ctx=6):
    """Solo lo que cambió, con unas palabras de contexto: '… que ~~se ven igual~~ **.** …'."""
    a, d = antes.split(), despues.split()
    if not a:
        return f'párrafo nuevo: «{despues.strip()}»'
    if not d:
        return f'párrafo borrado: «{antes.strip()}»'
    out = []
    ops = difflib.SequenceMatcher(None, a, d, autojunk=False).get_opcodes()
    for n, (op, i1, i2, j1, j2) in enumerate(ops):
        if op == 'equal':
            w = a[i1:i2]
            if len(w) > 2 * ctx:
                w = (w[:ctx] if n else []) + ['…'] + (w[-ctx:] if n < len(ops) - 1 else [])
            out += w
            continue
        if i2 > i1:
            out.append('~~' + ' '.join(a[i1:i2]) + '~~')
        if j2 > j1:
            out.append('**' + ' '.join(d[j1:j2]) + '**')
    return '«' + ' '.join(out) + '»'


def tipo_linea(t):
    if re.match(r'^\s*[-*] ', t):
        return 'li'
    if re.match(r'^\s*\d+\. ', t):
        return 'ol'
    if t.startswith('>'):
        return 'quote'
    return 'otro'


def emparejar(os_, ns):
    """En un tramo cambiado, qué nodo del Word viene de qué nodo del .md (por tipo y parecido)."""
    pares, libres = {}, set(range(len(os_)))
    tipo = lambda n: {'img?': 'img', 'fig': 'img', 'ilus': 'img', 'caso?': 'caso', 'res': 'caso'}.get(n.kind, n.kind)
    def txt(n):
        if n.src is not None:
            return plano(n.src)
        if n.kind == 'tabla':
            return ' '.join(' '.join(f) for f in n.filas)
        if n.kind == 'caja':
            return plano(n.titulo) + ' ' + ' '.join(plano(getattr(h, 'texto', '') or '') for h in n.nodos())
        return plano(getattr(n, 'texto', None) or getattr(n, 'pie', '') or '')
    for j, n in enumerate(ns):
        if n.kind == 'img?':      # las figuras se emparejan por código
            o = next((i for i in libres if getattr(os_[i], 'cod', None) == n.cod), None)
        elif n.kind == 'caso?':
            o = next((i for i in libres if getattr(os_[i], 'nombre', None) == n.nombre), None)
        else:
            mejor, o = 0.45, None
            for i in libres:
                if tipo(os_[i]) != tipo(n) and not ({tipo(os_[i]), tipo(n)} <= {'p', 'li', 'ol', 'quote'}):
                    continue
                r = difflib.SequenceMatcher(None, txt(os_[i]), txt(n)).ratio()
                if r > mejor:
                    mejor, o = r, i
        if o is not None:
            pares[j] = o
            libres.discard(o)
    return pares


def importar(docx, mapa):
    docx = pathlib.Path(docx).resolve()
    mapa = pathlib.Path(mapa) if mapa else docx.parent / '.mapa.json'
    Importador(docx, mapa).correr(docx)


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='orden', required=True)
    e = sub.add_parser('exportar')
    e.add_argument('caps', nargs='+')
    e.add_argument('--autor', default='poza')
    i = sub.add_parser('importar')
    i.add_argument('docx')
    i.add_argument('--mapa')
    a = ap.parse_args()
    if a.orden == 'exportar':
        for c in a.caps:
            exportar(c, a.autor)
        empaquetar(a.autor)
    else:
        importar(a.docx, a.mapa)
