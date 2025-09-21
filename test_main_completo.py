#!/usr/bin/env python3
"""
Script de prueba automatizada para el main del proyecto.
Valida todas las funcionalidades sin interacción del usuario.
"""

import sys
import os

# Add the root directory to the path
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

from src.main import AnalizadorCompleto
from src.parser.parser import parse_code

def test_analizador_completo():
    """Prueba automatizada de todas las funcionalidades."""
    
    print("🧪 PRUEBA AUTOMATIZADA DEL ANALIZADOR COMPLETO")
    print("=" * 60)
    
    # Inicializar analizador
    analizador = AnalizadorCompleto()
    
    # Probar carga de archivos
    print("\n1️⃣ PROBANDO CARGA DE ARCHIVOS")
    print("-" * 40)
    
    archivos_prueba = [
        "examples/factorial.txt",
        "examples/fibonacci.txt", 
        "examples/suma_iterativa.txt",
        "examples/merge_sort.txt",
        "examples/busqueda_binaria.txt",
        "examples/algoritmo_cubico.txt"
    ]
    
    resultados = {}
    
    for archivo in archivos_prueba:
        print(f"\n📁 Probando: {archivo}")
        codigo = analizador.cargar_pseudocodigo(archivo)
        
        if codigo:
            try:
                ast = parse_code(codigo)
                resultados[archivo] = ast
                print(f"   ✅ Archivo cargado y parseado correctamente")
            except Exception as e:
                print(f"   ❌ Error parseando: {e}")
                resultados[archivo] = None
        else:
            print(f"   ❌ Error cargando archivo")
            resultados[archivo] = None
    
    # Probar análisis con factorial
    print(f"\n2️⃣ PROBANDO ANÁLISIS CON FACTORIAL")
    print("-" * 40)
    
    factorial_ast = resultados.get("examples/factorial.txt")
    if factorial_ast:
        print(f"\n🔍 Análisis básico:")
        try:
            resultado_basico = analizador.analisis_basico(factorial_ast)
            print(f"   ✅ Completado: {resultado_basico.get('big_o', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print(f"\n🧠 Análisis con DP:")
        try:
            resultado_dp = analizador.analisis_con_dp(factorial_ast)
            print(f"   ✅ Completado: {resultado_dp.get('big_o', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print(f"\n🔄 Análisis de recursión:")
        try:
            resultado_rec = analizador.analisis_recursion(factorial_ast)
            print(f"   ✅ Completado: Recursivo={resultado_rec.get('recursivo', False)}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print(f"\n🌳 Análisis de árboles:")
        try:
            resultado_arbol = analizador.analisis_arboles_recurrencia(factorial_ast)
            print(f"   ✅ Completado: Árbol={resultado_arbol.get('tiene_arbol', False)}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print(f"\n📋 Reporte completo:")
        try:
            reporte = analizador.reporte_completo(factorial_ast)
            print(f"   ✅ Reporte generado ({len(reporte)} chars)")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Probar con diferentes tipos de algoritmos
    print(f"\n3️⃣ PROBANDO DIFERENTES ALGORITMOS")
    print("-" * 40)
    
    algoritmos_test = [
        ("examples/suma_iterativa.txt", "Iterativo lineal"),
        ("examples/fibonacci.txt", "Recursivo exponencial"),
        ("examples/merge_sort.txt", "Divide y vencerás"),
        ("examples/algoritmo_cubico.txt", "Bucles anidados")
    ]
    
    for archivo, descripcion in algoritmos_test:
        ast = resultados.get(archivo)
        if ast:
            print(f"\n📊 {descripcion} ({archivo}):")
            try:
                resultado = analizador.analisis_con_dp(ast)
                print(f"   Big O: {resultado.get('big_o', 'N/A')}")
                
                resultado_rec = analizador.analisis_recursion(ast)
                es_recursivo = resultado_rec.get('recursivo', False)
                print(f"   Recursivo: {'Sí' if es_recursivo else 'No'}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    print(f"\n✅ PRUEBA AUTOMATIZADA COMPLETADA")
    print("=" * 60)

if __name__ == "__main__":
    test_analizador_completo()