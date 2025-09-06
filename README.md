# OCR Médico HUV — Procesador de Informes PDF

Aplicación de escritorio en Python para procesar informes de Patología en PDF mediante OCR (Tesseract), extraer datos estructurados y exportarlos a Excel con formato.

## Características

- Interfaz gráfica (Tkinter) y procesamiento por lotes.
- OCR optimizado (Tesseract) con parámetros configurables.
- Extracción basada en regex adaptadas a informes del HUV.
- Exportación a Excel con `pandas` y formato de encabezados con `openpyxl`.
- Logs detallados y archivos de depuración de OCR por PDF.

## Requisitos del sistema

- Python 3.7+ (recomendado 3.9+)
- Windows 10+/Ubuntu 18+/macOS 10.14+
- Tesseract OCR instalado y accesible

## Instalación rápida

Opción A — Automática:
```bash
python instalar_dependencias.py
```

Opción B — Manual:
```bash
pip install -r requirements.txt
# Instala Tesseract según tu SO (ver INICIO_RAPIDO.md)
```

Ejecutar la app:
```bash
python huv_ocr_sistema_definitivo.py
```

## Configuración

Edita `config.ini`:
- `[PATHS]`: Rutas a `tesseract` por sistema (o deja vacío si está en PATH).
- `[OCR_SETTINGS]`: `DPI`, `PSM_MODE`, `LANGUAGE`, `OCR_CONFIG`.
- `[PROCESSING]`: Rango de páginas y tamaño mínimo.
- `[OUTPUT]`: Formato de nombre de archivo de salida.
- `[INTERFACE]`: Dimensiones de ventana y altura de log.

Verificación:
```bash
tesseract --version
python -c "import pytesseract, fitz, PIL, pandas, openpyxl, dateutil; print('OK')"
```

## Uso

1) Agrega PDFs (archivos o carpeta).
2) Selecciona carpeta de salida.
3) Procesa y revisa el Excel generado.

El Excel aplica formato de encabezados y ajuste de columnas automáticamente.

## Arquitectura y análisis completo

Consulta la documentación técnica en `analisis/`:
- `analisis/README.md` — índice y hojas por componente.

## Crear ejecutable (opcional)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name=OCR_Medico huv_ocr_sistema_definitivo.py
```
El ejecutable requiere Tesseract instalado en la máquina destino.

## Solución de problemas

- “Tesseract not found”: Instala Tesseract y configura `config.ini` o PATH.
- “No module named ...”: `pip install -r requirements.txt`.
- OCR pobre: aumenta `DPI`, revisa calidad del PDF, considera preprocesar.

## Notas

- Este repositorio contiene regex y mapeos específicos del HUV. Cambios en los formatos de informe requieren actualizar `huv_constants.PATTERNS_HUV`.

