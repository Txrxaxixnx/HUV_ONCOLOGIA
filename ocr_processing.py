#ocr_processing.py:
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Funciones relacionadas con el procesamiento OCR."""

import io
import os
import re
import sys
import configparser
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image
import pytesseract

# ─────────────────────────── CONFIGURACIÓN ─────────────────────────────
_config = configparser.ConfigParser(interpolation=None)
_config.read(Path(__file__).resolve().parent / "config.ini", encoding="utf-8")

def _post_ocr_cleanup(txt: str) -> str:
    """Normaliza errores comunes del OCR que afectan la segmentación por IHQ."""
    # Une 'I H Q 250006' o 'IHQ 250006' → 'IHQ250006'
    txt = re.sub(r'I\s*H\s*Q\s*(\d{5,7})', r'IHQ\1', txt, flags=re.IGNORECASE)
    # Corrige IHO/IH0/lHQ → IHQ solo si van seguidos de 6–7 dígitos
    txt = re.sub(r'IH[O0lI]\s*(\d{5,7})', r'IHQ\1', txt, flags=re.IGNORECASE)
    # Variantes de “N. petición”
    txt = re.sub(r'(N[°.\s]*|No\.\s*|Nº\s*|N\s*)petici[oó]n\s*[:\-]?', 'N. peticion :', txt, flags=re.IGNORECASE)
    # Colapsa espacios múltiples, conserva saltos de línea
    txt = re.sub(r'[ \t]+', ' ', txt)
    return txt

if sys.platform.startswith("win"):
    tesseract_cmd = _config.get(
        "PATHS", "WINDOWS_TESSERACT", fallback=os.getenv("WINDOWS_TESSERACT")
    )
elif sys.platform.startswith("darwin"):
    tesseract_cmd = _config.get(
        "PATHS", "MACOS_TESSERACT", fallback=os.getenv("MACOS_TESSERACT")
    )
else:
    tesseract_cmd = _config.get(
        "PATHS", "LINUX_TESSERACT", fallback=os.getenv("LINUX_TESSERACT")
    )

if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

# Parámetros OCR y de procesamiento
DPI = _config.getint("OCR_SETTINGS", "DPI", fallback=300)
PSM_MODE = _config.getint("OCR_SETTINGS", "PSM_MODE", fallback=6)
LANGUAGE = _config.get("OCR_SETTINGS", "LANGUAGE", fallback="spa")
_extra_config = _config.get("OCR_SETTINGS", "OCR_CONFIG", fallback="")
_extra_config = re.sub(r"--psm\s*\d+", "", _extra_config).strip()

FIRST_PAGE = _config.getint("PROCESSING", "FIRST_PAGE", fallback=1)
LAST_PAGE = _config.getint("PROCESSING", "LAST_PAGE", fallback=0)
MIN_WIDTH = _config.getint("PROCESSING", "MIN_WIDTH", fallback=1000)


def pdf_to_text_enhanced(pdf_path: str) -> str:
    """Convierte PDF a texto con OCR optimizado"""
    try:
        full_text = ""
        doc = fitz.open(pdf_path)

        start_page = max(0, FIRST_PAGE - 1)
        end_page = LAST_PAGE if LAST_PAGE > 0 else len(doc)

        for page_num in range(start_page, min(end_page, len(doc))):
            page = doc.load_page(page_num)

            # 1) Intento texto nativo (mucho más limpio si el PDF no es escaneado)
            native = page.get_text("text") or ""
            native_ok = bool(re.search(r'IHQ\s*\d{5,7}', native, flags=re.IGNORECASE))
            if native_ok and len(native) > 100:
                page_text = native
            else:
                # 2) Fallback a OCR con preprocesamiento + reintento de PSM
                pix = page.get_pixmap(matrix=fitz.Matrix(DPI / 72, DPI / 72))
                img_bytes = pix.tobytes("ppm")
                img = Image.open(io.BytesIO(img_bytes))

                if img.mode != "L":
                    img = img.convert("L")

                if img.width < MIN_WIDTH:
                    scale = MIN_WIDTH / img.width
                    new_size = (int(img.width * scale), int(img.height * scale))
                    img = img.resize(new_size, Image.LANCZOS)

                # Idioma por defecto: español+inglés (mejor para siglas)
                lang = LANGUAGE if LANGUAGE else "spa+eng"

                # Probamos PSM declarado y un alterno (6 y 4 cubren la mayoría de layouts)
                tried_psm = []
                candidates = [PSM_MODE] + [m for m in (6, 4) if m != PSM_MODE]
                page_text = ""
                for psm in candidates:
                    if psm in tried_psm:
                        continue
                    tried_psm.append(psm)
                    config_str = f"--oem 1 --psm {psm} {_extra_config}".strip()
                    page_text = pytesseract.image_to_string(img, lang=lang, config=config_str)
                    if re.search(r'IHQ\s*\d{5,7}', page_text, flags=re.IGNORECASE) or len(page_text) > 200:
                        break

            # Limpieza post-OCR / nativo para estabilizar tokens de corte
            page_text = _post_ocr_cleanup(page_text)
            full_text += f"\n--- PÁGINA {page_num + 1} ---\n" + page_text

        doc.close()
        return full_text
    except Exception as e:
        raise Exception(f"Error procesando PDF {pdf_path}: {str(e)}")

