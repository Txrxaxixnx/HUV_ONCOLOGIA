# Datos y artefactos del repositorio

## Carpetas y archivos relevantes
- `EXCEL/`: Ejemplos/artefactos de exportaciones previas (Excel) y salidas de depuración de OCR.
- `pdfs_patologia/`: PDFs de ejemplo/entrada.
- `spa.traineddata`: Datos de idioma español para Tesseract (si se distribuye junto al proyecto, documentar ubicación efectiva de Tesseract).
- `Release-25.07.0-0/poppler-25.07.0/`: Distribución de Poppler (terceros). No forma parte del código del sistema, se considera dependencia binaria.

## Buenas prácticas
- No versionar salidas (Excel/PDF procesado) salvo que se necesiten como fixtures de prueba.
- Mantener datos de ejemplo en carpetas dedicadas (`samples/`) con anonimización si corresponde.

