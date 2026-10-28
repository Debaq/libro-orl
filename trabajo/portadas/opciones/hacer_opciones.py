"""10 opciones de portada para los dos tomos: líneas simples sobre la portada del libro.

Cada opción es un par (tomo I herramientas / tomo II casos) con el mismo lenguaje.
Salida, en esta carpeta: portadas-opciones.pdf (20 portadas); los mosaicos
portadas-1.png y portadas-2.png se sacan de ese PDF con pdftoppm.

    python3 portadas/opciones/hacer_opciones.py
"""
import math
import re
import sys

sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parents[3] / 'herramientas'))
import hacer_libro as H  # noqa: E402

AQUI = str(__import__('pathlib').Path(__file__).resolve().parent)
W, HH = 600, 220                      # caja del dibujo (la franja de la portada actual)
ROSA, MENTA = '#E7A7BA', '#9fd6c9'    # acento del tomo I y del tomo II


# ---------- utilidades de trazo ----------
def linea(pts, color, w=1.6, op=0.9, dash=None):
    d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    ds = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-opacity="{op}"'
            f' stroke-linecap="round" stroke-linejoin="round"{ds}/>')


def grilla(x0, y0, w, h, nx, ny, color, op=0.16):
    s = []
    for i in range(nx + 1):
        x = x0 + w * i / nx
        s.append(linea([(x, y0), (x, y0 + h)], color, 0.6, op))
    for j in range(ny + 1):
        y = y0 + h * j / ny
        s.append(linea([(x0, y), (x0 + w, y)], color, 0.6, op))
    return ''.join(s)


def circulo(x, y, r, color, w=1.5, op=0.95):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="{color}" stroke-width="{w}" stroke-opacity="{op}"/>'


def cruz(x, y, r, color, w=1.5, op=0.95):
    return (linea([(x - r, y - r), (x + r, y + r)], color, w, op)
            + linea([(x - r, y + r), (x + r, y - r)], color, w, op))


def svg(cuerpo, ajuste='xMidYMid meet'):
    """ajuste='none' estira el dibujo a toda la franja, como la portada actual
    (sirve para trazos sin círculos ni cruces, que se deformarían)."""
    return (f'<svg class="trazos" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {HH}" '
            f'preserveAspectRatio="{ajuste}">{cuerpo}</svg>')


# ---------- los exámenes, como curvas ----------
def audiograma(x0, y0, w, h, od, oi, c, simbolos=True, gris=True, osea=None):
    """od/oi: dB HL en 125..8k (7 frecuencias). y crece hacia abajo (0 dB arriba)."""
    s = grilla(x0, y0, w, h, 6, 6, c) if gris else ''
    X = [x0 + w * i / 6 for i in range(7)]
    Y = lambda db: y0 + h * (db + 10) / 130
    for vals, sim, op in ((od, 'o', 0.95), (oi, 'x', 0.6)):
        if vals is None:
            continue
        pts = [(X[i], Y(v)) for i, v in enumerate(vals)]
        s += linea(pts, c, 1.4, op)
        if simbolos:
            for x, y in pts:
                s += circulo(x, y, 4.2, c, 1.4, op) if sim == 'o' else cruz(x, y, 3.6, c, 1.4, op)
    if osea:
        for i, v in enumerate(osea):
            if v is None:
                continue
            x, y = X[i] - 6, Y(v)
            s += linea([(x + 4, y - 5), (x - 2, y), (x + 4, y + 5)], c, 1.4, 0.95)   # "<" ósea OD
    return s


def timpano(x0, y0, w, h, picos, c, ops=None):
    """picos: [(admitancia relativa 0..1, presión -1..1 del pico, ancho)]; base abajo."""
    s = linea([(x0, y0 + h), (x0 + w, y0 + h)], c, 0.7, 0.25)
    s += linea([(x0 + w * 0.67, y0), (x0 + w * 0.67, y0 + h)], c, 0.7, 0.18)    # 0 daPa
    for k, (a, p0, ancho) in enumerate(picos):
        pts = []
        for i in range(161):
            p = -1 + 1.5 * i / 160             # -400 .. +200 daPa
            y = a * math.exp(-((p - p0) / ancho) ** 2) + 0.04
            pts.append((x0 + w * i / 160, y0 + h - y * h))
        s += linea(pts, c, 1.6, (ops or [0.95] * 9)[k])
    return s


