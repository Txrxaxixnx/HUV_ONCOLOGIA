# Analisis: `huv_ocr_sistema_definitivo.py`

## Rol
- Script de entrada. Inicializa configuracion para Tesseract (segun SO) y lanza la interfaz Tkinter (`HUVOCRSystem`).

## Estructura
- Lee `config.ini` con `configparser`.
- Determina la ruta de `tesseract` por sistema: `WINDOWS_TESSERACT`, `MACOS_TESSERACT`, `LINUX_TESSERACT` o variables de entorno.
- Si se define, asigna `pytesseract.pytesseract.tesseract_cmd`.
- Crea ventana raiz `tk.Tk()`, instancia `HUVOCRSystem` y entra a `mainloop()`.

## Dependencias
- `ui.HUVOCRSystem` (interfaz principal).
- `pytesseract` (para configurar binario tesseract).
- `config.ini` (seccion PATHS).

## Errores comunes
- Ruta Tesseract incorrecta -> OCR falla. Ver `config.ini` o variables de entorno.
- Falta de Tesseract en el sistema -> instalar segun README/INICIO_RAPIDO.

## Extensiones posibles
- Aceptar argumentos CLI (ej.: `--headless` para modo sin UI).
- Validar existencia del ejecutable de Tesseract y mostrar alerta clara antes de abrir la UI.
