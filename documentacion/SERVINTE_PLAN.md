Plan de Integracion con SERVINTE (Fase 4 - EVARISIS Gestor H.U.V)

Objetivo
- Integrar EVARISIS Gestor H.U.V con SERVINTE para carga automatica y segura de datos normalizados desde la base SQLite, eliminando la dependencia de Excel y reduciendo tiempos de registro.

Alcance funcional previsto
- Exportacion por lotes (CSV/DataFrame) y/o integracion por API si esta disponible.
- Validaciones previas por registro y por esquema; gestion de reintentos y bitacora de auditoria.
- Modo dry-run para pruebas sin impacto y reportes diferenciales.
- Parametrizacion via `config.ini` (switch de activacion, endpoints, credenciales, timeouts, tamano de lote).
- Resguardos: colas locales de reenvio y respaldos por lote transmitido.

Consideraciones tecnicas
- Trazabilidad: ID de lote, ID de registro, sellos de tiempo y estados (exito, error, reintento).
- Seguridad: uso de HTTPS, manejo seguro de credenciales y control de acceso por rol.
- Observabilidad: metricas de procesados/aceptados/rechazados, logs rotados y alertas tempranas.

Estado a 15/09/2025
- Planeado dentro de la Fase 4. La version 2.5 deja lista la base SQLite (`huv_oncologia.db`) y el pipeline de limpieza, habilitando la proxima etapa de integracion con SERVINTE.
- Acciones pendientes: definir especificaciones tecnicas del conector, establecer entorno de pruebas con datos anonimizados y validar esquema de autenticacion.
