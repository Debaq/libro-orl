#!/usr/bin/env python3
"""Copia a otoscopias/ las fotos de otoscopía de los casos del tomo II, según
otoscopias/CREDITOS-casos.md: desde los bancos (otoscopias/bancos/, que no se
versionan), en JPEG de calidad 90 con el lado mayor en 800 px, y reflejadas
horizontalmente si la columna "Reflejada" dice "sí" (una foto del otro lado).

    python3 herramientas/armar_otoscopias.py            # todas
    python3 herramientas/armar_otoscopias.py cap05_p36   # las de esos casos
"""
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

OTOS = Path(__file__).resolve().parent.parent / 'material' / 'otoscopias'


def filas():
    for linea in (OTOS / 'CREDITOS-casos.md').read_text(encoding='utf-8').splitlines():
        m = re.match(r'\|\s*(cap\S+\.jpg)\s*\|(.*)\|\s*$', linea)
        if m:
            c = [x.strip() for x in m[2].split('|')]
            yield m[1], c[2].strip('`'), c[3].lower().startswith('s')


def main(pedidos):
    hechas = 0
    for archivo, ruta, reflejada in filas():
        if pedidos and not any(archivo.startswith(p) for p in pedidos):
            continue
        im = Image.open(OTOS / 'bancos' / ruta).convert('RGB')
        im.thumbnail((800, 800))
        if reflejada:
            im = ImageOps.mirror(im)
        im.save(OTOS / archivo, quality=90)
        hechas += 1
    print(f'{hechas} otoscopías en {OTOS}')


if __name__ == '__main__':
    main(sys.argv[1:])
