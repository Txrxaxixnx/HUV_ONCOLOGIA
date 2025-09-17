# Analisis: `test_sistema.py`

## Rol
- Conjunto de pruebas smoke para validar dependencias, Tesseract y reglas basicas.

## Cobertura actual
- `test_dependencies()`: verifica importaciones de modulos clave.
- `test_tesseract()`: imprime version de Tesseract via `pytesseract`.
- `test_sample_processing()`: aplica regex simples sobre texto simulado.

## Gap en v2.5
- No valida la base SQLite ni la persistencia de registros.
- No cubre la automatizacion Selenium ni la generacion de graficos.
- No existen fixtures con PDFs reales anonimizados.

## Recomendaciones
- Migrar a `pytest` y agregar fixtures (PDFs sinteticos) para validar `procesador_ihq_biomarcadores`.
- Incluir pruebas que verifiquen inserciones en `database_manager` y calculo de KPIs.
- Simular ejecuciones de Selenium en modo headless (cuando sea viable) para asegurar selectores.
- Incorporar pruebas de regresion para `PATTERNS_HUV` y biomarcadores.

## Mejora a corto plazo
- Agregar test que confirme la existencia de `huv_oncologia.db` y columnas esperadas.
- Reportar versiones de dependencias criticas (CustomTkinter, matplotlib, selenium).
- Incluir bandera para generar logs estructurados que faciliten soporte.