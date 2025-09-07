# Analisis: `data_extraction.py`

## Rol
- Logica de extraccion y normalizacion de datos del texto OCR, especifica para los informes del HUV, y el mapeo a filas de Excel.

## Dependencias
- `huv_constants.py`: `HUV_CONFIG`, `CUPS_CODES`, `PROCEDIMIENTOS`, `ESPECIALIDADES_SERVICIOS`, `PATTERNS_HUV`, `MALIGNIDAD_KEYWORDS`.
- `python-dateutil` (relativedelta), `datetime`, `re`, `unicodedata`.

## Funciones clave
- `detect_report_type(text)`: Determina tipo de informe (AUTOPSIA, IHQ, BIOPSIA, REVISION) por numero de peticion/palabras clave.
- `split_full_name(full_name)`: Divide nombre completo en 4 componentes.
- `calculate_birth_date(edad_str, fecha_ref)`: Calcula fecha de nacimiento restando la edad (anos, meses, dias) a una fecha de referencia.
- `convert_date_format(date_str)`: Normaliza fechas a `DD/MM/YYYY`.
- `_normalize_text(u)`: Quita tildes y pasa a mayusculas para busquedas robustas.
- `detect_malignancy(*texts)`: Marca 'PRESENTE' si alguna palabra clave de malignidad aparece en diagnostico/micro/comentarios.
- `deduce_specialty(servicio, tipo_informe)`: Heuristicas para asignar especialidad a partir de servicio.
- `determine_hospitalization(servicio, tipo_informe)`: Decide si el paciente esta hospitalizado.
- `extract_specimens(organo_text, numero_peticion)`: Soporta multiples especimenes (A., B., ...) o unico.
- `extract_huv_data(text)`: Orquesta la extraccion usando `PATTERNS_HUV` y las utilidades, y arma un dict normalizado.
- `map_to_excel_format(extracted_data, filename)`: Construye filas con el orden y nombres exigidos por HUV para exportar a Excel.

## Relación con `processors/` (prototipos)
- Actualmente, `extract_huv_data` concentra la extracción estable usando `PATTERNS_HUV`.
- Los prototipos en `processors/` muestran cómo separar reglas por tipo (Autopsia, IHQ). A futuro, `extract_huv_data` podrá enrutar al procesador específico tras `detect_report_type`, manteniendo este módulo como orquestador y mapeador a Excel.

## `PATTERNS_HUV` (desde `huv_constants.py`)
- Conjunto de regex adaptadas al layout de los informes (encabezados como Nombre, N. peticion, N.Identificacion, Servicio, etc.).
- Puntos criticos:
  - `descripcion_macroscopica`, `descripcion_microscopica`, `diagnostico`, `comentarios` usan regex multi-linea con limites por secciones vecinas para evitar "over-capture".
  - `diagnostico`: version robusta que ignora encabezados y corta en "COMENTARIOS/Responsable.../TCPDF".

## Decisiones de normalizacion
- Identificacion: elimina separadores no numericos.
- Edad: conserva solo anos para la columna 'Edad', y usa el texto completo para derivar 'Fecha de nacimiento'.
- Fechas: para ordenamiento, usa `fecha_autopsia` si aplica; de lo contrario `fecha_ingreso`.
- CUPS y procedimiento: segun `tipo_informe` -> `CUPS_CODES` -> `PROCEDIMIENTOS`.
- Especimenes: para IHQ se fuerza `hospitalizado=NO`, `n_autorizacion=COEX`, `identificador_unico=0` y se expanden muestras.

## Mapeo a Excel
- Columnas definidas explicitamente en `EXCEL_COLUMNS` (orden fijo requerido por formatos del HUV).
- Genera una fila por especimen detectado.
- Aplica valores por defecto de `HUV_CONFIG` cuando corresponde.

## Riesgos y recomendaciones
- Los patrones regex dependen del formato del PDF; cambios de plantilla requieren actualizar `PATTERNS_HUV`.
- Unificar codificacion UTF-8 en repo para evitar mojibake.
- Anadir pruebas unitarias de extraccion con textos de ejemplo (fixtures) para cada tipo de informe.
- Considerar un parser por secciones (state machine) si crece la complejidad.
