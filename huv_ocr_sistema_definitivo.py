#huv_ocr_sistema_definitivo.py:
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Punto de entrada principal para el sistema OCR del HUV."""

import os
import sys
import configparser
from pathlib import Path
import tkinter as tk
import pytesseract

# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ CONFIGURACIÃ“N â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
_config = configparser.ConfigParser(interpolation=None)
_config.read(Path(__file__).resolve().parent / 'config.ini', encoding='utf-8')

if sys.platform.startswith("win"):
    tesseract_cmd = _config.get('PATHS', 'WINDOWS_TESSERACT', fallback=os.getenv('WINDOWS_TESSERACT'))
elif sys.platform.startswith("darwin"):
    tesseract_cmd = _config.get('PATHS', 'MACOS_TESSERACT', fallback=os.getenv('MACOS_TESSERACT'))
else:
    tesseract_cmd = _config.get('PATHS', 'LINUX_TESSERACT', fallback=os.getenv('LINUX_TESSERACT'))

if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

from ui import HUVOCRSystem
from tkinter import filedialog, messagebox
from pathlib import Path as _P
import threading

def _start_processing_ihq_avanzado(self) -> None:
    try:
        files = filedialog.askopenfilenames(
            title="Seleccionar archivos PDF IHQ",
            filetypes=[("Archivos PDF", "*.pdf")],
        )
        paths = list(files)
        if not paths:
            messagebox.showwarning("Sin archivos", "No se seleccionaron PDFs IHQ")
            return
        outdir = filedialog.askdirectory(title="Seleccionar carpeta de salida para IHQ")
        if not outdir:
            return
        def _worker():
            try:
                from procesador_ihq_biomarcadores import process_ihq_paths
                self._log("Procesando IHQ (biomarcadores)...")
                output_path = process_ihq_paths(paths, outdir)
                self._log(f"IHQ listo: {_P(output_path).name}")
                messagebox.showinfo("IHQ Completado", f"Archivo generado:\n{output_path}")
            except Exception as e:
                self._log(f"Error IHQ: {e}")
                messagebox.showerror("Error IHQ", str(e))
        threading.Thread(target=_worker, daemon=True).start()
    except Exception as e:
        try:
            self._log(f"Error inesperado IHQ: {e}")
        except Exception:
            pass

from ui import HUVOCRSystem as _UI
_UI.start_processing_ihq_avanzado = _start_processing_ihq_avanzado


def main() -> None:
    """Inicializa la interfaz y arranca el sistema."""
    root = tk.Tk()
    HUVOCRSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()

