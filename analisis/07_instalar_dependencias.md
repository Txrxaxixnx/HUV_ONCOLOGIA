# Análisis: `instalar_dependencias.py`

## Rol
- Instalador “express” de dependencias Python y guía de instalación de Tesseract.
- Genera un `requirements.txt` básico.

## Flujo
1) Verifica versión de Python y actualiza `pip`.
2) Instala paquetes: `pytesseract`, `PyMuPDF`, `pillow`, `pandas`, `openpyxl`, `python-dateutil`.
3) Crea/actualiza `requirements.txt`.
4) Muestra instrucciones para instalar Tesseract por sistema operativo y verifica `tesseract --version`.

## Notas
- No instala Tesseract en Windows/Linux; entrega instrucciones (correcto por permisos).
- En macOS intenta instalar vía Homebrew si está disponible.

## Sugerencias
- Añadir validación de presencia de `spa.traineddata` y guía para ubicarla si falta.
- Ofrecer opción `--yes/--quiet` para automatización sin interacción.

