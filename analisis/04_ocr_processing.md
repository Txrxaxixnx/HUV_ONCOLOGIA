# Análisis: `ocr_processing.py`

## Rol
- Convertir páginas de PDF a imágenes y aplicar OCR optimizado con Tesseract para obtener texto.

## Parámetros clave (desde `config.ini`)
- `OCR_SETTINGS.DPI`: Resolución de render (recomendado 300–400).
- `OCR_SETTINGS.PSM_MODE`: Page Segmentation Mode de Tesseract (por defecto 6: bloque de texto uniforme).
- `OCR_SETTINGS.LANGUAGE`: Idioma del OCR (ej. `spa`).
- `OCR_SETTINGS.OCR_CONFIG`: Parámetros adicionales para Tesseract.
- `PROCESSING.FIRST_PAGE` / `LAST_PAGE`: Rango de páginas a procesar.
- `PROCESSING.MIN_WIDTH`: Reescalado mínimo antes del OCR (mejora legibilidad).

## Función principal
### `pdf_to_text_enhanced(pdf_path: str) -> str`
- Abre el documento con `fitz` (PyMuPDF).
- Por página:
  - Renderiza con `Matrix(DPI/72, DPI/72)` para obtener un pixmap.
  - Convierte a `PIL.Image` (PPM) y a escala de grises (`L`).
  - Reescala si el ancho es menor que `MIN_WIDTH`.
  - Aplica `pytesseract.image_to_string` con `lang` y `config` derivados de INI.
  - Concatena el texto con separadores de página.
- Maneja excepciones agregando contexto del PDF en el mensaje.

## Conexiones
- Lee `config.ini` para ubicar `tesseract` y parámetros OCR.
- Consumido por `ui.HUVOCRSystem._process_files()`.

## Consideraciones
- PDF vectorial con texto real: Podría evaluarse extraer texto directo (PyMuPDF `get_text`) antes de OCR para rendimiento/calidad.
- Calidad OCR depende del render: filtros de binarización/contraste pueden mejorar resultados para scans complejos.
- `LANGUAGE=spa` requiere datos de idioma instalados (e.g., `spa.traineddata`).

## Mejoras sugeridas
- Detección heurística de “texto embebido” para saltar OCR si no hace falta.
- Preprocesamiento adicional opcional (umbralización, despeckle, desenfoque suave para contraste).
- Métricas por página (tiempo/longitud texto) para diagnóstico de calidad.

