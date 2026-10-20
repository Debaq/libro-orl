"""Latencia y amplitud de cada onda de las figuras ABR, con el caso de antes
y el de ahora, capturando con el mismo motor y la misma semilla que el libro.

Por onda da: la latencia del pico rotulado en la figura (ms) y su amplitud
medida en la curva promediada, del pico al valle de los 1,5 ms siguientes
(µV, como se mide en el cap. 12); y entre corchetes la latencia y amplitud que
puso el generador. "—" = la figura no la rotula.

Correr con el Python de LabSim, desde la raíz del libro:
  ~/micromamba/envs/labsim/bin/python .../ondas_abr.py cap12_esclerosis_multiple [...]
"""
import json
import pathlib
import sys

LIBRO = pathlib.Path(__file__).resolve().parents[3]
R = LIBRO / 'investigacion' / 'revision_abr_ehl_2026-10-19'
sys.path.insert(0, str(LIBRO / 'figuras'))
from motor import abr  # noqa: E402
from motor import datos  # noqa: E402


def caso_de(spec, nombre, antes):
    origen = spec['caso']
    if isinstance(origen, dict):
        base = R / 'casos_antes' / 'generados' if antes else LIBRO / 'casos' / 'generados'
        return datos.cargar_caso(f'archivo:{base / (nombre + ".json")}')
    if antes:
        todos = json.loads((R / 'casos_antes' / 'casos_demo.json').read_text())
        c = todos[origen.split(':')[1]]
        return dict(c.get('data', c))
    return datos.cargar_caso(origen)


def medir(c, onda):
    pico = abr._pico(c, onda)
    gen = c['ondas'].get(onda) or {}
    g = f"[{gen.get('lat', 0):.2f}/{gen.get('amp', 0):.2f}]" if gen else '[—]'
    if pico is None:
        return '—', g
    t, y = pico
    tras = [v for x, v in zip(c['x'], c['y']) if t < x <= t + 1.5]
    return f'{t:.2f}/{y - min(tras):.2f}', g


def main(nombres):
    for nombre in nombres:
        spec = json.loads((LIBRO / 'casos' / f'{nombre}.json').read_text())
        n_abr = 0
        for f in spec['figuras']:
            if f['tipo'] != 'abr':
                continue
            n_abr += 1
            fig = f'{nombre}_abr' + (f'_{n_abr}' if n_abr > 1 else '')
            if not (R / 'figuras_antes' / f'{fig}.svg').exists():
                continue
            print(f'## {fig}  ' + ', '.join(f'{k}={f[k]}' for k in ('estimulo', 'tasa', 'transductor') if k in f))
            res = {}
            for antes in (True, False):
                caso = caso_de(spec, nombre, antes)
                res[antes] = abr.capturar(caso, f.get('oidos', ['OD', 'OI']), f.get('niveles', [80, 60, 40]),
                                          estimulo=f.get('estimulo'), promediaciones=f.get('promediaciones', 2000),
                                          transductor=f.get('transductor', 'insercion'),
                                          polaridad=f.get('polaridad', 'alternada'), tasa=f.get('tasa', 21.1))
            marcar = f.get('marcar', ('I', 'III', 'V'))
            for lado in res[False]:
                for ca, cn in zip(res[True][lado], res[False][lado]):
                    celdas = []
                    for o in marcar:
                        (ma, ga), (mn, gn) = (medir(ca, o) if ca['visibles'] else ('—', '')), \
                                             (medir(cn, o) if cn['visibles'] else ('—', ''))
                        celdas.append(f'{o} {ma}{ga} → {mn}{gn}')
                    print(f'  {lado} {cn["db"]:>3g}: ' + ' | '.join(celdas))


if __name__ == '__main__':
    main(sys.argv[1:])
