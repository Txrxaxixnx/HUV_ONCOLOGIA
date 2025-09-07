# Sistema de procesadores por plantilla (`processors/`)

## Objetivo
- Facilitar la incorporación de nuevas plantillas de informe (p.ej. distintas variantes de HUV, centros externos, Biopsia, Citología) separando reglas y patrones por tipo de informe.

## Estado actual (prototipos)
- `processors/autopsy_processor.py` y `processors/ihq_processor.py` son prototipos que ilustran cómo aislar:
  - Patrones específicos por tipo (`PATTERNS_AUTOPSY`, `PATTERNS_IHQ`).
  - Reglas de negocio particulares (hospitalización, CUPS, composición de specimens, etc.).
- La ruta estable de extracción sigue siendo `data_extraction.extract_huv_data` + `huv_constants.PATTERNS_HUV`.
- Notar que los prototipos importan `PATTERNS_BASE` como futura base común; hoy, esta base está representada por `PATTERNS_HUV` en `huv_constants.py` y se migrará a `PATTERNS_BASE` cuando la modularización esté completa.

## Diseño propuesto
- `PATTERNS_BASE`: conjunto mínimo de patrones comunes (Nombre, N. petición, Identificación, Servicio, Fechas, secciones macro/micro/diagnóstico/comentarios).
- Un procesador por tipo de informe:
  - Define `PATTERNS_<TIPO>` heredando de `PATTERNS_BASE` y sobreescribiendo lo necesario.
  - Implementa `extract_<tipo>_data(text)` encargándose de:
    - Parsear con regex de su `PATTERNS_<TIPO>`.
    - Normalizar campos (edad, identificación, fechas).
    - Aplicar reglas de negocio específicas (hospitalizado, autorizaciones, CUPS y procedimiento, specimens).
  - Devuelve un diccionario normalizado compatible con `map_to_excel_format`.

## Flujo recomendado
1) Detección de tipo: reutilizar `data_extraction.detect_report_type`.
2) Enrutar a procesador específico: `extract_autopsy_data`, `extract_ihq_data`, etc.
3) Mapear a Excel: `data_extraction.map_to_excel_format` (sin cambios, recibe el diccionario normalizado).

## Cómo añadir una plantilla nueva (guía rápida)
- Crear `processors/<nuevo_tipo>_processor.py` con:
  - `PATTERNS_<NUEVO>` basado en `PATTERNS_HUV` (hasta que exista `PATTERNS_BASE`).
  - `extract_<nuevo>_data(text)` implementando normalizaciones y reglas propias.
- Añadir el nuevo tipo a `data_extraction.detect_report_type` (si aplica por patrón de N. de petición o palabras clave del encabezado).
- Mantener compatibilidad del diccionario resultante con `map_to_excel_format` (campos esperados).

## Consideraciones y riesgos
- Las regex son sensibles a los encabezados exactos. Usar límites entre secciones (lookahead) y `re.DOTALL`.
- Codificación: homogeneizar a UTF-8 para evitar mojibake en caracteres acentuados.
- Pruebas: utilizar textos OCR de ejemplo por tipo y asegurar regresión al modificar patrones.
- Desempeño: la separación por procesadores no cambia el costo OCR; sólo compone reglas por tipo.

## Relación con `huv_constants.PATTERNS_HUV`
- `PATTERNS_HUV` representa hoy la base funcional probada para informes del HUV (incluida Autopsia).
- En el plan de modularización, se extraerá lo común a `PATTERNS_BASE` y cada procesador aportará sus diferencias.
- Mientras tanto, los prototipos sirven como referencia de diseño y para experimentar con variaciones de plantillas.

