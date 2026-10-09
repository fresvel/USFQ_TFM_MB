"""Figuras de resultados de la tesis, versión para diapositivas.
Misma lógica, datos (Latex/assets/datos/*.csv) y colores que Latex/assets/datos/generar_figuras.py; cambian solo el
tamaño (1 pulgada = 100 px de diapositiva), la letra (para proyección) y que no llevan título (va en la diapositiva)."""
import sys, matplotlib, matplotlib.ticker; matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch, FancyBboxPatch
from matplotlib.lines import Line2D
from pathlib import Path
D = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
sns.set_theme(style="whitegrid", rc={"font.size": 17, "axes.labelsize": 17, "xtick.labelsize": 15, "ytick.labelsize": 16,
                                     "legend.fontsize": 15, "axes.edgecolor": "#bbbbbb", "grid.color": "#e6e6e6"})
TINTA = "#231F20"
plt.rcParams.update({"text.color": TINTA, "axes.labelcolor": TINTA, "xtick.color": TINTA, "ytick.color": TINTA})
COL = {"No analizado": "#e6e6e6", "No secuenciado": "#9ecae1", "Secuenciado: sin caracterización": "#fdae6b",
       "Secuenciado: linaje determinado": "#74c476", "Secuenciado: Coxsackievirus A1": "#9e9ac8"}
ORDER = list(COL.keys())
sars = pd.read_csv(D/"sars_cov2.csv"); pol = pd.read_csv(D/"poliovirus.csv"); rsv = pd.read_csv(D/"rsv.csv")
lon = pd.read_csv(D/"vigilancia_long.csv"); cq = pd.read_csv(D/"cq_sars_por_semana.csv")
def guardar(fig, nombre):
    fig.savefig(OUT/nombre, dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig); print(nombre)

# F3 rendimiento (barras apiladas)
rows = []
for v, df in [("SARS-CoV-2", sars), ("Enterovirus", pol), ("RSV", rsv)]:
    no_seq = (~df.secuenciado).sum()
    if v == "SARS-CoV-2":
        det = (df.estado == "determinado").sum(); nod = (df.estado == "no_determinado").sum(); cox = 0
    else:
        det = 0; nod = (df.hallazgo == "no_determinado").sum(); cox = df.hallazgo.str.contains("Coxsackie").sum()
    rows.append(dict(virus=v, **{"No secuenciado": no_seq, "Secuenciado: sin caracterización": nod,
                                 "Secuenciado: linaje determinado": det, "Secuenciado: Coxsackievirus A1": cox}))
eff = pd.DataFrame(rows).set_index("virus")[ORDER[1:]]
fig, ax = plt.subplots(figsize=(6.4, 4.9)); bottom = np.zeros(len(eff))
for s_ in eff.columns:
    ax.bar(eff.index, eff[s_], bottom=bottom, color=COL[s_], label=s_.replace("Secuenciado: ", "Secuenc.: "), edgecolor="white", lw=1)
    for i, val in enumerate(eff[s_]):
        if val > 0: ax.text(i, bottom[i] + val / 2, int(val), ha="center", va="center", fontsize=16, color=TINTA)
    bottom += eff[s_].values
ax.set_ylabel("Número de muestras"); ax.grid(axis="x", visible=False)
ax.legend(bbox_to_anchor=(0.5, -0.1), loc="upper center", ncol=2, frameon=False, fontsize=13)
guardar(fig, "rendimiento.png")

# F5 Cq por semana
estado_color = {"determinado": "#74c476", "no_determinado": "#fdae6b", "no_secuenciado": "#9ecae1"}
fig, ax = plt.subplots(figsize=(11.2, 4.6))
ax.axhspan(33, 36, color="#74c476", alpha=0.12, zorder=0)
for gene, marker, lbl in [("N1", "o", "N1 (HEX)"), ("N2", "s", "N2 (FAM)")]:
    sub = cq.dropna(subset=[gene])
    ax.plot(sub.semana, sub[gene], color="#cccccc", lw=1, zorder=1)
    ax.scatter(sub.semana, sub[gene], marker=marker, s=110, c=[estado_color[e] for e in sub.estado],
               edgecolor="k", lw=0.6, zorder=3)
ax.invert_yaxis(); ax.set_xlabel("Semana de muestreo (abr 2025 – ene 2026)"); ax.set_ylabel("Valor de Cq")
ax.set_xticks(range(2, 43, 4))
h1 = [Line2D([0], [0], marker=m, color="w", markerfacecolor="#dddddd", markeredgecolor="k", markersize=11, label=l)
      for m, l in [("o", "Gen N1"), ("s", "Gen N2")]]
