"""Versión 3 de la defensa: los diagramas y gráficos se construyen con bloques NATIVOS de Slides (formas, conectores,
cajas de texto, iconos y gráficos Chart.js) en vez de imágenes, para que todo quede editable en slides.com.
Toma defensa_tfm_v2.yaml y reemplaza las diapositivas de figura por diapositivas `lienzo`. Datos: los del manuscrito
(Latex/secciones/02_cuerpo y Latex/assets/datos/*.csv)."""
import csv, yaml
from pathlib import Path
AQUI = Path(__file__).resolve().parent
DATOS = AQUI.parent / "Latex/assets/datos"
ROJO, NEG, CREMA, GRIS, BEIGE, BL = "rojo", "negro_usfq", "crema", "gris_usfq", "beige", "blanco"
SARS, EV, RSV, COM = ("#ece7f2", "#8c86c0"), ("#fde5cc", "#f08a2c"), ("#dff1da", "#4fae55"), ("#dbe8f7", "#5a9bd4")
X0, X1, Y0, Y1 = 70, 1210, 132, 636          # cuerpo del marco USFQ

def P(t, b=False, a="center"):
    t = f"<strong>{t}</strong>" if b else t
    return f'<p style="text-align:{a}">{t}</p>'
K = 1.18   # factor de letra para proyección
def caja(x, y, w, h, html, fondo=None, borde=None, grosor=0, radio=8, tam=80, color=NEG, **k):
    return dict(tipo="caja", x=x, y=y, w=w, h=h, contenido=html, fondo=fondo, borde=borde, grosor=grosor, radio=radio,
                tam=min(round(tam * K), 110) if tam < 100 else tam, color=color, **k)
def texto(x, y, w, html, tam=70, color=NEG):
    return dict(tipo="texto", x=x, y=y, w=w, html=html, tam=min(round(tam * K), 110), color=color)
def forma(x, y, w, h, tipo="rect", relleno=NEG, **k):
    return dict(tipo="forma", x=x, y=y, w=w, h=h, tipo_forma=tipo, relleno=relleno, **k)
def flecha(x1, y1, x2, y2, color=GRIS, grosor=3, **k):
    return dict(tipo="conector", x1=x1, y1=y1, x2=x2, y2=y2, color=color, grosor=grosor, **k)
def icono(x, y, lado, nombre, color=NEG, **k):
    return dict(tipo="icono", x=x, y=y, lado=lado, nombre=nombre, color=color, **k)

L = {}

# ---- Vigilancia: dos rutas
e = [texto(X0, 140, 500, P("Vigilancia clínica", True, "left"), 80)]
for i, t in enumerate(["Síntomas", "Consulta", "Diagnóstico", "Notificación"]):
    x = X0 + i * 245
    e.append(caja(x, 190, 205, 70, P(t, True), fondo=CREMA, borde=BEIGE, grosor=2, tam=70))
    if i: e.append(flecha(x - 40, 225, x - 4, 225))
e.append(caja(X0 + 4 * 245, 190, 160, 70, P("Casos registrados"), tam=62, color=GRIS))
e.append(flecha(X0 + 4 * 245 - 40, 225, X0 + 4 * 245 - 4, 225))
e.append(texto(X0, 270, 1100, P("Cada paso filtra: las infecciones leves o asintomáticas no llegan al registro", a="left"), 62, ROJO))
e.append(texto(X0, 360, 500, P("Aguas residuales", True, "left"), 80))
for i, t in enumerate(["Toda la población conectada", "Alcantarillado", "Influente de la PTAR"]):
    x = X0 + i * 300
    e.append(caja(x, 410, 250, 80, P(t, True), fondo=COM[0], borde=COM[1], grosor=2, tam=70))
    if i: e.append(flecha(x - 46, 450, x - 4, 450, color=COM[1], grosor=4))
e.append(flecha(X0 + 850, 450, X0 + 900, 450, color=COM[1], grosor=4))
e.append(caja(X0 + 905, 405, 230, 90, P("Señal poblacional", True), fondo=COM[1], color=BL, tam=75, sombra="negro"))
e.append(texto(X0, 520, 1140, P("con y sin síntomas, sin depender de la consulta (Sims & Kasprzyk-Hordern, 2020; Parkins et al., 2023)", a="left"), 55, GRIS))
L["Vigilancia en aguas residuales"] = e

# ---- Antecedente en Quitumbe: KPI + barras de genomas
e = [texto(X0, 138, 800, P("PTAR Quitumbe · Mejía Calle (2024)", True, "left"), 70)]
for i, (n, t) in enumerate([("11", "barrios de Quito"), ("75 L/s", "caudal del influente"), ("24 h", "muestreo pasivo semanal"), ("JN.1", "en el agua antes que en pacientes")]):
    x = X0 + i * 290
    e.append(caja(x, 190, 260, 150, f'<h2 style="text-align:center; color:rgb({"237, 28, 36" if n=="JN.1" else "35, 31, 32"})"><strong>{n}</strong></h2>' + P(t),
                  fondo=CREMA, borde=BEIGE, grosor=2, radio=10, tam=62, anim=("fade-in", 0.5, 0.15 * i)))
