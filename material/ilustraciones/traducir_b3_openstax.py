#!/usr/bin/env python3
"""Traduce al español los rótulos de las tres figuras de OpenStax del cap. B3
(B3.6 mácula, B3.7 cresta ampular, B3.11 sistema olfatorio).

Lee el original en inglés (*-en.jpg, el que bajó de Commons ya reducido),
tapa cada rótulo con blanco y escribe el español en Nimbus Sans (clon de
Helvetica, la letra de OpenStax), con la altura de mayúscula del original.
Las cajas salen de tesseract sobre el original. CC BY permite modificar:
el pie y CREDITOS_B3.md dicen "rótulos traducidos".

    python3 material/ilustraciones/traducir_b3_openstax.py
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
LETRA = "/usr/share/fonts/gsfonts/NimbusSans-Regular.otf"


def fuente(mayuscula):
    """Fuente cuya H mide `mayuscula` px de alto."""
    t = 40
    alto = ImageFont.truetype(LETRA, t).getbbox("H")
    return ImageFont.truetype(LETRA, round(t * mayuscula / (alto[3] - alto[1])))


def partir(texto, f, ancho):
    """Una línea si cabe; si no, dos, cortando donde queden más parejas."""
    if f.getlength(texto) <= ancho:
        return [texto]
    p = texto.split()
    cortes = [(" ".join(p[:i]), " ".join(p[i:])) for i in range(1, len(p))]
    return list(min(cortes, key=lambda c: max(f.getlength(c[0]), f.getlength(c[1]))))


# Cada rótulo: caja a borrar (x0, y0, x1, y1), texto (str se parte solo si
# pasa de `ancho`; lista = líneas fijas), x, alineación (l, c, r) y línea
# base de la primera línea; "gris" al final borra solo lo gris (no el color).
FIGURAS = {
    "b3-macula-openstax": dict(mayuscula=20, interlinea=29.5, rotulos=[
        ((1544, 12, 1619, 33), ["Membrana", "otolítica"], 1544, "l", 32),
        ((1595, 107, 1688, 127), ["Célula", "ciliada"], 1595, "l", 127),
        ((17, 247, 100, 267), "Mácula", 17, "l", 267),
        ((13, 335, 146, 361), ["Utrículo", "(cortado)"], 13, "l", 355),
        ((251, 335, 343, 356), "Sáculo", 251, "l", 355),
        ((828, 421, 979, 446), "Cabeza erguida", 903, "c", 441),
        ((1571, 331, 1655, 351), "Mácula", 1613, "c", 351),
        ((460, 468, 589, 494), "Endolinfa", 459, "l", 488),
        ((459, 515, 543, 535), "Mácula", 459, "l", 535),
        ((458, 564, 575, 648), ["Cristales de", "carbonato", "de calcio"], 458, "l", 584),
        ((458, 678, 533, 698), "Membrana otolítica", 458, "l", 698),
        ((459, 736, 566, 756), "Células ciliadas", 459, "l", 756),
        ((458, 814, 736, 864), ["Rama vestibular del", "nervio vestibulococlear"], 458, "l", 834),
        ((828, 843, 1048, 865), "Cabeza hacia delante", 938, "c", 864),
        ((1475, 558, 1654, 584), "Gravedad", 1564, "c", 578, "gris"),
    ]),
    "b3-cresta-openstax": dict(mayuscula=21, interlinea=31.5, rotulos=[
        ((356, 391, 604, 418), "Cabeza en reposo", 480, "c", 412),
        ((1264, 391, 1431, 418), "Cabeza en rotación", 1347, "c", 412),
        ((670, 443, 758, 470), "Cúpula", 670, "l", 464),
        ((718, 512, 819, 539), "Ampolla", 718, "l", 533),
        ((198, 770, 402, 796), "Nervio ampular", 402, "r", 791),
        ((975, 745, 1286, 835), ["Al girar la cabeza,", "la cúpula se dobla en",
                                 "sentido opuesto al giro"], 975, "l", 766),
    ]),
    "b3-olfato-openstax": dict(mayuscula=28, interlinea=41.5, ancho=295, rotulos=[
        ((862, 72, 1093, 108), "Tracto olfatorio", 862, "l", 100),
        ((864, 200, 1036, 228), "Células mitrales", 862, "l", 228),
        ((862, 255, 1156, 291), "Neuronas olfatorias", 862, "l", 283),
        ((864, 380, 1091, 408), "Hueso etmoides", 862, "l", 408),
        ((865, 556, 1108, 634), ["Filetes del", "nervio olfatorio"], 864, "l", 585),
        ((863, 671, 1155, 699), "Tejido conectivo", 862, "l", 699),
        ((862, 751, 1111, 788), "Glándula olfatoria", 862, "l", 779),
        ((862, 866, 1159, 902), "Receptor olfatorio", 862, "l", 894),
        ((864, 1008, 1002, 1035), "Dendrita", 862, "l", 1035),
        ((864, 1074, 970, 1102), "Moco", 862, "l", 1102),
        ((27, 1034, 175, 1104), ["Cilios", "olfatorios"], 27, "l", 1062),
        ((262, 1190, 741, 1260), ["Trayecto del aire inspirado", "con moléculas odorantes"],
         262, "l", 1219),
        ((424, 1298, 755, 1334), "Sistema olfatorio", 590, "c", 1326),
    ]),
}

for nombre, fig in FIGURAS.items():
    img = Image.open(AQUI / f"{nombre}-en.jpg").convert("RGB")
    d = ImageDraw.Draw(img)
    f = fuente(fig["mayuscula"])
    for caja, texto, x, alin, base, *modo in fig["rotulos"]:
        x0, y0, x1, y1 = caja
        if modo:
            # Solo los grises: la flecha roja pasa por la caja y se queda.
            px = img.load()
            for i in range(x0 - 4, x1 + 5):
                for j in range(y0 - 4, y1 + 5):
                    r, g, b = px[i, j]
                    if max(r, g, b) - min(r, g, b) < 40:
                        px[i, j] = (255, 255, 255)
        else:
            d.rectangle((x0 - 4, y0 - 4, x1 + 4, y1 + 4), fill="white")
        lineas = partir(texto, f, fig.get("ancho", 1e9)) if isinstance(texto, str) else texto
        for i, linea in enumerate(lineas):
            ancla = {"l": "ls", "c": "ms", "r": "rs"}[alin]
            d.text((x, base + i * fig["interlinea"]), linea, font=f, fill="black", anchor=ancla)
            caja_txt = d.textbbox((x, base + i * fig["interlinea"]), linea, font=f, anchor=ancla)
            if caja_txt[2] > img.width or caja_txt[0] < 0:
                print(f"  ojo: «{linea}» se sale de {nombre}")
    img.save(AQUI / f"{nombre}.jpg", quality=95, subsampling=0)
    print(nombre, img.size)
