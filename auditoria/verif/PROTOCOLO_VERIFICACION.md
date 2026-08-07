# Protocolo de verificación de CONTEXTO (no búsqueda por patrón)

## Motivo
En la extracción previa las citas se localizaron buscando pasajes dentro del texto de `pdftotext` y verificando literalidad + página. Eso NO garantiza que el pasaje signifique lo que la afirmación dice. Esta pasada verifica el **contexto semántico** de cada cita.

## Para CADA fila (id) haz esto, sin atajos:
1. **Entiende el paper**: lee título + resumen/abstract del PDF citado para saber de qué trata realmente y en qué población/contexto.
2. **Lee la SECCIÓN COMPLETA** que rodea a cada cita (varios párrafos antes y después, no la línea suelta). Usa `pdftotext -f P -l P` sobre la página y las páginas vecinas.
3. **Confirma el respaldo semántico**: ¿el contexto realmente sostiene la `idea` de la tesis? Cuidado con:
   - citas sacadas de una sección que habla de OTRO virus/población/método;
   - negaciones o condicionales que invierten el sentido ("no se halló", "salvo que", "a diferencia de");
   - cifras que pertenecen a otra fila de una tabla o a otro grupo;
   - atribuciones (un autor citando a un tercero, no afirmándolo él).
4. **Verifica evidencia_textual y refuerzo_pico** (ambas columnas ya colocadas): confirma que existen verbatim y que están en contexto.

## Veredicto por fila (`estado`):
- `CONFIRMADO` — cita literal correcta Y contexto respalda la idea.
- `CORREGIDO` — la cita/página/atribución tenía un problema; se entrega la versión correcta.
- `FUERA_DE_CONTEXTO` — la cita es literal pero el contexto NO respalda la idea (se explica y, si existe, se ofrece la cita correcta).
- `CITA_NO_HALLADA` — no se encontró verbatim en la página indicada.

## Salida (CSV `OUT_V<bloque>.csv`), cabecera exacta:
`id,estado,evidencia_textual,refuerzo_pico,nota_contexto`
- `evidencia_textual` y `refuerzo_pico`: la versión CONFIRMADA o CORREGIDA (cita literal + (archivo, p.X)).
- `nota_contexto`: 1–2 frases sobre qué dice el contexto y por qué respalda (o no) la idea.
- Solo texto verificado leyendo el contexto. Prohibido inventar. Comillas CSV correctas.
