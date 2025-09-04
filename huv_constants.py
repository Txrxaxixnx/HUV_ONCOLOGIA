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

# ─────────────────────── PATRONES REGEX ─────────────────────────
PATTERNS_HUV = {
    'nombre_completo': r'(?:^|\n)\s*Nombre\s*:?[\t ]*([^\n]+?)(?=\s*N\.\s*petici[óo]n|Autopsia\s+No\.|$)',
    'numero_peticion': r'N\.\s*petici[óo]n\s*:\s*([A-Z0-9\-]+)',
    'identificacion_completa': r'N\.Identificaci[óo]n\s*:\s*([A-Z]{1,3}\.?\s*[0-9\.]+)',
    'identificacion_numero': r'N\.Identificaci[óo]n\s*:\s*[A-Z\.]{1,3}\s*([0-9\.]+)',
    'tipo_documento': r'N\.Identificaci[óo]n\s*:\s*([A-Z]{1,3})\.?',
    'genero': r'G[ée]nero\s*:\s*([A-Z]+)',
    'edad': r'Edad\s*:\s*(\d+)\s*años',
    'eps': r'EPS\s*:\s*([^\n]+)',
    # Permite capturar "Médico tratante" o "Médico remitente"
    'medico_tratante': r'(?:M[ée]dico\s+tratante|M[ée]dico\s+remitente)\s*:?[\t ]*([^\n]+)',
    'servicio': r'Servicio\s*:\s*([^\n]+)',
    'fecha_ingreso': r'Fecha Ingreso\s*:\s*(\d{2}/\d{2}/\d{4})',
    'fecha_ingreso_alt': r'Fecha\s+de\s+ingreso\s*:?[\t ]*(\d{2}/\d{2}/\d{4})',
    'fecha_informe': r'Fecha Informe\s*:\s*(\d{2}/\d{2}/\d{4})',
    'fecha_autopsia': r'Fecha y hora de la autopsia:\s*(\d{2}/\d{2}/\d{4})',
    'organo': r'[ÓO]rgano\s*:\s*([A-ZÁÉÍÓÚÑ\s\+\(\)]+)',
    'organo_tabla': r'(?is)[ÓO]rgano\s+Fecha\s+toma.*?\n\s*([A-ZÁÉÍÓÚÑ\s\+\(\)]+?)\s*(?:\n\s*)*(?:\d{4}-\d{2}-\d{2})',
    'fecha_toma': r'Fecha\s*toma\s*:?[\t ]*(\d{4}-\d{2}-\d{2})',
    'fecha_toma_tabla': r'(?is)[ÓO]rgano\s+Fecha\s+toma.*?\n\s*[A-ZÁÉÍÓÚÑ\s\+\(\)]+?\s*(?:\n\s*)*(\d{4}-\d{2}-\d{2})',
    'responsable_analisis': r'([A-ZÁÉÍÓÚÑ\s]+)\s*\n\s*Responsable del análisis',
    'usuario_finalizacion': r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}),\s*([A-ZÁÉÍÓÚÑ\s]+)',
    # Encabezados de descripción con o sin tildes
    'descripcion_macroscopica': r'(?:^|\n)DESCRIPCI[ÓO]N\s+MACROSC[ÓO]PICA\s*(.+?)(?=\n(?:DESCRIPCI[ÓO]N\s+MICROSC[ÓO]PICA|PROTOCOLO\s+MICROSC[ÓO]PICO|DIAGN[OÓ]STICO)|$)',
    'descripcion_microscopica': r'(?:^|\n)(?:DESCRIPCI[ÓO]N\s+MICROSC[ÓO]PICA|PROTOCOLO\s+MICROSC[ÓO]PICO)\s*(.+?)(?=\n(?:DIAGN[OÓ]STICO|COMENTARIOS)|$)',
    'diagnostico': r'(?:^|\n)(?:DIAGN[OÓ]STICO(?:S)?(?:\s+ANATOMOPATOL[ÓO]GICOS)?)\s*:?[\r\n]+(.+?)(?=\nCOMENTARIOS|\nResponsable|$)',
    'comentarios': r'(?:^|\n)COMENTARIOS\s*(.+?)(?=\nResponsable|$)',
    # Bloque de resumen clínico
    'datos_clinicos': r'(?:^|\n)Resumen de historia cl[íi]nica\.?\s*(.+?)(?=\nIm[áa]genes diagn[óo]sticas|\nPARACL[ÍI]NICOS|\nPROTOCOLO MACROSC[ÓO]PICO|$)',
    'identificador_unico': r'Identificador\s+[ÚU]nico[^:]*:\s*([0-9]{4,})',
    'numero_autorizacion': r'N\.\s*Autorizaci[óo]n[^:]*:\s*([A-Z0-9\-\.]+)',
}

# ─────────────────────── PALABRAS CLAVE MALIGNIDAD ───────────────────────
MALIGNIDAD_KEYWORDS = [
    'CARCINOMA', 'CANCER', 'MALIGNO', 'MALIGNIDAD', 'METASTASIS', 'METASTÁSICO',
    'NEOPLASIA MALIGNA', 'TUMOR MALIGNO', 'ADENOCARCINOMA', 'LINFOMA',
    'SARCOMA', 'MELANOMA', 'LEUCEMIA', 'HODGKIN', 'HODKING',
]

