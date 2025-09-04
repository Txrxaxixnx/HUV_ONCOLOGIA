#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utilidades y funciones de extracción de datos para el sistema OCR HUV."""

import re
from datetime import datetime, date

# ─────────────────────── CONFIGURACIÓN HOSPITALARIA ───────────────────────
HUV_CONFIG = {
    'hospital_name': 'HOSPITAL UNIVERSITARIO DEL VALLE',
    'hospital_code': 'HUV',
    'sede_default': 'PRINCIPAL',
    'departamento_default': 'VALLE DEL CAUCA',
    'municipio_default': 'CALI',
    'tipo_documento_default': 'CC',
    'tarifa_default': 'GENERAL',
    'valor_default': 0.0,
}

# ─────────────────────── CÓDIGOS Y ESPECIALIDADES ─────────────────────────
CUPS_CODES = {
    'AUTOPSIA': '898301',
    'INMUNOHISTOQUIMICA': '898807',
    'BIOPSIA': '898201',
    'REVISION': '898806',
    'CITOLOGIA': '898241',
    'CONGELACION': '898242',
}

PROCEDIMIENTOS = {
    '898301': '898301 Autopsia completa',
    '898807': '898807 Estudio anatomopatologico de marcacion inmunohistoquimica basica (especifico)',
    '898201': '898201 Estudio de coloracion basica en especimen de reconocimiento',
    '898806': '898806 Verificacion integral con preparacion de material de rutina',
}

ESPECIALIDADES_SERVICIOS = {
    'UCI': 'MEDICO INTENSIVISTA',
    'GINECOLOGIA': 'GINECOLOGIA Y OBSTETRICIA',
    'GINECOLOGIA ONCOLOGICA': 'GINECOLOGIA ONCOLOGICA',
    'ALTO RIESGO OBSTETRICO': 'GINECOLOGIA ONCOLOGICA',
    'MEDICINA': 'MEDICINA GENERAL',
    'URGENCIAS': 'MEDICINA DE URGENCIAS',
    'NEONATOLOGIA': 'NEONATOLOGIA',
    'PEDIATRIA': 'PEDIATRA',
}

# ─────────────────────── PATRONES REGEX ─────────────────────────
PATTERNS_HUV = {
    'nombre_completo': r'Nombre\s*:\s*([^\n]+?)\s*N\.\s*peticion',
    'numero_peticion': r'N\.\s*peticion\s*:\s*([A-Z0-9\-]+)',
    'identificacion_completa': r'N\.Identificación\s*:\s*([A-Z]{1,3}\.?\s*[0-9\.]+)',
    'identificacion_numero': r'N\.Identificación\s*:\s*[A-Z\.]{1,3}\s*([0-9\.]+)',
    'tipo_documento': r'N\.Identificación\s*:\s*([A-Z]{1,3})\.?',
    'genero': r'Genero\s*:\s*([A-Z]+)',
    'edad': r'Edad\s*:\s*(\d+)\s*años',
    'eps': r'EPS\s*:\s*([^\n]+)',
    'medico_tratante': r'Médico tratante\s*:\s*([^\n]+)',
    'servicio': r'Servicio\s*:\s*([^\n]+)',
    'fecha_ingreso': r'Fecha Ingreso\s*:\s*(\d{2}/\d{2}/\d{4})',
    'fecha_informe': r'Fecha Informe\s*:\s*(\d{2}/\d{2}/\d{4})',
    'fecha_autopsia': r'Fecha y hora de la autopsia:\s*(\d{2}/\d{2}/\d{4})',
    'organo': r'Organo\s*:\s*([A-ZÁÉÍÓÚÑ\s\+\(\)]+)',
    'fecha_toma': r'Fecha toma\s*:\s*(\d{4}-\d{2}-\d{2})',
    'responsable_analisis': r'([A-ZÁÉÍÓÚÑ\s]+)\s*\n\s*Responsable del análisis',
    'usuario_finalizacion': r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}),\s*([A-ZÁÉÍÓÚÑ\s]+)',
    'descripcion_macroscopica': r'DESCRIPCIÓN MACROSCÓPICA\s*(.+?)(?=DESCRIPCIÓN MICROSCÓPICA|PROTOCOLO MICROSCÓPICO|DIAGN[OÓ]STICO|$)',
    'descripcion_microscopica': r'(?:DESCRIPCIÓN MICROSCÓPICA|PROTOCOLO MICROSCÓPICO)\s*(.+?)(?=DIAGN[OÓ]STICO|COMENTARIOS|$)',
    'diagnostico': r'DIAGN[OÓ]STICO\s*(.+?)(?=COMENTARIOS|Todos los análisis|Responsable|$)',
    'comentarios': r'COMENTARIOS\s*(.+?)(?=Todos los análisis|Responsable|$)',
    'identificador_unico': r'Identificador Unico[^:]*:\s*(\d+)',
    'numero_autorizacion': r'N\.\s*Autorizacion[^:]*:\s*([A-Z0-9]+)',
}

