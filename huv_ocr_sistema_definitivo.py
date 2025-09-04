#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Punto de entrada principal para el sistema OCR del HUV."""

import os
import sys
import configparser
from pathlib import Path
import tkinter as tk
import pytesseract

# ─────────────────────────── CONFIGURACIÓN ─────────────────────────────
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


def main() -> None:
    """Inicializa la interfaz y arranca el sistema."""
    root = tk.Tk()
    HUVOCRSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
