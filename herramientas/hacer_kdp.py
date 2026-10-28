#!/usr/bin/env python3
"""Arma la edición impresa para KDP (Amazon): interior y portada completa de cada tomo.

La versión digital (A4, dos tomos) sigue con herramientas/hacer_libro.py y no
cambia: este armador usa el mismo diagramador, pero en otra carpeta, con su
propia caché y con la obra en TRES tomos (él, 2026-10-27), porque KDP no
imprime más de 590 páginas en tapa blanda a color ni 550 en tapa dura:

    Tomo I    Bases y caja de herramientas              (B, H)
    Tomo II   Casos clínicos: Partes I a VI             (capítulos 1-19)
    Tomo III  Casos clínicos: Partes VII a XII          (capítulos 20-38)

    python3 herramientas/hacer_kdp.py --tomo I                 -> ediciones/kdp/tapa-blanda/tomo-I-interior.pdf
                                                         ediciones/kdp/tapa-blanda/tomo-I-portada.pdf (+ -guias.pdf)
    python3 herramientas/hacer_kdp.py --tomos                  -> los tres tomos
    python3 herramientas/hacer_kdp.py --tomo II --solo-portada -> solo la portada (lee las páginas del interior ya armado)
    ... --formato dura                                -> tapa dura 8,25 x 11" (interior; la portada, pendiente)
    ... --papel premium | estandar | blanco | crema   -> grosor del papel para el lomo (por defecto premium)

Interior: tamaño de corte + sangrado (0,125" en el borde exterior, arriba y
abajo), sin portada ni contraportada (en KDP van en la portada completa). Las
páginas de parte llegan al borde. La cabecera y el número de página se
acercan al texto para quedar a más de 0,375" del corte, como pide KDP.

Portada: una sola página, contraportada + lomo + portada, con 0,125" de
sangrado. El lomo sale de las páginas del interior y del papel. La zona del
código de barras (abajo a la derecha de la contraportada) queda libre. El
-guias.pdf es el mismo con las líneas de corte, pliegue, zona segura y
código de barras, solo para revisar: a KDP se sube el que no tiene guías.
"""
import os
import pathlib
import re
import sys

AQUI = pathlib.Path(__file__).resolve().parent
LIBRO = AQUI.parent
sys.path.insert(0, str(LIBRO / 'herramientas'))
import hacer_libro as H  # noqa: E402
import armado_incremental as AI  # noqa: E402

PULGADA = 25.4
SANGRADO = 0.125 * PULGADA                    # 3,175 mm

# Tamaño de corte (pulgadas) y páginas máximas en KDP (papel blanco a color premium)
FORMATOS_KDP = {
    'blanda': {'corte': (8.5, 11), 'carpeta': 'tapa-blanda', 'max_paginas': 590},
    'dura': {'corte': (8.25, 11), 'carpeta': 'tapa-dura', 'max_paginas': 550},
}
# Márgenes desde el corte (mm): los del A4. El interior (lomo) cumple el
# mínimo de KDP hasta 828 páginas (22,3 mm).
MARGENES = {'interior': 24, 'exterior': 14, 'arriba': 17, 'abajo': 18}
# Grosor por página para el lomo (pulgadas), según KDP
PAPELES = {'premium': 0.002347, 'estandar': 0.002252, 'blanco': 0.002252, 'crema': 0.0025}

TOMOS_KDP = {
    'I': 'Bases y caja de herramientas',
    'II': 'Casos clínicos: Partes I a VI',
    'III': 'Casos clínicos: Partes VII a XII',
}
ULTIMO_CAP_TOMO_II = 19                         # Parte VI termina en el 19; la VII parte en el 20
ACENTO_KDP = {'III': '#a7c7e7'}                 # tomo III: celeste (I rosa y II menta, como en el A4)
OBRA_KDP = ('<p>Obra en tres tomos. Tomo I: Bases (B1-B5) y Caja de herramientas (H1-H32). '
            'Tomo II: casos clínicos, Partes I a VI (capítulos 1-19). '
            'Tomo III: casos clínicos, Partes VII a XII (capítulos 20-38). '
            'Las remisiones a B y H llevan al tomo I; a los capítulos 1 a 19, al tomo II, '
            'y a los capítulos 20 a 38, al tomo III.</p>')

