# -*- coding: utf-8 -*-
"""MLR, CAEP y P300 de casos del libro (algunos con el bloque Central modificado para mostrar una lesión,
el sueño o el artefacto postauricular) con el motor de LabSim. `capture` en el env labsim escribe cort_data.json;
sin argumento dibuja con el python del sistema: figv/cort_<nombre>.png."""
import sys, os, json, copy
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
sys.path.insert(0, '/home/nick/Escritorio/Proyectos/libro-orl/figuras'); sys.path.insert(0, '/home/nick/Escritorio/Proyectos/LabSim')
SCR = "/tmp/claude-1000/-home-nick-Escritorio-Asignaturas-2026-Electro/ed4e4dcf-48ed-41fe-8fbc-e5fca5865bd7/scratchpad/"
DATA = SCR + "cort_data.json"
OUT = SCR + "figv/"
RUTA = "archivo:/home/nick/Escritorio/Proyectos/libro-orl/casos/generados/%s.json"
NAVY, TEAL, CORAL, ORANGE, GREY, BLUE = "#1C2238", "#1F9E89", "#E2583E", "#E8A33D", "#5B6577", "#3F6FA8"
ROJO, AZUL = "#C62F3A", "#2A5DB0"
CENTRAL_SANO = {"estado": "despierto", "tension_cervical": 0.3, "mlr_hemisferio": "ninguno", "mlr_reduccion": 0.0, "mlr_pa_retardo_ms": 0.0,
                "mlr_oido": "ninguno", "mlr_oido_reduccion": 0.0, "p1_retardo_ms": 0.0, "n1p2_reduccion": 0.0, "p300_retardo_ms": 0.0,
                "p300_reduccion": 0.0, "mmn_reduccion": 0.0, "conteo_error": 0.0}

# nombre -> (caso base, edad, cambios al bloque Central, prueba, lados, niveles, tech extra, barridos)
REGISTROS = {
    # ---- latencia media
    "mlr_acv": ("cap19_unilateral", 58, dict(mlr_hemisferio="derecho", mlr_reduccion=0.7, mlr_pa_retardo_ms=4.0), "MLR", ["OD", "OI"], [70], None, None),
    "mlr_oido": ("cap11_schwannoma", 52, dict(mlr_oido="OD", mlr_oido_reduccion=0.55), "MLR", ["OD", "OI"], [70], None, None),
    "mlr_despierta": ("cap30_nino_otitis", 7, dict(estado="despierto"), "MLR", ["OD"], [70], None, None),
    "mlr_dormida": ("cap30_nino_otitis", 7, dict(estado="dormido"), "MLR", ["OD"], [70], None, None),
    "mlr_pam_mastoides": ("cap30_mayor_ruido", 71, dict(tension_cervical=0.95), "MLR", ["OD"], [70], dict(montage="vertex_mastoid"), None),
    "mlr_pam_lobulo": ("cap30_mayor_ruido", 71, dict(tension_cervical=0.95), "MLR", ["OD"], [70], dict(montage="vertex_earlobe"), None),
    "mlr_pam_relajada": ("cap30_mayor_ruido", 71, dict(tension_cervical=0.1), "MLR", ["OD"], [70], dict(montage="vertex_mastoid"), None),
    # ---- corticales
    "caep_implante_1": ("cap19_nina", 6, dict(p1_retardo_ms=130.0, n1p2_reduccion=0.3), "CAEP", ["OD"], [70], None, None),
    "caep_implante_2": ("cap19_nina", 7, dict(p1_retardo_ms=85.0, n1p2_reduccion=0.15), "CAEP", ["OD"], [70], None, None),
    "p300_lenta": ("h10_anciano", 76, dict(p300_retardo_ms=70.0, p300_reduccion=0.45, conteo_error=0.3), "P300", ["OD", "OI"], [70], None, None),
    "p300_sana": ("h10_anciano", 76, dict(), "P300", ["OD", "OI"], [70], None, None),
}


