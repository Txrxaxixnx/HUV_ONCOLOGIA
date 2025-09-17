# Analisis: `huv_constants.py`

## Rol
- Provee constantes y patrones compartidos para el ecosistema EVARISIS (v2.5).
- Alimenta tanto el pipeline moderno (`procesador_ihq_biomarcadores`) como los procesadores legacy.

## Contenido
- `HUV_CONFIG`: valores por defecto (sede, municipio, tipo documento, tarifas).
- `CUPS_CODES` y `PROCEDIMIENTOS`: mapeo de tipo de estudio a codigos CUPS y descripciones.
- `ESPECIALIDADES_SERVICIOS`: heuristicas para deducir especialidad desde el servicio reportado.
- `PATTERNS_HUV`: regex robustas para extraer datos comunales (identificacion, fechas, descripciones).
- `MALIGNIDAD_KEYWORDS`: lista de terminos para detectar malignidad en diagnosticos.

## Interaccion
- `procesador_ihq.py` y `procesador_ihq_biomarcadores.py` reutilizan `PATTERNS_HUV` como base antes de aplicar reglas especificas.
- Procesadores legacy (Biopsia, Autopsia, Revision) dependen de estas constantes; al migrarlos a SQLite se planea reusar el mismo modulo.
- Modulos auxiliares (instalacion, tests) pueden consultar `HUV_CONFIG` para valores por defecto.

## Consideraciones
- Cualquier cambio en `PATTERNS_HUV` debe probarse contra PDFs representativos (IHQ minimo).
- Agregar comentarios breves en el codigo cuando se introduzca un nuevo patron para facilitar auditoria clinica.
- Mantener sincronizada la lista de CUPS/procedimientos con la direccion de patologia.

## Acciones futuras
- Extraer subconjuntos de patrones comunes para facilitar migracion de Biopsia/Autopsia/Revision.
- Evaluar cargar constantes desde archivos YAML/JSON si la cantidad de mapeos crece.
- Crear pruebas unitarias que verifiquen coincidencias clave (identificador, fechas, organos) frente a textos de ejemplo.