def nistagmo(x0, y0, w, h, c, latidos=14, envolvente=None, op=0.9, deriva=1):
    """Diente de sierra: fase lenta en rampa y fase rápida que vuelve.
    envolvente(t) en 0..1 escala la amplitud (respuesta calórica)."""
    pts, t = [(x0, y0 + h / 2)], 0
    paso = w / latidos
    for k in range(latidos):
        a = envolvente(k / latidos) if envolvente else 1
        xa = x0 + k * paso
        pts += [(xa + paso * 0.82, y0 + h / 2 - deriva * a * h * 0.42), (xa + paso, y0 + h / 2)]
    return linea(pts, c, 1.5, op)


def peat(x0, y0, w, h, c, lat=5.6, amp=1.0, op=0.9):
    pts = []
    for i in range(241):
        ms = i / 20
        y = sum(a * math.exp(-((ms - l) / 0.28) ** 2) for a, l in ((0.5, 1.6), (0.7, lat - 1.8), (1.0, lat)))
        y -= 0.5 * math.exp(-((ms - lat - 1.1) / 0.5) ** 2)
        pts.append((x0 + w * ms / 12, y0 + h * 0.6 - y * amp * h * 0.5))
    return linea(pts, c, 1.5, op)


def oea(x0, y0, w, h, c, op=0.9, amp=1.0):
    pts = []
    for i in range(301):
        t = i / 300
        f = 6 + 34 * (1 - t)                     # chirp: agudos primero
        y = amp * math.exp(-((t - 0.25) / 0.2) ** 2) * math.sin(2 * math.pi * f * t)
        pts.append((x0 + w * t, y0 + h / 2 - y * h * 0.45))
    return linea(pts, c, 1.3, op)


def reflejo(x0, y0, w, h, c, op=0.9, forma='normal'):
    pts = []
    for i in range(201):
        t = i / 200
        on = 1 / (1 + math.exp(-(t - 0.3) * 120)) - 1 / (1 + math.exp(-(t - 0.7) * 120))
        if forma == 'normal':
            y = on
        else:                                    # ON-OFF
            y = math.exp(-((t - 0.31) / 0.03) ** 2) + math.exp(-((t - 0.71) / 0.03) ** 2)
        pts.append((x0 + w * t, y0 + h * 0.2 + y * h * 0.6))
    return linea(pts, c, 1.5, op)


def vhit(x0, y0, w, h, c, op=0.9, sacada=False):
    """Velocidad de cabeza (campana) y del ojo; con sacada encubierta si falla."""
    cab, ojo = [], []
    for i in range(201):
        t = i / 200
        v = math.exp(-((t - 0.35) / 0.1) ** 2)
        e = (0.45 if sacada else 0.97) * math.exp(-((t - 0.36) / 0.1) ** 2)
        if sacada:
            e += 0.8 * math.exp(-((t - 0.55) / 0.03) ** 2)
        cab.append((x0 + w * t, y0 + h - v * h * 0.85))
        ojo.append((x0 + w * t, y0 + h - e * h * 0.85))
    return linea(cab, c, 1.2, op * 0.45, '3 3') + linea(ojo, c, 1.6, op)


def rinomanometria(x0, y0, w, h, c, op=0.9, obstruida=False):
    """Curvas S de flujo contra presión, dos fosas."""
    s = linea([(x0, y0 + h / 2), (x0 + w, y0 + h / 2)], c, 0.7, 0.25)
    s += linea([(x0 + w / 2, y0), (x0 + w / 2, y0 + h)], c, 0.7, 0.25)
    for k, g in enumerate((1.0, 0.35 if obstruida else 0.8)):
        pts = []
        for i in range(121):
            p = -1 + 2 * i / 120
            f = g * math.copysign(abs(p) ** 0.55, p)
            pts.append((x0 + w / 2 + p * w / 2, y0 + h / 2 - f * h / 2 * 0.9))
        s += linea(pts, c, 1.6, op if k == 0 else op * 0.6)
    return s


# ---------- las 10 opciones: (nombre, idea, dibujo tomo I, dibujo tomo II) ----------
NORMAL_OD = [10, 10, 5, 10, 10, 15, 15]
NORMAL_OI = [15, 10, 10, 10, 15, 15, 20]
RUIDO = [10, 10, 15, 20, 35, 55, 30]
PRESBI = [15, 20, 20, 30, 45, 60, 70]


def calorica(t):
    return math.sin(math.pi * min(1, t * 1.1)) ** 1.5


def o1(c, t2):   # audiograma
    if not t2:
        return audiograma(150, 25, 300, 170, NORMAL_OD, NORMAL_OI, c)
    return audiograma(150, 25, 300, 170, RUIDO, PRESBI, c)