def capturar():
    from motor.datos import cargar_caso, RAIZ, fijar_azar
    from motor import cortical as MC
    store = json.load(open(DATA)) if os.path.exists(DATA) else {}
    antes = os.getcwd(); os.chdir(RAIZ)
    try:
        from abr import cortical as C
        from motor.abr import _elegir
        for nombre, (base, edad, cambios, prueba, lados, niveles, tech, prom) in REGISTROS.items():
            if nombre in store:
                continue
            caso = cargar_caso(RUTA % base)
            caso = copy.deepcopy(caso)
            caso['edad'] = edad
            c0 = dict(CENTRAL_SANO); c0.update(caso.get('Central') or {}); c0.update(cambios); caso['Central'] = c0
            caso['id'] = "%s_%s" % (caso.get('id'), nombre)
            w = MC._ventana(caso, prueba, prom, None)
            if tech:
                w.technical = dict(w.technical, **tech); w.apply_window()
            out = {}
            for lado in lados:
                g = w.graph_r if lado == 'OD' else w.graph_l
                out[lado] = []
                for db in niveles:
                    registros = []
                    for rep in (1, 2):
                        fijar_azar('cortical', prueba, caso.get('id'), lado, db, None, *(('replica',) if rep == 2 else ()))
                        i = w.control.cb_side.findText(lado)
                        if i >= 0:
                            w.control.cb_side.setCurrentIndex(i)
                        w.control.sb_intencity.setValue(db)
                        w.control.start_capture()
                        for _ in range(6000):
                            w.capture()
                            if w.state_capture != 'record':
                                break
                        grupo = w.current_capture_curve
                        lineas = {k.split('.', 1)[1]: v for k, v in g.data.items() if k.startswith(grupo + '.')}
                        registros.append((lineas, dict(w.last_metadata or {})))
                    (r1, meta), (r2, _) = registros
                    x = [float(t) for t in next(iter(r1.values()))['ipsi_xy'][0]]
                    canales = {c: ([float(v) for v in r1[c]['ipsi_xy'][1]], [float(v) for v in r2[c]['ipsi_xy'][1]]) for c in r1}
                    extra = {}
                    for c, v in r1.items():
                        for nom, (_, y) in (v.get('overlays') or {}).items():
                            extra.setdefault(nom, {})[c] = [float(t) for t in y]
                    # marcas con las mismas reglas del libro (motor.cortical)
                    marcas = {}
                    signos = {n: s for n, _, _, s in MC.VENTANAS[prueba]}
                    for c, (y1, y2) in canales.items():
                        promedio = [(a + b) / 2 for a, b in zip(y1, y2)]
                        m = MC._marcas(prueba, x, promedio, edad)
                        rel = {n: MC._relacion(x, y1, y2, t, signos[n], C.SNAP_MS[prueba]) for n, (t, _) in m.items()}
                        if not MC._hay_respuesta(prueba, rel, edad):
                            m = {}
                        marcas[c] = {n: [t, v, rel[n]] for n, (t, v) in m.items() if rel[n] >= 1.0}
                    out[lado].append(dict(db=db, x=x, canales=canales, extra=extra, marcas=marcas, meta={k: meta.get(k) for k in ('sl', 'waves_visible', 'conteo', 'conteo_error', 'aciertos') if k in meta}))
            w.close()
            store[nombre] = dict(prueba=prueba, edad=edad, base=base, curvas=out, central=caso['Central'])
            json.dump(store, open(DATA, "w"))
            print("ok", nombre, {l: {c: {n: round(v[0], 1) for n, v in out[l][0]['marcas'][c].items()} for c in out[l][0]['marcas']} for l in out})
    finally:
        os.chdir(antes)


ESCALA_UV = {'MLR': 1.0, 'CAEP': 5.0, 'P300': 12.0, 'MMN': 2.0}
CANALES = {'MLR': ('C3', 'Cz', 'C4'), 'CAEP': ('Cz',), 'P300': ('Pz',), 'MMN': ('Fz',)}


