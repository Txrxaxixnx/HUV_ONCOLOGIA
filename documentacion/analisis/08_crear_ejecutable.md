# Analisis: `crear_ejecutable.py`

## Rol
- Construccion de ejecutable autonomo con PyInstaller.

## Flujo
1) Verifica/instala PyInstaller.
2) Ejecuta `pyinstaller --onefile --windowed --name=OCR_Medico huv_ocr_sistema_definitivo.py`.
3) Verifica artefactos en `dist/` y muestra instrucciones de distribucion.

## Notas
- El ejecutable aun requiere Tesseract instalado en la maquina destino.
- Se puede extender agregando `--add-data` para paquetes de datos (p. ej., `spa.traineddata` si se distribuye externamente).

## Sugerencias
- Anadir `.spec` personalizado para incluir archivos de configuracion (`config.ini`) y controlar iconos/metadata.
