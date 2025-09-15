# Analisis: `test_sistema.py`

## Rol
- Pruebas manuales/smoke para validar entorno: modulos Python instalados, Tesseract accesible y extraccion regex basica.

## Pruebas
- `test_dependencies()`: Importa modulos clave y reporta faltantes.
- `test_tesseract()`: Muestra version de Tesseract via `pytesseract`.
- `test_sample_processing()`: Ejecuta regex simples sobre un texto simulado.

## Sugerencias
- Migrar a `pytest` con casos de prueba de texto real y fixtures.
- Anadir pruebas de regresion sobre `PATTERNS_HUV`.
