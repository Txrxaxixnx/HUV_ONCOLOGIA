
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de instalación de dependencias para OCR Médico
Este script instala automáticamente todas las dependencias necesarias
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Ejecutar comando y mostrar progreso"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Completado")
            return True
        else:
            print(f"❌ Error en {description}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando {description}: {str(e)}")
        return False

def install_python_packages():
    """Instalar paquetes de Python necesarios"""
    packages = [
        "pytesseract",
        "PyMuPDF",
        "pillow",
        "pandas",
        "openpyxl",
        "python-dateutil"
    ]

    print("📦 Instalando paquetes de Python...")

    for package in packages:
        success = run_command(
            f"{sys.executable} -m pip install {package}",
            f"Instalando {package}"
        )
        if not success:
            print(f"⚠️ Advertencia: No se pudo instalar {package}")

def install_tesseract():
    """Dar instrucciones para instalar Tesseract OCR"""
    system = platform.system().lower()

    print("\n🔍 Instalación de Tesseract OCR:")
    print("=" * 50)

    if system == "windows":
        print("📥 Para Windows:")
        print("1. Descarga el instalador desde:")
        print("   https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Ejecuta el instalador como administrador")
        print("3. Anota la ruta de instalación (ej: C:\Program Files\Tesseract-OCR\)")
        print("4. Asegúrate de que esté en el PATH del sistema")

    elif system == "linux":
        print("📥 Para Linux (Ubuntu/Debian):")
        print("Ejecuta: sudo apt-get install tesseract-ocr tesseract-ocr-spa")

        if run_command("sudo apt-get update", "Actualizando repositorios"):
            run_command(
                "sudo apt-get install -y tesseract-ocr tesseract-ocr-spa poppler-utils",
                "Instalando Tesseract OCR y dependencias"
            )

    elif system == "darwin":  # macOS
        print("📥 Para macOS:")
        print("Ejecuta: brew install tesseract tesseract-lang poppler")

        # Verificar si Homebrew está instalado
        if subprocess.run("which brew", shell=True, capture_output=True).returncode == 0:
            run_command("brew install tesseract tesseract-lang poppler", "Instalando Tesseract OCR")
        else:
            print("⚠️ Homebrew no encontrado. Instálalo desde: https://brew.sh")

    print("\n🔍 Verificando instalación de Tesseract...")
    if run_command("tesseract --version", "Verificando Tesseract"):
        print("✅ Tesseract OCR instalado correctamente")
    else:
        print("❌ Tesseract OCR no encontrado. Por favor instálalo manualmente.")

def create_requirements_file():
    """Crear archivo requirements.txt"""
    requirements = """# Dependencias para OCR Médico
pytesseract>=0.3.10
PyMuPDF>=1.23.0
pillow>=10.0.0
pandas>=2.0.0
openpyxl>=3.1.0
python-dateutil>=2.8.0
"""

    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements)
    print("📝 Archivo requirements.txt creado")

def main():
    print("🚀 Instalador de OCR Médico")
    print("=" * 40)
    print("Este script instalará todas las dependencias necesarias\n")

    # Verificar Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print("❌ Se requiere Python 3.7 o superior")
        print(f"   Versión actual: {python_version.major}.{python_version.minor}")
        return

    print(f"✅ Python {python_version.major}.{python_version.minor} detectado")

    # Actualizar pip
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Actualizando pip")

    # Instalar paquetes
    install_python_packages()

    # Crear requirements.txt
    create_requirements_file()

    # Instrucciones para Tesseract
    install_tesseract()

    print("\n" + "=" * 50)
    print("🎉 Instalación completada!")
    print("\n📋 Próximos pasos:")
    print("1. Verifica que Tesseract OCR esté instalado")
    print("2. Ajusta la ruta de Tesseract en ocr_medico_app.py si es necesario")
    print("3. Ejecuta: python ocr_medico_app.py")
    print("\n💡 Si tienes problemas, consulta el archivo README.md")

if __name__ == "__main__":
    main()
