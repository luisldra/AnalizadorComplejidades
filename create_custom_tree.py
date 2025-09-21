#!/usr/bin/env python3
"""
Script para crear árboles de recurrencia personalizados
Usa este script para generar y visualizar tus propios árboles
"""

import sys
import os

# Add the root directory to the path
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

from src.analyzer.recurrence_tree_builder import RecurrenceTreeBuilder
from src.analyzer.recurrence_visualizer import RecurrenceTreeVisualizer

def create_custom_tree():
    print("🌳 GENERADOR DE ÁRBOLES DE RECURRENCIA PERSONALIZADO")
    print("=" * 60)
    
    # Crear el constructor de árboles
    tree_builder = RecurrenceTreeBuilder()
    
    while True:
        print("\n📝 Opciones disponibles:")
        print("1. T(n) = 2T(n/2) + O(n)     - Divide y vencerás (Merge Sort)")
        print("2. T(n) = T(n-1) + O(1)      - Recursión lineal (Factorial)")
        print("3. T(n) = 2T(n-1) + O(1)     - Recursión binaria (Fibonacci)")
        print("4. T(n) = 3T(n-1) + O(1)     - Recursión exponencial")
        print("5. T(n) = 4T(n/2) + O(n)     - Divide y vencerás más complejo")
        print("6. Crear relación personalizada")
        print("0. Salir")
        
        choice = input("\n🎯 Selecciona una opción (0-6): ").strip()
        
        if choice == "0":
            print("👋 ¡Hasta luego!")
            break
        elif choice == "1":
            tree = tree_builder.build_tree("T(n) = 2T(n/2) + O(n)", "Merge Sort - Divide y vencerás")
        elif choice == "2":
            tree = tree_builder.build_tree("T(n) = T(n-1) + O(1)", "Factorial - Recursión lineal")
        elif choice == "3":
            tree = tree_builder.build_tree("T(n) = 2T(n-1) + O(1)", "Fibonacci - Recursión binaria")
        elif choice == "4":
            tree = tree_builder.build_tree("T(n) = 3T(n-1) + O(1)", "Recursión exponencial")
        elif choice == "5":
            tree = tree_builder.build_tree("T(n) = 4T(n/2) + O(n)", "Algoritmo divide y vencerás complejo")
        elif choice == "6":
            print("\n📝 Ingresa tu relación de recurrencia:")
            print("Ejemplos: T(n) = 2T(n/2) + O(n), T(n) = T(n-1) + O(1)")
            relation = input("Relación: ").strip()
            description = input("Descripción (opcional): ").strip()
            if not description:
                description = "Relación personalizada"
            tree = tree_builder.build_tree(relation, description)
        else:
            print("❌ Opción inválida")
            continue
        
        if tree:
            print(f"\n🌳 Árbol generado para: {tree.relation}")
            print("=" * 60)
            
            # Mostrar visualización completa
            print(tree.visualize_tree())
            
            # Mostrar análisis por niveles
            complexity, details = tree.calculate_total_complexity()
            print(f"📊 Análisis de complejidad:")
            print(f"   Método: {details['method']}")
            print(f"   Niveles analizados: {details['levels_analyzed']}")
            print(f"   Fórmula: {details['summation_formula']}")
            print(f"   ✅ Complejidad total: {complexity}")
            
            # Preguntar si quiere ver vista compacta
            show_compact = input("\n🎯 ¿Mostrar vista compacta? (s/n): ").strip().lower()
            if show_compact in ['s', 'si', 'sí', 'y', 'yes']:
                print("\n📋 Vista compacta:")
                print(tree.get_compact_summary())
        else:
            print("❌ No se pudo generar el árbol. Verifica la sintaxis de la relación.")

if __name__ == "__main__":
    create_custom_tree()