FMT = None          # el formato KDP elegido (lo fija preparar())
_css, _iniciales, _segmentos, _tomo_de = H.css, H.paginas_iniciales, AI.segmentos, H.tomo_de
_estilo_t2, _contraportada = H.estilo_t2, H.contraportada


def mm(x):
    return f'{x:.3f}mm'


def tomo_de(cap):
    if cap[:1] in ('B', 'H'):
        return 'I'
    return 'II' if int(re.sub(r'\D', '', cap) or 0) <= ULTIMO_CAP_TOMO_II else 'III'


def estilo_t2(cap):
    # la maquetación del tomo II se decide con los dos tomos del A4: el III también la lleva
    return _tomo_de(cap) == 'II' or _estilo_t2(cap)


def css():
    """El CSS del libro con las medidas de la página KDP en vez de las del A4."""
    ancho, alto = FMT['pagina']
    caja = alto - FMT['arriba'] - FMT['abajo']           # alto del texto
    s = _css()
    cambios = [
        ('height: 297mm', f'height: {mm(alto)}'),          # portada, contraportada, parte: a sangre
        ('width: 210mm', f'width: {mm(ancho)}'),           # trazos de la portada
        ('height: 255mm', f'height: {mm(caja - 7)}'),      # portada interior: el alto del texto - 7 mm, como en A4
        ('padding-top: 85mm', 'padding-top: 60mm'),        # créditos: más bajos y con tres tomos no caben a 85
    ]
    for viejo, nuevo in cambios:
        if viejo not in s:
            sys.exit(f'hacer_kdp: el CSS del libro ya no trae "{viejo}"; revisar css() de KDP')
        s = s.replace(viejo, nuevo)
    # cabecera y pie pegados al texto: a más de 0,375" del corte (KDP)
    return s + """
@page { @top-left { vertical-align: bottom; padding-bottom: 1.5mm; } @top-right { vertical-align: bottom; padding-bottom: 1.5mm; }
        @bottom-left { vertical-align: top; padding-top: 3mm; } @bottom-right { vertical-align: top; padding-top: 3mm; } }
"""


def paginas_iniciales(capitulos, tomo=None, piezas=False):
    p = _iniciales(capitulos, tomo, piezas)

    def tres_tomos(t):
        # créditos: la obra en tres tomos; el III es el volumen 3 (el A4 dice 2)
        t = re.sub(r'<p>Obra en dos tomos\..*?</p>', OBRA_KDP, t, flags=re.S)
        return t.replace(f'Vol. 2, {TOMOS_KDP["III"]}', f'Vol. 3, {TOMOS_KDP["III"]}')
    if piezas:
        return {k: tres_tomos(v) for k, v in p.items()}
    # la portada va en la portada completa, no en el interior
    return re.sub(r'<section class="portada".*?</section>', '', tres_tomos(p), count=1, flags=re.S)


def segmentos(tomo=None, caps=None):
    """Los del A4, con el índice de créditos de las imágenes al final del
    último tomo (el III), con los de toda la obra."""
    if tomo == 'III' and not caps:
        for a in sorted(H.CAPITULOS.glob('*.md')):
            md = a.read_text(encoding='utf-8')
            m = re.match(r'#\s+([A-Z]?\d+)\.', md)
            if m and tomo_de(m[1]) in ('I', 'II'):
                AI._solo_creditos(m[1], md)
    out, capitulos = _segmentos(tomo, caps)
    if tomo == 'II':
        out = [s for s in out if s[0] != 'creditos']
    if tomo == 'III' and not caps:
        creditos = AI.creditos_html()
        if creditos:
            out.append(('creditos', f'<div class="cuerpo">{creditos}</div>', False))
    return out, capitulos


