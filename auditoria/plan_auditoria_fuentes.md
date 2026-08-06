# Plan de auditoría de fuentes — TFM Microbiología

## 0. Motivación

Se detectó que había afirmaciones **referenciadas pero no verificadas** contra su fuente, e incluso una fuente citada (`Bruno_2025`) **cuyo PDF no estaba en el repositorio**, con un dato ("tasa de secuenciación baja") que resultó **engañoso** frente a lo que el paper dice de verdad (Ecuador secuenció 12 619 genomas, 1,15 % de casos, cruzando el umbral del 1 %). 

**Objetivo:** validar que **cada afirmación referenciada del cuerpo** de la tesis proviene *exactamente* de su(s) fuente(s), con **trazabilidad a página**, y sustituir toda **idea vaga** por la **idea real y específica** que la fuente respalda.

Regla rectora (de `CLAUDE.md`): toda afirmación debe trazar a un paper/libro presente en `Recursos/fuentes/`. Nada generativo, nada sin verificar.

## 1. Alcance y prioridad

Cuerpo (`Latex/secciones/02_cuerpo/`) + resumen/abstract:

| Sección | Archivo | Prioridad | Motivo |
|---|---|---|---|
| Introducción | `01_introduccion.tex` | **Alta** | Prosa referenciada densa; muchas afirmaciones externas |
| Discusión | `05_discusion.tex` | **Alta** | Interpretativa; alta detección IA; claims externos |
| Conclusiones | `06_conclusiones.tex` | **Alta** | Recomendaciones con citas |
| Metodología | `03_metodologia_diseno.tex` | Media | Protocolos (fuente = fabricante/primaria); pocos claims externos |
| Resultados | `04_analisis_datos.tex` | Baja | Datos propios; verificar solo las citas de contraste |
| Resumen/Abstract | `01_preliminares/07,08` | Media | Debe reflejar resultados reales |

## 2. Método (subagentes por sección/subsección)

**Paso 0 — Mapa cita→PDF.** Construir el mapeo `clave \cite{} → archivo en Recursos/fuentes/` (los nombres son DOIs/hashes). Se guarda en `auditoria/mapa_citas.csv`. Sin este mapa los subagentes no encuentran el PDF.

**Paso 1 — Un subagente por bloque** (≈10–12 en total):
- Intro-A: Antecedentes + Problemática
- Intro-B: Vigilancia basada en aguas residuales + Importancia + Muestreo pasivo
- Intro-C: Virus de interés (SARS-CoV-2, RSV, Enterovirus)
- Intro-D: Técnicas + Secuenciación + Herramientas bioinformáticas
- Intro-E: Contexto epidemiológico + Justificación + Problema/objetivos
- Met-A / Met-B: Metodología (solo claims con `\cite` a literatura, no protocolos de fabricante)
- Res: Resultados (solo citas de contraste)
- Dis-A / Dis-B: Discusión
- Con: Conclusiones

**Entrada a cada subagente:** los párrafos de su bloque, sus claves `\cite`, y el mapa cita→PDF.

**Tarea del subagente:**
1. Descomponer cada párrafo en **afirmaciones atómicas**.
2. Para cada afirmación, localizar la(s) fuente(s) citada(s) y **leer el PDF** (resumen, resultados, discusión, tablas).
3. Emitir **veredicto** y **página exacta** de traza.
4. Si es **vaga / inexacta / sin respaldo**, indicar **qué dice realmente la fuente** (con cifra y página) para reemplazarla.
5. Si la **fuente falta en el repo**, marcarlo (`SIN_FUENTE`) para descargar (si es acceso abierto) o sustituir.
6. **Prohibido** inventar o inferir; si no se encuentra el respaldo, se marca `NO`.

**Salida:** filas para la hoja `auditoria/trazabilidad_fuentes.csv` (formato en §4).

## 3. Reglas de veredicto

| Veredicto | Significado |
|---|---|
| `OK` | La fuente dice exactamente eso; página localizada |
| `PARCIAL` | Respaldo parcial / matiz distinto; requiere ajuste |
| `NO` | La fuente no lo dice / contradice el texto |
| `VAGA` | Afirmación sin valor concreto que la fuente sí ofrece → reemplazar por el dato real |
| `SIN_FUENTE` | La clave citada no tiene PDF en el repo |

## 4. Esquema de la hoja de cálculo (`trazabilidad_fuentes.csv`)

Columnas:

1. `id` — identificador del párrafo/afirmación (p. ej. `DIS-LINSARS-02`)
2. `seccion`
3. `subseccion`
4. `ubicacion` — `archivo:linea`
5. `idea` — la afirmación tal como está redactada
6. `citas` — claves `\cite{}` que la respaldan
7. `fuente_en_repo` — `S` / `N` / `parcial`
8. `veredicto` — `OK` / `PARCIAL` / `NO` / `VAGA` / `SIN_FUENTE`
9. `pagina_traza` — página exacta del PDF donde está el respaldo
10. `tipo_problema` — `—` / `vaga` / `inexacta` / `sin_fuente` / `no_respaldado`
11. `accion` — `mantener` / `corregir` / `reemplazar` / `conseguir_fuente`
12. `idea_real_fuente` — lo que la fuente dice de verdad (cifra + texto), para la corrección
13. `notas`

## 5. Flujo de corrección

Para cada fila con `accion ≠ mantener`:
1. Se muestra al usuario la idea vaga/errónea y la **idea real** (con página).
2. Se propone la reescritura **anclada en el dato verificado**.
3. Se aplica en `Latex/` tras aprobación, se recompila y se commitea.
4. Se marca la fila como resuelta.

## 6. Fuentes faltantes

Como `Bruno_2025`: si la clave está citada pero el PDF no está en `Recursos/fuentes/`:
- Si es **acceso abierto** → descargar el PDF al repo y verificar.
- Si no → marcar `conseguir_fuente` y decidir con el usuario (sustituir por fuente del repo o eliminar el claim).

## 7. Checklist de progreso

- [x] `Bruno_2025` descargado + claim de Ecuador corregido con datos reales (Tabla 2: 12 619 genomas, 1,15 %, serie 2020–2024)
- [ ] Paso 0: mapa cita→PDF completo
- [ ] Intro-A · Intro-B · Intro-C · Intro-D · Intro-E
- [ ] Met-A · Met-B
- [ ] Res
- [ ] Dis-A · Dis-B
- [ ] Con
- [ ] Barrido de todas las filas `VAGA`/`NO`/`SIN_FUENTE` → corregidas
