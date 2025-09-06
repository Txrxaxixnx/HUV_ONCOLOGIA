# processors/ihq_processor.py:
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Módulo especializado en la extracción de datos de informes de INMUNOHISTOQUÍMICA."""

import re
# Importa las constantes y utilidades compartidas
from huv_constants import PATTERNS_BASE, CUPS_CODES, PROCEDIMIENTOS
from data_extraction import (
    split_full_name,
    calculate_birth_date,
    deduce_specialty,
    detect_malignancy,
    extract_specimens
)

# Patrones específicos para IHQ
PATTERNS_IHQ = {
    **PATTERNS_BASE, # Hereda todos los patrones básicos
    'fecha_toma': r'Fecha toma\s*:\s*(\d{4}-\d{2}-\d{2})',
    'organo': r'Organo\s*:\s*([^\n]+)',
    # Este es el patrón específico que soluciona el problema de la macroscópica en IHQ
    'descripcion_macroscopica': r'INFORME DE ANATOMÍA PATOLÓGICA([\s\S]+?)(?=DESCRIPCIÓN MICROSCÓPICA)',
    'descripcion_microscopica': r'DESCRIPCIÓN MICROSCÓPICA([\s\S]+?)(?=DIAGNÓSTICO)',
    'diagnostico': r'DIAGNÓSTICO([\s\S]+?)(?=Todos los análisis son avalados|ARMANDO CORTES BUELVAS|$)',
}

def extract_ihq_data(text: str) -> dict:
    """Extrae datos de un informe de INMUNOHISTOQUÍMICA aplicando sus reglas específicas."""
    data = {'tipo_informe': 'INMUNOHISTOQUIMICA'}

    for key, pattern in PATTERNS_IHQ.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        data[key] = re.sub(r'\s+', ' ', match.group(1).strip()) if match else ''

    # --- Limpieza y Enriquecimiento ---
    data.update(split_full_name(data.get('nombre_completo', '')))
    data['identificacion_numero'] = re.sub(r'[^\d]', '', data.get('identificacion_numero', ''))
    
    edad_texto = data.get('edad', '')
    data['edad'] = re.search(r'(\d+)', edad_texto).group(1) if re.search(r'(\d+)', edad_texto) else ''
    data['fecha_nacimiento'] = calculate_birth_date(edad_texto, data.get('fecha_informe'))
    
    data['malignidad'] = detect_malignancy(data.get('diagnostico', ''), data.get('descripcion_microscopica', ''))
    data['especialidad_deducida'] = deduce_specialty(data.get('servicio', ''), 'INMUNOHISTOQUIMICA')

    # --- REGLAS DE NEGOCIO EXCLUSIVAS DE IHQ ---
    data['hospitalizado'] = 'NO'
    data['n_autorizacion'] = 'COEX'
    data['identificador_unico'] = '0'
    data['fecha_ordenamiento'] = data.get('fecha_toma', data.get('fecha_ingreso', ''))
    
    data['cups_code'] = CUPS_CODES.get(data['tipo_informe'], '')
    data['procedimiento'] = PROCEDIMIENTOS.get(data['cups_code'], '')
    
    # Para IHQ, el espécimen se extrae del campo órgano
    data['specimens'] = extract_specimens(data.get('organo', ''), data.get('numero_peticion', ''))
    
    return data