def capa_de_numeros(numerada, destino):
    """La de armado_incremental, con el número pegado al texto (ver css())."""
    from weasyprint import HTML
    f = H.FORMATO
    numero = "font: 8pt 'Plus Jakarta Sans'; color: #8f7a83; vertical-align: top; padding-top: 3mm;"
    fuentes = '\n'.join(l for l in H.css().splitlines() if l.startswith('@font-face'))
    estilo = (fuentes + f"""
@page {{ size: {f['tamano']}; margin: {f['arriba']} {f['exterior']} {f['abajo']} {f['interior']};
        @bottom-right {{ content: counter(page); {numero} }} }}
@page :left {{ margin-left: {f['exterior']}; margin-right: {f['interior']};
        @bottom-right {{ content: none; }} @bottom-left {{ content: counter(page); {numero} }} }}
@page sin {{ @bottom-left {{ content: none; }} @bottom-right {{ content: none; }} }}
body {{ margin: 0; }} div {{ height: 1px; }} .sin {{ page: sin; }} .salto {{ break-before: page; }}""")
    divs = ''.join(f'<div class="{"" if n else "sin"}{" salto" if i else ""}"></div>' for i, n in enumerate(numerada))
    HTML(string=f'<!doctype html><html><head><meta charset="utf-8"><style>{estilo}</style></head>'
                f'<body>{divs}</body></html>').write_pdf(str(destino))


def preparar(formato):
    """Cambia el diagramador del A4 por el de KDP (solo en este proceso)."""
    global FMT
    base = FORMATOS_KDP[formato]
    cw, ch = (x * PULGADA for x in base['corte'])
    FMT = dict(base, corte_mm=(cw, ch), pagina=(cw + SANGRADO, ch + 2 * SANGRADO),
               arriba=MARGENES['arriba'] + SANGRADO, abajo=MARGENES['abajo'] + SANGRADO,
               exterior=MARGENES['exterior'] + SANGRADO, interior=MARGENES['interior'])
    H.FORMATO = {'tamano': f'{mm(FMT["pagina"][0])} {mm(FMT["pagina"][1])}', 'interior': mm(FMT['interior']),
                 'exterior': mm(FMT['exterior']), 'arriba': mm(FMT['arriba']), 'abajo': mm(FMT['abajo'])}
    H.TOMOS = dict(TOMOS_KDP)
    H.ACENTO = {**H.ACENTO, **ACENTO_KDP}
    H.tomo_de = tomo_de
    H.estilo_t2 = estilo_t2
    H.css = css
    H.paginas_iniciales = paginas_iniciales
    H.contraportada = lambda tomo=None: ''           # va en la portada completa
    AI.segmentos = segmentos
    AI.capa_de_numeros = capa_de_numeros
    AI.CACHE = H.SALIDA / 'cache-kdp' / formato       # nunca la caché del A4
    salida = LIBRO / 'ediciones' / 'kdp' / base['carpeta']
    salida.mkdir(parents=True, exist_ok=True)
    return salida


def vacia(pag):
    """Página sin nada (o solo con el pie: título y número), sin imágenes."""
    rec = pag.get('/Resources') or {}
    if '/XObject' in rec and rec['/XObject']:
        return False
    texto = (pag.extract_text() or '').replace(H.TITULO, '')
    return not re.sub(r'[\d\s]', '', texto)


def quitar_finales_vacias(ruta):
    """El armado deja la hoja de la contraportada (vacía en KDP) y su blanca."""
    from pypdf import PdfReader, PdfWriter
    lector = PdfReader(str(ruta))
    n = len(lector.pages)
    while n > 1 and vacia(lector.pages[n - 1]):
        n -= 1
    if n == len(lector.pages):
        return n
    escritor = PdfWriter(clone_from=lector)
    for i in range(len(lector.pages) - 1, n - 1, -1):
        escritor.remove_page(i)
    temporal = ruta.with_name(f'.{ruta.name}.{os.getpid()}')
    with open(temporal, 'wb') as f:
        escritor.write(f)
    os.replace(temporal, ruta)
    return n


