# Analisis: `data_extraction.py` (estado en v2.5)

## Situacion actual
- El modulo `data_extraction.py` permanece en la carpeta `LEGACY/` como referencia de la canalizacion original basada en Excel (v1.x).
- En la version 2.5 la extraccion principal se realiza en `procesador_ihq_biomarcadores.py`, que reusa helpers de `procesador_ihq.py` para mapear campos base.
- Las funciones `extract_huv_data` y `map_to_excel_format` siguen disponibles para compatibilidad, pero no se invocan desde la UI moderna.

## Pipeline vigente
1. `ocr_processing.pdf_to_text_enhanced` produce el texto normalizado.
2. `procesador_ihq_biomarcadores` delega a `procesador_ihq` para obtener los 55 campos historicos y luego agrega biomarcadores/estudios solicitados.
3. Las filas resultantes se persisten en SQLite mediante `database_manager.save_records`.
4. La UI consume la base de datos sin generar Excel por defecto.

## Uso recomendado de `data_extraction`
- Limitar su uso a scripts de compatibilidad o migraciones legacy.
- En caso de necesitar exportaciones tradicionales, se puede ejecutar `LEGACY/data_extraction.py` o llamar directamente a `procesador_ihq.map_to_excel_format`.

## Plan de convergencia
- Reimplementar la logica generica de `data_extraction` como servicios reutilizables que alimenten SQLite (Biopsia, Autopsia, Revision).
- Documentar pruebas unitarias que cubran patrones clave antes de migrar los procesadores restantes.
- Depurar el esquema maestro para identificar columnas obligatorias cuando se integren nuevas plantillas.

## Riesgos
- Mantener dos rutas paralelas (legacy vs v2.5) puede generar divergencias si se actualiza un patron en un solo lugar.
- Algunos scripts externos podrian depender de `data_extraction.map_to_excel_format`; se recomienda encapsular nuevas salidas detras de funciones compatibles.

## Acciones sugeridas
- Extraer helpers compartidos (normalizacion de fechas, nombres, etc.) a un modulo comun reutilizable.
- Migrar gradualmente los procesadores legacy a la base SQLite para evitar regresiones.
- Incorporar pruebas de regresion que comparen salidas legacy vs v2.5 para los mismos PDFs.