def o2(c, t2):   # timpanogramas superpuestos
    if not t2:
        return timpano(140, 30, 320, 160, [(0.62, 0.0, 0.22), (0.3, 0.0, 0.2), (0.95, 0.0, 0.18)], c, [0.95, 0.6, 0.45])
    return timpano(140, 30, 320, 160, [(0.0, 0, 1), (0.55, -0.65, 0.22)], c, [0.95, 0.65])


def o3(c, t2):   # calórica: nistagmo con su culminación
    if not t2:
        return nistagmo(40, 50, 520, 120, c, 40, calorica)
    return (nistagmo(40, 20, 520, 80, c, 40, calorica)
            + nistagmo(40, 120, 520, 80, c, 40, lambda t: 0.3 * calorica(t), op=0.6))


def o4(c, t2):   # tríptico: audiometría | impedanciometría | calórica
    if not t2:
        return (audiograma(40, 50, 150, 120, NORMAL_OD, None, c)
                + timpano(225, 50, 150, 120, [(0.7, 0, 0.22)], c)
                + nistagmo(410, 50, 150, 120, c, 12, calorica))
    return (audiograma(40, 50, 150, 120, RUIDO, None, c)
            + timpano(225, 50, 150, 120, [(0.0, 0, 1)], c)
            + nistagmo(410, 50, 150, 120, c, 12, lambda t: 0.35 * calorica(t)))


def o5(c, t2):   # una sola línea que cambia de examen
    pts = []
    for i in range(601):
        x = i
        if x < 150:      # audiograma (escalera suave que baja)
            y = 70 + 40 * (x / 150) ** 2
        elif x < 300:    # timpanograma
            u = (x - 225) / 30
            y = 110 - 70 * math.exp(-u * u)
        elif x < 450:    # nistagmo
            u = ((x - 300) % 18) / 18
            y = 110 - 40 * (u / 0.8 if u < 0.8 else (1 - u) / 0.2)
        else:            # PEAT
            ms = (x - 450) / 150 * 10
            y = 110 - 45 * sum(a * math.exp(-((ms - l) / 0.3) ** 2) for a, l in ((0.5, 1.6), (0.7, 3.8), (1, 5.6)))
        pts.append((x, y))
    s = linea(pts, c, 1.8, 0.95)
    if t2:                                   # el eco: la misma línea, más tenue, debajo
        s += linea([(x, y + 50) for x, y in pts], c, 1.2, 0.35)
    return s


def o6(c, t2):   # trazos apilados, uno por examen (la portada actual, con exámenes distintos)
    filas = [peat, oea, None, reflejo, nistagmo, vhit]
    s, y = '', 8
    for k, f in enumerate(filas):
        op = 0.9 - k * 0.08
        if f is peat:
            s += peat(30, y, 540, 34, c, lat=6.4 if t2 else 5.6, op=op)
        elif f is oea:
            s += oea(30, y, 540, 34, c, op=op, amp=0.3 if t2 else 1)
        elif f is None:
            s += timpano(30, y, 540, 30, [(0.0, 0, 1)] if t2 else [(0.8, 0.0, 0.08)], c, [op])
        elif f is reflejo:
            s += reflejo(30, y, 540, 30, c, op=op, forma='onoff' if t2 else 'normal')
        elif f is nistagmo:
            s += nistagmo(30, y, 540, 30, c, 36, op=op)
        else:
            s += vhit(30, y, 540, 30, c, op=op, sacada=t2)
        y += 35
    return s


def o7(c, t2):   # mosaico 2 x 2
    if not t2:
        return (audiograma(110, 12, 170, 90, NORMAL_OD, NORMAL_OI, c)
                + timpano(320, 12, 170, 90, [(0.7, 0, 0.22)], c)
                + nistagmo(110, 122, 170, 90, c, 12, calorica)
                + peat(320, 122, 170, 90, c))
    return (vhit(110, 12, 170, 90, c, sacada=True)
            + rinomanometria(320, 12, 170, 90, c, obstruida=True)
            + audiograma(110, 122, 170, 90, PRESBI, None, c)
            + oea(320, 122, 170, 90, c, amp=0.35))


def o8(c, t2):   # un audiograma grande, sin grilla, solo la curva y sus símbolos
    if not t2:                               # sensorioneural: la ósea va pegada a la aérea
        return audiograma(60, 20, 480, 180, PRESBI, None, c, gris=False,
                          osea=[None, 15, 15, 25, 40, 55, None])
    # conductiva: aérea baja, ósea normal (gap)
    return audiograma(60, 20, 480, 180, [40, 40, 35, 30, 30, 35, 40], None, c, gris=False,
                      osea=[None, 10, 10, 15, 10, 15, None])


