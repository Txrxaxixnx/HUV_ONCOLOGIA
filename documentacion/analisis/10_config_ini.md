# Analisis: `config.ini`

## Secciones y claves
- `[PATHS]`: rutas especificas de Tesseract por sistema (dejar vacio si esta en PATH).
- `[OCR_SETTINGS]`: `DPI`, `PSM_MODE`, `LANGUAGE`, `OCR_CONFIG` controlan el comportamiento de Tesseract.
- `[PROCESSING]`: `FIRST_PAGE`, `LAST_PAGE` y `MIN_WIDTH` definen el rango de paginas y reescalado.
- `[OUTPUT]`: `TIMESTAMP_FORMAT`, `OUTPUT_FILENAME` (heredados para exportaciones Excel legacy).
- `[INTERFACE]`: tamanio de ventana y altura del log (mantiene compatibilidad; la UI moderna usa valores propios).
- `[PROCESSORS]`: `ENABLE_PROCESSORS` (bandera legacy, ya no afecta la UI v2.5).

## Impacto en v2.5
- `huv_ocr_sistema_definitivo.py` usa `[PATHS]` para configurar Tesseract antes de iniciar la UI.
- `ocr_processing.py` lee `[OCR_SETTINGS]` y `[PROCESSING]` para renderizar y aplicar OCR.
- La UI moderna no utiliza `[OUTPUT]` ni `[PROCESSORS]`, pero se conservan para compatibilidad e integraciones externas.

## Buenas practicas
- Mantener el archivo en UTF-8 y documentar cambios cuando se modifique DPI o PSM.
- En Windows usar rutas con doble barra (`C:\Program Files\...`).
- Si se distribuye un ejecutable, incluir `config.ini` editable junto al binario.

## Ideas futuras
- Exponer opciones adicionales (ruta de la base SQLite, modo headless de Selenium) via nuevas secciones.
- Eliminar o marcar como deprecadas las claves que pertenecen al pipeline legacy cuando Biopsia/Autopsia/Revision migren a SQLite.
- Validar automaticamente la existencia de Tesseract al iniciar y guiar al usuario si falta.