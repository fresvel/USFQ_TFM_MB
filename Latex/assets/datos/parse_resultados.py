import re, datetime as dt
import openpyxl, pandas as pd
from pathlib import Path

SRC = "Recursos/Resultados.xlsx"
OUT = Path("Latex/assets/datos"); OUT.mkdir(parents=True, exist_ok=True)

wb = openpyxl.load_workbook(SRC, data_only=True)
ws = wb["Sheet1"]
rows = list(ws.iter_rows(values_only=True))
def cell(r,c):
    v = rows[r][c] if r < len(rows) and c < len(rows[r]) else None
    return ("" if v is None else str(v).strip())

wk_re = re.compile(r"Semana\s+(\d+):\s*([\d/]+)\s*al\s*([\d/]+)")
def parse_label(s):
    m = wk_re.search(s)
    if not m: return None
    wk = int(m.group(1)); d0 = m.group(2)
    dd, mm = d0.split("/")[0], d0.split("/")[1]
    year = 2025 if wk <= 37 else 2026
    if wk == 38: year = 2025  # 29/12/25
    try: fecha = dt.date(year, int(mm), int(dd)).isoformat()
    except: fecha = ""
    return wk, fecha

def yesno(s):
    s = s.strip().lower()
    return True if s.startswith("s") else False

# Block specs: (row_start, row_end_inclusive, col_label, col_seq, col_res)
def grab(r0, r1, cl, cs, cr):
    out=[]
    for r in range(r0, r1+1):
        lab = cell(r, cl)
        p = parse_label(lab)
        if not p: continue
        wk, fecha = p
        out.append(dict(semana=wk, fecha_inicio=fecha,
                        secuenciado=yesno(cell(r,cs)), resultado_raw=cell(r,cr)))
    return out

# ---------- SARS-CoV-2 ----------
sars = grab(2,38,0,1,2) + grab(2,6,5,6,7)   # 2025 (sem1-37) + 2026 (sem38-42)
sdf = pd.DataFrame(sars).sort_values("semana").reset_index(drop=True)
def parse_sars(res):
    if not res: return ("","", "no_secuenciado_o_sin_dato")
    if "no se logra" in res.lower(): return ("","","no_determinado")
    clado = lin = ""
    mc = re.search(r"[Cc]lado\s+([0-9A-Za-z.]+)", res)
    ml = re.search(r"[Ll]inaje\s+([0-9A-Za-z.]+)", res)
    if mc: clado = mc.group(1)
    if ml: lin = ml.group(1)
    return (clado, lin, "determinado" if (clado or lin) else "otro")
sdf[["clado","linaje","estado"]] = sdf["resultado_raw"].apply(lambda x: pd.Series(parse_sars(x)))
sdf.loc[(~sdf.secuenciado),"estado"]="no_secuenciado"
sdf["virus"]="SARS-CoV-2"; sdf["tipo_muestra"]="prospectiva"; sdf["conservacion"]="fresca"
sdf.to_csv(OUT/"sars_cov2.csv", index=False)

# ---------- Poliovirus ----------
pol_pros = grab(9,22,5,6,7)
for d in pol_pros: d.update(tipo_muestra="prospectiva", conservacion="fresca")
pol_sh = grab(10,13,9,10,11)
for d in pol_sh: d.update(tipo_muestra="retrospectiva", conservacion="shield_2x")
pol_arn = grab(15,18,9,10,11)
for d in pol_arn: d.update(tipo_muestra="retrospectiva", conservacion="arn_-20C")
pdf = pd.DataFrame(pol_pros+pol_sh+pol_arn)
def parse_other(res):
    r=res.lower()
    if not res: return "no_determinado_o_sin_dato"
    if "no se logra" in r: return "no_determinado"
    if "coxsackie" in r: return "Coxsackie A (enterovirus no polio)"
    return res
