#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extractor dedicado de biomarcadores IHQ (HER2, Ki-67, ER/PR, PD-L1, P16, Estudios Solicitados).
No modifica el esquema operativo estándar ni otros procesadores.
Guarda los resultados en una base de datos SQLite para análisis posterior.
Capaz de procesar PDFs con múltiples informes, generando una fila por cada uno.
"""

import re
from datetime import datetime
from pathlib import Path
import pandas as pd

# Se asume que estos módulos están en el mismo directorio o en el PYTHONPATH
from ocr_processing import pdf_to_text_enhanced
import procesador_ihq as ihq
import database_manager  # Importamos el nuevo gestor de BD


# ---------------------------- Utilidades internas ----------------------------

_HDR_NEXT_STOPWORDS = (
    r'(?:\n\s*)(?:informe|descripci[oó]n|diagn[oó]stico|comentarios|responsable|nota)\b'
)

def _normalize_whitespace(text: str) -> str:
    # Conserva saltos de línea pero colapsa espacios múltiples
    return re.sub(r'[ \t]+', ' ', text)

def _iter_reports(full_text: str):
    """
    Segmenta el texto completo en bloques por informe, usando variaciones de
    'N. petición : IHQ######'. Incluye todo desde el marcador hasta antes del siguiente.
    """
    pattern = re.compile(
        r'(?:^|\n)\s*(?:N[°.\s]*|No\.\s*|Nº\s*|N\s*)?petici[oó]n\s*:\s*(IHQ\d{5,7})',
        re.IGNORECASE
    )
    matches = list(pattern.finditer(full_text))
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        yield full_text[start:end]

def _clean_token(t: str) -> str:
    """
    Limpieza y normalización ligera para tokens de 'Estudios solicitados'.
    Tolera errores de OCR comunes.
    """
    if not t:
        return ''
    u = t.upper().strip()

    # Elimina decoradores
    u = u.replace('·', '').replace('•', '').replace('–', '-').replace('_', '')
    u = re.sub(r'\s+', '', u)

    # Correcciones típicas de OCR
    repl = {
        'PL6': 'P16',          # p16 mal leído
        'WTI1': 'WT1',
        'MSHO6': 'MSH6',
        'MSHE6': 'MSH6',
        'CKAETE3': 'AE1/AE3',
        'CKAEI1/AE3': 'AE1/AE3',
        'CKAE1/AE3': 'AE1/AE3',
        'CK-AE1/AE3': 'AE1/AE3',
        'K167': 'KI67',
        'KI-67': 'KI67',
        'KI_67': 'KI67',
        'PDL1': 'PD-L1',
        'GATA3': 'GATA-3',
    }
    u = repl.get(u, u)

    # Filtra basura obvia
    if len(u) <= 1:
        return ''
    if u in {'PAG', 'COPIA', 'DE', 'DEL', 'EL'}:
        return ''
    return u

def _extract_estudios_solicitados(text: str) -> str:
    """
    Extrae bloque multi-línea de 'Estudios solicitados' y retorna una lista
    deduplicada de marcadores en formato 'A, B, C'.
    """
    # Captura desde el encabezado hasta antes del siguiente bloque típico o doble salto de línea
    m = re.search(
        rf'(?is)estudios\s+solicitados\s*:?.*?\n(.*?)(?:\n{{2,}}|{_HDR_NEXT_STOPWORDS})',
        text
    )
    if not m:
        # Fallback corto: lo que esté en la misma línea
        m2 = re.search(r'(?i)estudios\s+solicitados\s*:?\s*([^\n]+)', text)
        if not m2:
            return ''
        raw_block = m2.group(1)
    else:
        raw_block = m.group(1)

    # Divide por líneas y separadores comunes
    tokens = []
    for line in raw_block.splitlines():
        # Quita ruidos tipo columnas/guiones
        line = re.sub(r'^\s*[-–•]\s*', '', line)
        parts = re.split(r'[,\s;/|]+', line)
        for p in parts:
            t = _clean_token(p)
            if t:
                tokens.append(t)

    # Dedup manteniendo orden
    dedup = list(dict.fromkeys(tokens))
    return ', '.join(dedup)


# -------------------------- Extracción de biomarcadores -----------------------

def _extract_biomarkers(text: str) -> dict:
    """
    Función de extracción de biomarcadores mejorada y robustecida para manejar
    múltiples variaciones de texto encontradas en los informes del HUV.
    """
    out = {
        "IHQ_HER2": "",
        "IHQ_KI-67": "",
        "IHQ_RECEPTOR_ESTROGENO": "",
        "IHQ_RECEPTOR_PROGESTAGENOS": "",
        "IHQ_PDL-1": "",
        "IHQ_ESTUDIOS_SOLICITADOS": "",
        "IHQ_P16_ESTADO": "",
        "IHQ_P16_PORCENTAJE": "",
    }

    # Estudios Solicitados (bloque multi-línea, tolerante a tabla)
    out["IHQ_ESTUDIOS_SOLICITADOS"] = _extract_estudios_solicitados(text)

    # P16 (Patrones más flexibles)
    m_p16_estado = re.search(r'(?i)\bP\s*16\b[^\n]*?\b(positiv[oa]|negativ[oa])\b', text)
    if m_p16_estado:
        out["IHQ_P16_ESTADO"] = m_p16_estado.group(1).upper()
    elif re.search(r'(?i)\bP\s*16\b[^\n]*?\b(en\s+bloque|difus[ao])\b', text):
        out["IHQ_P16_ESTADO"] = 'POSITIVO'

    m_p16_pct = re.search(r'(?i)\bP\s*16\b[^\n%]*?(\d{1,3})\s*%', text)
    if m_p16_pct:
        out["IHQ_P16_PORCENTAJE"] = m_p16_pct.group(1)

    # HER2 (score e ISH/FISH)
    m_her2 = re.search(r'(?i)\bHER2(?:/NEU)?\b\s*[:\-(]?\s*(0|1\+|2\+|3\+|negativ[oa]|positiv[oa])', text)
    her2_score = ''
    if m_her2:
        val = m_her2.group(1).upper()
        if 'NEGATIVO' in val:
            her2_score = 'NEGATIVO'
        elif 'POSITIVO' in val:
            # Si sólo dice "positivo", asumimos 3+ a menos que ISH diga algo distinto
            her2_score = 'POSITIVO (3+)'
        else:
            her2_score = val

    m_ish = re.search(r'(?i)\b(?:I?FISH|ISH)\b[^\n]*?\b(amplificad[oa]|no\s*amplificad[oa])\b', text)
    her2_ish = m_ish.group(1).upper().replace(' ', '_') if m_ish else ''

    her2_final = her2_score
    if her2_ish:
        ish_status = 'AMPLIFICADO' if 'AMPLIFICAD' in her2_ish else 'NO AMPLIFICADO'
        her2_final = f"{her2_score} ({ish_status})" if her2_score else ish_status
    out["IHQ_HER2"] = her2_final.strip()

    # Ki-67 (tolerante a K167/KI 67 y "<1%")
    m_ki = re.search(
        r'(?i)\bK[IL]\s*[- ]?67\b[^\n%]*?(?:de|del|en|aproximadamente|menor\s+al|menor\s+del)?\s*<?\s*(\d{1,3})\s*%',
        text
    )
    if m_ki:
        out["IHQ_KI-67"] = f"{m_ki.group(1)}%"

    # ER/RE (Receptor de Estrógeno)
    m_re = re.search(
        r'(?i)(?:receptor(?:es)?(?:\s+hormonal)?\s+de\s+estr[oó]geno|\bRE\b|\bER\b)'
        r'[^\n]*?(positiv[oa]|negativ[oa])?\s*(?:en\s+el|de|del)?\s*\(?(\d{1,3})\s*%\)?',
        text
    )
    re_estado, re_pct = '', ''
    if m_re:
        if m_re.group(1):
            re_estado = m_re.group(1).upper()
        if m_re.group(2):
            re_pct = m_re.group(2) + "%"
    else:
        m_re_estado_fallback = re.search(
            r'(?i)(?:receptor(?:es)?(?:\s+hormonal)?\s+de\s+estr[oó]geno|\bRE\b|\bER\b)[^\n]*?\b(positiv[oa]|negativ[oa])\b',
            text
        )
        m_re_pct_fallback = re.search(
            r'(?i)(?:receptor(?:es)?(?:\s+hormonal)?\s+de\s+estr[oó]geno|\bRE\b|\bER\b)[^\n%]*?(\d{1,3})\s*%',
            text
        )
        if m_re_estado_fallback:
            re_estado = m_re_estado_fallback.group(1).upper()
        if m_re_pct_fallback:
            re_pct = m_re_pct_fallback.group(1) + "%"
    out["IHQ_RECEPTOR_ESTROGENO"] = f"{re_estado} {re_pct}".strip()

    # PR/RP (Receptor de Progestágenos)
    m_rp = re.search(
        r'(?i)(?:receptor(?:es)?(?:\s+hormonal)?\s+de\s+progest(?:erona|ágenos)|\bRP\b|\bPR\b)'
        r'[^\n]*?(positiv[oa]|negativ[oa])?\s*(?:en\s+el|de|del)?\s*\(?(\d{1,3})\s*%\)?',
        text
    )
    rp_estado, rp_pct = '', ''
    if m_rp:
        if m_rp.group(1):
            rp_estado = m_rp.group(1).upper()
        if m_rp.group(2):
            rp_pct = m_rp.group(2) + "%"
    else:
        m_rp_estado_fallback = re.search(
            r'(?i)(?:receptor(?:es)?(?:\s+hormonal)?\s+de\s+progest(?:erona|ágenos)|\bRP\b|\bPR\b)[^\n]*?\b(positiv[oa]|negativ[oa])\b',
            text
        )
        m_rp_pct_fallback = re.search(
            r'(?i)(?:receptor(?:es)?(?:\s+hormonal)?\s+de\s+progest(?:erona|ágenos)|\bRP\b|\bPR\b)[^\n%]*?(\d{1,3})\s*%',
            text
        )
        if m_rp_estado_fallback:
            rp_estado = m_rp_estado_fallback.group(1).upper()
        if m_rp_pct_fallback:
            rp_pct = m_rp_pct_fallback.group(1) + "%"
    out["IHQ_RECEPTOR_PROGESTAGENOS"] = f"{rp_estado} {rp_pct}".strip()

    # PD-L1 (TPS y/o CPS)
    m_tps = re.search(r'(?i)\bPD\s*-?L1\b[^\n]*?\bTPS\b[^\n%<]*?<?\s*(\d{1,3})\s*%', text)
    m_cps = re.search(r'(?i)\bPD\s*-?L1\b[^\n]*?\bCPS\b[^\n\d<]*?<?\s*(\d{1,3})', text)
    pdl1_parts = []
    if m_tps:
        pdl1_parts.append(f"TPS {m_tps.group(1)}%")
    if m_cps:
        pdl1_parts.append(f"CPS {m_cps.group(1)}")
    out["IHQ_PDL-1"] = ' '.join(pdl1_parts)
    if not out["IHQ_PDL-1"]:
        m_pdl1_fallback = re.search(r'(?i)\bPD\s*-?L1\b\s*[:\-(]?\s*([^\n]+)', text)
        if m_pdl1_fallback:
            out["IHQ_PDL-1"] = m_pdl1_fallback.group(1).strip()

    return out


# --------------------------- Proceso principal (IO) ---------------------------

def process_ihq_paths(pdf_paths: list[str], output_dir: str) -> int:
    """
    Procesa una lista de rutas de PDF, extrae los datos y los guarda en la BD.
    Devuelve el número de registros procesados.
    """
    rows = []
    extended_columns = None

    for pdf in pdf_paths:
        full_text = pdf_to_text_enhanced(pdf)
        if not isinstance(full_text, str):
            # Por si el OCR retorna lista de páginas; unifícalas
            try:
                full_text = '\n'.join(full_text)
            except Exception:
                full_text = str(full_text)

        full_text = _normalize_whitespace(full_text)

        # Segmentación robusta por informe
        for single_report_text in _iter_reports(full_text):
            # Extrae datos base del encabezado/secciones estándar
            base = ihq.extract_ihq_data(single_report_text)
            base_rows = ihq.map_to_excel_format(base)
            if not base_rows:
                continue

            row = dict(base_rows[0])

            # Biomarcadores y estudios solicitados
            biomarkers = _extract_biomarkers(single_report_text)
            row.update(biomarkers)
            rows.append(row)

            # Preparar columnas completas solo una vez
            if extended_columns is None:
                base_cols = list(base_rows[0].keys())
                extra_cols = list(biomarkers.keys())
                extended_columns = base_cols + extra_cols

    if not rows:
        raise RuntimeError("No se pudo extraer información de los PDFs IHQ seleccionados.")

    df = pd.DataFrame(rows)
    if extended_columns:
        df = df.reindex(columns=extended_columns)

    # --- Persistencia en Base de Datos ---
    records_to_save = df.to_dict('records')
    database_manager.init_db()         # Se asegura que la DB y tabla existan
    database_manager.save_records(records_to_save)

    print(f"✅ {len(records_to_save)} registros guardados/actualizados en la base de datos.")
    return len(records_to_save)
