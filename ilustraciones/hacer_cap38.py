#!/usr/bin/env python3
"""Registros de sueño de los cuatro pacientes del capítulo 38 (El que ronca).

    python3 ilustraciones/hacer_cap38.py            dibuja los SVG e imprime todos los índices
    python3 ilustraciones/hacer_cap38.py --indices  solo imprime los índices

Cada paciente es una noche SIMULADA con semilla fija (no hay datos de personas): hipnograma, posición,
eventos respiratorios (con su duración, tipo y caída de saturación), despertares, ronquido y SpO2 segundo a
segundo. Los índices del capítulo se CALCULAN de esos datos (nunca se escriben a mano) y los trazos de
flujo y esfuerzo de las figuras se generan a partir de los mismos eventos, así que las figuras y las tablas
coinciden. Criterios de puntuación: AASM (Berry y cols., 2012): apnea con caída del flujo >= 90 % por >= 10 s;
hipopnea con caída >= 30 % por >= 10 s y desaturación >= 3 % o despertar; RERA aparte.

Salidas (ilustraciones/):
    cap38-colapso.svg                 esquema: resistencia nasal y colapso faríngeo
    cap38-pg-roncador-resumen.svg     poligrafía del roncador simple (resumen de la noche)
    cap38-pg-roncador-trazo.svg       lo mismo, 2 minutos de registro
    cap38-pg-moderado-resumen.svg     poligrafía del SAOS moderado
    cap38-pg-moderado-trazo.svg
    cap38-psg-grave-resumen.svg       polisomnografía del SAOS grave
    cap38-psg-grave-trazo.svg
    cap38-psg-dudosa-resumen.svg      polisomnografía cuando la poligrafía no alcanzó
    cap38-psg-dudosa-trazo.svg
    cap38-psg-dudosa-pg.svg           la poligrafía previa de ese paciente
"""
import json
import math
import pathlib
import random
import sys

AQUI = pathlib.Path(__file__).parent
TINTA, TENUE, GRILLA, FUERTE = '#24101a', '#6b6b72', '#e7e5e0', '#cfccc5'
COCLEAR, RETRO, AVISO, AZUL = '#c0571c', '#21796c', '#c62f3a', '#2f5d9e'
F = "font-family=\"'Plus Jakarta Sans', sans-serif\""
ORDEN = {'W': 4, 'R': 3, 'N1': 2, 'N2': 1, 'N3': 0}
NOM_ETAPA = {'W': 'Vigilia', 'R': 'REM', 'N1': 'N1', 'N2': 'N2', 'N3': 'N3'}
COL_POS = {'supino': AVISO, 'izquierda': RETRO, 'derecha': AZUL}


