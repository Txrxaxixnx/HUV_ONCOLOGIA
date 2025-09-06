# Análisis: `huv_constants.py`

## Rol
- Provee constantes y tablas de referencia compartidas para todo el sistema.

## Contenido
- `HUV_CONFIG`: Valores por defecto (sede, municipio, tipo documento, tarifas).
- `CUPS_CODES`: Mapeo tipo de informe → código CUPS.
- `PROCEDIMIENTOS`: Descripción extendida por código CUPS.
- `ESPECIALIDADES_SERVICIOS`: Heurísticas para deducir especialidad a partir de palabras clave de servicio.
- `PATTERNS_HUV`: Regex oficiales/robustas para capturar campos desde el texto de los informes.
- `MALIGNIDAD_KEYWORDS`: Palabras clave para clasificar malignidad.

## Interacción
- Importado por `data_extraction.py` para toda la lógica de extracción.

## Sugerencias
- Consolidar pruebas de regresión cuando se modifique `PATTERNS_HUV`.
- Centralizar normalizaciones de mayúsculas/acento si se añaden más tablas.

