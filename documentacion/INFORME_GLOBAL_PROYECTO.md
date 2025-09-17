EVARISIS Gestor H.U.V: Informe Global del Proyecto

Version del software: v2.5 (15/09/2025)
Fecha de esta actualizacion documental: 15/09/2025

Resumen ejecutivo
- EVARISIS Gestor H.U.V consolida un pipeline de captura, analisis y persistencia de informes de patologia para oncologia HUV.
- La version 2.5 incorpora una interfaz moderna, pipeline persistente en SQLite y un dashboard analitico integrado para decision clinica e investigacion.
- La automatizacion del portal institucional reduce tareas manuales de descarga y garantiza alimentacion oportuna de la base de datos.

Vision estrategica
- Mision: transformar informes de patologia en informacion estructurada confiable para la gestion clinica, investigacion y planeacion hospitalaria.
- Objetivos estrategicos:
  - Analitica institucional: tableros operativos con posibilidad de integracion a Power BI.
  - Investigacion clinica: seguimiento de biomarcadores y cohortes longitudinales.
  - Optimizacion de recursos: monitoreo de volumen, tiempos y responsables.
  - Automatizacion de procesos: eliminacion de transcripcion manual y conectores con sistemas HUV.
  - Fundacion para IA: dataset curado para futuros modelos predictivos y asistentes clinicos.

Gobernanza y roles
- Lider medico e investigador principal: Dr. Juan Camilo Bayona (Oncologia).
- Desarrollador principal: Ing. Daniel Restrepo (Area de Innovacion y Desarrollo, GDI).
- Jefe de Gestion de la Informacion: Ing. Diego Pena.
- Entidad ejecutora: Area de Innovacion y Desarrollo del HUV Evaristo Garcia.

Alcance actual (v2.5)
- OCR hibrido (texto nativo + Tesseract) con configuracion via `config.ini`.
- Extraccion especializada IHQ (`procesador_ihq_biomarcadores`) con segmentacion multi informe y normalizacion de biomarcadores.
- Persistencia en SQLite (`huv_oncologia.db`) gestionada por `database_manager`, evitando duplicados.
- Interfaz CustomTkinter con vistas de Procesamiento, Visualizacion y Dashboard, mas modo claro/oscuro.
- Dashboard Matplotlib/Seaborn con filtros dinamicos, comparador parametrico y exportacion visual.
- Automatizacion Selenium (`huv_web_automation.py`) para consultas en `huvpatologia.qhorte.com`.
- Widget `CalendarioInteligente` para seleccion contextual de fechas y festivos.

Hoja de ruta (roadmap)
- Fase 1 – Fundacion y validacion (completa, v1.0).
- Fase 2 – Enriquecimiento de datos IHQ (completa, v1.1).
- Fase 3 – Centralizacion y visualizacion (en curso, v2.5 entrega base persistente y dashboard integrado; pendiente integrar otras plantillas).
- Fase 4 – Integracion SERVINTE (planeada: API/CSV, colas locales, modo dry-run).
- Fase 5 – Inteligencia aumentada (planeada: modelos predictivos, asistente clinico).

Metodologia y gestion del proyecto
- Versionamiento semantico; 2.5 representa la primera entrega con persistencia integrada.
- `CHANGELOG.md` y `BITACORA_DE_ACERCAMIENTOS.md` como fuentes de verdad para cambios y compromisos.
- Enfoque incremental: primeras fases cerradas, nuevas fases iterativas sobre la base SQLite.

Activos y fuentes de datos
- Base operativa: `huv_oncologia.db` (tabla `informes_ihq`).
- Esquema maestro HUV (167 campos) como norte para futuras ampliaciones (autopsia, biopsia, revision).
- Portal de patologia HUV `https://huvpatologia.qhorte.com/index.php` como fuente primaria de PDFs.
- Repositorio de conocimiento: CAP, Pathology Outlines, OMS (para enriquecimiento futuro).

Arquitectura (resumen)
- `huv_ocr_sistema_definitivo.py`: punto de entrada, configura Tesseract y lanza la UI.
- `ui.py`: interfaz CustomTkinter, orquestacion del pipeline y dashboard.
- `ocr_processing.py`: render OCR con estrategia hibrida y limpieza post OCR.
- `procesador_ihq_biomarcadores.py`: extraccion especializada y persistencia.
- `database_manager.py`: inicializacion de SQLite, guardado y lectura.
- `huv_web_automation.py`: automatizacion del portal con Selenium.
- `calendario.py`: calendario inteligente con festivos.

Ejecucion y despliegue
- App principal: `python huv_ocr_sistema_definitivo.py`.
- Dependencias: Tesseract instalado, Python 3.9+, paquetes de `requirements.txt`, Google Chrome.
- Primer arranque descarga ChromeDriver automaticamente (requiere internet).

Notas finales
- La version 2.5 estabiliza el pipeline IHQ, entrega visualizaciones inmediatas y sienta las bases para integrar otras plantillas y sistemas core (SERVINTE, Power BI).
- Proximos pasos: extender persistencia a Biopsia/Autopsia, habilitar sincronizacion incremental con el data warehouse y reforzar pruebas automatizadas de extraccion.
