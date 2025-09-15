Presentación al Equipo de Innovación y Desarrollo – EVARISIS Gestor H.U.V (v1.1)
Actualización v1.1 (10/09/2025): Botón en la UI para análisis avanzado de IHQ y extractor dedicado que generan un Excel con biomarcadores (HER2, Ki‑67, RE/ER, RP/PR, PD‑L1, P16, Estudios Solicitados) sin impactar el esquema operativo estándar.

Introducción
- Caso de éxito institucional: de PDFs a datos confiables con impacto inmediato en Oncología.

El Reto Técnico
- Trabajar con PDFs escaneados y datos no estructurados: variabilidad de plantillas, ruido, OCR y manejo robusto de expresiones regulares.

La Solución Tecnológica
- Stack: Python, Tesseract (pytesseract), PyMuPDF, PIL, Pandas, OpenPyXL, Tkinter.
- Diseño: motor OCR + capa de extracción/normalización + mapeo a esquema operativo (55 columnas) + procesadores especializados (Autopsia, IHQ, Biopsia, Revisión).

Metodología y Buenas Prácticas
- Documentación viva (esta reestructuración) y roadmap claro por fases.
- Modularidad por procesador, orquestación central y configuración en `config.ini`.
- Control de versiones (semántico) y `CHANGELOG.md` como fuente de verdad.

Roadmap Técnico
- Fase 2: enriquecimiento de IHQ con biomarcadores (HER2, KI67, RE, RP, PDL-1, Estudios Solicitados, P16[Estado/Porcentaje]).
- Scraper institucional: login seguro, búsquedas/descargas masivas, organización de PDFs.
- Fase 3: diseño de base de datos y modelo de datos interoperable; preparación de ETL.
- Fase 4: integración con SERVINTE (CSV/API, validaciones, reintentos, auditoría).
- Fase 5: exploración de ML para modelos predictivos y asistente IA.

Cierre
- Este proyecto demuestra nuestra capacidad para entregar soluciones de alto impacto. La experiencia acumulada es un activo transversal para futuras iniciativas de la GDI.