def interior(tomo, salida):
    destino = salida / f'tomo-{tomo}-interior.pdf'
    AI.armar(tomo=tomo, destino=destino, sufijo=f'-kdp-{tomo}')
    paginas = quitar_finales_vacias(destino)
    print(f'{destino.name}: {paginas} páginas', flush=True)
    return destino, paginas


def portada(tomo, paginas, papel, salida):
    """Contraportada + lomo + portada en una página, con sangrado."""
    from weasyprint import HTML
    cw, ch = FMT['corte_mm']
    B = SANGRADO
    lomo = paginas * PAPELES[papel] * PULGADA
    ancho, alto = 2 * B + 2 * cw + lomo, ch + 2 * B
    x_atras, x_lomo, x_frente = B, B + cw, B + cw + lomo
    acento = H.ACENTO[tomo]
    frente = H.paginas_iniciales([], tomo, piezas=True)['portada']
    atras = _contraportada(tomo)
    texto_lomo = 'Tomo ' + tomo
    letra_lomo = max(8, min(15, lomo * 0.45 / 0.3528))       # pt: la letra ocupa ~45 % del ancho del lomo
    estilo = H.css() + f"""
@page tapa {{ size: {mm(ancho)} {mm(alto)}; margin: 0; background: #24101a;
             @top-left {{ content: none; }} @top-right {{ content: none; }}
             @bottom-left {{ content: none; }} @bottom-right {{ content: none; }} }}
.tapa {{ page: tapa; position: relative; width: {mm(ancho)}; height: {mm(alto)}; }}
.panel {{ position: absolute; top: {mm(B)}; width: {mm(cw)}; height: {mm(ch)}; }}
.panel > section {{ page: tapa; position: absolute; top: 0; left: 0; width: 100%; height: 100%; break-before: auto; margin: 0; }}
/* portada: la banda y los trazos llegan al sangrado; alturas a 11" (eran de A4) */
.frente .pt-banda-sup {{ top: {mm(-B)}; right: {mm(-B)}; height: {mm(14 + B)}; padding-top: {mm(B)}; box-sizing: border-box; }}
.frente .pt-centro {{ top: 52mm; }}
.frente .trazos {{ top: 136mm; height: 70mm; width: {mm(cw + B)}; right: auto; }}
/* contraportada: la licencia bajo los logos, lejos del código de barras */
.atras .cp-licencia {{ right: auto; left: 22mm; bottom: 7mm; }}
.atras .cp-titulo {{ hyphens: manual; }}
.lomo {{ position: absolute; top: {mm(B)}; left: {mm(x_lomo)}; width: {mm(lomo)}; height: {mm(ch)}; overflow: hidden; }}
.lomo-giro {{ position: absolute; width: {mm(ch)}; height: {mm(lomo)}; left: {mm((lomo - ch) / 2)}; top: {mm((ch - lomo) / 2)};
             transform: rotate(90deg); display: flex; align-items: center; justify-content: space-between;
             padding: 0 16mm; box-sizing: border-box; }}
.lm-titulo {{ font: 700 {letra_lomo:.1f}pt/1 Fraunces, serif; color: #F8F1F3; white-space: nowrap; }}
.lm-tomo {{ font: 700 {letra_lomo * 0.62:.1f}pt/1 'Plus Jakarta Sans'; letter-spacing: 2pt; text-transform: uppercase;
           color: {acento}; white-space: nowrap; }}
.guia {{ position: absolute; box-sizing: border-box; }}
"""
    lomo_html = (f'<div class="lomo"><div class="lomo-giro"><span class="lm-titulo">{H.TITULO}</span>'
                 f'<span class="lm-tomo">{texto_lomo}</span></div></div>') if paginas >= 80 else ''
    cuerpo = (f'<div class="panel atras" style="left: {mm(x_atras)}">{atras}</div>{lomo_html}'
              f'<div class="panel frente" style="left: {mm(x_frente)}">{frente}</div>')

    def guias():
        def caja(x, y, w, h, borde):
            return (f'<div class="guia" style="left: {mm(x)}; top: {mm(y)}; width: {mm(w)}; height: {mm(h)}; '
                    f'border: {borde}"></div>')
        seguro = 0.25 * PULGADA
        cb_w, cb_h, cb_m = 2 * PULGADA, 1.2 * PULGADA, 0.25 * PULGADA
        return ''.join([
            caja(B, B, ancho - 2 * B, ch, '0.6pt solid #00e5ff'),                         # corte
            caja(x_lomo, 0, lomo, alto, '0.6pt dashed #ffeb3b'),                          # pliegues del lomo
            caja(x_atras + seguro, B + seguro, cw - 2 * seguro, ch - 2 * seguro, '0.5pt dotted #7CFC00'),
            caja(x_frente + seguro, B + seguro, cw - 2 * seguro, ch - 2 * seguro, '0.5pt dotted #7CFC00'),
            caja(x_lomo - cb_m - cb_w, B + ch - cb_m - cb_h, cb_w, cb_h, '1pt solid #ff1744'),   # código de barras
        ])

    rutas = []
    for nombre, extra in ((f'tomo-{tomo}-portada.pdf', ''), (f'tomo-{tomo}-portada-guias.pdf', guias())):
        doc = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{H.TITULO}. Tomo {tomo}</title>'
               f'<style>{estilo}</style></head><body><div class="tapa">{cuerpo}{extra}</div></body></html>')
        ruta = salida / nombre
        HTML(string=doc, base_url=str(LIBRO) + '/').write_pdf(str(ruta))
        rutas.append(ruta)
    pulg = lambda x: x / PULGADA    # noqa: E731
    print(f'{rutas[0].name}: {pulg(ancho):.3f}" x {pulg(alto):.3f}" ({ancho:.1f} x {alto:.1f} mm), '
          f'lomo {pulg(lomo):.3f}" ({lomo:.1f} mm) para {paginas} páginas en papel {papel}', flush=True)
    return rutas


