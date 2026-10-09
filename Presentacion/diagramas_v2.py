"""Diagramas y gráficos de la versión 2 de la defensa (menos texto, más visual).
Todos los datos salen del manuscrito (Latex/secciones/02_cuerpo) y de las fuentes que cita.
Paleta USFQ (negro, rojo, crema, gris, beige) + colores por virus del flujo multipatógeno.
Tamaño: 1 pulgada = 100 px de diapositiva; letra de 14–18 pt; sin títulos dentro de la imagen."""
import sys, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon
from pathlib import Path
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
NEG, ROJO, CREMA, GRIS, BEIGE = "#231F20", "#ED1C24", "#FAF3E9", "#4A4B4C", "#D8D4CB"
SARS, EV, RSV, COM = ("#ece7f2", "#8c86c0"), ("#fde5cc", "#f08a2c"), ("#dff1da", "#4fae55"), ("#dbe8f7", "#5a9bd4")
plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": NEG, "font.size": 15})

def lienzo(w, h, xm=100, ym=None):
    fig, ax = plt.subplots(figsize=(w, h)); ax.set_xlim(0, xm); ax.set_ylim(0, ym or xm * h / w); ax.axis("off")
    return fig, ax
def caja(ax, x, y, w, h, c, titulo=None, texto=None, fs=14, fst=15.5, alin="center", r=1.2, lw=1.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=c[0], ec=c[1], lw=lw))
    if titulo and texto:
        ax.text(x + w / 2, y + h * 0.68, titulo, ha="center", va="center", fontsize=fst, weight="bold")
        ax.text(x + w / 2, y + h * 0.32, texto, ha="center", va="center", fontsize=fs, color=GRIS, linespacing=1.2)
    elif titulo:
        ax.text(x + w / 2, y + h / 2, titulo, ha="center", va="center", fontsize=fst, weight="bold", linespacing=1.2)
def flecha(ax, x0, y0, x1, y1, c=GRIS, lw=1.8, estilo="-|>"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle=estilo, color=c, lw=lw, mutation_scale=18))
def guardar(fig, n):
    fig.savefig(OUT / n, dpi=200, bbox_inches="tight", facecolor="white", pad_inches=0.08); plt.close(fig); print(n)
def virus(ax, x, y, r, c, envuelto=True):
    ax.add_patch(Circle((x, y), r, fc=c[0], ec=c[1], lw=2.2))
    import math
    if envuelto:
        for k in range(12):
            a = 2 * math.pi * k / 12
            ax.plot([x + r * math.cos(a), x + 1.28 * r * math.cos(a)], [y + r * math.sin(a), y + 1.28 * r * math.sin(a)],
                    color=c[1], lw=2)
            ax.add_patch(Circle((x + 1.33 * r * math.cos(a), y + 1.33 * r * math.sin(a)), r * 0.09, fc=c[1], ec=c[1]))
    else:   # cápside icosaédrica sin envoltura
        pts = [(x + r * math.cos(math.pi / 6 + k * math.pi / 3), y + r * math.sin(math.pi / 6 + k * math.pi / 3)) for k in range(6)]
        ax.patches[-1].remove(); ax.add_patch(Polygon(pts, closed=True, fc=c[0], ec=c[1], lw=2.2))
        for p in pts: ax.plot([x, p[0]], [y, p[1]], color=c[1], lw=1.2)

# 1. Vigilancia clínica frente a aguas residuales
fig, ax = lienzo(11.2, 4.6)
ax.text(1, 42, "Vigilancia clínica", fontsize=17, weight="bold", va="center")
pasos = ["Síntomas", "Consulta", "Diagnóstico", "Notificación"]
for i, t in enumerate(pasos):
    caja(ax, 1 + i * 19.5, 29, 16.5, 8, (CREMA, BEIGE), t, fst=14)
    if i: flecha(ax, i * 19.5 - 2, 33, i * 19.5 + 1, 33)
