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

# ─────────────────────── CONFIGURACIÓN HOSPITALARIA ───────────────────────
HUV_CONFIG = {
    'hospital_name': 'HOSPITAL UNIVERSITARIO DEL VALLE',
    'hospital_code': 'HUV',
    'sede_default': 'PRINCIPAL',
    'departamento_default': 'VALLE DEL CAUCA',
    'municipio_default': 'CALI',
    'tipo_documento_default': 'CC',
    'tarifa_default': 'GENERAL',
    'valor_default': 0.0
}

# ─────────────────────── CÓDIGOS Y ESPECIALIDADES ─────────────────────────
CUPS_CODES = {
    'AUTOPSIA': '898301',
    'INMUNOHISTOQUIMICA': '898807', 
    'BIOPSIA': '898201',
    'REVISION': '898806',
    'CITOLOGIA': '898241',
    'CONGELACION': '898242'
}

PROCEDIMIENTOS = {
    '898301': '898301 Autopsia completa',
    '898807': '898807 Estudio anatomopatologico de marcacion inmunohistoquimica basica (especifico)',
    '898201': '898201 Estudio de coloracion basica en especimen de reconocimiento',
    '898806': '898806 Verificacion integral con preparacion de material de rutina'
}

ESPECIALIDADES_SERVICIOS = {
    'UCI': 'MEDICO INTENSIVISTA',
    'GINECOLOGIA': 'GINECOLOGIA Y OBSTETRICIA',
    'GINECOLOGIA ONCOLOGICA': 'GINECOLOGIA ONCOLOGICA',
    'ALTO RIESGO OBSTETRICO': 'GINECOLOGIA ONCOLOGICA',
    'MEDICINA': 'MEDICINA GENERAL',
    'URGENCIAS': 'MEDICINA DE URGENCIAS',
    'NEONATOLOGIA': 'NEONATOLOGIA',
    'PEDIATRIA': 'PEDIATRA'
}

# ─────────────────────── PATRONES REGEX DEFINITIVOS (VERSIÓN CORREGIDA) ───────────────────────
PATTERNS_HUV = {
    # Información básica del paciente - Patrones más robustos que capturan hasta el final de la línea
    'nombre_completo': r'Nombre\s*:\s*([^\n]+?)\s*N\.\s*peticion',
    'numero_peticion': r'N\.\s*peticion\s*:\s*([A-Z0-9\-]+)',
    'identificacion_completa': r'N\.Identificación\s*:\s*([A-Z]{1,3}\.?\s*[0-9\.]+)',
    'identificacion_numero': r'N\.Identificación\s*:\s*[A-Z\.]{1,3}\s*([0-9\.]+)',
    'tipo_documento': r'N\.Identificación\s*:\s*([A-Z]{1,3})\.?',
    'genero': r'Genero\s*:\s*([A-Z]+)',
    'edad': r'Edad\s*:\s*(\d+)\s*años', # <--- Captura solo los dígitos antes de "años"
    'eps': r'EPS\s*:\s*([^\n]+)',
    'medico_tratante': r'Médico tratante\s*:\s*([^\n]+)',
    'servicio': r'Servicio\s*:\s*([^\n]+)',
    'fecha_ingreso': r'Fecha Ingreso\s*:\s*(\d{2}/\d{2}/\d{4})',
    'fecha_informe': r'Fecha Informe\s*:\s*(\d{2}/\d{2}/\d{4})',

    'fecha_autopsia': r'Fecha y hora de la autopsia:\s*(\d{2}/\d{2}/\d{4})',

    
    # Información específica de estudios
    'organo': r'Organo\s*:\s*([A-ZÁÉÍÓÚÑ\s\+\(\)]+)',
    'fecha_toma': r'Fecha toma\s*:\s*(\d{4}-\d{2}-\d{2})',
    
    # Responsables
    'responsable_analisis': r'([A-ZÁÉÍÓÚÑ\s]+)\s*\n\s*Responsable del análisis', # <--- Más específico
    'usuario_finalizacion': r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}),\s*([A-ZÁÉÍÓÚÑ\s]+)',
    
    # Descripciones largas (CORRECCIÓN CRÍTICA AQUÍ)
    'descripcion_macroscopica': r'DESCRIPCIÓN MACROSCÓPICA\s*(.+?)(?=DESCRIPCIÓN MICROSCÓPICA|PROTOCOLO MICROSCÓPICO|DIAGN[OÓ]STICO|$)',
    'descripcion_microscopica': r'(?:DESCRIPCIÓN MICROSCÓPICA|PROTOCOLO MICROSCÓPICO)\s*(.+?)(?=DIAGN[OÓ]STICO|COMENTARIOS|$)',
    'diagnostico': r'DIAGN[OÓ]STICO\s*(.+?)(?=COMENTARIOS|Todos los análisis|Responsable|$)', # <--- CORREGIDO con [OÓ]
    'comentarios': r'COMENTARIOS\s*(.+?)(?=Todos los análisis|Responsable|$)',
    
    # Identificadores únicos en contenido
    'identificador_unico': r'Identificador Unico[^:]*:\s*(\d+)',
    'numero_autorizacion': r'N\.\s*Autorizacion[^:]*:\s*([A-Z0-9]+)',
}

# ─────────────────────── PALABRAS CLAVE PARA MALIGNIDAD ───────────────────────
MALIGNIDAD_KEYWORDS = [
    'CARCINOMA', 'CANCER', 'MALIGNO', 'MALIGNIDAD', 'METASTASIS', 'METASTÁSICO',
    'NEOPLASIA MALIGNA', 'TUMOR MALIGNO', 'ADENOCARCINOMA', 'LINFOMA', 
    'SARCOMA', 'MELANOMA', 'LEUCEMIA', 'HODGKIN', 'HODKING'
]

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
