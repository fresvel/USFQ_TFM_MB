import pymupdf, sys, os, json, re

CYAN = (0.3203125, 0.77734375, 0.85546875)
def close(c, t=0.06):
    return c is not None and all(abs(a-b) < t for a, b in zip(c, t and t or 0 and c or c, )) if False else (
        c is not None and len(c)==3 and all(abs(a-b)<0.06 for a,b in zip(c, CYAN)))

def run(path):
    doc = pymupdf.open(path)
    out = {"file": os.path.basename(path), "pages": doc.page_count, "cover": "", "segments": []}
    # cover text (first 2 pages)
    cov = []
    for pno in range(min(2, doc.page_count)):
        cov.append(doc[pno].get_text())
    out["cover"] = "\n".join(cov)
    cur = None
    for pno in range(doc.page_count):
        p = doc[pno]
        rects = [d['rect'] for d in p.get_drawings() if close(d.get('fill'))]
        if not rects: 
            if cur: out["segments"].append(cur); cur=None
            continue
        rects.sort(key=lambda r: (r.y0, r.x0))
        words = p.get_text("words")  # x0,y0,x1,y1,word,block,line,wordno
        lines = []
        for r in rects:
            sel = [w for w in words if w[1] >= r.y0-3 and w[3] <= r.y1+3 and w[0] >= r.x0-2 and w[2] <= r.x1+2]
            sel.sort(key=lambda w: (round(w[1]), w[0]))
            txt = " ".join(w[4] for w in sel)
            if txt.strip():
                lines.append({"page": pno+1, "y0": round(r.y0,1), "x0": round(r.x0,1), "text": txt})
        # group consecutive lines into segments: contiguous y
        for ln in lines:
            if cur is None:
                cur = {"page_start": ln["page"], "lines": [ln]}
            else:
                last = cur["lines"][-1]
                gap = ln["y0"] - last["y0"]
                if ln["page"] == last["page"] and 0 < gap < 40:
                    cur["lines"].append(ln)
                elif ln["page"] == last["page"]+1 and last["y0"] > 600:
                    cur["lines"].append(ln)
                else:
                    out["segments"].append(cur); cur = {"page_start": ln["page"], "lines": [ln]}
    if cur: out["segments"].append(cur)
    for s in out["segments"]:
        s["text"] = re.sub(r"\s+", " ", " ".join(l["text"] for l in s["lines"])).strip()
        s["pages"] = sorted({l["page"] for l in s["lines"]})
        del s["lines"]
    return out

if __name__ == "__main__":
    res = [run(p) for p in sys.argv[1:]]
    print(json.dumps(res, ensure_ascii=False, indent=1))
