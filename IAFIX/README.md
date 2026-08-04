# Plantilla TFM USFQ

Esta carpeta contiene la plantilla LaTeX para Trabajo Final de Posgrado de la USFQ, adaptada desde `Recursos/Plantilla.docx`.

Edita primero `config/datos.tex`; allí están los campos de portada, aprobación y derechos de autor. Los campos en rojo se generan con `\USFQCampo{...}` y deben reemplazarse antes de entregar el documento.

Estructura principal:

- `main.tex`: documento maestro.
- `preambulo/preambulo.tex`: formato USFQ, estilos, bibliografía, tablas e índices.
- `secciones/00_guia`: hoja de instrucciones de la plantilla Word.
- `secciones/01_preliminares`: portada, aprobación, derechos, resumen, abstract e índices.
- `secciones/02_cuerpo`: introducción, revisión de literatura, metodología, análisis y conclusiones.
- `secciones/03_finales`: referencias, índice de anexos y anexos.
- `assets/bibliografia.bib`: base BibTeX para referencias APA.
- `assets/figuras`: imágenes propias del nuevo documento.
- `assets/tablas`: tablas extensas reutilizables con `longtblr`/`tabularray`.

Para ocultar la hoja de guía, cambia `\USFQIncluirGuiatrue` por `\USFQIncluirGuiafalse` en `preambulo/preambulo.tex`.

Para compilar:

```bash
make
```

La carpeta `build/` y los PDF de `out/` son artefactos generados y quedan ignorados por Git.

Para limpiar:

```bash
make clean
```
