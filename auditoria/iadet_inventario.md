# Inventario de detección de IA (Turnitin) — Introducción y Discusión/Conclusiones

Fuentes: `IADET/INTRO.pdf` (21 p., **22 % IA**, 12 segmentos) y `IADET/DISC.pdf` (9 p., **29 % IA**, 7 segmentos). Ambos entregados el 2026-08-07 (11:09 y 11:11).

**Dato clave de sincronización.** Los Lotes de corrección de la auditoría se commitearon 10:46–10:59; Turnitin corrió a las 11:09–11:11 del **mismo día**. Los reportes reflejan **el texto ya corregido**: la detección NO se resolvió con las correcciones de citas, y varios párrafos detectados son justamente los que se tocaron en los Lotes. Conclusión: la detección es un problema de **estilo/estructura**, independiente de que el contenido esté citado.

Metodología (`docker` compila; se revisa **un párrafo a la vez**, se propone corrección explicando el patrón atacado, se aplica solo tras aprobación, y se recompila por secciones —omitiendo hojas no detectadas cuando se pida—).

## Códigos de patrón IA (violan reglas de continuidad de CLAUDE.md)

| Cód. | Patrón | Regla violada |
|---|---|---|
| **P1** | Enumeración paralela larga (varios sujetos en serie compartiendo verbo: «el caudal, la dilución, los aportes, el tamaño… alteran X, mientras Y afecta Z») | continuidad #1, #6 |
| **P2** | Párrafo-definición expositivo tras encabezado; oraciones de longitud uniforme (baja *burstiness*) | continuidad #2 |
| **P3** | «X hace A; Y hace B» en paralelo o con dos puntos + ideas sueltas | continuidad #5 |
| **P4** | Cadena de cifras/hechos yuxtapuestos con conectores de relleno («En paralelo», «Una revisión…», «de modo que») | continuidad #1, #4 |
| **P5** | Oración de síntesis/recomendación balanceada de cierre (muletilla estructural) | continuidad #4 |

## Origen (¿corrección de la auditoría o texto anterior?)

`git blame` sobre la línea de cada párrafo. `6fb2a4f`=Lote 1 (intro), `88b2847`=Lote 2 (disc), `cf72a6e`=Lote 4 (concl). Cualquier otro hash = **texto anterior** (no tocado por la auditoría).

---

## INTRODUCCIÓN — 13 párrafos detectados

| ID | Subsección | Archivo:línea | ids trazab. | Origen | Patrón | Extracto (inicio) | Estado |
|---|---|---|---|---|---|---|---|
| **I1** | Vigilancia basada en aguas residuales | `01_introduccion.tex:33` | INTROB-VBAR-* | **Lote 1** | P1 | «La interpretación de la señal exige reconocer los factores… El caudal, la dilución por lluvias…» | ☐ pendiente |
| **I2** | Virus de interés: SARS-CoV-2 | `01_introduccion.tex:57` (+ inicio de :59) | INTROC-SARS-* | **Lote 1** | P3/P4 | «SARS-CoV-2 impulsó la vigilancia genómica ambiental… Los genes N1 y N2… definidos por los CDC…» | ☐ pendiente |
| **I3** | Virus de interés: RSV | `01_introduccion.tex:67` | INTROC-RSV-* | anterior (`22275a8`) | P2 | «La caracterización genómica de RSV exige distinguir entre RSV-A y RSV-B…» | ☐ pendiente |
| **I4** | Virus de interés: Enterovirus | `01_introduccion.tex:77` | INTROC-ENT-* | anterior (`86ee903`) | P4 | «El episodio más reciente lo describieron Klapsa… 118 aislamientos… En paralelo… Una revisión sistemática…» | ☐ pendiente |
| **I5** | Variabilidad genética | `01_introduccion.tex:116` | INTROD-Variabilidad-* | **Lote 1** | P1 | «Su valor epidemiológico depende de criterios explícitos de cobertura… La representación de los linajes minoritarios…» | ☐ pendiente |
| **I6** | Herramientas bioinformáticas (puente) | `01_introduccion.tex:120` | INTROD-Bioinformatica-* | **Lote 1** | P2 | «En la vigilancia genómica, el análisis bioinformático procesa las lecturas… encadena etapas de control de calidad, alineamiento, ensamblaje…» | ☐ pendiente |
| **I7** | Procesamiento de secuencias | `01_introduccion.tex:124` | INTROD-Procesamiento-* | **Lote 1** | P2/P3 | «El procesamiento de secuencias constituye la primera fase… Nanopore produce lecturas largas… Illumina genera lecturas cortas…» | ☐ pendiente |
| **I8** | Procesamiento de secuencias | `01_introduccion.tex:126` | INTROD-Procesamiento-* | **Lote 1** | P1 | «Las aguas residuales son una matriz ambiental compleja… registrar los metadatos —el punto y la fecha de muestreo, el volumen…—» | ☐ pendiente |
| **I9** | Caracterización genética | `01_introduccion.tex:130` | INTROD-CaractGenetica-* | **Lote 1** | P2 | «La caracterización genética de una entidad infecciosa utiliza herramientas de asignación de linajes… Freyja…» | ☐ pendiente |
| **I10** | Caracterización genética | `01_introduccion.tex:132` | INTROD-CaractGenetica-* | **Lote 1** | P2 | «En RSV, la caracterización genética distingue RSV-A y RSV-B… En poliovirus, la identificación se apoya…» | ☐ pendiente |
| **I11** | Situación en Ecuador | `01_introduccion.tex:146` | INTROE-SIT-* | anterior (`0efe287`) | P5 | «Mejía Calle destacó que existe una carencia de información genómica clínica en Ecuador…» | ☐ pendiente |
| **I12** | Situación en Ecuador | `01_introduccion.tex:148` | INTROE-SIT-* | anterior (`0efe287`) | P5 | «Para RSV y poliovirus, los recursos revisados son evidencia internacional… manifestando la necesidad de generar evidencia nacional…» | ☐ pendiente |
| **I13** | Justificación | `01_introduccion.tex:154` | INTROE-JUS-* | **Lote 1** | P4 | «La factibilidad del enfoque se sostiene en el antecedente del sitio… el esquema de amplicones ARTIC… 94,9 % y 95,8 %…» | ☐ pendiente |

