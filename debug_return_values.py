#!/usr/bin/env python3
"""Debug específico para los valores de Return."""

from src.parser.parser import parse_code

def debug_return_values():
    """Debug específico para ver qué contienen los Return statements."""
    
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
    
    print("🔍 DEBUG DE VALORES DE RETURN")
    print("=" * 50)
    
    ast = parse_code(code)
    
    def find_returns(node, path=""):
        """Encuentra todos los Return statements y muestra su contenido."""
        if hasattr(node, '__class__') and node.__class__.__name__ == 'Return':
            print(f"\n📍 Return encontrado en: {path}")
            print(f"   Tipo: {type(node).__name__}")
            
            # Examinar todos los atributos
            for attr_name in dir(node):
                if not attr_name.startswith('_'):
                    attr_value = getattr(node, attr_name)
                    if attr_value is not None and not callable(attr_value):
                        print(f"   {attr_name}: {attr_value} ({type(attr_value).__name__})")
            
            # Si tiene expr, explorarlo
            if hasattr(node, 'expr') and node.expr is not None:
                print(f"\n   🔎 Explorando expr:")
                explore_node(node.expr, "      ")
        
        # Continuar búsqueda recursiva
        for attr_name in ['functions', 'body', 'then_body', 'else_body', 'condition', 'left', 'right', 'value', 'args']:
            if hasattr(node, attr_name):
                attr_value = getattr(node, attr_name)
                if attr_value is not None:
                    if isinstance(attr_value, list):
                        for i, item in enumerate(attr_value):
                            find_returns(item, f"{path}.{attr_name}[{i}]")
                    elif hasattr(attr_value, '__class__'):
                        find_returns(attr_value, f"{path}.{attr_name}")

    def explore_node(node, indent):
        """Explora un nodo en detalle."""
        if node is None:
            return
            
        print(f"{indent}Tipo: {type(node).__name__}")
        
        # Mostrar atributos importantes
        for attr_name in dir(node):
            if not attr_name.startswith('_') and attr_name not in ['__class__', '__dict__', '__module__']:
                try:
                    attr_value = getattr(node, attr_name)
                    if attr_value is not None and not callable(attr_value):
                        if isinstance(attr_value, (str, int, float, bool)):
                            print(f"{indent}{attr_name}: {attr_value}")
                        elif isinstance(attr_value, list):
                            print(f"{indent}{attr_name}: [lista con {len(attr_value)} elementos]")
                            for i, item in enumerate(attr_value):
                                print(f"{indent}  [{i}]: {type(item).__name__}")
                                if hasattr(item, 'name'):
                                    print(f"{indent}      name: {item.name}")
                        else:
                            print(f"{indent}{attr_name}: {type(attr_value).__name__}")
                            if hasattr(attr_value, 'name'):
                                print(f"{indent}  name: {attr_value.name}")
                            if hasattr(attr_value, 'op'):
                                print(f"{indent}  op: {attr_value.op}")
                except Exception as e:
                    print(f"{indent}{attr_name}: Error accediendo - {e}")
    
    find_returns(ast)

if __name__ == "__main__":
    debug_return_values()