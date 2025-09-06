# processors/autopsy_processor.py:
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Módulo especializado en la extracción de datos de informes de AUTOPSIA."""

import re
# Importa las constantes y utilidades compartidas
from huv_constants import PATTERNS_BASE, CUPS_CODES, PROCEDIMIENTOS
from data_extraction import (
    split_full_name,
    calculate_birth_date,
    deduce_specialty,
    detect_malignancy
)

# Patrones específicos que se suman o sobreescriben a los básicos
PATTERNS_AUTOPSY = {
    **PATTERNS_BASE, # Hereda todos los patrones básicos
    'fecha_autopsia': r'Fecha y hora de la autopsia:\s*(\d{2}/\d{2}/\d{4})',
    'certificado_defuncion': r'No\.\s*Certificado\s*de\s*defunción\s*([0-9]+)',
    'descripcion_macroscopica': r'Resumen de historia clínica\.([\s\S]+?)(?=DESCRIPCIÓN MICROSCÓPICA|PROTOCOLO MICROSCÓPICO)',
    'descripcion_microscopica': r'(?:DESCRIPCIÓN MICROSCÓPICA|PROTOCOLO MICROSCÓPICO)\s*\n?([\s\S]+?)(?=DIAGN[OÓ]STICO)',
    'diagnostico': r'DIAGNÓSTICO\s*\n(?:Diagnósticos anatomopatológicos:)?\s*([\s\S]+?)(?=\s*COMENTARIOS|\n\s*ARMANDO CORTES BUELVAS)',
    'comentarios': r'(?:^|\n)\s*COMENTARIOS\s*\n(.+?)(?=\n\s*ARMANDO CORTES BUELVAS|Responsable del análisis|$)',
}

def extract_autopsy_data(text: str) -> dict:
    """Extrae datos de un informe de AUTOPSIA aplicando sus reglas específicas."""
    data = {'tipo_informe': 'AUTOPSIA'}

    for key, pattern in PATTERNS_AUTOPSY.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        data[key] = re.sub(r'\s+', ' ', match.group(1).strip()) if match else ''

    # --- Limpieza y Enriquecimiento ---
    data.update(split_full_name(data.get('nombre_completo', '')))
    data['identificacion_numero'] = re.sub(r'[^\d]', '', data.get('identificacion_numero', ''))
    
    edad_texto = data.get('edad', '')
    data['edad'] = re.search(r'(\d+)', edad_texto).group(1) if re.search(r'(\d+)', edad_texto) else ''
    data['fecha_nacimiento'] = calculate_birth_date(edad_texto, data.get('fecha_informe'))
    
    data['malignidad'] = detect_malignancy(data.get('diagnostico', ''), data.get('comentarios', ''))
    data['especialidad_deducida'] = deduce_specialty(data.get('servicio', ''), 'AUTOPSIA')

    # --- REGLAS DE NEGOCIO EXCLUSIVAS DE AUTOPSIA ---
    data['hospitalizado'] = 'SI'
    data['organo_final'] = 'CUERPO HUMANO COMPLETO'
    data['fecha_ordenamiento'] = data.get('fecha_autopsia', data.get('fecha_ingreso', ''))
    data['identificador_unico'] = data.get('certificado_defuncion', '')
    
    data['cups_code'] = CUPS_CODES.get(data['tipo_informe'], '')
    data['procedimiento'] = PROCEDIMIENTOS.get(data['cups_code'], '')
    
    num_peticion = data.get('numero_peticion', '')
    data['specimens'] = [{'muestra': num_peticion, 'organo': 'CUERPO HUMANO COMPLETO'}]
    
    return data