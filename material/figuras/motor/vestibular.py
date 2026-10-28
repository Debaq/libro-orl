"""Figuras vestibulares del libro, desde los datos que declara cada caso.

LabSim no genera nistagmo ni calórica: los valores son del caso y van en su
spec (casos/<caso>.json), y aquí solo se dibujan con el estilo del motor.

nistagmo  la hoja del campo clínico: un hexágono con fijación y otro sin
          fijación. Triángulo izquierdo = mirada a la izquierda; derecho =
          mirada a la derecha; franjas = mirada arriba, al frente y abajo.
          Flechas hacia donde bate la fase rápida; su número da la intensidad.
          Un campo sin nistagmo lleva (−), como en la hoja: nunca queda en blanco.
mariposa  las cuatro irrigaciones de la calórica bitermal en el tiempo, con la
          velocidad de la fase lenta (arriba bate a la derecha, abajo a la
          izquierda).
"""
import math

from . import estilo as E
from .svg import Svg

CAMPOS = ('izquierda', 'arriba', 'centro', 'abajo', 'derecha')
DIRECCION = {'izquierda': (-1, 0), 'derecha': (1, 0), 'arriba': (0, -1), 'abajo': (0, 1)}


def _leer(v):
    """Un campo del hexágono: número (VFL horizontal, negativo = bate a la
    izquierda) o {'dir': 'izquierda|derecha|arriba|abajo', 'vfl': n}.
    Devuelve (dirección, vfl) o None si no hay nistagmo."""
    if v in (None, 0):
        return None
    if isinstance(v, (int, float)):
        return ('izquierda' if v < 0 else 'derecha', abs(float(v)))
    return (v['dir'], float(v.get('vfl', 1)))


def _cuantas(vfl):
    """Número de flechas según la intensidad (°/s)."""
    return 1 if vfl < 4 else (2 if vfl < 7 else 3)


def _flecha(s, cx, cy, d, largo=16):
    dx, dy = DIRECCION[d]
    x1, y1 = cx - dx * largo / 2, cy - dy * largo / 2
    x2, y2 = cx + dx * largo / 2, cy + dy * largo / 2
    s.linea(x1, y1, x2 - dx * 6, y2 - dy * 6, E.OD, 2.2)
    # punta
    px, py = -dy, dx
    s.crudo(f'<polygon points="{x2:.1f},{y2:.1f} {x2 - dx * 8 + px * 4.5:.1f},{y2 - dy * 8 + py * 4.5:.1f} '
            f'{x2 - dx * 8 - px * 4.5:.1f},{y2 - dy * 8 - py * 4.5:.1f}" fill="{E.OD}"/>')


def _hexagono(s, x0, y0, titulo, campos):
    w, h, p = 240, 120, 60
    xr0, xr1 = x0 + p, x0 + p + w
    s.texto(x0 + p + w / 2, y0 - 12, titulo, E.T_TITULO, E.TINTA, 'middle', 600)
    s.crudo(f'<polygon points="{x0},{y0 + h / 2} {xr0},{y0} {xr1},{y0} {xr1 + p},{y0 + h / 2} '
            f'{xr1},{y0 + h} {xr0},{y0 + h}" fill="none" stroke="{E.TINTA}" stroke-width="1.6"/>')
    for x in (xr0, xr1):
        s.linea(x, y0, x, y0 + h, E.TINTA, 1.6)
    for y in (y0 + h / 3, y0 + 2 * h / 3):
        s.linea(xr0, y, xr1, y, E.TINTA, 1.1)
    centros = {'izquierda': (x0 + p * 0.6, y0 + h / 2), 'derecha': (xr1 + p * 0.4, y0 + h / 2),
               'arriba': (xr0 + w / 2, y0 + h / 6), 'centro': (xr0 + w / 2, y0 + h / 2),
               'abajo': (xr0 + w / 2, y0 + 5 * h / 6)}
    for campo in CAMPOS:
        dato = _leer(campos.get(campo))
        cx, cy = centros[campo]
        if not dato:
            s.texto(cx, cy + 5, '(−)', E.T_TITULO + 2, E.TINTA, 'middle', 600)
            continue
        d, vfl = dato
        n = _cuantas(vfl)
        lateral = campo in ('izquierda', 'derecha')
        paso, largo = (15, 13) if lateral else (30, 20)
        for i in range(n):
            _flecha(s, cx + (i - (n - 1) / 2) * paso, cy, d, largo)


def nistagmo(con_fijacion, sin_fijacion):
    s = Svg(800, 175)
    _hexagono(s, 20, 34, 'Con fijación', con_fijacion or {})
    _hexagono(s, 420, 34, 'Sin fijación', sin_fijacion or {})
    return s.svg()