# ─────────────────────── PALABRAS CLAVE MALIGNIDAD ───────────────────────
MALIGNIDAD_KEYWORDS = [
    'CARCINOMA', 'CANCER', 'MALIGNO', 'MALIGNIDAD', 'METASTASIS', 'METASTÁSICO',
    'NEOPLASIA MALIGNA', 'TUMOR MALIGNO', 'ADENOCARCINOMA', 'LINFOMA',
    'SARCOMA', 'MELANOMA', 'LEUCEMIA', 'HODGKIN', 'HODKING',
]


# ─────────────────────── FUNCIONES DE UTILIDAD ─────────────────────────
def detect_report_type(text: str) -> str:
    """Detecta el tipo de informe basado en patrones del HUV"""
    m = re.search(r'N\.\s*peticion\s*:\s*([A-Z0-9\-]+)', text, re.IGNORECASE)
    if m:
        numero = m.group(1)
        if re.match(r'A\d{6}', numero):
            return 'AUTOPSIA'
        if re.match(r'IHQ\d{6}', numero):
            return 'INMUNOHISTOQUIMICA'
        if re.match(r'M\d{7}', numero):
            return 'BIOPSIA'
        if re.match(r'R\d{6}', numero):
            return 'REVISION'
    text_upper = text.upper()
    if 'AUTOPSIA' in text_upper:
        return 'AUTOPSIA'
    if 'INMUNOHISTOQUIMICA' in text_upper:
        return 'INMUNOHISTOQUIMICA'
    if 'HISTOLOGIA' in text_upper or 'BIOPSIA' in text_upper:
        return 'BIOPSIA'
    if 'REVISION' in text_upper:
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
    except Exception:
        return ''


def convert_date_format(date_str: str) -> str:
    """Normaliza fechas a DD/MM/YYYY"""
    try:
        if not date_str:
            return ''
        s = str(date_str).strip()
        m = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', s)
        if m:
            y, mo, d = m.groups()
            return f"{d}/{mo}/{y}"
        m = re.match(r'^(\d{1,2})-(\d{1,2})-(\d{4})$', s)
        if m:
            d, mo, y = m.groups()
            return f"{int(d):02d}/{int(mo):02d}/{y}"
        m = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{4})$', s)
        if m:
            d, mo, y = m.groups()
            return f"{int(d):02d}/{int(mo):02d}/{y}"
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
    for key, specialty in ESPECIALIDADES_SERVICIOS.items():
        if key in servicio_upper:
            return specialty
    if 'UCI' in servicio_upper:
        return 'MEDICO INTENSIVISTA'
    if 'GINECO' in servicio_upper:
        return 'GINECOLOGIA Y OBSTETRICIA'
    if 'OBSTETRICO' in servicio_upper:
        return 'GINECOLOGIA ONCOLOGICA'
    if 'URGENCIA' in servicio_upper:
        return 'MEDICINA DE URGENCIAS'
    if 'NEONAT' in servicio_upper:
        return 'NEONATOLOGIA'
    if 'PEDIATR' in servicio_upper:
        return 'PEDIATRA'
    return 'MEDICINA GENERAL'


def determine_hospitalization(servicio: str, tipo_informe: str) -> str:
    """Determina si el paciente está hospitalizado"""
    servicio_upper = servicio.upper()
    if any(keyword in servicio_upper for keyword in ['UCI', 'URGENCIAS', 'ADMISION', 'QUIROFANO']):
        return 'SI'
    if tipo_informe in ['AUTOPSIA', 'BIOPSIA']:
        return 'SI'
    if tipo_informe in ['INMUNOHISTOQUIMICA', 'REVISION']:
        return 'NO'
    return 'NO'


