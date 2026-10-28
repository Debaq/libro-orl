#!/usr/bin/env python3
"""Ilustraciones del ASSR de Alba (rubéola congénita, caso 17.3, cap. 17):

    cap17-assr-deteccion.svg   detección por oído, frecuencia y nivel (valor de p de la prueba F)
    cap17-assr-audiograma.svg  umbral del ASSR (dB nHL) y audiograma estimado (dB eHL), con el ABR al lado

LabSim no genera ASSR: esto es una SIMULACIÓN propia, no un registro. De dónde sale cada cifra:

* Umbral "verdadero" de cada oído y frecuencia: audiometría modelada del caso
  (casos/generados/cap17_rubeola_congenita.json, data.Aerea; columnas 500, 1.000, 2.000 y 4.000 Hz):
      OD 80 / 85 / 90 / 95 dB HL        OI 80 / 80 / 85 / 90 dB HL
* Umbral del ASSR (dB nHL) = audiometría + diferencia promedio ASSR - conductual de lactantes menores
  de 2 años (9,24 / 7,19 / 6,35 / 7,42 dB en 500 / 1.000 / 2.000 / 4.000 Hz; metaanálisis de Huang, Kluk y Perugia,
  Syst Rev 2025, doi:10.1186/s13643-025-03003-x; DOI y cifras verificados en Crossref, resumen), redondeado a pasos de 5 dB.
  Queda <= 100 dB nHL: sobre 100 dB nHL por vía aérea las respuestas pueden ser vestibulares o artefacto
  (BSA, 2023, OD104-115, sec. 7.4; leído en el documento).
* Corrección alternativa a dB eHL: tabla provisional de la BSA (2023, tabla 1), fonos de inserción,
  hasta 12 semanas de EDAD CORREGIDA (<=84 dias), umbrales sobre 30 dB eHL: -20 / -20 / -15 / -15.
  Alba tiene 85 dias de vida (edad_horas=2050) pero nacio a las 37 semanas (historia clinica del caso):
  edad corregida de unos 64 dias, dentro del tramo. La tabla no tiene otra fila para mayores.
* Pasos de la búsqueda: BSA (2023): sobre 80 dB nHL una frecuencia por vez; sin respuesta, subir 20;
  con respuesta, bajar 10 y luego 5; criterio de 95 % con réplica en el umbral.
* Detección: prueba F sobre el espectro del EEG (potencia en la frecuencia de modulación frente al
  promedio de 60 contenedores vecinos; F con 2 y 120 grados de libertad, p = (1 + F/60)^-60). La
  respuesta del paciente es una amplitud sobre el ruido que crece desde el umbral; las demás cifras
  (p) las produce la simulación con semilla fija. No son datos de un equipo."""
import math
import pathlib
import random

TINTA, TENUE, GRILLA, FUERTE = '#24101a', '#6f6f76', '#e7e5e0', '#cfccc5'
OK, AUS, ROJO, AZUL = '#21796c', '#8a8a90', '#c62f3a', '#2a5db0'
F = "font-family=\"'Plus Jakarta Sans', sans-serif\""
AQUI = pathlib.Path(__file__).parent

FRS = [500, 1000, 2000, 4000]
AUDIO = {'OD': [80, 85, 90, 95], 'OI': [80, 80, 85, 90]}
DIF_LACT = [9, 7, 6, 7]
BSA = [20, 20, 15, 15]
ABR_EHL = {'OD': {500: 80}, 'OI': {500: 80}}      # burst de 500 Hz: 100 dB nHL - 20 (cap. 17)
CLICK_EHL = 90                                    # click, sin corrección (cap. 17)


def r5(x):
    return int(5 * round(x / 5))


UMBRAL = {o: [r5(a + d) for a, d in zip(AUDIO[o], DIF_LACT)] for o in AUDIO}   # dB nHL del ASSR
EHL_BSA = {o: [u - c for u, c in zip(UMBRAL[o], BSA)] for o in AUDIO}
EHL_LACT = {o: [r5(u - d) for u, d in zip(UMBRAL[o], DIF_LACT)] for o in AUDIO}


def pval(f):
    return (1 + f / 60) ** -60


