Diccionario Técnico de Variables – EVARISIS Gestor H.U.V (v1.1)

data_extraction.py
- `ENABLE_PROCESSORS` (bool): habilita el enrutamiento a procesadores especializados definido en `config.ini`.
- `detect_report_type(text)` (func): detecta tipo de informe por número de petición/encabezados.
- `split_full_name(full_name)` (func): separa nombre completo en 4 componentes.
- `calculate_birth_date(edad_str, fecha_ref)` (func): deriva fecha de nacimiento desde edad + fecha de referencia.
- `convert_date_format(date_str)` (func): normaliza fechas a `DD/MM/YYYY`.
- `_normalize_text(u)` (func): normaliza texto (tildes y mayúsculas) para búsquedas robustas.
- `detect_malignancy(*texts)` (func): detecta presencia de malignidad por palabras clave.
- `deduce_specialty(servicio, tipo_informe)` (func): asigna especialidad a partir del servicio/tipo.
- `determine_hospitalization(servicio, tipo_informe)` (func): determina estado de hospitalización.
- `extract_specimens(organo_text, numero_peticion)` (func): extrae múltiples especímenes (A., B., C.).
- `extract_huv_data(text)` (func): orquestación de extracción (regex `PATTERNS_HUV`) + normalizaciones.
- `process_text_to_excel_rows(text, filename)` (func): alto nivel, detecta tipo y enruta a procesadores o ruta base.
- `extracted_data` (dict): estructura intermedia con campos crudos/normalizados previo a mapeo Excel; claves típicas: `nombre_completo`, `numero_peticion`, `identificacion_numero`, `tipo_documento`, `genero`, `edad`, `eps`, `medico_tratante`, `servicio`, `fecha_ingreso`, `fecha_informe`, `descripcion_macroscopica`, `descripcion_microscopica`, `diagnostico`, `comentarios`, `malignidad`, `especialidad_deducida`, `hospitalizado`, `cups_code`, `procedimiento`, `specimens`.

huv_constants.py
- `HUV_CONFIG` (dict): parámetros institucionales por defecto (sede, municipio, documento, tarifas).
- `CUPS_CODES` (dict): mapeo tipo de informe → código CUPS.
- `PROCEDIMIENTOS` (dict): código CUPS → descripción de procedimiento.
- `ESPECIALIDADES_SERVICIOS` (dict): heurística servicio → especialidad.
- `PATTERNS_HUV` (dict): patrones regex definitivos por campo (incluye secciones largas y límites por encabezados).
- `MALIGNIDAD_KEYWORDS` (list[str]): palabras clave para detección de malignidad.

ocr_processing.py
- `DPI` (int): resolución de render para OCR (por defecto 300).
- `PSM_MODE` (int): modo de segmentación de páginas de Tesseract.
- `LANGUAGE` (str): idioma de OCR (por defecto `spa`).
- `_extra_config` (str): banderas adicionales para Tesseract, limpiadas de `--psm`.
- `FIRST_PAGE`/`LAST_PAGE` (int): rango opcional de páginas a procesar.
- `MIN_WIDTH` (int): reescalado mínimo de imagen para mejorar OCR.
- `pdf_to_text_enhanced(pdf_path)` (func): pipeline PDF → imagen → OCR acumulando texto por página.

huv_ocr_sistema_definitivo.py
- `main()` (func): inicializa Tk y lanza `HUVOCRSystem` (UI).

ui.py
- `HUVOCRSystem` (class): interfaz Tkinter.
  - `files` (list[str]): rutas de PDFs a procesar.
  - `output_dir` (str): carpeta de destino Excel.
  - `progress_bar` (ttk.Progressbar): estado de procesamiento.
  - Métodos clave: `add_files()`, `add_folder()`, `select_output_dir()`, `start_processing()` y `_log()`.
  - Depende de `process_text_to_excel_rows` para convertir texto OCR en filas Excel.

huv_ocr_sistema_definitivo.py (inyectado v1.1)
- `start_processing_ihq_avanzado(self)` (func): método asociado dinámicamente a `HUVOCRSystem` que:
  - Solicita PDFs IHQ y carpeta de salida (Tk dialogs).
  - Llama a `procesador_ihq_biomarcadores.process_ihq_paths(paths, outdir)`.
  - Muestra mensajes de éxito/error.

procesador_ihq_biomarcadores.py (nuevo en v1.1)
- `process_ihq_paths(paths: list[str], output_dir: str) -> Path`: orquesta el OCR y genera un Excel extendido (55 + 8 columnas IHQ) solo para IHQ.
- `_extract_biomarkers(text: str) -> dict`: extrae campos avanzados de IHQ.
- Columnas adicionales (solo en Excel IHQ extendido): `IHQ_HER2`, `IHQ_KI-67`, `IHQ_RECEPTOR_ESTROGENO`, `IHQ_RECEPTOR_PROGESTAGENOS`, `IHQ_PDL-1`, `IHQ_ESTUDIOS_SOLICITADOS`, `IHQ_P16_ESTADO`, `IHQ_P16_PORCENTAJE`.

procesador_autopsia.py / procesador_ihq.py / procesador_biopsia.py / procesador_revision.py
- `PATTERNS_*` (dict): patrones especializados por tipo de informe.
- `extract_*_data(text)` (func): extracción y normalización específica.
- `map_to_excel_format(...)` (func): construcción de filas en el orden de 55 columnas.
- Variables de soporte frecuentes: `row_data` (dict), `EXCEL_COLUMNS` (list[str]).

Notas
- v1.1 mantiene el esquema operativo estándar (55 columnas) intacto; el análisis avanzado de IHQ se realiza en un Excel separado vía módulo dedicado.
