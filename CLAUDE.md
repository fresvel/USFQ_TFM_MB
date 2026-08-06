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

### Continuidad y naturalidad (anti-detección de IA)

Regla obtenida de la auditoría de detección de IA (Turnitin). El objetivo es que cada párrafo lea como un **argumento encadenado**, no como una lista de hechos yuxtapuestos. Aplica siempre lo siguiente:

1. **Cadena causal, no listado de oraciones.** Cada oración debe ser consecuencia o desarrollo de la anterior, unida con subordinación real (`ya que`, `de modo que`, `como… por ello`, `pues`, `dado que… exige`). Prohibido encadenar hechos independientes con puntos seguidos sin relación explícita entre ellos.
2. **Define antes de usar, y con cita.** No introduzcas un término o concepto (p. ej. "bioinformática", "plataforma de secuenciación") sin definirlo primero de forma referenciada. Tras un encabezado, escribe un **párrafo puente** que defina y encuadre el tema antes de entrar en subsecciones; nunca saltes de un `\subsection`/`\subsubsection` directo al detalle.
3. **Sujetos y referencias concretas.** Prohibido el "back-reference" vago: nada de "la matriz descrita", "este enfoque", "dicho procesamiento" cuando el antecedente no está nombrado con claridad. Nombra el sujeto explícito ("las aguas residuales", "el procesamiento de secuencias").
4. **Sin muletillas de IA.** Evita "Es importante destacar que", "Cabe señalar", "En este sentido", "Por otro lado" como relleno, y cualquier fórmula que no aporte contenido.
5. **Sin `:` seguido de ideas sueltas en paralelo.** El patrón "X hace A, mientras que Y hace B" tras dos puntos es un marcador típico de IA. Sustitúyelo por oraciones con causa/consecuencia propias para cada elemento.
6. **Listas dentro de la prosa.** Una enumeración larga va como inciso entre guiones (—…—) dentro de una oración con sentido, no como una oración-lista aislada.
7. **Gramática limpia.** Sin comas empalmadas (dos oraciones independientes unidas por coma); usa subordinación o punto y coma.

Metodología de trabajo para reducir detección: se revisa **un párrafo a la vez**, se muestra al usuario la sección detectada, se propone la corrección explicando qué patrón se ataca, y solo se aplica tras su aprobación (en `Latex/` y, si corresponde, en `IAFIX/`). Nunca inventar contenido para "sonar humano": los hechos y las citas se conservan.

## Commit conventions

Commit messages in this repo are short and in Spanish (e.g. `metodologia`, `Introducción v1`). Match that style.