e.append(texto(X0, 380, 900, P("Genomas de SARS-CoV-2 depositados por Ecuador (Bruno et al., 2025)", True, "left"), 65))
for i, (anio, v, c) in enumerate([("2022", 5102, NEG), ("2024", 744, ROJO)]):
    y = 440 + i * 70; w = 620 * v / 5102
    e.append(texto(X0, y + 6, 90, P(anio, a="left"), 70))
    e.append(forma(X0 + 90, y, w, 46, "rect", c, radio=4, anim=("slide-right", 0.8)))
    e.append(texto(X0 + 100 + w, y + 6, 160, P(f"{v:,}".replace(",", " "), True, "left"), 70))
e.append(caja(870, 430, 340, 130, P("Sin datos ambientales de RSV ni poliovirus en Ecuador", True), borde=ROJO, grosor=3,
              estilo_borde="dashed", radio=12, color=ROJO, tam=68))
L["Antecedente en Quitumbe"] = e


# ---- dibujos de virus con bloques nativos (formas + líneas + lápiz)
import math
def _hélice(x0, x1, yc, amp, vueltas, pasos=80):
    pts = [(x0 + (x1 - x0) * k / pasos, yc + amp * math.sin(2 * math.pi * vueltas * k / pasos)) for k in range(pasos + 1)]
    return "M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts)
def dibujo(x, y, w, h, trazos, **k):
    return dict(tipo="dibujo", x=x, y=y, w=w, h=h, trazos=trazos, **k)

def virus_sars(cx, cy, R, c):
    e = []
    for k in range(14):                       # espículas S: línea con punta redonda (proteína en forma de maza)
        a = 2 * math.pi * k / 14
        e.append(dict(tipo="conector", x1=cx + (R - 4) * math.cos(a), y1=cy + (R - 4) * math.sin(a),
                      x2=cx + (R + 17) * math.cos(a), y2=cy + (R + 17) * math.sin(a), color=c[1], grosor=4,
                      inicio="none", fin="circle", estilo="solid-rounded"))
    e.append(forma(cx - R, cy - R, 2 * R, 2 * R, "circle", "#ffffff", borde=c[1], grosor=4))       # envoltura
    for k in range(7):                        # proteínas M y E en la membrana
        a = 2 * math.pi * (k + 0.5) / 7
        e.append(forma(cx + (R - 2) * math.cos(a) - 4, cy + (R - 2) * math.sin(a) - 4, 8, 8, "circle", c[1]))
    L = 2 * R                                 # ARN (+) con nucleocápside: hélice dentro
    e.append(dibujo(cx - R + 12, cy - 16, L - 24, 32, [{"d": _hélice(4, L - 28, 16, 9, 3.5), "borde": c[1], "grosor": 3}]))
    return e

