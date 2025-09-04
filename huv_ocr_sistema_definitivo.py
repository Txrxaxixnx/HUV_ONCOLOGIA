#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# huv_ocr_sistema_definitivo.py:
"""
Sistema OCR para Hospital Universitario del Valle - VERSIÓN DEFINITIVA
Extracción precisa basada en análisis de mapeo PDF → Excel real

Autor: Sistema de Análisis HUV
Fecha: Agosto 2025
"""

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

def convert_date_format(date_str: str) -> str:
    """Normaliza a DD/MM/YYYY desde DD/MM/YYYY, DD-MM-YYYY o YYYY-MM-DD"""
    import re
    try:
        if not date_str:
            return ''
        s = str(date_str).strip()
        # yyyy-mm-dd -> dd/mm/yyyy
        m = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', s)
        if m:
            y, mo, d = m.groups()
            return f"{d}/{mo}/{y}"
        # dd-mm-yyyy -> dd/mm/yyyy
        m = re.match(r'^(\d{1,2})-(\d{1,2})-(\d{4})$', s)
        if m:
            d, mo, y = m.groups()
            return f"{int(d):02d}/{int(mo):02d}/{y}"
        # dd/mm/yyyy -> validar y normalizar ceros a la izquierda
        m = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{4})$', s)
        if m:
            d, mo, y = m.groups()
            return f"{int(d):02d}/{int(mo):02d}/{y}"
        # catch-all para d-m-aaaa o d/m/aaaa
        m = re.match(r'^(\d{1,2})[-/](\d{1,2})[-/](\d{4})$', s)
        if m:
            d, mo, y = m.groups()
            return f"{int(d):02d}/{int(mo):02d}/{y}"
        return s
    except Exception:
        return ''


def detect_malignancy(diagnostico: str, descripcion_micro: str = '') -> str:
    """Detecta malignidad basada en palabras clave"""
    text_to_check = f"{diagnostico} {descripcion_micro}".upper()
    
    for keyword in MALIGNIDAD_KEYWORDS:
        if keyword in text_to_check:
            return 'PRESENTE'
    
    return 'AUSENTE'

def deduce_specialty(servicio: str, tipo_informe: str = '') -> str:
    """Deduce especialidad basada en servicio y tipo de informe"""
    servicio_upper = servicio.upper()
    
    # Buscar coincidencias exactas primero
    for key, specialty in ESPECIALIDADES_SERVICIOS.items():
        if key in servicio_upper:
            return specialty
    
    # Casos específicos
    if 'UCI' in servicio_upper:
        return 'MEDICO INTENSIVISTA'
    elif 'GINECO' in servicio_upper:
        return 'GINECOLOGIA Y OBSTETRICIA'
    elif 'OBSTETRICO' in servicio_upper:
        return 'GINECOLOGIA ONCOLOGICA'
    elif 'URGENCIA' in servicio_upper:
        return 'MEDICINA DE URGENCIAS'
    elif 'NEONAT' in servicio_upper:
        return 'NEONATOLOGIA'
    elif 'PEDIATR' in servicio_upper:
        return 'PEDIATRA'
    else:
        return 'MEDICINA GENERAL'

def determine_hospitalization(servicio: str, tipo_informe: str) -> str:
    """Determina si el paciente está hospitalizado"""
    servicio_upper = servicio.upper()
    
    # Siempre hospitalizados
    if any(keyword in servicio_upper for keyword in ['UCI', 'URGENCIAS', 'ADMISION', 'QUIROFANO']):
        return 'SI'
    
    # Por tipo de informe
    if tipo_informe in ['AUTOPSIA', 'BIOPSIA']:
        return 'SI'
    elif tipo_informe in ['INMUNOHISTOQUIMICA', 'REVISION']:
        return 'NO'
    
    return 'NO'

