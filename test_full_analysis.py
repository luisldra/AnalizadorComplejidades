#!/usr/bin/env python3
"""Test del análisis completo de recursión para factorial."""

import sys
import os
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

from src.parser.parser import parse_code
from src.analyzer.recurrence_solver import RecursiveAlgorithmAnalyzer

def test_full_recursion_analysis():
    """Test del análisis completo de recursión."""
    
    print("🔍 TEST DEL ANÁLISIS COMPLETO DE RECURSIÓN")
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
    
    # Analizar la función factorial
    print("🔍 Analizando patrón de recursión...")
    result = analyzer.analyze_recursive_algorithm(factorial_func)
    
    print(f"\n📊 RESULTADO DEL ANÁLISIS:")
    print(f"=" * 40)
    
    for key, value in result.items():
        print(f"{key}: {value}")
    
    if factorial_func:
        print(f"\n🔍 ANÁLISIS ESPECÍFICO DE FACTORIAL:")
        print(f"=" * 40)
        
        # Encontrar llamadas recursivas
        calls = analyzer._find_recursive_calls(factorial_func)
        print(f"Llamadas recursivas encontradas: {len(calls)}")
        
        # Analizar el patrón
        if calls:
            pattern_analysis = analyzer._analyze_call_pattern(calls)
            print(f"Análisis del patrón: {pattern_analysis}")
            
            # Derivar relación de recurrencia
            relation = analyzer._derive_recurrence_relation(factorial_func, calls)
            print(f"Relación de recurrencia: {relation}")

if __name__ == "__main__":
    test_full_recursion_analysis()