def main():
    args = sys.argv[1:]

    def opcion(nombre, defecto):
        if nombre in args:
            i = args.index(nombre)
            valor = args[i + 1]
            del args[i:i + 2]
            return valor
        return defecto
    formato = opcion('--formato', 'blanda')
    papel = opcion('--papel', 'premium')
    tomo = opcion('--tomo', None)
    solo_portada = '--solo-portada' in args
    tomos = list(TOMOS_KDP) if '--tomos' in args else [tomo.upper()] if tomo else []
    if formato not in FORMATOS_KDP or papel not in PAPELES or not tomos or any(t not in TOMOS_KDP for t in tomos):
        print(__doc__)
        sys.exit('Falta --tomo I|II|III o --tomos (y --formato blanda|dura, --papel premium|estandar|blanco|crema)')
    salida = preparar(formato)
    resumen = []
    for t in tomos:
        if solo_portada:
            ruta = salida / f'tomo-{t}-interior.pdf'
            if not ruta.exists():
                sys.exit(f'No está {ruta}: primero el interior (sin --solo-portada)')
            paginas = quitar_finales_vacias(ruta)
        else:
            _, paginas = interior(t, salida)
        if formato == 'dura':
            print('Portada de tapa dura: pendiente (KDP la pide con otras medidas)', flush=True)
        else:
            portada(t, paginas, papel, salida)
        resumen.append((t, paginas))
    for t, paginas in resumen:
        aviso = '' if paginas <= FMT['max_paginas'] else f'  <-- pasa el máximo de KDP ({FMT["max_paginas"]})'
        print(f'Tomo {t}: {paginas} páginas{aviso}')


if __name__ == '__main__':
    main()
