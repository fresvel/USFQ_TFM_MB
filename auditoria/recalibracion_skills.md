# Recalibración de las tres skills contra la evidencia del TFM

**Fecha:** 4 de septiembre de 2026
**Alcance:** `auditoria-generativa`, `auditoria-fuentes`, `reduccion-extension` y el fichero
de memoria asociado. Los cuatro son globales y viven en `~/.claude/`, no en este repositorio.

**Material de contraste usado** (ninguno se había usado al escribir las skills):

- Los **12 informes de Turnitin** del historial de git: `IADET/RES · DIS · CON · INTRO ·
  DISC · DISC3 · DISCREC · INT01 (×2) · INT058 · MET03 · M03`. Solo `M03.pdf` seguía en el
  árbol de trabajo.
- `Metodologia_IADET/met_completa · met_parte1 · met_parte2 · met_parte3` — que **no son
  informes**, son los PDF compilados que se enviaron a Turnitin.
- `auditoria/trazabilidad_fuentes.csv` (211 filas), `auditoria/refuerzo/*.csv`,
  `auditoria/verif/OUT_V*.csv`.
- `auditoria/iadet_inventario.md` como verdad de referencia para medir el detector.

---

## 1. Ficheros tocados

| fichero | cambio |
|---|---:|
| `~/.claude/skills/auditoria-generativa/SKILL.md` | +179 / −20 líneas |
| `~/.claude/skills/auditoria-generativa/scripts/detectar_generativo.py` | reescrito (≈120 líneas nuevas) |
| `~/.claude/skills/auditoria-generativa/references/caso-D1-registro-de-reporte.md` | +60 / −18 |
| `~/.claude/skills/auditoria-fuentes/SKILL.md` | +225 / −15 |
| `~/.claude/skills/reduccion-extension/SKILL.md` | +9 / −2 |
| `~/.claude/projects/-home-fresvel/memory/reduccion-y-auditoria-manuscritos.md` | +30 / −9 |

---

## 2. Qué cambió cada skill

### 2.1 `auditoria-generativa`

**El mecanismo, que no estaba.** El «% detectado como IA» de Turnitin **es la fracción de
palabras resaltadas sobre las enviadas**: comprobado en los 12 informes, con coincidencia
dentro de ±1,5 puntos en 11 de ellos. La skill incorpora la tabla completa y las tres
consecuencias que se derivan:

1. Pulir un párrafo que sigue resaltado no mueve el número.
2. Alargar un párrafo ya resaltado **sube** el porcentaje.
3. Trocear infla el porcentaje del trozo que contiene el bloque marcado.

**Condición de alcance del principio rector.** «Traer el dato real» vale cuando hay un autor
externo a quien atribuir un hallazgo medido. No vale cuando se añade detalle del procedimiento
propio. D1 y MET03/M03 se presentan ahora como par:

| | D1 — funciona | MET03 → M03 — falla |
|---|---|---|
| qué se hizo | registro de reporte con Bruno y cols. (2025) | detalle del procedimiento propio (HEX/FAM, NEBNext ARTIC, Cq≈35, 75 L/s, BSL-2, UV 15 min) |
| resultado | el párrafo deja de aparecer resaltado | **28 % → 40 %**; el bloque resaltado pasa de 295 a 446 palabras |
| anclaje | `639ec51`; `DISC.pdf` 29 % → `DISC3.pdf` 28 % | `47993b8` (28 %) → `a4cba7e` (40 %) |

**La unidad de trabajo es el *run*, no el párrafo.** Turnitin resalta tramos contiguos que
absorben encabezados y vecinos. Encabezados resaltados solos: «Contexto epidemiológico del
estudio Situación en Ecuador.» (7 palabras, en 3 informes), «Importancia y aplicaciones.»
(3 palabras). El mismo párrafo I9 aparece como 29 / 237 / 234 / 260 palabras según el envío.

**P2 corregido: la premisa de *burstiness* estaba invertida.** Los párrafos marcados tienen
más variabilidad de longitud de oración que los limpios (sd 8,0 vs 7,2; cv 0,27 vs 0,25;
AUC 0,58–0,59). Se conserva la parte estructural de P2 (párrafo-definición tras encabezado) y
se retira la parte rítmica.

**Cuatro categorías de riesgo nuevas**, que no se arreglan reescribiendo mejor:

| | bloque | evidencia |
|---|---|---|
| B1 | encabezado + primera frase | encabezados resaltados solos en 4 informes |
| B2 | texto obligado (ética, bioseguridad) | resaltado en `RES`, `MET03`, `M03`; añadir detalle lo empeoró |
| B3 | prosa de protocolo propio | bloque de controles resaltado en `MET03` y `M03` |
| B4 | resultados propios | `RES.pdf` S7, 300 palabras de datos experimentales originales |