def _respuesta(t, pico):
    """Curva de una irrigación: sube desde ~20 s, culmina ~70 s y decae."""
    x = max(t - 20, 0)
    return pico * (x / 50) ** 2 * math.exp(2 * (1 - x / 50))


def mariposa(od44, od30, oi44, oi30):
    """VFL máximas (°/s, sin signo) de cada irrigación."""
    irr = (('OD 44 °C', od44, +1, E.OD, None), ('OD 30 °C', od30, -1, E.OD, '5 3'),
           ('OI 44 °C', oi44, -1, E.OI, None), ('OI 30 °C', oi30, +1, E.OI, '5 3'))
    tope = max(10, math.ceil(max(od44, od30, oi44, oi30) / 10) * 10)
    pw, ph, ml, mt = 470, 190, 46, 34
    s = Svg(ml + pw + 140, mt + ph + 40)

    def X(t):
        return ml + t / 180 * pw

    def Y(v):
        return mt + ph / 2 - v / tope * (ph / 2)

    s.rect(X(0), mt, X(40) - X(0), ph, E.LAVADO)
    s.texto(X(20), mt + 12, 'irrigación', E.T_CHICO, E.TENUE)
    for v in range(-tope, tope + 1, 10):
        s.linea(X(0), Y(v), X(180), Y(v), E.GRILLA_FUERTE if v == 0 else E.GRILLA, 1)
        s.texto(X(0) - 6, Y(v) + 3, v, E.T_EJE, E.TENUE, 'end')
    for t in range(0, 181, 30):
        s.texto(X(t), mt + ph + 14, t, E.T_EJE, E.TENUE)
    s.texto(X(90), mt + ph + 30, 'Tiempo desde el inicio de la irrigación (s)', E.T_EJE, E.TENUE)
    s.texto(14, mt + ph / 2, 'VFL (°/s)', E.T_EJE, E.TENUE,
            extra=f'transform="rotate(-90 14 {mt + ph / 2:.1f})"')
    s.texto(X(180), mt - 6, 'bate a la derecha', E.T_CHICO, E.TENUE, 'end')
    s.texto(X(180), Y(-tope) - 4, 'bate a la izquierda', E.T_CHICO, E.TENUE, 'end')
    for k, (nombre, pico, signo, col, guiones) in enumerate(irr):
        pts = [(X(t), Y(signo * _respuesta(t, pico))) for t in range(0, 181, 2)]
        s.trazo(pts, col, 2.0, guiones=guiones)
        y = mt + 16 + k * 18
        s.linea(ml + pw + 14, y - 3, ml + pw + 36, y - 3, col, 2.0,
                f'stroke-dasharray="{guiones}"' if guiones else '')
        s.texto(ml + pw + 42, y, f'{nombre}: {pico:g} °/s'.replace('.', ','), E.T_ROTULO, E.TINTA, 'start')
    return s.svg()


# --- VNG de una maniobra posicional -------------------------------------------
H_COLOR, V_COLOR = '#1d1d1f', '#21796c'


def _vfl(c, t):
    """VFL (°/s, con signo de la fase rápida: + derecha o arriba) de un
    componente en el tiempo t desde que se llega a la posición.
    c = {'dir': +1|-1, 'lat': s, 'pico': °/s, 'dur': s, 'tipo': 'paroxistico'|'persistente'}"""
    if not c or t < c.get('lat', 0):
        return 0.0
    x = t - c.get('lat', 0)
    pico, dur = c['pico'], c.get('dur', 60)
    if c.get('tipo', 'paroxistico') == 'persistente':
        v = pico * min(1.0, x / 1.5)
    else:
        if x >= dur:
            return 0.0
        sube = dur * 0.3                          # crescendo hasta un 30 % del tiempo, después decae
        v = pico * (x / sube if x < sube else math.cos((x - sube) / (dur - sube) * math.pi / 2) ** 1.5)
    return c['dir'] * v


def _batidas(c, seg, semilla):
    """Simula el ojo: fase lenta a la VFL, fase rápida al llegar a ±A grados.
    Devuelve (traza [(t, pos)], batidas [(t, vfl)])."""
    import random
    r = random.Random(semilla)
    dt, A = 0.005, 2.5
    p, t, traza, bat, desde = 0.0, 0.0, [], [], 0.0
    lentas = []
    while t <= seg:
        v = _vfl(c, t)
        p -= v * dt                                # la fase lenta va al revés de la rápida
        lentas.append(v)
        if abs(p) >= A * (0.8 + 0.4 * r.random()):
            traza.append((t, p))
            p = -p * 0.6                           # fase rápida: vuelve y cruza
            if len(lentas) > 10:
                bat.append((t, sum(lentas) / len(lentas) * (0.9 + 0.2 * r.random())))
            lentas = []
        traza.append((t, p))
        t += dt
    return traza, bat