# ----------------------------------------------------------------------------------- lienzo
class Lienzo:
    def __init__(self, w, h):
        self.w, self.h, self.o = w, h, []

    def t(self, x, y, s, size=12.5, color=TINTA, anchor='start', peso=400):
        s = str(s)
        self.o.append(f'<text x="{x:.1f}" y="{y:.1f}" {F} font-size="{size}" fill="{color}" text-anchor="{anchor}" '
                      f'font-weight="{peso}">{s}</text>')

    def l(self, x1, y1, x2, y2, color=TINTA, w=1, dash=None, op=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        o = f' stroke-opacity="{op}"' if op else ''
        self.o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{w}"{d}{o}/>')

    def poli(self, pts, color, w=1.4, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        p = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        self.o.append(f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="round"{d}/>')

    def rect(self, x, y, w, h, fill='none', stroke=None, sw=1, op=None, r=0):
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
        o = f' fill-opacity="{op}"' if op is not None else ''
        self.o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}"{o}{s}/>')

    def raw(self, s):
        self.o.append(s)

    def guardar(self, nombre):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" '
               f'height="{self.h}"><rect width="{self.w}" height="{self.h}" fill="#fff"/>' + ''.join(self.o) + '</svg>')
        (AQUI / nombre).write_text(svg, encoding='utf-8')


def coma(x, d=1):
    return f'{x:.{d}f}'.replace('.', ',')


# ----------------------------------------------------------------------------------- pacientes
# seq: etapas (etapa, minutos); la primera W es la latencia. pos: (desde, hasta, posición) en min desde apagar luces.
# tasa: eventos/h de sueño por etapa en posición lateral; fpos: factor por posición; mix: tipo -> proporción
# drop_*: caída media de SpO2 (puntos) de apneas e hipopneas; hip_sin: fracción de hipopneas con caída < 3 (solo despertar)
PACIENTES = {
    'roncador': dict(
        titulo='Poligrafía · roncador simple', semilla=3801, tib=470,
        seq=[('W', 16), ('N1', 6), ('N2', 30), ('N3', 40), ('N2', 20), ('R', 14), ('W', 4), ('N2', 36), ('N3', 24),
             ('N2', 28), ('R', 22), ('W', 6), ('N2', 40), ('R', 28), ('N1', 6), ('N2', 30), ('R', 30), ('W', 5),
             ('N2', 20), ('N1', 5), ('N2', 20), ('W', 8), ('N2', 32)],
        pos=[(0, 130, 'supino'), (130, 250, 'derecha'), (250, 330, 'supino'), (330, 470, 'izquierda')],
        tasa=dict(N1=4.0, N2=2.4, N3=0.6, R=4.5), fpos=dict(supino=1.6, izquierda=0.6, derecha=0.7),
        mix=dict(ao=0.30, am=0.0, ac=0.05, h=0.65), drop_ap=3.5, drop_hip=3.4, hip_sin=0.35, rem_extra=0.8,
        base=96.8, p_ar=0.7, ar_esp=9.0, ron_p=dict(supino=0.85, izquierda=0.5, derecha=0.6), dur_ap=(10, 20), dur_h=(10, 24)),
    'moderado': dict(
        titulo='Poligrafía · SAOS moderado con obstrucción nasal', semilla=3802, tib=475,
        seq=[('W', 20), ('N1', 6), ('N2', 22), ('N3', 28), ('N2', 18), ('R', 10), ('W', 6), ('N1', 4), ('N2', 30),
             ('N3', 14), ('N2', 22), ('R', 16), ('W', 8), ('N2', 34), ('N1', 6), ('R', 20), ('W', 6), ('N2', 30),
             ('N1', 8), ('R', 24), ('W', 10), ('N2', 26), ('N1', 6), ('N2', 20), ('W', 5), ('N2', 30)],
        pos=[(0, 140, 'supino'), (140, 210, 'derecha'), (210, 340, 'supino'), (340, 400, 'izquierda'), (400, 475, 'supino')],
        tasa=dict(N1=21.0, N2=18.0, N3=9.0, R=40.0), fpos=dict(supino=1.7, izquierda=0.45, derecha=0.55),
        mix=dict(ao=0.30, am=0.05, ac=0.02, h=0.63), drop_ap=6.5, drop_hip=4.8, hip_sin=0.15, rem_extra=2.2,
        base=95.3, p_ar=0.85, ar_esp=8.0, ron_p=dict(supino=0.85, izquierda=0.35, derecha=0.5), dur_ap=(11, 34), dur_h=(10, 36)),
    'grave': dict(
        titulo='Polisomnografía · SAOS grave', semilla=3803, tib=462,
        seq=[('W', 18), ('N1', 14), ('N2', 26), ('N1', 6), ('W', 8), ('N2', 20), ('N3', 6), ('N2', 16), ('N1', 8), ('R', 8),
             ('W', 14), ('N1', 10), ('N2', 30), ('N1', 6), ('W', 10), ('N2', 28), ('R', 10), ('N1', 8), ('W', 12),
             ('N2', 30), ('N1', 10), ('R', 12), ('W', 14), ('N1', 8), ('N2', 26), ('W', 8), ('N2', 22), ('R', 8), ('N1', 6),
             ('W', 4), ('N2', 18)],
        pos=[(0, 90, 'supino'), (90, 160, 'derecha'), (160, 300, 'supino'), (300, 370, 'izquierda'), (370, 462, 'supino')],
        tasa=dict(N1=95.0, N2=90.0, N3=70.0, R=120.0), fpos=dict(supino=1.25, izquierda=0.75, derecha=0.85), gap=(3, 10),
        mix=dict(ao=0.42, am=0.07, ac=0.01, h=0.50), drop_ap=11.0, drop_hip=6.5, hip_sin=0.07, rem_extra=4.0,
        base=93.6, p_ar=0.9, ar_esp=5.0, ron_p=dict(supino=0.95, izquierda=0.7, derecha=0.8), dur_ap=(12, 44), dur_h=(11, 36)),
    'dudosa': dict(
        titulo='Polisomnografía · cuando la poligrafía no alcanza', semilla=3804, tib=456,
        seq=[('W', 38), ('N1', 10), ('N2', 22), ('W', 16), ('N1', 6), ('N2', 26), ('N3', 14), ('N2', 10), ('W', 24),
             ('N1', 8), ('N2', 24), ('R', 10), ('W', 30), ('N1', 6), ('N2', 20), ('R', 14), ('N1', 6), ('W', 22),
             ('N2', 30), ('N1', 8), ('R', 18), ('W', 26), ('N2', 20), ('N1', 6), ('W', 12), ('N2', 10)],
        pos=[(0, 120, 'supino'), (120, 200, 'izquierda'), (200, 330, 'supino'), (330, 456, 'derecha')],
        tasa=dict(N1=44.0, N2=34.0, N3=14.0, R=52.0), fpos=dict(supino=1.2, izquierda=0.8, derecha=0.9),
        mix=dict(ao=0.04, am=0.0, ac=0.01, h=0.70, rera=0.25), drop_ap=3.6, drop_hip=3.5, hip_sin=0.82, rem_extra=0.8,
        base=97.4, p_ar=1.0, ar_esp=6.0, ron_p=dict(supino=0.45, izquierda=0.15, derecha=0.2), dur_ap=(10, 18), dur_h=(10, 30)),
    # la noche de poligrafía en casa del mismo paciente (sueño más largo, mismas características)
    'dudosa_pg': dict(
        titulo='Poligrafía previa', semilla=3805, tib=438,
        seq=[('W', 30), ('N1', 8), ('N2', 30), ('N3', 22), ('N2', 16), ('W', 12), ('N2', 26), ('R', 12), ('N1', 6),
             ('W', 14), ('N2', 34), ('N3', 10), ('N2', 20), ('R', 16), ('W', 18), ('N2', 36), ('N1', 6), ('R', 20),
             ('W', 10), ('N2', 22), ('N1', 8), ('R', 14), ('W', 6), ('N2', 20)],
        pos=[(0, 150, 'supino'), (150, 260, 'derecha'), (260, 438, 'izquierda')],
        tasa=dict(N1=44.0, N2=34.0, N3=14.0, R=52.0), fpos=dict(supino=1.2, izquierda=0.8, derecha=0.9),
        mix=dict(ao=0.04, am=0.0, ac=0.01, h=0.70, rera=0.25), drop_ap=3.6, drop_hip=3.5, hip_sin=0.82, rem_extra=0.8,
        base=97.4, p_ar=1.0, ar_esp=6.0, ron_p=dict(supino=0.45, izquierda=0.15, derecha=0.2), dur_ap=(10, 18), dur_h=(10, 30)),
}
TIPOS = [('ao', 'apnea obstructiva'), ('am', 'apnea mixta'), ('ac', 'apnea central'), ('h', 'hipopnea'), ('rera', 'RERA')]


# ----------------------------------------------------------------------------------- simulación
def simular(clave):
    P = PACIENTES[clave]
    rng = random.Random(P['semilla'])
    seg, t = [], 0
    for e, d in P['seq']:
        seg.append((e, t * 60, (t + d) * 60))
        t += d
    # la noche dura lo que dice tib: se recorta o se rellena con la última etapa
    N = P['tib'] * 60
    seg = [(e, a, min(b, N)) for e, a, b in seg if a < N]
    if seg[-1][2] < N:
        e, a, b = seg[-1]
        seg[-1] = (e, a, N)
    etapa = ['W'] * N
    for e, a, b in seg:
        for s in range(a, b):
            etapa[s] = e
    pos = ['supino'] * N
    for a, b, p in P['pos']:
        for s in range(a * 60, min(b * 60, N)):
            pos[s] = p
    ev, s, libre = [], 0, 0
    tipos, pesos = zip(*P['mix'].items())
    while s < N:
        e = etapa[s]
        if e == 'W' or s < libre:
            s += 1
            continue
        lam = P['tasa'][e] * P['fpos'][pos[s]] / 3600.0
        if rng.random() < lam:
            tp = rng.choices(tipos, pesos)[0]
            if tp == 'rera':
                dur = rng.randint(10, 18)
            elif tp == 'h':
                dur = rng.randint(*P['dur_h'])
            else:
                dur = rng.randint(*P['dur_ap'])
            fin_seg = next(b for ee, a, b in seg if a <= s < b)
            dur = min(dur, fin_seg - s - 3)
            if dur < 10:
                s += 1
                continue
            extra = P['rem_extra'] if e == 'R' else 0.0
            if tp in ('ao', 'am'):
                drop = max(1.0, rng.gauss(P['drop_ap'] + extra + 0.06 * dur, 1.6))
            elif tp == 'ac':
                drop = max(1.0, rng.gauss(P['drop_ap'] - 1.0, 1.0))
            elif tp == 'h':
                if rng.random() < P['hip_sin']:
                    drop = rng.uniform(0.4, 2.6)
                else:
                    drop = max(3.0, rng.gauss(P['drop_hip'] + extra * 0.7, 1.2))
            else:
                drop = rng.uniform(0.0, 1.6)
            if tp == 'rera' or (tp == 'h' and drop < 3.0):
                arousal = True
            else:
                arousal = rng.random() < P['p_ar']
            ev.append(dict(t=s, dur=dur, tipo=tp, etapa=e, pos=pos[s], drop=drop, arousal=arousal))
            libre = s + dur + rng.randint(*P.get('gap', (6, 22)))
            s = libre
        else:
            s += 1
    # despertares espontáneos
    esp = []
    for s in range(N):
        if etapa[s] != 'W' and rng.random() < P['ar_esp'] / 3600.0:
            esp.append(s)
    # SpO2 segundo a segundo
    caida = [0.0] * N
    for x in ev:
        if x['tipo'] == 'rera':
            continue
        t0 = x['t'] + int(0.3 * x['dur'])
        nadir_t = x['t'] + x['dur'] + 7
        d = x['drop']
        for k in range(t0, min(N, nadir_t + 60)):
            if k <= nadir_t:
                v = d * (k - t0) / max(1, nadir_t - t0)
            else:
                v = d * math.exp(-(k - nadir_t) / 9.0)
            caida[k] = max(caida[k], v)
    sp = []
    rr = random.Random(P['semilla'] + 1)
    ruido = 0.0
    for k in range(N):
        ruido = 0.8 * ruido + rr.uniform(-0.08, 0.08)
        sp.append(round(P['base'] - caida[k] + ruido, 1))
    # ronquido por minuto
    ron = [False] * (N // 60 + 1)
    for m in range(N // 60):
        if etapa[m * 60 + 30] != 'W':
            p = P['ron_p'][pos[m * 60 + 30]] * (0.4 if etapa[m * 60 + 30] == 'N3' else 1.0)
            ron[m] = rr.random() < p
    return dict(P=P, clave=clave, seg=seg, N=N, etapa=etapa, pos=pos, ev=ev, esp=esp, sp=sp, ron=ron)


def odi(sp, etapa, umbral=3):
    """Cuenta caídas de la saturación de al menos `umbral` puntos respecto del máximo de los 2 min previos (solo sueño)."""
    n, k, en = 0, 0, False
    ref = 0
    N = len(sp)
    for s in range(N):
        a = max(0, s - 120)
        if not en:
            ref = max(sp[a:s + 1])
            if etapa[s] != 'W' and sp[s] <= ref - umbral:
                n += 1
                en = True
        else:
            if sp[s] >= ref - 1:
                en = False
    return n


def resumen(S, modo='psg'):
    """modo 'psg': por hora de sueño. modo 'pg': por hora de registro, sin etapas (solo lo que ve una poligrafía)."""
    ev, etapa, pos, N, sp, seg = S['ev'], S['etapa'], S['pos'], S['N'], S['sp'], S['seg']
    r = {}
    sueno = [s for s in range(N) if etapa[s] != 'W']
    tst = len(sueno) / 60.0
    tib = N / 60.0
    r['TIB'], r['TST'] = tib, tst
    r['eficiencia'] = 100 * tst / tib
    lat = seg[0][2] / 60.0
    r['latencia'] = lat
    rem = next((a for e, a, b in seg if e == 'R'), None)
    r['latencia REM'] = (rem / 60.0 - lat) if rem is not None else None
    r['WASO'] = sum(b - a for e, a, b in seg if e == 'W') / 60.0 - lat
    for e in ('N1', 'N2', 'N3', 'R'):
        m = sum(b - a for ee, a, b in seg if ee == e) / 60.0
        r['min ' + e] = m
        r['% ' + e] = 100 * m / tst
    cuenta = {tp: sum(1 for x in ev if x['tipo'] == tp) for tp, _ in TIPOS}
    r['n'] = cuenta
    hip_des = [x for x in ev if x['tipo'] == 'h' and x['drop'] >= 3.0]
    hip_ar = [x for x in ev if x['tipo'] == 'h' and x['drop'] < 3.0]
    r['hip con desaturación'], r['hip solo despertar'] = len(hip_des), len(hip_ar)
    apn = [x for x in ev if x['tipo'] in ('ao', 'am', 'ac')]
    r['n IAH'] = len(apn) + cuenta['h']
    r['n REI'] = len(apn) + len(hip_des)                    # lo que ve una poligrafía: sin despertares
    r['n IAH4'] = len(apn) + sum(1 for x in ev if x['tipo'] == 'h' and x['drop'] >= 4.0)
    base_h = tst if modo == 'psg' else tib
    r['base horas'] = base_h / 60.0
    r['IAH'] = r['n IAH'] / (tst / 60.0)
    r['IAH4'] = r['n IAH4'] / (tst / 60.0)
    r['IDR'] = (r['n IAH'] + cuenta['rera']) / (tst / 60.0)
    r['REI'] = r['n REI'] / (tib / 60.0)                     # por hora de registro
    r['REI sobre TST'] = r['n REI'] / (tst / 60.0)
    r['IAI'] = len(apn) / (tst / 60.0)
    r['durmax'] = max(x['dur'] for x in ev if x['tipo'] != 'rera')
    r['durmed'] = sum(x['dur'] for x in ev if x['tipo'] != 'rera') / max(1, len([x for x in ev if x['tipo'] != 'rera']))
    nar = sum(1 for x in ev if x['arousal']) + len(S['esp'])
    r['n despertares'] = nar
    r['IDespertares'] = nar / (tst / 60.0)
    r['ODI3'] = odi(sp, etapa, 3)
    r['IDO3'] = r['ODI3'] / (tst / 60.0)
    r['IDO3 reg'] = r['ODI3'] / (tib / 60.0)
    r['ODI4'] = odi(sp, etapa, 4)
    r['IDO4'] = r['ODI4'] / (tst / 60.0)
    if modo == 'psg':
        vals = [round(sp[s]) for s in sueno]
        r['T90'] = 100 * sum(1 for v in vals if v < 90) / len(vals)
        r['T88'] = 100 * sum(1 for v in vals if v <= 88) / len(vals)
    else:
        vals = [round(v) for v in sp]
        r['T90'] = 100 * sum(1 for v in vals if v < 90) / len(vals)
    r['SpO2 media'] = sum(vals) / len(vals)
    r['SpO2 min'] = min(vals)
    for p in ('supino', 'izquierda', 'derecha'):
        m_reg = sum(1 for s in range(N) if pos[s] == p) / 60.0
        m_sue = sum(1 for s in sueno if pos[s] == p) / 60.0
        r['min ' + p] = m_reg
        r['REI ' + p] = sum(1 for x in apn + hip_des if x['pos'] == p) / (m_reg / 60.0) if m_reg else 0
        r['IAH ' + p] = sum(1 for x in apn + [y for y in ev if y['tipo'] == 'h'] if x['pos'] == p) / (m_sue / 60.0) if m_sue else 0
    for e in ('N1', 'N2', 'N3', 'R'):
        h = r['min ' + e] / 60.0
        r['IAH ' + e] = sum(1 for x in apn + [y for y in ev if y['tipo'] == 'h'] if x['etapa'] == e) / h if h else 0
    nrem_h = (tst - r['min R']) / 60.0
    r['IAH NREM'] = sum(1 for x in apn + [y for y in ev if y['tipo'] == 'h'] if x['etapa'] != 'R') / nrem_h
    s2 = sum(1 for k in range(min(7200, N)) if etapa[k] != 'W') / 3600.0
    r['sueño primeras 2 h'] = s2 * 60
    r['IAH primeras 2 h'] = sum(1 for x in apn + [y for y in ev if y['tipo'] == 'h'] if x['t'] < 7200) / s2
    r['ronquido %'] = 100 * sum(S['ron']) / tib if modo == 'pg' else 100 * sum(S['ron']) / tst
    return r


def gravedad(i):
    return 'normal' if i < 5 else 'leve' if i < 15 else 'moderada' if i < 30 else 'grave'


# ----------------------------------------------------------------------------------- señales (ventana de segundos)
def ventana(S, t0, dur, fs=20):
    """Flujo (presión nasal), tórax, abdomen, EEG, EMG, ronquido: generados a partir de los eventos reales."""
    P = S['P']
    rng = random.Random(P['semilla'] + t0)
    f = 0.25
    out = {k: [] for k in ('flujo', 'torax', 'abd', 'eeg', 'emg', 'ron')}
    evs = [x for x in S['ev'] if x['t'] + x['dur'] + 10 >= t0 and x['t'] <= t0 + dur]
    ph0 = rng.random() * 6
    # fase respiratoria acumulada
    ph = ph0
    et = S['etapa'][min(S['N'] - 1, t0 + dur // 2)]
    eeg_amp = {'W': 0.25, 'N1': 0.35, 'N2': 0.45, 'N3': 0.9, 'R': 0.3}[et]
    for i in range(int(dur * fs)):
        t = t0 + i / fs
        env_f, env_e, par, lim, silencio_e = 1.0, 1.0, 0.0, False, False
        arousal_on = False
        ron_amp = 0.0
        for x in evs:
            a, b = x['t'], x['t'] + x['dur']
            if a <= t <= b:
                u = (t - a) / x['dur']
                tp = x['tipo']
                if tp == 'ao':
                    env_f, env_e, par = 0.05, 0.5 + 1.1 * u, min(1.0, 0.4 + 0.8 * u)
                elif tp == 'ac':
                    env_f, env_e = 0.05, 0.05
                elif tp == 'am':
                    env_f = 0.05
                    if u < 0.4:
                        env_e = 0.05
                    else:
                        env_e, par = 0.5 + 1.1 * (u - 0.4) / 0.6, min(1.0, 0.4 + 0.8 * (u - 0.4) / 0.6)
                elif tp == 'h':
                    env_f, env_e, par, lim = 0.5, 0.8 + 0.4 * u, 0.3, True
                else:  # RERA: flujo casi normal, aplanado; esfuerzo creciente
                    env_f, env_e, par, lim = 0.8, 0.8 + 0.7 * u, 0.4, True
            elif b < t <= b + 4:
                if x['tipo'] != 'rera':
                    env_f, env_e = 1.45, 1.4
                    ron_amp = 0.9
            if x['arousal'] and b - 1 <= t <= b + 5:
                arousal_on = True
        for s0 in S['esp']:
            if s0 - 0 <= t <= s0 + 5:
                arousal_on = True
        if S['ron'][min(len(S['ron']) - 1, int(t // 60))] and ron_amp == 0.0:
            ron_amp = 0.45
        ph += 2 * math.pi * f / fs * (1 + 0.04 * math.sin(t / 3.1))
        base = math.sin(ph)
        sn = base
        if lim and base > 0:
            sn = min(base, 0.6) / 0.6 * 0.85
        flujo = env_f * sn + rng.uniform(-0.03, 0.03)
        torax = env_e * base + rng.uniform(-0.03, 0.03)
        abd = env_e * math.sin(ph + 0.2) * (1 - 2 * par) + rng.uniform(-0.03, 0.03)
        insp = max(0.0, base)
        ron = ron_amp * insp * rng.uniform(-1, 1) * (1.0 if env_f > 0.3 else 0.0)
        # EEG: delta/theta de fondo; ráfaga alfa en el despertar
        if arousal_on:
            eeg = 0.28 * math.sin(2 * math.pi * 10.5 * t) + 0.12 * rng.uniform(-1, 1)
            emg = rng.uniform(-1, 1) * 0.9
        else:
            eeg = eeg_amp * (0.6 * math.sin(2 * math.pi * 1.1 * t + 1) + 0.25 * math.sin(2 * math.pi * 5.5 * t)) \
                + 0.1 * rng.uniform(-1, 1)
            emg = rng.uniform(-1, 1) * (0.08 if et in ('R',) else 0.22)
        out['flujo'].append(flujo)
        out['torax'].append(torax)
        out['abd'].append(abd)
        out['eeg'].append(eeg)
        out['emg'].append(emg)
        out['ron'].append(ron)
    return out


# ----------------------------------------------------------------------------------- figuras
def hipnograma(c, x0, y0, w, h, S, rot=True):
    N = S['N']
    X = lambda s: x0 + s / N * w
    nivel = lambda e: y0 + h - ORDEN[e] / 4 * h
    for k in range(5):
        c.l(x0, y0 + h - k / 4 * h, x0 + w, y0 + h - k / 4 * h, GRILLA, 1)
    for e, k in ORDEN.items():
        c.t(x0 - 8, y0 + h - k / 4 * h + 4, NOM_ETAPA[e], 12.5, TINTA, 'end')
    for hh in range(0, int(N / 3600) + 1):
        c.l(X(hh * 3600), y0, X(hh * 3600), y0 + h, GRILLA, 1)
        c.t(X(hh * 3600), y0 + h + 17, hh, 12.5, TENUE, 'middle')
    for e, a, b in S['seg']:
        if e == 'R':
            c.rect(X(a), nivel('R') - 5, X(b) - X(a), 10, AVISO, op=.35)
    pts = []
    for e, a, b in S['seg']:
        pts += [(X(a), nivel(e)), (X(b), nivel(e))]
    c.poli(pts, TINTA, 1.8)
    return X


def resumen_fig(S, nombre, modo, titulo, pie=None):
    N = S['N']
    W = 800
    x0, w = 100, 660
    X = lambda s: x0 + s / N * w
    y = 8
    c = Lienzo(W, 560)
    c.t(8, y + 14, titulo, 14, TINTA, 'start', 700)
    y += 34
    if modo == 'psg':
        c.t(8, y + 4, 'Etapas', 12.5, TINTA, 'start', 700)
        hipnograma(c, x0, y, w, 86, S)
        y += 86 + 26
    # eventos
    c.t(8, y + 8, 'Eventos', 12.5, TINTA, 'start', 700)
    filas = [('ao', 'AO', AVISO), ('am', 'AM', TINTA), ('ac', 'AC', AZUL), ('h', 'H', COCLEAR)]
    if modo == 'psg':
        filas.append(('rera', 'RERA', TENUE))
    for j, (tp, ab, col) in enumerate(filas):
        yy = y + j * 18
        c.t(x0 - 8, yy + 12, ab, 12.5, col, 'end', 700)
        c.l(x0, yy + 16, x0 + w, yy + 16, GRILLA, 1)
        for x in S['ev']:
            if x['tipo'] == tp:
                if tp == 'h' and modo == 'pg' and x['drop'] < 3.0:
                    c.l(X(x['t']), yy + 6, X(x['t']), yy + 15, TENUE, 1.1, '2 2')   # hipopnea sin desaturación: la poligrafía no la cuenta
                else:
                    c.l(X(x['t']), yy + 1, X(x['t']), yy + 15, col, 1.3)
    y += len(filas) * 18 + 8
    # despertares (PSG) o ronquido (PG)
    if modo == 'psg':
        c.t(x0 - 8, y + 12, 'Desp.', 12.5, TENUE, 'end', 700)
        c.l(x0, y + 16, x0 + w, y + 16, GRILLA, 1)
        for x in S['ev']:
            if x['arousal']:
                c.l(X(x['t'] + x['dur']), y + 2, X(x['t'] + x['dur']), y + 15, TINTA, 1)
        for s in S['esp']:
            c.l(X(s), y + 2, X(s), y + 15, TENUE, 1)
        y += 26
    else:
        c.t(x0 - 8, y + 12, 'Ronquido', 12.5, TINTA, 'end', 700)
        for m, v in enumerate(S['ron']):
            if v:
                c.rect(X(m * 60), y + 2, max(1.0, w * 60 / N), 13, COCLEAR, op=.7)
        c.l(x0, y + 16, x0 + w, y + 16, GRILLA, 1)
        y += 26
    # posición
    c.t(x0 - 8, y + 12, 'Posición', 12.5, TINTA, 'end', 700)
    a = 0
    for p, ini in [(S['pos'][0], 0)] + [(S['pos'][k], k) for k in range(1, N) if S['pos'][k] != S['pos'][k - 1]]:
        pass
    cortes = [0] + [k for k in range(1, N) if S['pos'][k] != S['pos'][k - 1]] + [N]
    for i in range(len(cortes) - 1):
        p = S['pos'][cortes[i]]
        c.rect(X(cortes[i]), y + 1, X(cortes[i + 1]) - X(cortes[i]), 17, COL_POS[p], op=.65)
        if X(cortes[i + 1]) - X(cortes[i]) > 60:
            c.t((X(cortes[i]) + X(cortes[i + 1])) / 2, y + 14, p, 12, '#fff', 'middle', 700)
    y += 34
    # SpO2
    hs = 90
    c.t(8, y + 14, 'SpO₂ (%)', 12.5, TINTA, 'start', 700)
    lo = min(80, int((round(min(S['sp'])) - 3) // 10 * 10))
    paso = 10
    Y = lambda v: y + hs - (v - lo) / (100 - lo) * hs
    for v in range(lo, 101, paso):
        c.l(x0, Y(v), x0 + w, Y(v), AVISO if v == 90 else GRILLA, 1, '5 3' if v == 90 else None)
        c.t(x0 - 8, Y(v) + 4, v, 12.5, TENUE, 'end')
    pts = []
    for s in range(0, N, 5):
        pts.append((X(s), Y(max(lo, min(100, min(S['sp'][s:s + 5]))))))
    c.poli(pts, AZUL, 1.1)
    for hh in range(0, int(N / 3600) + 1):
        c.t(X(hh * 3600), y + hs + 17, hh, 12.5, TENUE, 'middle')
    c.t(x0 + w / 2, y + hs + 35, 'horas desde que se apagan las luces', 12.5, TINTA, 'middle')
    y += hs + 52
    if modo == 'psg':
        c.t(8, y, 'AO apnea obstructiva · AM mixta · AC central · H hipopnea · RERA despertar por esfuerzo', 12, TENUE)
        c.t(8, y + 16, 'Desp.: despertares (marca al terminar el evento y despertares espontáneos, en gris)', 12, TENUE)
        y += 16
    else:
        c.t(8, y, 'AO apnea obstructiva · AM mixta · AC central · H hipopnea', 12, TENUE)
        c.t(8, y + 16, 'Línea punteada en H: hipopnea sin desaturación, que la poligrafía no cuenta.', 12, TENUE)
        y += 16
    c.h = int(y + 10)
    c.guardar(nombre)
    return c


def trazo_fig(S, nombre, t0, dur, canales, titulo, notas=()):
    """canales: lista de 'eeg','emg','flujo','torax','abd','ron','spo2'."""
    fs = 20
    sig = ventana(S, t0, dur, fs)
    W = 800
    x0, w = 116, 646
    X = lambda t: x0 + (t - t0) / dur * w
    alto, sep = 60, 12
    H = 40 + len(canales) * (alto + sep) + 56
    c = Lienzo(W, H)
    c.t(8, 20, titulo, 14, TINTA, 'start', 700)
    rot = dict(eeg='EEG C4-M1', emg='EMG mentón', flujo='Presión nasal', torax='Tórax', abd='Abdomen', ron='Ronquido', spo2='SpO₂ (%)')
    colr = dict(eeg=TINTA, emg=TINTA, flujo=COCLEAR, torax=RETRO, abd=RETRO, ron=TENUE, spo2=AZUL)
    ev_v = [x for x in S['ev'] if x['t'] + x['dur'] >= t0 and x['t'] <= t0 + dur and x['tipo'] != 'rera' or
            (x['tipo'] == 'rera' and x['t'] + x['dur'] >= t0 and x['t'] <= t0 + dur)]
    y = 34
    for k in canales:
        c.t(x0 - 8, y + alto / 2 + 4, rot[k], 12.5, TINTA, 'end', 700)
        c.rect(x, y, w, alto, '#fff', FUERTE, 1) if False else c.rect(x0, y, w, alto, '#fff', FUERTE, 1)
        for x in ev_v:
            a, b = max(t0, x['t']), min(t0 + dur, x['t'] + x['dur'])
            c.rect(X(a), y, X(b) - X(a), alto, AVISO if x['tipo'] != 'h' else COCLEAR, op=.09)
        for sg in range(0, dur + 1, 10):
            c.l(X(t0 + sg), y, X(t0 + sg), y + alto, GRILLA, 1)
        if k == 'spo2':
            vals = [S['sp'][s] for s in range(t0, t0 + dur)]
            lo = min(80, min(vals) - 2) if min(vals) < 90 else 88
            hi = 100
            Y = lambda v: y + alto - (v - lo) / (hi - lo) * alto
            c.poli([(X(t0 + i), Y(v)) for i, v in enumerate(vals)], AZUL, 1.8)
            for tv in (90, 95, 100):
                if lo < tv <= hi:
                    c.t(x0 + w + 4, Y(tv) + 4, tv, 12, TENUE)
            mn = min(vals)
            if mn < 95:
                c.t(X(t0 + vals.index(mn)), Y(mn) + 15, f'mín. {round(mn)}', 12, AZUL, 'middle', 700)
        else:
            v = sig[k]
            amp = {'eeg': 1.15, 'emg': 1.2, 'ron': 1.0}.get(k, 1.6)
            c.poli([(X(t0 + i / fs), y + alto / 2 - v[i] / amp * (alto / 2 - 4)) for i in range(len(v))], colr[k], 1.1 if k in ('eeg', 'emg') else 1.5)
        y += alto + sep
    # arousals
    if 'eeg' in canales:
        for x in S['ev']:
            if x['arousal'] and t0 <= x['t'] + x['dur'] <= t0 + dur:
                xa = X(x['t'] + x['dur'] - 0.5)
                c.rect(xa, 30, X(x['t'] + x['dur'] + 4.5) - xa, 6, TINTA)
    # eje
    for sg in range(0, dur + 1, 10):
        c.t(X(t0 + sg), y + 14, sg, 12.5, TENUE, 'middle')
    c.t(x0 + w / 2, y + 32, 'segundos', 12.5, TINTA, 'middle')
    c.h = H
    c.guardar(nombre)


def elegir_ventana(S, criterio, dur):
    """Busca la ventana de `dur` s que cumple `criterio(lista de eventos de la ventana)` con más eventos."""
    mejor, mejor_n = None, -1
    for t0 in range(60, S['N'] - dur - 60, 10):
        evs = [x for x in S['ev'] if t0 + 4 <= x['t'] and x['t'] + x['dur'] <= t0 + dur - 4]
        if S['etapa'][t0 + dur // 2] == 'W' or not evs:
            continue
        if criterio(evs, t0):
            n = len(evs)
            if n > mejor_n:
                mejor, mejor_n = t0, n
    return mejor


def fig_colapso():
    c = Lienzo(800, 330)
    c.t(8, 20, 'Esquema: la nariz y la faringe durante la inspiración dormida (sin escala)', 14, TINTA, 'start', 700)
    paneles = [('A. Nariz permeable', 0, 0.35), ('B. Nariz obstruida', 400, 1.0)]
    for tit, ox, ob in paneles:
        c.t(ox + 8, 50, tit, 13, TINTA, 'start', 700)
        # tubo: nariz (fija) - faringe (blanda) - tráquea
        y0 = 80
        c.raw(f'<path d="M{ox+20},{y0+40} L{ox+130},{y0+40} L{ox+130},{y0+110} L{ox+20},{y0+110} Z" fill="#fbefec" stroke="{TINTA}" stroke-width="1.6"/>')
        # obstrucción nasal (cornete/tabique): estrecha la luz
        h = 14 + 34 * ob
        c.raw(f'<rect x="{ox+60}" y="{y0+40}" width="40" height="{h:.0f}" fill="#f0c3b8" stroke="{COCLEAR}" stroke-width="1.4"/>')
        c.raw(f'<rect x="{ox+60}" y="{y0+110-h:.0f}" width="40" height="{h:.0f}" fill="#f0c3b8" stroke="{COCLEAR}" stroke-width="1.4"/>')
        c.t(ox + 80, y0 + 32, 'nariz', 12.5, COCLEAR, 'middle', 700)
        # faringe blanda: se estrecha más cuanto más obstruida la nariz
        g = 36 - 28 * ob
        c.raw(f'<path d="M{ox+130},{y0+40} Q{ox+185},{y0+40} {ox+200},{y0+75-g/2:.0f} L{ox+260},{y0+75-g/2:.0f} L{ox+260},{y0+75+g/2:.0f} L{ox+200},{y0+75+g/2:.0f} Q{ox+185},{y0+110} {ox+130},{y0+110}" fill="none" stroke="{TINTA}" stroke-width="1.6"/>')
        c.raw(f'<rect x="{ox+200}" y="{y0+75-g/2:.0f}" width="60" height="{g:.0f}" fill="{"#d9e6f5" if ob < .5 else "#f5d9d9"}" opacity=".7"/>')
        c.t(ox + 230, y0 + 36, 'faringe', 12.5, TINTA, 'middle', 700)
        c.t(ox + 230, y0 + 112, 'abierta' if ob < .5 else 'se cierra', 12.5, TINTA if ob < .5 else AVISO, 'middle', 700)
        # flecha de flujo
        c.raw(f'<path d="M{ox+4},{y0+75} L{ox+40},{y0+75}" stroke="{AZUL}" stroke-width="2.4" marker-end="url(#fl)"/>')
        c.t(ox + 8, y0 + 138, 'aire inspirado', 12.5, AZUL, 'start')
        # presión: barra de caída
        c.t(ox + 8, y0 + 170, 'presión en la faringe:', 12.5, TENUE, 'start')
        ln = 60 + 120 * ob
        c.rect(ox + 8, y0 + 178, ln, 14, AVISO if ob > .5 else AZUL, op=.7)
        c.t(ox + 8 + ln + 6, y0 + 190, 'más negativa' if ob > .5 else 'poco negativa', 12.5, TINTA)
    c.raw(f'<defs><marker id="fl" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{AZUL}"/></marker></defs>')
    c.t(8, 318, 'Una nariz que resiste obliga a un esfuerzo mayor; la presión dentro de la faringe baja más y la pared blanda se cierra con más facilidad.', 12, TENUE)
    c.h = 330
    c.guardar('cap38-colapso.svg')


# ----------------------------------------------------------------------------------- principal
def todo(dibujar=True):
    R = {}
    S = {k: simular(k) for k in PACIENTES}
    R['roncador'] = resumen(S['roncador'], 'pg')
    R['moderado'] = resumen(S['moderado'], 'pg')
    R['grave'] = resumen(S['grave'], 'psg')
    R['dudosa'] = resumen(S['dudosa'], 'psg')
    R['dudosa_pg'] = resumen(S['dudosa_pg'], 'pg')
    if not dibujar:
        return S, R
    fig_colapso()
    resumen_fig(S['roncador'], 'cap38-pg-roncador-resumen.svg', 'pg', 'Poligrafía respiratoria · noche en casa')
    resumen_fig(S['moderado'], 'cap38-pg-moderado-resumen.svg', 'pg', 'Poligrafía respiratoria · noche en casa')
    resumen_fig(S['grave'], 'cap38-psg-grave-resumen.svg', 'psg', 'Polisomnografía · noche con técnico presente')
    resumen_fig(S['dudosa'], 'cap38-psg-dudosa-resumen.svg', 'psg', 'Polisomnografía · noche con técnico presente')
    resumen_fig(S['dudosa_pg'], 'cap38-psg-dudosa-pg.svg', 'pg', 'Poligrafía previa · noche en casa')
    V = {}
    # roncador: ventana con ronquido y sin eventos
    t0 = next(t for t in range(3600, S['roncador']['N'] - 200, 30)
              if S['roncador']['pos'][t] == 'supino' and S['roncador']['etapa'][t + 60] in ('N2', 'N1') and
              S['roncador']['ron'][t // 60] and S['roncador']['ron'][(t + 100) // 60] and
              not any(t - 10 <= x['t'] <= t + 130 for x in S['roncador']['ev']))
    V['roncador'] = (t0, 120)
    trazo_fig(S['roncador'], 'cap38-pg-roncador-trazo.svg', t0, 120, ['flujo', 'ron', 'torax', 'abd', 'spo2'],
              'Dos minutos de la poligrafía, decúbito supino')
    t0 = elegir_ventana(S['moderado'], lambda e, t: S['moderado']['pos'][t + 60] == 'supino' and
                        any(x['tipo'] in ('ao', 'am') and x['drop'] >= 4 for x in e) and len(e) >= 2, 120)
    V['moderado'] = (t0, 120)
    trazo_fig(S['moderado'], 'cap38-pg-moderado-trazo.svg', t0, 120, ['flujo', 'ron', 'torax', 'abd', 'spo2'],
              'Dos minutos de la poligrafía, decúbito supino')
    t0 = elegir_ventana(S['grave'], lambda e, t: sum(1 for x in e if x['tipo'] in ('ao', 'am') and x['drop'] >= 6) >= 2, 90)
    V['grave'] = (t0, 90)
    trazo_fig(S['grave'], 'cap38-psg-grave-trazo.svg', t0, 90, ['eeg', 'emg', 'flujo', 'torax', 'abd', 'spo2'],
              'Noventa segundos de la polisomnografía')
    t0 = elegir_ventana(S['dudosa'], lambda e, t: S['dudosa']['etapa'][t + 45] in ('N1', 'N2') and
                        sum(1 for x in e if x['tipo'] == 'h' and x['drop'] < 3.0) >= 2, 90)
    V['dudosa'] = (t0, 90)
    trazo_fig(S['dudosa'], 'cap38-psg-dudosa-trazo.svg', t0, 90, ['eeg', 'emg', 'flujo', 'torax', 'abd', 'spo2'],
              'Noventa segundos de la polisomnografía')
    return S, R, V


def imprimir(S, R, V=None):
    for k, r in R.items():
        print('=====', k, PACIENTES[k]['titulo'])
        for kk, vv in r.items():
            if isinstance(vv, float):
                vv = round(vv, 2)
            print('  ', kk, '=', vv)
        print('   gravedad por IAH:', gravedad(r['IAH']), '| por REI:', gravedad(r['REI']))
    if V:
        print('ventanas', V)


if __name__ == '__main__':
    if '--indices' in sys.argv:
        S, R = todo(False)
        imprimir(S, R)
    else:
        S, R, V = todo(True)
        imprimir(S, R, V)
