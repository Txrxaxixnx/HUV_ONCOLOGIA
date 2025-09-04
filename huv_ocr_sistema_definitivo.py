#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Punto de entrada principal para el sistema OCR del HUV."""

import os, re, sys, io, threading, configparser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, date
from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import pandas as pd
from huv_constants import (
    HUV_CONFIG,
    CUPS_CODES,
    PROCEDIMIENTOS,
    ESPECIALIDADES_SERVICIOS,
    PATTERNS_HUV,
    MALIGNIDAD_KEYWORDS,
)

# ─────────────────────────── CONFIGURACIÓN ─────────────────────────────
_config = configparser.ConfigParser()
_config.read('config.ini')

if sys.platform.startswith("win"):
    tesseract_cmd = _config.get('PATHS', 'WINDOWS_TESSERACT', fallback=os.getenv('WINDOWS_TESSERACT'))
elif sys.platform.startswith("darwin"):
    tesseract_cmd = _config.get('PATHS', 'MACOS_TESSERACT', fallback=os.getenv('MACOS_TESSERACT'))
else:
    tesseract_cmd = _config.get('PATHS', 'LINUX_TESSERACT', fallback=os.getenv('LINUX_TESSERACT'))

if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

# ─────────────────────── FUNCIONES DE UTILIDAD ───────────────────────
def detect_report_type(text: str) -> str:
    """Detecta el tipo de informe basado en patrones del HUV"""
    # Buscar número de petición
    m = re.search(r'N\.\s*peticion\s*:\s*([A-Z0-9\-]+)', text, re.IGNORECASE)
    if m:
        numero = m.group(1)
        if re.match(r'A\d{6}', numero):
            return 'AUTOPSIA'
        elif re.match(r'IHQ\d{6}', numero):
            return 'INMUNOHISTOQUIMICA' 
        elif re.match(r'M\d{7}', numero):
            return 'BIOPSIA'
        elif re.match(r'R\d{6}', numero):
            return 'REVISION'
    
    # Detectar por contenido
    text_upper = text.upper()
    if 'AUTOPSIA' in text_upper:
        return 'AUTOPSIA'
    elif 'INMUNOHISTOQUIMICA' in text_upper:
        return 'INMUNOHISTOQUIMICA'
    elif 'HISTOLOGIA' in text_upper or 'BIOPSIA' in text_upper:
        return 'BIOPSIA'
    elif 'REVISION' in text_upper:
        return 'REVISION'
    
    return 'DESCONOCIDO'

def split_full_name(full_name: str) -> dict:
    """Divide nombre completo según lógica del HUV"""
    if not full_name:
        return {'primer_nombre': '', 'segundo_nombre': '', 'primer_apellido': '', 'segundo_apellido': ''}
    
    parts = [p.strip() for p in full_name.strip().split() if p.strip()]
    result = {'primer_nombre': '', 'segundo_nombre': '', 'primer_apellido': '', 'segundo_apellido': ''}
    
    if len(parts) == 1:
        result['primer_nombre'] = parts[0]
    elif len(parts) == 2:
        result['primer_nombre'] = parts[0]
        result['primer_apellido'] = parts[1]
    elif len(parts) == 3:
        result['primer_nombre'] = parts[0]
        result['primer_apellido'] = parts[1]
        result['segundo_apellido'] = parts[2]
    elif len(parts) >= 4:
        result['primer_nombre'] = parts[0]
        result['segundo_nombre'] = parts[1]
        result['primer_apellido'] = parts[2]
        result['segundo_apellido'] = ' '.join(parts[3:])
    
    return result

def calculate_birth_date(edad: int, fecha_referencia: str = None) -> str:
    """Calcula fecha de nacimiento basada en edad"""
    try:
        if fecha_referencia:
            ref_date = datetime.strptime(fecha_referencia, '%Y-%m-%d').date()
        else:
            ref_date = date.today()
        
        birth_year = ref_date.year - edad
        birth_date = date(birth_year, ref_date.month, ref_date.day)
        return birth_date.strftime('%d/%m/%Y')
    except:
        return ''

from ui import HUVOCRSystem


def main() -> None:
    """Inicializa la interfaz y arranca el sistema."""
    root = tk.Tk()
    HUVOCRSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