def vng(paneles):
    """Registro de VNG de una o más posiciones, como lo entrega el equipo:
    arriba, la VFL de cada batida en el tiempo (un punto por batida; horizontal
    y vertical); abajo, 4 s de la posición del ojo en el pico.
    paneles = [{'titulo': ..., 'seg': 40, 'h': comp|None, 'v': comp|None}]"""
    n = len(paneles)
    gap, ml = 30, 44
    pw = (800 - ml - 10 - gap * (n - 1)) / n
    alto_vfl, alto_pos = 120, 70
    y0 = 30
    tope = max(10, math.ceil(max(abs(c['pico']) for p in paneles for c in (p.get('h'), p.get('v')) if c) / 10) * 10)
    s = Svg(800, y0 + alto_vfl + 34 + alto_pos * 2 + 46)
    for i, pan in enumerate(paneles):
        x0 = ml + i * (pw + gap)
        seg = pan.get('seg', 40)
        s.texto(x0 + pw / 2, 14, pan['titulo'], E.T_TITULO, E.TINTA, 'middle', 600)

        def X(t):
            return x0 + t / seg * pw

        def Y(v):
            return y0 + alto_vfl / 2 - v / tope * (alto_vfl / 2)
        # VFL por batida
        for v in range(-tope, tope + 1, 10):
            s.linea(x0, Y(v), x0 + pw, Y(v), E.GRILLA_FUERTE if v == 0 else E.GRILLA, 1)
            if i == 0:
                s.texto(x0 - 5, Y(v) + 3, v, E.T_EJE, E.TENUE, 'end')
        for t in range(0, seg + 1, 10):
            s.texto(X(t), y0 + alto_vfl + 12, t, E.T_EJE, E.TENUE)
        s.texto(x0 + pw / 2, y0 + alto_vfl + 24, 'Tiempo desde que llega a la posición (s)', E.T_CHICO, E.TENUE)
        s.linea(X(0), y0, X(0), y0 + alto_vfl, E.TENUE, 1, 'stroke-dasharray="3 3"')
        pico_t = {}
        for k, (canal, col) in enumerate((('h', H_COLOR), ('v', V_COLOR))):
            c = pan.get(canal)
            if not c:
                continue
            _, bat = _batidas(c, seg, 7 + i * 3 + k)
            for t, v in bat:
                s.circulo(X(t), Y(v), 1.6, col, col, 0.6)
            if bat:
                # el pico de la envolvente (el primero, si es una meseta), no el de una batida
                env = [(k10 / 10, abs(_vfl(c, k10 / 10))) for k10 in range(seg * 10 + 1)]
                tope_env = max(v for _, v in env)
                pico_t[canal] = next(tt for tt, v in env if v >= tope_env * 0.98) + 1.5
        if not pico_t:
            s.texto(x0 + pw / 2, Y(0) - 6, 'sin nistagmo', E.T_ROTULO, E.TENUE)
        # posición del ojo, 4 s alrededor del pico
        centro = max(pico_t.values()) if pico_t else seg / 2
        t0 = max(0.0, min(seg - 4.0, centro - 2.0))
        yb = y0 + alto_vfl + 34
        for k, (canal, col, rot) in enumerate((('h', H_COLOR, 'Horizontal'), ('v', V_COLOR, 'Vertical'))):
            yc = yb + k * alto_pos + alto_pos / 2
            s.linea(x0, yc, x0 + pw, yc, E.GRILLA, 1)
            s.texto(x0 + 2, yc - alto_pos / 2 + 10, f'{rot} (°)', E.T_CHICO, E.TENUE, 'start')
            c = pan.get(canal)
            traza = _batidas(c, seg, 7 + i * 3 + k)[0] if c else [(0, 0), (seg, 0)]
            pts = [(x0 + (t - t0) / 4 * pw, yc - p * 9) for t, p in traza if t0 <= t <= t0 + 4]
            if not c:
                pts = [(x0, yc), (x0 + pw, yc)]
            s.trazo(pts, col, 1.1)
        s.texto(x0 + pw / 2, yb + 2 * alto_pos + 12,
                f'Posición del ojo, de {t0:.0f} a {t0 + 4:.0f} s'.replace('.', ','), E.T_CHICO, E.TENUE)
    s.texto(14, y0 + alto_vfl / 2, 'VFL (°/s)', E.T_EJE, E.TENUE, extra=f'transform="rotate(-90 14 {y0 + alto_vfl / 2:.1f})"')
    yl = y0 + alto_vfl + 34 + alto_pos * 2 + 34
    s.circulo(ml + 4, yl - 3, 2.2, H_COLOR, H_COLOR, 0.6)
    s.texto(ml + 12, yl, 'horizontal: + bate a la derecha', E.T_CHICO, E.TINTA, 'start')
    s.circulo(ml + 194, yl - 3, 2.2, V_COLOR, V_COLOR, 0.6)
    s.texto(ml + 202, yl, 'vertical: + bate hacia arriba', E.T_CHICO, E.TINTA, 'start')
    s.texto(ml + 384, yl, 'Un punto por batida. En la posición del ojo, el salto brusco es la fase rápida.',
            E.T_CHICO, E.TENUE, 'start')
    return s.svg()


