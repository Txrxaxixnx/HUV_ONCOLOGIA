# Sistema de procesadores por plantilla

## Objetivo
- Incorporar nuevas plantillas de informe (variantes del HUV y centros externos) separando reglas y patrones por tipo.

## Estado actual (operativo en modo independiente)
- Procesadores incluidos en la raíz del repositorio:
  - `procesador_ihq.py` — Inmunohistoquímica (IHQ)
  - `procesador_biopsia.py` — Biopsias con múltiples especímenes (A., B., C.)
  - `procesador_revision.py` — Revisión de casos externos (R)
- Cada procesador:
  - Implementa extracción especializada (regex y reglas de negocio propias).
  - Normaliza campos y mapea a las 55 columnas requeridas por el HUV.
  - Genera Excel con encabezados formateados (openpyxl).

## Integración con el flujo principal
- Ruta estable actual: `data_extraction.extract_huv_data` + `huv_constants.PATTERNS_HUV`.
- Plan: enrutar automáticamente según `detect_report_type(text)` hacia el procesador correspondiente manteniendo compatibilidad con el mapeo a Excel.
- Ver detalles en `analisis/14_integracion_procesadores.md`.

## Interfaz propuesta por procesador
Todo procesador debería exponer, como mínimo, estas funciones:
- `extract_<tipo>_data(text: str) -> dict`: devuelve un diccionario normalizado con claves compatibles con el mapeo a Excel.
- `map_to_excel_format(data: dict) -> list[dict]` o `map_to_excel_format(common_data: dict, specimens: list) -> list[dict]` para tipos con múltiples especímenes.
- Opcional: `detect(text: str) -> bool` si se necesita una detección más precisa que `detect_report_type`.

## Flujo recomendado
1) Detección de tipo: `data_extraction.detect_report_type(text)`.
2) Enrutamiento: llamar al procesador especializado si existe; en caso contrario, usar `extract_huv_data`.
3) Mapeo a Excel: usar el mapeo propio del procesador o `data_extraction.map_to_excel_format` si el diccionario es compatible.

## Cómo añadir una plantilla nueva
- Crear `procesador_<nuevo>.py` con:
  - `PATTERNS_<NUEVO>` basado en lo común de `PATTERNS_HUV` más las particularidades.
  - `extract_<nuevo>_data(text)` y su `map_to_excel_format`.
- Añadir el nuevo tipo a `data_extraction.detect_report_type` si aplica por N. de petición o encabezados.
- Mantener compatibilidad del diccionario con el esquema de 55 columnas.

## Consideraciones y riesgos
- Regex sensibles a encabezados exactos. Usar separadores de secciones (lookahead) y `re.DOTALL`.
- Codificación: homogeneizar UTF-8 para evitar mojibake.
- Pruebas: textos OCR representativos por tipo y pruebas de regresión al actualizar patrones.
- Desempeño: la modularización no cambia el costo OCR; mejora mantenibilidad y extensibilidad.

## Relación con `huv_constants.PATTERNS_HUV`
- `PATTERNS_HUV` es hoy la base funcional probada para informes del HUV.
- Se propone extraer una `PATTERNS_BASE` común y permitir sobreescrituras por tipo en cada procesador.

