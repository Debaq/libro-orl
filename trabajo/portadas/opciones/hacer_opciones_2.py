"""Segunda ronda de portadas: todas en el lenguaje de la portada actual.

Siete trazos a todo el ancho, apilados, cada uno más tenue que el anterior
(la geometría de trazos_portada() en hacer_libro.py). La opción 1 es la
portada actual tal cual; las otras cambian el examen que se dibuja.

    python3 portadas/opciones/hacer_opciones_2.py     -> portadas-opciones-2.pdf
"""
import math

import hacer_opciones as O

FILAS = 7


def fila(k):
    """Base, amplitud y opacidad de la fila k, como en la portada actual."""
    return 30 + k * 27, 14 * (1 - k / (FILAS + 2)), 0.85 - k * 0.09


def trazo(fx, k, c):
    """fx(t, k) -> desplazamiento hacia arriba (en amplitudes) para t de 0 a 1."""
    base, amp, op = fila(k)
    pts = [(600 * i / 300, base - fx(i / 300, k) * amp) for i in range(301)]
    return O.linea(pts, c, 1.6, op)


def apilado(fx, c):
    return ''.join(trazo(fx, k, c) for k in range(FILAS))


# ---------- los exámenes, como función del tiempo (t de 0 a 1) ----------
def f_peat(t, k, retraso=0.0):
    ms = t * 12
    lat = 5.6 + k * 0.35 + retraso * k
    y = sum(a * math.exp(-((ms - l) / 0.28) ** 2) for a, l in ((0.5, 1.6 + k * .08), (0.7, 3.8 + k * .2), (1.0, lat)))
    y -= 0.5 * math.exp(-((ms - lat - 1.1) / 0.5) ** 2)
    return y + 0.06 * math.sin(ms * 7 + k)


def f_timpano(t, k, desvio=0.0, aplana=0.0):
    p0 = 0.62 - desvio * k / (FILAS - 1)
    a = 1.8 * (1 - aplana * k / (FILAS - 1)) * (0.75 + 0.25 * math.cos(k))   # 1.8: el más alto no se corta
    return a * math.exp(-((t - p0) / 0.07) ** 2) + 0.05 * math.sin(t * 40 + k)


def f_nistagmo(t, k, ganancia=1.0):
    env = math.sin(math.pi * min(1, max(0, (t - 0.08) / 0.84))) ** 1.4
    u = (t * 34 + k * 0.37) % 1
    saw = u / 0.82 if u < 0.82 else (1 - u) / 0.18
    return 1.6 * ganancia * env * saw


NORMAL = [0.2, 0.5, 0.35, 0.6, 0.3, 0.45, 0.1]          # 125 a 8k, en amplitudes (arriba = oye mejor)


def f_audiograma(t, k, caida=0.0):
    """Un audiograma: tramos rectos entre las 7 frecuencias, como se dibuja.
    caida > 0 abre una muesca en 4 kHz que se profundiza fila a fila (ruido)."""
    vals = [v + 0.25 * math.sin(i * 1.7 + k) for i, v in enumerate(NORMAL)]
    if caida:
        muesca = caida * (0.4 + 0.45 * k)
        vals[4] -= muesca * 1.6
        vals[5] -= muesca * 0.9
        vals[6] -= muesca * 0.4
    x = t * 6
    i = min(5, int(x))
    return vals[i] + (vals[i + 1] - vals[i]) * (x - i)


def o1(c, t2):   # la portada actual
    return apilado(lambda t, k: f_peat(t, k), c)


def o2(c, t2):   # timpanogramas apilados
    if not t2:
        return apilado(lambda t, k: f_timpano(t, k), c)
    return apilado(lambda t, k: f_timpano(t, k, desvio=0.32, aplana=0.85), c)


def o3(c, t2):   # calórica: nistagmo que crece y se apaga
    if not t2:
        return apilado(lambda t, k: f_nistagmo(t, k), c)
    return apilado(lambda t, k: f_nistagmo(t, k, ganancia=1 - 0.75 * k / (FILAS - 1)), c)


def o4(c, t2):   # audiogramas apilados
    if not t2:
        return apilado(lambda t, k: f_audiograma(t, k), c)
    return apilado(lambda t, k: f_audiograma(t, k, caida=1.0), c)


def o5(c, t2):   # un examen por trazo, con la geometría de la portada actual
    examenes = [lambda t, k: f_peat(t, k), lambda t, k: f_timpano(t, k),
                lambda t, k: f_nistagmo(t, k), lambda t, k: f_audiograma(t, k)]
    if t2:
        examenes = [lambda t, k: f_peat(t, k, retraso=0.25), lambda t, k: f_timpano(t, 3, desvio=0.5, aplana=0.6),
                    lambda t, k: f_nistagmo(t, k, ganancia=0.35), lambda t, k: f_audiograma(t, 5, caida=1.0)]
    return ''.join(trazo(examenes[k % 4], k, c) for k in range(FILAS))


def o6(c, t2):   # transición: arriba un examen, abajo otro, y en medio la mezcla
    a, b = ((lambda t, k: f_peat(t, k)), (lambda t, k: f_nistagmo(t, k))) if not t2 else \
           ((lambda t, k: f_timpano(t, k)), (lambda t, k: f_audiograma(t, k, caida=1.0)))
    return apilado(lambda t, k: (1 - k / (FILAS - 1)) * a(t, k) + k / (FILAS - 1) * b(t, k), c)


OPCIONES = [
    ('La actual', 'Los trazos de PEAT de hoy. II: igual, en menta.', o1),
    ('Timpanogramas', 'Siete timpanogramas apilados. II: se corren a presión negativa y se aplanan (C y B).', o2),
    ('Prueba calórica', 'Nistagmo que crece y se apaga. II: cada trazo responde menos (paresia).', o3),
    ('Audiogramas', 'Siete audiogramas, de 125 Hz a 8 kHz. II: la muesca de 4 kHz se profundiza (ruido).', o4),
    ('Un examen por trazo', 'PEAT, timpanograma, nistagmo y audiograma alternados. II: los mismos alterados.', o5),
    ('Transición', 'I: del PEAT arriba al nistagmo abajo. II: del timpanograma al audiograma que cae.', o6),
]

if __name__ == '__main__':
    O.armar(OPCIONES, 'portadas-opciones-2.pdf', ajuste='none')
