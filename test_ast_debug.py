#!/usr/bin/env python3
"""
Test debug más detallado para ver el AST
"""

import sys
import os

# Add the root directory to the path
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

from src.parser.parser import parse_code

def print_ast_structure(node, indent=0):
    """Print AST structure recursively."""
    spacing = "  " * indent
    node_type = type(node).__name__
    
    print(f"{spacing}{node_type}", end="")
    
    # Show important attributes
    if hasattr(node, 'name'):
        print(f" (name='{node.name}')", end="")
    if hasattr(node, 'op'):
        print(f" (op='{node.op}')", end="")
    if hasattr(node, 'value') and not hasattr(node, 'body') and not isinstance(node.value, (list, object)):
        print(f" (value='{node.value}')", end="")
    
    print()
    
    # Special handling for Return nodes
    if node_type == 'Return' and hasattr(node, 'value'):
        print(f"{spacing}  return_value:")
        print_ast_structure(node.value, indent + 2)
    
    # Traverse children
    if hasattr(node, 'functions'):
        for func in node.functions:
            print_ast_structure(func, indent + 1)
    elif hasattr(node, 'body') and isinstance(node.body, list):
        for stmt in node.body:
            print_ast_structure(stmt, indent + 1)
    elif hasattr(node, 'then_body'):
        if isinstance(node.then_body, list):
            print(f"{spacing}  then_body:")
            for stmt in node.then_body:
                print_ast_structure(stmt, indent + 2)
        else:
            print(f"{spacing}  then_body:")
            print_ast_structure(node.then_body, indent + 2)
        
        if hasattr(node, 'else_body') and node.else_body:
            if isinstance(node.else_body, list):
                print(f"{spacing}  else_body:")
                for stmt in node.else_body:
                    print_ast_structure(stmt, indent + 2)
            else:
                print(f"{spacing}  else_body:")
                print_ast_structure(node.else_body, indent + 2)
    
    if hasattr(node, 'condition') and node.condition:
        print(f"{spacing}  condition:")
        print_ast_structure(node.condition, indent + 2)
    
    if hasattr(node, 'value') and node.value is not None and not hasattr(node, 'body'):
        if not isinstance(node.value, (int, str, float, bool)):
            print(f"{spacing}  value:")
            print_ast_structure(node.value, indent + 2)
    
    if hasattr(node, 'left'):
        print(f"{spacing}  left:")
        print_ast_structure(node.left, indent + 2)
    
    if hasattr(node, 'right'):
        print(f"{spacing}  right:")
        print_ast_structure(node.right, indent + 2)
    
    if hasattr(node, 'args') and node.args:
        print(f"{spacing}  args:")
        for arg in node.args:
            print_ast_structure(arg, indent + 2)
    
    if hasattr(node, 'args') and node.args:
        print(f"{spacing}  args:")
        for arg in node.args:
            print_ast_structure(arg, indent + 2)

def test_ast_debug():
    print("🔍 DEBUG DEL AST DEL CÓDIGO FACTORIAL")
    print("=" * 60)
    
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
        print("📝 Parseando código...")
        ast = parse_code(factorial_code)
        
        print(f"\n🌳 Estructura completa del AST:")
        print_ast_structure(ast)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ast_debug()