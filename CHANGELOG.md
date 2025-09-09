# Changelog

Todos los cambios notables de este proyecto se documentarán en este archivo.
Sigue el formato de Keep a Changelog y se inspira en Semantic Versioning.

## [Unreleased]
- Integración con SERVINTE (CSV/API), validaciones, reintentos y auditoría.
- Modo CLI headless y mejoras de UX (resumen por archivo, re-OCR selectivo).
- Unificación de utilidades y `PATTERNS_BASE` para reducir duplicación.
- Pruebas unitarias/regresión por procesador con textos anonimizados.

## [2025-09-09]
### Añadido
- Nuevo procesador: `procesador_autopsia.py` (plantilla 55 columnas, 1 muestra: "Cuerpo humano completo").
- Enrutamiento del tipo Autopsia en `data_extraction.process_text_to_excel_rows`.
- Documento de plan: `SERVINTE_PLAN.md` (visión de integración y fases).

### Mejorado
- `INFORME_GLOBAL_PROYECTO.md`: versión enriquecida (autoría, arquitectura, roadmap, TOC).
- `README.md`: créditos institucionales, referencia a enrutamiento y plan SERVINTE.
- `INICIO_RAPIDO.md`: créditos y ejemplo para ejecutar Autopsia.

