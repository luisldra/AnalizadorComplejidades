#!/usr/bin/env python3
"""Test específico para verificar detección de llamadas recursivas."""

import sys
import os
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

from src.parser.parser import parse_code
from src.analyzer.recurrence_solver import RecursiveAlgorithmAnalyzer

def test_recursive_calls_detection():
    """Test la detección de llamadas recursivas en factorial."""
    
    print("🔍 TEST DE DETECCIÓN DE LLAMADAS RECURSIVAS")
    print("=" * 60)
    
    code = """
    function factorial(n)
    begin
        if n <= 1
        begin
            return 1
        end
        else
        begin
            return n * call factorial(n - 1)
        end
    end
    """
    
    # Parse el código
    print("📝 Parseando código...")
    ast = parse_code(code)
    
    # Crear analizador
    analyzer = RecursiveAlgorithmAnalyzer()
    
    # Encontrar la función factorial
    factorial_func = None
    if hasattr(ast, 'functions'):
        for func in ast.functions:
            if hasattr(func, 'name') and func.name == 'factorial':
                factorial_func = func
                break
    
    if not factorial_func:
        print("❌ No se encontró la función factorial")
        return
    
    print(f"✅ Función factorial encontrada: {factorial_func.name}")
    
    # Buscar llamadas recursivas
    recursive_calls = analyzer._find_recursive_calls(factorial_func)
    
    print(f"\n🔍 Llamadas recursivas encontradas: {len(recursive_calls)}")
    
    for i, call in enumerate(recursive_calls):
        print(f"\n📞 Llamada {i+1}:")
        for key, value in call.items():
            print(f"   {key}: {value}")
    
    if len(recursive_calls) > 0:
        print("✅ ¡Detección de recursión exitosa!")
    else:
        print("❌ No se detectaron llamadas recursivas")
        
        # Debug: mostrar estructura de la función
        print("\n🔍 Estructura de la función para debug:")
        def debug_structure(node, indent=0):
            spacing = "  " * indent
            node_type = type(node).__name__
            print(f"{spacing}{node_type}", end="")
            
            if hasattr(node, 'name'):
                print(f" (name='{node.name}')", end="")
            if hasattr(node, 'op'):
                print(f" (op='{node.op}')", end="")
                
            print()
            
            # Explorar hijos
            for attr_name in ['body', 'then_body', 'else_body', 'condition', 'left', 'right', 'expr', 'args']:
                if hasattr(node, attr_name):
                    attr_value = getattr(node, attr_name)
                    if attr_value is not None:
                        if isinstance(attr_value, list):
                            if attr_value:
                                print(f"{spacing}  {attr_name}:")
                                for item in attr_value:
                                    debug_structure(item, indent + 2)
                        elif not isinstance(attr_value, (int, str, float, bool)):
                            print(f"{spacing}  {attr_name}:")
                            debug_structure(attr_value, indent + 2)
        
        debug_structure(factorial_func)

if __name__ == "__main__":
    test_recursive_calls_detection()