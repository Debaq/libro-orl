"""Prueba valores de un caso para su ECochG: carga el caso (con la corrección
nueva), cambia lo que se le pida y mide como lo haría la figura del libro.

  ~/micromamba/envs/labsim/bin/python .../ajustar_ecochg.py <caso> 'OI.ecochg.sp_ap=0.55' ...

<caso> es el nombre de casos/<caso>.json; si es un paciente demo se lee de
LabSim (docs/manual/capturas/casos_demo.json), si no, de casos/generados/.
"""
import json
import pathlib
import sys

LIBRO = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(LIBRO / 'figuras'))
from motor import datos, ecochg  # noqa: E402


def cargar(nombre):
    spec = json.loads((LIBRO / 'casos' / f'{nombre}.json').read_text())
    origen = spec['caso']
    if isinstance(origen, dict):
        d = json.loads((LIBRO / 'casos' / 'generados' / f'{nombre}.json').read_text())
        return d.get('data', d)
    todos = json.loads((datos.RAIZ / 'docs/manual/capturas/casos_demo.json').read_text())
    c = todos[origen.split(':')[1]]
    return c.get('data', c)


def aplicar(caso, cambio):
    ruta, valor = cambio.split('=')
    lado, *claves = ruta.split('.')
    obj = caso['ABR'][lado]
    for k in claves[:-1]:
        obj = obj[k]
    obj[claves[-1]] = json.loads(valor)


def medir(caso):
    out = {}
    for lado in ('OD', 'OI'):
        r = ecochg.registrar(caso, lado, 90)
        if r is None:
            out[lado] = 'sin ECochG'
            continue
        m = r['medida']
        if 'base' not in m:
            out[lado] = 'sin respuesta identificable'
            continue
        f = lambda v: '—' if v is None else f'{v:.2f}'
        out[lado] = (f"PS/PA {f(m.get('sp_ap'))} áreas {f(m.get('area_ratio'))} "
                     f"PA {r['marcas'].get('PA', 0):.2f} FIN {r['marcas'].get('FIN', 0):.2f}")
    return out


if __name__ == '__main__':
    caso = cargar(sys.argv[1])
    for c in sys.argv[2:]:
        aplicar(caso, c)
    for lado, v in medir(caso).items():
        print(f'  {lado}: {v}')
