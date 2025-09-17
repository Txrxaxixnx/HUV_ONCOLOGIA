# Analisis: `crear_ejecutable.py`

## Rol
- Guia para construir un ejecutable autonomo con PyInstaller.

## Flujo actual
1. Verifica/instala PyInstaller.
2. Ejecuta `pyinstaller --onefile --windowed --name=OCR_Medico huv_ocr_sistema_definitivo.py`.
3. Indica que el ejecutable quedara en `dist/` y recuerda instalar Tesseract en la maquina destino.

## Consideraciones v2.5
- El ejecutable debe incluir `config.ini` y asegurarse de que `huv_oncologia.db` tenga una ubicacion escribible.
- Selenium y webdriver-manager descargan Chromedriver en tiempo de ejecucion; se requiere conexion y Chrome instalado.
- CustomTkinter, matplotlib y seaborn incrementan el tamano del bundle; considerar usar `--exclude-module` para componentes no usados.

## Recomendaciones
- Crear un archivo `.spec` personalizado para agregar recursos (`config.ini`, iconos) y establecer la ruta de datos.
- Documentar los pasos post-instalacion: instalar Tesseract, agregar `spa.traineddata`, verificar Chrome.
- Probar el ejecutable en entorno limpio (sin Python) para validar que las dependencias embebidas funcionen.

## Mejoras posibles
- Automatizar la copia de `config.ini` y la creacion de carpeta de logs/datos.
- Agregar versionado en el nombre del ejecutable (`--name=EVARISIS_Gestor_v2_5`).
- Evaluar empaquetadores alternos (cx_Freeze, Briefcase) si se requiere mejor integracion con instaladores GUI.