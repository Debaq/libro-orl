"""Mide latencias y amplitudes de las ondas rotuladas en una figura ABR del motor.

Lee el SVG: las anclas dan la posición de cada pico rotulado y el trazo
promediado (opacidad 1) da la curva. Escala del motor: 22 px por ms y
80 px por µV; cada panel parte en x0 = 70 + i * (ancho_panel + 40).

Amplitud: del pico a la depresión más baja de los 1,5 ms siguientes
(para la V es V-SN10), y también la altura del pico sobre la media del trazo.

Uso: python3 medir_abr.py figura.svg [figura_antes.svg]
"""
import json
import re
import sys

MS_PX, UV_PX = 22, 80


def leer(path):
    s = open(path).read()
    W = float(re.search(r'<svg[^>]*width="([\d.]+)"', s).group(1))
    an = json.loads(re.search(r'<metadata id="anclas">(.*?)</metadata>', s, re.S).group(1))
    lados = [l for l in ('OD', 'OI') if any(k.startswith(l + ' ') for k in an)]
    pw = (W - 134 - (len(lados) - 1) * 40) / len(lados)
    x0s = {l: 70 + i * (pw + 40) for i, l in enumerate(lados)}
    trazos = []
    for d in re.findall(r'<path d="(M[^"]+)"[^>]*stroke-opacity="1(?:\.0)?"', s):
        pts = [tuple(map(float, p.split(','))) for p in d[1:].split(' L')]
        trazos.append(pts)
    # asignar cada trazo a su nivel: mismo panel y media más cercana a la base
    curvas = {}
    for k, (x, y) in an.items():
        p = k.split()
        if len(p) != 2:
            continue
        lado = p[0]
        cands = [t for t in trazos if abs(t[0][0] - x0s[lado]) < 1]
        t = min(cands, key=lambda t: abs(sum(q[1] for q in t) / len(t) - y))
        curvas[k] = (t, y)
    out = {}
    for k, (x, y) in an.items():
        p = k.split()
        if len(p) != 3:
            continue
        nivel = ' '.join(p[:2])
        t, base = curvas[nivel]
        lat = (x - x0s[p[0]]) / MS_PX
        alto = (base - y) / UV_PX
        tras = [q[1] for q in t if x < q[0] <= x + 1.5 * MS_PX]
        pp = (max(tras) - y) / UV_PX if tras else None
        out[k] = {'lat': round(lat, 2), 'pp': round(pp, 2) if pp is not None else None,
                  'alto': round(alto, 2)}
    niveles = [k for k in an if len(k.split()) == 2]
    return out, niveles


def tabla(path, antes=None):
    b, niv = leer(path)
    a, niva = leer(antes) if antes else ({}, [])
    for lado in ('OD', 'OI'):
        ns = sorted({int(k.split()[1]) for k in niv + niva if k.startswith(lado)}, reverse=True)
        for n in ns:
            celdas = []
            for o in ('I', 'III', 'V'):
                k = f'{lado} {n} {o}'
                f = lambda d: f"{d[k]['lat']:.2f}/{d[k]['pp']:.2f}" if k in d else '—'
                celdas.append(f'{o} {f(a)}→{f(b)}' if antes else f'{o} {f(b)}')
            print(f'  {lado} {n:>3}: ' + ' | '.join(celdas))


if __name__ == '__main__':
    tabla(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
