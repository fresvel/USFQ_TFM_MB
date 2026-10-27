# Contexto para el punto 3: controles de la PCR multiplex sin valores

Encargo para otro agente. Tarea acotada. **No toques nada más del manuscrito.**

## El repositorio

Raíz: `/home/fresvel/Insync/homero.j.velastegui.i@pucese.edu.ec/OneDrive Biz/Documentos/Posgrados/Microbiología/TFM`

No es software: es la tesis de maestría en Microbiología (USFQ) sobre vigilancia genómica
de SARS-CoV-2, enterovirus y RSV en el influente de la PTAR Quitumbe, Quito. LaTeX, en
español. Lee `CLAUDE.md` y `AGENTS.md` antes de redactar; sus reglas mandan sobre cualquier
estilo por defecto.

Compilación, desde `Latex/`: `./make.sh` (XeLaTeX en Docker) → `Latex/out/main.pdf`.
Recompila y revisa el PDF después de tocar cualquier `.tex`.

## Qué pidió la revisora

De `Recursos/Correcciones/Comentarios tesis Eliana Viscarra.pdf`, «Puntos importantes»:

> **Controles de lab (p 45, 47-54):** La metodología menciona los controles de forma
> cualitativa, pero en Resultados falta el estado por corrida, los valores del control
> positivo, el blanco de extracción y, sobre todo con Cq altos, un control negativo y
> alguna evaluación de contaminación cruzada o salto de índices.

Este encargo cubre **solo la parte de la PCR multiplex**. El blanco de extracción, del mismo
comentario, va en otro encargo: `auditoria/contexto_punto2_blanco_extraccion.md`. Los dos
tocan la misma subsección, así que coordínate para no editarla a la vez.

## Estado actual

Los controles de **RT-qPCR** están resueltos con valores y tabla: subsección «Controles de
laboratorio» en `Latex/secciones/02_cuerpo/04_analisis_datos.tex:56-60`, con el Anexo C
(`Latex/secciones/03_finales/03_anexos_i.tex:125-147`) generado desde
`Latex/assets/datos/controles.csv`, que da por análisis la fecha, el control del kit Luna,
el control positivo de extracción y el estado del NTC.

Los controles de la **PCR multiplex** solo aparecen de forma cualitativa, en tres sitios:

- `03_metodologia_diseno.tex:128` — «con inclusión de controles positivos y negativos para
  verificar la validez de los resultados y descartar contaminación \cite{NEB_2021}».
- `03_metodologia_diseno.tex:266` — «Las PCR multiplex de SARS-CoV-2 incluyeron controles
  positivo y negativo, evaluados por electroforesis \cite{NEB_2021}».
- `04_analisis_datos.tex:60` — «Los controles de la PCR multiplex se evaluaron en gel y no
  se secuenciaron, de modo que ninguna corrida de secuenciación incluyó un control negativo
  con código de barras».

No hay en ninguna parte el resultado de esos controles por corrida: si el positivo dio banda
y el negativo quedó limpio en cada una de las cuatro corridas de secuenciación.

Dato relacionado ya escrito, en `03_metodologia_diseno.tex:268`: «Los controles positivos
disponibles se limitaron a SARS-CoV-2», es decir, no hubo control positivo de poliovirus ni
RT-qPCR de RSV.

## Lo que hay que preguntar al autor

Una pregunta concreta cada vez (lo exige `CLAUDE.md`):

1. ¿Conserva el registro o las fotografías de los geles con los controles de la PCR
   multiplex, por análisis o por corrida? Los geles del termociclador y otros registros
   están en `Recursos/Correcciones/registros/`; conviene mirar ahí antes de preguntar.
2. Si los conserva: ¿el control positivo mostró la banda esperada y el negativo quedó sin
   banda en todas las corridas, o hubo excepciones?

Si no hay registro recuperable, lo correcto es declararlo con la misma honestidad que el
resto de ausencias, sin inventar estados ni valores. **Prohibido rellenar con datos
plausibles**; el autor ya rechazó antes que se maquillaran procedimientos.

## Dónde iría

- Con datos: una o dos oraciones en la subsección de controles
  (`04_analisis_datos.tex:56-60`), después de la de RT-qPCR y antes de la que explica la
  falta de control negativo secuenciado. Si hubiera valores por corrida, una columna nueva
  en `controles.csv` y su reflejo en el Anexo C.
- Sin datos: una frase en esa misma subsección que diga que el resultado de los controles de
  la PCR multiplex se valoró solo de forma cualitativa en el gel, sin registro por corrida, y
  la mención correspondiente en las limitaciones (`06_conclusiones.tex:7`), donde ya conviven
  la falta de curva estándar, de control de recuperación, de normalización fecal, de límite
  de detección, de réplicas técnicas y de control negativo secuenciado.

## Reglas de redacción

De `CLAUDE.md`: redacción referenciada (en metodología valen fuentes primarias u oficiales),
citas APA con BibTeX en `Latex/assets/bibliografia.bib`, prohibición estricta de los giros de
IA generativa («no A sino B», muletillas, dos puntos con ideas en paralelo, back-reference
vago), cadena causal entre oraciones, y una cita repetida una sola vez al final del párrafo.

Método: un párrafo a la vez, se muestra al autor, se aplica tras su aprobación, se recompila
y se verifica en el PDF. Un commit por cambio aprobado, mensaje corto en español.

## Estado del repositorio

Rama `main`, al día con el remoto, árbol limpio. `Latex/build/` ya no se rastrea.
