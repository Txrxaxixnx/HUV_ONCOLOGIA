# Analisis: `procesador_biopsia.py` (estado v2.5)

## Situacion actual
- Se mantiene en `LEGACY/` con salida Excel (55 columnas).
- Aun no se integra al pipeline SQLite ni al dashboard.

## Responsabilidades en legacy
- Extraer campos clinicos de informes de biopsia (organos, margenes, diagnostico).
- Utiliza `huv_constants` y regex especificas para corrientes de texto.

## Plan de migracion
1. Reutilizar helpers comunes (normalizacion, identificacion) para generar un diccionario compatible con SQLite.
2. Ampliar el esquema de `huv_oncologia.db` o crear tablas relacionadas para campos exclusivos de biopsia.
3. Agregar visualizaciones especificas (ej. distribucion por organo, margenes positivos).
4. Implementar pruebas comparativas con la version legacy antes de activar en la UI.

## Riesgos
- Cambios en plantillas de biopsia pueden requerir nuevas regex.
- Faltan datasets anonimizados representativos para pruebas automatizadas.

## Recomendaciones
- Construir set de fixtures anonimizados que cubran escenarios tipicos (con/ sin margenes, organos multiples).
- Definir columnas minimas para integracion (fecha, servicio, responsable, organo, margenes, diagnostico).
- Coordinar con el area clinica para priorizar biomarcadores o indicadores especificos de biopsia.
