"""Marcas y medidas de la ECochG (marcado automático del equipo), antes y ahora.
Correr con el Python de LabSim desde la raíz del libro:
  ~/micromamba/envs/labsim/bin/python .../marcas_ecochg.py cap09_p38 [...]
"""
import json
import pathlib
import sys

LIBRO = pathlib.Path(__file__).resolve().parents[3]
R = LIBRO / 'investigacion' / 'revision_abr_ehl_2026-10-19'
sys.path.insert(0, str(LIBRO / 'figuras'))
sys.path.insert(0, str(R / 'herramientas'))
from motor import ecochg  # noqa: E402
from ondas_abr import caso_de  # noqa: E402

for nombre in sys.argv[1:]:
    spec = json.loads((LIBRO / 'casos' / f'{nombre}.json').read_text())
    f = next(f for f in spec['figuras'] if f['tipo'] == 'ecochg')
    print('##', nombre)
    for antes in (True, False):
        caso = caso_de(spec, nombre, antes)
        for lado in ('OD', 'OI'):
            r = ecochg.registrar(caso, lado, f.get('nivel', 90))
            if r is None:
                print(f'  {"antes" if antes else "ahora"} {lado}: sin datos'); continue
            m = {k: (round(v, 2) if isinstance(v, float) else v) for k, v in r['medida'].items()}
            mk = {k: round(v, 2) for k, v in r['marcas'].items()}
            print(f'  {"antes" if antes else "ahora"} {lado}: marcas {mk} | medida {m}')
