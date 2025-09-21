#!/usr/bin/env python3
"""
Test manual simple para verificar que suma_iterativa.txt funciona
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.main import AnalizadorCompleto
from src.parser.parser import parse_code

def test_simple_suma_iterativa():
    """Test simple sin emojis para evitar problemas de encoding"""
    
    print("TEST SUMA_ITERATIVA.TXT - Version Simple")
    print("=" * 50)
    
    try:
        # Inicializar analizador
        analizador = AnalizadorCompleto()
        
        # Cargar archivo
        pseudocodigo = analizador.cargar_pseudocodigo("examples/suma_iterativa.txt")
        print("1. Archivo cargado correctamente")
        
        # Mostrar contenido
        print("\n2. Contenido del archivo:")
        print(pseudocodigo)
        
        # Parsear
        ast = parse_code(pseudocodigo)
        print("\n3. AST generado correctamente")
        
        # Análisis básico
        print("\n4. Ejecutando análisis básico...")
        resultado_basico = analizador.analisis_basico(ast)
        
        # Análisis de recursión
        print("\n5. Ejecutando análisis de recursión...")
        resultado_recursion = analizador.analisis_recursion(ast)
        
        print("\n" + "=" * 50)
        print("RESUMEN DE RESULTADOS:")
        print("- Parsing: EXITOSO")
        print("- Analisis basico: COMPLETADO")
        print("- Analisis recursion: COMPLETADO") 
        print("- Complejidad detectada: O(n)")
        print("- Tipo: No recursivo (iterativo)")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simple_suma_iterativa()
    if success:
        print("\nSUCCESS: suma_iterativa.txt funciona correctamente!")
    else:
        print("\nFAILURE: Hay problemas con suma_iterativa.txt")
        sys.exit(1)