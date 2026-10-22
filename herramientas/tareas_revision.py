#!/usr/bin/env python3
"""Excel de tareas de revisión para los colegas (primera versión, 2026-10-22).

    python3 herramientas/tareas_revision.py   -> revision_colegas/tareas_revision_autores.xlsx

Una hoja por autor (menos el editor, que recibe y consolida) con:
  - sus capítulos como autor, con las páginas de cada PDF;
  - los capítulos cuyos casos revisa (Benjamín y Jocelyn);
  - los puntos pendientes de protocolo_vs_libro.xlsx que tocan sus capítulos;
  - una tabla vacía para sus observaciones.
Lee la autoría de hacer_libro.py y las páginas del índice de cada PDF, así que
hay que armar los dos tomos antes.
"""
import pathlib
import re
import sys

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from pypdf import PdfReader

AQUI = pathlib.Path(__file__).resolve().parent
LIBRO = AQUI.parent
sys.path.insert(0, str(AQUI))
import hacer_libro as H  # noqa: E402

PROTOCOLO = LIBRO / 'investigacion' / 'errores_tomo1_2026-10-22' / 'protocolo_vs_libro.xlsx'
SALIDA = LIBRO / 'revision_colegas' / 'tareas_revision_autores.xlsx'
FILAS_OBS = 60

FUENTE = 'Arial'
VINO = '6F5A63'
F_TIT = Font(name=FUENTE, size=14, bold=True, color=VINO)
F_SUB = Font(name=FUENTE, size=11, bold=True, color=VINO)
F_CAB = Font(name=FUENTE, size=10, bold=True, color='FFFFFF')
F_TXT = Font(name=FUENTE, size=10)
F_GRIS = Font(name=FUENTE, size=10, italic=True, color='6E6E73')
R_CAB = PatternFill('solid', fgColor=VINO)
R_LLENAR = PatternFill('solid', fgColor='FFF2CC')     # celdas que llena el colega
R_EJEMPLO = PatternFill('solid', fgColor='F2F2F2')
LINEA = Side(style='thin', color='D0D0D0')
BORDE = Border(left=LINEA, right=LINEA, top=LINEA, bottom=LINEA)
ARRIBA = Alignment(vertical='top', wrap_text=True)

ESTADOS = '"Pendiente,En curso,Listo"'
TIPOS = ('Error de contenido', 'Cifra, valor o referencia', 'Caso clínico', 'Figura o tabla',
         'Redacción', 'Errata', 'Falta algo', 'Sugerencia')
GRAVEDAD = '"Grave,Importante,Menor"'


# --- datos -----------------------------------------------------------------

def paginas(tomo):
    """{'H3' o '17': (título, primera, última)} del índice del PDF."""
    r = PdfReader(LIBRO / f'libro-tomo-{tomo}.pdf')
    planos = []

    def recorrer(o):
        for x in o:
            if isinstance(x, list):
                recorrer(x)
            else:
                planos.append((r.get_destination_page_number(x) + 1, x.title))
    recorrer(r.outline)
    # solo el primer nivel de cada capítulo: entradas "H3. ...", "17. ...", partes y apéndices cortan
    cortes = sorted({p for p, t in planos if re.match(r'([HB]?\d+)\. |Parte |Créditos|Caja |Bases', t)})
    out = {}
    for p, t in planos:
        m = re.match(r'([HB]?\d+)\. (.+)', t)
        if m and m[1] not in out:
            fin = next((c - 1 for c in cortes if c > p), len(r.pages))
            out[m[1]] = (m[2], p, fin)
    autores_pag = next(p for p, t in planos if t == 'Autoras y autores') if any(
        t == 'Autoras y autores' for _, t in planos) else None
    return out, autores_pag


def caps_de(texto):
    """'H7, caps. 2 y 3' -> ['H7', '2', '3']; '24, H20' -> ['H20', '24']."""
    s = str(texto)
    hs = re.findall(r'\b[HB]\d+\b', s)
    resto = re.sub(r'\b[HB]\d+\b', '', s)
    return hs + re.findall(r'\b\d{1,2}\b', resto)