ax.text(80.5, 33, "Casos\nregistrados", fontsize=15, va="center", color=GRIS)
ax.text(1, 24.5, "Cada paso filtra: las infecciones leves o asintomáticas no llegan al registro", fontsize=13, color=ROJO, style="italic")
ax.text(1, 17, "Aguas residuales", fontsize=17, weight="bold", va="center")
caja(ax, 1, 3, 26, 9, COM, "Toda la población\nconectada", fst=14.5)
caja(ax, 35, 3, 22, 9, COM, "Alcantarillado", fst=15)
caja(ax, 65, 3, 18, 9, COM, "Influente\nde la PTAR", fst=14.5)
for a, b in [(27, 35), (57, 65)]: flecha(ax, a, 7.5, b, 7.5, c=COM[1], lw=2.4)
flecha(ax, 83, 7.5, 88, 7.5, c=COM[1], lw=2.4)
ax.text(89, 7.5, "Señal\npoblacional", fontsize=15, va="center", weight="bold", color=COM[1])
ax.text(1, 0, "con y sin síntomas, sin depender de la consulta (Sims & Kasprzyk-Hordern, 2020; Parkins et al., 2023)", fontsize=12, color=GRIS)
guardar(fig, "vigilancia_dos_rutas.png")

# 2. Antecedente en Quitumbe: infografía
fig, ax = lienzo(11.2, 4.7)
kpis = [("11", "barrios de Quito"), ("75 L/s", "caudal del influente"), ("24 h", "muestreo pasivo\nsemanal"), ("JN.1", "en el agua antes\nque en pacientes")]
for i, (n, t) in enumerate(kpis):
    x = 1 + i * 24.5
    caja(ax, x, 22, 22, 18, (CREMA, BEIGE), r=1.5)
    ax.text(x + 11, 34, n, ha="center", va="center", fontsize=28, weight="bold", color=ROJO if n == "JN.1" else NEG)
    ax.text(x + 11, 26.3, t, ha="center", va="center", fontsize=14, color=GRIS, linespacing=1.15)
ax.text(1, 44, "PTAR Quitumbe · Mejía Calle (2024)", fontsize=16, weight="bold")
ax.text(1, 16.5, "Genomas de SARS-CoV-2 de Ecuador (Bruno et al., 2025)", fontsize=15, weight="bold")
for i, (anio, v) in enumerate([("2022", 5102), ("2024", 744)]):
    y = 9.5 - i * 7; w = 44 * v / 5102
    ax.add_patch(Rectangle((10, y - 2.3), w, 4.6, fc=NEG if i == 0 else ROJO, ec="none"))
    ax.text(8.5, y, anio, ha="right", va="center", fontsize=15)
    ax.text(10 + w + 1.2, y, f"{v:,}".replace(",", " "), va="center", fontsize=15, weight="bold")
ax.text(99, 6, "Sin datos ambientales\nde RSV ni poliovirus\nen Ecuador", ha="right", va="center", fontsize=15, color=ROJO, weight="bold", linespacing=1.2)
guardar(fig, "antecedente_quitumbe.png")

# 3. Tres virus
fig, ax = lienzo(11.2, 5.0)
fichas = [("SARS-CoV-2", SARS, True, "Coronavirus envuelto\nARN (+), 27–30 kb", "Linajes y variantes\nque circulan"),
          ("Enterovirus", EV, False, "Picornaviridae, sin envoltura\nARN (+), ~7,5 kb", "Parálisis en ≤ 1 de cada\n100 infecciones por polio"),
          ("RSV", RSV, True, "Pneumoviridae, envuelto\nARN (−), subgrupos A y B", "Alta carga en lactantes\ny adultos mayores")]
