# Informe Global del Proyecto — OCR Médico HUV

## Resumen Ejecutivo
- Objetivo: Automatizar la extracción de datos clínico-patológicos desde informes PDF del Hospital Universitario del Valle (HUV) mediante OCR, normalizar la información y generar archivos Excel listos para integrar en flujos clínicos/administrativos.
- Alcance actual: Aplicación de escritorio con GUI para procesar lotes de PDFs; OCR optimizado con Tesseract; extracción por expresiones regulares robustas; mapeo a 55 columnas estándar; formateo de encabezados; registro detallado y artefactos de depuración.
- Extensión: Procesadores especializados por plantilla (IHQ, Biopsia, Revisión) operativos en modo independiente, con plan de integración al pipeline principal.

## Capacidades Clave
- OCR de PDFs escaneados con PyMuPDF + Tesseract (parámetros configurables en `config.ini`).
- Extracción de campos clínicos y administrativos: identificación, servicio, fechas, secciones macro/micro/diagnóstico/comentarios, órgano/especímenes, responsable, malignidad, etc.
- Normalización: nombre completo, edad→fecha de nacimiento, formatos de fecha, números de identificación.
- Mapeo a Excel (55 columnas) con estilos visuales profesionales.
- Procesamiento por lotes con barra de progreso y logs.
- Depuración: guarda el texto OCR por PDF para análisis rápido.

## Ventajas Diferenciales
- Parametrización completa desde `config.ini` (sin recompilar).
- Patrones y reglas ajustadas a los layouts reales del HUV.
- Procesadores especializados por tipo, que aumentan precisión y facilitan mantenimiento.
- Generación de Excel listo para uso con estilos y ancho de columnas automático.
- Diseño modular y documentado para incorporar nuevas plantillas.

## Arquitectura del Sistema
- `huv_ocr_sistema_definitivo.py`: punto de entrada; configura Tesseract por SO y lanza la GUI (`ui.HUVOCRSystem`).
- `ui.py`: interfaz (Tkinter); orquesta por lote: OCR → extracción → mapeo → exportación; gestiona logs, progreso y avisos.
- `ocr_processing.py`: convierte páginas PDF en imágenes y aplica OCR con Tesseract; soporta DPI, PSM, idioma y reescalado.
- `data_extraction.py`: extracción estable basada en `PATTERNS_HUV` + utilidades (detección de tipo, normalizaciones, specimens, malignidad); mapeo a 55 columnas.
- `huv_constants.py`: constantes y tablas (CUPS, procedimientos, especialidades, patrones regex, keywords de malignidad, defaults HUV).
- Procesadores especializados:
  - `procesador_ihq.py`: reglas y patrones específicos IHQ.
  - `procesador_biopsia.py`: manejo de múltiples especímenes (A., B., C.).
  - `procesador_revision.py`: revisión de material externo.
- Utilidades: `instalar_dependencias.py`, `crear_ejecutable.py`, `test_sistema.py`.

## Flujo de Proceso (App Principal)
1) Selección de PDFs y carpeta de salida (GUI).
2) OCR por página (PyMuPDF → PIL → Tesseract). Reescalado a `MIN_WIDTH` y PSM configurable.
3) Extracción con `data_extraction.extract_huv_data` (regex multi-sección, normalizaciones, detección de malignidad, specimens).
4) Mapeo a 55 columnas con `data_extraction.map_to_excel_format`.
5) Exportación a Excel (pandas + openpyxl) con estilos en encabezados y ajuste de columnas.
6) Log de resultados (archivos procesados/errores/filas) y artefactos de depuración `DEBUG_OCR_OUTPUT_<pdf>.txt`.

## Procesadores Especializados (Modo Independiente)
Descripción detallada en `analisis/15_procesador_ihq.md`, `analisis/16_procesador_biopsia.md`, `analisis/17_procesador_revision.md`.

- IHQ (`procesador_ihq.py`):
  - Secciones “Informe de Estudios…”/“Se recibe orden…”, microscópica/dx, fecha de diagnóstico, responsable.
  - Reglas: ambulatorio (hospitalizado=NO), COEX como autorización, identificador=0, especialidad por servicio.
  - Mapeo a Excel de 1 fila.

- Biopsia (`procesador_biopsia.py`):
  - Secciones macro/micro/dx completas y división por letras de espécimen (A., B., C.).
  - Reglas: hospitalizado=SI, especialidad por servicio, identificador único desde encabezado, malignidad desde dx.
  - Mapeo a Excel de N filas (una por espécimen).

- Revisión (`procesador_revision.py`):
  - Secciones específicas de revisión; limpieza de “Bloques y láminas …”.
  - Reglas: hospitalizado=SI, especialidad fija (hematoonco adulto), firma de patóloga, malignidad desde dx.
  - Mapeo a Excel de 1 fila con ubicación/identificador parametrizados en el ejemplo.