def virus_enterovirus(cx, cy, R, c):
    # cápside icosaédrica vista sobre su eje de simetría 3: hexágono exterior, triángulo central y 9 facetas
    V = [(R + R * math.cos(math.pi / 6 + i * math.pi / 3), R + R * math.sin(math.pi / 6 + i * math.pi / 3)) for i in range(6)]
    T = [(R + 0.48 * R * math.cos(-math.pi / 2 + i * 2 * math.pi / 3), R + 0.48 * R * math.sin(-math.pi / 2 + i * 2 * math.pi / 3)) for i in range(3)]
    def tri(a, b, d): return f"M {a[0]:.1f} {a[1]:.1f} L {b[0]:.1f} {b[1]:.1f} L {d[0]:.1f} {d[1]:.1f} Z"
    claro, medio, oscuro = "#fde5cc", "#f7b877", "#f08a2c"
    # teselación sin huecos: un triángulo por cada lado del hexágono hacia el vértice interno más cercano, uno por cada
    # vértice exterior donde cambia ese vértice interno, y el triángulo central
    cerca = lambda p: min(range(3), key=lambda i: math.dist(p, T[i]))
    lado = [cerca(((V[k][0] + V[(k + 1) % 6][0]) / 2, (V[k][1] + V[(k + 1) % 6][1]) / 2)) for k in range(6)]
    trazos = []
    for k in range(6):
        trazos.append({"d": tri(V[k], V[(k + 1) % 6], T[lado[k]]), "relleno": medio if k % 2 else claro, "borde": "#ffffff", "grosor": 2})
        p_, n_ = lado[k - 1], lado[k]
        if p_ != n_:
            trazos.append({"d": tri(V[k], T[p_], T[n_]), "relleno": medio, "borde": "#ffffff", "grosor": 2})
    trazos.append({"d": tri(*T), "relleno": oscuro, "borde": "#ffffff", "grosor": 2})
    trazos.append({"d": "M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in V) + " Z", "relleno": "none", "borde": c[1], "grosor": 3})
    return [dibujo(cx - R, cy - R, 2 * R, 2 * R, trazos)]

def virus_rsv(cx, cy, R, c):
    rx, ry = R * 1.2, R * 0.9                  # envoltura pleomórfica (ovalada)
    e = []
    for k in range(18):                        # glicoproteínas: G (delgada, punta redonda) y F (punta cuadrada)
        a = 2 * math.pi * k / 18
        px, py = cx + rx * math.cos(a), cy + ry * math.sin(a)
        nx, ny = math.cos(a) / rx, math.sin(a) / ry; n = math.hypot(nx, ny); nx, ny = nx / n, ny / n
        largo = 15 if k % 2 else 12
        e.append(dict(tipo="conector", x1=px - 3 * nx, y1=py - 3 * ny, x2=px + largo * nx, y2=py + largo * ny, color=c[1],
                      grosor=3 if k % 2 else 2.5, inicio="none", fin="circle" if k % 2 else "square", estilo="solid-rounded"))
    e.append(forma(cx - rx, cy - ry, 2 * rx, 2 * ry, "circle", "#ffffff", borde=c[1], grosor=4))
    L = 2 * rx - 30                            # nucleocápside helicoidal del ARN (−), más apretada que la de SARS-CoV-2
    e.append(dibujo(cx - L / 2, cy - 14, L, 28, [{"d": _hélice(2, L - 2, 14, 10, 6, 140), "borde": c[1], "grosor": 2.5}]))
    return e

# ---- Por qué estos tres virus
e = []
fichas = [("SARS-CoV-2", SARS, "Coronavirus envuelto · ARN (+), 27–30 kb", "Linajes y variantes que circulan", "cog"),
          ("Enterovirus", EV, "Picornaviridae sin envoltura · ARN (+), ~7,5 kb", "Parálisis en ≤ 1 de cada 100 infecciones por polio", "octagon"),
          ("RSV", RSV, "Pneumoviridae envuelto · ARN (−), subgrupos A y B", "Alta carga en lactantes y adultos mayores", "sun")]
for i, (n, c, bio, por, ic) in enumerate(fichas):
    x = X0 + i * 385
    e.append(caja(x, 145, 355, 435, "", fondo=c[0], borde=c[1], grosor=3, radio=14))
    e.append(texto(x, 165, 355, P(n, True), 95))
    dib = {"SARS-CoV-2": virus_sars, "Enterovirus": virus_enterovirus, "RSV": virus_rsv}[n]
    e += dib(x + 177, 282, 40 if n != "Enterovirus" else 50, c)
    e.append(texto(x + 20, 355, 315, P(bio), 62))
    e.append(forma(x + 40, 450, 275, 2, "rect", c[1]))
    e.append(texto(x + 20, 470, 315, P(por, True), 64))
e.append(texto(X0, 592, 1140, P("Crits-Christoph et al., 2021; Zurbriggen et al., 2008; Hughes et al., 2022", a="left"), 50, GRIS))
L["Por qué estos tres virus"] = e

# ---- Objetivos
e = [caja(X0, 145, 1140, 90, P("Analizar la presencia molecular y la caracterización genómica de SARS-CoV-2, enterovirus y RSV en la PTAR Quitumbe", True),
          fondo=NEG, color=BL, radio=10, tam=72)]
for i, (t, d) in enumerate([("1 · Identificar", "material genético de los tres virus"), ("2 · Caracterizar", "las señales genómicas con secuenciación"),
                            ("3 · Interpretar", "frente a la vigilancia y al contexto local"), ("4 · Delimitar", "alcances y límites del análisis multipatógeno")]):
    x = X0 + i * 290
    e.append(flecha(X0 + 570, 235, x + 130, 318, color=BEIGE, grosor=3))
    e.append(forma(x, 320, 260, 14, "rect", ROJO))
    e.append(caja(x, 334, 260, 230, P(t, True) + P(d), fondo=CREMA, borde=BEIGE, grosor=2, radio=0, tam=74,
                  anim=("slide-up", 0.5, 0.2 * i)))
L["Objetivos"] = e

# ---- Flujo multipatógeno
e = []
comunes = [("Muestreo", "torpedo, 24 h"), ("Concentración", "PEG"), ("Extracción", "ARN (Zymo)")]
for i, (t, d) in enumerate(comunes):
    x = X0 + i * 190
    e.append(caja(x, 325, 175, 110, P(t, True) + P(d), fondo=COM[0], borde=COM[1], grosor=2, tam=54))
    if i: e.append(flecha(x - 15, 380, x - 2, 380, color=COM[1]))
ramas = [("SARS-CoV-2", "RT-qPCR N1/N2 · PCR ARTIC/VarSkip", SARS, 160), ("Enterovirus", "PCR anidada 5'NTR-Cre → VP1", EV, 325), ("RSV", "PCR multiplex RSV-A y RSV-B", RSV, 490)]
for t, d, c, y in ramas:
    e.append(flecha(X0 + 555, 380, 675, y + 55, color=GRIS, grosor=3))
    e.append(caja(680, y, 310, 110, P(t, True) + P(d), fondo=c[0], borde=c[1], grosor=3, tam=54))
    e.append(flecha(990, y + 55, 1025, 380, color=GRIS, grosor=3))
e.append(caja(1030, 315, 180, 130, P("Nanopore", True) + P("gel + Cq < 35") + P("R10.4.1"), fondo=NEG, color=BL, tam=54, radio=10))
e.append(texto(1020, 455, 200, P("EPI2ME → Nextclade · BLAST"), 48, GRIS))
e.append(texto(X0, 600, 600, P("Azul: etapas comunes · color: etapas propias de cada virus", a="left"), 48, GRIS))
L["Flujo multipatógeno"] = e

# ---- Selección de muestras
e = [caja(X0, 320, 170, 120, P("RT-qPCR", True) + P("control + y NTC"), fondo=COM[0], borde=COM[1], grosor=2, tam=52),
     forma(275, 300, 160, 160, "diamond", BL, borde=ROJO, grosor=3), texto(275, 358, 160, P("Cq < 35", True), 70),
     caja(475, 315, 200, 130, P("PCR de amplicones", True) + P("control + hisopados"), fondo=COM[0], borde=COM[1], grosor=2, tam=52),
     forma(705, 280, 200, 200, "diamond", BL, borde=ROJO, grosor=3), texto(725, 340, 160, P("¿Banda<br>esperada?", True), 58),
     caja(940, 325, 270, 110, P("Nanopore R10.4.1", True) + P("EPI2ME → consenso"), fondo=NEG, color=BL, tam=64, radio=10),
     caja(420, 540, 360, 70, P("Descartar o reprocesar", True), fondo=CREMA, borde=BEIGE, grosor=2, tam=70)]
for a, b in [(240, 272), (435, 477), (670, 702), (905, 937)]:
    e.append(flecha(a, 380, b, 380))
for x in (447, 900):
    e.append(texto(x - 5, 342, 40, P("sí", True), 55, "#4fae55"))
e.append(flecha(355, 460, 470, 540, color=ROJO)); e.append(flecha(805, 470, 730, 540, color=ROJO))
e.append(texto(360, 490, 60, P("no", True), 55, ROJO)); e.append(texto(790, 490, 60, P("no", True), 55, ROJO))
e.append(texto(X0, 175, 1140, P("Una muestra pasa a secuenciación solo si supera los dos filtros", a="left"), 70))
L["Selección y controles"] = e

# ---- Rendimiento por virus: barras apiladas con formas (colores exactos)
e = []
datos = [("SARS-CoV-2", 19, 17, 6), ("Enterovirus", 20, 0, 2), ("RSV", 18, 4, 0)]
colores = [("#9ecae1", "No secuenciada"), ("#fdae6b", "Secuenciada sin caracterizar"), (ROJO, "Caracterizada")]
esc = 420 / 42; base = 590
e.append(forma(100, base, 640, 2, "rect", GRIS))
for i, (v, *vals) in enumerate(datos):
    x = 140 + i * 205; y = base
    for k, val in enumerate(vals):
        if not val: continue
        h = val * esc; y -= h
        e.append(forma(x, y, 150, h, "rect", colores[k][0], anim=("slide-up", 0.5, 0.3 * i)))
        e.append(texto(x, y + h / 2 - 18, 150, P(str(val), True), 70, BL if k == 2 else NEG))
    e.append(texto(x - 20, base + 8, 190, P(v, True), 64))
for k, (c, t) in enumerate(colores):
    e.append(forma(820, 230 + k * 60, 28, 28, "rect", c, radio=4))
    e.append(texto(860, 226 + k * 60, 340, P(t, a="left"), 64))
e.append(caja(820, 430, 390, 150, P("SARS-CoV-2: 23 secuenciadas, 6 con linaje") + P("Enterovirus: 2, ambas Coxsackievirus A") + P("RSV: 4, sin subgrupo"),
              fondo=CREMA, radio=10, tam=58, alinear="left"))
L["Rendimiento por virus"] = e

# ---- Cq de SARS-CoV-2: dispersión con formas (eje invertido: arriba = más carga viral)
filas = list(csv.DictReader(open(DATOS / "cq_sars_por_semana.csv")))
col_estado = {"determinado": "#4fae55", "no_determinado": "#f08a2c", "no_secuenciado": "#5a9bd4"}
gx0, gx1, gy0, gy1, c0, c1 = 180, 1190, 150, 520, 31, 45
Xs = lambda w: gx0 + (w - 1) * (gx1 - gx0) / 41
Yc = lambda c: gy0 + (c - c0) * (gy1 - gy0) / (c1 - c0)
e = [forma(gx0, Yc(33), gx1 - gx0, Yc(36) - Yc(33), "rect", "#dff1da", radio=0)]
e.append(texto(gx1 - 360, Yc(33) + 4, 350, P("Cq de las 6 muestras con linaje (33–36)", a="right"), 48, "#4fae55"))
for c in range(32, 46, 2):
    e.append(forma(gx0 - 8, Yc(c), 8, 2, "rect", GRIS)); e.append(texto(gx0 - 70, Yc(c) - 14, 55, P(str(c), a="right"), 48, GRIS))
e.append(forma(gx0, gy0, 2, gy1 - gy0, "rect", GRIS)); e.append(forma(gx0, gy1, gx1 - gx0, 2, "rect", GRIS))
e.append(texto(X0 - 10, gy0 - 40, 110, P("Cq", True, "right"), 55))
for w in range(2, 43, 4):
    e.append(texto(Xs(w) - 30, gy1 + 8, 60, P(str(w)), 48, GRIS))
e.append(texto(gx0, gy1 + 38, gx1 - gx0, P("Semana de muestreo (abr 2025 – ene 2026)"), 50, GRIS))
for r in filas:
    for gen, tipo in (("N1", "circle"), ("N2", "diamond")):
        v = r.get(gen)
        if v not in ("", "NA", None):
            e.append(forma(Xs(int(r["semana"])) - 9, Yc(float(v)) - 9, 18, 18, tipo, col_estado.get(r["estado"], GRIS), borde=NEG, grosor=1))
for k, (t, c) in enumerate([("Linaje determinado", "#4fae55"), ("Secuenciado sin determinar", "#f08a2c"), ("No secuenciado", "#5a9bd4")]):
    e.append(forma(X0 + 110 + k * 300, 604, 20, 20, "circle", c)); e.append(texto(X0 + 138 + k * 300, 598, 260, P(t, a="left"), 50))
e.append(forma(1000, 604, 20, 20, "circle", GRIS)); e.append(texto(1024, 598, 60, P("N1", a="left"), 50))
e.append(forma(1080, 604, 20, 20, "diamond", GRIS)); e.append(texto(1104, 598, 60, P("N2", a="left"), 50))
L["Valores de Cq de SARS-CoV-2"] = e

# ---- Linajes: línea de tiempo con formas
e = [forma(120, 400, 1040, 4, "rect", BEIGE)]
lin = [(3, "JN.1", "24A"), (5, "LZ.5", "24A"), (6, "JN.1", "24A"), (7, "LZ.5", "24A"), (8, "LU.2.1.1", "24A"), (9, "LF.7.1.3", "24H")]
for i, (sem, l, cl) in enumerate(lin):
    x = 150 + (sem - 3) * 165
    col = ROJO if cl == "24H" else NEG
    e.append(forma(x - 22, 380, 44, 44, "circle", col, anim=("scale-up", 0.4, 0.2 * i)))
    e.append(texto(x - 80, 440, 160, P(f"Sem. {sem}"), 60, GRIS))
    e.append(caja(x - 85, 260 if i % 2 == 0 else 300, 170, 70, P(l, True), fondo=CREMA if cl == "24A" else ROJO, color=NEG if cl == "24A" else BL, radio=8, tam=72))
    e.append(dict(tipo="conector", x1=x, y1=(330 if i % 2 == 0 else 370), x2=x, y2=378, color=BEIGE, grosor=2, fin="none"))
e.append(forma(X0, 520, 28, 28, "rect", NEG, radio=14)); e.append(texto(X0 + 38, 516, 300, P("Clado 24A", a="left"), 64))
e.append(forma(X0 + 260, 520, 28, 28, "rect", ROJO, radio=14)); e.append(texto(X0 + 298, 516, 300, P("Clado 24H", a="left"), 64))
e.append(texto(X0, 160, 1140, P("6 linajes en las semanas 3–9 (28 abr – 9 jun 2025), todos descendientes de <strong>JN.1</strong>; desde la semana 10, sin linaje", a="left"), 68))
L["Linajes de SARS-CoV-2"] = e

# ---- Enterovirus: genoma
e = [texto(X0, 150, 900, P("Genoma de enterovirus (esquema, no a escala)", a="left"), 62, GRIS)]
segs = [("5'NTR", 95), ("VP4", 80), ("VP2", 95), ("VP3", 95), ("VP1", 105), ("P2 · P3 (no estructurales)", 490), ("3'", 50)]
x = 90; pos = {}
for n, w in segs:
    vp = n.startswith("VP")
    e.append(caja(x, 290, w, 70, P(n, vp), fondo=EV[0] if vp else "#f3f3f3", borde=EV[1] if vp else "#bbbbbb", grosor=2, radio=0, tam=62))
    pos[n] = (x, w); x += w
x1, w1 = pos["VP1"]
e.append(caja(x1, 215, w1, 40, "", borde=GRIS, grosor=3, estilo_borde="dashed", radio=4))
e.append(texto(x1 + w1 + 15, 215, 520, P("blanco esperado: VP1 (cebadores Y7/Q8)", a="left"), 60, GRIS))
x4, w4 = pos["VP4"]
e.append(forma(pos["5'NTR"][0] + 50, 395, (x4 + w4) - (pos["5'NTR"][0] + 50), 30, "rect", ROJO, radio=4, anim=("slide-right", 0.6)))
e.append(texto(X0 + 20, 440, 460, P("amplicón obtenido: posiciones 529–1049 (VP4)", True, "left"), 62, ROJO))
e.append(caja(700, 450, 510, 140, P("Coxsackievirus A", True) + P("semanas 45 y 46 · BLAST") + P("0 de 22 muestras con poliovirus"),
              fondo=CREMA, borde=BEIGE, grosor=2, radio=12, tam=66))
L["Enterovirus"] = e

# ---- RSV: embudo
e = []
for i, (n, t, w, c) in enumerate([("22", "muestras analizadas", 700, "#e8e8e8"), ("4", "secuenciadas (sem. 50, 52, 53 y 54)", 460, RSV[0]), ("0", "con subgrupo o clado", 220, CREMA)]):
    y = 160 + i * 130; x = 480 - w / 2
    e.append(caja(x, y, w, 105, f'<h2 style="text-align:center"><strong>{n}</strong></h2>', fondo=c, borde=BEIGE, grosor=2, radio=10,
                  color=ROJO if n == "0" else NEG, tam=100, anim=("fade-in", 0.5, 0.3 * i)))
    e.append(texto(x + w + 25, y + 30, 1210 - (x + w + 25), P(t, a="left"), 70))
e.append(texto(X0, 575, 1140, P("EPI2ME no alineó las lecturas con la referencia de RSV de la plataforma", a="left"), 62, GRIS))
L["Virus sincitial respiratorio"] = e

# ---- Conservación (resultados): gráfico nativo agrupado
e = [dict(tipo="grafico", x=X0, y=150, w=720, h=440, columnas=["Conservación", "Secuenciadas", "No secuenciadas"],
          filas=[["Fresca (prosp.) · Enterovirus", 2, 12], ["Fresca (prosp.) · RSV", 4, 10], ["Shield 2X (retrosp.)", 0, 8], ["PBS 1X (retrosp.)", 0, 8]],
          tipo_grafico="bar", tema="mono-dark", tam_letra=15, posicion="bottom"),
     caja(830, 200, 380, 330, P("0 de 8", True) + P("muestras retrospectivas con secuencia, en DNA/RNA Shield 2X o en PBS 1X") + P("Todas las secuencias vinieron de muestras frescas"),
          fondo=CREMA, borde=ROJO, grosor=3, radio=12, tam=70)]
L["Conservación y secuencia"] = e

# ---- Ventanas de análisis: mapa de calor con formas
estado_col = {"No analizado": "#eeeeee", "No secuenciado": "#9ecae1", "Secuenciado: no determinado": "#fdae6b",
              "Secuenciado: determinado": "#74c476", "Secuenciado: Coxsackie A": "#9e9ac8"}
grid = {}
for r in csv.DictReader(open(DATOS / "vigilancia_long.csv")):
    grid[(r["virus"], int(r["semana"]))] = r["estado"]
e = []
virus = [("SARS-CoV-2", "SARS-CoV-2"), ("Poliovirus", "Enterovirus"), ("RSV", "RSV")]
cw = 36
for panel, (w0, w1, rot) in enumerate([(1, 28, "Semanas 1–28 (abr – oct 2025)"), (29, 56, "Semanas 29–56 (nov 2025 – may 2026)")]):
    y0 = 150 + panel * 210
    for j, (vk, vn) in enumerate(virus):
        e.append(texto(X0 - 10, y0 + j * 40 + 2, 170, P(vn, a="right"), 55))
        for sem in range(w0, w1 + 1):
            e.append(forma(240 + (sem - w0) * cw, y0 + j * 40, cw - 3, 36, "rect", estado_col.get(grid.get((vk, sem), "No analizado"), "#eeeeee"), radio=3))
    for sem in range(w0, w1 + 1, 3):
        e.append(texto(240 + (sem - w0) * cw - 20, y0 + 122, cw + 40, P(str(sem)), 45, GRIS))
    e.append(texto(240, y0 + 150, 700, P(rot, a="left"), 52, GRIS))
for k, (t, c) in enumerate(estado_col.items()):
    x = X0 + (k % 3) * 380; y = 575 + (k // 3) * 32
    e.append(forma(x, y + 4, 24, 24, "rect", c, radio=3)); e.append(texto(x + 32, y, 340, P(t, a="left"), 50))
L["Ventanas de análisis"] = e

# ---- La carga viral decide: rangos de Cq con formas sobre un eje
e = []
xmin, xmax, gx0, gx1 = 24, 44, 620, 1190
X = lambda v: gx0 + (v - xmin) * (gx1 - gx0) / (xmax - xmin)
filas_cq = [("Haque et al. (2023), Dhaka: cobertura 94,2–99,8 %", 28.8, 32.1, "#4fae55"), ("Crits-Christoph et al. (2021): genomas completos", 24, 33, "#4fae55"),
            ("Esta tesis: linaje determinado", 33.1, 35.8, "#74c476"), ("Esta tesis: secuenciado sin determinar", 33.9, 42.3, "#fdae6b"),
            ("Esta tesis: no secuenciado", 34.4, 42.9, "#9ecae1")]
for i, (t, a, b, c) in enumerate(filas_cq):
    y = 170 + i * 72
    e.append(texto(X0, y + 4, 540, P(t, "Esta" in t, "right"), 58))
    e.append(forma(X(a), y, X(b) - X(a), 40, "rect", c, radio=6, borde=NEG if "Esta" in t else None, grosor=2 if "Esta" in t else 0, anim=("slide-right", 0.5, 0.15 * i)))
e.append(forma(gx0, 540, gx1 - gx0, 2, "rect", GRIS))
for v in range(24, 45, 4):
    e.append(forma(X(v) - 1, 540, 2, 10, "rect", GRIS)); e.append(texto(X(v) - 30, 552, 60, P(str(v)), 52, GRIS))
e.append(dict(tipo="conector", x1=X(35), y1=160, x2=X(35), y2=540, color=ROJO, grosor=3, fin="none", estilo="dashed"))
e.append(texto(X(35) + 8, 140, 300, P("criterio: Cq < 35", True, "left"), 55, ROJO))
e.append(texto(gx0, 590, gx1 - gx0, P("Valor de Cq (menor = más carga viral)"), 55, GRIS))
L["La carga viral decide"] = e

# ---- Enterovirus y RSV: dos gráficos nativos
e = [texto(X0, 140, 540, P("Recuperación de enterovirus (%)", True, "left"), 66),
     dict(tipo="grafico", x=X0, y=190, w=540, h=380, columnas=["Referencia", "Muestras con enterovirus (%)"], filas=[["Esta tesis (pasivo)", 9], ["OMS instrumental", 10], ["OMS puntual", 30]],
          tipo_grafico="column", tema="mono-dark", leyenda=False, tam_letra=15),
     texto(670, 140, 540, P("Recuperación del ARN (%)", True, "left"), 66),
     dict(tipo="grafico", x=670, y=190, w=540, h=380, columnas=["Forma", "Eficiencia de recuperación (%)"], filas=[["ARN desnudo", 71], ["Partículas envueltas (RSV)", 17]],
          tipo_grafico="column", tema="mono-dark", leyenda=False, tam_letra=15),
     texto(X0, 585, 1140, P("O'Reilly et al., 2020; Bubba et al., 2023; Toribio-Avedillo et al., 2024", a="left"), 50, GRIS)]
L["Enterovirus y RSV"] = e

# ---- La conservación de la muestra: gráfico nativo
e = [dict(tipo="grafico", x=X0, y=150, w=760, h=430, columnas=["Material de partida", "Cobertura mediana del genoma (%)"],
          filas=[["ARN fresco", 94], ["Extracto de ARN congelado", 88], ["Agua residual congelada", 55]], tipo_grafico="column",
          tema="mono-dark", leyenda=False, tam_letra=15),
     caja(880, 230, 330, 250, f'<h2 style="text-align:center; color:rgb(237, 28, 36)"><strong>0 de 8</strong></h2>' + P("retrospectivas de esta tesis, conservadas sobre la matriz completa, con secuencia"),
          fondo=CREMA, borde=ROJO, grosor=3, radio=12, tam=68),
     texto(X0, 590, 1140, P("Barbé et al., 2022: secuenciación Nanopore de SARS-CoV-2 en aguas residuales", a="left"), 50, GRIS)]
L["La conservación de la muestra"] = e

# ---- Limitaciones
e = []
for i, (t, d, ic) in enumerate([("Matriz ambiental", "Poco material viral y Cq altos: cobertura insuficiente", "rain"),
                                ("Conservación", "Retrospectivas sin secuencia en Shield 2X y PBS 1X", "clock"),
                                ("Diseño temporal", "Ventanas con poco solapamiento; SARS-CoV-2 no analizado en 43–56", "denied"),
                                ("Métodos", "Cebadores de VP1 que amplificaron VP4; 22 muestras de un solo sitio", "cog")]):
    x = X0 + (i % 2) * 585; y = 150 + (i // 2) * 235
    e.append(caja(x, y, 555, 205, "", fondo=CREMA, borde=BEIGE, grosor=2, radio=10))
    e.append(forma(x, y, 12, 205, "rect", ROJO))
    e.append(icono(x + 40, y + 30, 60, ic, ROJO))
    e.append(texto(x + 120, y + 30, 410, P(t, True, "left"), 80))
    e.append(texto(x + 120, y + 95, 410, P(d, a="left"), 64, GRIS))
L["Limitaciones"] = e

# ---- Conclusiones: escalera
e = []
for j, t in enumerate(["Detección", "Secuencia", "Caracterización"]):
    e.append(texto(400 + j * 230 - 115, 150, 230, P(t, True), 64))
for i, (n, c, ok, nota) in enumerate([("SARS-CoV-2", SARS, [1, 1, 1], "linajes JN.1 (24A, 24H)"), ("Enterovirus", EV, [1, 1, 1], "Coxsackievirus A"), ("RSV", RSV, [1, 1, 0], "sin subgrupo")]):
    y = 230 + i * 110
    e.append(texto(X0, y + 8, 260, P(n, True, "left"), 80))
    for j, v in enumerate(ok):
        x = 400 + j * 230
        if j:
            e.append(forma(x - 230 + 36, y + 27, 158, 8, "rect", c[1] if v else BEIGE))
        e.append(icono(x - 34, y - 3, 68, "checkmark-circle" if v else "minus-circle", c[1] if v else BEIGE, anim=("scale-up", 0.4, 0.2 * (i * 3 + j))))
    e.append(texto(930, y + 10, 280, P(nota, a="left"), 62, GRIS))
e.append(caja(X0, 560, 1140, 60, P("La carga viral y la conservación de la muestra fijaron hasta dónde llegó cada virus.", True), fondo=NEG, color=BL, radio=8, tam=66))
L["Conclusiones"] = e

# ---- Aporte y recomendaciones: chevrones armados con formas (cuerpo rect + punta triangle-right + muesca blanca)
def chevron(x, y, w, h, punta, color, primero=False, anim=None):
    """Chevrón de ancho total w: el cuerpo va de x a x+w-punta y la punta ocupa [x+w-punta, x+w]. Salvo el primero,
    lleva una muesca blanca a la izquierda donde encaja la punta del anterior. Se dibujan de derecha a izquierda."""
    # las piezas se solapan 2 px: sin solape el suavizado de bordes deja una línea fina en la unión
    e = [forma(x, y, w - punta + 2, h, "rect", color, anim=anim), forma(x + w - punta, y, punta, h, "triangle-right", color, anim=anim)]
    if not primero:
        e.append(forma(x - 2, y - 1, punta + 2, h + 2, "triangle-right", BL, anim=anim))
    return e
pasos = [("Procesar pronto", "sin conservación prolongada"), ("Seleccionar<br>por Cq", "y amplificar el genoma"),
         ("Enriquecer RSV", "antes de secuenciar"), ("Ampliar", "muestras y réplicas"), ("Cruzar", "con datos clínicos y repositorios")]
n, H, A, G = len(pasos), 160, 48, 16                  # alto, punta, separación blanca entre chevrones
W = ((X1 - X0) + (n - 1) * (A - G)) / n                # ancho total de cada chevrón para llenar el cuerpo
paso = W - A + G                                       # la punta entra en la muesca siguiente dejando G de aire
ys = 240
e = []
for i in reversed(range(n)):                           # derecha a izquierda: la punta queda sobre la muesca siguiente
    x = X0 + i * paso
    color = NEG if i % 2 == 0 else GRIS
    e += chevron(x, ys, W, H, A, color, primero=(i == 0), anim=("slide-right", 0.4, 0.15 * i))
for i, (t, d) in enumerate(pasos):
    x = X0 + i * paso
    ini = x + (A * 0.75 if i else 8)
    e.append(texto(ini, ys + H / 2 - 30, (x + W - A * 0.35) - ini, P(t, True), 64, BL))
    e.append(texto(x, ys + H + 25, W - A, P(d), 64, GRIS))
e.append(texto(X0, 560, X1 - X0, P("<em>Aporte: primera línea de base molecular y genómica multipatógeno de aguas residuales en Quito</em>"), 62, NEG))
L["Aporte y recomendaciones"] = e

# ---------------------------------------------------------------- ensamblar v3
g = yaml.safe_load(open(AQUI / "defensa_tfm_v2.yaml"))
g["titulo"] = "Defensa TFM (v3, nativa) — Análisis genómico de SARS-CoV-2, enterovirus y RSV en aguas residuales"
hechos = []
for i, d in enumerate(g["diapositivas"]):
    if d.get("titulo") in L and d["diseno"] in ("imagen", "contenido", "columnas"):
        nuevo = {"diseno": "lienzo", "numero": d.get("numero"), "titulo": d["titulo"], "elementos": L[d["titulo"]], "notas": d.get("notas")}
        g["diapositivas"][i] = {k: v for k, v in nuevo.items() if v is not None}
        hechos.append(d["titulo"])
yaml.safe_dump(g, open(AQUI / "defensa_tfm_v3.yaml", "w"), allow_unicode=True, sort_keys=False, width=140)
print(len(hechos), "diapositivas nativas:", hechos)
print("sin usar:", [k for k in L if k not in hechos])
