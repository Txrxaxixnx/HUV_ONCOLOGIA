# Plan de Integración con SERVINTE

Este documento resume la propuesta para habilitar el envío automático de datos normalizados desde el pipeline OCR hacia SERVINTE.

## Objetivo
- Automatizar la transmisión segura de datos clínico-administrativos hacia SERVINTE, reduciendo retrabajos y tiempos de registro.

## Alcance (fases)
- Exportación por lotes en formato interoperable (CSV) y/o integración por API (si está disponible).
- Validaciones previas por registro y esquema, gestión de reintentos y bitácora de auditoría.
- Modo “dry-run” para verificación sin impacto productivo y reportes de diferencias.
- Parametrización vía `config.ini` (activar/desactivar, endpoints, autenticación, timeouts, tamaño de lote).
- Resguardos: colas locales para reenvío, y archivos de respaldo de cada lote transmitido.

## Consideraciones Técnicas
- Trazabilidad: ID de lote, ID de registro y sellos de tiempo por operación.
- Seguridad: uso de HTTPS y credenciales almacenadas de forma segura.
- Observabilidad: métricas básicas (procesados, aceptados, rechazados, reintentos) y logs rotados.

## Estado
- Planeado. No habilitado por defecto en la versión actual del sistema.

