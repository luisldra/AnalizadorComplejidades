#!/usr/bin/env python3
"""
Test específico para detección de recursión
"""

import sys
import os

# Add the root directory to the path
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

from src.parser.parser import parse_code
from src.analyzer.recurrence_solver import RecursiveAlgorithmAnalyzer

def test_recursion_detection():
    print("🔍 TEST DE DETECCIÓN DE RECURSIÓN")
    print("=" * 50)
    
    factorial_code = """
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
    
    try:
        # Parse the code
        print("📝 Parseando código factorial...")
        ast = parse_code(factorial_code)
        function = ast.functions[0]
        print(f"✅ Función parseada: {function.name}")
        
        # Analyze recursion
        print("\n🔍 Analizando recursión...")
        analyzer = RecursiveAlgorithmAnalyzer()
        analysis = analyzer.analyze_recursive_algorithm(function)
        
        print(f"📊 Resultado del análisis:")
        print(f"   Nombre: {analysis['function_name']}")
        print(f"   ¿Tiene recursión?: {analysis['has_recursion']}")
        print(f"   Llamadas recursivas: {len(analysis['recursive_calls'])}")
        print(f"   Casos base: {analysis['base_cases']}")
        print(f"   Trabajo por llamada: {analysis['work_per_call']}")
        print(f"   Relación de recurrencia: {analysis['recurrence_relation']}")
        print(f"   Complejidad estimada: {analysis['estimated_complexity']}")
        print(f"   Tipo de patrón: {analysis['pattern_type']}")
        
        if analysis['recursive_calls']:
            print(f"\n📋 Detalles de llamadas recursivas:")
            for i, call in enumerate(analysis['recursive_calls']):
                print(f"   Llamada {i+1}: profundidad={call['depth']}, args={call['arguments']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_recursion_detection()