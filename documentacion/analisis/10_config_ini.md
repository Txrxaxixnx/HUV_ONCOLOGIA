# Analisis: `config.ini`

## Secciones y claves
- `[PATHS]`:
  - `WINDOWS_TESSERACT`, `MACOS_TESSERACT`, `LINUX_TESSERACT`: rutas al ejecutable de Tesseract por sistema. Si esta en `PATH`, puede dejarse en blanco.
- `[OCR_SETTINGS]`:
  - `DPI`, `PSM_MODE`, `LANGUAGE`, `OCR_CONFIG`: parametros OCR. Ver documentacion de Tesseract para `--psm` y `-c`.
- `[PROCESSING]`:
  - `FIRST_PAGE`, `LAST_PAGE`: controla el rango de paginas; `0` en `LAST_PAGE` significa "hasta el final".
  - `MIN_WIDTH`: reescalado minimo antes del OCR (mejora reconocimiento).
- `[OUTPUT]`:
  - `TIMESTAMP_FORMAT`, `OUTPUT_FILENAME`: nombre del Excel resultante.
- `[INTERFACE]`:
  - Tamano de ventana y altura del log.

## Nueva sección `[PROCESSORS]`
- `ENABLE_PROCESSORS`: `true|false` para activar la integración con procesadores especializados (IHQ, Biopsia, Revisión).
  - Cuando `true`, el sistema enruta automáticamente el texto OCR al procesador según `detect_report_type`.
  - Cuando `false`, usa siempre la ruta base (`extract_huv_data` + `map_to_excel_format`).

## Efecto en el sistema
- `huv_ocr_sistema_definitivo.py` y `ocr_processing.py` leen estas claves al inicio de la ejecucion.
- Cambios se reflejan sin recompilar.

## Sugerencias
- Mantener codificacion UTF-8 y rutas absolutas en Windows con doble barra `C:\\...` si se edita a mano.
- Si Tesseract esta en PATH, se puede dejar el valor vacio para simplificar despliegues.
