# Informe Global del Proyecto — OCR Médico HUV

## Tabla de Contenidos
- [Resumen Ejecutivo](#resumen-ejecutivo)
- [Autoría y Gobierno del Proyecto](#autoría-y-gobierno-del-proyecto)
- [Capacidades Clave](#capacidades-clave)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Flujo de Proceso (App Principal)](#flujo-de-proceso-app-principal)
- [Esquema de Datos (55 columnas)](#esquema-de-datos-55-columnas)
- [Integración de Procesadores](#integración-de-procesadores)
- [Calidad, Seguridad y Operación](#calidad-seguridad-y-operación)
- [Hoja de Ruta y Planes de Mejora](#hoja-de-ruta-y-planes-de-mejora)
- [Cómo Ejecutar](#cómo-ejecutar)
- [Recursos y Dependencias](#recursos-y-dependencias)
- [Conclusión](#conclusión)

## Resumen Ejecutivo
- Objetivo: Automatizar la extracción de datos clínico‑patológicos desde informes PDF del Hospital Universitario del Valle (HUV) con OCR (Tesseract), normalizar información y generar Excel listos para uso clínico/administrativo.
- Alcance actual: App de escritorio con GUI (Tkinter) para lotes; OCR optimizado; extracción robusta por expresiones regulares; mapeo a 55 columnas; estilos en Excel; logs y artefactos de depuración.
- Extensión: Procesadores especializados por plantilla (Autopsia, IHQ, Biopsia, Revisión) operativos en modo independiente y enrutable desde la app principal.

## Autoría y Gobierno del Proyecto
- Área responsable: Área de Innovación y Desarrollo del HUV.
- Dirección médica: Liderado por el Jefe Médico de Oncología, Dr. Juan Camilo Bayona.
- Propósito institucional: Reducir tiempos de registro, mejorar calidad de datos y habilitar analítica clínica en patología oncológica.

## Capacidades Clave
- OCR de PDFs escaneados (PyMuPDF + Tesseract) con parámetros ajustables (`config.ini`).
- Extracción de campos clínicos y administrativos (identificación, servicio, fechas, macro/micro/diagnóstico/comentarios, órgano/especímenes, responsables, malignidad, etc.).
- Normalizaciones: nombre completo, edad → fecha de nacimiento, formatos de fecha, números de identificación.
- Mapeo a Excel (55 columnas) con formato profesional (encabezados y ancho ajustado).
- Procesamiento por lotes con barra de progreso y registro de eventos.
- Depuración: guarda texto OCR por PDF para revisión rápida.

## Arquitectura del Sistema
- `huv_ocr_sistema_definitivo.py`: punto de entrada; configura Tesseract por SO y lanza GUI (`ui.HUVOCRSystem`).
- `ui.py`: interfaz gráfica; orquesta OCR → extracción → mapeo → exportación; administra logs y progreso.
- `ocr_processing.py`: render de páginas PDF, preprocesado y OCR con Tesseract (DPI, PSM, idioma, reescalado).
- `data_extraction.py`: extracción y normalizaciones base (regex `PATTERNS_HUV`, detección de tipo, specimens, malignidad) y mapeo a 55 columnas.
- `huv_constants.py`: constantes y tablas (CUPS, procedimientos, especialidades, patrones regex, defaults del HUV).
- Procesadores especializados:
  - `procesador_autopsia.py`: autopsias; 1 muestra (Cuerpo humano completo); hospitalizado=SI; CUPS/Procedimiento propios.
  - `procesador_ihq.py`: Inmunohistoquímica; adaptado a ambas plantillas; ambulatorio, COEX, identificador=0.
  - `procesador_biopsia.py`: biopsias con múltiples especímenes (A., B., C.); genera N filas por informe.
  - `procesador_revision.py`: revisión de casos externos; extracción dedicada y mapeo a 1 fila.
- Utilidades: `instalar_dependencias.py`, `crear_ejecutable.py`, `test_sistema.py`.

## Flujo de Proceso (App Principal)
1) Selección de PDFs y carpeta de salida (GUI).
2) OCR por página (PyMuPDF → PIL → Tesseract) con reescalado y PSM configurables.
3) Enrutamiento por tipo: `data_extraction.process_text_to_excel_rows` delega a Autopsia/IHQ/Biopsia/Revisión si están habilitados; si no, usa la extracción base.
4) Mapeo a 55 columnas (mapeo del procesador o mapeo base según corresponda).
5) Exportación a Excel (pandas + openpyxl) con estilos.
6) Logs + artefacto de depuración: `DEBUG_OCR_OUTPUT_<pdf>.txt`.

## Esquema de Datos (55 columnas)
- Conjunto estandarizado utilizado por el HUV: identificación del caso y paciente, atención/servicio, autorizaciones, fechas (ingreso/ordenamiento/finalización), especialidad, hospitalización, CUPS/procedimiento, órgano/muestra, descripciones macro/micro/diagnóstico, malignidad, comentarios y campos de auditoría (usuario, hora desc. macro, responsable macro).

## Integración de Procesadores
- Enrutador activo: `data_extraction.process_text_to_excel_rows` detecta tipo y delega a procesadores (Autopsia, IHQ, Biopsia, Revisión) cuando está habilitado por configuración.
- Fallback: `extract_huv_data` + `map_to_excel_format` para tipos no soportados o cuando se deshabilita.
- Activación/Desactivación: `[PROCESSORS].ENABLE_PROCESSORS` en `config.ini` (true/false).
- Detalles técnicos: `analisis/14_integracion_procesadores.md`.

## Calidad, Seguridad y Operación
- Codificación: UTF‑8 extremo a extremo; sanitización de caracteres en extracción.
- Robustez de regex: uso de delimitadores por encabezados y `re.DOTALL`, con planes para `PATTERNS_BASE` y overrides por procesador.
- Rendimiento: el costo está dominado por OCR; la modularización mejora mantenibilidad.
- Operación: procesamiento por lotes no bloqueante; logs con conteos de archivos/errores/filas.
- Compatibilidad: Windows/Linux/macOS; ejecutable con PyInstaller opcional (requiere Tesseract instalado).

## Hoja de Ruta y Planes de Mejora
- Integración con SERVINTE (planeada): ver `SERVINTE_PLAN.md`.
  - Exportación por lotes (CSV/API), validaciones, reintentos y bitácora de auditoría.
  - Modo “dry‑run” y parametrización en `config.ini` (endpoints, autenticación, timeouts).
  - Resguardos con colas locales y respaldos por lote.
- Extracción más robusta
  - Unificar utilidades en módulo compartido; crear `PATTERNS_BASE` para reducir duplicación.
  - Mejorar detección de tipo con clasificadores ML ligeros y heurísticas adicionales.
  - Aumentar cobertura de patrones para nuevas variantes de plantillas.
- Experiencia de usuario
  - Estado por archivo con resumen de campos clave y validaciones previas al exportar.
  - Reintentos selectivos y re‑OCR para páginas conflictivas.
  - Modo CLI headless para automatizaciones planificadas (tareas programadas/cron).
- Calidad y pruebas
  - Pruebas unitarias por procesador y regresión de patrones con textos anonimizados.
  - Dataset de ejemplo expandido (sin datos sensibles) para QA.
- Despliegue y gestión
  - Contenedorización opcional y empaquetado multi‑plataforma.
  - Telemetría opcional (local) de performance y errores, con opt‑in institucional.
  - Hardening de seguridad (manejo seguro de credenciales, aislamiento de procesos OCR).

## Cómo Ejecutar
- App principal (GUI): `python huv_ocr_sistema_definitivo.py`.
- Procesadores individuales:
  - `python procesador_autopsia.py`
  - `python procesador_ihq.py`
  - `python procesador_biopsia.py`
  - `python procesador_revision.py`

## Recursos y Dependencias
- Python 3.7+; ver `requirements.txt` o ejecutar `instalar_dependencias.py`.
- Tesseract OCR instalado y `spa.traineddata` disponible.
- PDFs de ejemplo en `pdfs_patologia/` y artefactos de depuración en `EXCEL/` (en ejemplos) o en la carpeta de salida.

## Conclusión
Proyecto institucional del HUV (Innovación y Desarrollo), dirigido por el Dr. Juan Camilo Bayona. La versión actual entrega valor inmediato con extracción confiable y exportación estándar, y mantiene una ruta clara para evolucionar hacia integración automática con SERVINTE, mayor robustez, mejor UX y operación escalable.
