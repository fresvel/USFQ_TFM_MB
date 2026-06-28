# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not a software project**. It is the LaTeX manuscript for a Master's thesis (TFM) in Microbiology at USFQ, titled *"Análisis Genómico de SARS-CoV-2, Poliovirus y Otros Virus Patógenos en Aguas Servidas"*. The research uses samples from the Quitumbe wastewater treatment plant (PTAR) in Quito, Ecuador, studying SARS-CoV-2, poliovirus, and respiratory syncytial virus (RSV) through wastewater-based epidemiology.

Most work in this repo is **scientific writing in Spanish**, edited as `.tex` source files. The product is a compiled PDF.

## Build

The manuscript lives in `Latex/`. Build from there:

```bash
cd Latex && make          # full build → out/main.pdf (and compressed out/report.pdf)
make clean                # remove build/ and out/ artifacts
```

`make` runs `make.sh`, which compiles **inside Docker** (image `usfq-tex`, built on first run from `docker/Dockerfile`). The pipeline is `xelatex → bibtex → xelatex → xelatex` (XeLaTeX is required for the Times fonts in `docker/fonts/`). To force a rebuild of the Docker image: `BUILD_IMAGE=1 ./make.sh`.

`build/` and `out/` are generated artifacts, git-ignored. **Always recompile and check the PDF after editing any `.tex` file.**

## Manuscript structure (`Latex/`)

- `main.tex` — master document; `\input`s the three section groups in order.
- `config/datos.tex` — cover/approval/copyright field values. Fields rendered in red via `\USFQCampo{...}` are placeholders to fill before final submission.
- `preambulo/preambulo.tex` — USFQ formatting, styles, bibliography setup, tables, indices. Toggle `\USFQIncluirGuiatrue/false` here to show/hide the template guide sheet.
- `secciones/01_preliminares/` — cover, approval, copyright, abstract/resumen, indices.
- `secciones/02_cuerpo/` — the body: `01_introduccion`, `02_revision_literatura`, `03_metodologia_diseno`, `04_analisis_datos`, `05_conclusiones`.
- `secciones/03_finales/` — references, annex index, annexes.
- `assets/bibliografia.bib` — BibTeX database (APA references). New citations go here.
- `assets/figuras/` — figures; `assets/tablas/` — reusable long tables via `longtblr`/`tabularray`.

`Recursos/` holds the source material: papers and books under `Recursos/fuentes/` (organized by `RSV/`, `polio/`, `Sars-cov2/`, `libros/`), plus protocols and notes. These are the evidence base for the writing — they are **inputs, not outputs**.

## Writing rules (mandatory — from AGENTS.md / Contexto.md)

These govern all prose you produce and override default writing behavior:

1. **Referenced writing only.** Every claim in a section/subsection must trace to a paper or book present in the repository (`Recursos/fuentes/`). For methodology, primary or official online sources may also be used. **Never write generatively** or invent experimental claims/inferred data.
2. **Cite in APA style via BibTeX.** Leave `\cite{...}` keys pointing to entries in `assets/bibliografia.bib`; add new entries there.
3. **No generative AI tells.** Strictly avoid constructions like *"no A sino B"*, *"no solo A sino también B"*, and similar. Use direct, descriptive, analytical statements with articulation between paragraphs.
4. Do not revert others' changes or touch unrelated files.
5. When an indispensable fact is missing, ask the user one concrete question at a time rather than assuming.

### Reglas de Redacción (textual, de `AGENTS.md`)

> Todas las redacciones que se te pidan para las secciónes y subsecciones deben ser realizadas con un carácter referenciado, es decir garantizando que la información haga referencia a un paper o libro del repositorio. Evita de manera estricta la redacción generativa.
>
> El estilo de citación a utilizar será APA, pero utilizaremos bibtext, por lo tanto deja citado con referencias a bibtext.
>
> En las redacciones solicitadas evita de manera estricta el uso de desviaciones generativas tales como: "no idea A sino idea B", "no solo idea A sino también idea B" y otras similares típicas de IA generativa. En su lugar utiliza ideas directas y descriptivas.

## Commit conventions

Commit messages in this repo are short and in Spanish (e.g. `metodologia`, `Introducción v1`). Match that style.
