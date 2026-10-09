import json,re,os,statistics as st,importlib.util
spec=importlib.util.spec_from_file_location("dg",os.path.expanduser("~/.claude/skills/auditoria-generativa/scripts/detectar_generativo.py"))
dg=importlib.util.module_from_spec(spec);spec.loader.exec_module(dg)
S=os.path.dirname(os.path.abspath(__file__))
GT={("01_introduccion.tex",l) for l in (33,57,67,77,116,120,124,126,130,132,146,148,154)}|\
   {("05_discusion.tex",l) for l in (17,23,27,31)}|{("06_conclusiones.tex",l) for l in (3,11,13)}
rows=json.load(open(S+"/det_rows.json"))
def raw(r):
    lines=open(S+"/tex_cf72a6e/"+r['file'],encoding='utf-8').read().split("\n")
    i=r['line']-1;buf=[]
    while i<len(lines) and lines[i].strip()!="": buf.append(lines[i]);i+=1
    return "\n".join(buf)
A=[];B=[]
for r in rows:
    R=raw(r); T=dg.limpiar(R)
    sents=[s for s in re.split(r"(?<=[.;])\s+",T) if len(s.split())>3]
    L=[len(s.split()) for s in sents] or [0]
    ncit=len(re.findall(r"\\cite\w*\{",R))
    nkeys=len(re.findall(r"[,{]\s*[A-Z][A-Za-z]+_\d{4}",R))
    # sujeto-autor: parrafo empieza con Nombre y cols./Apellido (20xx) o "X y cols."
    autor_ini = bool(re.match(r"^[A-ZÁÉÍÓÚ][a-zà-ú]+( [A-ZÁÉÍÓÚ][a-zà-ú]+)? (y cols\.|\\cite)", T))
    n_autor = len(re.findall(r"\b[A-ZÁÉÍÓÚ][a-zà-ú]{2,}\s+y\s+cols\.", T)) + len(re.findall(r"\\cite\w*\{[^}]*\}\s*\.", R))
    ncifra = len(re.findall(r"\d[\d.,]*\s*(?:%|\\%|copias|genomas|muestras|nt|pb|mL|L/s|millones)", R)) + len(re.findall(r"\b\d{2,}\b", T))
    f=dict(file=r['file'],line=r['line'],w=r['words'],nsent=len(sents),
           mlen=round(st.mean(L),1), sd=round(st.pstdev(L),1),
           cv=round(st.pstdev(L)/max(st.mean(L),1),2),
           cit100=round(100*ncit/max(r['words'],1),1), keys=nkeys,
           autor_ini=autor_ini, ncifra=ncifra, cifra100=round(100*ncifra/max(r['words'],1),1),
           marcas=r['n'])
    ((A if (r['file'],r['line']) in GT else B)).append(f)
def summ(name,X,k):
    v=[x[k] for x in X]
    return f"{name} n={len(v)} media={st.mean(v):.2f} mediana={st.median(v):.2f}"
print(f"FLAGGED n={len(A)}   LIMPIOS n={len(B)}")
for k in ("w","nsent","mlen","sd","cv","cit100","cifra100","marcas"):
    a=[x[k] for x in A]; b=[x[k] for x in B]
    print(f"  {k:9} flagged med={st.median(a):7.2f} media={st.mean(a):7.2f} | limpio med={st.median(b):7.2f} media={st.mean(b):7.2f}")
print("  autor_ini: flagged", sum(x['autor_ini'] for x in A),"/",len(A), " limpio", sum(x['autor_ini'] for x in B),"/",len(B))
json.dump({"flag":A,"clean":B},open(S+"/feats.json","w"),indent=1)
