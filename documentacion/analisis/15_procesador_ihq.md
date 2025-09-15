# Análisis: `procesador_ihq.py`

## Rol
- Procesador especializado para informes de Inmunohistoquímica (IHQ) que funciona de forma independiente.
- Extrae texto (vía `ocr_processing.pdf_to_text_enhanced`), aplica patrones específicos IHQ, normaliza datos y exporta Excel con encabezados formateados.

## Patrones y reglas
- `PATTERNS_IHQ`:
  - `descripcion_macroscopica_ihq`: captura bloque entre “Informe de Estudios de Inmunohistoquímica” o “Se recibe orden…” y la sección microscópica.
  - `descripcion_microscopica_ihq`: bloque entre “DESCRIPCIÓN MICROSCÓPICA”/“RESULTADO DE INMUNOHISTOQUÍMICA.” y “DIAGNÓSTICO”.
  - `diagnostico_final_ihq`: bloque de diagnóstico hasta la firma/responsable.
  - `fecha_diagnostico_ihq`: fecha de diagnóstico (alimenta “Fecha ordenamiento”).
  - `responsable_ihq`: nombre sobre el rótulo de responsable (robusto a títulos variables).
- `MALIGNIDAD_KEYWORDS_IHQ`: lista extendida para IHQ.

## Extracción principal
- `extract_ihq_data(text)`:
  - Usa `PATTERNS_HUV` (base) para datos comunes y `PATTERNS_IHQ` para secciones IHQ.
  - Normaliza nombre, identificación, edad y fechas (`convert_date_format`, `calculate_birth_date`).
  - Reglas IHQ:
    - `hospitalizado = NO`, `n_autorizacion = COEX`, `identificador_unico = 0`.
    - Deducción de especialidad mediante `deduce_specialty_ihq(servicio)`.
    - `malignidad` por palabras clave sobre diagnóstico.
    - Órgano: extraído desde macro (por patrón “corresponde a …” o campo “Órgano: …”).
    - `fecha_ordenamiento` desde `fecha_diagnostico_ihq` (con valor por defecto si no se encuentra).
  - Limpieza de OCR en diagnóstico para eliminar artefactos.

## Mapeo a Excel
- `map_to_excel_format(extracted_data) -> list[dict]`:
  - Genera una fila con 55 columnas requeridas por HUV.
  - Completa Sede/Departamento/Municipio/Tarifa/Valor desde `HUV_CONFIG`.
  - Rellena `CUPS` y `Procedimiento` según “INMUNOHISTOQUÍMICA”.
  - Copia macro/micro/diagnóstico a sus columnas correspondientes.
  - Aplica estilo de encabezados vía `openpyxl` al guardar.

## Entrada/Salida
- Entrada: PDF seleccionado mediante diálogo.
- Salida: `Informe_IHQ_<timestamp>.xlsx` en la carpeta del PDF.

## Observaciones
- El valor por defecto de `fecha_ordenamiento` se mantiene para un template específico; puede parametrizarse.
- Recomendada la integración por enrutamiento automático desde `data_extraction.detect_report_type`.
