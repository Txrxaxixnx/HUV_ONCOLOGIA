# 📄 OCR Médico - Procesador de Informes PDF

Una aplicación de escritorio desarrollada en Python para procesar informes médicos en formato PDF utilizando tecnología OCR (Reconocimiento Óptico de Caracteres). Extrae automáticamente datos estructurados de informes de inmunohistoquímica y los organiza en archivos Excel.

## 🌟 Características

- **Interfaz gráfica amigable**: Desarrollada con tkinter
- **Procesamiento por lotes**: Procesa múltiples PDFs simultáneamente  
- **OCR optimizado**: Utiliza Tesseract con configuración específica para documentos médicos
- **Extracción inteligente**: Reconoce patrones específicos de informes médicos
- **Salida estructurada**: Genera archivos Excel organizados por columnas
- **Procesamiento en segundo plano**: No bloquea la interfaz durante el procesamiento
- **Log detallado**: Seguimiento en tiempo real del proceso
- **Liviano y portable**: Puede convertirse en ejecutable independiente

## 📋 Requisitos del Sistema

- **Python 3.7+** (recomendado Python 3.9+)
- **Sistema operativo**: Windows 10+, Linux Ubuntu 18+, macOS 10.14+
- **RAM**: Mínimo 4GB (recomendado 8GB)
- **Espacio en disco**: 500MB libres
- **Tesseract OCR**: Engine de OCR (se instala por separado)

## 🚀 Instalación Rápida

### Método 1: Instalación Automática (Recomendado)

1. **Descargar el proyecto**:
   ```bash
   git clone <repositorio>
   cd ocr-medico
   ```

2. **Ejecutar el instalador automático**:
   ```bash
   python instalar_dependencias.py
   ```

3. **Ejecutar la aplicación**:
   ```bash
   python ocr_medico_app.py
   ```

### Método 2: Instalación Manual

