# OCR Médico HUV — Procesador de Informes PDF

Aplicación de escritorio en Python para procesar informes de Patología del HUV en PDF mediante OCR (Tesseract), extraer datos estructurados y exportarlos a Excel con formato profesional.

## Características

- Interfaz gráfica (Tkinter) y procesamiento por lotes.
- OCR optimizado (Tesseract) con parámetros configurables.
- Extracción basada en expresiones regulares adaptadas a informes del HUV.
- Exportación a Excel con `pandas` y formato de encabezados con `openpyxl`.
- Logs detallados y archivo de depuración OCR por PDF.

## Requisitos

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

Ejecutar la app principal:
```bash
python huv_ocr_sistema_definitivo.py
```

## Configuración

Edita `config.ini`:
- `[PATHS]`: Rutas a `tesseract` por sistema (o deja vacío si está en PATH).
- `[OCR_SETTINGS]`: `DPI`, `PSM_MODE`, `LANGUAGE`, `OCR_CONFIG`.
- `[PROCESSING]`: Rango de páginas y tamaño mínimo.
- `[OUTPUT]`: Formato del nombre del archivo Excel de salida.
- `[INTERFACE]`: Dimensiones de ventana y altura del log.

Verificación:
```bash
tesseract --version
python -c "import pytesseract, fitz, PIL, pandas, openpyxl, dateutil; print('OK')"
```

## Uso (app principal)

1) Agrega PDFs (archivos o carpeta).
2) Selecciona carpeta de salida.
3) Procesa y revisa el Excel generado.

El Excel aplica formato de encabezados y ajuste de columnas automáticamente.

## Procesadores especializados (por plantilla)

Además de la app principal, el proyecto incluye procesadores independientes por tipo de informe. Funcionan de forma autónoma y generan un Excel listo para uso.

- `procesador_ihq.py`: Inmunohistoquímica (IHQ)
- `procesador_biopsia.py`: Biopsias con múltiples especímenes (A., B., C.)
- `procesador_revision.py`: Revisiones de casos externos (R)

Ejecución (abre un selector de archivo PDF):
```bash
python procesador_ihq.py
python procesador_biopsia.py
python procesador_revision.py
```

- Estado: los procesadores funcionan de forma individual y aplican reglas específicas de negocio y mapeos a Excel.
- Integración al flujo principal: ver `analisis/13_processors.md` y el plan en `analisis/14_integracion_procesadores.md`.

## Arquitectura y análisis

Consulta la documentación técnica en `analisis/`:
- `analisis/README.md` — índice y guías por componente.

## Crear ejecutable (opcional)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name=OCR_Medico huv_ocr_sistema_definitivo.py
```
El ejecutable requiere Tesseract instalado en la máquina destino.

## Solución de problemas

- “Tesseract not found”: Instala Tesseract y configura `config.ini` o PATH.
- “No module named …”: `pip install -r requirements.txt`.
- OCR pobre: aumenta `DPI`, revisa calidad del PDF, considera preprocesar.

## Notas

- Este repositorio contiene regex y mapeos específicos del HUV. Cambios en los formatos de informe requieren actualizar `huv_constants.PATTERNS_HUV`.

