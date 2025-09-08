# Guia de Inicio Rapido - OCR Medico HUV

## Instalacion Express (5 minutos)

### Windows
```cmd
# 1) Descargar e instalar Tesseract OCR
# https://github.com/UB-Mannheim/tesseract/wiki

# 2) Instalar dependencias de Python
pip install -r requirements.txt

# 3) Ejecutar la aplicacion
python huv_ocr_sistema_definitivo.py
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-spa poppler-utils
pip install -r requirements.txt
python huv_ocr_sistema_definitivo.py
```

### macOS
```bash
brew install tesseract tesseract-lang poppler
pip install -r requirements.txt
python huv_ocr_sistema_definitivo.py
```

## Uso en 3 pasos

1) Agregar PDFs: "Agregar Archivos" o "Agregar Carpeta".
2) Elegir destino: "Seleccionar Carpeta de Salida".
3) Procesar: "Procesar PDFs".

### Procesadores especializados (opcional)
Puedes ejecutar los procesadores individuales por tipo:
```bash
python procesador_ihq.py
python procesador_biopsia.py
python procesador_revision.py
```

## Verificacion rapida

```bash
python test_sistema.py
```

## Problemas comunes

| Problema | Solucion |
|---|---|
| Tesseract not found | Instalar Tesseract y agregar al PATH o configurar en config.ini |
| No module named ... | `pip install -r requirements.txt` |
| Resultados imprecisos | Aumentar DPI en config.ini, revisar calidad del PDF |
| Lento con PDFs grandes | Procesar por lotes pequenos, cerrar otras apps |

## Rendimiento esperado

- 1 PDF (2 paginas): ~30 s
- 10 PDFs: ~5 min
- Precision: 85-95% (segun calidad del documento)

---
Para mas detalles tecnicos: `analisis/README.md`