def pendientes_protocolo():
    wb = openpyxl.load_workbook(PROTOCOLO, read_only=True)
    out = []
    for hoja in ('Decide tú', 'Actualizaciones', 'Otros avisos'):
        filas = list(wb[hoja].iter_rows(values_only=True))
        i = next(k for k, f in enumerate(filas) if f and f[0] in ('N.º', 'N.º original'))
        est = filas[i].index('Estado hoy')
        for f in filas[i + 1:]:
            if f and f[0] is not None and str(f[est]).startswith('Pendiente'):
                out.append(dict(hoja=hoja, n=str(f[0]), caps=caps_de(f[1]), cap_txt=str(f[1]), tema=str(f[2])))
    return out


def tomo_de(cap):
    return 'I' if cap[0] in 'HB' else 'II'


def orden_cap(cap):
    return (cap[0] if cap[0] in 'HB' else 'Z', int(re.sub(r'\D', '', cap)))


def casos_por_capitulo():
    out = {}
    for f in (LIBRO / 'capitulos').glob('[0-9][0-9]-*.md'):
        out[str(int(f.name[:2]))] = f.read_text(encoding='utf-8').count('{{caso ')
    return out


# --- hojas -------------------------------------------------------------------

def cabecera(ws, fila, nombres, anchos=None):
    for j, n in enumerate(nombres, 1):
        c = ws.cell(fila, j, n)
        c.font, c.fill, c.alignment, c.border = F_CAB, R_CAB, Alignment(vertical='center', wrap_text=True), BORDE
    ws.row_dimensions[fila].height = 30


def celda(ws, f, j, v, llenar=False, fuente=F_TXT):
    c = ws.cell(f, j, v)
    c.font, c.alignment, c.border = fuente, ARRIBA, BORDE
    if llenar:
        c.fill = R_LLENAR
    return c


