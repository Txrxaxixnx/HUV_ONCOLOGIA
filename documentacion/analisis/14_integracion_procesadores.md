# Analisis: Integracion de procesadores

## Estado actual
- IHQ esta integrado al flujo moderno (SQLite + dashboard).
- Biopsia, Autopsia y Revision operan solo en la ruta legacy (Excel).

## Estrategia de integracion
1. Revisar patrones y campos obligatorios de cada procesador legacy.
2. Crear adaptadores que transformen la salida legacy a diccionarios compatibles con `database_manager.save_records`.
3. Extender la tabla SQLite con columnas especificas (manteniendo la compatibilidad con informes IHQ).
4. Actualizar la UI para permitir filtros por tipo de informe y graficos adicionales.

## Dependencias
- `procesador_ihq_biomarcadores` ya reusa logica de `procesador_ihq`; se espera seguir la misma linea con Biopsia/Autopsia/Revision.
- Se requiere actualizar `huv_constants.py` cuando se agreguen nuevos codigos o patrones.

## Consideraciones
- La base actual contiene columnas específicas de IHQ; se debe evaluar normalizar campos comunes o crear tablas adicionales.
- Garantizar que la insercion en SQLite siga el mismo control de duplicados (numero de peticion).
- Actualizar pruebas y dashboard para reflejar nuevos tipos de informe.

## Proximos pasos sugeridos
- Diseñar un mapeo maestro que indique para cada tipo de informe que columnas se poblan.
- Implementar pruebas cruzadas (legacy vs nuevo pipeline) antes de habilitar la vista en produccion.
- Coordinar con BI/Power BI para asegurar que los cambios de esquema se reflejen en los reportes.
