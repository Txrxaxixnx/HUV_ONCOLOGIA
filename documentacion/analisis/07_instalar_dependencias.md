# Analisis: `instalar_dependencias.py`

## Rol
- Instalador express de dependencias Python y guia de instalacion de Tesseract.
- Genera/actualiza `requirements.txt`.

## Flujo actual
1. Verifica version de Python y actualiza `pip`.
2. Instala paquetes minimos (legacy): `pytesseract`, `PyMuPDF`, `pillow`, `pandas`, `openpyxl`, `python-dateutil`.
3. Crea o actualiza `requirements.txt` con esa lista.
4. Muestra instrucciones para instalar Tesseract por sistema operativo y valida `tesseract --version`.

## Ajustes necesarios para v2.5
- Incluir nuevas dependencias: `customtkinter`, `matplotlib`, `seaborn`, `selenium`, `webdriver-manager`, `ttkbootstrap`, `Babel`, `holidays`.
- Opcional: `numpy` (requerido indirectamente por pandas/matplotlib) y `scipy` si se agregan analiticas futuras.
- Considerar chequear la presencia de Google Chrome (requerido por Selenium).

## Notas
- No instala Tesseract automaticamente; proporciona instrucciones (mantener por permisos).
- En macOS puede intentar usar Homebrew si esta disponible.

## Recomendaciones
- Actualizar el script para leer dependencias desde `requirements.txt` y evitar duplicacion.
- Agregar modos silenciosos (`--yes/--quiet`) para automatizacion sin interaccion.
- Registrar en log los paquetes instalados y los que ya estaban presentes.

## Mejora futura
- Detectar y descargar `spa.traineddata` cuando no este presente o indicar la ubicacion oficial.
- Validar versiones minimas (ej. Selenium >= 4.12) y reportar incompatibilidades.
- Ofrecer opcion de crear entorno virtual automaticamente.