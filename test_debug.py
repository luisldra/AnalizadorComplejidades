#!/usr/bin/env python3
"""
Test debug para ver qué está pasando con el nodo If y Condition
"""

import sys
import os

# Add the root directory to the path
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

from src.parser.parser import parse_code
from src.analyzer.advanced_complexity import AdvancedComplexityAnalyzer

def test_debug():
    print("🔍 DEBUG DEL ERROR 'Condition' object is not iterable")
    print("=" * 60)
    
    code = """
    function test()
    begin
        if n <= 1
        begin
            return 1
        end
    end
    """
    
    try:
        # Parse the code
        print("📝 Parseando código...")
        ast = parse_code(code)
        print(f"✅ AST: {ast}")
        
        # Get the function
        function = ast.functions[0]
        print(f"✅ Función: {function}")
        print(f"   Nombre: {function.name}")
        print(f"   Body: {function.body}")
        
        # Get the if statement  
        if_stmt = function.body[0]
        print(f"✅ If statement: {if_stmt}")
        print(f"   Tipo: {type(if_stmt)}")
        print(f"   Condition: {if_stmt.condition}")
        print(f"   Condition tipo: {type(if_stmt.condition)}")
        print(f"   Then body: {if_stmt.then_body}")
        print(f"   Then body tipo: {type(if_stmt.then_body)}")
        
        # Try to analyze
        print("\n📊 Intentando analizar...")
        analyzer = AdvancedComplexityAnalyzer()
        result = analyzer.analyze(ast)
        print(f"✅ Resultado: {result}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"   Tipo: {type(e).__name__}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_debug()