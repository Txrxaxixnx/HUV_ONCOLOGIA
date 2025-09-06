# Resumen de Arquitectura del Sistema OCR HUV

Este documento explica, de manera ejecutiva, cómo está organizado el proyecto, cómo fluyen los datos y cómo se conectan los componentes principales. Sirve como mapa mental previo a los análisis por archivo.

## Objetivo del sistema
- Extraer texto de informes PDF de Patología del HUV mediante OCR (Tesseract via `pytesseract`).
- Estructurar la información relevante con expresiones regulares robustas.
- Exportar el resultado a Excel con formato profesional.
- Ofrecer una interfaz de escritorio (Tkinter) para procesamiento por lotes.

## Flujo de datos (alto nivel)
1) Usuario selecciona PDFs y carpeta de salida en la interfaz (`ui.py`).
2) Por cada PDF:
   - Se renderiza cada página con PyMuPDF (`ocr_processing.pdf_to_text_enhanced`).
   - Se aplica OCR con Tesseract para obtener texto.
   - Se analizan patrones específicos del HUV para estructurar datos (`data_extraction.extract_huv_data`).
   - Se mapea a filas de Excel (`data_extraction.map_to_excel_format`).
3) Se genera un `.xlsx` con `pandas` y `openpyxl` y se aplican estilos a encabezados.

## Componentes principales
- `huv_ocr_sistema_definitivo.py`: Punto de entrada. Carga configuración y levanta la UI.
- `ui.py`: Interfaz Tkinter. Orquesta el flujo, progreso y logs. Gestiona la salida Excel.
- `ocr_processing.py`: Capa de OCR. Render PDF -> Imagen -> OCR (Tesseract). Parámetros vía `config.ini`.
- `data_extraction.py`: Reglas de extracción. Usa regex y heurísticas del HUV. Mapea a filas Excel.
- `huv_constants.py`: Constantes compartidas: configuración hospitalaria, códigos CUPS, patrones regex.
- `config.ini`: Parámetros de rutas (Tesseract), OCR, procesamiento y UI.
- `requirements.txt`: Dependencias Python.
- Utilidades y soporte: `instalar_dependencias.py`, `crear_ejecutable.py`, `test_sistema.py`.

## Conexiones entre módulos
- `huv_ocr_sistema_definitivo.py` importa `HUVOCRSystem` de `ui.py`.
- `ui.py` depende de:
  - `ocr_processing.pdf_to_text_enhanced` para el OCR.
  - `data_extraction.extract_huv_data` para estructurar.
  - `data_extraction.map_to_excel_format` para construir filas Excel.
- `ocr_processing.py` y `huv_ocr_sistema_definitivo.py` leen `config.ini` para localizar Tesseract y parámetros OCR.
- `data_extraction.py` usa constantes de `huv_constants.py`.

## Entradas/Salidas
- Entradas: PDFs (carpeta o selección individual). Opcionalmente rutas de Tesseract en `config.ini`.
- Salidas: Archivo Excel con nombre `OUTPUT_FILENAME_YYYYMMDD_hhmmss.xlsx` en carpeta elegida. Archivos de depuración de OCR por PDF.

## Consideraciones de calidad
- OCR: Calidad depende de DPI, idioma, limpieza y contraste; parametrizable en `config.ini`.
- Patrones: Las regex están personalizadas para la maquetación habitual de informes del HUV.
- Rendimiento: Procesamiento por lotes con hilo en background; UI permanece responsiva.

## Próximos pasos sugeridos
- Unificar codificación UTF-8 en archivos de texto para evitar mojibake (caracteres raros de acentos).
- Añadir pruebas unitarias a utilidades de extracción (regex y normalización).
- Opcional: soporte CLI sin interfaz para automatizaciones.