**Núcleo estable frente a ruido.** De 37 bloques resaltados distintos, 21 aparecen en un solo
informe. Los que se repiten en ≥3 son el objetivo real. La campaña nunca limpió su propio
núcleo: el bloque C2+C3 se resaltó idéntico, 227 palabras, en cuatro informes.

**Flujo reescrito**: parte del informe resaltado, no del detector; separa núcleo de ruido;
clasifica el bloque en B1–B4 antes de reescribir; obliga a indicar si el tramo crece o mengua;
y el criterio de éxito pasa a ser la desaparición del tramo, no la bajada de puntos.

### 2.2 `detectar_generativo.py`

Reencuadrado como **higiene léxica**, con la matriz de confusión impresa en el propio
docstring. Retirada la banda de densidad. Añadidos `--por-parrafo` (emite `fichero:línea`,
que es lo que permite cruzarlo con un inventario) y `--largos`. Corregidos los dos defectos:
exclusión de `Borrador.tex`/`draft`/`old` (con `--incluir-borradores` para revertir) y filtro
del intensificador cuando hay respaldo estadístico a ±110 caracteres.

**Re-medición, mismo montaje** (snapshot `cf72a6e`, 72 párrafos, etiqueta `iadet_inventario.md`):

| modo | TP | FN | FP | TN | recall | precisión | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| léxico, versión anterior | 1 | 19 | 6 | 46 | 0,05 | 0,14 | **0,07** |
| léxico, versión nueva | 1 | 19 | 6 | 46 | 0,05 | 0,14 | **0,07** |
| `--largos` (>110 palabras) | 12 | 8 | 16 | 36 | 0,60 | 0,43 | **0,50** |
| unión léxico OR largo | 12 | 8 | 18 | 34 | 0,60 | 0,40 | 0,48 |

**El barrido léxico no mejoró y no iba a mejorar.** Los dos defectos corregidos no afectaban a
este snapshot. Lo que cambia es que ya no da consejo falso, que es cruzable, y que añade una
cola de candidatos con F1 0,50 donde no había ninguna. La unión de ambos modos empeora
respecto a `--largos` solo, así que no se propone como modo por defecto.

Verificación de los defectos sobre el cuerpo actual: `Borrador.tex` excluido (6 ficheros /
11 443 palabras frente a 7 / 12 384) y la marca del caso Kruskal-Wallis desaparece (1 → 0).

### 2.3 `references/caso-D1-registro-de-reporte.md`

Reescrito para separar lo comprobable de lo que no lo es. **El 35 % de la v4 no existe en el
árbol ni en git** y se marca explícitamente como no verificable. Queda lo defendible: 29 %
(`DISC.pdf`) → 28 % (`DISC3.pdf`) y, sobre todo, que **el párrafo D1 deja de aparecer
resaltado**. Añadidos los dos límites del registro de reporte: los dos segmentos de
`INT058.pdf` escritos en ese estilo y resaltados igual, y el caso MET03/M03.

### 2.4 `auditoria-fuentes`

**Sexto veredicto: `FABRICANTE-OFICIAL`** (5 filas reales, todas en Metodología), para no
forzar la regla «traza a un paper del repositorio» donde no aplica.

**Reequilibrio `VAGA` / `PARCIAL`**, con la distribución real (n = 211):

| veredicto | n | % |
|---|---:|---:|
| `OK` | 153 | 72,5 % |
| `PARCIAL` | 39 | 18,5 % |
| `SIN_FUENTE` | 10 | 4,7 % |
| `FABRICANTE-OFICIAL` | 5 | 2,4 % |
| `NO` | 2 | 0,9 % |
| `VAGA` | 2 | 0,9 % |

`PARCIAL` es el veredicto de trabajo: 22 de sus 39 filas (56 %) acabaron corregidas en la
pasada 2, frente a 2 de 153 en `OK`.

**Modos de fallo de contexto sustituidos por los reales** (31 casos):

| modo | n |
|---|---:|
| **Reatribución** — se atribuye por tema y no por frase | **13** |
| **Enumeración inflada** — lista de *n*, la fuente respalda *k* | **6** |
| **Rastro incorrecto** — página, verbatim o unidad | **4** |
| Fuente ausente del repositorio | 3 |
| Calificador omitido que cambia la extensión del término | 2 |
| Nomenclatura o edición desfasada | 2 |
| Cifra mal asignada | 1 |
| Sobreestimación del rol institucional | 1 |
| Procedimiento narrado en vez de hallazgo | 1 |