def simular():
    """Devuelve res[oido][frec_idx][nivel] = p, siguiendo la búsqueda de la BSA."""
    rnd = random.Random(2310)
    res = {}
    for o in AUDIO:
        res[o] = []
        for i in range(4):
            thr = UMBRAL[o][i]
            vistos = {}

            def medir(n):
                lam = 0 if n < thr else 9 * 1.35 ** ((n - thr) / 5)   # amplitud^2 sobre el ruido
                for _ in range(200):
                    re, im = rnd.gauss(0, math.sqrt(.5)), rnd.gauss(0, math.sqrt(.5))
                    pot = (math.sqrt(lam) + re) ** 2 + im ** 2
                    ruido = sum(rnd.expovariate(1) for _ in range(60)) / 60
                    f = pot / ruido
                    p = pval(f)
                    if (n >= thr) == (p < .05):   # semilla elegida: el caso típico, sin falsos positivos
                        return p
                raise SystemExit('no converge')
            vistos[80] = medir(80)
            vistos[100] = medir(100)
            n = 90
            vistos[90] = medir(90)
            if vistos[90] < .05:          # responde a 90: bajar de 5 en 5
                n = 85
                while n > 80:
                    vistos[n] = medir(n)
                    if vistos[n] >= .05:
                        break
                    n -= 5
            else:                          # no responde a 90: subir a 95
                vistos[95] = medir(95)
            res[o].append(vistos)
    return res


class Lienzo:
    def __init__(self, w, h):
        self.w, self.h, self.out = w, h, []

    def t(self, x, y, s, size=11.5, color=TINTA, anchor='middle', peso=400):
        self.out.append(f'<text x="{x:.1f}" y="{y:.1f}" {F} font-size="{size}" fill="{color}" '
                        f'text-anchor="{anchor}" font-weight="{peso}">{s}</text>')

    def l(self, x1, y1, x2, y2, color=TINTA, w=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        self.out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{w}"{d}/>')

    def r(self, x, y, w, h, fill, stroke='none'):
        self.out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="3" fill="{fill}" stroke="{stroke}"/>')

    def guardar(self, nombre):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
               f'width="{self.w}" height="{self.h}"><rect width="{self.w}" height="{self.h}" fill="#fff"/>'
               + ''.join(self.out) + '</svg>')
        (AQUI / nombre).write_text(svg, encoding='utf-8')
        print(nombre)


def fmt(p):
    return '&lt;0,001' if p < .001 else f'{p:.3f}'.replace('.', ',') if p < .1 else f'{p:.2f}'.replace('.', ',')


def deteccion(res):
    c = Lienzo(700, 330)
    niveles = [100, 95, 90, 85, 80]
    cw, ch = 70, 32
    for k, (o, x0) in enumerate((('OD', 52), ('OI', 382))):
        c.t(x0 + 4 * cw / 2, 24, ('Oído derecho' if o == 'OD' else 'Oído izquierdo'), 13, ROJO if o == 'OD' else AZUL, 'middle', 700)
        for i, fr in enumerate(FRS):
            c.t(x0 + i * cw + cw / 2, 50, f'{fr:,}'.replace(',', '.'), 11.5, TENUE, 'middle', 600)
        for j, n in enumerate(niveles):
            y = 60 + j * ch
            c.t(x0 - 6, y + ch / 2 + 4, n, 11.5, TENUE, 'end')
            for i in range(4):
                p = res[o][i].get(n)
                x = x0 + i * cw
                if p is None:
                    c.r(x + 2, y + 2, cw - 4, ch - 4, '#fff', GRILLA)
                    continue
                if p < .05:
                    c.r(x + 2, y + 2, cw - 4, ch - 4, '#dcefe9', OK)
                    c.t(x + cw / 2, y + ch / 2 + 4, fmt(p), 11.5, OK, 'middle', 700)
                else:
                    c.r(x + 2, y + 2, cw - 4, ch - 4, '#f3f2ef', FUERTE)
                    c.t(x + cw / 2, y + ch / 2 + 4, fmt(p), 11.5, AUS, 'middle', 400)
        c.t(x0 - 6, 52, 'dB nHL', 11.5, TENUE, 'end')
        # umbral marcado con borde grueso
        for i in range(4):
            j = niveles.index(UMBRAL[o][i])
            c.out.append(f'<rect x="{x0 + i * cw + 2}" y="{60 + j * ch + 2}" width="{cw - 4}" height="{ch - 4}" rx="3" fill="none" stroke="{TINTA}" stroke-width="2"/>')
    yl = 60 + 5 * ch + 22
    c.r(52, yl - 12, 20, 14, '#dcefe9', OK)
    c.t(78, yl, 'respuesta clara (p &lt; 0,05); borde grueso: umbral', 11.5, TINTA, 'start')
    c.r(382, yl - 12, 20, 14, '#f3f2ef', FUERTE)
    c.t(408, yl, 'respuesta ausente (p ≥ 0,05)', 11.5, TINTA, 'start')
    c.t(52, yl + 22, 'Celda en blanco: nivel no probado. Sobre 80 dB nHL el equipo prueba una frecuencia por vez y baja 10 y luego 5 dB.', 11.5, TENUE, 'start')
    c.t(52, yl + 40, 'Cada número es el valor de p de la prueba F; el umbral exige réplica (criterio de 95 %).', 11.5, TENUE, 'start')
    c.guardar('cap17-assr-deteccion.svg')


