import json, re, os, sys, importlib.util, unicodedata
spec = importlib.util.spec_from_file_location("dg", os.path.expanduser("~/.claude/skills/auditoria-generativa/scripts/detectar_generativo.py"))
dg = importlib.util.module_from_spec(spec); spec.loader.exec_module(dg)
S=os.path.dirname(os.path.abspath(__file__))

def norm(t):
    t=t.replace("- ","")  # hyphenation from PDF
    t=unicodedata.normalize("NFKD",t.lower())
    t="".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]"," ",t)
def toks(t): return [w for w in norm(t).split() if len(w)>3]

rows=json.load(open(S+"/det_rows.json"))
segs=[]
for r in json.load(open(S+"/out_all.json")):
    if r['file'] in ('INTRO.pdf','DISC.pdf'):
        for i,s in enumerate(r['segments'],1):
            segs.append((r['file'],i,s['text']))

# build shingles per tex paragraph
para=[]
for r in rows:
    raw=open(S+"/tex_cf72a6e/"+r['file'],encoding='utf-8').read().split("\n")
    txt=dg.limpiar("\n".join(raw[r['line']-1:r['line']-1+ (200)]))
    para.append(r)

def para_text(r):
    lines=open(S+"/tex_cf72a6e/"+r['file'],encoding='utf-8').read().split("\n")
    buf=[]
    i=r['line']-1
    while i<len(lines) and lines[i].strip()!="":
        buf.append(lines[i]); i+=1
    return dg.limpiar("\n".join(buf))

ptok={ (r['file'],r['line']): set(toks(para_text(r))) for r in rows }

print(f"{'segmento Turnitin':30} -> parrafos .tex con solape (jaccard>0.15)")
hits={}
for f,i,txt in segs:
    st=set(toks(txt))
    best=[]
    for k,pt in ptok.items():
        if not pt: continue
        inter=len(st&pt)
        cov=inter/max(len(pt),1)   # fraccion del parrafo cubierta por el segmento
        if cov>0.5 and inter>15: best.append((round(cov,2),k,inter))
    best.sort(reverse=True)
    print(f"{f} S{i:<2} ({len(txt.split()):>3}p) -> {[(k[0].replace('_diseno','').replace('01_','').replace('05_','').replace('.tex',''),k[1],c) for c,k,n in best]}")
    for c,k,n in best: hits[k]=hits.get(k,0)+1
json.dump({f"{k[0]}:{k[1]}":v for k,v in hits.items()}, open(S+"/turnitin_hits.json","w"), indent=1)
print("\nPARRAFOS .tex marcados por Turnitin (ground truth):")
for k in sorted(hits): print("  ", k[0], k[1])
