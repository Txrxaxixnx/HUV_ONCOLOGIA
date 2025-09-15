Datos y Artefactos del Ecosistema

Activos Clave
- Esquema operativo (55 columnas): formato actual de salida del EVARISIS Gestor H.U.V validado para operación inicial.
- Esquema Maestro H.U.V (167 columnas): referencia exhaustiva institucional que guía el enriquecimiento futuro del esquema operativo.

Fuente Primaria de Informes (PDFs)
- Portal de Patología H.U.V: `https://huvpatologia.qhorte.com/index.php`
  - Nota de acceso: aplicación de red local; solo intranet HUV (similar a SERVINTE). El proyecto cuenta con credenciales institucionales.

Fuentes de Conocimiento Científico (para futura IA)
- CAP: `https://www.cap.org/protocols-and-guidelines/cancer-reporting-tools/cancer-protocol-templates`
- Pathology Outlines: `https://www.pathologyoutlines.com/`
- OMS (Libros Azules): `https://tumourclassification.iarc.who.int/home`

Carpetas y Archivos del Repositorio
- `EXCEL/`: artefactos de exportaciones (Excel) y salidas de depuración del OCR.
- `pdfs_patologia/`: PDFs de ejemplo/entrada.
- `spa.traineddata`: datos de idioma español para Tesseract (si se distribuye con el proyecto, documentar la ruta efectiva del binario Tesseract).
- Dependencias de terceros (ej. Poppler): no forman parte del código del sistema.

Buenas Prácticas
- No versionar salidas (Excel/PDF procesado) salvo como fixtures de prueba.
- Mantener datos de ejemplo en carpetas dedicadas con anonimización cuando aplique.
