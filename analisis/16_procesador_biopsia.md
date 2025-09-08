# Análisis: `procesador_biopsia.py`

## Rol
- Procesador especializado para informes de Biopsia con múltiples especímenes (A., B., C.).
- Extrae datos comunes, identifica y divide bloques por espécimen, y genera una fila por cada uno.

## Patrones y reglas
- `PATTERNS_BIOPSIA`:
  - `descripcion_macroscopica_full`: bloque entre “DESCRIPCIÓN MACROSCÓPICA” y sección microscópica.
  - `descripcion_microscopica_full`: bloque entre sección microscópica y “DIAGNÓSTICO”.
  - `diagnostico_full`: diagnóstico hasta firma/responsable.
  - `responsable_analisis`: nombre sobre el rótulo “Responsable del análisis”.
- `MALIGNIDAD_KEYWORDS_BIOPSIA`: lista extendida para identificar malignidad.

## Lógica de especímenes
- `extract_specimens_data(text, numero_peticion) -> list`:
  - Detecta letras de especímenes en el bloque macroscópico.
  - Divide diagnóstico y microscópico por letra usando anclajes “^A.”, “^B.”, etc. (modo multilinea).
  - Construye para cada espécimen: `numero_muestra` (p.ej., M1234567-A), órgano, diagnóstico/micro específicos.

## Extracción principal
- `extract_biopsy_data(text)`:
  - Aplica `BASE_PATTERNS` (= `PATTERNS_HUV`) para campos comunes.
  - Usa `PATTERNS_BIOPSIA` para macro/micro/diagnóstico y responsable.
  - Normaliza nombre, identificación, edad y fechas.
  - Reglas:
    - `hospitalizado = SI`.
    - `especialidad_deducida` por servicio (`deduce_specialty_biopsia`).
    - `malignidad` desde `diagnostico_full`.
    - `identificador_unico_final` desde “Seguimos Haciendo Historia <número>”.

## Mapeo a Excel
- `map_to_excel_format(common_data, specimens_data) -> list[dict]`:
  - Carga datos comunes y luego sobreescribe campos por espécimen.
  - Rellena `CUPS` y `Procedimiento` para “BIOPSIA”.
  - Genera tantas filas como especímenes detectados (55 columnas cada una).

## Entrada/Salida
- Entrada: PDF seleccionado mediante diálogo.
- Salida: `Informe_Biopsia_<timestamp>.xlsx` en la carpeta del PDF.

## Observaciones
- El campo “Fecha ordenamiento” está fijo en el ejemplo; se sugiere calcularlo desde `fecha_ingreso` o extraerlo de encabezado.
- Recomendado fortalecer el patrón de división de especímenes para comillas/tipografías variables.
