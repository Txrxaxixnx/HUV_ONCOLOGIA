# Analisis: Procesadores especializados

## Estado actual (v2.5)
- IHQ: activo y remodelado en `procesador_ihq_biomarcadores.py`; integra biomarcadores y persistencia SQLite.
- Biopsia, Autopsia, Revision: disponibles en `LEGACY/` con salida Excel; pendientes de migracion al pipeline persistente.

## Objetivos por procesador
- IHQ: mantener cobertura de biomarcadores, tolerancia a OCR y duplicados; extender a nuevos marcadores cuando se soliciten.
- Biopsia: migrar patrones a una version compatible con la base SQLite, incluir mapeo de margenes y organos.
- Autopsia: adaptar descripciones largas y tiempos de necropsia para analisis temporal.
- Revision: conservar trazabilidad de diagnostico original vs revision y documentar reglas de conciliacion.

## Plan de migracion
1. Consolidar helpers compartidos (normalizacion de nombres, fechas, servicios) en un modulo comun.
2. Migrar Biopsia -> SQLite usando enfoque similar al de IHQ (segmentacion, persistencia, dashboard).
3. Migrar Autopsia y Revision, asegurando campos clave para indicadores clinicos.
4. Actualizar dashboard para permitir filtros por tipo de informe una vez se incorporen nuevos procesadores.

## Riesgos
- Divergencia entre codigo legacy y nuevo si se corrige un patron en un solo lado.
- Falta de pruebas unitarias para procesadores legacy; se recomienda crear fixtures antes de migrar.

## Recomendaciones
- Documentar casos de prueba representativos (PDF anonimizados) para cada plantilla.
- Incorporar validaciones automatizadas comparando salida legacy vs nueva pipeline antes de retirar Excel.
- Planear capacitacion a usuarios cuando se integren nuevos tipos de informe al dashboard.
