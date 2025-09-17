Datos y Artefactos del Ecosistema (v2.5)

Activos clave
- Base operativa SQLite: `huv_oncologia.db` (tabla `informes_ihq`).
- Esquema maestro HUV (167 campos) como referencia para futuras ampliaciones.
- Plantillas legacy (Excel 55 columnas) disponibles solo para comparacion en `LEGACY/`.

Fuentes primarias
- Portal de Patologia H.U.V: `https://huvpatologia.qhorte.com/index.php` (intranet).
- Descargas automatizadas via `huv_web_automation.py` (Selenium).

Fuentes de conocimiento
- CAP, Pathology Outlines, OMS (Libros Azules) para estandarizar nomenclaturas.

Carpetas y archivos relevantes
- `documentacion/`: guias, informes y comunicados.
- `LEGACY/`: version 1.x del pipeline (Excel).
- `pdfs_patologia/`: ejemplos de entrada (asegurar anonimizacion).
- `EXCEL/`: artefactos de exportaciones historicas (mantener solo como fixtures).
- `spa.traineddata`: datos de idioma para Tesseract (verificar ruta real instalada).

Buenas practicas
- Evitar versionar nuevos excels generados; usar exportaciones bajo demanda o adjuntar como evidencia en carpetas temporales.
- Realizar respaldos periodicos de `huv_oncologia.db` antes de pruebas masivas.
- Documentar origen y fecha de los PDFs utilizados para entrenamiento o validacion.
