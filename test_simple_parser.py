#!/usr/bin/env python3
"""
Test simple para debuggear el parser paso a paso
"""

import sys
import os

# Add the root directory to the path
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

from src.parser.parser import parse_code

def test_simple_cases():
    print("🧪 PRUEBAS SIMPLES DEL PARSER")
    print("=" * 40)
    
    # Casos de prueba incrementalmente más complejos
    test_cases = [
        # Caso 1: Función vacía
        """
        function test()
        begin
        end
        """,
        
        # Caso 2: Función con return simple
        """
        function test()
        begin
            return 1
        end
        """,
        
        # Caso 3: Función con asignación
        """
        function test()
        begin
            x ← 1
        end
        """,
        
        # Caso 4: Función con if simple
        """
        function test()
        begin
            if n <= 1
            begin
                return 1
            end
        end
        """,
    ]
    
    for i, code in enumerate(test_cases, 1):
        print(f"\n📝 Caso {i}:")
        print("=" * 20)
        print(code.strip())
        print("=" * 20)
        
        try:
            ast = parse_code(code)
            print("✅ ¡Éxito!")
            print(f"AST: {ast}")
        except Exception as e:
            print(f"❌ Error: {e}")
            print(f"   Tipo: {type(e).__name__}")

if __name__ == "__main__":
    test_simple_cases()