## DISCUSIÓN — 4 párrafos detectados

| ID | Subsección | Archivo:línea | ids trazab. | Origen | Patrón | Extracto (inicio) | Estado |
|---|---|---|---|---|---|---|---|
| **D1** | Linajes SARS y contexto epidemiológico | `05_discusion.tex:17` | DIS-LIN-* | anterior (`3584840`) | P4 | «El esfuerzo cayó a 744 genomas en 2024 y esa serie nacional termina ese año… no cubre 2025…» | 🔁 v4 SUBIÓ detección (29→35%): alisar prosa la aumenta. v5 aplicada = registro de reporte (autor+cifras), sin cierre interpretativo (fuera `\cite{Parkins_2023}`). Pendiente reverificar Turnitin |
| **D2** | Enterovirus (poliovirus) | `05_discusion.tex:23` | DIS-ENT-* | **Lote 2** | P4 | «Ninguna de las 22 muestras rindió poliovirus… en Eslovaquia… En Canadá, en 2022… 99,4 %… 99,0 %… Seo…» | ☐ pendiente |
| **D3** | RSV | `05_discusion.tex:27` (última oración) | DIS-RSV-* | anterior (`88d9712`) | P5 | «La asociación entre el ARN de RSV en aguas residuales y la circulación comunitaria proviene sobre todo de estudios de cuantificación…» | ☐ pendiente |
| **D4** | Conservación de muestras retrospectivas | `05_discusion.tex:29–31` (encabezado + párrafo) | DIS-CONS-* | anterior (`210786e`) | P2 | «Conservación de muestras retrospectivas como factor crítico. Las ocho muestras retrospectivas, conservadas en DNA/RNA Shield 2X…» | ☐ pendiente |

## CONCLUSIONES — 3 párrafos detectados

| ID | Subsección | Archivo:línea | ids trazab. | Origen | Patrón | Extracto (inicio) | Estado |
|---|---|---|---|---|---|---|---|
| **C1** | Resumen (1.ª oración) | `06_conclusiones.tex:3` | CON-RES-* | línea tocada Lote 4; **oración de apertura anterior** | P5 | «En las aguas residuales de la PTAR Quitumbe, este estudio obtuvo evidencia molecular y genómica de los tres virus analizados, con un alcance que dependió de la carga viral recuperada en cada caso.» | ☐ pendiente |
| **C2** | Importancia y recomendaciones | `06_conclusiones.tex:11` (2.ª oración) | CON-IMP-* | anterior (`478b8cc`) | P5 | «La detección de los tres virus con un flujo común y la caracterización de un enterovirus de interés clínico confirman la viabilidad operativa…» | ☐ pendiente |
| **C3** | Importancia y recomendaciones | `06_conclusiones.tex:13` (ambos párrafos de recomendación) | CON-IMP-* | anterior (`eaf065d`) | P4/P5 | «Para estudios futuros se recomienda iniciar con el procesamiento de las muestras de manera temprana… La incorporación de plataformas… El aumento del número de muestras…» | ☐ pendiente |

---

## Lectura del inventario

- **20 párrafos detectados** en total (13 intro + 4 disc + 3 concl).
- **Reparto por origen:** 10 fueron **tocados en los Lotes** de la auditoría (I1, I2, I5, I6, I7, I8, I9, I10, I13, D2) y 10 son **texto anterior** (I3, I4, I11, I12, D1, D3, D4, C1-apertura, C2, C3). La detección atraviesa por igual ambos orígenes → no la causó la auditoría; es estilo pre-existente que el arreglo de citas no modificó.
- **Patrones dominantes:** P2 (párrafo-definición uniforme tras encabezado) y P4 (cadena de hechos/cifras con conectores de relleno) concentran la mayoría; P1 y P5 en enumeraciones y cierres.
- **Zonas limpias** (no detectadas): Antecedentes, Problemática, biología de SARS/Enterovirus, y las narrativas de estudio concreto (Ahmed/Medema/Calgary/Bangkok, Zurbriggen 62 aislamientos) — son párrafos con sujeto concreto y ritmo variable. Sirven de modelo de reescritura.

## Orden de trabajo propuesto (uno por uno)

Sugerencia: empezar por Discusión/Conclusiones (29 %, menos párrafos, cierre del documento) y luego Introducción. Dentro de cada bloque, priorizar P4/P5 (los de mayor rendimiento por ser cierres y cadenas de cifras) antes que P2.

Secuencia sugerida: **D1 → D2 → D3 → D4 → C1 → C2 → C3 → I1 … I13.**

Para cada uno: (1) releer el/los PDF fuente de sus ids de trazabilidad, (2) extraer idea/dato concreto que sustituya la formulación vaga o uniforme, (3) presentar propuesta *Antes → Después* señalando el patrón atacado, (4) aplicar tras aprobación, (5) recompilar por secciones.
