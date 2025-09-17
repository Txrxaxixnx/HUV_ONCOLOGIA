# Analisis: `huv_web_automation.py`

## Rol
- Automatiza el portal institucional `huvpatologia.qhorte.com` (modulo Entrega de resultados) usando Selenium y webdriver-manager.
- Permite ejecutar consultas guiadas desde la UI sin abandonar EVARISIS Gestor.

## Flujo
1. Configura Chrome con opciones headless opcionales y maximiza la ventana.
2. Inicia sesion con las credenciales provistas (`Credenciales`).
3. Navega al menu SEGUIMIENTO / Entrega de resultados.
4. Selecciona criterio (por data-valor o texto) y establece fechas.
5. Ejecuta la consulta e intenta detectar la tabla de resultados o mensajes de respuesta.
6. Retorna True si la ejecucion fue exitosa y cierra el navegador.

## Funciones y utilidades
- `automatizar_entrega_resultados(...)`: funcion principal; recibe fechas en formato DD/MM/AAAA, credenciales y callbacks de log.
- `_log`: helper que reenvia mensajes al callback o a stdout.
- Diccionario `CRITERIOS`: mapea etiquetas a data-valor para el menu desplegable.

## Dependencias
- `selenium`, `webdriver_manager.chrome`, `Options`, `WebDriverWait`, `expected_conditions`.
- Requiere Google Chrome instalado; webdriver-manager descarga el driver adecuado.

## Integracion con la UI
- `ui.App.open_web_auto_modal` construye el formulario y lanza `_run_web_automation` en un hilo daemon.
- Los mensajes de avance se muestran en la ventana de Procesar PDFs o en la barra de estado.

## Riesgos y mitigaciones
- Cambios en el HTML del portal pueden romper selectores; mantener pruebas manuales periodicas.
- Las credenciales deben manejarse con cuidado (no se almacenan en disco).
- La automatizacion no descarga archivos automaticamente; solo prepara la consulta.

## Mejoras futuras
- Agregar opcion headless en la UI, con advertencia de compatibilidad.
- Exportar resultados (ej. `pandas.read_html`) cuando el portal lo permita.
- Registrar metricas de ejecucion (tiempo, errores) para auditoria.