def o9(c, t2):   # mitad audición, mitad equilibrio (II: equilibrio y nariz)
    if not t2:
        return audiograma(40, 30, 240, 160, NORMAL_OD, NORMAL_OI, c) + nistagmo(320, 40, 240, 140, c, 18, calorica)
    return vhit(40, 40, 240, 140, c, sacada=True) + rinomanometria(320, 30, 240, 160, c, obstruida=True)


def o10(c, t2):  # cuatro glifos chicos en fila, mucho aire
    xs = [70, 205, 340, 475]
    if not t2:
        return (audiograma(xs[0], 70, 70, 70, NORMAL_OD, None, c, gris=False)
                + timpano(xs[1], 70, 70, 70, [(0.8, 0, 0.25)], c)
                + nistagmo(xs[2], 70, 70, 70, c, 5)
                + peat(xs[3], 70, 70, 70, c))
    return (vhit(xs[0], 70, 70, 70, c, sacada=True)
            + rinomanometria(xs[1], 70, 70, 70, c)
            + oea(xs[2], 70, 70, 70, c)
            + reflejo(xs[3], 70, 70, 70, c, forma='onoff'))


OPCIONES = [
    ('Audiograma', 'I: aérea normal OD (○) y OI (×). II: muesca de ruido y presbiacusia.', o1),
    ('Timpanogramas', 'I: curvas A, As y Ad superpuestas. II: B plana y C con presión negativa.', o2),
    ('Prueba calórica', 'I: nistagmo con su culminación. II: dos oídos, uno con paresia.', o3),
    ('Tríptico', 'Audiometría | impedanciometría | calórica. II: los mismos con hallazgos.', o4),
    ('Una sola línea', 'Un trazo continuo: audiograma, timpanograma, nistagmo y PEAT. II: con su eco.', o5),
    ('Trazos apilados', 'La portada actual, con un examen por trazo: PEAT, OEA, timpanograma, reflejo, nistagmo, vHIT.', o6),
    ('Mosaico 2 × 2', 'I: audiograma, timpanograma, calórica y PEAT. II: vHIT, rinomanometría, presbiacusia y OEA.', o7),
    ('Audiograma grande', 'Una sola curva, sin grilla. I: caída en agudos con la ósea pegada. II: pérdida conductiva, la ósea (<) separada.', o8),
    ('Audición | equilibrio', 'I: audiograma y calórica. II: vHIT con sacada y rinomanometría.', o9),
    ('Cuatro glifos', 'Cuatro dibujos chicos con mucho aire. II: vHIT, rinomanometría, OEA y reflejo.', o10),
]


def portada(n, tomo, dibujo, ajuste='xMidYMid meet'):
    html = H.paginas_iniciales([], tomo)
    sec = re.search(r'<section class="portada">.*?</section>', html, re.S)[0]
    sec = re.sub(r'<svg class="trazos".*?</svg>', lambda _: svg(dibujo, ajuste), sec, flags=re.S)
    clase = 'portada t2' if tomo == 'II' else 'portada'
    sec = sec.replace('<section class="portada">', f'<section class="{clase}">', 1)
    return sec.replace('</section>', f'<p class="op">Opción {n} · Tomo {tomo}</p></section>')


def armar(opciones, salida, ajuste='xMidYMid meet'):
    """Una portada por opción y tomo, en un PDF (salida: nombre del archivo en esta carpeta)."""
    css_extra = f"""
    .portada {{ break-after: page; }}
    .portada .trazos {{ top: 146mm; height: 82mm; }}
    .t2 .pt-centro {{ border-left-color: {MENTA}; }}
    .t2 .bajada {{ color: {MENTA}; }}
    .op {{ position: absolute; right: 8mm; bottom: 4mm; margin: 0; font: 600 8pt 'Plus Jakarta Sans'; color: #8f7a83; }}
    """
    cuerpo = ''.join(portada(n, t, f(ROSA if t == 'I' else MENTA, t == 'II'), ajuste)
                     for n, (_, _, f) in enumerate(opciones, 1) for t in ('I', 'II'))
    doc = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{H.css()}{css_extra}</style></head>'
           f'<body>{cuerpo}</body></html>')
    from weasyprint import HTML  # noqa: E402
    HTML(string=doc, base_url=str(H.LIBRO) + '/').write_pdf(f'{AQUI}/{salida}')
    for n, (nombre, idea, _) in enumerate(opciones, 1):
        print(f'{n}. {nombre}: {idea}')


if __name__ == '__main__':
    armar(OPCIONES, 'portadas-opciones.pdf')
