# Análisis: `requirements.txt` y dependencias

## Dependencias directas
- `pytesseract`: Wrapper de Tesseract OCR.
- `PyMuPDF` (`fitz`): Renderizado de PDF a imágenes/objetos.
- `pillow`: Manejo de imágenes (PIL).
- `pandas`: Construcción de DataFrames y exportación a Excel.
- `openpyxl`: Motor de Excel y formateo.
- `python-dateutil`: Cálculos precisos de fechas (relativedelta).

## Dependencias del sistema
- Tesseract OCR (binario): Debe estar instalado y accesible.
- Datos de idioma de Tesseract: `spa.traineddata` (instalado en la ruta de datos de Tesseract).
- Poppler-utils (opcional): no se usa directamente en código actual, pero útil si se añade extracción alternativa.

## Notas de instalación
- Windows: usar instalador de Tesseract y verificar ruta en `config.ini`.
- Linux/macOS: paquetes vía gestor (apt/brew) según README/INICIO_RAPIDO.

