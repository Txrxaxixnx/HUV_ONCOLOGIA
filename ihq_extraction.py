# ihq_extraction.py:
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lógica de extracción específica para informes de INMUNOHISTOQUIMICA."""

import re
from huv_constants import CUPS_CODES, PROCEDIMIENTOS, MALIGNIDAD_KEYWORDS
# Importamos las funciones de utilidad que son genéricas
from data_extraction import (
    split_full_name,
    calculate_birth_date,
    deduce_specialty,
    detect_malignancy
)

# --- PATRONES ESPECÍFICOS PARA INMUNOHISTOQUIMICA ---
PATTERNS_IHQ = {
    # La mayoría de los patrones básicos son iguales al de autopsia
    'nombre_completo': r'Nombre\s*:\s*([^\n]+?)\s*(?:N\.\s*peticion|N\.Identificación)',
    'numero_peticion': r'N\.\s*peticion\s*:\s*([A-Z0-9\-]+)',
    'identificacion_numero': r'N\.Identificación\s*:\s*[A-Z\.]{1,3}\s*([0-9\.]+)',
    'tipo_documento': r'N\.Identificación\s*:\s*([A-Z]{1,3})\.?',
    'genero': r'Genero\s*:\s*([A-Z]+)',
    'edad': r'Edad\s*:\s*([^\n]+)',
    'eps': r'EPS\s*:\s*([^\n]+)',
    'medico_tratante': r'Médico tratante\s*:\s*([^\n]+?)\s*(?:Servicio|Fecha Ingreso|$)',
    'servicio': r'Servicio\s*:\s*([^\n]+)',
    'fecha_ingreso': r'Fecha Ingreso[^\d/]*(\d{2}/\d{2}/\d{4})',
    'fecha_informe': r'Fecha Informe[^\d/]*(\d{2}/\d{2}/\d{4})',
    'responsable_analisis': r'([A-ZÁÉÍÓÚÑ\s]+)\s*\n\s*Responsable del análisis',
    
    # --- PATRONES CORREGIDOS Y NUEVOS PARA IHQ ---
    # CORREGIDO: El 'organo' en IHQ no siempre tiene dos puntos. Hacemos ':' opcional.
    'organo': r'Organo\s*:?\s*([^\n]+)',
    
    # NUEVO: Patrón para capturar la 'Fecha toma' específica de IHQ.
    'fecha_toma': r'Fecha toma\s*:\s*(\d{4}-\d{2}-\d{2})',
    
    # CORREGIDO: La macroscópica en IHQ empieza después de la primera "DESCRIPCIÓN MACROSCÓPICA".
    'descripcion_macroscopica': r'DESCRIPCIÓN MACROSCÓPICA\s*\n([\s\S]+?)(?=DESCRIPCIÓN MICROSCÓPICA)',
    
    # Estos patrones funcionan bien para ambos formatos.
    'descripcion_microscopica': r'DESCRIPCIÓN MICROSCÓPICA([\s\S]+?)(?=DIAGN[OÓ]STICO)',
    'diagnostico': r'DIAGNÓSTICO\s*\n([\s\S]+?)(?=\s*ARMANDO CORTES BUELVAS|Todos los análisis son avalados)',
    # Para IHQ no hay sección de comentarios, así que podemos omitirlo o hacerlo muy general.
    'comentarios': r'(?:^|\n)\s*COMENTARIOS\s*\n(.+?)(?=\n\s*ARMANDO CORTES BUELVAS|$)',
}

def extract_ihq_data(text: str) -> dict:
    """Función principal para extraer datos de un informe de IHQ."""
    data = {'tipo_informe': 'INMUNOHISTOQUIMICA'}

    for key, pattern in PATTERNS_IHQ.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        data[key] = re.sub(r'\s+', ' ', match.group(1).strip()) if match else ''

    # --- LÓGICA DE PROCESAMIENTO Y LIMPIEZA ESPECÍFICA DE IHQ ---

    # 1. Limpieza de EPS (error de OCR 5.0.5 -> S.O.S)
    if data.get('eps'):
        data['eps'] = data['eps'].upper().replace('5.0.5', 'S.O.S').replace('5.O.5', 'S.O.S')

    # 2. Procesamiento de nombre e identificación
    data.update(split_full_name(data['nombre_completo']))
    data['identificacion_numero'] = re.sub(r'[^\d]', '', data['identificacion_numero'])
    
    # 3. Cálculo de fecha de nacimiento (usando la fecha correcta como referencia)
    edad_texto_completo = data['edad']
    anos_match = re.search(r'(\d+)', edad_texto_completo)
    data['edad'] = anos_match.group(1) if anos_match else ''
    ref_date_str = data.get('fecha_informe') or data.get('fecha_ingreso')
    data['fecha_nacimiento'] = calculate_birth_date(edad_texto_completo, ref_date_str)

    # 4. Asignación de Fecha de Ordenamiento (priorizando 'fecha_toma')
    data['fecha_ordenamiento'] = data.get('fecha_toma') or data.get('fecha_ingreso', '')

    # 5. Lógica de Hospitalización y Autorización para IHQ
    data['hospitalizado'] = 'NO'
    data['n_autorizacion'] = 'COEX'
    data['identificador_unico'] = '0'

    # 6. Deducción de Especialidad y Malignidad
    servicio = data.get('servicio', '')
    data['especialidad_deducida'] = deduce_specialty(servicio)
    # Aquí usamos la función global 'detect_malignancy' que actualizaremos
    data['malignidad'] = detect_malignancy(
        data.get('diagnostico', ''),
        data.get('descripcion_microscopica', '')
    )

    # 7. Asignación de CUPS
    data['cups_code'] = CUPS_CODES.get('INMUNOHISTOQUIMICA', '')
    data['procedimiento'] = PROCEDIMIENTOS.get(data['cups_code'], '')

    # 8. Creación de la lista de especímenes
    # Para IHQ, asumimos una sola muestra principal por ahora.
    organo_limpio = data.get('organo', 'No especificado').strip()
    data['specimens'] = [{'muestra': data.get('numero_peticion'), 'organo': organo_limpio}]
    
    return data