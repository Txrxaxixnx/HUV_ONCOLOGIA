# Análisis: `procesador_revision.py`

## Rol
- Procesador especializado para informes de Revisión de Casos Externos (R). Funciona de forma independiente.

## Patrones y reglas
- `PATTERNS_REVISION` (versión corregida):
  - `descripcion_macroscopica_rev`: bloque desde “Se recibe orden para revisión…” hasta la sección microscópica.
  - `descripcion_microscopica_rev`: bloque microscópico hasta “DIAGNÓSTICO”.
  - `diagnostico_rev`: bloque diagnóstico hasta “COMENTARIOS”.
  - `comentarios_rev`: comentarios hasta firma/aval.
  - `organo_rev`: bloque “Bloques y láminas …” hasta el encabezado siguiente (se limpia “material de rutina”).
  - `responsable_final`: captura explícita “NANCY MEJIA VARGAS” (evita IndexError).
  - `medico_tratante_rev`: extrae médico tratante robustamente (con dos puntos/guiones/espacios).

## Extracción principal
- `extract_revision_data(text)`:
  - Usa `BASE_PATTERNS` (= `PATTERNS_HUV`) y luego aplica `PATTERNS_REVISION`.
  - Prioriza `medico_tratante_rev` si está presente.
  - Normaliza nombre, identificación, edad y fechas.
  - Reglas:
    - `hospitalizado = SI`.
    - `especialidad_deducida = HEMATOONCOLOGIA ADULTO` (heurística fija).
    - `malignidad` desde `diagnostico_rev`.
    - `usuario_finalizacion_final = 'NANCY MEJIA VARGAS'` si se reconoce la firma.
    - `organo_final` limpiando saltos de línea y textos auxiliares.

## Mapeo a Excel
- `map_to_excel_format(extracted_data) -> list[dict]`:
  - Genera una fila con las 55 columnas.
  - Completa Sede/Departamento/Municipio/Tarifa/Valor desde `HUV_CONFIG`.
  - Fija “Ubicación” a “OBSERVACION CONS URGENCIAS” e “Identificador Unico” en el ejemplo de plantilla.

## Entrada/Salida
- Entrada: PDF seleccionado mediante diálogo.
- Salida: `Informe_Revision_<timestamp>.xlsx` en la carpeta del PDF.

## Observaciones
- Consolidar cómo se alimentan “Ubicación” e “Identificador Unico” para generalizar a más plantillas.
- Ajustar `deduce_specialty_revision` si se amplían servicios/centros de origen.