h2 = [Line2D([0], [0], marker="o", color="w", markerfacecolor=estado_color[k], markeredgecolor="k", markersize=12, label=v)
      for k, v in [("determinado", "Linaje determinado"), ("no_determinado", "Secuenciado, sin caracterización"),
                   ("no_secuenciado", "No secuenciado")]]
banda = [Patch(facecolor="#74c476", alpha=0.25, edgecolor="none", label="Rango con linaje (Cq 33–36)")]
ax.legend(handles=h2 + h1 + banda, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3, frameon=False, fontsize=13,
          columnspacing=1.4, handletextpad=0.4)
guardar(fig, "cq_sars.png")

# F2 linajes: abundancia por biblioteca (Freyja) y linaje del consenso, como f2_linajes_sars de la tesis (09/10/2026:
# la tesis reemplazó la línea de tiempo, que sugería una sucesión de linajes que los datos no sostienen)
fr = pd.read_csv(D/"freyja_sars.csv").sort_values(["semana", "cebadores"])
fr["etq"] = [f"{s}{'A' if c.startswith('ARTIC') else 'V'}" for s, c in zip(fr.semana, fr.cebadores)]
xs = []; x = 0; prev = None
for s_ in fr.semana:
    if prev is not None and s_ != prev: x += 0.5
    xs.append(x); x += 1; prev = s_
comp = [("QA4", "QA.4 (24H)", "#de2d26"), ("LZ5", "LZ.5 (24A)", "#3182bd"), ("otros", "Otros", "#bdbdbd")]
fig, ax = plt.subplots(figsize=(7.2, 4.6)); bottom = np.zeros(len(fr))
for col, lbl, c in comp:
    ax.bar(xs, fr[col], bottom=bottom, color=c, edgecolor="white", lw=0.8, width=0.8, label=lbl)
    bottom += fr[col].values
for xi, (_, r) in zip(xs, fr.iterrows()):
    ax.text(xi, 103, r.linaje_consenso, ha="center", va="bottom", fontsize=13, rotation=90, color=TINTA)
ax.set_xticks(xs); ax.set_xticklabels(fr.etq, fontsize=14)
ax.set_xlabel("Semana (A: ARTIC V3 · V: VarSkip)"); ax.set_ylim(0, 140); ax.set_yticks(range(0, 101, 20))
ax.set_ylabel("Abundancia relativa (%)"); ax.grid(axis="x", visible=False)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=3, frameon=False, fontsize=14)
guardar(fig, "linajes_sars.png")

# F4 conservación
pr = pd.concat([pol.assign(grupo="Enterovirus"), rsv.assign(grupo="RSV")])
cons_lbl = {"fresca": "Fresca\n(prosp.)", "shield_2x": "Shield 2X\n(retrosp.)", "pbs_1x": "PBS 1X\n(retrosp.)"}
pr["cons"] = pr.conservacion.map(cons_lbl); pr["estado_simple"] = np.where(pr.secuenciado, "Secuenciada", "No secuenciada")
order_c = list(cons_lbl.values())
fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.4), sharey=True)
for ax, (g, sub) in zip(axes, pr.groupby("grupo")):
    tab = sub.groupby(["cons", "estado_simple"]).size().unstack(fill_value=0).reindex(order_c).fillna(0)
    bottom = np.zeros(len(tab))
    for col_, c in [("No secuenciada", "#9ecae1"), ("Secuenciada", "#74c476")]:
        vals = tab[col_].values if col_ in tab else np.zeros(len(tab))
        ax.bar(tab.index, vals, bottom=bottom, color=c, label=col_, edgecolor="white", lw=1)
        for i, v in enumerate(vals):
            if v > 0: ax.text(i, bottom[i] + v / 2, int(v), ha="center", va="center", fontsize=15)
        bottom += vals
    ax.set_title(g, fontsize=17, weight="bold"); ax.grid(axis="x", visible=False); ax.tick_params(axis="x", labelsize=14)
axes[0].yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
axes[0].set_ylabel("Número de muestras"); axes[1].legend(loc="upper center", bbox_to_anchor=(-0.1, -0.2), ncol=2, fontsize=14, frameon=False)
guardar(fig, "conservacion.png")

