# Analisis: `instalar_dependencias.py`

## Rol
- Instalador "express" de dependencias Python y guia de instalacion de Tesseract.
- Genera un `requirements.txt` basico.

## Flujo
1) Verifica version de Python y actualiza `pip`.
2) Instala paquetes: `pytesseract`, `PyMuPDF`, `pillow`, `pandas`, `openpyxl`, `python-dateutil`.
3) Crea/actualiza `requirements.txt`.
4) Muestra instrucciones para instalar Tesseract por sistema operativo y verifica `tesseract --version`.

## Notas
- No instala Tesseract en Windows/Linux; entrega instrucciones (correcto por permisos).
- En macOS intenta instalar via Homebrew si esta disponible.

## Sugerencias
- Anadir validacion de presencia de `spa.traineddata` y guia para ubicarla si falta.
- Ofrecer opcion `--yes/--quiet` para automatizacion sin interaccion.
