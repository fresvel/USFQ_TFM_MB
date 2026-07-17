"""Genera las figuras del capitulo de analisis a partir de los datasets CSV.
Uso: python generar_figuras.py  (desde la raiz del repo)"""
import matplotlib; matplotlib.use("Agg")
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from pathlib import Path

sns.set_theme(style="whitegrid", font_scale=0.95)
D = Path("Latex/assets/datos")
OUT = Path("Latex/assets/figuras/resultados"); OUT.mkdir(parents=True, exist_ok=True)

COL = {
    "No analizado":               "#e6e6e6",
    "No secuenciado":             "#9ecae1",
    "Secuenciado: no determinado":"#fdae6b",
    "Secuenciado: determinado":   "#74c476",
    "Secuenciado: Coxsackie A":   "#9e9ac8",
}
ORDER = list(COL.keys())

sars = pd.read_csv(D/"sars_cov2.csv")
pol  = pd.read_csv(D/"poliovirus.csv")
rsv  = pd.read_csv(D/"rsv.csv")
lon  = pd.read_csv(D/"vigilancia_long.csv")

# ---------- F1: mapa de calor temporal semana x virus (dos paneles apilados) ----------
virus_order = ["SARS-CoV-2","Poliovirus","RSV"]   # claves de vigilancia_long.csv: no tocar
virus_lbl   = ["SARS-CoV-2","Enterovirus","RSV"]  # etiquetas mostradas en el eje
code = {s:i for i,s in enumerate(ORDER)}
grid = np.zeros((3,56), dtype=int)  # default 0 = No analizado
for _,r in lon.iterrows():
    vi = virus_order.index(r["virus"]); wk=int(r["semana"])-1
    grid[vi,wk] = code.get(r["estado"], 1)
cmap = ListedColormap([COL[s] for s in ORDER])
fig, axes = plt.subplots(2,1, figsize=(11,5.4))
segments = [(1,28,"Semanas 1–28 (abr – oct 2025)"),
            (29,56,"Semanas 29–56 (nov 2025 – may 2026)")]
for ax,(w0,w1,lbl) in zip(axes, segments):
    sub = grid[:, w0-1:w1]
    ax.imshow(sub, aspect="auto", cmap=cmap, vmin=0, vmax=len(ORDER)-1,
              extent=[w0-0.5, w1+0.5, 2.5, -0.5], interpolation="nearest")
    ax.set_yticks([0,1,2]); ax.set_yticklabels(virus_lbl)
    ax.set_xticks(range(w0, w1+1)); ax.set_xticklabels(range(w0,w1+1), fontsize=8)
    for x in np.arange(w0-0.5, w1+1, 1): ax.axvline(x,color="white",lw=0.5)
    for y in [0.5,1.5]: ax.axhline(y,color="white",lw=2)
    ax.set_xlabel(lbl)
axes[0].set_title("Estado de detección y secuenciación por virus y semana", fontsize=11, weight="bold")
handles=[Patch(facecolor=COL[s],edgecolor="#888",label=s) for s in ORDER]
axes[1].legend(handles=handles, bbox_to_anchor=(0.5,-0.55), loc="upper center",
          ncol=3, frameon=False, fontsize=8)
plt.tight_layout()
fig.savefig(OUT/"f1_heatmap_temporal.pdf", bbox_inches="tight"); plt.close(fig)

# ---------- F2: linea de tiempo de linajes SARS-CoV-2 ----------
det = sars[sars.estado=="determinado"].copy().sort_values("semana")
cladecol = {"24A":"#3182bd","24H":"#de2d26"}
fig,ax = plt.subplots(figsize=(7.5,3.3))
ax.plot(det.semana, range(len(det)), color="#bbbbbb", lw=1.2, zorder=1)
for i,(_,r) in enumerate(det.iterrows()):
    ax.scatter(r.semana, i, s=180, color=cladecol.get(r.clado,"#666"), zorder=3, edgecolor="k", lw=0.5)
    ax.text(r.semana+0.25, i, f"  {r.linaje}", va="center", ha="left", fontsize=10)
ax.set_yticks(range(len(det))); ax.set_yticklabels([f"Sem. {w}" for w in det.semana])
ax.set_xlim(2, 11); ax.set_xlabel("Semana de muestreo (abr – jun 2025)")
ax.set_title("Linajes de SARS-CoV-2 identificados en aguas residuales", fontsize=11, weight="bold")
handles=[Patch(facecolor=c,edgecolor="k",label=f"Clado {k}") for k,c in cladecol.items()]
ax.legend(handles=handles, loc="lower right", frameon=True, fontsize=9)
plt.tight_layout(); fig.savefig(OUT/"f2_linajes_sars.pdf", bbox_inches="tight"); plt.close(fig)

# ---------- F3: esfuerzo y rendimiento de secuenciacion por virus ----------
def counts(df, col):
    return df[col].value_counts()
rows=[]
for v,df,col in [("SARS-CoV-2",sars,"estado"),("Enterovirus",pol,"hallazgo"),("RSV",rsv,"hallazgo")]:
    n=len(df)
    no_seq=(~df.secuenciado).sum()
    if v=="SARS-CoV-2":
        det_n=(df.estado=="determinado").sum(); nod=(df.estado=="no_determinado").sum(); cox=0
    else:
        det_n=0; nod=(df.hallazgo=="no_determinado").sum(); cox=df.hallazgo.str.contains("Coxsackie").sum()
    rows.append(dict(virus=v, **{"No secuenciado":no_seq,"Secuenciado: no determinado":nod,
                                 "Secuenciado: determinado":det_n,"Secuenciado: Coxsackie A":cox}))