def extract_specimens(organo_text: str, numero_peticion: str) -> list:
    """Extrae información de especímenes múltiples de forma más robusta."""
    found_specimens = []
    
    # Patrones para buscar especímenes múltiples A., B., C., etc.
    # Usamos re.finditer para obtener las coincidencias y sus posiciones
    matches = list(re.finditer(r'(?m)^[ \t]*([A-J])\.\s*[\"\']?([^\"\'\:\n]+?)[\"\' ]?\s*:', organo_text))
    
    # Si encontramos más de una coincidencia (ej. A y B), o si la única coincidencia no es 'A'
    # (indicando que es parte de una serie), procesamos como múltiples especímenes.
    if len(matches) > 1 or (len(matches) == 1 and matches[0].group(1).upper() != 'A'):
        for match in matches:
            suffix = match.group(1).upper()
            organo = match.group(2).strip()
            found_specimens.append({
                'muestra': f"{numero_peticion}-{suffix}",
                'organo': organo
            })

    # Si NO hay evidencia clara de múltiples especímenes (o solo hay una "A."),
    # se asume que es una única muestra y se usa el número de petición principal.
    if not found_specimens:
        # Extraemos el texto del órgano, limpiando posibles marcadores "A." al inicio.
        organo_limpio = re.sub(r'^[A-Z]\.\s*', '', organo_text.strip()).strip()
        found_specimens.append({
            'muestra': numero_peticion,
            'organo': organo_limpio if organo_limpio else "No especificado"
        })
        
    return found_specimens

# ─────────────────────── EXTRACCIÓN PRINCIPAL ─────────────────────────
def extract_huv_data(text: str) -> dict:
    """Extracción de datos según la lógica exacta del HUV"""
    data = {}
    
    # 1. Detectar tipo de informe
    tipo_informe = detect_report_type(text)
    data['tipo_informe'] = tipo_informe
    
    # 2. Extraer datos básicos
    for key, pattern in PATTERNS_HUV.items():
        try:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                value = match.group(1).strip()
                # Limpiar valor
                value = re.sub(r'\s+', ' ', value)
                data[key] = value
            else:
                data[key] = ''
        except Exception as e:
            data[key] = ''
    
    # 3. Procesar nombres
    if data.get('nombre_completo'):
        names = split_full_name(data['nombre_completo'])
        data.update(names)
    
    # 4. Procesar identificación
    if data.get('identificacion_numero'):
        # Limpiar puntos y espacios
        data['identificacion_numero'] = re.sub(r'[^\d]', '', data['identificacion_numero'])
    
    # 5. Calcular fecha de nacimiento
    if data.get('edad'):
        try:
            # Ahora data['edad'] es solo el número, ej: "33"
            edad = int(data['edad']) 
            data['fecha_nacimiento'] = calculate_birth_date(edad)
        except:
            data['fecha_nacimiento'] = ''
    
    # 6. Convertir fechas
    for date_field in ['fecha_ingreso', 'fecha_informe']:
        if data.get(date_field):
            data[f"{date_field}_converted"] = convert_date_format(data[date_field])
    

    # 6.1. Ahora: separa “Fecha ordenamiento” y deja “Fecha ingreso” sin tocar
    if tipo_informe == 'AUTOPSIA' and data.get('fecha_autopsia'):
        data['fecha_ordenamiento'] = data['fecha_autopsia']  # p.ej. 12/07/2025
    else:
        data['fecha_ordenamiento'] = data.get('fecha_ingreso', '')

    # 7. Deducir campos automáticos
    servicio = data.get('servicio', '')
    data['especialidad_deducida'] = deduce_specialty(servicio, tipo_informe)
    data['hospitalizado'] = determine_hospitalization(servicio, tipo_informe)
    
    # 8. Detectar malignidad
    diagnostico = data.get('diagnostico', '')
    descripcion_micro = data.get('descripcion_microscopica', '')
    data['malignidad'] = detect_malignancy(diagnostico, descripcion_micro)
    
    # 9. Asignar códigos según tipo
    if tipo_informe in CUPS_CODES:
        data['cups_code'] = CUPS_CODES[tipo_informe]
        data['procedimiento'] = PROCEDIMIENTOS.get(CUPS_CODES[tipo_informe], '')
    
    # 10. Configuración específica por tipo
    if tipo_informe == 'AUTOPSIA':
        data['organo_final'] = 'CUERPO HUMANO COMPLETO'
        data['hospitalizado'] = 'SI'
    elif tipo_informe == 'INMUNOHISTOQUIMICA':
        data['hospitalizado'] = 'NO'
        data['n_autorizacion'] = 'COEX'
        data['identificador_unico'] = '0'
    
    # 11. Procesar especímenes múltiples
    if tipo_informe == 'AUTOPSIA':
        # Forzar una sola muestra para autopsia completa
        num = data.get('numero_peticion', '')
        data['specimens'] = [{'muestra': num, 'organo': 'CUERPO HUMANO COMPLETO'}]
    else:
        organo_text = data.get('organo', '') + ' ' + data.get('descripcion_macroscopica', '')
        data['specimens'] = extract_specimens(organo_text, data.get('numero_peticion', ''))
    return data