for i, (n, c, env, bio, por) in enumerate(fichas):
    x = 1 + i * 33.3
    caja(ax, x, 1, 31, 43, (c[0], c[1]), r=1.8, lw=2)
    ax.text(x + 15.5, 39, n, ha="center", fontsize=20, weight="bold")
    virus(ax, x + 15.5, 29, 4.6, (BLANCO := "#ffffff", c[1]), envuelto=env)
    ax.text(x + 15.5, 17.5, bio, ha="center", va="center", fontsize=13.5, color=NEG, linespacing=1.2)
    ax.plot([x + 4, x + 27], [12.5, 12.5], color=c[1], lw=1)
    ax.text(x + 15.5, 7.2, por, ha="center", va="center", fontsize=13.5, color=NEG, weight="bold", linespacing=1.2)
guardar(fig, "tres_virus.png")

# 4. Objetivos
fig, ax = lienzo(11.2, 5.0, ym=47)
caja(ax, 1, 35, 98, 10.5, (NEG, NEG), None)
ax.text(50, 40.5, "Analizar la presencia molecular y la caracterización genómica\nde SARS-CoV-2, enterovirus y RSV en la PTAR Quitumbe",
        ha="center", va="center", fontsize=14.5, color="white", weight="bold", linespacing=1.25)
objs = [("1  Identificar", "material genético\nde los tres virus"), ("2  Caracterizar", "las señales genómicas\ncon secuenciación"),
        ("3  Interpretar", "frente a la vigilancia\ny al contexto local"), ("4  Delimitar", "alcances y límites del\nanálisis multipatógeno")]
for i, (t, d) in enumerate(objs):
    x = 1 + i * 25; caja(ax, x, 4, 23, 22, (CREMA, BEIGE), r=1.5)
    ax.add_patch(Rectangle((x, 22.5), 23, 3.5, fc=ROJO, ec="none"))
    ax.text(x + 11.5, 17, t, ha="center", fontsize=16, weight="bold")
    ax.text(x + 11.5, 10, d, ha="center", va="center", fontsize=13.5, color=GRIS, linespacing=1.2)
    flecha(ax, 50, 36, x + 11.5, 26.2, c=BEIGE, lw=1.6)
guardar(fig, "objetivos.png")

# 5. Selección de muestras (decisión)
fig, ax = lienzo(11.4, 4.7)
def rombo(x, y, w, h, t):
    ax.add_patch(Polygon([(x, y + h / 2), (x + w / 2, y + h), (x + w, y + h / 2), (x + w / 2, y)], fc="white", ec=ROJO, lw=2))
    ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=14, weight="bold", linespacing=1.1)
caja(ax, 0.5, 20, 15, 10, COM, "RT-qPCR", "controles\n+ y NTC", fs=11.5)
rombo(19, 17, 16, 16, "Cq < 35")
caja(ax, 38.5, 20, 17, 10, COM, "PCR de\namplicones", None, fst=14)
ax.text(47, 17.5, "control + hisopados", ha="center", fontsize=12, color=GRIS)
rombo(58, 15, 20, 20, "¿Banda\nesperada?")
caja(ax, 80, 20, 19.5, 10, (NEG, NEG), None)
ax.text(89.75, 25, "Nanopore\nR10.4.1", ha="center", va="center", fontsize=14.5, color="white", weight="bold")
for a, b in [(15.5, 19), (35, 38.5), (55.5, 58), (78, 80)]: flecha(ax, a, 25, b, 25)
ax.text(36.5, 27, "sí", fontsize=13, color=RSV[1], weight="bold"); ax.text(78.2, 27, "sí", fontsize=13, color=RSV[1], weight="bold")
caja(ax, 30, 1.5, 36, 8, (CREMA, BEIGE), "Descartar o reprocesar", fst=14.5)
flecha(ax, 27, 17, 36, 9.5, c=ROJO); flecha(ax, 68, 15, 60, 9.5, c=ROJO)
ax.text(27.5, 12.5, "no", fontsize=13, color=ROJO, weight="bold"); ax.text(66, 12.5, "no", fontsize=13, color=ROJO, weight="bold")
ax.text(89.75, 13.5, "EPI2ME → consenso\nNextclade · BLAST", ha="center", va="center", fontsize=12.5, color=GRIS, linespacing=1.2)
flecha(ax, 89.75, 20, 89.75, 16.5)
guardar(fig, "seleccion_muestras.png")

