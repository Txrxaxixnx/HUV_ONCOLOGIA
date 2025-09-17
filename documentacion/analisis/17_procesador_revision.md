# Analisis: `procesador_revision.py` (estado v2.5)

## Situacion actual
- Se conserva en `LEGACY/` generando Excel; no se ha migrado a la base SQLite.
- Responsable de capturar informacion de revisiones de lamina/segunda opinion.

## Elementos clave en legacy
- Comparacion entre diagnostico original y revision.
- Identificacion de responsable, fechas de revision, comentarios adicionales.

## Plan de migracion
1. Definir campos minimos para revision dentro de la base (diagnostico original, revisado, motivo, responsable).
2. Adaptar regex y normalizaciones para alimentar SQLite usando `database_manager`.
3. Extender el dashboard con indicadores de concordancia y motivos de revision.

## Riesgos
- Diferencias de formato entre revisiones antiguas y recientes.
- Necesidad de anonimizar datos sensibles (comentarios libres).

## Recomendaciones
- Crear pruebas con casos reales anonimizados que incluyan discrepancias y confirmaciones.
- Coordinar con patologia para definir niveles de severidad/accion a incluir en los reportes.
- Planear capacitacion al equipo sobre nuevos filtros de concordancia una vez se integre al dashboard.
