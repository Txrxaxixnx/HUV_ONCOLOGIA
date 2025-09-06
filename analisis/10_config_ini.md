# Análisis: `config.ini`

## Secciones y claves
- `[PATHS]`:
  - `WINDOWS_TESSERACT`, `MACOS_TESSERACT`, `LINUX_TESSERACT`: rutas al ejecutable de Tesseract por sistema. Si está en `PATH`, puede dejarse en blanco.
- `[OCR_SETTINGS]`:
  - `DPI`, `PSM_MODE`, `LANGUAGE`, `OCR_CONFIG`: parámetros OCR. Ver documentación de Tesseract para `--psm` y `-c`.
- `[PROCESSING]`:
  - `FIRST_PAGE`, `LAST_PAGE`: controla el rango de páginas; `0` en `LAST_PAGE` significa “hasta el final”.
  - `MIN_WIDTH`: reescalado mínimo antes del OCR (mejora reconocimiento).
- `[OUTPUT]`:
  - `TIMESTAMP_FORMAT`, `OUTPUT_FILENAME`: nombre del Excel resultante.
- `[INTERFACE]`:
  - Tamaño de ventana y altura del log.

## Efecto en el sistema
- `huv_ocr_sistema_definitivo.py` y `ocr_processing.py` leen estas claves al inicio de la ejecución.
- Cambios se reflejan sin recompilar.

## Sugerencias
- Mantener codificación UTF-8 y rutas absolutas en Windows con doble barra `C:\\...` si se edita a mano.
- Si Tesseract está en PATH, se puede dejar el valor vacío para simplificar despliegues.