def extract_specimens(organo_text: str, numero_peticion: str) -> list:
    """Extrae información de especímenes múltiples"""
    found_specimens = []
    matches = list(re.finditer(r'(?m)^[ \t]*([A-J])\.\s*[\"\']?([^\"\'\:\n]+?)[\"\' ]?\s*:', organo_text))
    if len(matches) > 1 or (len(matches) == 1 and matches[0].group(1).upper() != 'A'):
        for match in matches:
            suffix = match.group(1).upper()
            organo = match.group(2).strip()
            found_specimens.append({'muestra': f"{numero_peticion}-{suffix}", 'organo': organo})
    if not found_specimens:
        organo_limpio = re.sub(r'^[A-Z]\.\s*', '', organo_text.strip()).strip()
        found_specimens.append({'muestra': numero_peticion, 'organo': organo_limpio if organo_limpio else "No especificado"})
    return found_specimens


def extract_huv_data(text: str) -> dict:
    """Extracción de datos según la lógica del HUV"""
    data = {}
    tipo_informe = detect_report_type(text)
    data['tipo_informe'] = tipo_informe
    for key, pattern in PATTERNS_HUV.items():
        try:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                value = match.group(1).strip()
                value = re.sub(r'\s+', ' ', value)
                data[key] = value
            else:
                data[key] = ''
        except Exception:
            data[key] = ''
    if data.get('nombre_completo'):
        names = split_full_name(data['nombre_completo'])
        data.update(names)
    if data.get('identificacion_numero'):
        data['identificacion_numero'] = re.sub(r'[^\d]', '', data['identificacion_numero'])
    if data.get('edad'):
        try:
            edad = int(data['edad'])
            data['fecha_nacimiento'] = calculate_birth_date(edad)
        except Exception:
            data['fecha_nacimiento'] = ''
    for date_field in ['fecha_ingreso', 'fecha_informe']:
        if data.get(date_field):
            data[f"{date_field}_converted"] = convert_date_format(data[date_field])
    if tipo_informe == 'AUTOPSIA' and data.get('fecha_autopsia'):
        data['fecha_ordenamiento'] = data['fecha_autopsia']
    else:
        data['fecha_ordenamiento'] = data.get('fecha_ingreso', '')
    servicio = data.get('servicio', '')
    data['especialidad_deducida'] = deduce_specialty(servicio, tipo_informe)
    data['hospitalizado'] = determine_hospitalization(servicio, tipo_informe)
    diagnostico = data.get('diagnostico', '')
    descripcion_micro = data.get('descripcion_microscopica', '')
    data['malignidad'] = detect_malignancy(diagnostico, descripcion_micro)
    if tipo_informe in CUPS_CODES:
        data['cups_code'] = CUPS_CODES[tipo_informe]
        data['procedimiento'] = PROCEDIMIENTOS.get(CUPS_CODES[tipo_informe], '')
    if tipo_informe == 'AUTOPSIA':
        data['organo_final'] = 'CUERPO HUMANO COMPLETO'
        data['hospitalizado'] = 'SI'
    elif tipo_informe == 'INMUNOHISTOQUIMICA':
        data['hospitalizado'] = 'NO'
        data['n_autorizacion'] = 'COEX'
        data['identificador_unico'] = '0'
    if tipo_informe == 'AUTOPSIA':
        num = data.get('numero_peticion', '')
        data['specimens'] = [{'muestra': num, 'organo': 'CUERPO HUMANO COMPLETO'}]
    else:
        organo_text = data.get('organo', '') + ' ' + data.get('descripcion_macroscopica', '')
        data['specimens'] = extract_specimens(organo_text, data.get('numero_peticion', ''))
    return data


