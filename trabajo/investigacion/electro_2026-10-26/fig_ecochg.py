# -*- coding: utf-8 -*-
"""ECochG en LabSim: la misma paciente (Patricia, demo:38, OI con hidrops) registrada con distintos parámetros.
Dos modos: `capture` en el env labsim (escribe ec_data.json) y dibujo con el python del sistema (figv/ec_*.png).
micromamba run -n labsim python fig_ecochg.py capture"""
import sys, os, json
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
sys.path.insert(0, '/home/nick/Escritorio/Proyectos/libro-orl/figuras'); sys.path.insert(0, '/home/nick/Escritorio/Proyectos/libro-orl/labsim')
sys.path.insert(0, '/home/nick/Escritorio/Proyectos/LabSim')
SCR = "/tmp/claude-1000/-home-nick-Escritorio-Asignaturas-2026-Electro/ed4e4dcf-48ed-41fe-8fbc-e5fca5865bd7/scratchpad/"
DATA = SCR + "ec_data.json"
OUT = SCR + "figv/"
if "capture" in sys.argv:
    from motor import abr
    from motor.datos import cargar_caso, RAIZ, fijar_azar
import numpy as np
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    MODO = "plot"
except ImportError:
    MODO = "capture"
STORE = json.load(open(DATA)) if os.path.exists(DATA) else {}
NAVY, TEAL, CORAL, ORANGE, PURPLE, GREY, BLUE = "#1C2238", "#1F9E89", "#E2583E", "#E8A33D", "#8E5BA8", "#5B6577", "#3F6FA8"
CASOS = {}
LIMITE = {'extratympanic': 0.50, 'tympanic': 0.40, 'transtympanic': 0.35, 'vertex_mastoid': None}


def captura(caso='demo:38', lado='OI', hp='5', lp='3000', tasa=11.1, pol='alternada', prom=1500, ventana=10.0, db=90,
            montage='tympanic', stim=None, tech=None, semilla=None):
    key = json.dumps([caso, lado, hp, lp, tasa, pol, prom, ventana, db, montage, stim, tech, semilla], sort_keys=True)
    if key in STORE:
        d = STORE[key]
        return dict(x=np.array(d['x']), y=np.array(d['y']), marcas=d['marcas'], medida=d['medida'], meta=d['meta'])
    if MODO != "capture":
        raise RuntimeError("falta capturar: " + key)
    from abr import ecochg
    if caso not in CASOS:
        CASOS[caso] = cargar_caso(caso)
    c = CASOS[caso]
    antes = os.getcwd(); os.chdir(RAIZ)
    try:
        w = abr._ventana(c, prom, 'insercion', tasa, 12.0)
        w.control.cb_test.setCurrentText('ECochG')      # test_changed -> protocolo ECochG
        t = dict(w.technical, montage=montage, window_ms=float(ventana), gain=100000.0)
        if tech:
            t.update(tech)
        w.technical = t
        w.apply_window()
        for combo, texto in ((w.control.cb_filter_up, hp), (w.control.cb_filter_down, lp)):
            i = combo.findText(texto); assert i >= 0, (texto, [combo.itemText(k) for k in range(combo.count())]); combo.setCurrentIndex(i)
        abr._elegir(w.control.cb_stim, stim or 'click')
        abr._elegir(w.control.cb_pol, abr.POLARIDADES[pol])
        fijar_azar('ecochg', c.get('id'), lado, db, None, 'param', hp, lp, tasa, pol, prom, ventana, montage, stim, json.dumps(tech, sort_keys=True), semilla)
        g = w.graph_r if lado == 'OD' else w.graph_l
        i = w.control.cb_side.findText(lado); w.control.cb_side.setCurrentIndex(i)
        w.control.sb_rate.setValue(tasa); w.control.sb_prom.setValue(prom)
        w.control.sb_intencity.setValue(db)
        w.control.start_capture()
        for _ in range(6000):
            w.capture()
            if w.state_capture != 'record':
                break
        v = g.data[list(g.data)[-1]]
        meta = w.last_metadata or {}
        x, y = np.array(v['ipsi_xy'][0], float), np.array(v['ipsi_xy'][1], float)
        marcas, medida = {}, {}
        try:
            marcas = ecochg.auto_marks(x, y)
            con_y = {k: (vv, float(np.interp(vv, x, y))) for k, vv in marcas.items()}
            medida = ecochg.measure_complex(x, y, con_y)
        except Exception as e:
            medida = {'error': str(e)}
        out = dict(x=x, y=y, marcas={k: float(vv) for k, vv in marcas.items()},
                   medida={k: (float(vv) if isinstance(vv, (int, float)) else vv) for k, vv in medida.items() if not isinstance(vv, (list, dict, tuple))},
                   meta={k: meta.get(k) for k in ('fsp', 'residual_noise', 'rejected', 'sweeps', 'accepted') if k in meta})
        w.close()
    finally:
        os.chdir(antes)
    STORE[key] = dict(x=out['x'].tolist(), y=out['y'].tolist(), marcas=out['marcas'], medida=out['medida'], meta=out['meta'])
    json.dump(STORE, open(DATA, "w"))
    return out


