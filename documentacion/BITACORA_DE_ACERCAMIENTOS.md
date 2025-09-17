Bitacora de Acercamientos - EVARISIS Gestor H.U.V

Proposito
- Registro formal y auditable de la evolucion del proyecto. Documenta cada sesion de trabajo y validacion con el Dr. Juan Camilo Bayona, el Jefe de Gestion de la Informacion (Ing. Diego Pena) y otros stakeholders.

Plantilla por entrada
---
### Reunion de Seguimiento - [Fecha]
Version del Proyecto Presentada: v[X.Y]

1. Resumen y Objetivos
- [Breve descripcion de los temas tratados]

2. Impacto y Hallazgos
- [Valor generado y hallazgos principales]

3. Estado de Requerimientos Anteriores
- [Requerimiento]: [Estado]

4. Feedback y Nuevas Ideas
- [Puntos clave]

5. Nuevos Requerimientos
- [Requerimiento]: [Descripcion]
---

Entradas

### Reunion de Seguimiento - 05 de septiembre, 2025
Version del Proyecto Presentada: v1.0 - Funcionalidad base

1. Resumen y Objetivos
- Presentacion de la version 1.0 con cuatro procesadores (Autopsia, IHQ, Biopsia, Revision) y exportacion validada a 55 columnas.

2. Impacto y Hallazgos
- Reduccion drastica de tiempos de transcripcion manual; mejora en calidad y trazabilidad de datos.

3. Estado de Requerimientos Anteriores
- Sin registro previo.

4. Feedback y Nuevas Ideas
- Priorizar extraccion avanzada para IHQ (biomarcadores clave) y preparar integracion a dashboards.

5. Nuevos Requerimientos (v1.1)
- Enriquecimiento IHQ: HER2, KI67, RE, RP, PDL-1, Estudios Solicitados, P16 (Estado/Porcentaje).
- Diseno de modulo de adquisicion automatizada (scraper institucional) para `huvpatologia.qhorte.com`.
- Plan tecnico de migracion a base de datos y alineacion con Power BI.

### Reunion de Seguimiento - 10 de septiembre, 2025
Version del Proyecto Presentada: v1.1 - Analisis Avanzado IHQ

1. Resumen y Objetivos
- Presentacion de la version 1.1 con boton Analizar Biomarcadores IHQ (v1.1) y generacion de Excel extendido con biomarcadores.

2. Impacto y Hallazgos
- Analisis profundo de IHQ sin alterar el flujo operativo; soporte para investigacion y validaciones clinicas.

3. Estado de Requerimientos Anteriores (05/09/2025)
- Enriquecimiento IHQ: completado (v1.1 con extractor dedicado y boton en UI).
- Modulo de adquisicion automatizada: en proceso (definicion de flujos y autenticacion).
- Plan tecnico de migracion a BD y Power BI: en proceso.

4. Feedback y Nuevas Ideas
- Mantener extractor IHQ independiente para aislar riesgos operativos.
- Evaluar plantillas de salida alternativas (CSV/tablas) para carga a BD en Fase 3.

5. Nuevos Requerimientos (v1.2)
- Prototipo funcional del scraper institucional (login, filtros, descarga, estructura de carpetas).
- Diseno de modelo de datos relacional para Fase 3 y primer ETL desde Excel estandar + IHQ extendido.

### Reunion de Seguimiento - 15 de septiembre, 2025
Version del Proyecto Presentada: v2.5 - Plataforma Persistente y Dashboard Integrado

1. Resumen y Objetivos
- Presentacion del redisenho completo de la aplicacion, pipeline persistente en SQLite y dashboard analitico integrado.

2. Impacto y Hallazgos
- Eliminacion de Excel operativo; datos disponibles en linea para decision rapida.
- Visualizacion inmediata de volumenes, biomarcadores y tiempos con filtros hospitalarios.

3. Estado de Requerimientos Anteriores (10/09/2025)
- Scraper institucional: entregado como modulo de automatizacion web (login, filtros, ejecucion guiada).
- Modelo de datos relacional: primera entrega implementada en `huv_oncologia.db` (tabla informes_ihq).
- Integracion Power BI: pendiente (requiere conectores y datasets ampliados).

4. Feedback y Nuevas Ideas
- Priorizar incorporacion de Biopsia y Autopsia al pipeline persistente.
- Habilitar exportacion directa a CSV o Power Query para acelerar informes estadisticos.
- Explorar paneles clinicos personalizados por servicio (mastologia, ginecologia, etc.).

5. Nuevos Requerimientos (v2.6)
- Unificar procesadores de Biopsia y Autopsia sobre la base SQLite con indicadores de calidad.
- Definir flujo de publicacion a Power BI (dataset incremental + dataflows).
- Incorporar pruebas automatizadas para patrones de extraccion y graficos clave.
