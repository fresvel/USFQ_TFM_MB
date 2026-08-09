#!/usr/bin/env python3
"""Corrige el mapeo cmap de las fuentes Times del proyecto.

Las times*.ttf originales asignan el mismo glifo `semicolon` a dos codepoints:
U+003B (;) y U+037E (signo de interrogacion griego). XeLaTeX, al invertir el
cmap para construir el ToUnicode, elige el codepoint alto (U+037E), de modo que
cada ';' del PDF se EXTRAE como U+037E. Turnitin lo reporta como "caracter
reemplazado". El render es identico; solo se corrige la extraccion.

Este script elimina el alias U+037E del cmap. Reejecutar si se reemplazan las
fuentes por versiones nuevas con el mismo defecto.

Uso:  python3 patch-fonts.py            (parcha docker/fonts/*.ttf in place)
Requiere: pip install fonttools
"""
from fontTools.ttLib import TTFont
import os

FONTS = ["times.ttf", "timesbd.ttf", "timesbi.ttf", "timesi.ttf"]
BAD = 0x037E
HERE = os.path.join(os.path.dirname(__file__), "fonts")

for fn in FONTS:
    p = os.path.join(HERE, fn)
    f = TTFont(p)
    n = 0
    for st in f["cmap"].tables:
        if BAD in st.cmap:
            del st.cmap[BAD]
            n += 1
    if n:
        f.save(p)
    print(f"{fn}: U+037E eliminado de {n} subtabla(s)")