def panel(ax, c, titulo, ms_max=10, escala=None, limite=0.40, marcar=True):
    m = (c['x'] <= ms_max)
    x, y = c['x'][m], c['y'][m]
    base = c['medida'].get('base')
    if base is None:
        base = float(np.mean(y[(x >= 0) & (x <= 0.5)])) if np.any((x >= 0) & (x <= 0.5)) else float(np.mean(y))
    y = y - base
    ax.plot(x, y, color=NAVY, lw=1.5)
    ax.axhline(0, color=GREY, lw=0.6, ls=(0, (3, 3)))
    if marcar:
        for k, col in (('PS', TEAL), ('PA', CORAL)):
            lat = c['marcas'].get(k)
            if lat is None or lat > ms_max:
                continue
            j = np.argmin(np.abs(x - lat))
            ax.plot([x[j], x[j]], [0, y[j]], color=col, lw=1.2)
            ax.annotate(k, (x[j], y[j]), xytext=(0, -11 if y[j] < 0 else 6), textcoords="offset points", ha="center", fontsize=9, fontweight="bold", color=col)
        for k in ('MC',):
            lat = c['marcas'].get(k)
            if lat is not None and lat <= ms_max:
                j = np.argmin(np.abs(x - lat))
                ax.annotate("MC", (x[j], y[j]), xytext=(0, 6), textcoords="offset points", ha="center", fontsize=9, fontweight="bold", color=PURPLE)
    ax.set_title(titulo, fontsize=10, loc="left", color=NAVY, fontweight="bold")
    ax.set_xlim(0, ms_max); ax.set_yticks([])
    if escala:
        ax.set_ylim(*escala)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=8, colors=GREY)


def rotulo(c, limite):
    m = c['medida']
    r, a, lat = m.get('sp_ap'), m.get('area_ratio'), m.get('ap_lat')
    partes = []
    if r is not None:
        partes.append("PS/PA %s" % ("%.2f" % r).replace('.', ','))
    if a is not None:
        partes.append("áreas %s" % ("%.2f" % a).replace('.', ','))
    if lat is not None:
        partes.append("PA %s ms" % ("%.2f" % lat).replace('.', ','))
    if not partes:
        partes.append("sin complejo medible")
    col = CORAL if (r is not None and limite and r > limite) else GREY
    return " · ".join(partes), col