# 6. Enterovirus: blanco esperado y obtenido (esquema no a escala)
fig, ax = lienzo(11.2, 4.4)
segs = [("5'NTR", 9), ("VP4", 5), ("VP2", 8), ("VP3", 8), ("VP1", 9), ("P2 · P3 (no estructurales)", 45), ("3'", 4)]
x = 6
pos = {}
for n, w in segs:
    col = (EV[0], EV[1]) if n in ("VP4", "VP2", "VP3", "VP1") else ("#f3f3f3", "#bbbbbb")
    ax.add_patch(Rectangle((x, 20), w, 7, fc=col[0], ec=col[1], lw=1.5)); pos[n] = (x, w)
    ax.text(x + w / 2, 23.5, n, ha="center", va="center", fontsize=13.5, weight="bold" if n.startswith("VP") else "normal")
    x += w
ax.text(6, 40, "Genoma de enterovirus (esquema, no a escala)", fontsize=14, color=GRIS)
x1, w1 = pos["VP1"]
ax.add_patch(Rectangle((x1, 29), w1, 3.5, fc="none", ec=GRIS, lw=2, ls="--"))
ax.text(x1 + w1 + 1.5, 30.8, "blanco esperado: VP1 (cebadores Y7/Q8)", va="center", fontsize=13, color=GRIS)
x4, w4 = pos["VP4"]
ax.add_patch(Rectangle((pos["5'NTR"][0] + 5, 14.5), (x4 + w4) - (pos["5'NTR"][0] + 5), 3.5, fc=ROJO, ec=ROJO))
ax.text(6, 9, "amplicón obtenido:\nposiciones 529–1049 (VP4)", va="center", fontsize=13, color=ROJO, weight="bold")
caja(ax, 56, 2, 43, 13, (CREMA, BEIGE), "Coxsackievirus A", "semanas 45 y 46 · BLAST\n0 de 22 muestras con poliovirus", fs=13, fst=17)
guardar(fig, "enterovirus_vp4.png")

# 7. RSV: embudo
fig, ax = lienzo(11.2, 4.6, ym=42.5)
etapas = [("22", "muestras analizadas", 70, "#e8e8e8"), ("4", "secuenciadas\n(sem. 50, 52, 53, 54)", 46, RSV[0]), ("0", "con subgrupo o clado", 22, CREMA)]
for i, (n, t, w, c) in enumerate(etapas):
    y = 32 - i * 11.5; x = 38 - w / 2
    ax.add_patch(FancyBboxPatch((x, y), w, 9, boxstyle="round,pad=0,rounding_size=1", fc=c, ec=BEIGE, lw=1.5))
    ax.text(38, y + 4.5, n, ha="center", va="center", fontsize=26, weight="bold", color=ROJO if n == "0" else NEG)
    ax.text(38 + w / 2 + 2, y + 4.5, t, va="center", fontsize=14.5, linespacing=1.15)
ax.text(38, 2.5, "EPI2ME no alineó las lecturas con la referencia de RSV de la plataforma", ha="center", va="center", fontsize=13.5, color=GRIS)
guardar(fig, "rsv_embudo.png")

# 8. Carga viral: rangos de Cq
fig, ax = plt.subplots(figsize=(11.2, 4.6))
filas = [("Haque et al. (2023), Dhaka:\ncobertura 94,2–99,8 %", 28.8, 32.1, "#4fae55"),
         ("Crits-Christoph et al. (2021):\ngenomas completos con Cq < 33", 24, 33, "#4fae55"),
         ("Esta tesis: linaje determinado", 33.1, 35.8, "#74c476"),
         ("Esta tesis: secuenciado sin determinar", 33.9, 42.3, "#fdae6b"),
         ("Esta tesis: no secuenciado", 34.4, 42.9, "#9ecae1")]
