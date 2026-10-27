# Contexto para el punto 6: duplicación y cita faltante en la discusión del Cq

Encargo para otro agente. Tarea de redacción, acotada a **una sola oración**.
No toques nada más del manuscrito.

## El repositorio

Raíz: `/home/fresvel/Insync/homero.j.velastegui.i@pucese.edu.ec/OneDrive Biz/Documentos/Posgrados/Microbiología/TFM`

Tesis de maestría en Microbiología (USFQ) sobre vigilancia genómica de SARS-CoV-2,
enterovirus y RSV en el influente de la PTAR Quitumbe, Quito. LaTeX, en español. Lee
`CLAUDE.md` y `AGENTS.md` antes de redactar.

Compilación, desde `Latex/`: `./make.sh` → `Latex/out/main.pdf`. Recompila y revisa el PDF.

## El problema

En `Latex/secciones/02_cuerpo/05_discusion.tex:11`, apartado «Carga viral, valores de Cq y
rendimiento de la secuenciación», la quinta de siete oraciones dice:

> Un Cq tardío tampoco impide por sí solo la secuenciación, pues en el alcantarillado de San
> Diego la cobertura por amplicones se mantuvo alta con Cq cercanos a 38; por ello, la
> ausencia total de lecturas del virus en las corridas posteriores a la semana 9 señala
> también un fallo de la amplificación en esas corridas, además de la baja carga.

Dos defectos:

1. **Repite una conclusión que el autor pidió retirar.** El arranque del mismo párrafo decía
   antes que el fallo estaba en la amplificación, y el autor lo hizo quitar con una
   instrucción expresa: «no asegures que el fallo está en la amplificación». La oración de
   San Diego mantiene esa afirmación, de modo que el párrafo se contradice con la decisión
   ya tomada.
2. **No lleva cita.** El dato de San Diego (cobertura alta con Cq cercanos a 38) procede de
   `Karthikeyan_2022`, que en el párrafo solo se cita al final y para otro asunto, la
   intermitencia de la señal cerca del límite de detección. Todas las demás comparaciones
   del párrafo sí están citadas: `Child_2023`, `Itokawa_2020`, `Haque_2023`.

## Cómo quedó el arranque del párrafo (no lo toques)

> Las seis muestras con linaje asignado tuvieron los valores de Cq más bajos del periodo, y
> el Cq del gen N1 se correlacionó de forma inversa con la fracción del genoma cubierta
> (Spearman, ρ = −0,70; p < 0,001). Las semanas 13 y 14 presentaron Cq de 33,9 y 34,9,
> dentro del rango de las caracterizadas; sin embargo, se secuenciaron sin llegar a
> caracterizarse, y sus bibliotecas se compusieron de productos de amplificación inespecífica
> y de material no amplificado por los cebadores.

Obsérvese que la composición de las bibliotecas se deja como **observación**, sin atribuirle
causa. Esa es la línea que debe seguir la oración corregida.

El autor también rechazó el argumento del orden de las corridas («no tiene nada que ver que
se haya hecho primero y que se haya logrado caracterizar»), así que no lo reintroduzcas.

## Qué debe hacer la oración corregida

Conservar lo que aporta la fuente ajena —que con Cq cercanos a 38 la cobertura por amplicones
se mantuvo alta en el alcantarillado de San Diego—, con su cita, y soltar la conclusión sobre
dónde estuvo el fallo. El hecho propio (ninguna lectura del virus después de la semana 9) ya
está dicho en el arranque del párrafo y en resultados, así que repetirlo aquí sobra.

Verifica el dato en la fuente antes de escribir. El PDF está en
`Recursos/fuentes/Sars-cov2/s41586-022-05049-6.pdf` (Karthikeyan et al., 2022, Nature). La
entrada BibTeX es `Karthikeyan_2022` en `Latex/assets/bibliografia.bib`. Si el valor exacto
no sale de ahí, dilo en lugar de arrastrarlo.

## Nota sobre la función del párrafo

Hay una regla del proyecto registrada en memoria: en la discusión, cada comparación debe
**confrontar el resultado propio con el antecedente**, no limitarse a recortar duplicados.
La oración de San Diego existe para eso, para contrastar un caso donde un Cq tardío sí rindió
cobertura. Mantén esa función.

## Reglas de redacción

De `CLAUDE.md`: redacción referenciada, citas APA con BibTeX, prohibición estricta de los
giros de IA generativa («no A sino B», «no solo A sino también B», muletillas como «cabe
señalar» o «en este sentido», dos puntos seguidos de ideas en paralelo, el patrón «X…,
mientras que Y», back-reference vago), cadena causal con subordinación real, sin comas
empalmadas, y una cita repetida una sola vez al final del párrafo.

Método: muestra la redacción propuesta al autor, aplícala solo tras su aprobación, recompila
y verifica en el PDF. Un commit, mensaje corto en español.

El autor pide además **no alargar el párrafo**: ya objetó una versión anterior por haber
crecido demasiado. La oración corregida debe ser igual o más corta que la actual.

## Estado del repositorio

Rama `main`, al día con el remoto, árbol limpio. `Latex/build/` ya no se rastrea.
Último commit del área: `d3ea673` (conclusiones: límite de detección y positividad 31/42).
