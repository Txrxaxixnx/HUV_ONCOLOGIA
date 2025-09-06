# Analisis: `requirements.txt` y dependencias

## Dependencias directas
- `pytesseract`: Wrapper de Tesseract OCR.
- `PyMuPDF` (`fitz`): Renderizado de PDF a imagenes/objetos.
- `pillow`: Manejo de imagenes (PIL).
- `pandas`: Construccion de DataFrames y exportacion a Excel.
- `openpyxl`: Motor de Excel y formateo.
- `python-dateutil`: Calculos precisos de fechas (relativedelta).

## Dependencias del sistema
- Tesseract OCR (binario): Debe estar instalado y accesible.
- Datos de idioma de Tesseract: `spa.traineddata` (instalado en la ruta de datos de Tesseract).
- Poppler-utils (opcional): no se usa directamente en codigo actual, pero util si se anade extraccion alternativa.

## Notas de instalacion
- Windows: usar instalador de Tesseract y verificar ruta en `config.ini`.
- Linux/macOS: paquetes via gestor (apt/brew) segun README/INICIO_RAPIDO.