eff=pd.DataFrame(rows).set_index("virus")[["No secuenciado","Secuenciado: no determinado","Secuenciado: determinado","Secuenciado: Coxsackie A"]]
fig,ax=plt.subplots(figsize=(6.5,4))
bottom=np.zeros(len(eff))
for s in eff.columns:
    ax.bar(eff.index, eff[s], bottom=bottom, color=COL[s], label=s, edgecolor="white", lw=0.6)
    for i,val in enumerate(eff[s]):
        if val>0: ax.text(i, bottom[i]+val/2, int(val), ha="center", va="center", fontsize=9)
    bottom+=eff[s].values
ax.set_ylabel("Número de muestras"); ax.set_title("Esfuerzo y rendimiento de la secuenciación por virus", fontsize=11, weight="bold")
ax.legend(bbox_to_anchor=(0.5,-0.12), loc="upper center", ncol=2, frameon=False, fontsize=8)
plt.tight_layout(); fig.savefig(OUT/"f3_rendimiento.pdf", bbox_inches="tight"); plt.close(fig)

# ---------- F4: polio/RSV por conservacion y desenlace ----------
pr = pd.concat([pol.assign(grupo="Enterovirus"), rsv.assign(grupo="RSV")])
cons_lbl={"fresca":"Fresca\n(prospectiva)","shield_2x":"Shield 2X\n(retrospectiva)","pbs_1x":"PBS 1X\n(retrospectiva)"}
pr["cons"]=pr.conservacion.map(cons_lbl)
pr["estado_simple"]=np.where(pr.secuenciado,"Secuenciada","No secuenciada")
order_c=[cons_lbl["fresca"],cons_lbl["shield_2x"],cons_lbl["pbs_1x"]]
fig,axes=plt.subplots(1,2,figsize=(9,3.8),sharey=True)
for ax,(g,sub) in zip(axes, pr.groupby("grupo")):
    tab=sub.groupby(["cons","estado_simple"]).size().unstack(fill_value=0).reindex(order_c)
    for col_,c in [("No secuenciada","#9ecae1"),("Secuenciada","#74c476")]:
        if col_ not in tab: tab[col_]=0
    bottom=np.zeros(len(tab))
    for col_,c in [("No secuenciada","#9ecae1"),("Secuenciada","#74c476")]:
        ax.bar(tab.index, tab[col_], bottom=bottom, color=c, label=col_, edgecolor="white")
        bottom+=tab[col_].values
    ax.set_title(g, fontsize=11, weight="bold"); ax.set_xlabel("")
    ax.tick_params(axis="x", labelsize=8)
axes[0].set_ylabel("Número de muestras")
axes[1].legend(loc="upper right", fontsize=8, frameon=True)
fig.suptitle("Muestras de enterovirus y RSV por método de conservación", fontsize=11, weight="bold", y=1.02)
plt.tight_layout(); fig.savefig(OUT/"f4_conservacion.pdf", bbox_inches="tight"); plt.close(fig)

print("Figuras generadas en", OUT.resolve())
for f in sorted(OUT.glob("*.pdf")): print(" -", f.name, f.stat().st_size,"B")

# ---------- F5: Cq por semana (N1, N2) coloreado por estado ----------
cq = pd.read_csv(D/"cq_sars_por_semana.csv")
estado_color = {"determinado":"#74c476","no_determinado":"#fdae6b","no_secuenciado":"#9ecae1"}
fig, ax = plt.subplots(figsize=(11,4.2))
# franja de "determinables": las 6 muestras determinadas
ax.axhspan(33, 36, color="#74c476", alpha=0.10, zorder=0)
for gene, marker, lbl in [("N1","o","Gen N1 (HEX)"),("N2","s","Gen N2 (FAM)")]:
    sub = cq.dropna(subset=[gene])
    ax.scatter(sub.semana, sub[gene], marker=marker, s=70,
               c=[estado_color[e] for e in sub.estado], edgecolor="k", lw=0.5,
               label=lbl, zorder=3)
    ax.plot(sub.semana, sub[gene], color="#cccccc", lw=0.8, zorder=1)
ax.invert_yaxis()  # Cq bajo = más arriba (mayor carga)
ax.set_xlabel("Semana de muestreo (abr 2025 – ene 2026)"); ax.set_ylabel("Valor de Cq")
ax.set_title("Valores de Cq de SARS-CoV-2 por semana (genes N1 y N2)", fontsize=11, weight="bold")
ax.set_xticks(range(2,43,2))
from matplotlib.lines import Line2D
leg1 = ax.legend(loc="upper right", fontsize=8, frameon=True, title="Marcador")
ax.add_artist(leg1)
est_handles=[Line2D([0],[0],marker='o',color='w',markerfacecolor=estado_color[k],markeredgecolor='k',
             markersize=9,label=v) for k,v in
             [("determinado","Linaje determinado"),("no_determinado","Secuenciado, no determinado"),
              ("no_secuenciado","No secuenciado")]]
ax.legend(handles=est_handles, loc="lower left", fontsize=8, frameon=True, title="Resultado")
ax.text(0.5,34.5,"Rango de las muestras\ncon linaje determinado", fontsize=7.5, color="#3d8b3d", ha="left")
plt.tight_layout(); fig.savefig(OUT/"f5_cq_sars.pdf", bbox_inches="tight"); plt.close(fig)
print("F5 generada:", (OUT/"f5_cq_sars.pdf").stat().st_size, "B")