## Detección de Tipo de Informe
- `data_extraction.detect_report_type(text)`:
  - Por N. de petición: `A######` (AUTOPSIA), `IHQ######` (IHQ), `M#######` (BIOPSIA), `R######` (REVISIÓN).
  - Por palabras clave en encabezado si no hay N. de petición.

## Esquema de Datos (55 columnas)
- Columnas clínicas/administrativas esperadas por HUV: N. petición, Hospitalizado, Sede, EPS, Servicio, Médico tratante, Especialidad, Ubicación, N. Autorización, Identificador Único, Datos clínicos, Fecha ordenamiento, Tipo de documento, N. de identificación, Nombre y apellidos, Fecha de nacimiento, Edad, Género, Departamento, Municipio, N. muestra, CUPS, Tipo de examen, Procedimiento, Órgano, Tarifa, Valor, Fechas ingreso/finalización, Usuario finalización, Usuario/Fecha asignación micro, Malignidad, Condición, Macroscópica, Microscópica, Diagnóstico, Diagnóstico principal, Comentario, Informe adicional, Congelaciones/Otros, Líquidos, Citometría de flujo, Hora Desc. macro, Responsable macro.
- Fuentes:
  - Datos comunes: `PATTERNS_HUV` y tablas `huv_constants`.
  - Secciones extensas: regex de bloque con límites por encabezados vecinos.
  - Especímenes: heurística por prefijos “A.”, “B.” … (multi-fila).

## Configuración (`config.ini`)
- PATHS: ruta a Tesseract por SO (o usar PATH del sistema).
- OCR_SETTINGS: DPI (p.ej. 400), PSM_MODE (6 por defecto), LANGUAGE (`spa`), OCR_CONFIG (parámetros extra de Tesseract).
- PROCESSING: FIRST_PAGE/LAST_PAGE, MIN_WIDTH (reescalado mínimo para legibilidad OCR).
- OUTPUT: formato de timestamp y nombre base del Excel.
- INTERFACE: dimensiones y altura del log.

## Calidad y Rendimiento
- OCR depende de DPI, idioma y calidad del escaneo; `MIN_WIDTH` evita OCR sobre imágenes pequeñas.
- Regex multi-sección evita “over-capture” y mantiene bloques delimitados.
- Proceso por lotes con hilo en segundo plano para no bloquear la UI.

## Pruebas y Depuración
- `test_sistema.py`: smoke tests de dependencias, Tesseract y regex de ejemplo.
- Artefactos de texto OCR por PDF (carpeta `EXCEL/` en ejemplos y en carpeta de salida del usuario).
- PDFs de ejemplo en `pdfs_patologia/`.

## Integración de Procesadores
- Enrutador activo: `data_extraction.process_text_to_excel_rows` detecta tipo y delega a procesadores (IHQ, Biopsia, Revisión) cuando están habilitados.
- Fallback: se mantiene `extract_huv_data` + `map_to_excel_format` para tipos no soportados o cuando se deshabilita.
- Bandera de activación: `[PROCESSORS].ENABLE_PROCESSORS` en `config.ini` (true/false).
- Más detalles: `analisis/14_integracion_procesadores.md`.

## Limitaciones Actuales
- Dependencia de layouts y encabezados: cambios de plantilla requieren actualizar regex.
- Algunos campos fijos de ejemplo (p.ej., fecha de ordenamiento en Biopsia) deben generalizarse.
- Codificación: garantizar UTF-8 de extremo a extremo para evitar caracteres extraños en entornos con CP locales.

## Hoja de Ruta
- Unificar utilidades comunes en un módulo compartido.
- Extraer `PATTERNS_BASE` y reducir duplicación entre procesadores.
- Añadir pruebas unitarias y de regresión con textos reales anonimizados.
- Integración completa de procesadores con conmutador en `config.ini`.
- Modo CLI headless para automatización por lotes.

## Cómo Ejecutar
- App principal (GUI): `python huv_ocr_sistema_definitivo.py`.
- Procesadores individuales:
  - `python procesador_ihq.py`
  - `python procesador_biopsia.py`
  - `python procesador_revision.py`

## Recursos y Dependencias
- Python: ver `requirements.txt` o ejecutar `instalar_dependencias.py`.
- Tesseract OCR instalado y `spa.traineddata` presente.
- Windows/Linux/macOS soportados.

## Conclusión
El proyecto ofrece un pipeline robusto y extensible para procesar informes de Patología del HUV, con una base estable y procesadores especializados listos para integrarse. La documentación y el plan de integración facilitan su evolución y despliegue controlado, maximizando precisión y manteniendo la mantenibilidad a largo plazo.
