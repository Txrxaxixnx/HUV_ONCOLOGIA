# Análisis: `crear_ejecutable.py`

## Rol
- Construcción de ejecutable autónomo con PyInstaller.

## Flujo
1) Verifica/instala PyInstaller.
2) Ejecuta `pyinstaller --onefile --windowed --name=OCR_Medico huv_ocr_sistema_definitivo.py`.
3) Verifica artefactos en `dist/` y muestra instrucciones de distribución.

## Notas
- El ejecutable aún requiere Tesseract instalado en la máquina destino.
- Se puede extender agregando `--add-data` para paquetes de datos (p. ej., `spa.traineddata` si se distribuye externamente).

## Sugerencias
- Añadir `.spec` personalizado para incluir archivos de configuración (`config.ini`) y controlar iconos/metadata.

