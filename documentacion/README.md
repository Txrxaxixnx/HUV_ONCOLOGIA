EVARISIS Gestor H.U.V: Gestion e Investigacion Hospitalaria

Version actual del software: v2.5 (15/09/2025). Este repositorio contiene la aplicacion de escritorio del ecosistema EVARISIS Gestor H.U.V que transforma informes PDF de patologia en datos estructurados persistidos para analitica clinica y gestion institucional.

Vision estrategica
- Mision: convertir los informes de patologia del HUV en una base confiable para decisiones clinicas, investigacion y planeacion de recursos.
- Objetivos:
  - Inteligencia de negocio: tablero interactivo y sincronia futura con Power BI.
  - Investigacion clinica/epidemiologica: trazabilidad completa de biomarcadores IHQ.
  - Optimizacion de recursos: tiempos de proceso y productividad por servicio o responsable.
  - Automatizacion institucional: pipeline sin hojas de calculo intermedias y conectores con portales HUV.
  - Soporte clinico: cimentar los datasets que habilitaran modelos predictivos en fases siguientes.

Que hace hoy (v2.5)
- Procesamiento masivo de PDFs IHQ con OCR hibrido (texto nativo + Tesseract) y limpieza referencial.
- Extraccion especializada de biomarcadores y metadatos clinicos mediante `procesador_ihq_biomarcadores`.
- Persistencia automatica en la base SQLite `huv_oncologia.db` con control de duplicados (`database_manager`).
- Interfaz moderna con CustomTkinter: vistas para Procesar PDFs, Visualizar datos y Dashboard analitico.
- Tablero integrado (Matplotlib/Seaborn) con filtros dinamicos, comparador parametrico, modo pantalla completa y KPIs.
- Consulta guiada al portal `huvpatologia.qhorte.com` via Selenium (`huv_web_automation.py`) desde la opcion Automatizar BD Web.
- Seleccion asistida de fechas usando `CalendarioInteligente` con soporte de festivos (Babel + holidays).

Novedades clave v2.5
- Redisenho de la UI: barra lateral, tarjetas KPI, tabla maestro con detalle y tema claro/oscuro.
- Pipeline persistente: cada lote genera filas normalizadas disponibles para analitica inmediata sin pasos manuales.
- Segmentacion multi informe por PDF IHQ (maneja codigos IHQ###### repetidos y errores de OCR).
- Tablero comparativo de biomarcadores (HER2, Ki-67, RE/RP, PD-L1) y tiempos de atencion.
- Automatizacion operacional del portal institucional para reducir trabajo manual de descarga.

Ejecucion
```bash
python huv_ocr_sistema_definitivo.py
```
El primer arranque instala automaticamente el ChromeDriver via `webdriver-manager`. Mantenga Google Chrome actualizado para evitar incompatibilidades.

Flujo dentro de la aplicacion
1. Procesar PDFs: seleccione archivos, revise el log en vivo y espere la confirmacion de registros guardados.
2. Visualizar datos: cargue o actualice la tabla maestra desde la base SQLite, busque por peticion o apellido y consulte el panel de detalles.
3. Dashboard Analitico: aplique filtros (fecha, servicio, malignidad, responsable) y explore graficos; haga doble clic para pantalla completa.
4. Automatizar BD Web: defina credenciales y rango de fechas; el sistema ejecuta Selenium y deja la consulta lista en el navegador.

Persistencia y datos
- Archivo de base: `huv_oncologia.db` (tabla `informes_ihq`).
- Identificador de control: N. peticion (0. Numero de biopsia).
- Los Excel extendidos pueden generarse manualmente exportando desde la vista Visualizar (copiar/pegar o `df.to_excel` desde consola si se requiere).

Dashboard y analitica
- Overview: volumen mensual, distribucion de malignidad, top servicios y top organos.
- Biomarcadores: histogramas de Ki-67, barras de HER2, estado RE/RP y PD-L1.
- Tiempos: boxplot tiempo de proceso, throughput semanal, dispersion edad vs Ki-67.
- Calidad: campos faltantes, productividad por responsable, longitud del diagnostico.
- Comparador: agregaciones por dimension seleccionable (conteo o promedio).

Automatizacion del portal
- Utiliza Selenium y ChromeDriver gestionado por `webdriver-manager`.
- Opciones de criterio soportadas: Fecha de Ingreso, Fecha de Finalizacion, Rango de Peticion, Datos del Paciente.
- El log integrado muestra el avance del bot y captura errores.

Gobernanza y autoria
- Lider clinico: Dr. Juan Camilo Bayona (Oncologia).
- Desarrollador principal: Ing. Daniel Restrepo (Area de Innovacion y Desarrollo, GDI).
- Jefe de Gestion de la Informacion: Ing. Diego Pena.
- Entidad ejecutora: Area de Innovacion y Desarrollo del HUV Evaristo Garcia.

Instalacion rapida
```cmd
pip install -r requirements.txt
python huv_ocr_sistema_definitivo.py
```
Para despliegues nuevos en Windows instale Tesseract y verifique que el ejecutable coincida con `config.ini`.

Requisitos
- Python 3.9+ (probado en 3.13).
- Tesseract OCR instalado (con idioma spa).
- Paquetes de `requirements.txt` (incluye customtkinter, matplotlib, selenium, webdriver-manager, Babel, holidays).
- Google Chrome para la automatizacion web.
- Acceso a los PDFs institucionales.

Verificacion rapida
```bash
tesseract --version
python -c 'import pytesseract, fitz, PIL, pandas, customtkinter, selenium'
```

Configuracion relevante (config.ini)
- [PATHS]: rutas especificas de Tesseract por sistema operativo.
- [OCR_SETTINGS]: DPI, PSM y banderas adicionales de Tesseract.
- [PROCESSING]: rango de paginas y ancho minimo para el render.
- [OUTPUT]: parametros historicos para nombres de Excel (opcional si se usa export manual).
- [INTERFACE]: dimensiones y altura del log (heredado del modo clasico).

Hoja de ruta
- Fase 1 – Fundacion (completa, v1.0).
- Fase 2 – Enriquecimiento IHQ (completa, v1.1).
- Fase 3 – Centralizacion y visualizacion (en curso, v2.5 entrega dashboard y SQLite).
- Fase 4 – Integracion SERVINTE (planeada: API o CSV y colas de reenvio).
- Fase 5 – Inteligencia aumentada (planeada: modelos predictivos y asistente).

Arquitectura y analisis
- Ver `documentacion/analisis/README.md` para el indice detallado.
- Modulos destacados: `ui.py`, `procesador_ihq_biomarcadores.py`, `database_manager.py`, `huv_web_automation.py`, `calendario.py`, `ocr_processing.py`, `huv_constants.py`.

Soporte y problemas comunes
- 'Tesseract not found': revise `config.ini` o agregue el ejecutable al PATH.
- Selenium falla al iniciar: confirme la version de Chrome y que la red permita descargar el driver.
- OCR deficiente: incremente DPI, verifique calidad del PDF y revise MIN_WIDTH.
- Datos duplicados: verifique que el PDF no reutilice el mismo numero de peticion; la base ignora duplicados exactos.

Historial
- Cambios: `documentacion/CHANGELOG.md`.
- Bitacora de acercamientos: `documentacion/BITACORA_DE_ACERCAMIENTOS.md`.
