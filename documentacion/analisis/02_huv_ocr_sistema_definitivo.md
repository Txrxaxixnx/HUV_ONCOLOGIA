# Analisis: `huv_ocr_sistema_definitivo.py`

## Rol
- Script de entrada. Configura la ruta de Tesseract segun el sistema operativo y lanza la nueva interfaz `App` definida en `ui.py`.

## Flujo
1. Lee `config.ini` con `configparser` (sin interpolacion) para obtener las claves `[PATHS]`.
2. Determina `pytesseract.pytesseract.tesseract_cmd` segun plataforma (Windows/Mac/Linux) si la ruta existe.
3. Muestra advertencia si la ruta no es valida y se apoyara en el PATH del sistema.
4. Instancia `App()` y ejecuta `mainloop()`. La clase App hereda de `customtkinter.CTk`, por lo que no se requiere `tk.Tk()` externo.

## Diferencias frente a la version legacy
- La UI ahora usa CustomTkinter y centraliza todo el flujo (procesamiento, dashboard, automatizacion).
- El script no genera Excel ni maneja archivos temporales; se limita a preparar el entorno y disparar la UI.
- Se conserva el uso de `config.ini`, pero el resultado principal es `huv_oncologia.db` administrado desde `ui.py`.

## Riesgos y buenas practicas
- Validar que `config.ini` este presente junto al ejecutable; en despliegues empaquetados incluirlo como recurso.
- Mostrar mensajes claros cuando la ruta de Tesseract sea invalida para facilitar soporte en campo.
- Futuras versiones podrian aceptar parametros CLI (ej. `--headless`, `--config=/ruta`, `--log-level`).
