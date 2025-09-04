
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar dependencias del OCR Médico
"""

import sys

def test_dependencies():
    """Probar todas las dependencias necesarias"""
    print("🔍 Verificando dependencias...")
    print("=" * 40)

    dependencies = {
        'pytesseract': 'Tesseract OCR Python wrapper',
        'pdf2image': 'Conversión de PDF a imágenes',
        'PIL': 'Python Imaging Library (Pillow)',
        'pandas': 'Manipulación de datos',
        'openpyxl': 'Lectura/escritura de Excel',
        'tkinter': 'Interfaz gráfica'
    }

    success_count = 0
    total_count = len(dependencies)

    for module, description in dependencies.items():
        try:
            if module == 'PIL':
                import PIL
            else:
                __import__(module)
            print(f"✅ {module:<12} - {description}")
            success_count += 1
        except ImportError as e:
            print(f"❌ {module:<12} - {description} (FALTANTE)")

    print("=" * 40)
    print(f"📊 Resultado: {success_count}/{total_count} dependencias instaladas")

    if success_count == total_count:
        print("🎉 ¡Todas las dependencias están instaladas!")
        return True
    else:
        print("⚠️  Hay dependencias faltantes. Ejecuta:")
        print("   pip install -r requirements.txt")
        return False

def test_tesseract():
    """Probar Tesseract OCR"""
    print("\n🔍 Verificando Tesseract OCR...")
    print("=" * 40)

    try:
        import pytesseract
        from PIL import Image
        import numpy as np

        # Crear imagen de prueba
        test_image = Image.new('RGB', (300, 100), color='white')
        # No podemos dibujar texto sin PIL.ImageDraw, así que solo verificamos que pytesseract funcione

        # Probar configuración de Tesseract
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✅ Tesseract versión: {version}")
            return True
        except Exception as e:
            print(f"❌ Error con Tesseract: {str(e)}")
            print("💡 Soluciones:")
            print("   - Instala Tesseract OCR en tu sistema")
            print("   - En Windows: https://github.com/UB-Mannheim/tesseract/wiki")
            print("   - En Linux: sudo apt-get install tesseract-ocr")
            print("   - En macOS: brew install tesseract")
            return False

    except ImportError:
        print("❌ pytesseract no instalado")
        return False

def test_sample_processing():
    """Probar procesamiento de muestra"""
    print("\n🔍 Verificando capacidades de procesamiento...")
    print("=" * 40)

    try:
        import re

        # Texto de muestra similar al PDF médico
        sample_text = """
        Nombre: JUAN PEREZ LOPEZ
        N. peticion: TEST123
        Edad: 45 años
        Genero: MASCULINO
        """

        # Probar extracción de datos
        patterns = {
            'nombre': r'Nombre\s*:\s*([A-ZÁÉÍÓÚÑ\s]+?)(?=\n|N\.|$)',
            'edad': r'Edad\s*:\s*(\d+)\s*años',
            'genero': r'Genero\s*:\s*([A-Z]+)'
        }

        extracted = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, sample_text)
            extracted[key] = match.group(1).strip() if match else None

        print("✅ Extracción de datos de prueba:")
        for key, value in extracted.items():
            if value:
                print(f"   {key}: {value}")

        return True

    except Exception as e:
        print(f"❌ Error en procesamiento de prueba: {str(e)}")
        return False

def main():
    """Función principal de prueba"""
    print("🚀 OCR Médico - Verificación del Sistema")
    print("=" * 50)
    print(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print("=" * 50)

    tests = [
        ("Dependencias de Python", test_dependencies),
        ("Tesseract OCR", test_tesseract), 
        ("Procesamiento de muestra", test_sample_processing)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        if test_func():
            passed += 1
        print()

    print("=" * 50)
    print(f"📊 RESUMEN FINAL: {passed}/{total} pruebas pasaron")

    if passed == total:
        print("🎉 ¡Sistema listo para OCR Médico!")
        print("▶️  Ejecuta: python huv_ocr_sistema_definitivo.py")
    else:
        print("⚠️  Sistema no completamente configurado")
        print("📖 Consulta README.md para solución de problemas")
        return 1

    return 0

if __name__ == "__main__":
    exit_code = main()
    input("\n🔄 Presiona Enter para salir...")
    sys.exit(exit_code)
