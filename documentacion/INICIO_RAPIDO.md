Guia de Inicio Rapido - EVARISIS Gestor H.U.V (v2.5)

Proyecto institucional del Hospital Universitario del Valle, liderado por Oncologia y desarrollado por el Area de Innovacion y Desarrollo.

Instalacion express (menos de 10 minutos)
- Windows
```cmd
pip install -r requirements.txt
python huv_ocr_sistema_definitivo.py
```
- Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-spa poppler-utils
pip install -r requirements.txt
python huv_ocr_sistema_definitivo.py
```
- macOS
```bash
brew install tesseract tesseract-lang poppler
pip install -r requirements.txt
python huv_ocr_sistema_definitivo.py
```

Primera ejecucion
1) Verifique que Tesseract este accesible (config.ini o PATH).
2) Ejecute `python huv_ocr_sistema_definitivo.py`.
3) El sistema instalara automaticamente ChromeDriver (requiere internet la primera vez).

Uso en 4 pasos
1) Procesar PDFs: seleccione archivo(s) IHQ, observe el log y espere el mensaje de registros guardados.
2) La aplicacion extrae biomarcadores, normaliza datos y guarda el resultado en `huv_oncologia.db`.
3) Visualizar datos: abra la pestaña correspondiente, use el buscador o seleccione una fila para ver detalles.
4) Dashboard Analitico: ajuste filtros, explore graficos y abra modo pantalla completa con doble clic.

Automatizar BD Web
- Abra la vista Automatizar BD Web.
- Ingrese usuario, clave y rango de fechas (boton Elegir abre el calendario inteligente).
- El bot Selenium recorre el portal `huvpatologia.qhorte.com`, establece el criterio y ejecuta la consulta.

Verificacion rapida
```bash
tesseract --version
python -c 'import pytesseract, fitz, pandas, customtkinter, selenium'
```

Problemas comunes
- Tesseract not found: ajuste `config.ini` o agregue la ruta al PATH.
- Error Selenium/Chrome: actualice Google Chrome y reintente; el driver se vuelve a descargar.
- OCR pobre: aumente `OCR_SETTINGS.DPI` o mejore el PDF de origen.
- Registro duplicado: revise si el PDF reutiliza el mismo numero de peticion.

Atajos utiles
- F5 en Visualizar datos ejecuta la opcion Actualizar.
- Doble clic sobre un grafico abre modo pantalla completa.
- El switch Modo Claro alterna la paleta de la UI en vivo.

Mas detalles
- Documentacion completa: `documentacion/README.md`.
- Analisis por modulo: `documentacion/analisis/README.md`.
