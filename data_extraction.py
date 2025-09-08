# data_extraction.py:
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utilidades y funciones de extracción de datos para el sistema OCR HUV."""

import re
import unicodedata
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import configparser
from pathlib import Path
from huv_constants import (
    HUV_CONFIG,
    CUPS_CODES,
    PROCEDIMIENTOS,
    ESPECIALIDADES_SERVICIOS,
    PATTERNS_HUV,
    MALIGNIDAD_KEYWORDS,
)

# Configuración para habilitar enrutamiento a procesadores especializados
_config = configparser.ConfigParser(interpolation=None)
_config.read(Path(__file__).resolve().parent / 'config.ini', encoding='utf-8')
ENABLE_PROCESSORS = _config.getboolean('PROCESSORS', 'ENABLE_PROCESSORS', fallback=True)

# Importación opcional de procesadores especializados
try:
    import procesador_ihq as _proc_ihq
except Exception:
    _proc_ihq = None

try:
    import procesador_biopsia as _proc_biopsia
except Exception:
    _proc_biopsia = None

try:
    import procesador_revision as _proc_revision
except Exception:
    _proc_revision = None

# ─────────────────────── FUNCIONES DE UTILIDAD ─────────────────────────

def detect_report_type(text: str) -> str:
    """Detecta el tipo de informe basado en patrones del HUV"""
    m = re.search(r'N\.\s*peticion\s*:\s*([A-Z0-9\-]+)', text, re.IGNORECASE)
    if m:
        numero = m.group(1).upper()
        if re.match(r'A\d{6}', numero):
            return 'AUTOPSIA'
        elif re.match(r'IHQ\d{6}', numero):
            return 'INMUNOHISTOQUIMICA'
        elif re.match(r'M\d{7}', numero):
            return 'BIOPSIA'
        elif re.match(r'R\d{6}', numero):
            return 'REVISION'
            
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

def calculate_birth_date(edad_str: str, fecha_referencia_str: str = None) -> str:
    """
    Calcula la fecha de nacimiento de forma precisa a partir de un texto de edad
    (ej. "33 años 10 meses 27 dias") y una fecha de referencia.
    """
    try:
        years_match = re.search(r'(\d+)\s*a[ñn]os', edad_str, re.IGNORECASE)
        months_match = re.search(r'(\d+)\s*meses', edad_str, re.IGNORECASE)
        days_match = re.search(r'(\d+)\s*d[ií]as', edad_str, re.IGNORECASE)
        
        years = int(years_match.group(1)) if years_match else 0
        months = int(months_match.group(1)) if months_match else 0
        days = int(days_match.group(1)) if days_match else 0

        if not years and not months and not days:
            return ''

        ref_date = date.today()
        if fecha_referencia_str:
            for fmt in ('%d/%m/%Y', '%Y-%m-%d'):
                try:
                    ref_date = datetime.strptime(fecha_referencia_str, fmt).date()
                    break
                except ValueError:
                    continue
        
        birth_date = ref_date - relativedelta(years=years, months=months, days=days)
        return birth_date.strftime('%d/%m/%Y')
        
    except Exception:
        return ''

def convert_date_format(date_str: str) -> str:
    """Normaliza a DD/MM/YYYY desde varios formatos"""
    if not date_str:
        return ''
    try:
        dt = datetime.strptime(date_str.strip(), '%d/%m/%Y')
        return dt.strftime('%d/%m/%Y')
    except ValueError:
        try:
            dt = datetime.strptime(date_str.strip(), '%Y-%m-%d')
            return dt.strftime('%d/%m/%Y')
        except ValueError:
            return date_str

def _normalize_text(u: str) -> str:
    """Normaliza texto para búsquedas (quita tildes, mayúsculas)"""
    return unicodedata.normalize('NFKD', u or '').encode('ASCII', 'ignore').decode().upper()

def detect_malignancy(*texts: str) -> str:
    """Detecta malignidad basada en palabras clave en múltiples textos."""
    text_to_check = " ".join(_normalize_text(t) for t in texts if t)
    for keyword in MALIGNIDAD_KEYWORDS:
        if re.search(r'\b' + keyword + r'\b', text_to_check):
            return 'PRESENTE'
    return 'AUSENTE'

def deduce_specialty(servicio: str, tipo_informe: str = '') -> str:
    """Deduce especialidad basada en servicio y tipo de informe"""
    servicio_upper = servicio.upper()
    for key, specialty in ESPECIALIDADES_SERVICIOS.items():
        if key in servicio_upper:
            return specialty
    return 'MEDICINA GENERAL'

def determine_hospitalization(servicio: str, tipo_informe: str) -> str:
    """Determina si el paciente está hospitalizado"""
    servicio_upper = servicio.upper()
    if any(keyword in servicio_upper for keyword in ['UCI', 'URGENCIAS', 'ADMISION', 'QUIROFANO']):
        return 'SI'
    if tipo_informe in ['AUTOPSIA', 'BIOPSIA']:
        return 'SI'
    elif tipo_informe in ['INMUNOHISTOQUIMICA', 'REVISION']:
        return 'NO'
    return 'NO'

def extract_specimens(organo_text: str, numero_peticion: str) -> list:
    """Extrae información de especímenes múltiples de forma robusta."""
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

# ─────────────────────── EXTRACCIÓN PRINCIPAL ─────────────────────────
def extract_huv_data(text: str) -> dict:
    """Extracción de datos según la lógica exacta del HUV"""
    data = {}
    tipo_informe = detect_report_type(text)
    data['tipo_informe'] = tipo_informe

    for key, pattern in PATTERNS_HUV.items():
        try:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            data[key] = re.sub(r'\s+', ' ', match.group(1).strip()) if match else ''
        except Exception:
            data[key] = ''

    if data.get('nombre_completo'):
        data.update(split_full_name(data['nombre_completo']))
        
    if data.get('identificacion_numero'):
        data['identificacion_numero'] = re.sub(r'[^\d]', '', data['identificacion_numero'])
        
    if data.get('edad'):
        edad_texto_completo = data['edad']
        anos_match = re.search(r'(\d+)', edad_texto_completo)
        data['edad'] = anos_match.group(1) if anos_match else ''
        ref_date_str = data.get('fecha_ingreso') or data.get('fecha_informe')
        data['fecha_nacimiento'] = calculate_birth_date(edad_texto_completo, ref_date_str)

    if tipo_informe == 'AUTOPSIA' and data.get('fecha_autopsia'):
        data['fecha_ordenamiento'] = data['fecha_autopsia']
    else:
        data['fecha_ordenamiento'] = data.get('fecha_ingreso', '')

    servicio = data.get('servicio', '')
    data['especialidad_deducida'] = deduce_specialty(servicio, tipo_informe)
    data['hospitalizado'] = determine_hospitalization(servicio, tipo_informe)

    data['malignidad'] = detect_malignancy(
        data.get('diagnostico', ''),
        data.get('descripcion_microscopica', ''),
        data.get('comentarios', '')
    )
    
    if data.get('certificado_defuncion'):
        data['identificador_unico'] = data['certificado_defuncion']
    
    if tipo_informe in CUPS_CODES:
        data['cups_code'] = CUPS_CODES[tipo_informe]
        data['procedimiento'] = PROCEDIMIENTOS.get(CUPS_CODES[tipo_informe], '')

    if tipo_informe == 'AUTOPSIA':
        data['organo_final'] = 'CUERPO HUMANO COMPLETO'
        data['hospitalizado'] = 'SI'
        num = data.get('numero_peticion', '')
        data['specimens'] = [{'muestra': num, 'organo': 'CUERPO HUMANO COMPLETO'}]
    elif tipo_informe == 'INMUNOHISTOQUIMICA':
        data['hospitalizado'] = 'NO'
        data['n_autorizacion'] = 'COEX'
        data['identificador_unico'] = '0'
        organo_text = data.get('organo', '') + ' ' + data.get('descripcion_macroscopica', '')
        data['specimens'] = extract_specimens(organo_text, data.get('numero_peticion', ''))
    else:
        organo_text = data.get('organo', '') + ' ' + data.get('descripcion_macroscopica', '')
        data['specimens'] = extract_specimens(organo_text, data.get('numero_peticion', ''))

    if 'numero_autorizacion' in data and not data.get('n_autorizacion'):
        data['n_autorizacion'] = data['numero_autorizacion']
            
    return data

# ─────────────────────── MAPEO A EXCEL (VERSIÓN FINAL) ─────────────────────────
def map_to_excel_format(extracted_data: dict, filename: str) -> list:
    """Mapea datos extraídos al formato Excel de 55 columnas del HUV"""
    EXCEL_COLUMNS = [
        "N. peticion (0. Numero de biopsia)", "Hospitalizado", "Sede", "EPS", "Servicio",
        "Médico tratante", "Especialidad", "Ubicación", "N. Autorizacion", "Identificador Unico",
        "Datos Clinicos", "Fecha ordenamiento", "Tipo de documento", "N. de identificación",
        "Primer nombre", "Segundo nombre", "Primer apellido", "Segundo apellido", "Fecha de nacimiento",
        "Edad", "Genero", "Número celular", "Direccion de correo electronico", "Direccion de correo electronico 2",
        "Contacto de emergencia", "Departamento", "Teléfono del contacto", "Municipio", "N. muestra",
        "CUPS", "Tipo de examen (4, 12, Metodo de obtención de la muestra, factor de certeza para el diagnóstico)",
        "Procedimiento (11. Tipo de estudio para el diagnóstico)", "Organo (1. Muestra enviada a patología)",
        "Tarifa", "Valor", "Copago", "Descuento", "Fecha de ingreso (2. Fecha de la muestra)",
        "Fecha finalizacion (3. Fecha del informe)", "Usuario finalizacion", "Usuario asignacion micro",
        "Fecha asignacion micro", "Malignidad", "Condicion", "Descripcion macroscopica",
        "Descripcion microscopica (8,9, 10,12,. Invasión linfovascular y perineural, indice mitótico/Ki67, Inmunohistoquímica, tamaño tumoral)",
        "Descripcion Diagnostico (5,6,7 Tipo histológico, subtipo histológico, margenes tumorales)",
        "Diagnostico Principal", "Comentario", "Informe adicional", "Congelaciones /Otros estudios",
        "Liquidos (5 Tipo histologico)", "Citometria de flujo (5 Tipo histologico)", "Hora Desc. macro",
        "Responsable macro"
    ]

    rows = []
    specimens = extracted_data.get('specimens', []) or [{'muestra': extracted_data.get('numero_peticion', ''), 'organo': extracted_data.get('organo', '')}]

    for specimen in specimens:
        row_data = {col: '' for col in EXCEL_COLUMNS}

        # --- Mapeo de datos ---
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
        row_data["Datos Clinicos"] = 'SI' if len(extracted_data.get('descripcion_macroscopica', '')) > 50 else 'NO'
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
        row_data["Departamento"] = HUV_CONFIG['departamento_default']
        row_data["Municipio"] = HUV_CONFIG['municipio_default']
        row_data["N. muestra"] = specimen.get('muestra', '')
        row_data["CUPS"] = extracted_data.get('cups_code', '')
        row_data["Tipo de examen (4, 12, Metodo de obtención de la muestra, factor de certeza para el diagnóstico)"] = extracted_data.get('tipo_informe', '')
        row_data["Procedimiento (11. Tipo de estudio para el diagnóstico)"] = extracted_data.get('procedimiento', '')
        row_data["Organo (1. Muestra enviada a patología)"] = extracted_data.get('organo_final') or specimen.get('organo', '')
        row_data["Tarifa"] = HUV_CONFIG['tarifa_default']
        row_data["Valor"] = HUV_CONFIG['valor_default']
        row_data["Fecha de ingreso (2. Fecha de la muestra)"] = convert_date_format(extracted_data.get('fecha_ingreso', ''))
        row_data["Fecha finalizacion (3. Fecha del informe)"] = convert_date_format(extracted_data.get('fecha_informe', ''))
        
        resp_name = extracted_data.get('responsable_analisis', '')
        row_data["Usuario finalizacion"] = resp_name
        
        row_data["Malignidad"] = extracted_data.get('malignidad', 'AUSENTE')
        
        # --- SECCIÓN CORREGIDA ---
        row_data["Descripcion macroscopica"] = extracted_data.get('descripcion_macroscopica', '')
        row_data["Descripcion microscopica (8,9, 10,12,. Invasión linfovascular y perineural, indice mitótico/Ki67, Inmunohistoquímica, tamaño tumoral)"] = extracted_data.get('descripcion_microscopica', '')
        row_data["Descripcion Diagnostico (5,6,7 Tipo histológico, subtipo histológico, margenes tumorales)"] = extracted_data.get('diagnostico', '')
        # CORREGIDO: Se deja la columna 'Diagnostico Principal' vacía como se requiere en el ejemplo.
        row_data["Diagnostico Principal"] = ''
        row_data["Comentario"] = extracted_data.get('comentarios', '')
        # --- FIN DE SECCIÓN CORREGIDA ---
        
        row_data["Hora Desc. macro"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row_data["Responsable macro"] = resp_name
        
        rows.append(row_data)

    return rows


def process_text_to_excel_rows(text: str, filename: str) -> list:
    """Devuelve filas mapeadas a Excel usando procesadores si están habilitados.
    Fallback a la ruta base estable si no hay procesador disponible.
    """
    tipo = detect_report_type(text or '')

    if ENABLE_PROCESSORS:
        if tipo == 'INMUNOHISTOQUIMICA' and _proc_ihq is not None:
            try:
                data = _proc_ihq.extract_ihq_data(text)
                return _proc_ihq.map_to_excel_format(data)
            except Exception:
                pass
        if tipo == 'BIOPSIA' and _proc_biopsia is not None:
            try:
                common = _proc_biopsia.extract_biopsy_data(text)
                num = common.get('numero_peticion', '')
                specimens = _proc_biopsia.extract_specimens_data(text, num)
                return _proc_biopsia.map_to_excel_format(common, specimens)
            except Exception:
                pass
        if tipo == 'REVISION' and _proc_revision is not None:
            try:
                data = _proc_revision.extract_revision_data(text)
                return _proc_revision.map_to_excel_format(data)
            except Exception:
                pass

    # Fallback base
    extracted_data = extract_huv_data(text)
    return map_to_excel_format(extracted_data, filename)
