# Contexto para el punto 2: blanco de extracción

Encargo para otro agente. Tarea acotada: resolver una sola observación de la revisora
sobre los controles de laboratorio del TFM. **No toques nada más del manuscrito.**

## El repositorio

Raíz: `/home/fresvel/Insync/homero.j.velastegui.i@pucese.edu.ec/OneDrive Biz/Documentos/Posgrados/Microbiología/TFM`

No es software: es la tesis de maestría en Microbiología (USFQ) sobre vigilancia genómica
de SARS-CoV-2, enterovirus y RSV en el influente de la PTAR Quitumbe, Quito. Se escribe en
LaTeX y en español. Lee `CLAUDE.md` y `AGENTS.md` antes de redactar: sus reglas son
obligatorias y mandan sobre cualquier estilo por defecto.

Compilación, desde `Latex/`: `./make.sh` (XeLaTeX en Docker). Produce `Latex/out/main.pdf`.
Hay que recompilar después de editar cualquier `.tex` y comprobar el PDF.

## Qué pidió la revisora

Del PDF `Recursos/Correcciones/Comentarios tesis Eliana Viscarra.pdf`, apartado «Puntos
importantes», literal:

> **Controles de lab (p 45, 47-54):** La metodología menciona los controles de forma
> cualitativa, pero en Resultados falta el estado por corrida, los valores del control
> positivo, el blanco de extracción y, sobre todo con Cq altos, un control negativo y
> alguna evaluación de contaminación cruzada o salto de índices. Sin eso no se puede
> descartar que parte de la señal sea artefacto. Sugiero una subsección corta de controles.

## Qué ya está hecho

La subsección existe: `Latex/secciones/02_cuerpo/04_analisis_datos.tex:56-60`, titulada
«Controles de laboratorio». Cubre casi todo lo pedido:

- Control positivo del ensayo Luna en los ocho análisis, con Cq de N1 entre 20,38 y 25,52
  y de N2 entre 20,03 y 24,47.
- NTC (control sin molde) sin señal en N1 ni N2 en los ocho análisis.
- Control positivo de extracción (hisopados faríngeos positivos para SARS-CoV-2) en los
  análisis 2 a 7, con Cq de N1 entre 11,28 y 20,83. El análisis 1 se corrió sin él y sus
  resultados se descartaron.
- Control interno RP en 19 de las 40 muestras.
- La ausencia de control negativo secuenciado y sus consecuencias (contaminación cruzada,
  salto de índices) está declarada en la misma subsección y en las limitaciones
  (`06_conclusiones.tex:7`).
- Tabla por análisis en el **Anexo C**, `Latex/secciones/03_finales/03_anexos_i.tex:125-147`,
  generada desde `Latex/assets/datos/controles.csv`.

## Qué falta exactamente

**El blanco de extracción.** Es el único elemento de la lista de la revisora que no aparece:
agua libre de nucleasas procesada desde el paso de extracción, en paralelo con las muestras,
para detectar contaminación introducida durante el propio procesamiento. No se reporta que
se hiciera y tampoco se declara que no se hizo. El único control negativo documentado es el
NTC, que entra en la reacción de RT-qPCR y no cubre la extracción.

Secundario, del mismo comentario: de los controles de la **PCR multiplex** solo se dice que
«se evaluaron en gel y no se secuenciaron». No hay estado por corrida ni valores, a
diferencia de los de RT-qPCR.

## Lo que hay que preguntar al autor, antes de escribir nada

Una pregunta concreta cada vez (lo exige `CLAUDE.md`):

1. ¿En algún análisis se procesó agua libre de nucleasas desde la extracción, como blanco?
   Si la respuesta es sí, hacen falta los valores de Cq por análisis para llevarlos a la
   subsección y al Anexo C.
2. Si no se hizo, se declara la ausencia igual que las demás, sin inventar nada.

**No asumas la respuesta ni rellenes con datos plausibles.** La regla del repositorio
prohíbe la redacción generativa y la invención de datos experimentales; el autor ya rechazó
en otra ocasión que se maquillaran procedimientos.

## Dónde iría cada cosa

- Si el blanco existe: subsección de controles (`04_analisis_datos.tex:56-60`) y una columna
  o fila nueva en `Latex/assets/datos/controles.csv`, de donde se regenera el Anexo C.
- Si no existe: una frase en la subsección de controles y la mención correspondiente en las
  limitaciones, `06_conclusiones.tex:7`, donde ya conviven la falta de curva estándar, de
  control de recuperación, de normalización fecal, de límite de detección, de réplicas
  técnicas y de control negativo secuenciado.

## Reglas de redacción que aplican

De `CLAUDE.md`, resumidas: redacción referenciada (cada afirmación trazable a una fuente del
repositorio; en metodología valen fuentes primarias u oficiales), citas APA mediante BibTeX
en `Latex/assets/bibliografia.bib`, prohibición estricta de los giros de IA generativa («no A
sino B», muletillas, dos puntos seguidos de ideas en paralelo, back-reference vago), cadena
causal entre oraciones y una cita repetida una sola vez al final del párrafo.

Método de trabajo: **un párrafo a la vez**, se muestra al autor la redacción propuesta, se
aplica solo tras su aprobación, se recompila y se verifica en el PDF. Un commit por cambio
aprobado, con mensaje corto en español.

## Estado del repositorio

Rama `main`, al día con el remoto, árbol limpio. Últimos commits relevantes:
`3bc758c` (figura 5: amplicón de VP1 tipificado como Coxsackievirus A1) y `d3ea673`
(conclusiones: límite de detección en limitaciones y positividad 31/42 con IC).

`Latex/build/` dejó de rastrearse; los artefactos de compilación ya no entran en los commits.
