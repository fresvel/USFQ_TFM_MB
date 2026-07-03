"""Construye el dataset de Cq de SARS-CoV-2 por semana desde la bitacora de laboratorio
(metodologia/Outline.docx, Analisis 1-7). Mapeo: WWnnn == semana nnn.
Fluoroforos: HEX=N1, FAM=N2, Cy5=RP (control humano). Uso: python cq_dataset.py (desde la raiz)."""
import pandas as pd
from pathlib import Path
OUT = Path("Latex/assets/datos")

# (semana, analisis, N1_HEX, N2_FAM) -- 'NA' = no amplifica
raw = [
 # Analisis 1 (fallo: sin amplificacion, sin control +)
 (1,1,'NA','NA'),(2,1,'NA','NA'),(3,1,'NA','NA'),(4,1,'NA','NA'),(5,1,'NA','NA'),
 # Analisis 2
 (3,2,35.8,35.77),(4,2,42.89,'NA'),(5,2,33.96,34.7),(6,2,34.18,44.13),
 (7,2,33.14,34.17),(8,2,33.18,32.3),(9,2,34.02,33.81),
 # Analisis 3
 (10,3,36.35,34.02),(11,3,36.12,32.79),(12,3,37.1,33.89),(13,3,33.89,31.83),
 (14,3,34.92,31.65),(15,3,'NA','NA'),(16,3,36.41,33.2),(17,3,35.27,'NA'),
 # Analisis 4 (N2 mayormente NA)
 (14,4,35.75,'NA'),(17,4,43.77,'NA'),(18,4,'NA','NA'),(19,4,'NA','NA'),
 (20,4,'NA','NA'),(21,4,36.61,'NA'),
 # Analisis 5
 (22,5,'NA','NA'),(23,5,37.36,'NA'),(24,5,36.17,35.43),(25,5,42.28,'NA'),
 (26,5,'NA','NA'),(27,5,'NA','NA'),
 # Analisis 6
 (28,6,37.34,'NA'),(29,6,36.37,37.28),(30,6,37.01,'NA'),(31,6,'NA','NA'),(32,6,36.37,39.46),
 # Analisis 7 (semanas 33-38) -- sin secuenciacion posterior (sin bandas visibles)
 (33,7,'NA',44.3),(34,7,38.96,'NA'),(35,7,39.21,'NA'),(36,7,40.49,40.13),(37,7,38.63,40.33),(38,7,38.53,'NA'),
]
df = pd.DataFrame(raw, columns=["semana","prueba","N1_HEX","N2_FAM"])
df.to_csv(OUT/"cq_crudo.csv", index=False)

# Regla canonica: excluir analisis 1 (fallo). Para semanas repetidas, usar la corrida
# con mas blancos detectados (menor n de NA; empate -> menor numero de analisis).
def numna(r): return sum(1 for v in [r.N1_HEX,r.N2_FAM] if v=='NA')
df2 = df[df.prueba!=1].copy()
df2["nNA"]=df2.apply(numna,axis=1)
canon=[]
for wk,g in df2.groupby("semana"):
    g=g.sort_values(["nNA","prueba"])
    canon.append(g.iloc[0])
cq=pd.DataFrame(canon)[["semana","prueba","N1_HEX","N2_FAM"]].sort_values("semana")
def num(x): return None if x=='NA' else float(x)
cq["N1"]=cq.N1_HEX.map(num); cq["N2"]=cq.N2_FAM.map(num)
sars=pd.read_csv(OUT/"sars_cov2.csv")[["semana","estado"]]
cq=cq.merge(sars,on="semana",how="left")
cq[["semana","prueba","N1","N2","estado"]].to_csv(OUT/"cq_sars_por_semana.csv", index=False)

det=cq.dropna(subset=["N1"])
print("=== Cq N1 por estado ===")
print(det.groupby("estado")["N1"].agg(['count','mean','min','max']).round(2).to_string())
print("\nEscrito:", (OUT/'cq_sars_por_semana.csv').resolve())