# ─────────────────────── MAPEO A EXCEL ─────────────────────────
def map_to_excel_format(extracted_data: dict, filename: str) -> list:
    """Mapea datos extraídos al formato Excel de 55 columnas del HUV"""
    
    # Definir las 55 columnas exactas
    excel_columns = [
        "N. peticion (0. Numero de biopsia)", "Hospitalizado", "Sede", "EPS", "Servicio",
        "Médico tratante", "Especialidad", "Ubicación", "N. Autorizacion", "Identificador Unico",
        "Datos Clinicos", "Fecha ordenamiento", "Tipo de documento", "N. de identificación",
        "Primer nombre", "Segundo nombre", "Primer apellido", "Segundo apellido",
        "Fecha de nacimiento", "Edad", "Genero", "Número celular",
        "Direccion de correo electronico", "Direccion de correo electronico 2",
        "Contacto de emergencia", "Departamento", "Teléfono del contacto", "Municipio",
        "N. muestra", "CUPS", "Tipo de examen (4, 12, Metodo de obtención de la muestra, factor de certeza para el diagnóstico) ",
        "Procedimiento (11. Tipo de estudio para el diagnóstico)", "Organo (1. Muestra enviada a patología)",
        "Tarifa", "Valor", "Copago", "Descuento", "Fecha de ingreso (2. Fecha de la muestra)",
        "Fecha finalizacion (3. Fecha del informe)", "Usuario finalizacion", "Usuario asignacion micro",
        "Fecha asignacion micro", "Malignidad", "Condicion", "Descripcion macroscopica",
        "Descripcion microscopica (8,9, 10,12,. Invasión linfovascular y perineural, indice mitótico/Ki67, Inmunohistoquímica, tamaño tumoral)",
        "Descripcion Diagnostico (5,6,7 Tipo histológico, subtipo histológico, margenes tumorales)",
        "Diagnostico Principal", "Comentario", "Informe adicional", "Congelaciones /Otros estudios",
        "Liquidos (5 Tipo histologico)", "Citometria de flujo (5 Tipo histologico)",
        "Hora Desc. macro", "Responsable macro"
    ]
    
    # Crear filas para cada espécimen
    rows = []
    specimens = extracted_data.get('specimens', [{'muestra': extracted_data.get('numero_peticion', ''), 'organo': extracted_data.get('organo', '')}])
    
    for specimen in specimens:
        row_data = {}
        
        # Mapeo directo de campos
        row_data["N. peticion (0. Numero de biopsia)"] = extracted_data.get('numero_peticion', '')
        row_data["Hospitalizado"] = extracted_data.get('hospitalizado', 'NO')
        row_data["Sede"] = HUV_CONFIG['sede_default']
        row_data["EPS"] = extracted_data.get('eps', '')
        row_data["Servicio"] = extracted_data.get('servicio', '')
        row_data["Médico tratante"] = extracted_data.get('medico_tratante', '')
        row_data["Especialidad"] = extracted_data.get('especialidad_deducida', '')
        row_data["Ubicación"] = extracted_data.get('servicio', '')
        row_data["N. Autorizacion"] = extracted_data.get('n_autorizacion', '')
        row_data["Identificador Unico"] = extracted_data.get('identificador_unico', '')
        
        # Datos clínicos
        row_data["Datos Clinicos"] = 'SI' if len(extracted_data.get('descripcion_macroscopica', '')) > 100 else 'NO'
        row_data["Fecha ordenamiento"] = convert_date_format(extracted_data.get('fecha_ordenamiento',''))
        row_data["Tipo de documento"] = extracted_data.get('tipo_documento', HUV_CONFIG['tipo_documento_default'])
        row_data["N. de identificación"] = extracted_data.get('identificacion_numero', '')
        
        # Nombres
        row_data["Primer nombre"] = extracted_data.get('primer_nombre', '')
        row_data["Segundo nombre"] = extracted_data.get('segundo_nombre', '')
        row_data["Primer apellido"] = extracted_data.get('primer_apellido', '')
        row_data["Segundo apellido"] = extracted_data.get('segundo_apellido', '')
        
        # Datos personales
        row_data["Fecha de nacimiento"] = extracted_data.get('fecha_nacimiento', '')
        row_data["Edad"] = extracted_data.get('edad', '')
        row_data["Genero"] = extracted_data.get('genero', '')
        row_data["Número celular"] = ''
        row_data["Direccion de correo electronico"] = ''
        row_data["Direccion de correo electronico 2"] = ''
        row_data["Contacto de emergencia"] = ''
        row_data["Departamento"] = HUV_CONFIG['departamento_default']
        row_data["Teléfono del contacto"] = ''
        row_data["Municipio"] = HUV_CONFIG['municipio_default']
        
        # Información de la muestra - específica por espécimen
        row_data["N. muestra"] = specimen['muestra']
        row_data["CUPS"] = extracted_data.get('cups_code', '')
        row_data["Tipo de examen (4, 12, Metodo de obtención de la muestra, factor de certeza para el diagnóstico) "] = extracted_data.get('tipo_informe', '')
        row_data["Procedimiento (11. Tipo de estudio para el diagnóstico)"] = extracted_data.get('procedimiento', '')
        row_data["Organo (1. Muestra enviada a patología)"] = (
            extracted_data.get('organo_final') or specimen['organo']
        )
        
        # Información financiera
        row_data["Tarifa"] = HUV_CONFIG['tarifa_default']
        row_data["Valor"] = HUV_CONFIG['valor_default']
        row_data["Copago"] = ''
        row_data["Descuento"] = ''
        
        # Fechas
        row_data["Fecha de ingreso (2. Fecha de la muestra)"] = convert_date_format(extracted_data.get('fecha_ingreso',''))
        row_data["Fecha finalizacion (3. Fecha del informe)"] = convert_date_format(extracted_data.get('fecha_informe',''))
        resp_name = extracted_data.get('responsable_analisis', '')
        row_data["Usuario finalizacion"] = ' '.join(resp_name.split()[:2]) if resp_name else ''
        row_data["Usuario asignacion micro"] = ''
        row_data["Fecha asignacion micro"] = ''
        
        # Información clínica
        row_data["Malignidad"] = extracted_data.get('malignidad', 'AUSENTE')
        row_data["Condicion"] = ''
        row_data["Descripcion macroscopica"] = extracted_data.get('descripcion_macroscopica', '')
        row_data["Descripcion microscopica (8,9, 10,12,. Invasión linfovascular y perineural, indice mitótico/Ki67, Inmunohistoquímica, tamaño tumoral)"] = extracted_data.get('descripcion_microscopica', '')
        row_data["Descripcion Diagnostico (5,6,7 Tipo histológico, subtipo histológico, margenes tumorales)"] = extracted_data.get('diagnostico', '')
        row_data["Diagnostico Principal"] = extracted_data.get('diagnostico', '')
        row_data["Comentario"] = extracted_data.get('comentarios', '')
        row_data["Informe adicional"] = ''
        row_data["Congelaciones /Otros estudios"] = ''
        row_data["Liquidos (5 Tipo histologico)"] = ''
        row_data["Citometria de flujo (5 Tipo histologico)"] = ''
        row_data["Hora Desc. macro"] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        row_data["Responsable macro"] = ' '.join(resp_name.split()[:2]) if resp_name else ''

        
        rows.append(row_data)
    
    return rows

