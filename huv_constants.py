# huv_constants.py:
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Constantes compartidas para el sistema OCR HUV."""

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

# ─────────────────────── PATRONES REGEX DEFINITIVOS (VERSIÓN CORREGIDA) ───────────────────────
PATTERNS_HUV = {
    # Información básica del paciente
    'nombre_completo': r'Nombre\s*:\s*([^\n]+?)\s*(?:N\.\s*peticion|N\.Identificación)',
    'numero_peticion': r'N\.\s*peticion\s*:\s*([A-Z0-9\-]+)',
    'identificacion_completa': r'N\.Identificación\s*:\s*([A-Z]{1,3}\.?\s*[0-9\.]+)',
    'identificacion_numero': r'N\.Identificación\s*:\s*[A-Z\.]{1,3}\s*([0-9\.]+)',
    'tipo_documento': r'N\.Identificación\s*:\s*([A-Z]{1,3})\.?',
    'genero': r'Genero\s*:\s*([A-Z]+)',
    'edad': r'Edad\s*:\s*([^\n]+)',
    'eps': r'EPS\s*:\s*([^\n]+)',
    'medico_tratante': r'Médico tratante\s*:\s*([^\n]+?)\s*(?:Servicio|Fecha Ingreso|$)',
    'servicio': r'Servicio\s*:\s*([^\n]+)',
    'fecha_ingreso': r'Fecha Ingreso[^\d/]*(\d{2}/\d{2}/\d{4})',
    'fecha_informe': r'Fecha Informe[^\d/]*(\d{2}/\d{2}/\d{4})',
    'fecha_autopsia': r'Fecha y hora de la autopsia:\s*(\d{2}/\d{2}/\d{4})',

    # Información específica de estudios
    'organo': (r'(?is)(?:^|\n)\s*Ó?rgano(?:s)?(?:\s*\(1\.\s*Muestra enviada a patología\))?'
              r'\s*[:\-]?\s*([A-ZÁÉÍÓÚÑa-záéíóúñ0-9/ .,+\-]+?)'
              r'(?=(?:\s{2,}[A-ZÁÉÍÓÚÑ]{2,}|\n(?:Tipo de examen|Tipo de estudio|CUPS|Tarifa|Valor|Copago|Descuento|Fecha|Procedimiento|Servicio)\b|\n\n|$))'),
    'fecha_toma': r'Fecha toma\s*:\s*(\d{4}-\d{2}-\d{2})',
    'certificado_defuncion': r'No\.\s*Certificado\s*de\s*defunción\s*([0-9]+)',

    # Responsables
    'responsable_analisis': r'([A-ZÁÉÍÓÚÑ\s]+)\s*\n\s*Responsable del análisis',
    'usuario_finalizacion': r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}),\s*([A-ZÁÉÍÓÚÑ\s]+)',

    # --- SECCIÓN CORREGIDA ---
    # Descripciones largas
    # CORREGIDO: Captura el resumen clínico completo y la descripción macroscópica.
    'descripcion_macroscopica': r'Resumen de historia clínica\.([\s\S]+?)(?=DESCRIPCIÓN MICROSCÓPICA|PROTOCOLO MICROSCÓPICO)',
    
    # Este patrón ya era robusto y se mantiene.
    'descripcion_microscopica': r'(?:DESCRIPCIÓN MICROSCÓPICA|PROTOCOLO MICROSCÓPICO)\s*\n?([\s\S]+?)(?=DIAGN[OÓ]STICO)',
    
    # CORREGIDO: Captura la lista completa de diagnósticos.
    'diagnostico': r'DIAGNÓSTICO\s*\n(?:Diagnósticos anatomopatológicos:)?\s*([\s\S]+?)(?=\s*COMENTARIOS|\n\s*ARMANDO CORTES BUELVAS)',
    
    'comentarios': r'(?:^|\n)\s*COMENTARIOS\s*\n(.+?)(?=\n\s*ARMANDO CORTES BUELVAS|Responsable del análisis|$)',
    # --- FIN DE SECCIÓN CORREGIDA ---

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