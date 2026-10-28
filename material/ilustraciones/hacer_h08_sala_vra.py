#!/usr/bin/env python3
"""Dibuja h08-sala-vra.svg (fig. H8.1): la sala de VRA vista desde arriba.

El niño en las rodillas de la mamá, en la silla marcada en el piso; un
parlante con su refuerzo visual a cada lado, a 1 m y cerca de los 90°; al
frente, la mesa baja con el segundo examinador; tras el vidrio, el
examinador que maneja el audiómetro y los refuerzos. Es la sala que describe
la lista de Equipo y sala del capítulo (BSA, 2025a y 2025b). Esquema propio,
no IA; las medidas son las del texto (1 m = 200 px).

    python3 material/ilustraciones/hacer_h08_sala_vra.py
"""
import pathlib

AQUI = pathlib.Path(__file__).resolve().parent
TINTA, TENUE, MURO = '#24101a', '#6b6b72', '#8a8a90'
PIEL, ROPA, ROPA_2 = '#efd9c6', '#d9cfe0', '#cfe0d9'
PARLANTE, REFUERZO, VIDRIO = '#4a4a50', '#e0a526', '#cfe3f2'
F = "font-family=\"'Plus Jakarta Sans', sans-serif\""
T = 15            # letra: a todo el ancho (~172 mm) queda en ~8 pt impresa

out = []


def texto(x, y, s, size=T, anchor='middle', peso=400, color=TINTA):
    out.append(f'<text x="{x}" y="{y}" {F} font-size="{size}" fill="{color}" '
               f'text-anchor="{anchor}" font-weight="{peso}">{s}</text>')


def rect(x, y, w, h, fill, stroke=TINTA, sw=1.2, r=0, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
               f'stroke="{stroke}" stroke-width="{sw}"{d}/>')


def linea(x1, y1, x2, y2, color=TINTA, sw=1.2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d}/>')


def persona(x, y, mira, ropa, cabeza=17, hombros=(44, 19)):
    """Una persona vista desde arriba: hombros y cabeza, con la nariz hacia `mira`."""
    dx, dy = {'arriba': (0, -1), 'abajo': (0, 1), 'izquierda': (-1, 0)}[mira]
    rx, ry = hombros if dy else hombros[::-1]
    out.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{ropa}" stroke="{TINTA}" stroke-width="1.2"/>')
    out.append(f'<circle cx="{x}" cy="{y}" r="{cabeza}" fill="{PIEL}" stroke="{TINTA}" stroke-width="1.2"/>')
    nx, ny = x + dx * cabeza, y + dy * cabeza
    out.append(f'<polygon points="{nx + dx * 6},{ny + dy * 6} {nx - dy * 5},{ny + dx * 5} {nx + dy * 5},{ny - dx * 5}" '
               f'fill="{PIEL}" stroke="{TINTA}" stroke-width="1.2"/>')


def parlante(x, y, hacia):
    """Parlante (caja con el cono hacia el niño) y, encima, el refuerzo visual."""
    rect(x - 17, y - 26, 34, 52, PARLANTE, r=3)
    cx = x + 17 * hacia
    out.append(f'<polygon points="{cx},{y - 14} {cx},{y + 14} {cx + 9 * hacia},{y + 20} {cx + 9 * hacia},{y - 20}" '
               f'fill="{PARLANTE}" stroke="{TINTA}" stroke-width="1"/>')
    # el refuerzo, sobre el parlante: caja oscura con el juguete iluminado
    rect(x - 13, y - 13, 26, 26, '#2b2b30', stroke=REFUERZO, sw=2, r=3)
    out.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{REFUERZO}"/>')


W, H = 900, 560
# Salas y vidrio
rect(20, 30, 630, 510, '#ffffff', MURO, 3)
rect(650, 30, 230, 510, '#f6f4f1', MURO, 3)
rect(644, 190, 12, 220, VIDRIO, MURO, 1.2)
texto(36, 60, 'Sala de prueba', 16, 'start', 700)
texto(666, 60, 'Sala de control', 16, 'start', 700)
texto(636, 300, 'vidrio', anchor='end', color=TENUE)

# La silla marcada en el piso: el punto calibrado
C = (330, 340)
out.append(f'<circle cx="{C[0]}" cy="{C[1] + 22}" r="64" fill="none" stroke="{TENUE}" stroke-width="1.4" '
           f'stroke-dasharray="6 5"/>')

# Distancias: 1 m a cada parlante
for xp, xt in ((130, 232), (530, 428)):
    linea(C[0], C[1], xp, C[1], TENUE, 1.2, '4 4')
    texto(xt, C[1] - 8, '1 m', color=TENUE)
parlante(130, C[1], 1)
parlante(530, C[1], -1)

# Mamá (atrás) con el fono, y el niño en sus rodillas, los dos mirando al frente
persona(C[0], C[1] + 50, 'arriba', ROPA, 19, (48, 21))
out.append(f'<path d="M {C[0] - 21} {C[1] + 50} A 21 21 0 0 1 {C[0] + 21} {C[1] + 50}" fill="none" '
           f'stroke="{TINTA}" stroke-width="2.4"/>')
for s in (-1, 1):
    rect(C[0] + s * 22 - 4, C[1] + 43, 8, 14, TINTA, r=2)
persona(C[0], C[1], 'arriba', ROPA_2, 14, (30, 14))

# Al frente: mesa baja y el segundo examinador
rect(270, 170, 120, 44, '#efe9df', r=4)
for x in (300, 330, 362):
    out.append(f'<circle cx="{x}" cy="192" r="7" fill="#d98aa3" stroke="{TINTA}" stroke-width="1"/>')
persona(330, 128, 'abajo', '#e3d3b8', 16, (42, 18))
texto(400, 190, 'mesa baja,', anchor='start')
texto(400, 208, 'juguetes silenciosos', anchor='start')
texto(384, 116, 'examinador 2:', anchor='start', peso=700)
texto(384, 134, 'lo entretiene al frente', anchor='start')

# El giro de cabeza que se refuerza
out.append(f'<path d="M {C[0] + 16} {C[1] - 16} Q 430 268 505 312" fill="none" stroke="{REFUERZO}" '
           f'stroke-width="2.6" marker-end="url(#punta)"/>')
texto(436, 262, 'gira al sonido: se enciende', 14, color='#9a6a00')
texto(436, 279, 'el juguete', 14, color='#9a6a00')

# Rótulos de los parlantes y de la silla
for x in (130, 530):
    texto(x, 392, 'parlante y')
    texto(x, 410, 'refuerzo visual')
    texto(x, 428, 'encima')
texto(C[0], 456, 'niño en las rodillas de la mamá;')
texto(C[0], 474, 'ella, con un fono con música')
texto(C[0], 504, 'silla marcada en el piso: el punto calibrado', color=TENUE)

# Sala de control: el audiómetro y el examinador 1
rect(664, 228, 46, 144, '#efe9df', r=3)
rect(670, 262, 34, 76, '#3a3a40', r=3)
persona(752, 300, 'izquierda', '#e3d3b8', 16, (42, 18))
texto(765, 400, 'examinador 1:', peso=700)
texto(765, 418, 'audiómetro')
texto(765, 436, 'y refuerzos')
texto(687, 222, 'audiómetro', 13, color=TENUE)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
       f'<defs><marker id="punta" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
       f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{REFUERZO}"/></marker></defs>'
       f'<rect width="{W}" height="{H}" fill="#fff"/>' + ''.join(out) + '</svg>')
(AQUI / 'h08-sala-vra.svg').write_text(svg, encoding='utf-8')
print('h08-sala-vra.svg')