# ─────────────────────── PROCESAMIENTO DE PDF ─────────────────────────
def pdf_to_text_enhanced(pdf_path: str) -> str:
    """Convierte PDF a texto con OCR optimizado"""
    try:
        full_text = ""
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(400/72, 400/72))  # 400 DPI
            img_bytes = pix.tobytes("ppm")
            img = Image.open(io.BytesIO(img_bytes))
            
            # Preprocesamiento
            if img.mode != "L":
                img = img.convert("L")
            
            if img.width < 2000:
                scale = 2000 / img.width
                new_size = (int(img.width * scale), int(img.height * scale))
                img = img.resize(new_size, Image.LANCZOS)
            
            # OCR optimizado para documentos médicos
            page_text = pytesseract.image_to_string(
                img, 
                lang="spa",
                config = '--psm 6 -c preserve_interword_spaces=1 -c tessedit_do_invert=0'
            )
            
            full_text += f"\n--- PÁGINA {page_num + 1} ---\n" + page_text
        
        doc.close()
        return full_text
        
    except Exception as e:
        raise Exception(f"Error procesando PDF {pdf_path}: {str(e)}")

# ─────────────────────── INTERFAZ GRÁFICA ─────────────────────────
class HUVOCRSystem:
    def __init__(self, root):
        self.root = root
        root.title("Sistema OCR - Hospital Universitario del Valle")
        root.geometry("1100x800")
        root.configure(bg="#f8f9fa")
        
        self.files = []
        self.output_dir = ""
        
        self._setup_gui()
    
    def _setup_gui(self):
        # Título y logo
        title_frame = tk.Frame(self.root, bg="#f8f9fa")
        title_frame.pack(pady=15, fill="x")
        
        title_label = tk.Label(title_frame, text="SISTEMA OCR - HOSPITAL UNIVERSITARIO DEL VALLE",
                               font=("Arial", 16, "bold"), bg="#f8f9fa", fg="#2c3e50")
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Extracción automatizada de informes de patología",
                                  font=("Arial", 10), bg="#f8f9fa", fg="#7f8c8d")
        subtitle_label.pack()
        
        # Botones superiores
        button_frame = tk.Frame(self.root, bg="#f8f9fa")
        button_frame.pack(pady=10, fill="x", padx=20)
        
        tk.Button(button_frame, text="📄 Añadir PDFs", command=self.add_files,
                  bg="#3498db", fg="white", padx=20, pady=10, font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="📁 Carpeta PDFs", command=self.add_folder,
                  bg="#2ecc71", fg="white", padx=20, pady=10, font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="🗑️ Limpiar", command=self.clear_files,
                  bg="#e74c3c", fg="white", padx=20, pady=10, font=("Arial", 10, "bold")).pack(side="right", padx=5)
        
        # Lista de archivos
        list_frame = tk.Frame(self.root, bg="#f8f9fa")
        list_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        list_label = tk.Label(list_frame, text="Archivos seleccionados:",
                              font=("Arial", 12, "bold"), bg="#f8f9fa")
        list_label.pack(anchor="w", pady=(0, 5))
        
        # Lista con scrollbar
        list_container = tk.Frame(list_frame)
        list_container.pack(fill="both", expand=True)
        
        self.file_listbox = tk.Listbox(list_container, font=("Consolas", 10), 
                                       bg="white", selectmode=tk.EXTENDED, height=12)
        scrollbar = tk.Scrollbar(list_container, orient="vertical")
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.file_listbox.yview)
        
        self.file_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Carpeta de salida
        output_frame = tk.Frame(self.root, bg="#f8f9fa")
        output_frame.pack(pady=15, fill="x", padx=20)
        
        tk.Button(output_frame, text="📂 Carpeta de Salida", command=self.select_output_dir,
                  bg="#f39c12", fg="white", padx=15, pady=8, font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        self.output_label = tk.Label(output_frame, text="No seleccionada", 
                                     bg="#f8f9fa", font=("Arial", 10))
        self.output_label.pack(side="left", padx=15)
        
        # Progreso y procesamiento
        process_frame = tk.Frame(self.root, bg="#f8f9fa")
        process_frame.pack(pady=15, fill="x", padx=20)
        
        self.progress_bar = ttk.Progressbar(process_frame, length=500, mode="determinate")
        self.progress_bar.pack(side="left", padx=10, expand=True, fill="x")
        
        tk.Button(process_frame, text="🚀 PROCESAR INFORMES", command=self.start_processing,
                  bg="#9b59b6", fg="white", padx=25, pady=12, font=("Arial", 12, "bold")).pack(side="right", padx=10)
        
        # Log de actividades
        log_frame = tk.Frame(self.root, bg="#f8f9fa")
        log_frame.pack(fill="both", expand=True, padx=20, pady=(5, 20))
        
        log_label = tk.Label(log_frame, text="Registro de procesamiento:",
                             font=("Arial", 12, "bold"), bg="#f8f9fa")
        log_label.pack(anchor="w", pady=(0, 5))
        
        log_container = tk.Frame(log_frame)
        log_container.pack(fill="both", expand=True)
        
        self.log_text = tk.Text(log_container, height=10, bg="#2c3e50", fg="#ecf0f1",
                                font=("Consolas", 9), wrap="word")
        log_scrollbar = tk.Scrollbar(log_container, orient="vertical")
        self.log_text.config(yscrollcommand=log_scrollbar.set)
        log_scrollbar.config(command=self.log_text.yview)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scrollbar.pack(side="right", fill="y")
    
    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Seleccionar informes PDF",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")]
        )
        
        added = 0
        for file_path in files:
            if file_path not in self.files:
                self.files.append(file_path)
                filename = Path(file_path).name
                self.file_listbox.insert(tk.END, f"📄 {filename}")
                added += 1
        
        self._log(f"➕ {added} archivos añadidos. Total: {len(self.files)}")
    
    def add_folder(self):
        folder = filedialog.askdirectory(title="Seleccionar carpeta con PDFs")
        if not folder:
            return
        
        pdf_files = list(Path(folder).glob("*.pdf"))
        added = 0
        
        for pdf_path in pdf_files:
            file_str = str(pdf_path)
            if file_str not in self.files:
                self.files.append(file_str)
                self.file_listbox.insert(tk.END, f"📄 {pdf_path.name}")
                added += 1
        
        self._log(f"📁 {added} archivos añadidos desde carpeta. Total: {len(self.files)}")
    
    def clear_files(self):
        self.files.clear()
        self.file_listbox.delete(0, tk.END)
        self._log("🗑️ Lista de archivos limpiada")
    
    def select_output_dir(self):
        directory = filedialog.askdirectory(title="Seleccionar carpeta de salida")
        if directory:
            self.output_dir = directory
            self.output_label.config(text=f"📁 {directory}")
            self._log(f"📂 Carpeta de salida: {directory}")
    
    def _log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_processing(self):
        if not self.files:
            messagebox.showwarning("Sin archivos", "Seleccione al menos un archivo PDF para procesar.")
            return
        
        if not self.output_dir:
            messagebox.showwarning("Sin carpeta de salida", "Seleccione una carpeta para guardar los resultados.")
            return
        
        # Procesar en hilo separado
        threading.Thread(target=self._process_files, daemon=True).start()
    
    def _process_files(self):
        total_files = len(self.files)
        self.progress_bar["maximum"] = total_files
        
        all_rows = []
        processed_count = 0
        error_count = 0
        
        self._log(f"🚀 Iniciando procesamiento de {total_files} archivos")
        self._log("=" * 60)
        
        for idx, pdf_path in enumerate(self.files, 1):
            filename = Path(pdf_path).name
            self._log(f"📄 [{idx}/{total_files}] Procesando: {filename}")
            
            try:
                # 1. Extraer texto del PDF
                self._log("   🔍 Extrayendo texto con OCR...")
                pdf_text = pdf_to_text_enhanced(pdf_path)
                
                if not pdf_text.strip():
                    self._log("   ⚠️  Advertencia: No se extrajo texto del PDF")
                    continue
                
                # 2. Extraer datos estructurados
                self._log("   📊 Extrayendo datos estructurados...")
                extracted_data = extract_huv_data(pdf_text)
                
                # 3. Mapear a formato Excel
                self._log("   📋 Mapeando a formato Excel...")
                excel_rows = map_to_excel_format(extracted_data, filename)
                
                # 4. Agregar filas
                all_rows.extend(excel_rows)
                processed_count += 1
                
                # Log de resultados
                tipo_informe = extracted_data.get('tipo_informe', 'DESCONOCIDO')
                num_specimens = len(extracted_data.get('specimens', []))
                self._log(f"   ✅ Completado - Tipo: {tipo_informe} - Especímenes: {num_specimens}")
                
            except Exception as e:
                error_count += 1
                self._log(f"   ❌ Error: {str(e)}")
            
            # Actualizar progreso
            self.progress_bar["value"] = idx
            self.root.update_idletasks()
        
        # Generar archivo Excel
        if all_rows:
            self._log("=" * 60)
            self._log("💾 Generando archivo Excel...")
            
            try:
                # Crear DataFrame
                df = pd.DataFrame(all_rows)
                
                # Generar nombre de archivo
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"Informes_HUV_{timestamp}.xlsx"
                output_path = Path(self.output_dir) / output_filename
                
                # Guardar Excel
                df.to_excel(output_path, index=False, engine="openpyxl")
                
                # Estadísticas finales
                self._log("=" * 60)
                self._log("🎉 PROCESAMIENTO COMPLETADO")
                self._log(f"✅ Archivos procesados exitosamente: {processed_count}")
                self._log(f"❌ Archivos con errores: {error_count}")
                self._log(f"📊 Total de registros generados: {len(all_rows)}")
                self._log(f"📁 Archivo guardado: {output_filename}")
                self._log("=" * 60)
                
                # Mostrar mensaje de éxito
                messagebox.showinfo(
                    "Procesamiento Completado",
                    f"✅ Procesamiento exitoso!\n\n"
                    f"📊 {processed_count} archivos procesados\n"
                    f"📄 {len(all_rows)} registros generados\n"
                    f"📁 Archivo: {output_filename}\n\n"
                    f"El archivo Excel ha sido guardado en:\n{output_path}"
                )
                
            except Exception as e:
                self._log(f"❌ Error generando Excel: {str(e)}")
                messagebox.showerror("Error", f"Error generando archivo Excel:\n{str(e)}")
        
        else:
            self._log("⚠️ No se procesó ningún archivo exitosamente")
            messagebox.showwarning("Sin resultados", "No se pudo extraer información de ningún archivo")

# ─────────────────────── EJECUCIÓN PRINCIPAL ─────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = HUVOCRSystem(root)
    root.mainloop()