def alto(vals, anchos):
    """Alto de fila (pt) para que el texto envuelto se vea entero."""
    lineas = max(-(-len(str(v or '')) // max(1, int(w * 1.15))) for v, w in zip(vals, anchos))
    return max(15, 13.5 * lineas + 3)


def hoja_leeme(wb, n_autores):
    ws = wb.active
    ws.title = 'Léeme'
    ws.column_dimensions['A'].width = 24
    ws.column_dimensions['B'].width = 100
    ws['A1'] = 'Revisión de la primera versión del libro'
    ws['A1'].font = F_TIT
    filas = [
        ('Qué es', 'Evaluación y rehabilitación en otorrinolaringología, primera versión completa en dos tomos. '
                   'Te pedimos leer lo tuyo, evaluarlo y anotar tus observaciones en este Excel.'),
        ('Qué recibes', 'libro-tomo-I.pdf (bases y caja de herramientas: capítulos B y H). '
                        'libro-tomo-II.pdf (capítulos clínicos 1 a 38). '
                        'Este Excel (tus tareas y tus observaciones). '
                        'protocolo_vs_libro.xlsx (dónde el protocolo ORL 2019, las clases y el libro no dicen lo mismo).'),
        ('Tu hoja', 'Busca la pestaña con tu apellido. Arriba están tus tareas, con el tomo, el capítulo y las páginas del PDF; '
                    'abajo, la tabla para tus observaciones.'),
        ('Cómo marcar', 'En "Estado" elige Pendiente, En curso o Listo. En "Comentario" anota lo general de esa tarea '
                        '(por ejemplo, "sin observaciones" o "ver observaciones 3 a 7").'),
        ('Observaciones', 'Una fila por observación, con el tomo, el capítulo y la página del PDF, para que se encuentre rápido. '
                          'Si propones un cambio, escribe el texto como quieres que quede. Si corriges una cifra o un valor de '
                          'referencia, pon la fuente (autor, año y DOI si lo tienes).'),
        ('Celdas amarillas', 'Son las únicas que hay que llenar. El resto se calcula solo o viene del libro.'),
        ('Los casos', 'Los pacientes son ficticios y sus exámenes salen de LabSim. Si un dato no calza con la historia, con el '
                      'texto o con otro examen, anótalo como "Caso clínico": así se corrige también el simulador.'),
        ('protocolo_vs_libro', 'En tus tareas aparecen los puntos pendientes que tocan tus capítulos (hoja y N.º). '
                               'Léelos y deja tu opinión en tu hoja de este Excel, no en el otro archivo.'),
        ('No edites', 'No edites los PDF ni el otro Excel: todo va en tu hoja de este archivo.'),
        ('Fecha de entrega', None),
        ('Devolver a', 'Nicolás Baier-Quezada, editor.'),
    ]
    f = 3
    for k, v in filas:
        ws.cell(f, 1, k).font = Font(name=FUENTE, size=10, bold=True)
        c = ws.cell(f, 2, v)
        c.font, c.alignment = F_TXT, Alignment(wrap_text=True, vertical='top')
        ws.row_dimensions[f].height = alto([v], [100])
        ws.cell(f, 1).alignment = Alignment(vertical='top')
        if v is None:
            c.fill = R_LLENAR
            ws.cell(f, 3, '← la pone el editor antes de enviar').font = F_GRIS
        f += 1
    f += 1
    ws.cell(f, 1, 'Ejemplo de una observación (así se llena la tabla de tu hoja)').font = F_SUB
    f += 1
    cols = ['N.º', 'Tomo', 'Capítulo', 'Página', 'Dónde', 'Tipo', 'Gravedad', 'Observación', 'Propuesta de cambio', 'Fuente']
    for j, n in enumerate(cols, 1):
        c = ws.cell(f, j, n)
        c.font, c.fill, c.border = F_CAB, R_CAB, BORDE
    ej = [1, 'II', '17', 377, 'Caso 17.3, informe de PEAT', 'Cifra, valor o referencia', 'Importante',
          'La corrección a dB eHL del burst de 500 Hz no calza con la tabla de la página 365.',
          'Usar 20 dB, como en la tabla.', 'BSA (2019), OD104-84']
    for j, v in enumerate(ej, 1):
        c = ws.cell(f + 1, j, v)
        c.font, c.fill, c.border, c.alignment = F_GRIS, R_EJEMPLO, BORDE, ARRIBA
    ws.cell(f + 2, 1, 'La fila de ejemplo es inventada: no es una observación real.').font = F_GRIS
    ws.freeze_panes = 'A3'


def hoja_autor(wb, k, tareas):
    a = H.AUTORES[k]
    ws = wb.create_sheet(a['apellidos'].split('-')[0])
    anchos = [6, 7, 9, 40, 11, 56, 26, 13, 40]
    for j, w in enumerate(anchos, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws['A1'] = H.nombre_completo(k)
    ws['A1'].font = F_TIT
    ws['A2'] = '. '.join(x for x in (a.get('rol'), a.get('areas')) if x) or 'Autor'
    ws['A2'].font = F_GRIS

    ws['A4'] = 'Tus tareas'
    ws['A4'].font = F_SUB
    cabecera(ws, 5, ['N.º', 'Tomo', 'Capítulo', 'Título', 'Páginas del PDF', 'Qué revisar', 'Con quién lo compartes',
                     'Estado', 'Comentario'])
    dv_est = DataValidation(type='list', formula1=ESTADOS, allow_blank=True)
    ws.add_data_validation(dv_est)
    f = 6
    for i, t in enumerate(tareas, 1):
        vals = [i, t['tomo'], t['cap'], t['titulo'], t['pags'], t['que'], t['con']]
        for j, v in enumerate(vals, 1):
            celda(ws, f, j, v)
        ws.row_dimensions[f].height = alto(vals, anchos)
        celda(ws, f, 8, 'Pendiente', llenar=True)
        celda(ws, f, 9, None, llenar=True)
        dv_est.add(ws.cell(f, 8))
        f += 1
    fin_tareas = f - 1

    f += 2
    ws.cell(f, 1, 'Tus observaciones (una por fila; el ejemplo está en la hoja Léeme)').font = F_SUB
    f += 1
    cabecera(ws, f, ['N.º', 'Tomo', 'Capítulo', 'Página', 'Dónde (sección, caso, figura, tabla)', 'Tipo', 'Gravedad',
                     'Observación', 'Propuesta de cambio y fuente'])
    # en esta tabla las columnas cambian de sentido: más ancho para lo que se escribe
    ini_obs = f + 1
    dv_tomo = DataValidation(type='list', formula1='"I,II"', allow_blank=True)
    dv_tipo = DataValidation(type='list', formula1='"' + ','.join(TIPOS) + '"', allow_blank=True)
    dv_grav = DataValidation(type='list', formula1=GRAVEDAD, allow_blank=True)
    for dv in (dv_tomo, dv_tipo, dv_grav):
        ws.add_data_validation(dv)
    for i in range(1, FILAS_OBS + 1):
        r = ini_obs + i - 1
        celda(ws, r, 1, i)
        for j in range(2, 10):
            celda(ws, r, j, None, llenar=True)
        dv_tomo.add(ws.cell(r, 2))
        dv_tipo.add(ws.cell(r, 6))
        dv_grav.add(ws.cell(r, 7))
    fin_obs = ini_obs + FILAS_OBS - 1
    ws.freeze_panes = 'A6'
    return ws.title, (6, fin_tareas), (ini_obs, fin_obs)


def hoja_resumen(wb, filas):
    ws = wb.create_sheet('Resumen', 1)
    ws['A1'] = 'Resumen por autor'
    ws['A1'].font = F_TIT
    ws['A2'] = 'Se calcula solo con lo que cada uno marca en su hoja.'
    ws['A2'].font = F_GRIS
    cabecera(ws, 4, ['Autor', 'Hoja', 'Capítulos como autor', 'Capítulos de casos que revisa', 'Puntos de protocolo',
                     'Tareas', 'Listas', 'Avance', 'Observaciones anotadas'])
    for j, w in enumerate([34, 12, 12, 14, 12, 9, 9, 9, 14], 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    f = 5
    for nombre, hoja, n_aut, n_rev, n_prot, (t0, t1), (o0, o1) in filas:
        ref = f"'{hoja}'!"
        vals = [nombre, hoja, n_aut, n_rev, n_prot,
                f'=COUNTA({ref}A{t0}:A{t1})',
                f'=COUNTIF({ref}H{t0}:H{t1},"Listo")',
                f'=IF(F{f}=0,0,G{f}/F{f})',
                f'=COUNTA({ref}H{o0}:H{o1})']
        for j, v in enumerate(vals, 1):
            c = celda(ws, f, j, v)
            if j == 8:
                c.number_format = '0%'
        f += 1
    celda(ws, f, 1, 'Total', fuente=Font(name=FUENTE, size=10, bold=True))
    for j in range(3, 10):
        col = get_column_letter(j)
        c = celda(ws, f, j, f'=SUM({col}5:{col}{f - 1})' if j != 8 else f'=IF(F{f}=0,0,G{f}/F{f})',
                  fuente=Font(name=FUENTE, size=10, bold=True))
        if j == 8:
            c.number_format = '0%'
    ws.cell(f + 2, 1, 'El editor no tiene hoja: recibe y consolida. Los capítulos que firma con otros aparecen en la hoja '
                      'del coautor.').font = F_GRIS
    ws.freeze_panes = 'A5'


# --- armado ----------------------------------------------------------------

def main():
    pags_I, autores_I = paginas('I')
    pags_II, autores_II = paginas('II')
    pags = {**pags_I, **pags_II}
    casos = casos_por_capitulo()
    prot = pendientes_protocolo()
    wb = openpyxl.Workbook()
    hoja_leeme(wb, 0)
    resumen = []
    for k in H.orden_autores():
        if k == H.EDITOR:
            continue
        a = H.AUTORES[k]
        tareas = []
        datos = 'Revisa tu ficha: nombre, títulos, afiliación, áreas y ORCID.'
        if a.get('falta'):
            datos += f' Falta: {a["falta"]}; envíalo al editor.'
        tareas.append(dict(tomo='I y II', cap='—', titulo='Autoras y autores',
                           pags=f'I: {autores_I}; II: {autores_II}', que=datos, con='—'))
        mios = sorted((c for c, aut in H.AUTORIA.items() if k in aut), key=orden_cap)
        for c in mios:
            titulo, p0, p1 = pags.get(c, ('', None, None))
            otros = ', '.join(H.AUTORES[x]['nombre'] for x in H.AUTORIA[c] if x != k) or '—'
            if c[0] in 'HB':
                que = ('Como autor: contenido técnico y procedimiento, valores de referencia y sus citas, figuras y pies, '
                       'y los casos de práctica si el capítulo los tiene.')
            else:
                rev = H.AUTORES[H.revisor_casos(c)]['nombre']
                que = (f'Como autor: el razonamiento clínico, los cuadros, las cifras y sus citas, las figuras. '
                       f'Sus {casos.get(c, 0)} casos los revisa {rev}, pero puedes comentarlos.')
            tareas.append(dict(tomo=tomo_de(c), cap=c, titulo=titulo, pags=f'{p0}–{p1}' if p0 else '', que=que, con=otros))
        revisa = sorted((str(c) for c in H.REVISORES_CASOS.get(k, [])), key=orden_cap)
        for c in revisa:
            titulo, p0, p1 = pags.get(c, ('', None, None))
            autores_c = ', '.join(H.AUTORES[x]['nombre'] for x in H.AUTORIA.get(c, []))
            que = (f'Revisor de los {casos.get(c, 0)} casos: que la historia calce con los exámenes y las figuras, '
                   'los globos, las preguntas de cada paso, la guía docente, el informe y la conclusión.')
            tareas.append(dict(tomo='II', cap=c, titulo=titulo, pags=f'{p0}–{p1}', que=que,
                               con=f'Autores: {autores_c}' if autores_c else '—'))
        puntos = [p for p in prot if any(k in H.AUTORIA.get(c, []) for c in p['caps'])]
        que_hoja = {'Decide tú': 'Opina: ¿el libro vuelve al protocolo, se deja como está o se conversa?',
                    'Actualizaciones': 'Verificación pendiente: si sabes la respuesta o la fuente, anótala.',
                    'Otros avisos': 'Aviso sin cerrar: di qué prefieres.'}
        for p in sorted(puntos, key=lambda p: ('Decide tú', 'Actualizaciones', 'Otros avisos').index(p['hoja'])):
            tareas.append(dict(tomo='—', cap=p['cap_txt'], titulo=f'protocolo_vs_libro, hoja "{p["hoja"]}", N.º {p["n"]}: {p["tema"]}',
                               pags='—', que=que_hoja[p['hoja']], con='Lo decide el equipo'))
        hoja, rt, ro = hoja_autor(wb, k, tareas)
        resumen.append((H.nombre_completo(k), hoja, len(mios), len(revisa), len(puntos), rt, ro))
    hoja_resumen(wb, resumen)
    for ws in wb.worksheets:       # impresa: horizontal y al ancho de la hoja
        ws.page_setup.orientation = 'landscape'
        ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
        ws.sheet_properties.pageSetUpPr.fitToPage = True
    SALIDA.parent.mkdir(exist_ok=True)
    wb.save(SALIDA)
    print(SALIDA)
    for r in resumen:
        print(r[:5])


if __name__ == '__main__':
    main()