1. **Instalar Python**: Descarga desde [python.org](https://python.org)

2. **Instalar Tesseract OCR**:

   **Windows**:
   - Descarga desde [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
   - Instala y anota la ruta (ej: `C:\Program Files\Tesseract-OCR\`)

    **Linux (Ubuntu/Debian)**:
    Ejecuta manualmente:
    ```bash
    sudo apt-get update
    sudo apt-get install tesseract-ocr tesseract-ocr-spa poppler-utils
    ```

   **macOS**:
   ```bash
   brew install tesseract tesseract-lang poppler
   ```

3. **Instalar dependencias de Python**:
   ```bash
    pip install pytesseract PyMuPDF pillow pandas openpyxl python-dateutil
   ```

## 🔧 Configuración

### Configurar Ruta de Tesseract (Solo Windows)

Si Tesseract no se encuentra automáticamente, edita el archivo `ocr_medico_app.py` en la línea:

```python
# Busca esta línea (aproximadamente línea 35)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

Cambia la ruta por donde instalaste Tesseract.

### Verificar Instalación

```bash
tesseract --version
python -c "import pytesseract, fitz, PIL, pandas, openpyxl, dateutil; print('✅ Todas las dependencias instaladas')"
```

## 📖 Manual de Uso

### 1. Iniciar la Aplicación

```bash
python ocr_medico_app.py
```

### 2. Agregar Archivos PDF

**Opción A - Archivos individuales**:
- Clic en "🗂️ Agregar Archivos PDF"
- Selecciona uno o varios archivos PDF
- Se agregarán a la lista

**Opción B - Carpeta completa**:
- Clic en "📁 Agregar Carpeta" 
- Selecciona una carpeta
- Se agregarán todos los PDFs de la carpeta

### 3. Configurar Salida

- Clic en "📂 Seleccionar Carpeta de Salida"
- Elige donde guardar el archivo Excel resultante

### 4. Procesar Documentos

- Clic en "🚀 Procesar PDFs"
- Observa el progreso en la barra y en el log
- Al finalizar, se mostrará la ubicación del archivo Excel

### 5. Revisar Resultados

El archivo Excel generado contiene estas columnas:

| Campo | Descripción |
|-------|-------------|
| `archivo_origen` | Nombre del PDF procesado |
| `nombre` | Nombre del paciente |
| `numero_peticion` | Número de petición del estudio |
| `identificacion` | Documento de identidad |
| `genero` | Género del paciente |
| `edad` | Edad del paciente |
| `eps` | Entidad de salud |
| `medico_tratante` | Médico responsable |
| `servicio` | Servicio médico |
| `fecha_ingreso` | Fecha de ingreso |
| `fecha_informe` | Fecha del informe |
| `organo` | Órgano estudiado |
| `receptores_estrogeno` | Resultado receptores de estrógeno |
| `receptores_progesterona` | Resultado receptores de progesterona |
| `her2` | Resultado HER2 |
| `ki67` | Índice de proliferación Ki-67 |
| `patologo` | Patólogo responsable |
| `fecha_procesamiento` | Cuando se procesó el documento |

## 🔧 Crear Ejecutable (Opcional)

Para crear un archivo `.exe` que funcione sin instalar Python:

1. **Instalar PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Crear el ejecutable**:
   ```bash
   pyinstaller --onefile --windowed --name="OCR_Medico" ocr_medico_app.py
   ```

3. **Encontrar el ejecutable**:
   - Se crea en la carpeta `dist/`
   - Archivo: `OCR_Medico.exe` (Windows) o `OCR_Medico` (Linux/Mac)

4. **Distribuir**:
   - Copia el ejecutable a cualquier computadora
   - **Importante**: Tesseract OCR debe estar instalado en la máquina destino

## 🛠️ Solución de Problemas

### Error: "Tesseract not found"

**Solución**:
- Verifica que Tesseract esté instalado: `tesseract --version`
- En Windows, ajusta la ruta en el código
- Agrega Tesseract al PATH del sistema

### Error: "No module named 'pytesseract'"

**Solución**:
```bash
pip install pytesseract PyMuPDF pillow pandas openpyxl python-dateutil
```

### Error: "Permission denied" o problemas de permisos

**Solución**:
- Ejecuta como administrador (Windows) o con `sudo` (Linux/Mac)
- Verifica permisos de las carpetas de entrada y salida

### PDFs no se procesan correctamente

**Solución**:
- Verifica que los PDFs no estén corruptos
- Asegúrate de que sean informes médicos con texto legible
- Aumenta la resolución de DPI en el código (línea con `convert_from_path`)

### Resultados de OCR imprecisos

**Solución**:
- Verifica la calidad del PDF original
- Los mejores resultados se obtienen con PDFs de alta resolución
- Documentos escaneados pueden requerir preprocesamiento adicional

### Error de memoria con PDFs grandes

**Solución**:
- Procesa archivos en lotes más pequeños
- Cierra otras aplicaciones para liberar RAM
- Considera usar una máquina con más memoria

## 📝 Tipos de Documentos Soportados

La aplicación está optimizada para informes de **inmunohistoquímica** que contengan:

- Datos del paciente (nombre, identificación, edad, etc.)
- Información del estudio (fechas, médico, servicio)
- Resultados de biomarcadores (receptores de estrógeno, progesterona, HER2, Ki-67)
- Diagnóstico y patólogo responsable

Para otros tipos de informes médicos, es necesario modificar las expresiones regulares en la función `extract_medical_data()`.

## 🔄 Personalización

### Modificar Campos Extraídos

Edita la función `extract_medical_data()` en `ocr_medico_app.py`:

```python
# Agregar nuevos patrones
patterns = {
    'nuevo_campo': r'Patrón de búsqueda: ([^\n]+)',
    # ... otros patrones
}
```

### Cambiar Configuración de OCR

Modifica la línea de configuración de Tesseract:

```python
# Configuración actual
config = '--psm 6 -c tessedit_char_whitelist=...'

# Otras opciones útiles:
# --psm 3: Completamente automático (por defecto)
# --psm 6: Un bloque uniforme de texto
# --psm 11: Texto disperso
```

## 📊 Rendimiento

### Tiempos Estimados

- **1 PDF (2 páginas)**: 15-30 segundos
- **10 PDFs**: 3-5 minutos  
- **50 PDFs**: 15-25 minutos

*Los tiempos varían según la potencia del procesador y calidad de los PDFs*

### Optimización

- **DPI**: Balance entre calidad y velocidad (300 DPI recomendado)
- **Páginas**: Procesa solo las páginas necesarias (1-2 por defecto)
- **Resolución**: Las imágenes se redimensionan automáticamente

## 🤝 Contribuir

¿Quieres mejorar la aplicación?

1. Fork el repositorio
2. Crea una rama: `git checkout -b mi-mejora`
3. Realiza cambios y confirma: `git commit -m 'Agregar nueva característica'`
4. Push: `git push origin mi-mejora`
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

¿Necesitas ayuda?

- 📧 **Email**: [tu-email@ejemplo.com]
- 🐛 **Issues**: Reporta bugs en el repositorio
- 💬 **Discusiones**: Usa las discusiones del repositorio

## 🏆 Créditos

Desarrollado por **[Tu Nombre]** con:

- **Tesseract OCR**: Google's open-source OCR engine
- **pytesseract**: Python wrapper for Tesseract
- **tkinter**: Python's standard GUI library
- **pandas & openpyxl**: Data processing and Excel generation

---

⭐ **¿Te gusta el proyecto?** ¡Dale una estrella en GitHub!

**Última actualización**: $(date +'%Y-%m-%d')
