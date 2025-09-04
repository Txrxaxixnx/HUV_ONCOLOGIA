#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Funciones relacionadas con el procesamiento OCR."""

import io
import sys

import fitz  # PyMuPDF
from PIL import Image
import pytesseract

# Configuración específica para Windows
if sys.platform.startswith("win"):
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def pdf_to_text_enhanced(pdf_path: str) -> str:
    """Convierte PDF a texto con OCR optimizado"""
    try:
        full_text = ""
        doc = fitz.open(pdf_path)

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(400 / 72, 400 / 72))  # 400 DPI
            img_bytes = pix.tobytes("ppm")
            img = Image.open(io.BytesIO(img_bytes))

            # Preprocesamiento
            if img.mode != "L":
                img = img.convert("L")

            if img.width < 2000:
                scale = 2000 / img.width
                new_size = (int(img.width * scale), int(img.height * scale))
                img = img.resize(new_size, Image.LANCZOS)

            page_text = pytesseract.image_to_string(
                img,
                lang="spa",
                config="--psm 6 -c preserve_interword_spaces=1 -c tessedit_do_invert=0",
            )

            full_text += f"\n--- PÁGINA {page_num + 1} ---\n" + page_text

        doc.close()
        return full_text
    except Exception as e:
        raise Exception(f"Error procesando PDF {pdf_path}: {str(e)}")
