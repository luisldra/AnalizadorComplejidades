#!/usr/bin/env python3
"""
Script para probar suma_iterativa.txt con el programa principal
de forma automática
"""
import subprocess
import sys
import os

def test_main_programa():
    """Test del programa principal de forma automática"""
    
    print("🧪 TESTING MAIN.PY CON SUMA_ITERATIVA.TXT")
    print("=" * 60)
    
    # Cambiar al directorio del proyecto
    os.chdir("d:\\ArchivosLaptop\\Universidad\\Analisis y Diseño de Algoritmos\\Proyecto20252\\AnalizadorComplejidades")
    
    # Input automático para el programa
    inputs = [
        "examples/suma_iterativa.txt",  # Cargar archivo
        "1",                            # Opción 1: Análisis básico
        "",                            # Enter para continuar
        "3",                            # Opción 3: Análisis de recursión  
        "",                            # Enter para continuar
        "2",                            # Opción 2: Análisis DP
        "",                            # Enter para continuar
        "8"                             # Opción 8: Salir
    ]
    
    input_string = "\n".join(inputs) + "\n"
    
    try:
        # Ejecutar el programa principal con inputs automáticos
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            input=input_string,
            text=True,
            capture_output=True,
            timeout=30
        )
        
        print("📤 SALIDA DEL PROGRAMA:")
        print("-" * 40)
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ ERRORES:")
            print("-" * 40)
            print(result.stderr)
        
        print(f"\n✅ Código de salida: {result.returncode}")
        
        # Verificar si fue exitoso
        if result.returncode == 0:
            print(f"\n🎉 ¡ÉXITO! El programa principal funciona correctamente con suma_iterativa.txt")
            
            # Verificar que muestre complejidad O(n)
            if "Big O (peor caso):     n" in result.stdout:
                print(f"✅ Complejidad O(n) detectada correctamente")
            else:
                print(f"⚠️ Verificar detección de complejidad O(n)")
                
            # Verificar que detecte que no es recursivo
            if "No se detectaron algoritmos recursivos" in result.stdout:
                print(f"✅ Correctamente detectado como no recursivo")
            else:
                print(f"⚠️ Verificar detección de recursión")
                
        else:
            print(f"\n❌ ERROR: El programa terminó con código {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print(f"\n⏰ TIMEOUT: El programa tardó más de 30 segundos")
    except Exception as e:
        print(f"\n💥 ERROR EJECUTANDO: {e}")

if __name__ == "__main__":
    test_main_programa()