# Analisis: `ocr_processing.py`

## Rol
- Convertir paginas de PDF a texto usando estrategia hibrida: primero se intenta texto nativo de PyMuPDF y se recurre a Tesseract cuando es necesario.

## Parametros clave (`config.ini`)
- `OCR_SETTINGS.DPI`: resolucion de render (300-400 recomendado).
- `OCR_SETTINGS.PSM_MODE`: modo de segmentacion de pagina predeterminado.
- `OCR_SETTINGS.LANGUAGE`: idiomas para Tesseract (por defecto `spa`).
- `OCR_SETTINGS.OCR_CONFIG`: banderas adicionales para Tesseract (sin `--psm` duplicados).
- `PROCESSING.FIRST_PAGE` / `LAST_PAGE`: rango de paginas a procesar.
- `PROCESSING.MIN_WIDTH`: ancho minimo; las imagenes se escalan si son menores.

## Funcion principal
### `pdf_to_text_enhanced(pdf_path: str) -> str`
1. Abre el documento con `fitz`.
2. Calcula el rango de paginas usando FIRST_PAGE/LAST_PAGE.
3. Intenta `page.get_text('text')`; si detecta tokens IHQ o suficiencia de texto, usa la salida nativa.
4. Si no, renderiza la pagina con el DPI configurado, convierte a escala de grises y escala segun `MIN_WIDTH`.
5. Ejecuta Tesseract variando PSM (valor configurado, 6 y 4) hasta obtener texto util.
6. `_post_ocr_cleanup` normaliza patrones clave (IHQ######, N. peticion, espacios multiples).
7. Concatena el texto con separadores `--- PAGINA X ---` y devuelve el resultado.

## Conexiones
- Consumido por `procesador_ihq_biomarcadores` y por los procesadores legacy cuando se ejecutan de forma independiente.
- Lee `config.ini` para localizar Tesseract segun sistema operativo.

## Consideraciones
- El fallback de PSM cubre layouts frecuentes; nuevos templates pueden requerir valores adicionales.
- `_post_ocr_cleanup` es critico para segmentar informes multiples en un mismo PDF.
- El modulo no exporta texto crudo; se puede agregar una bandera para debug.

## Mejoras sugeridas
- Detectar automaticamente PDF vectorial para omitir OCR y mejorar rendimiento.
- Exponer tiempo de procesamiento por pagina como metrica de diagnostico.
- Permitir configuracion de idiomas alternos (ej. spa+eng) desde `config.ini`.