pdf["hallazgo"]=pdf["resultado_raw"].apply(parse_other)
pdf.loc[(~pdf.secuenciado),"hallazgo"]="no_secuenciado"
pdf["virus"]="Poliovirus"
pdf=pdf.sort_values(["tipo_muestra","semana"]).reset_index(drop=True)
pdf.to_csv(OUT/"poliovirus.csv", index=False)

# ---------- RSV ----------
rsv_pros = grab(26,39,5,6,7)
for d in rsv_pros: d.update(tipo_muestra="prospectiva", conservacion="fresca")
rsv_sh = grab(28,31,9,10,11)
for d in rsv_sh: d.update(tipo_muestra="retrospectiva", conservacion="shield_2x")
rsv_arn = grab(33,36,9,10,11)
for d in rsv_arn: d.update(tipo_muestra="retrospectiva", conservacion="arn_-20C")
rdf = pd.DataFrame(rsv_pros+rsv_sh+rsv_arn)
rdf["hallazgo"]=rdf["resultado_raw"].apply(parse_other)
rdf.loc[(~rdf.secuenciado),"hallazgo"]="no_secuenciado"
rdf["virus"]="RSV"
rdf=rdf.sort_values(["tipo_muestra","semana"]).reset_index(drop=True)
rdf.to_csv(OUT/"rsv.csv", index=False)

# ---------- Tidy long (cross-virus) ----------
def estado_unif(row):
    if not row["secuenciado"]: return "No secuenciado"
    h = str(row.get("estado", row.get("hallazgo","")))
    if "determinado" == h or h=="determinado": return "Secuenciado: determinado"
    if h=="no_determinado": return "Secuenciado: no determinado"
    if "Coxsackie" in h: return "Secuenciado: Coxsackie A"
    return "Secuenciado: "+h
s_long = sdf.assign(estado_unif=sdf.apply(lambda r: "No secuenciado" if not r.secuenciado else ("Secuenciado: determinado" if r.estado=="determinado" else "Secuenciado: no determinado"), axis=1))
def long_from(df, estadocol):
    rec=[]
    for _,r in df.iterrows():
        if not r["secuenciado"]: e="No secuenciado"
        else:
            h=r[estadocol]
            if h=="determinado": e="Secuenciado: determinado"
            elif h=="no_determinado": e="Secuenciado: no determinado"
            elif "Coxsackie" in str(h): e="Secuenciado: Coxsackie A"
            else: e="Secuenciado: "+str(h)
        rec.append(dict(virus=r["virus"], semana=r["semana"], fecha_inicio=r["fecha_inicio"],
                        tipo_muestra=r["tipo_muestra"], conservacion=r["conservacion"],
                        secuenciado=r["secuenciado"], estado=e, resultado_raw=r["resultado_raw"]))
    return rec
long = long_from(sdf,"estado")+long_from(pdf,"hallazgo")+long_from(rdf,"hallazgo")
ldf = pd.DataFrame(long).sort_values(["virus","tipo_muestra","semana"]).reset_index(drop=True)
ldf.to_csv(OUT/"vigilancia_long.csv", index=False)

# ---------- Resumen ----------
print("=== SARS-CoV-2 (n=%d) ==="%len(sdf))
print(sdf["estado"].value_counts().to_string())
print("Determinados:", sdf[sdf.estado=='determinado'][['semana','clado','linaje']].to_dict('records'))
print("\n=== Poliovirus (n=%d) ==="%len(pdf))
print(pdf.groupby(['tipo_muestra'])["secuenciado"].agg(['sum','count']).to_string())
print(pdf["hallazgo"].value_counts().to_string())
print("\n=== RSV (n=%d) ==="%len(rdf))
print(rdf.groupby(['tipo_muestra'])["secuenciado"].agg(['sum','count']).to_string())
print(rdf["hallazgo"].value_counts().to_string())
print("\nArchivos escritos en", OUT.resolve())
for f in sorted(OUT.glob("*.csv")): print(" -", f.name, f.stat().st_size, "B")
