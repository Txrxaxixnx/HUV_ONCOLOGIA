# Analisis: `calendario.py`

## Rol
- Proporciona un `CalendarioInteligente` basado en `ttkbootstrap` para seleccionar fechas con contexto (festivos, datos de usuario).
- Se utiliza en la vista Automatizar BD Web para elegir rangos de consulta.

## Caracteristicas
- Modal `Toplevel` con bloqueo (`grab_set`) para asegurar interaccion.
- Carga dinamica de festivos mediante la libreria `holidays` (cache por anio).
- Permite resaltar dias con informacion adicional (`mapa_de_datos`).
- Integra tooltips que describen el estado del dia (usando `ttkbootstrap.tooltip`).
- Soporta cambio de tema y localizacion via Babel (`get_month_names`, `get_day_names`).

## Uso
- Metodo de clase `seleccionar_fecha` devuelve la fecha seleccionada o None.
- Parametros relevantes: `fecha_inicial`, `mapa_de_datos`, `locale`, `codigo_pais_festivos`, `mapa_estilos`.
- Se centra sobre la ventana padre y retorna al cerrar (OK/Cancelar).

## Integracion con la UI
- `ui.App.open_web_auto_modal` lo usa para fijar fechas inicial/final sin abandonar la ventana modal.
- Tras seleccionar fecha se reactiva el modal original asegurando foco y `grab_set`.

## Riesgos y mejoras
- Requiere `holidays` y `Babel`; validar instalacion en entornos nuevos.
- Manejar correctamente la ausencia de internet para carga de festivos (si aplica).
- Agregar soporte para seleccionar rangos multiples o calendario doble en futuras versiones.