def figura(nombre, condiciones, titulo, ncol=None, ms_max=10, propia=False, marcar=True):
    n = len(condiciones); ncol = ncol or n
    nrow = (n + ncol - 1) // ncol
    if MODO == "capture":
        for lab, kw in condiciones:
            kw = {k: v for k, v in kw.items() if k != 'marcar'}
            c = captura(**kw); print("cap", nombre, lab, c['marcas'], c['medida'], c['meta'])
        return
    fig, axs = plt.subplots(nrow, ncol, figsize=(3.3 * ncol, 2.4 * nrow + 0.4), dpi=200, squeeze=False)
    caps = []
    for lab, kw in condiciones:
        kw = dict(kw); mk = kw.pop('marcar', marcar)
        caps.append((lab, captura(**kw), dict(kw, _marcar=mk)))

    def centrada(c, mm):
        mk = (c['x'] <= mm)
        b = c['medida'].get('base')
        b = b if b is not None else float(np.mean(c['y'][mk]))
        return c['y'][mk] - b
    lim = max(np.max(np.abs(centrada(c, ms_max if not isinstance(ms_max, (list, tuple)) else ms_max[k]))) for k, (_, c, _) in enumerate(caps)) * 1.2
    for k, (lab, c, kw) in enumerate(caps):
        ax = axs[k // ncol][k % ncol]
        mm = ms_max[k] if isinstance(ms_max, (list, tuple)) else ms_max
        panel(ax, c, lab, ms_max=mm, escala=None if propia else (-lim, lim), marcar=kw['_marcar'])
        ax.set_xlabel("ms", fontsize=8, color=GREY)
        txt, col = rotulo(c, LIMITE.get(kw.get('montage', 'tympanic')))
        if not kw['_marcar']:
            txt, col = "sin marcar", GREY
        ax.text(0.98, 0.04, txt, transform=ax.transAxes, ha="right", fontsize=8, color=col)
    for k in range(n, nrow * ncol):
        axs[k // ncol][k % ncol].axis("off")
    fig.suptitle(titulo, fontsize=10.5, color=GREY, x=0.01, ha="left")
    fig.tight_layout(); fig.savefig(OUT + nombre, facecolor="white"); plt.close(fig)
    print("ok", nombre, [(lab, c['medida'].get('sp_ap'), c['medida'].get('area_ratio'), c['medida'].get('ap_lat')) for lab, c, _ in caps])


NEURO = 'archivo:/home/nick/Escritorio/Proyectos/libro-orl/casos/generados/cap13_neuropatia.json'

if __name__ == "__main__":
    que = [a for a in sys.argv[1:] if a != "capture"] or ["oidos", "hp", "nivel", "pol", "electrodo", "ventana", "barridos", "burst", "tasa", "peat", "neuro"]
    if "oidos" in que:
        figura("ec_oidos.png", [("OD (referencia)", dict(lado='OD')), ("OI (hidrops)", dict(lado='OI'))],
               "Patricia · click alternado a 90 dB nHL, timpánico, 5 a 3.000 Hz · marcado automático del equipo", ncol=2)
    if "hp" in que:
        figura("ec_pasa_alto.png", [("Pasa alto 5 Hz (ECochG)", dict(hp='5')), ("Pasa alto 100 Hz (el del PEATC)", dict(hp='100')), ("Pasa alto 250 Hz", dict(hp='250'))],
               "Patricia, OI (hidrops) · el mismo oído con tres pasa altos (pasa bajo 3.000 Hz)")
    if "nivel" in que:
        figura("ec_nivel.png", [("90 dB nHL", dict(db=90)), ("70 dB nHL", dict(db=70)), ("50 dB nHL", dict(db=50))],
               "Patricia, OI (hidrops) · el PS necesita nivel: a 70 o 50 dB la razón no tiene límite validado")
    if "pol" in que:
        figura("ec_polaridad.png", [("Rarefacción", dict(pol='rarefaccion')), ("Condensación", dict(pol='condensacion')), ("Alternada", dict(pol='alternada'))],
               "Patricia, OI · las tres polaridades: la microfónica se invierte y la alternada la cancela", ms_max=5, marcar=False)
    if "electrodo" in que:
        figura("ec_electrodo.png", [("Conducto (TIPtrode) · límite 0,50", dict(montage='extratympanic')), ("Timpánico · límite 0,40", dict(montage='tympanic')), ("Transtimpánico · límite 0,35", dict(montage='transtympanic'))],
               "Patricia, OI · los tres electrodos (cada panel con su escala): cambia el tamaño y el límite", propia=True)
    if "ventana" in que:
        figura("ec_ventana.png", [("Ventana de 6 ms", dict(ventana=6.0)), ("Ventana de 10 ms", dict(ventana=10.0))],
               "Patricia, OI · ventana de 6 y de 10 ms: el retorno a la base está a 8,8 ms", ncol=2, ms_max=[6, 10])
    if "barridos" in que:
        figura("ec_barridos.png", [("Conducto · 300 barridos", dict(montage='extratympanic', prom=300)), ("Conducto · 1.500 barridos", dict(montage='extratympanic', prom=1500)), ("Timpánico · 300 barridos", dict(montage='tympanic', prom=300)), ("Timpánico · 1.500 barridos", dict(montage='tympanic', prom=1500))],
               "Patricia, OI · electrodo y barridos (cada panel con su escala): lejos y con pocos, el PA se hunde en el ruido", ncol=2, propia=True)
    if "burst" in que:
        figura("ec_burst.png", [("Click · ventana 10 ms", dict(stim='click')), ("Burst 1 kHz (1-10-1 ms) · ventana 20 ms", dict(stim='Burst 1 kHz', ventana=20.0, tech={'burst_envelope': 'ms-1-10-1'}))],
               "Patricia, OI · click y tone burst (cada panel con su escala): con burst el PS es una meseta", ncol=2, ms_max=[10, 20], propia=True)
    if "tasa" in que:
        figura("ec_tasa.png", [("11,1 estímulos/s", dict(tasa=11.1)), ("91,1 estímulos/s", dict(tasa=91.1))],
               "Patricia, OI · tasa de rutina y tasa alta: el PA se corre y se achica", ncol=2)
    if "peat" in que:
        figura("ec_montaje_peat.png", [("Electrodo timpánico", dict(montage='tympanic')), ("Montaje Cz-mastoides (el del PEATC)", dict(montage='vertex_mastoid', marcar=False))],
               "Patricia, OI · prueba ECochG con montaje del PEATC: sale un PEATC, sin PS", ncol=2, propia=True)
    if "neuro" in que:
        figura("ec_neuropatia.png", [("Rarefacción", dict(caso=NEURO, lado='OD', pol='rarefaccion')), ("Condensación", dict(caso=NEURO, lado='OD', pol='condensacion')), ("Alternada", dict(caso=NEURO, lado='OD', pol='alternada'))],
               "Esther (neuropatía), OD · click a 90 dB nHL, timpánico: la microfónica se invierte y no hay PA detrás", ms_max=5, marcar=False)
