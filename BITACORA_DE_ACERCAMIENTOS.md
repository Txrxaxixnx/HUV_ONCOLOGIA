Bitácora de Acercamientos – EVARISIS Gestor H.U.V

Propósito
- Registro formal y auditable de la evolución del proyecto. Documenta cada sesión de trabajo y validación con el Dr. Juan Camilo Bayona y otros stakeholders.

Plantilla por Entrada
---
### Reunión de Seguimiento - [Fecha de la Reunión]

Versión del Proyecto Presentada: v[Número de Versión]

1. Resumen y Objetivos de la Sesión
- [Breve descripción de los temas tratados]

2. Impacto y Hallazgos de la Versión Actual
- [Comentarios sobre valor y funcionamiento]

3. Estado de Requerimientos Anteriores (Compromisos de la reunión del [Fecha Anterior])
- [Requerimiento 1]: [Estado]
- [Requerimiento 2]: [Estado]
- [Requerimiento 3]: [Estado]

4. Feedback, Mejoras Críticas y Nuevas Ideas
- [Puntos clave y sugerencias]

5. Nuevos Requerimientos (Compromisos para la v[Siguiente Versión])
- [Requerimiento A]: [Descripción]
- [Requerimiento B]: [Descripción]
---

Entradas

### Reunión de Seguimiento - 05 de septiembre, 2025
Versión del Proyecto Presentada: v1.0 – Funcionalidad Base

1. Resumen y Objetivos de la Sesión
- Presentación de la versión 1.0 con cuatro procesadores (Autopsia, IHQ, Biopsia, Revisión) y exportación validada a 55 columnas.

2. Impacto y Hallazgos de la Versión Actual
- Reducción drástica de tiempos de transcripción manual; mejora en calidad y trazabilidad de datos.

3. Estado de Requerimientos Anteriores (sin registro previo)
- N/A

4. Feedback, Mejoras Críticas y Nuevas Ideas
- Priorizar extracción avanzada para IHQ (biomarcadores clave) y preparar integración a dashboards.

5. Nuevos Requerimientos (Compromisos para la v1.1)
- Enriquecimiento IHQ: HER2, KI67, RE, RP, PDL-1, Estudios Solicitados, P16 (Estado/Porcentaje).
- Diseño de módulo de adquisición automatizada (scraper institucional) para `huvpatologia.qhorte.com`.
- Plan técnico de migración a base de datos y alineación con Power BI.

### Reunión de Seguimiento - 10 de septiembre, 2025
Versión del Proyecto Presentada: v1.1 – Análisis Avanzado IHQ

1. Resumen y Objetivos de la Sesión
- Presentación de la versión 1.1 con el botón de “Analizar Biomarcadores IHQ (v1.1)” en la UI y generación de Excel extendido con biomarcadores.

2. Impacto y Hallazgos de la Versión Actual
- Análisis profundo de IHQ sin afectar el esquema operativo estándar; facilita investigación y validaciones clínicas.

3. Estado de Requerimientos Anteriores (Compromisos de la reunión del 05 de septiembre, 2025)
- Enriquecimiento IHQ: ✅ Completado (v1.1 – extractor dedicado y botón en UI).
- Diseño de módulo de adquisición automatizada: ⏳ En proceso (definición de flujos y autenticación).
- Plan técnico de migración a BD y alineación con Power BI: ⏳ En proceso.

4. Feedback, Mejoras Críticas y Nuevas Ideas
- Mantener extractor IHQ independiente para evitar riesgos en operación.
- Considerar plantillas de salida alternativas (CSV/tablas) para carga a BD en Fase 3.

5. Nuevos Requerimientos (Compromisos para la v1.2)
- Prototipo funcional del scraper institucional (login, filtros, descarga, estructura de carpetas).
- Diseño de modelo de datos relacional para Fase 3 y primer ETL desde Excel estándar + IHQ extendido.
