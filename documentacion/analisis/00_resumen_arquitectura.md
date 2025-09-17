# Resumen de Arquitectura - EVARISIS Gestor H.U.V (v2.5)

Este documento resume como esta organizado el proyecto, el flujo de datos y la relacion entre componentes en la version 2.5.

## Objetivo del sistema
- Extraer texto de informes PDF de patologia (enfoque IHQ) mediante OCR hibrido.
- Normalizar datos clinicos y biomarcadores usando reglas especificas del HUV.
- Persistir la informacion en una base SQLite unificada y habilitar analitica inmediata.
- Ofrecer una interfaz moderna para procesamiento, exploracion y automatizacion web.

## Flujo de datos (alto nivel)
1) El usuario ingresa a la vista Procesar PDFs en `ui.App`.
2) Por cada PDF seleccionado:
   - `ocr_processing.pdf_to_text_enhanced` intenta extraer texto nativo y aplica OCR con Tesseract (DPI configurable).
   - `procesador_ihq_biomarcadores` limpia el texto, segmenta informes (IHQ######) y obtiene datos base via funciones heredadas de `procesador_ihq`.
   - Se calculan biomarcadores clave (HER2, Ki-67, RE, RP, PD-L1, P16, estudios solicitados) con heuristicas robustas.
   - `database_manager.save_records` inserta filas normalizadas en la tabla `informes_ihq` evitando duplicados por numero de peticion.
3) La vista Visualizar datos lee la base con `database_manager.get_all_records_as_dataframe`, muestra la tabla y detalle contextual.
4) La vista Dashboard aplica filtros (fecha, servicio, malignidad, responsable), genera graficos con Matplotlib/Seaborn y ofrece modo pantalla completa.
5) Opcionalmente, el usuario lanza la automatizacion del portal (`huv_web_automation.automatizar_entrega_resultados`) para preparar nuevas descargas.

## Componentes principales
- `huv_ocr_sistema_definitivo.py`: configura Tesseract y lanza `ui.App`.
- `ui.py`: interfaz CustomTkinter (Procesar PDFs, Visualizar datos, Dashboard, Automatizar BD Web) y coordinacion de hilos.
- `ocr_processing.py`: motor OCR hibrido con limpieza dedicada para tokens IHQ.
- `procesador_ihq_biomarcadores.py`: extraccion especializada, normalizacion y escritura en SQLite.
- `database_manager.py`: inicializa la base y expone operaciones CRUD (init_db, save_records, get_all_records_as_dataframe).
- `huv_web_automation.py`: automatizacion Selenium para el portal institucional.
- `calendario.py`: calendario modal con festivos para seleccionar fechas.
- `huv_constants.py`: constante hospitalarias y patrones compartidos.
- `config.ini`: parametros OCR, rutas y ajustes heredados de UI clasica.

## Conexiones entre modulos
- `huv_ocr_sistema_definitivo` importa `App` y prepara el entorno Tesseract.
- `App` (ui.py) usa `procesador_ihq_biomarcadores` y `database_manager` para el pipeline, `Matplotlib` para graficos y `huv_web_automation` para Selenium.
- `procesador_ihq_biomarcadores` reusa utilidades de `procesador_ihq` (legacy) para campos base y complementa biomarcadores.
- `database_manager` depende de `sqlite3` y se invoca desde `ui` y `procesador_ihq_biomarcadores`.
- `calendario.CalendarioInteligente` se usa en la vista de automatizacion web.

## Entradas y salidas
- Entradas: PDFs IHQ, credenciales del portal (para automatizacion), configuracion Tesseract.
- Salidas: registros en `huv_oncologia.db`, logs de procesamiento, visualizaciones en dashboard y (opcional) consultas abiertas en el portal web.

## Consideraciones de calidad
- OCR: calidad depende de DPI y nitidez; el motor escala imagenes segun `MIN_WIDTH`.
- Biomarcadores: heuristicas toleran errores comunes de OCR, pero requieren revision ante nuevos formatos.
- Base de datos: los duplicados se bloquean por numero de peticion; conviene monitorear colisiones legitimas.
- UI: el procesamiento se ejecuta en hilos para no bloquear la interfaz; logs reflejan el avance.

## Proximos pasos sugeridos
- Incorporar plantillas de Biopsia/Autopsia al pipeline persistente.
- Habilitar exportacion incremental hacia Power BI y data warehouse.
- Fortalecer pruebas automatizadas (unitarias para regex y integracion para dashboards).