def map_to_excel_format(extracted_data: dict, filename: str) -> list:
    """Mapea datos extraídos al formato Excel de 55 columnas del HUV"""
    excel_columns = [
        "N. peticion (0. Numero de biopsia)", "Hospitalizado", "Sede", "EPS", "Servicio",
        "Médico tratante", "Especialidad", "Ubicación", "N. Autorizacion", "Identificador Unico",
        "Datos Clinicos", "Fecha ordenamiento", "Tipo de documento", "N. de identificación",
        "Primer nombre", "Segundo nombre", "Primer apellido", "Segundo apellido",
        "Fecha de nacimiento", "Edad", "Genero", "Número celular",
        "Direccion de correo electronico", "Direccion de correo electronico 2",
        "Contacto de emergencia", "Departamento", "Teléfono del contacto", "Municipio",
        "N. muestra", "CUPS", "Tipo de examen (4, 12, Metodo de obtención de la muestra, factor de certeza para el diagnóstico)",
        "Procedimiento (11. Tipo de estudio para el diagnóstico)", "Organo (1. Muestra enviada a patología)",
        "Tarifa", "Valor", "Copago", "Descuento", "Fecha de ingreso (2. Fecha de la muestra)",
        "Fecha finalizacion (3. Fecha del informe)", "Usuario finalizacion", "Usuario asignacion micro",
        "Fecha asignacion micro", "Malignidad", "Condicion", "Descripcion macroscopica",
        "Descripcion microscopica (8,9, 10,12,. Invasión linfovascular y perineural, indice mitótico/Ki67, Inmunohistoquímica, tamaño tumoral)",
        "Descripcion Diagnostico (5,6,7 Tipo histológico, subtipo histológico, margenes tumorales)",
        "Diagnostico Principal", "Comentario", "Informe adicional", "Congelaciones /Otros estudios",
        "Liquidos (5 Tipo histologico)", "Citometria de flujo (5 Tipo histologico)",
        "Hora Desc. macro", "Responsable macro",
    ]
    rows = []
    specimens = extracted_data.get('specimens', []) or [{}]
    for specimen in specimens:
        row_data = {col: '' for col in excel_columns}
        row_data["N. peticion (0. Numero de biopsia)"] = extracted_data.get('numero_peticion', '')
        row_data["Hospitalizado"] = extracted_data.get('hospitalizado', 'NO')
        row_data["Sede"] = HUV_CONFIG['sede_default']
        row_data["EPS"] = extracted_data.get('eps', '')
        row_data["Servicio"] = extracted_data.get('servicio', '')
        row_data["Médico tratante"] = extracted_data.get('medico_tratante', '')
        row_data["Especialidad"] = extracted_data.get('especialidad_deducida', '')
        row_data["Ubicación"] = ''
        row_data["N. Autorizacion"] = extracted_data.get('n_autorizacion', '')
        row_data["Identificador Unico"] = extracted_data.get('identificador_unico', '')
        row_data["Datos Clinicos"] = ''
        row_data["Fecha ordenamiento"] = convert_date_format(extracted_data.get('fecha_ordenamiento', ''))
        row_data["Tipo de documento"] = extracted_data.get('tipo_documento', HUV_CONFIG['tipo_documento_default'])
        row_data["N. de identificación"] = extracted_data.get('identificacion_numero', '')
        row_data["Primer nombre"] = extracted_data.get('primer_nombre', '')
        row_data["Segundo nombre"] = extracted_data.get('segundo_nombre', '')
        row_data["Primer apellido"] = extracted_data.get('primer_apellido', '')
        row_data["Segundo apellido"] = extracted_data.get('segundo_apellido', '')
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
        row_data["N. muestra"] = specimen.get('muestra', '')
        row_data["CUPS"] = extracted_data.get('cups_code', '')
        row_data["Tipo de examen (4, 12, Metodo de obtención de la muestra, factor de certeza para el diagnóstico)"] = extracted_data.get('tipo_informe', '')
        row_data["Procedimiento (11. Tipo de estudio para el diagnóstico)"] = extracted_data.get('procedimiento', '')
        row_data["Organo (1. Muestra enviada a patología)"] = specimen.get('organo', '')
        row_data["Tarifa"] = HUV_CONFIG['tarifa_default']
        row_data["Valor"] = HUV_CONFIG['valor_default']
        row_data["Copago"] = ''
        row_data["Descuento"] = ''
        row_data["Fecha de ingreso (2. Fecha de la muestra)"] = convert_date_format(extracted_data.get('fecha_ingreso', ''))
        row_data["Fecha finalizacion (3. Fecha del informe)"] = convert_date_format(extracted_data.get('fecha_informe', ''))
        resp_name = extracted_data.get('responsable_analisis', '')
        row_data["Usuario finalizacion"] = ' '.join(resp_name.split()[:2]) if resp_name else ''
        row_data["Usuario asignacion micro"] = ''
        row_data["Fecha asignacion micro"] = ''
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