Los tres dominantes llevan ejemplo verbatim del CSV. Se documenta además que los dos modos
que listaba la versión anterior —negaciones que invierten el sentido, autor citando a un
tercero— **no aparecieron ni una vez** en las 211 filas.

**Rendimiento de la pasada 2**: `CONFIRMADO` 180 (85,3 %), `CORREGIDO` 26 (12,3 %),
`CITA_NO_HALLADA` 3, `FUERA_DE_CONTEXTO` 2. Con dos avisos: 2 filas dadas por `OK` en la
pasada 1 resultaron mal, y **6 marcadas `SIN_FUENTE` resultaron `CONFIRMADO`** por no haber
buscado en el resto del repositorio.

**Esquema real del CSV**, con `ubicacion (archivo:linea)` marcada como obligatoria y explicado
por qué: sin ella la auditoría de fuentes no se puede cruzar con `iadet_inventario.md` ni con
`detectar_generativo.py --por-parrafo`. Son las dos auditorías del mismo texto y no había
clave común.

**Vocabularios controlados** para `accion`, `tipo_problema` y `pagina_traza`, con lo que pasó
en la ejecución real: `accion` recogió `Ninguna`/`ninguna`/`revisar`/`revisar_redaccion` y
4 celdas con un párrafo entero; `tipo_problema` tuvo cuatro grafías de «matiz».

**Pasada 3 — refuerzo PICOC**, que faltaba entera pese a ocupar `auditoria/refuerzo/` con
7 bloques y 209 filas. Se documenta el marco, las 5 reglas de extracción y el formato, con el
aviso de que **ninguna** de las 209 filas siguió el formato `PICOC[...]` que su propio
protocolo exige.

**Cierre de la auditoría** como parte del trabajo: en el TFM quedan **18 filas con
`accion ≠ mantener` sin resolver** y solo 33 de 211 marcadas como resueltas.

### 2.5 `reduccion-extension`

La estimación «Bajo: 3–8 % de la prosa» pasa a «Bajo, sin cifra validada», diciendo que el
3–8 % procedía de cinco artículos LNCS y que la banda de densidad en la que se apoyaba fue
retirada. Se conserva el corolario, que sigue medido en LNCS: limpiar la redacción no salva un
artículo que se pasa un 40 %. Se añade una línea aclarando que el detector de
`auditoria-generativa` es higiene léxica y no estima ni páginas ni detección.

*(Bloque aplicado por un subagente con especificación cerrada; verificado después por mí
línea a línea: solo 2 hunks, y la calibración de 444 palabras/página, los límites de Springer
y el presupuesto de páginas quedaron intactos.)*

### 2.6 Fichero de memoria

Corregidos los dos errores señalados —el titular «28 % → 35 %» y la banda de densidad— más la
cautela de particiones («partido en 4 dio 0 % en todas», sin respaldo). Añadidos: el mecanismo
del porcentaje, la condición de alcance del registro de reporte, el reequilibrio
`VAGA`/`PARCIAL`, la reatribución como modo dominante, y dónde están los informes de Turnitin
con cómo extraer el texto resaltado. Frontmatter intacto.

---

## 3. Qué quedó sin resolver

**Anotado como trabajo pendiente, no aplicado** (por indicación expresa):

- **Punto 16.** El solapamiento entre la redundancia entre secciones y el núcleo estable de
  detección. El bloque C2+C3 de 227 palabras aparece idéntico en cuatro informes, y
  `detectar_redundancia.py` nunca se cruzó con la detección de IA.
- **Solapamiento P1 ↔ «enumeración inflada».** Las dos skills describen el mismo defecto desde
  lados distintos —la lista que se alarga más allá de la evidencia— y siguen sin cruzarse
  operativamente. Hoy solo hay una mención en el texto de `auditoria-fuentes`.

**Sin medir, por falta de datos:**

- **El suelo de ruido de Turnitin.** En los 12 envíos nunca se remitió texto idéntico dos
  veces. Se resuelve reenviando el mismo PDF dos veces; hasta entonces, cualquier conclusión
  basada en uno o dos puntos de diferencia está sin fundamento.
- **La salida B3.** El commit `c0ea721` convirtió la prosa de protocolo en una enumeración
  —que es lo que la skill recomienda ahora para ese caso— y **nunca se volvió a medir en
  Turnitin**. Está marcado como aviso dentro de la tabla B1–B4.
