# 🚀 Guía de Inicio Rápido - OCR Médico

## ⚡ Instalación Express (5 minutos)

### Windows
```cmd
# 1. Descargar e instalar Tesseract OCR
# https://github.com/UB-Mannheim/tesseract/wiki

# 2. Instalar Python dependencies
pip install pytesseract pdf2image pillow pandas openpyxl

# 3. Ejecutar aplicación
python ocr_medico_app.py
```

### Linux (Ubuntu/Debian)
```bash
# 1. Instalar Tesseract y dependencias del sistema
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-spa poppler-utils

# 2. Instalar Python dependencies
pip install pytesseract pdf2image pillow pandas openpyxl

# 3. Ejecutar aplicación
python ocr_medico_app.py
```

### macOS
```bash
# 1. Instalar Tesseract
brew install tesseract tesseract-lang poppler

# 2. Instalar Python dependencies
pip install pytesseract pdf2image pillow pandas openpyxl

# 3. Ejecutar aplicación
python ocr_medico_app.py
```

## 🖱️ Uso en 3 Pasos

1. **📂 Agregar PDFs**: Clic en "Agregar Archivos" o "Agregar Carpeta"
2. **💾 Elegir destino**: Clic en "Seleccionar Carpeta de Salida" 
3. **🚀 Procesar**: Clic en "Procesar PDFs" y esperar

## ✅ Verificación Rápida

```python
# Ejecutar para probar el sistema
python test_sistema.py
```

## 🔧 Solución de Problemas Comunes

| Problema | Solución |
|----------|----------|
| "Tesseract not found" | Instalar Tesseract OCR y agregarlo al PATH |
| "No module named ..." | `pip install -r requirements.txt` |
| Resultados imprecisos | Verificar calidad del PDF original |
| Proceso muy lento | Usar PDFs de menos de 5MB, cerrar otras apps |

## 📊 Rendimiento Esperado

- **1 PDF (2 páginas)**: ~30 segundos
- **10 PDFs**: ~5 minutos
- **Precisión**: 85-95% (dependiendo de calidad del documento)

---
💡 **Para más detalles**: Ver README.md completo
