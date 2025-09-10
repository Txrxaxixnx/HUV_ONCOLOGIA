            messagebox.showwarning("Sin resultados", "No se pudo extraer informaciÃ³n de ningÃºn archivo")
#ui.py:
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interfaz grÃ¡fica del sistema OCR HUV."""

import threading
from datetime import datetime
from pathlib import Path
import configparser

import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, PatternFill

from ocr_processing import pdf_to_text_enhanced
from data_extraction import process_text_to_excel_rows, detect_report_type

_config = configparser.ConfigParser(interpolation=None)
_config.read(Path(__file__).resolve().parent / "config.ini", encoding="utf-8")

TIMESTAMP_FORMAT = _config.get("OUTPUT", "TIMESTAMP_FORMAT", fallback="%Y%m%d_%H%M%S")
OUTPUT_FILENAME = _config.get("OUTPUT", "OUTPUT_FILENAME", fallback="informes_medicos")

WINDOW_WIDTH = _config.getint("INTERFACE", "WINDOW_WIDTH", fallback=900)
WINDOW_HEIGHT = _config.getint("INTERFACE", "WINDOW_HEIGHT", fallback=700)
LOG_HEIGHT = _config.getint("INTERFACE", "LOG_HEIGHT", fallback=8)


class HUVOCRSystem:
    """Interfaz basada en Tkinter para procesar informes PDF."""

