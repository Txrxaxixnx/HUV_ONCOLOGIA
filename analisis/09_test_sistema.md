# Análisis: `test_sistema.py`

## Rol
- Pruebas manuales/smoke para validar entorno: módulos Python instalados, Tesseract accesible y extracción regex básica.

## Pruebas
- `test_dependencies()`: Importa módulos clave y reporta faltantes.
- `test_tesseract()`: Muestra versión de Tesseract vía `pytesseract`.
- `test_sample_processing()`: Ejecuta regex simples sobre un texto simulado.

## Sugerencias
- Migrar a `pytest` con casos de prueba de texto real y fixtures.
- Añadir pruebas de regresión sobre `PATTERNS_HUV`.