# F1 mapa de calor temporal
virus_order = ["SARS-CoV-2", "Poliovirus", "RSV"]; virus_lbl = ["SARS-CoV-2", "Enterovirus", "RSV"]
code = {s_: i for i, s_ in enumerate(ORDER)}; grid = np.zeros((3, 56), dtype=int)
for _, r in lon.iterrows():
    grid[virus_order.index(r["virus"]), int(r["semana"]) - 1] = code.get(r["estado"], 1)
cmap = ListedColormap([COL[s_] for s_ in ORDER])
fig, axes = plt.subplots(2, 1, figsize=(11.2, 4.9))
for ax, (w0, w1, lbl) in zip(axes, [(1, 28, "Semanas 1–28 (abr – oct 2025)"), (29, 56, "Semanas 29–56 (nov 2025 – may 2026)")]):
    ax.imshow(grid[:, w0 - 1:w1], aspect="auto", cmap=cmap, vmin=0, vmax=len(ORDER) - 1,
              extent=[w0 - 0.5, w1 + 0.5, 2.5, -0.5], interpolation="nearest")
    ax.set_yticks([0, 1, 2]); ax.set_yticklabels(virus_lbl, fontsize=15)
    ax.set_xticks(range(w0, w1 + 1, 2)); ax.set_xticklabels(range(w0, w1 + 1, 2), fontsize=13)
    for x in np.arange(w0 - 0.5, w1 + 1, 1): ax.axvline(x, color="white", lw=0.8)
    for y in [0.5, 1.5]: ax.axhline(y, color="white", lw=2.5)
    ax.set_xlabel(lbl, fontsize=15); ax.grid(False)
axes[1].legend(handles=[Patch(facecolor=COL[s_], edgecolor="#888", label=s_) for s_ in ORDER],
               bbox_to_anchor=(0.5, -0.55), loc="upper center", ncol=3, frameon=False, fontsize=13)
plt.tight_layout(); guardar(fig, "heatmap_temporal.png")

# Flujo multipatógeno (etapas comunes en azul; SARS-CoV-2 violeta; enterovirus naranja; RSV verde)
C_COM, C_SARS, C_EV, C_RSV = ("#dbe8f7", "#6baed6"), ("#ece7f2", "#9e9ac8"), ("#fde5cc", "#f5a55a"), ("#dff1da", "#74c476")
fig, ax = plt.subplots(figsize=(11.4, 5.2)); ax.set_xlim(0, 120); ax.set_ylim(0, 54); ax.axis("off")
def caja(x, y, w, h, t, c, fs=12.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc=c[0], ec=c[1], lw=1.6))
    tit, *rest = t.split("\n")
    ax.text(x + w / 2, y + h / 2 + (2.3 if rest else 0), tit, ha="center", va="center", fontsize=fs + 0.5,
            color=TINTA, weight="bold")
    if rest:
        ax.text(x + w / 2, y + h / 2 - 2.6, "\n".join(rest), ha="center", va="center", fontsize=fs - 1, color=TINTA,
                linespacing=1.1)
def flecha(x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.4, mutation_scale=16))
Y = 21.5
caja(0.5, Y, 19, 12, "Muestreo\ntorpedo, 24 h", C_COM)
caja(23.5, Y, 19, 12, "Concentración\nPEG", C_COM)
caja(46.5, Y, 19, 12, "Extracción\nARN (Zymo)", C_COM)
for a, b in [(19.5, 23.5), (42.5, 46.5)]: flecha(a, Y + 6, b, Y + 6)
caja(70, 40, 27, 12, "SARS-CoV-2\nRT-qPCR N1/N2\nPCR ARTIC/VarSkip", C_SARS)
caja(70, Y, 27, 12, "Enterovirus\nPCR anidada\n5'NTR-Cre → VP1", C_EV)
caja(70, 3, 27, 12, "RSV\nPCR multiplex\nRSV-A y RSV-B", C_RSV)
for yy in (46, Y + 6, 9): flecha(65.5, Y + 6, 70, yy)
caja(100.5, Y, 19, 12, "Nanopore\ngel + Cq < 35\nR10.4.1", C_COM)
for yy in (46, Y + 6, 9): flecha(97, yy, 100.5, Y + 6)
ax.text(110, Y - 2.5, "EPI2ME\nNextclade · BLAST", ha="center", va="top", fontsize=11.5, color="#444", linespacing=1.15)
guardar(fig, "flujo_multipatogeno.png")
