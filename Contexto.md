# Contexto del proyecto TFM

## Descripción

Este repositorio contiene el Trabajo de Fin de Máster en Microbiología para la USFQ titulado **“Análisis Genómico de SARS-CoV-2, Poliovirus y Otros Virus Patógenos en Aguas Servidas”**. La investigación se realizó con muestras de la Planta de Tratamiento de Aguas Residuales Quitumbe, en Quito, y estudia SARS-CoV-2, poliovirus y virus sincitial respiratorio (RSV).

## Estructura relevante

- `Latex/`: documento LaTeX del TFM.
- `Latex/secciones/`: capítulos y secciones del manuscrito.
- `Latex/assets/bibliografia.bib`: referencias BibTeX.
- `Latex/assets/figuras/metodologia/`: imágenes de los procedimientos experimentales.
- `Recursos/`: artículos, libros y documentación de respaldo.
- `Recursos/metodologia/`: descripción detallada de los procedimientos.
- `Recursos/polio/`: protocolo de poliovirus; revisar especialmente `polio_parte1` y `polio_parte2`.
- `PROMPT_METODOLOGIA.md`: solicitud original de redacción metodológica.
- `IDEAS_METODOLOGIA.md`: requisitos metodológicos ordenados.

## Reglas obligatorias

1. Consultar `AGENTS.md` antes de realizar cambios.
2. Prefijar los comandos de terminal con `rtk`, según `/home/fresvel/.codex/RTK.md`.
3. Sustentar la redacción científica con artículos o libros del repositorio. Para la metodología también se deben buscar fuentes primarias u oficiales en internet.
4. Citar en estilo APA mediante BibTeX.
5. Evitar afirmaciones experimentales inferidas o inventadas.
6. Evitar fórmulas generativas como “no A sino B”, “no solo A sino también B” y construcciones similares.
7. Mantener una redacción directa, analítica, profesional y articulada entre párrafos.
8. Utilizar `apply_patch` para editar archivos manualmente.
9. No revertir cambios ajenos ni modificar archivos no relacionados.
10. Compilar y revisar el PDF después de modificar LaTeX.

## Estado del manuscrito

La introducción, problemática, justificación, pregunta de investigación, objetivos, propósito y estructura del estudio fueron revisados previamente. El marco teórico fue desarrollado en `Latex/secciones/02_cuerpo/02_revision_literatura.tex` y comprende vigilancia epidemiológica, vigilancia basada en aguas residuales, muestreo pasivo, virus de interés, técnicas moleculares, secuenciación, bioinformática y contexto ecuatoriano.

La evidencia local disponible es sólida para SARS-CoV-2 y la PTAR Quitumbe. La documentación específica de Ecuador sobre vigilancia de RSV y poliovirus en aguas residuales es limitada y debe reconocerse como una debilidad bibliográfica.

## Tarea pendiente: metodología

Redactar e integrar la metodología siguiendo la estructura sugerida en la plantilla LaTeX. Reconstruir los procedimientos mediante las figuras y documentos internos, y respaldarlos con bibliografía verificable. Revisar primero `PROMPT_METODOLOGIA.md` e `IDEAS_METODOLOGIA.md`.

### Diseño temporal confirmado

- Semanas 1 a 42: análisis de SARS-CoV-2.
- Semanas 43 a 56: análisis de SARS-CoV-2, poliovirus y RSV.
- Muestras retrospectivas para poliovirus y RSV: semanas 17–20 y 34–37.
- Métodos de preservación: DNA/RNA Shield 2X, PBS y congelación del ARN.
- Total de muestras analizadas para poliovirus y RSV: 22.

La metodología debe explicar cómo se obtuvieron las 22 muestras a partir de los periodos prospectivos y retrospectivos, sin asumir una distribución no documentada entre semanas o métodos de conservación.

### Procedimientos específicos

- **SARS-CoV-2:** reconstruir el protocolo completo desde muestreo y conservación hasta detección, secuenciación y análisis bioinformático.
- **Poliovirus:** basarse en `Recursos/polio`, especialmente en `polio_parte1` y `polio_parte2`.
- **RSV:** describir la PCR múltiple con cebadores ARTIC para RSV-A y RSV-B, la amplificación del genoma completo, la electroforesis y la selección de muestras para secuenciación.

Evaluar si se necesitan diagramas editables en draw.io para poliovirus o RSV. Si falta un dato indispensable, formular al usuario una sola pregunta concreta cada vez.

## Resultado esperado

La entrega debe incluir la metodología integrada en LaTeX, las referencias añadidas a BibTeX, los recursos gráficos necesarios, una compilación verificada y un listado final de debilidades metodológicas, vacíos de información y posibles sesgos.
