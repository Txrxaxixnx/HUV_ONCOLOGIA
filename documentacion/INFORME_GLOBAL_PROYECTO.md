EVARISIS Gestor H.U.V: Informe Global del Proyecto

Versión del software: v1.1 (10/09/2025)
Fecha de esta actualización documental: 10/09/2025

Resumen Ejecutivo
- EVARISIS Gestor H.U.V es la plataforma institucional para estructurar y analizar datos clínicos verídicos provenientes de informes de patología, fortaleciendo la toma de decisiones, la investigación y la gestión de recursos del HUV.
- La versión actual (v1.1) automatiza la extracción desde PDFs, normaliza la información y la entrega en un esquema operativo validado de 55 columnas. Incluye procesadores especializados (Autopsia, IHQ, Biopsia, Revisión) y agrega un análisis avanzado de IHQ mediante un botón en la interfaz que genera un Excel separado con biomarcadores (HER2, Ki‑67, RE/ER, RP/PR, PD‑L1, P16 y Estudios Solicitados).

Visión Estratégica
- Misión: Transformar informes de patología del HUV en un activo de datos centralizado para decisiones clínicas, investigación y gestión.
- Objetivos estratégicos:
  - Inteligencia de negocio hospitalaria (Power BI).
  - Investigación clínica y epidemiológica (énfasis en IHQ y moleculares).
  - Optimización de recursos (análisis predictivo para convenios/farmacéuticas).
  - Automatización de procesos (desde OCR hasta integración con SERVINTE).
  - Soporte a decisiones clínicas (bases para IA futura).

Gobernanza y Roles
- Líder de Proyecto e Investigador Principal: Dr. Juan Camilo Bayona (Jefe Médico de Oncología).
- Desarrollador Principal: Ing. Daniel Restrepo (Área de Innovación y Desarrollo, GDI).
- Entidad Ejecutora: Área de Innovación y Desarrollo del HUV Evaristo García.
- Jefe de Gestión de la Información (GDI): Ing. Diego Peña.

Alcance Actual (v1.1)
- OCR (PyMuPDF + Tesseract) y extracción por expresiones regulares.
- Mapeo a esquema operativo de 55 columnas y exportación a Excel.
- Procesadores especializados: Autopsia, IHQ, Biopsia, Revisión.
- Análisis avanzado de IHQ: botón en la UI “Analizar Biomarcadores IHQ (v1.1)” que produce un Excel extendido con biomarcadores.
- Artefactos operativos: logs, archivos de depuración OCR y UI para procesamiento por lotes.

Hoja de Ruta (Roadmap)
- Fase 1 – Fundación y Validación (Completada – v1.0):
  - Motor de OCR y app de escritorio.
  - Procesadores especializados para cuatro plantillas base (Biopsia, IHQ, Autopsia, Revisión).
  - Salida validada a Excel de 55 columnas.
- Fase 2 – Enriquecimiento de Datos para Investigación (v1.1 liberada y en avance):
  - Análisis avanzado de IHQ (v1.1): biomarcadores clave (HER2, Ki‑67, RE/ER, RP/PR, PD‑L1, P16, Estudios Solicitados) en Excel separado.
  - Próximo: Módulo de adquisición automatizada (scraper institucional) para `huvpatologia.qhorte.com` con login, descarga masiva y organización de PDFs.
- Fase 3 – Centralización y Visualización de Datos:
  - Migración de Excel a base de datos centralizada (SQL o similar).
  - Dashboards y reportes dinámicos en Power BI.
- Fase 4 – Integración y Automatización Sistémica:
  - Módulo de integración con SERVINTE (carga automática y segura de datos).
  - Escalamiento a otras áreas de alto costo.
- Fase 5 – Inteligencia Aumentada:
  - Modelos predictivos (demanda de medicamentos, tendencias).
  - Asistente de IA para soporte diagnóstico (conocimiento validado y data histórica).

Metodología y Gestión del Proyecto
- Versionamiento: semántico. Versión estable v1.1 consolidada el 10/09/2025.
- Historial de cambios: `CHANGELOG.md` como fuente de verdad del histórico.
- Trazabilidad: `BITACORA_DE_ACERCAMIENTOS.md` para registrar reuniones, acuerdos y seguimiento.

Activos y Fuentes de Datos
- Esquemas de datos de referencia:
  - Esquema operativo (55 columnas): estándar validado de salida actual.
  - Esquema Maestro H.U.V (167 columnas): formato exhaustivo institucional (guía para el enriquecimiento futuro).
- Fuente primaria de informes (PDFs):
  - Portal de Patología H.U.V: `https://huvpatologia.qhorte.com/index.php` (acceso solo intranet HUV).
- Fuentes de conocimiento científico (para futura IA):
  - CAP: `https://www.cap.org/protocols-and-guidelines/cancer-reporting-tools/cancer-protocol-templates`
  - Pathology Outlines: `https://www.pathologyoutlines.com/`
  - OMS Libros Azules: `https://tumourclassification.iarc.who.int/home` (acceso con credenciales).

Arquitectura (Resumen)
- `huv_ocr_sistema_definitivo.py`: punto de entrada y GUI.
- `ocr_processing.py`: renderizado PDF e interfaz con Tesseract.
- `data_extraction.py`: extracción/normalización y mapeo a 55 columnas.
- `huv_constants.py`: constantes, CUPS/procedimientos, patrones.
- Procesadores: `procesador_autopsia.py`, `procesador_ihq.py`, `procesador_biopsia.py`, `procesador_revision.py`.

Ejecución Básica
- App principal: `python huv_ocr_sistema_definitivo.py`
- Requisitos: Tesseract instalado; dependencias de `requirements.txt`.

Notas Finales
- La v1.1 entrega valor inmediato, añade análisis avanzado de IHQ y sienta la base técnica para centralización, visualización estratégica, integración con SERVINTE e inteligencia aumentada.
