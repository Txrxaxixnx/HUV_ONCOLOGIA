#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear ejecutable de OCR Médico
"""

import subprocess
import sys
import os
from pathlib import Path
import argparse

def run_command(command, description):
    """Ejecutar comando y mostrar progreso"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Completado")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error en {description}")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando {description}: {str(e)}")
        return False

def check_dependencies():
    """Verificar que PyInstaller esté instalado"""
    print("🔍 Verificando PyInstaller...")

    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} encontrado")
        return True
    except ImportError:
        print("❌ PyInstaller no instalado")
        print("📦 Instalando PyInstaller...")
        return run_command(f"{sys.executable} -m pip install pyinstaller", "Instalando PyInstaller")

def build_executable(main_script: str):
    """Construir el ejecutable"""

    if not os.path.exists(main_script):
        print(f"❌ No se encuentra {main_script}")
    if not os.path.exists("huv_ocr_sistema_definitivo.py"):
        print("❌ No se encuentra huv_ocr_sistema_definitivo.py")
        return False

    # Comando de PyInstaller
    command = [
        "pyinstaller",
        "--onefile",           # Un solo archivo
        "--windowed",          # Sin ventana de consola
        "--name=OCR_Medico",   # Nombre del ejecutable
        "--clean",             # Limpiar cache
        main_script
        "huv_ocr_sistema_definitivo.py"
    ]

    cmd_str = " ".join(command)
    print(f"🚀 Construyendo ejecutable...")
    print(f"   Comando: {cmd_str}")

    return run_command(cmd_str, "Creando ejecutable")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="Constructor de Ejecutable OCR Médico"
    )
    parser.add_argument(
        "script",
        nargs="?",
        default="huv_ocr_sistema_definitivo.py",
        help="Script principal de la aplicación",
    )
    args = parser.parse_args()

    print("🏗️  Constructor de Ejecutable OCR Médico")
    print("=" * 50)

    # Verificar dependencias
    if not check_dependencies():
        print("❌ No se pueden verificar dependencias")
        return 1

    # Construir ejecutable
    if not build_executable(args.script):
        print("❌ Error al construir ejecutable")
        return 1

    # Verificar resultado
    dist_dir = Path("dist")
    if dist_dir.exists():
        executables = list(dist_dir.glob("OCR_Medico*"))
        if executables:
            exe_path = executables[0]
            exe_size = exe_path.stat().st_size / (1024 * 1024)  # MB

            print("=" * 50)
            print("🎉 ¡Ejecutable creado exitosamente!")
            print(f"📍 Ubicación: {exe_path}")
            print(f"📊 Tamaño: {exe_size:.1f} MB")
            print()
            print("📋 Instrucciones:")
            print("1. Copia el ejecutable a cualquier computadora")
            print("2. Instala Tesseract OCR en la máquina destino")
            print("3. Ejecuta el archivo para usar OCR Médico")
            print()
            print("⚠️  IMPORTANTE: Tesseract OCR debe estar instalado")
            print("   en cada computadora donde uses el ejecutable")

            return 0
        else:
            print("❌ No se encontró el ejecutable en dist/")
            return 1
    else:
        print("❌ Carpeta dist/ no creada")
        return 1

if __name__ == "__main__":
    exit_code = main()
    input("\n🔄 Presiona Enter para salir...")
    sys.exit(exit_code)