for i, (t, a, b, c) in enumerate(filas):
    y = len(filas) - 1 - i
    ax.barh(y, b - a, left=a, height=0.55, color=c, edgecolor=NEG if "Esta" in t else "none", lw=0.8,
            hatch="//" if "Crits" in t else None, alpha=0.9)
    ax.text(a - 0.3, y, t, ha="right", va="center", fontsize=13.5)
ax.axvline(35, color=ROJO, ls="--", lw=1.6); ax.text(35.1, 4.55, "criterio de selección: Cq < 35", color=ROJO, fontsize=12.5)
ax.set_xlim(14, 44); ax.set_ylim(-0.6, 4.9); ax.set_yticks([]); ax.set_xlabel("Valor de Cq (menor = más carga viral)", fontsize=14)
ax.set_xticks(range(24, 45, 2)); ax.tick_params(axis="x", labelsize=13)
for s_ in ("top", "right", "left"): ax.spines[s_].set_visible(False)
ax.grid(axis="x", color="#eeeeee")
guardar(fig, "cq_rangos.png")

# 9. Enterovirus y RSV: recuperación
fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.4), gridspec_kw={"wspace": 0.45})
ax = axes[0]
v = [("Esta tesis\n(pasivo)", 9, EV[1]), ("OMS\ninstrumental", 10, BEIGE), ("OMS\npuntual", 30, BEIGE)]
ax.bar([t for t, _, _ in v], [x for _, x, _ in v], color=[c for _, _, c in v], width=0.6)
for i, (_, x, _) in enumerate(v): ax.text(i, x + 0.8, f"{x} %", ha="center", fontsize=15, weight="bold")
ax.set_title("Recuperación de enterovirus", fontsize=15, weight="bold", loc="left"); ax.set_ylim(0, 35)
ax = axes[1]
v = [("ARN desnudo", 71, BEIGE), ("Partículas\nenvueltas (RSV)", 17, RSV[1])]
ax.bar([t for t, _, _ in v], [x for _, x, _ in v], color=[c for _, _, c in v], width=0.55)
for i, (_, x, _) in enumerate(v): ax.text(i, x + 2, f"{x} %", ha="center", fontsize=15, weight="bold")
ax.set_title("Eficiencia de recuperación del ARN", fontsize=15, weight="bold", loc="left"); ax.set_ylim(0, 82)
for ax in axes:
    ax.set_yticks([]); ax.tick_params(axis="x", labelsize=13)
    for s_ in ("top", "right", "left"): ax.spines[s_].set_visible(False)
guardar(fig, "recuperacion_ev_rsv.png")

# 10. Conservación
fig, ax = plt.subplots(figsize=(10.4, 4.4))
v = [("ARN fresco", 94, "#74c476"), ("Extracto de ARN\ncongelado", 88, "#a1d99b"), ("Agua residual\ncongelada", 55, "#fdae6b")]
ax.bar([t for t, _, _ in v], [x for _, x, _ in v], color=[c for _, _, c in v], width=0.55)
for i, (_, x, _) in enumerate(v): ax.text(i, x + 2, f"{x} %", ha="center", fontsize=16, weight="bold")
ax.bar(["Esta tesis:\nretrospectivas en matriz"], [0], color=ROJO)
ax.text(3, 6, "0 de 8\ncon secuencia", ha="center", fontsize=15, weight="bold", color=ROJO)
ax.set_ylim(0, 105); ax.set_yticks([]); ax.tick_params(axis="x", labelsize=13.5)
ax.set_ylabel("Cobertura mediana del genoma\n(Barbé et al., 2022)", fontsize=13.5)
for s_ in ("top", "right", "left"): ax.spines[s_].set_visible(False)
guardar(fig, "conservacion_cobertura.png")

