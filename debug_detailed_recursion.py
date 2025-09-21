#!/usr/bin/env python3
"""Debug detallado de la detección de recursión."""

import sys
import os
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

from src.parser.parser import parse_code
from src.ast.nodes import Call, Function, Var

def debug_recursion_detection():
    """Debug detallado de la detección de recursión."""
    
    print("🔍 DEBUG DETALLADO DE DETECCIÓN DE RECURSIÓN")
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
        
    print(f"✅ Función encontrada: {factorial_func.name} (tipo: {type(factorial_func.name)})")
    
    # Traversar todo el AST buscando Call nodes
    print("\n🔍 Buscando todos los Call nodes...")
    
    def find_calls(node, path="", depth=0):
        """Encuentra todos los Call nodes y muestra detalles."""
        indent = "  " * depth
        
        if isinstance(node, Call):
            print(f"{indent}📞 CALL ENCONTRADO en {path}:")
            print(f"{indent}   node.name: {node.name}")
            print(f"{indent}   tipo de node.name: {type(node.name)}")
            
            if hasattr(node.name, 'name'):
                print(f"{indent}   node.name.name: {node.name.name}")
                print(f"{indent}   tipo de node.name.name: {type(node.name.name)}")
            
            print(f"{indent}   function_node.name: {factorial_func.name}")
            print(f"{indent}   tipo de function_node.name: {type(factorial_func.name)}")
            
            # Hacer la comparación paso a paso
            call_name = None
            if hasattr(node.name, 'name'):
                call_name = node.name.name
                print(f"{indent}   call_name extraído: '{call_name}'")
            elif isinstance(node.name, str):
                call_name = node.name
                print(f"{indent}   call_name (string directo): '{call_name}'")
            
            if call_name:
                is_recursive = call_name == factorial_func.name
                print(f"{indent}   ¿Es recursiva? {is_recursive} ('{call_name}' == '{factorial_func.name}')")
            else:
                print(f"{indent}   ❌ No se pudo extraer call_name")
            
            print(f"{indent}   args: {len(node.args) if hasattr(node, 'args') and node.args else 0}")
            print()
        
        # Continuar búsqueda recursiva
        for attr_name in ['functions', 'body', 'then_body', 'else_body', 'condition', 'left', 'right', 'expr', 'args']:
            if hasattr(node, attr_name):
                attr_value = getattr(node, attr_name)
                if attr_value is not None:
                    if isinstance(attr_value, list):
                        for i, item in enumerate(attr_value):
                            find_calls(item, f"{path}.{attr_name}[{i}]", depth + 1)
                    elif hasattr(attr_value, '__class__'):
                        find_calls(attr_value, f"{path}.{attr_name}", depth + 1)
    
    find_calls(factorial_func, "factorial_func")

if __name__ == "__main__":
    debug_recursion_detection()