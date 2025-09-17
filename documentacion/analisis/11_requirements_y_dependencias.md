# Analisis: `requirements.txt` y dependencias

## Dependencias directas (v2.5)
- `pytesseract`: wrapper de Tesseract OCR.
- `PyMuPDF` (`fitz`): renderizado de PDF.
- `pillow`: manejo de imagenes.
- `pandas`: DataFrames y transformaciones.
- `openpyxl`: escritor Excel (legacy/compatibilidad).
- `python-dateutil`: manejo de fechas.
- `customtkinter`: interfaz moderna.
- `matplotlib` y `seaborn`: graficos para dashboard.
- `selenium`: automatizacion del portal.
- `webdriver-manager`: descarga automatica del driver de Chrome.
- `ttkbootstrap`: estilos y tooltips avanzados.
- `Babel`: localizacion (meses, dias).
- `holidays`: calculo de festivos.

## Dependencias indirectas importantes
- `numpy`: requerido por pandas/matplotlib.
- `tkinter`: incluido con Python (verificar en distribuciones minimalistas).

## Dependencias del sistema
- Tesseract OCR + datos de idioma (`spa.traineddata`).
- Google Chrome (para Selenium).
- Poppler-utils (opcional para futuras conversiones PDF).

## Notas de instalacion
- Windows: usar instalador oficial de Tesseract y actualizar `config.ini` con la ruta.
- Linux/macOS: instalar Tesseract via apt/brew segun README/INICIO_RAPIDO.
- Para Selenium, confirmar que la red permita descargar el driver la primera vez.

## Recomendaciones
- Mantener `requirements.txt` alineado con la version del proyecto.
- Usar entornos virtuales para aislar dependencias.
- Documentar versiones minimas cuando se identifiquen incompatibilidades.