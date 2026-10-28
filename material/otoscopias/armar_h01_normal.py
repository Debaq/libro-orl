#!/usr/bin/env python3
"""Arma otoscopias/h01-normal.jpg (fig. H1.4): dos membranas normales lado a
lado, A derecha y B izquierda (las dos de Viscaino), para ver que son imágenes
en espejo. Mismo formato que las otras compuestas de H1 (CREDITOS.md):
recorte cuadrado desde el centro, 500 × 500 px, 16 px entre paneles, letra
en un círculo blanco en la esquina (copiada de h01-cerumen.jpg).

    python3 material/otoscopias/armar_h01_normal.py
"""
import pathlib
from PIL import Image, ImageDraw

AQUI = pathlib.Path(__file__).resolve().parent
BANCOS = AQUI / "bancos"
PANELES = [
    BANCOS / "viscaino/Datos/Testing/Normal/n14.jpg",  # A: OD
    BANCOS / "viscaino/Datos/Testing/Normal/n11.jpg",  # B: OI
]
LADO, SEP = 500, 16


def cuadrado(ruta):
    a = Image.open(ruta).convert("RGB")
    s = min(a.size)
    x, y = (a.width - s) // 2, (a.height - s) // 2
    return a.crop((x, y, x + s, y + s)).resize((LADO, LADO), Image.LANCZOS)


# Las letras A y B, con su círculo, salen de h01-cerumen.jpg (centro 40, 40; radio 26).
modelo = Image.open(AQUI / "h01-cerumen.jpg").convert("RGB")
mascara = Image.new("L", (56, 56), 0)
ImageDraw.Draw(mascara).ellipse((1, 1, 55, 55), fill=255)

salida = Image.new("RGB", (2 * LADO + SEP, LADO), "white")
for i, ruta in enumerate(PANELES):
    x = i * (LADO + SEP)
    salida.paste(cuadrado(ruta), (x, 0))
    salida.paste(modelo.crop((x + 12, 12, x + 68, 68)), (x + 12, 12), mascara)
salida.save(AQUI / "h01-normal.jpg", quality=90)
print(salida.size)
