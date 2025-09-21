#!/usr/bin/env python3
"""
Test para verificar si el parser puede analizar el código factorial
"""

import sys
import os

# Add the root directory to the path
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

from src.parser.parser import parse_code

def test_factorial_code():
    print("🧪 PROBANDO PARSER CON CÓDIGO FACTORIAL")
    print("=" * 50)
    
    # Código factorial con diferentes formatos
    test_codes = [
        # Formato 1: Con begin/end y paréntesis
        """
        function factorial(n)
        begin
            if (n <= 1) then
            begin
                return 1
            end
            else
            begin
                return n * call factorial(n - 1)
            end
        end
        """,
        
        # Formato 2: Sin paréntesis en if
        """
        function factorial(n)
        begin
            if n <= 1 then
            begin
                return 1
            end
            else
            begin
                return n * call factorial(n - 1)
            end
        end
        """,
        
        # Formato 3: Más simple
        """
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
    ]
    
    for i, code in enumerate(test_codes, 1):
        print(f"\n📝 Probando formato {i}:")
        print("=" * 30)
        print(code.strip())
        print("=" * 30)
        
        try:
            ast = parse_code(code)
            print("✅ ¡Parser exitoso!")
            print(f"AST: {ast}")
        except Exception as e:
            print(f"❌ Error: {e}")
            
    print(f"\n🎯 Prueba completada")

if __name__ == "__main__":
    test_factorial_code()