# --- vHIT ---------------------------------------------------------------------
def _impulso(t, pico=220, dur=150):
    """Velocidad de la cabeza en un impulso (°/s), campana de ~150 ms."""
    if t < 0 or t > dur:
        return 0.0
    return pico * math.sin(math.pi * t / dur) ** 2


def vhit(der, izq):
    """vHIT del canal lateral: un gráfico por oído (él, 2026-10-20). En cada
    uno la cabeza (gris) y el ojo (color del lado) van en sentidos opuestos,
    porque el ojo compensa. Oído derecho: el ojo hacia arriba y la cabeza
    hacia abajo; oído izquierdo: la cabeza hacia arriba y el ojo hacia abajo. La ganancia es lo que
    alcanza el ojo respecto de la cabeza; las sacadas van hacia donde va el ojo.
    der / izq = {'ganancia': 0.95, 'sacadas': None|'covert'|'overt'|'ambas'}."""
    import random
    pw, ph, ml, mt, gap = 230, 170, 40, 30, 34
    s = Svg(ml + 2 * pw + gap + 10, mt + ph + 34)
    for k, (lado, d, col, signo) in enumerate((('derecha', der, E.OD, 1), ('izquierda', izq, E.OI, -1))):
        x0 = ml + k * (pw + gap)

        def X(t):
            return x0 + t / 400 * pw

        def Y(v):
            return mt + ph / 2 - v / 300 * (ph / 2)
        s.texto(x0 + pw / 2, 14, f"Oído {'derecho' if signo > 0 else 'izquierdo'}: impulsos hacia la {lado}",
                E.T_TITULO, E.TINTA, 'middle', 600)
        for v in range(-300, 301, 100):
            s.linea(x0, Y(v), x0 + pw, Y(v), E.GRILLA_FUERTE if v == 0 else E.GRILLA, 1)
            if k == 0:
                s.texto(x0 - 6, Y(v) + 3, v, E.T_EJE, E.TENUE, 'end')
        for t in range(0, 401, 100):
            s.texto(X(t), mt + ph + 13, t, E.T_EJE, E.TENUE)
        g = float(d.get('ganancia', 1.0))
        sac = d.get('sacadas')
        r = random.Random(11 + k)
        for n in range(8):                                   # varios impulsos superpuestos
            pico = 190 + r.random() * 60
            off = r.uniform(-6, 6)
            s.trazo([(X(t), Y(-signo * _impulso(t - 20 - off, pico))) for t in range(0, 401, 4)], E.TENUE, 0.8, opacidad=0.6)
            ojo = []
            for t in range(0, 401, 4):
                v = g * _impulso(t - 24 - off, pico)
                if sac in ('covert', 'ambas'):                # dentro del impulso
                    v += 160 * math.exp(-((t - 120 - off) / 14) ** 2) * (0.8 + 0.4 * r.random())
                if sac in ('overt', 'ambas'):                 # después del impulso
                    v += 170 * math.exp(-((t - 230 - off) / 16) ** 2) * (0.8 + 0.4 * r.random())
                ojo.append((X(t), Y(signo * v)))             # el ojo, al revés que la cabeza
            s.trazo(ojo, col, 1.0, opacidad=0.8)
        # rótulos en la mitad donde va el ojo
        yr = mt + 14 if signo > 0 else mt + ph - 26
        s.texto(x0 + pw - 6, yr, f'ganancia {g:.2f}'.replace('.', ','), E.T_ROTULO + 1, col, 'end', 700)
        if sac:
            s.texto(x0 + pw - 6, yr + 13, {'covert': 'sacadas covert', 'overt': 'sacadas overt',
                                           'ambas': 'sacadas covert y overt'}[sac], E.T_ROTULO, col, 'end', 600)
    s.texto(ml + pw + gap / 2, mt + ph + 28, 'Tiempo (ms). Gris: cabeza; color: ojo.', E.T_CHICO, E.TENUE)
    s.texto(12, mt + ph / 2, '°/s', E.T_EJE, E.TENUE)
    return s.svg()
