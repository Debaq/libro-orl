# -*- coding: utf-8 -*-
"""ASSR de los casos del libro con el modelo de LabSim (abr/assr.py): registro con la estrategia automática
hasta encerrar el umbral de las ocho portadoras. `capture` en el env labsim escribe assr_data.json;
sin argumento, dibuja con el python del sistema: figv/assr_<caso>_grilla.png, _espectro.png, _audiograma.png."""
import sys, os, json
sys.path.insert(0, '/home/nick/Escritorio/Proyectos/libro-orl/figuras'); sys.path.insert(0, '/home/nick/Escritorio/Proyectos/LabSim')
SCR = "/tmp/claude-1000/-home-nick-Escritorio-Asignaturas-2026-Electro/ed4e4dcf-48ed-41fe-8fbc-e5fca5865bd7/scratchpad/"
DATA = SCR + "assr_data.json"
OUT = SCR + "figv/"
CASOS = ["cap17_rubeola_congenita", "cap17_cmv_congenito", "cap17_efusion_neonatal", "cap17_asfixia_perinatal", "cap19_sobre_real", "cap19_nina"]
RUTA = "/home/nick/Escritorio/Proyectos/libro-orl/casos/generados/%s.json"
FRS = [500, 1000, 2000, 4000]
NAVY, TEAL, CORAL, ORANGE, GREY, BLUE, LIGHT = "#1C2238", "#1F9E89", "#E2583E", "#E8A33D", "#5B6577", "#3F6FA8", "#EEF3F6"
ROJO, AZUL = "#C62F3A", "#2A5DB0"


def capturar():
    from motor.datos import cargar_caso, RAIZ
    import numpy as np
    antes = os.getcwd(); os.chdir(RAIZ)
    try:
        from abr import assr
        from abr.ABR_generator import case_quality
        store = json.load(open(DATA)) if os.path.exists(DATA) else {}
        for nombre in CASOS:
            if nombre in store:
                continue
            d = cargar_caso('archivo:' + RUTA % nombre)
            abrs = d['ABR']
            ref = abrs.get('OD') or abrs.get('OI')
            rec = assr.Recording({'OD': abrs.get('OD'), 'OI': abrs.get('OI')}, patient=d, quality=case_quality(ref),
                                 inquietud=float(ref.get('inquietud') or 0.0), reject_uv=20.0)
            assr.MAX_EPOCHS = 3000
            rec.reset()
            for c in assr.channels():
                rec.set_level(c, 90 if 'rubeola' in nombre else 60)
            pasos = 0
            while not rec.all_done() and rec.n < assr.MAX_EPOCHS:
                rec.step(10); rec.auto_step(); pasos += 1
            snap = rec.snapshot()
            # historial completo de cada portadora (niveles, n, detectado, concluyente, estadística)
            hist = {assr.channel_key(c): list(rec.history[c]) + [dict(level=rec.levels[c], abierto=True, **rec.stats(c))] for c in assr.channels() if rec.active(c)}
            espectros = {}
            for c in assr.channels():
                if not rec.active(c):
                    continue
                medio, n = rec.mean_spectrum(c)
                espectros[assr.channel_key(c)] = dict(nivel=rec.levels[c], n=int(n), bin=int(assr.FM_BIN[c[0]][assr.CARRIERS.index(c[1])]),
                                                       amp=[float(abs(v)) * 1000.0 for v in medio])
            store[nombre] = dict(snapshot=snap, historial=hist, espectros=espectros, hl={assr.channel_key(c): rec.hl[c] for c in assr.channels()},
                                 phys={assr.channel_key(c): rec.phys[c] for c in assr.channels()}, freqs=[float(f) for f in rec.freqs], n=rec.n, rechazadas=rec.rejected,
                                 aerea=d.get('Aerea'), edad=d.get('edad'), edad_horas=d.get('edad_horas'), nombre=(d.get('paciente_snapshot') or {}).get('nombre'))
            json.dump(store, open(DATA, "w"), default=lambda o: o if isinstance(o, (int, float, str, list, dict, bool)) or o is None else str(o))
            print("ok", nombre, "épocas", rec.n, {k: (v['umbral_hl'], v['umbral_ehl'], v['hl_caso']) for k, v in snap['canales'].items()})
    finally:
        os.chdir(antes)


