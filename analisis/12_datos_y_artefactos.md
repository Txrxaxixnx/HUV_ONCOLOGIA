# Datos y artefactos del repositorio

## Carpetas y archivos relevantes
- `EXCEL/`: Ejemplos/artefactos de exportaciones previas (Excel) y salidas de depuracion de OCR.
- `pdfs_patologia/`: PDFs de ejemplo/entrada.
- `spa.traineddata`: Datos de idioma espanol para Tesseract (si se distribuye junto al proyecto, documentar ubicacion efectiva de Tesseract).
- `Release-25.07.0-0/poppler-25.07.0/`: Distribucion de Poppler (terceros). No forma parte del codigo del sistema, se considera dependencia binaria.

## Buenas practicas
- No versionar salidas (Excel/PDF procesado) salvo que se necesiten como fixtures de prueba.
- Mantener datos de ejemplo en carpetas dedicadas (`samples/`) con anonimizacion si corresponde.