def audiograma():
    c = Lienzo(700, 330)
    for k, (o, x0) in enumerate((('OD', 60), ('OI', 390))):
        col = ROJO if o == 'OD' else AZUL
        w, y0, alto = 250, 52, 200
        X = lambda i: x0 + 25 + i * (w - 50) / 3
        Y = lambda db: y0 + (db - 20) / 100 * alto
        c.t(x0 + w / 2, 24, ('Oído derecho' if o == 'OD' else 'Oído izquierdo'), 13, col, 'middle', 700)
        for db in range(20, 121, 20):
            c.l(x0, Y(db), x0 + w, Y(db), GRILLA, 1)
            c.t(x0 - 8, Y(db) + 4, db, 11.5, TENUE, 'end')
        for i, fr in enumerate(FRS):
            c.t(X(i), y0 - 8, f'{fr:,}'.replace(',', '.'), 11.5, TENUE, 'middle', 600)
        c.t(x0 - 8, y0 - 28, 'dB eHL', 11.5, TENUE, 'end')
        # rango entre las dos correcciones
        for i in range(4):
            a, b = EHL_BSA[o][i], EHL_LACT[o][i]
            c.out.append(f'<rect x="{X(i) - 8:.1f}" y="{Y(a):.1f}" width="16" height="{Y(b) - Y(a):.1f}" rx="3" fill="{col}" fill-opacity=".15"/>')
        c.out.append(f'<polyline points="{" ".join(f"{X(i):.1f},{Y(EHL_BSA[o][i]):.1f}" for i in range(4))}" fill="none" stroke="{col}" stroke-width="1.6"/>')
        for i in range(4):
            xx, yy = X(i), Y(EHL_BSA[o][i])
            c.out.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="5" fill="#fff" stroke="{col}" stroke-width="2"/>')
            xx, yy = X(i), Y(EHL_LACT[o][i])
            c.out.append(f'<rect x="{xx - 4.5:.1f}" y="{yy - 4.5:.1f}" width="9" height="9" fill="{col}"/>')
        # ABR: burst de 500 Hz (triángulo en 500) y click (triángulo entre 2.000 y 4.000)
        for xx, db in ((X(0) + 22, 80), ((X(2) + X(3)) / 2, CLICK_EHL)):
            yy = Y(db)
            c.out.append(f'<polygon points="{xx:.1f},{yy - 6:.1f} {xx + 7:.1f},{yy + 6:.1f} {xx - 7:.1f},{yy + 6:.1f}" fill="{TINTA}"/>')
    # leyenda
    ly = 285
    c.out.append(f'<circle cx="68" cy="{ly - 4}" r="5" fill="#fff" stroke="{TINTA}" stroke-width="2"/>')
    c.t(80, ly, 'ASSR corregido con la tabla de la BSA (2023)', 11.5, TINTA, 'start')
    c.out.append(f'<rect x="388" y="{ly - 9}" width="9" height="9" fill="{TINTA}"/>')
    c.t(402, ly, 'ASSR con la diferencia de lactantes (Huang, 2025)', 11.5, TINTA, 'start')
    c.out.append(f'<polygon points="68,{ly + 11} 75,{ly + 23} 61,{ly + 23}" fill="{TINTA}"/>')
    c.t(80, ly + 22, 'ABR: burst de 500 Hz (80 dB eHL) y click (90 dB eHL, entre 2.000 y 4.000 Hz)', 11.5, TINTA, 'start')
    c.t(68, ly + 42, 'La banda sombreada es el rango entre las dos correcciones.', 11.5, TENUE, 'start')
    c.guardar('cap17-assr-audiograma.svg')


if __name__ == '__main__':
    res = simular()
    for o in AUDIO:
        print(o, 'nHL', UMBRAL[o], 'eHL BSA', EHL_BSA[o], 'eHL lact', EHL_LACT[o])
        for i, fr in enumerate(FRS):
            print('  ', fr, {n: round(p, 4) for n, p in sorted(res[o][i].items(), reverse=True)})
    deteccion(res)
    audiograma()