def dibujar():
    import numpy as np, matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    store = json.load(open(DATA))
    for nombre, d in store.items():
        canales = d['snapshot']['canales']; hist = d['historial']
        lados = d['snapshot']['oidos']
        # ---------- grilla de detección
        niveles = sorted({h['level'] for k in hist for h in hist[k]}, reverse=True)
        fig, axs = plt.subplots(1, len(lados), figsize=(4.0 * len(lados) + 0.6, 0.42 * len(niveles) + 1.6), dpi=200, squeeze=False)
        for j, lado in enumerate(lados):
            ax = axs[0][j]
            for i, f in enumerate(FRS):
                k = "%s:%d" % (lado, f)
                if k not in hist:
                    continue
                por = {}
                for h in hist[k]:
                    por.setdefault(h['level'], []).append(h)
                umbral = canales[k]['umbral_hl']
                for r, nivel in enumerate(niveles):
                    if nivel not in por:
                        continue
                    hs = por[nivel]
                    det = any(h.get('detected') for h in hs); conc = any(h.get('conclusive') for h in hs)
                    col = TEAL if det else (GREY if conc else ORANGE)
                    ax.add_patch(Rectangle((i, r), 1, 1, facecolor=col, edgecolor="white", lw=1.5))
                    p = min((h.get('p') if h.get('p') is not None else h.get('p_f', 1.0)) for h in hs) if hs else None
                    txt = ("p < 0,001" if p is not None and p < 0.001 else ("p = %.3f" % p).replace(".", ",")) if p is not None else ""
                    if not det and not conc:
                        txt = "no concl."
                    elif not det:
                        txt = "ausente"
                    ax.text(i + 0.5, r + 0.5, txt, ha="center", va="center", fontsize=7, color="white", fontweight="bold")
                    if det and umbral == nivel:
                        ax.add_patch(Rectangle((i, r), 1, 1, facecolor="none", edgecolor=NAVY, lw=2.5))
            ax.set_xlim(0, 4); ax.set_ylim(len(niveles), 0)
            ax.set_xticks([i + 0.5 for i in range(4)]); ax.set_xticklabels(["500", "1.000", "2.000", "4.000"], fontsize=8, color=GREY)
            ax.set_yticks([r + 0.5 for r in range(len(niveles))]); ax.set_yticklabels(["%d" % n for n in niveles], fontsize=8, color=GREY)
            ax.set_title("Oído %s" % ("derecho" if lado == "OD" else "izquierdo"), fontsize=10, loc="left", color=ROJO if lado == "OD" else AZUL, fontweight="bold")
            ax.set_xlabel("Portadora (Hz)", fontsize=8, color=GREY)
            if j == 0:
                ax.set_ylabel("Nivel (dB nHL)", fontsize=8, color=GREY)
            for s in ax.spines.values():
                s.set_visible(False)
            ax.tick_params(length=0)
        fig.suptitle("Detección por oído, portadora y nivel · verde: respuesta clara · gris: ausente · borde: umbral", fontsize=9, color=GREY, x=0.01, ha="left")
        fig.tight_layout(rect=(0, 0, 1, 0.94)); fig.savefig(OUT + "assr_%s_grilla.png" % nombre, facecolor="white"); plt.close(fig)
        # ---------- espectro
        freqs = np.array(d['freqs'])
        fig, axs = plt.subplots(1, len(lados), figsize=(4.2 * len(lados) + 0.4, 2.6), dpi=200, squeeze=False)
        for j, lado in enumerate(lados):
            ax = axs[0][j]
            bins = {}
            for f in FRS:
                e = d['espectros'].get("%s:%d" % (lado, f))
                if e:
                    bins[f] = e
            if not bins:
                continue
            e = bins[2000]
            amp = np.array(e['amp'])
            m = (freqs >= 70) & (freqs <= 115)
            ax.plot(freqs[m], amp[m], color=GREY, lw=0.9)
            for f, ee in bins.items():
                b = ee['bin']
                ax.plot([freqs[b]], [amp[b]], "o", color=TEAL if canales["%s:%d" % (lado, f)]['umbral_hl'] is not None else CORAL, ms=5)
                ax.annotate("%s Hz\n%d dB" % (("%d" % f) if f < 1000 else ("%d.000" % (f // 1000)), ee['nivel']), (freqs[b], amp[b]), xytext=(0, 5), textcoords="offset points", ha="center", fontsize=6, color=NAVY)
            ax.set_title("Oído %s · espectro promedio del EEG (%d épocas)" % ("derecho" if lado == "OD" else "izquierdo", e['n']), fontsize=9, loc="left", color=ROJO if lado == "OD" else AZUL, fontweight="bold")
            ax.set_xlabel("Frecuencia (Hz)", fontsize=8, color=GREY); ax.set_ylabel("nV", fontsize=8, color=GREY)
            ax.tick_params(labelsize=7, colors=GREY)
            for s in ("top", "right"):
                ax.spines[s].set_visible(False)
        fig.suptitle("Las cuatro líneas de cada oído en el espectro: cada una en su frecuencia de modulación", fontsize=9, color=GREY, x=0.01, ha="left")
        fig.tight_layout(rect=(0, 0, 1, 0.9)); fig.savefig(OUT + "assr_%s_espectro.png" % nombre, facecolor="white"); plt.close(fig)
        # ---------- audiograma: umbral ASSR (nHL), estimado (eHL) y audiometría del caso
        fig, axs = plt.subplots(1, len(lados), figsize=(3.6 * len(lados) + 0.4, 3.2), dpi=200, squeeze=False)
        aerea = d.get('aerea')
        for j, lado in enumerate(lados):
            ax = axs[0][j]; col = ROJO if lado == "OD" else AZUL
            x = [0, 1, 2, 3]
            nhl = [canales["%s:%d" % (lado, f)]['umbral_hl'] for f in FRS]
            ehl = [canales["%s:%d" % (lado, f)]['umbral_ehl'] for f in FRS]
            if aerea:
                idx = {500: 2, 1000: 3, 2000: 5, 4000: 7}
                cond = [aerea[idx[f]][0 if lado == "OD" else 1] for f in FRS]
                ax.plot(x, cond, "-", color=GREY, lw=1.2, label="audiometría del caso")
                ax.plot(x, cond, "o" if lado == "OD" else "x", color=GREY, ms=6, mfc="white")
            xs = [xi for xi, v in zip(x, nhl) if v is not None]
            ax.plot(xs, [v for v in nhl if v is not None], "s", color=col, ms=6, mfc="white", label="umbral ASSR (dB nHL)")
            ax.plot(xs, [v for v in ehl if v is not None], "s-", color=col, ms=6, label="estimado (dB eHL)")
            for xi, v in zip(x, nhl):
                if v is None:
                    ax.annotate("sin\nrespuesta", (xi, 110), ha="center", fontsize=7, color=col)
            ax.set_ylim(120, -10); ax.set_xlim(-0.4, 3.4)
            ax.set_xticks(x); ax.set_xticklabels(["500", "1k", "2k", "4k"], fontsize=8, color=GREY)
            ax.set_yticks(range(0, 121, 20)); ax.tick_params(labelsize=7, colors=GREY)
            ax.grid(True, color="#E5E8EC", lw=0.6)
            ax.set_title("Oído %s" % ("derecho" if lado == "OD" else "izquierdo"), fontsize=10, loc="left", color=col, fontweight="bold")
            ax.set_xlabel("Hz", fontsize=8, color=GREY)
            if j == 0:
                ax.set_ylabel("dB", fontsize=8, color=GREY)
                ax.legend(fontsize=6.5, loc="lower left", frameon=False)
            for s in ("top", "right"):
                ax.spines[s].set_visible(False)
        corr = d['snapshot']['correccion']
        fig.suptitle("Umbral del ASSR y audiograma estimado · corrección %s dB en 500 / 1.000 / 2.000 / 4.000 Hz" % " / ".join("%g" % corr[str(f)] for f in FRS), fontsize=9, color=GREY, x=0.01, ha="left")
        fig.tight_layout(rect=(0, 0, 1, 0.93)); fig.savefig(OUT + "assr_%s_audiograma.png" % nombre, facecolor="white"); plt.close(fig)
        print("ok", nombre, {k: (v['umbral_hl'], v['umbral_ehl'], v['hl_caso']) for k, v in canales.items()})


if __name__ == "__main__":
    if "capture" in sys.argv:
        capturar()
    else:
        dibujar()
