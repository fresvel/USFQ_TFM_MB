#!/usr/bin/env python3
"""detectar_generativo con salida por parrafo (fichero:linea)."""
import re, sys, os, glob, importlib.util, json
spec = importlib.util.spec_from_file_location("dg", os.path.expanduser("~/.claude/skills/auditoria-generativa/scripts/detectar_generativo.py"))
dg = importlib.util.module_from_spec(spec); spec.loader.exec_module(dg)

def parrafos(path):
    lines = open(path, encoding='utf-8', errors='ignore').read().split("\n")
    out=[]; buf=[]; start=None
    for i,l in enumerate(lines,1):
        if l.strip()=="" :
            if buf: out.append((start, "\n".join(buf))); buf=[]; start=None
            continue
        if start is None: start=i
        buf.append(l)
    if buf: out.append((start,"\n".join(buf)))
    return out

rows=[]
for path in sys.argv[1:]:
    for start, raw in parrafos(path):
        txt = dg.limpiar(raw)
        if len(txt.split()) < 12: continue
        marcas=[]
        for nombre,p in dg.PAT_ES.items():
            for m in re.finditer(p, txt, re.I):
                marcas.append((nombre, m.group(0)))
        rows.append({"file":os.path.basename(path),"line":start,"words":len(txt.split()),
                     "n":len(marcas),"dens":round(1000*len(marcas)/max(len(txt.split()),1),1),
                     "marcas":marcas,"head":txt[:90]})
json.dump(rows, open(sys.argv[0].rsplit('/',1)[0]+"/det_rows.json","w"), ensure_ascii=False, indent=1)
for r in sorted(rows,key=lambda r:(r['file'],r['line'])):
    print(f"{r['file']}:{r['line']:>4} w={r['words']:>4} marcas={r['n']:>2} dens={r['dens']:>5} | {[m[0] for m in r['marcas']]}")