def dibujar_uno(nombre, d, titulo=None, canales=None, ax_w=4.2, marcar=True):
    import numpy as np, matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    prueba = d['prueba']; canales = canales or CANALES[prueba]
    lados = [l for l in ("OD", "OI") if l in d['curvas']]
    filas = [(c, n) for n in range(max(len(d['curvas'][l]) for l in lados)) for c in canales]
    fig, axs = plt.subplots(1, len(lados), figsize=(ax_w * len(lados) + 0.8, max(2.8, 1.05 * len(filas) + 1.2)), dpi=200, squeeze=False)
    esc = ESCALA_UV[prueba]
    for j, lado in enumerate(lados):
        ax = axs[0][j]; col = ROJO if lado == "OD" else AZUL
        for k, (canal, n) in enumerate(filas):
            c = d['curvas'][lado][n]
            x = np.array(c['x']); y1 = np.array(c['canales'][canal][0]); y2 = np.array(c['canales'][canal][1])
            base = -k * 2.6
            for nom, porcanal in c['extra'].items():
                if canal in porcanal:
                    yo = np.array(porcanal[canal]); ax.plot(x, base + (yo - yo.mean()) / esc, color="#B8BEC8", lw=0.8)
            ax.plot(x, base + (y1 - y1.mean()) / esc, color=col, lw=1.0)
            ax.plot(x, base - 0.9 + (y2 - y2.mean()) / esc, color=col, lw=1.0, alpha=0.75)
            ax.text(-0.02 * x.max(), base + 0.15, "%s · %g dB" % (canal, c['db']), ha="right", va="center", fontsize=7.5, color=GREY)
            marcas = dict(c['marcas'].get(canal, {}))
            if prueba == 'CAEP' and not marcas and d['edad'] < 10:
                prom = (y1 + y2) / 2; sel = (x >= 120) & (x <= 320)
                i = int(np.argmax(np.where(sel, prom, -1e9))); marcas = {'P1': [float(x[i]), float(prom[i]), 9.9]}
            if marcar:
                for nom, (t, v, rel) in marcas.items():
                    i = int(np.argmin(np.abs(x - t))); yy = base + (y1[i] - y1.mean()) / esc
                    arriba = (y1[i] - y1.mean()) >= 0
                    ax.annotate(nom, (t, yy), xytext=(0, 7 if arriba else -10), textcoords="offset points", ha="center", fontsize=7, fontweight="bold", color=NAVY)
        ax.set_xlim(0, x.max()); ax.set_yticks([])
        ax.set_ylim(-len(filas) * 2.6 - 0.4, 1.6)
        ax.set_title("Oído %s" % ("derecho" if lado == "OD" else "izquierdo"), fontsize=10, loc="left", color=col, fontweight="bold")
        ax.set_xlabel("Latencia (ms)", fontsize=8, color=GREY); ax.tick_params(labelsize=7, colors=GREY)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.grid(True, axis="x", color="#E5E8EC", lw=0.6)
    # barra de escala
    axs[0][-1].plot([x.max() * 0.97] * 2, [-len(filas) * 2.6 + 0.3, -len(filas) * 2.6 + 1.3], color=GREY, lw=1.2)
    axs[0][-1].text(x.max() * 0.985, -len(filas) * 2.6 + 0.8, "%g µV" % esc, fontsize=6.5, color=GREY, va="center")
    fig.suptitle(titulo or nombre, fontsize=9.5, color=GREY, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.93)); fig.savefig(OUT + "cort_%s.png" % nombre, facecolor="white"); plt.close(fig)


def dibujar():
    store = json.load(open(DATA))
    T = {"mlr_acv": "Roberto, 58 años, ACV de la arteria cerebral media derecha hace 6 meses · MLR con click a 70 dB nHL, C3, Cz y C4, dos réplicas",
         "mlr_oido": "Hombre de 52 años con schwannoma vestibular derecho · MLR con click a 70 dB nHL, C3, Cz y C4",
         "mlr_despierta": "Natalia, 7 años, despierta · MLR con click a 70 dB nHL, OD",
         "mlr_dormida": "Natalia, 7 años, dormida · el mismo registro",
         "mlr_pam_mastoides": "Sara, 71 años, cuello tenso, referencia en la mastoides · MLR OD a 70 dB nHL",
         "mlr_pam_lobulo": "Sara, cuello tenso, referencia en el lóbulo · el mismo registro",
         "mlr_pam_relajada": "Sara, cuello relajado, referencia en la mastoides · el mismo registro",
         "caep_implante_1": "Camila, 6 años, un mes después de encender el implante · CAEP a 70 dB nHL en campo libre, Cz",
         "caep_implante_2": "Camila, 7 años, doce meses después · el mismo registro",
         "p300_lenta": "Juan Joaquín, 76 años, olvidos y dificultad para seguir conversaciones · P300 en Pz, 70 dB nHL, cuenta los raros (30 % de error)",
         "p300_sana": "Adulto de 76 años sin queja cognitiva · P300 en Pz, 70 dB nHL, cuenta bien los raros"}
    for nombre, d in store.items():
        dibujar_uno(nombre, d, T.get(nombre))
        print("ok", nombre, {l: {c: {n: round(v[0]) for n, v in d['curvas'][l][0]['marcas'][c].items()} for c in d['curvas'][l][0]['marcas']} for l in d['curvas']})


if __name__ == "__main__":
    capturar() if "capture" in sys.argv else dibujar()
