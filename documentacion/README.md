EVARISIS Gestor H.U.V: Gestión e Investigación Hospitalaria

Versión actual del software: v1.1 (10/09/2025). Este repositorio contiene la aplicación de escritorio base del ecosistema EVARISIS Gestor H.U.V, que transforma informes PDF de patología en datos estructurados listos para análisis y toma de decisiones.

Visión Estratégica
- Misión: Estructurar y analizar datos clínicos verídicos provenientes de informes de patología para transformar la toma de decisiones, la investigación y la gestión de recursos del HUV.
- Objetivos:
  - Inteligencia de negocio: centralizar datos y habilitar dashboards en Power BI.
  - Investigación clínica/epidemiológica: priorizar IHQ y estudios moleculares.
  - Optimización de recursos: análisis predictivo para convenios y compras por volumen.
  - Automatización: reducir errores y tiempos; futura integración con SERVINTE.
  - Soporte clínico: sentar bases de futuras herramientas de IA.

¿Qué hace hoy (v1.1)?
- GUI en Python (Tkinter) para procesamiento por lotes de PDFs.
- OCR robusto (Tesseract + PyMuPDF) y extracción por expresiones regulares.
- Mapeo a un esquema operativo validado (55 columnas) y exportación a Excel.
- Procesadores especializados activos: Autopsia, IHQ, Biopsia y Revisión.

Ejecución
- App principal: `python huv_ocr_sistema_definitivo.py`
- Procesadores (opcionales):
  - `python procesador_autopsia.py`
  - `python procesador_ihq.py`
  - `python procesador_biopsia.py`
  - `python procesador_revision.py`

Análisis Avanzado IHQ (v1.1)
- En la aplicación, usa el botón `Analizar Biomarcadores IHQ (v1.1)` para seleccionar uno o varios PDFs de IHQ y una carpeta de salida.
- Genera un Excel separado con biomarcadores: HER2, Ki‑67, RE/ER, RP/PR, PD‑L1, P16 (estado/porcentaje) y "Estudios Solicitados".
- No modifica el esquema operativo estándar de 55 columnas del flujo principal.

Gobernanza y Autoría
- Líder de Proyecto e Investigador Principal: Dr. Juan Camilo Bayona (Jefe Médico de Oncología).
- Desarrollador Principal: Ing. Daniel Restrepo (Área de Innovación y Desarrollo, GDI).
- Entidad Ejecutora: Área de Innovación y Desarrollo del HUV Evaristo García.
- Jefe de Gestión de la Información (GDI): Ing. Diego Peña.

Instalación Rápida
- Opción A – Automática: `python instalar_dependencias.py`
- Opción B – Manual:
  - `pip install -r requirements.txt`
  - Instala Tesseract según tu SO (ver `INICIO_RAPIDO.md`)

Requisitos
- Python 3.7+ (recomendado 3.9+)
- Windows 10+/Ubuntu 18+/macOS 10.14+
- Tesseract OCR instalado y accesible

Verificación
```bash
tesseract --version
python -c "import pytesseract, fitz, PIL, pandas, openpyxl, dateutil; print('OK')"
```

Configuración
- Edita `config.ini`:
  - `[PATHS]`: rutas a `tesseract` por sistema.
  - `[OCR_SETTINGS]`: `DPI`, `PSM_MODE`, `LANGUAGE`, `OCR_CONFIG`.
  - `[PROCESSING]`: rango de páginas y tamaño mínimo.
  - `[OUTPUT]`: nombre del Excel resultante.
  - `[INTERFACE]`: dimensiones de ventana y altura del log.

Hoja de Ruta
- Fase 1 – Fundación y Validación (Completada – v1.0, 05/09/2025)
- Fase 2 – Enriquecimiento de Datos (En proceso): priorizar IHQ, agregar biomarcadores (HER2, KI67, RE Estrogeno, RP Progesterona, PDL-1, Estudios Solicitados, P16[Estado, Porcentaje]).
- Fase 3 – Centralización y Visualización: migrar a base de datos + dashboards Power BI.
- Fase 4 – Integración y Automatización: integración con SERVINTE.
- Fase 5 – Inteligencia Aumentada: modelos predictivos y asistente IA.

Arquitectura y Análisis
- Documentación técnica: `analisis/` (índice en `analisis/README.md`).
- Plan SERVINTE: `SERVINTE_PLAN.md`.

Crear ejecutable (opcional)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name=EVARISIS_Gestor huv_ocr_sistema_definitivo.py
```
El ejecutable requiere Tesseract instalado en la máquina destino.

Soporte y Problemas Comunes
- “Tesseract not found”: instala Tesseract y configura `config.ini` o PATH.
- “No module named …”: `pip install -r requirements.txt`.
- OCR pobre: aumenta `DPI` y revisa calidad del PDF.

Historial
- Cambios: `CHANGELOG.md`
- Seguimiento estratégico: `BITACORA_DE_ACERCAMIENTOS.md`
