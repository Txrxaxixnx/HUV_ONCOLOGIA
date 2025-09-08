# Plan de Integración de Procesadores al Flujo Principal

## Objetivo
Integrar los procesadores especializados (IHQ, Biopsia, Revisión) al pipeline principal sin romper compatibilidad con la app actual.

## Estrategia
- Enrutar por tipo detectado y delegar la extracción al procesador cuando exista uno especializado.
- Mantener `data_extraction.map_to_excel_format` como mapeador por defecto; permitir que cada procesador use su propio mapeo si genera múltiples filas (p.ej., Biopsia).
- Habilitar/inhabilitar la integración vía bandera de configuración para despliegues controlados.

## Cambios propuestos (mínimos y seguros)
- `data_extraction.py`:
  - Añadir funciones de puente (import lazy/try-except) hacia `procesador_ihq`, `procesador_biopsia`, `procesador_revision`.
  - Nueva función `extract_data_router(text)`: usa `detect_report_type(text)` y:
    - Si tipo == IHQ y módulo disponible: `procesador_ihq.extract_ihq_data(text)`.
    - Si tipo == BIOPSIA: `procesador_biopsia.extract_biopsy_data(text)` + `procesador_biopsia.extract_specimens_data(text, num)` para construir filas.
    - Si tipo == REVISION: `procesador_revision.extract_revision_data(text)`.
    - En caso contrario: `extract_huv_data(text)` (actual).
  - Para el mapeo:
    - IHQ/REVISION: usar `procesador_ihq.map_to_excel_format(data)` / `procesador_revision.map_to_excel_format(data)`.
    - BIOPSIA: usar `procesador_biopsia.map_to_excel_format(common_data, specimens)`.
    - Fallback: `map_to_excel_format(extracted_data, filename)` actual.
- `ui.py`:
  - Cambiar llamada de `extract_huv_data` a `extract_data_router` y adaptar mapeo según retorno.
  - Mantener logs y artefacto de depuración sin cambios.

## Bandera de activación
- Añadir en `config.ini` (sección `[PROCESSORS]`): `ENABLE_PROCESSORS = true|false`.
- Si `false`, usar siempre `extract_huv_data` + `map_to_excel_format` actual.

## Orden de trabajo sugerido
1) Limpieza de imports y consolidación de esquema de datos (hecho: eliminación de imports obsoletos en `data_extraction.py`).
2) Implementar `extract_data_router` con `try/except ImportError` para no romper en entornos mínimos.
3) Ajustar `ui.py` a la nueva ruta de extracción y mapeo sin cambiar la UI.
4) Validar con PDFs de ejemplo (IHQ, Biopsia múltiple, Revisión).
5) Documentar comportamiento y actualizar `INICIO_RAPIDO.md`.

## Riesgos y mitigaciones
- Diferencias en claves del diccionario entre módulos: documentar el contrato mínimo de campos; agregar rellenos por defecto.
- Variaciones de plantillas: mantener pruebas con textos representativos y revisar patrones al incorporar nuevas fuentes.
- Codificación: asegurar UTF-8 y sanitización de caracteres previos al mapeo.

## Futuro
- Extraer `PATTERNS_BASE` común y unificar utilidades compartidas (split de nombre, fechas, normalizaciones) en un módulo `common_extraction.py`.
- Añadir tests unitarios por procesador y pruebas de regresión para patrones críticos.

