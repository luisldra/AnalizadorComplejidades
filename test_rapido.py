#!/usr/bin/env python3
"""Test rápido del main con factorial."""

import sys
import os
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

from src.main import AnalizadorCompleto
from src.parser.parser import parse_code

def test_rapido():
    print("🧪 TEST RÁPIDO DEL MAIN")
    print("=" * 40)
    
    analizador = AnalizadorCompleto()
    
    # Cargar factorial
    codigo = analizador.cargar_pseudocodigo("examples/factorial.txt")
    if codigo:
        ast = parse_code(codigo)
        
        print("\n1. Análisis básico:")
        resultado = analizador.analisis_basico(ast)
        print(f"   ✅ Big O: {resultado.get('big_o', 'N/A')}")
        
        print("\n2. Análisis recursión:")
        resultado = analizador.analisis_recursion(ast)
        print(f"   ✅ Recursivo: {resultado.get('recursivo', False)}")
        
        print("\n✅ Test completado")

if __name__ == "__main__":
    test_rapido()