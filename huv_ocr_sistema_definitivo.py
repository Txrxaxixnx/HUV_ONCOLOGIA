#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Punto de entrada principal para la aplicación EVARISIS Gestor H.U.V v2.0.

Este script se encarga de:
1. Configurar la ruta del ejecutable de Tesseract OCR.
2. Iniciar la interfaz gráfica de usuario moderna (dashboard).
"""

import configparser
import os
import sys
import pytesseract
from pathlib import Path

# Importamos la nueva y única clase 'App' desde nuestro módulo 'ui' rediseñado
from ui import App

def configure_tesseract():
    """
    Lee el archivo config.ini para encontrar la ruta de Tesseract OCR
    y la configura para que Pytesseract pueda utilizarla.
    """
    try:
        config = configparser.ConfigParser(interpolation=None)
        config_path = Path(__file__).resolve().parent / 'config.ini'
        config.read(config_path, encoding='utf-8')

        tesseract_cmd = None
        if sys.platform.startswith("win"):
            tesseract_cmd = config.get('PATHS', 'WINDOWS_TESSERACT', fallback=None)
        elif sys.platform.startswith("darwin"):
            tesseract_cmd = config.get('PATHS', 'MACOS_TESSERACT', fallback=None)
        else: # Asumimos Linux/otro
            tesseract_cmd = config.get('PATHS', 'LINUX_TESSERACT', fallback=None)

        if tesseract_cmd and Path(tesseract_cmd).exists():
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
            print(f"Tesseract OCR configurado en: {tesseract_cmd}")
        else:
            print("ADVERTENCIA: No se encontró la ruta de Tesseract en config.ini o la ruta no es válida.")
            print("El sistema intentará usar la variable de entorno PATH.")

    except Exception as e:
        print(f"Error al configurar Tesseract desde config.ini: {e}")
        print("Se continuará usando la configuración por defecto de Pytesseract.")


def main():
    """
    Función principal que configura el entorno y lanza la aplicación.
    """
    print("Iniciando EVARISIS Gestor H.U.V...")
    
    # 1. Configuramos Tesseract antes de que cualquier otra cosa lo necesite
    configure_tesseract()
    
    # 2. Creamos una instancia de nuestra nueva clase App y la ejecutamos
    #    La clase App ahora maneja su propia ventana y ciclo de vida.
    app = App()
    app.mainloop()
    
    print("Aplicación cerrada. ¡Hasta luego!")


if __name__ == "__main__":
    # Este es el único punto de ejecución del programa.
    main()