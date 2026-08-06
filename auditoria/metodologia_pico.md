# Metodología PICOC para la columna `refuerzo_pico`

## Objetivo
Para CADA afirmación de la hoja `trazabilidad_fuentes.csv`, añadir una **idea de refuerzo** extraída **textualmente** de un PDF del repositorio, con trazabilidad (archivo + página). El refuerzo debe **aportar evidencia adicional** al tema de la afirmación, preferentemente desde una **fuente distinta** a la ya citada.

## Marco PICOC (adaptado a vigilancia viral en aguas residuales)
Cada afirmación se descompone en su pregunta PICOC antes de buscar el refuerzo:

- **P — Population / Problem:** la muestra o el agente (influente/aguas residuales; SARS-CoV-2, RSV, enterovirus/poliovirus; población conectada al alcantarillado).
- **I — Intervention / Interest:** la acción de vigilancia (EBAR, muestreo pasivo, RT-qPCR, PCR por amplicones, secuenciación Nanopore/Illumina, bioinformática/asignación de linajes).
- **C — Comparison:** el contraste (vs vigilancia clínica; entre métodos; entre virus/subgrupos; entre matrices sólido/líquido).
- **O — Outcome:** el desenlace medido (correlación con clínica, sensibilidad/cobertura, lead time, costo, detección de linajes/variantes).
- **C — Context:** el entorno (LMIC, sitio centinela urbano, país con IPV, pandemia, temporada respiratoria).

## Regla de extracción
1. El refuerzo debe ser **cita literal** entre comillas del PDF, con `(archivo, p.X)`.
2. Debe **coincidir con al menos P + I + (O o C)** de la afirmación (relevancia PICOC).
3. Preferir una **fuente NO citada aún** en esa afirmación (triangulación); si la mejor evidencia está en la misma fuente pero en otra página/dato, se acepta indicándolo.
4. **Prohibido** parafrasear o inventar en la columna de refuerzo: solo texto literal verificable.
5. Si no existe refuerzo pertinente en el repositorio, se marca `sin refuerzo disponible`.

## Salida
Nueva columna `refuerzo_pico` en `trazabilidad_fuentes.csv`, con formato:
`PICOC[<P/I/C/O/C resumido>] — "<cita literal>" (<archivo>, p.X)`