- **`CON.pdf`** es el único informe donde mi ratio de palabras resaltadas (33,4 %) no cuadra
  con el porcentaje reportado (29 %). Con 680 palabras es el envío más pequeño; puede ser
  imprecisión de mi extracción o redondeo de Turnitin. No afecta a la conclusión, que se
  apoya en los otros 11.

---

## 4. La afirmación más frágil de las que quedan

**El F1 de 0,50 del clasificador por longitud.** Es la única recomendación operativa nueva
respaldada por una sola medición, y es débil por tres razones:

1. Sale de **un corpus, un idioma, un autor y una partición**: 72 párrafos de un TFM. No hay
   validación cruzada ni segundo documento.
2. El umbral de 110 palabras se eligió mirando esos mismos 72 párrafos, así que está
   **sobreajustado**. El F1 real sobre texto nuevo será menor. La curva es plana entre 90 y
   150 palabras (F1 0,44–0,50), lo que sugiere que el umbral concreto importa poco, pero eso
   tampoco está validado fuera.
3. Un AUC de 0,67 es señal modesta. Con precisión 0,43, más de la mitad de lo que señala son
   falsos positivos. Está escrito como «cola de candidatos, no veredicto», y conviene que siga
   leyéndose así.

La segunda más frágil es la **generalización de las categorías B1–B4** fuera de este
manuscrito: son consistentes en los 12 informes, pero los 12 son del mismo documento, la misma
disciplina y el mismo detector. Que el bloque de ética se marque siempre aquí no demuestra que
se marque siempre en general.

En cambio, lo mejor anclado del conjunto es el mecanismo del porcentaje (12 informes, ±1,5
puntos en 11) y el par MET03/M03 (dos commits, dos párrafos de diferencia, identificados por
verbatim del resaltado).

---

## 5. Dónde están los artefactos

**Copiados a este repositorio**, en `auditoria/iadet_extraccion/`:

| fichero | qué es |
|---|---|
| `extraer_iadet.py` | extrae el texto resaltado de un informe de Turnitin (rectángulos cian `RGB 0.320/0.777/0.855` intersectados con las cajas de palabras, vía PyMuPDF) |
| `det_lineas.py` | variante del detector que emite marcas por párrafo con `archivo:línea` |
| `match.py` | casa los segmentos resaltados con los párrafos del `.tex` por solape de tokens |
| `feats.py` | calcula los rasgos por párrafo (longitud, burstiness, densidad de citas) |
| `segmentos_resaltados.json` | los 37 bloques resaltados de los 12 informes, con página y texto |
| `rasgos_parrafos.json` | los 72 párrafos del snapshot `cf72a6e` con sus rasgos y su etiqueta |

**En el scratchpad de la sesión** (volátil, se borra con `/tmp`):
`/tmp/claude-1000/…/92b30440-1681-487d-b361-88b00b055b3f/scratchpad/`, con los 12 PDF
extraídos de git, los snapshots `.tex` por commit y la copia de seguridad del detector
original (`detectar_generativo.py.orig`).

**Los informes de Turnitin no hacen falta copiarlos**: están en git. Se recuperan con

```bash
git cat-file -p 639ec51:IADET/INTRO.pdf   > INTRO.pdf
git cat-file -p 639ec51:IADET/DISC.pdf    > DISC.pdf
git cat-file -p 639ec51:IADET/DISC3.pdf   > DISC3.pdf
git cat-file -p a4cba7e:IADET/MET03.pdf   > MET03.pdf
git cat-file -p 47993b8:IADET/INT058.pdf  > INT058.pdf
git cat-file -p a1b200f:IADET/RES.pdf     > RES.pdf
```

Usar `git cat-file -p`, no `git show`: en esta sesión el proxy de `git show` corrompió un PDF
binario, y `diff` reportó como idénticos dos ficheros que no lo eran. Comprobar siempre el
tamaño contra `git cat-file -s`.

### Cómo rehacer la medición del detector

```bash
cd auditoria/iadet_extraccion
mkdir -p /tmp/snap && cd "$(git rev-parse --show-toplevel)"
for f in 01_introduccion 05_discusion 06_conclusiones; do
  git cat-file -p cf72a6e:Latex/secciones/02_cuerpo/$f.tex > /tmp/snap/$f.tex
done
python3 ~/.claude/skills/auditoria-generativa/scripts/detectar_generativo.py \
  /tmp/snap/*.tex --por-parrafo --largos
```

y cruzar la salida con las líneas de `auditoria/iadet_inventario.md`
(`01_introduccion.tex`: 33, 57, 67, 77, 116, 120, 124, 126, 130, 132, 146, 148, 154 ·
`05_discusion.tex`: 17, 23, 27, 31 · `06_conclusiones.tex`: 3, 11, 13).
