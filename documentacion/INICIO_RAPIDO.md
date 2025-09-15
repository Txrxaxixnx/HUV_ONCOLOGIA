Guía de Inicio Rápido – EVARISIS Gestor H.U.V

Proyecto institucional del Hospital Universitario del Valle (HUV), desarrollado por el Área de Innovación y Desarrollo y liderado clínicamente por el Dr. Juan Camilo Bayona (Oncología).

Instalación Express (5 minutos)
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

Uso en 3 pasos
1) Agregar PDFs: “Agregar Archivos” o “Agregar Carpeta”.
2) Elegir destino: “Seleccionar Carpeta de Salida”.
3) Procesar: “Procesar PDFs”.

Análisis Avanzado IHQ (v1.1)
- Botón: “Analizar Biomarcadores IHQ (v1.1)”.
- Selecciona uno o varios PDFs de IHQ y una carpeta de salida.
- Se genera un Excel separado con biomarcadores (HER2, Ki‑67, RE/ER, RP/PR, PD‑L1, P16 y Estudios Solicitados) sin afectar el esquema estándar.

Procesadores especializados (opcional)
```bash
python procesador_autopsia.py
python procesador_ihq.py
python procesador_biopsia.py
python procesador_revision.py
```

Verificación rápida
```bash
python test_sistema.py
```

Problemas comunes
| Problema               | Solución                                                          |
|---                     |---                                                                |
| Tesseract not found    | Instalar Tesseract y agregar al PATH o configurar en `config.ini` |
| No module named …      | `pip install -r requirements.txt`                                 |
| Resultados imprecisos  | Aumentar `DPI`; revisar calidad del PDF                           |
| Lento con PDFs grandes | Procesar por lotes pequeños; cerrar otras apps                    |

Rendimiento esperado
- 1 PDF (2 páginas): ~30 s
- 10 PDFs: ~5 min
- Precisión: 85–95% (según calidad del documento)

Más detalles técnicos: `analisis/README.md`