# 11. Limitaciones
fig, ax = lienzo(11.2, 4.8)
lims = [("Matriz ambiental", "Poco material viral y Cq altos:\ncobertura insuficiente"),
        ("Conservación", "Retrospectivas sin secuencia\nen Shield 2X y PBS 1X"),
        ("Diseño temporal", "Ventanas con poco solapamiento;\nSARS-CoV-2 no analizado en 43–56"),
        ("Métodos", "Cebadores de VP1 que amplificaron\nVP4; 22 muestras de un solo sitio")]
for i, (t, d) in enumerate(lims):
    x = 1 + (i % 2) * 50; y = 25 - (i // 2) * 23
    caja(ax, x, y, 48, 20, (CREMA, BEIGE), r=1.5)
    ax.add_patch(Rectangle((x, y), 1.8, 20, fc=ROJO, ec="none"))
    ax.text(x + 5, y + 14.5, t, fontsize=17, weight="bold", va="center")
    ax.text(x + 5, y + 7, d, fontsize=14, color=GRIS, va="center", linespacing=1.25)
guardar(fig, "limitaciones.png")

# 12. Conclusiones: hasta dónde llegó cada virus
fig, ax = lienzo(11.2, 4.6)
etap = ["Detección", "Secuencia", "Caracterización"]
for j, e in enumerate(etap): ax.text(34 + j * 22, 41, e, ha="center", fontsize=16, weight="bold")
datos = [("SARS-CoV-2", SARS, [True, True, True], "linajes JN.1 (24A, 24H)"),
         ("Enterovirus", EV, [True, True, True], "Coxsackievirus A"),
         ("RSV", RSV, [True, True, False], "sin subgrupo")]
for i, (n, c, ok, nota) in enumerate(datos):
    y = 30 - i * 11
    ax.text(1, y, n, fontsize=17, weight="bold", va="center")
    for j, v in enumerate(ok):
        x = 34 + j * 22
        if j: ax.plot([x - 22 + 4, x - 4], [y, y], color=c[1] if v else BEIGE, lw=4)
        ax.add_patch(Circle((x, y), 3.3, fc=c[1] if v else "white", ec=c[1] if v else BEIGE, lw=2.5))
        ax.text(x, y, "✓" if v else "–", ha="center", va="center", fontsize=17, color="white" if v else GRIS, weight="bold")
    ax.text(83, y, nota, fontsize=14, va="center", color=GRIS)
ax.text(1, 0.5, "La carga viral y la conservación de la muestra fijaron hasta dónde llegó cada virus.", fontsize=15, color=ROJO, weight="bold")
guardar(fig, "conclusiones_escalera.png")

# 13. Recomendaciones: hoja de ruta
fig, ax = lienzo(11.2, 3.9)
recs = [("Procesar\npronto", "sin conservación\nprolongada"), ("Seleccionar\npor Cq", "y amplificar\nel genoma"),
        ("Enriquecer\nRSV", "antes de\nsecuenciar"), ("Ampliar", "muestras\ny réplicas"), ("Cruzar", "con datos clínicos\ny repositorios")]
for i, (t, d) in enumerate(recs):
    x = 1 + i * 19.8
    ax.add_patch(Polygon([(x, 12), (x + 16.5, 12), (x + 19.3, 22), (x + 16.5, 32), (x, 32), (x + 2.8, 22)] if i else
                         [(x, 12), (x + 16.5, 12), (x + 19.3, 22), (x + 16.5, 32), (x, 32)], fc=NEG if i % 2 == 0 else GRIS, ec="white", lw=2))
    ax.text(x + 9.9, 22, t, ha="center", va="center", fontsize=12.5, color="white", weight="bold", linespacing=1.1)
    ax.text(x + 9.6, 5.5, d, ha="center", va="center", fontsize=13, color=GRIS, linespacing=1.15)
guardar(fig, "hoja_de_ruta.png")
