# Analisis: `huv_constants.py`

## Rol
- Provee constantes y tablas de referencia compartidas para todo el sistema.

## Contenido
- `HUV_CONFIG`: Valores por defecto (sede, municipio, tipo documento, tarifas).
- `CUPS_CODES`: Mapeo tipo de informe -> codigo CUPS.
- `PROCEDIMIENTOS`: Descripcion extendida por codigo CUPS.
- `ESPECIALIDADES_SERVICIOS`: Heuristicas para deducir especialidad a partir de palabras clave de servicio.
- `PATTERNS_HUV`: Regex oficiales/robustas para capturar campos desde el texto de los informes.
- `MALIGNIDAD_KEYWORDS`: Palabras clave para clasificar malignidad.

## Interaccion
- Importado por `data_extraction.py` para toda la logica de extraccion.
- En los prototipos de `processors/` se hace referencia a una futura `PATTERNS_BASE` (base común). Por ahora, esa base práctica es `PATTERNS_HUV` y la migración se realizará cuando la modularización esté consolidada.

## Sugerencias
- Consolidar pruebas de regresion cuando se modifique `PATTERNS_HUV`.
- Centralizar normalizaciones de mayusculas/acento si se anaden mas tablas.
- Planificar refactor hacia `PATTERNS_BASE` para compartir lo común entre tipos de informe y permitir sobreescrituras por procesador.
