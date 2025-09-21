#!/usr/bin/env python3
"""
Test directo para suma_iterativa.txt
Identifica y soluciona el problema con este algoritmo específico
"""

import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_suma_iterativa_debug():
    """Test para identificar el problema con suma_iterativa.txt"""
    
    print("🔍 DEBUGGING SUMA_ITERATIVA.TXT")
    print("=" * 60)
    
    # 1. Cargar el archivo
    print("\n1. CARGANDO ARCHIVO...")
    try:
        with open("examples/suma_iterativa.txt", 'r', encoding='utf-8') as f:
            pseudocodigo = f.read().strip()
        print(f"✅ Archivo cargado:")
        print(f"'{pseudocodigo}'")
    except Exception as e:
        print(f"❌ Error cargando archivo: {e}")
        return
    
    # 2. Test de parsing
    print("\n2. TESTING PARSER...")
    try:
        from src.parser.parser import parse_code
        ast = parse_code(pseudocodigo)
        print(f"✅ AST generado: {type(ast).__name__}")
        
        # Mostrar estructura del AST
        def mostrar_ast(nodo, nivel=0):
            indent = "  " * nivel
            if hasattr(nodo, '__class__'):
                nombre_clase = nodo.__class__.__name__
                print(f"{indent}{nombre_clase}")
                
                # Mostrar atributos importantes
                for attr in ['name', 'value', 'op', 'left', 'right', 'condition', 'body', 'else_body']:
                    if hasattr(nodo, attr):
                        valor = getattr(nodo, attr)
                        if valor is not None:
                            if isinstance(valor, list):
                                print(f"{indent}  {attr}: [{len(valor)} items]")
                                for item in valor:
                                    mostrar_ast(item, nivel + 2)
                            elif hasattr(valor, '__class__') and hasattr(valor.__class__, '__name__'):
                                print(f"{indent}  {attr}:")
                                mostrar_ast(valor, nivel + 2)
                            else:
                                print(f"{indent}  {attr}: {valor}")
            else:
                print(f"{indent}{nodo}")
        
        mostrar_ast(ast)
        
    except Exception as e:
        print(f"❌ Error en parsing: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 3. Test de análisis básico
    print("\n3. TESTING ANÁLISIS BÁSICO...")
    try:
        from src.analyzer.complexity_engine import ComplexityAnalysisEngine
        engine = ComplexityAnalysisEngine()
        complejidad = engine.analyze_complexity(ast)
        print(f"✅ Complejidad detectada: {complejidad}")
    except Exception as e:
        print(f"❌ Error en análisis básico: {e}")
        import traceback
        traceback.print_exc()
    
    # 4. Test con el sistema principal
    print("\n4. TESTING SISTEMA PRINCIPAL...")
    try:
        from src.main import AnalizadorCompleto
        analizador = AnalizadorCompleto()
        
        print("🔍 Ejecutando análisis básico...")
        analizador.analisis_basico(pseudocodigo)
        
        print("\n🔍 Ejecutando análisis de recursión...")
        analizador.analisis_recursion(pseudocodigo)
        
    except Exception as e:
        print(f"❌ Error en sistema principal: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_suma_iterativa_debug()