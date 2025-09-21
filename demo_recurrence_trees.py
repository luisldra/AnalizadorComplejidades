"""
Demo completo del Sistema de Árboles de Recurrencia
==================================================

Este demo muestra las nuevas capacidades del sistema para analizar algoritmos
recursivos mediante árboles de recurrencia, integrando técnicas de Dynamic Programming.
"""

import sys
import os

# Add the root directory to the path
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

from src.parser.parser import parse_code
from src.analyzer.dp_analyzer import DynamicProgrammingAnalyzer
from src.analyzer.recurrence_tree_builder import RecurrenceTreeBuilder
from src.analyzer.recurrence_models import RecurrenceTree, RecurrenceTreeNode

def demo_recurrence_trees():
    """Demonstrar el sistema completo de árboles de recurrencia."""
    
    print("🌳 SISTEMA DE ÁRBOLES DE RECURRENCIA")
    print("=" * 60)
    print("Análisis avanzado de algoritmos recursivos con visualización")
    print("Integrado con técnicas de Dynamic Programming")
    print("=" * 60)
    
    # Initialize components
    dp_analyzer = DynamicProgrammingAnalyzer()
    tree_builder = RecurrenceTreeBuilder()
    
    # Test cases with different recurrence patterns
    recurrence_examples = [
        {
            "name": "🔄 Divide & Conquer (Merge Sort)",
            "relation": "T(n) = 2T(n/2) + O(n)",
            "description": "Cada llamada divide el problema en 2 subproblemas de tamaño n/2 y hace trabajo O(n)"
        },
        {
            "name": "📈 Binary Recursion (Fibonacci)",  
            "relation": "T(n) = T(n-1) + T(n-2) + O(1)",
            "description": "Cada llamada genera 2 subproblemas decrementando n en 1 y 2"
        },
        {
            "name": "➡️ Linear Recursion (Factorial)",
            "relation": "T(n) = T(n-1) + O(1)", 
            "description": "Cada llamada genera 1 subproblema decrementando n en 1"
        },
        {
            "name": "🌿 Exponential Recursion",
            "relation": "T(n) = 3T(n-1) + O(1)",
            "description": "Cada llamada genera 3 subproblemas decrementando n en 1"
        }
    ]
    
    for i, example in enumerate(recurrence_examples, 1):
        print(f"\n{i}. {example['name']}")
        print("-" * 50)
        print(f"📝 Relación: {example['relation']}")
        print(f"💡 Descripción: {example['description']}")
        
        try:
            # Build recurrence tree
            tree = tree_builder.build_tree(example['relation'], max_levels=4)
            
            print(f"\n🌳 Árbol de Recurrencia:")
            print(tree.visualize_tree(max_width=70))
            
            print(f"\n📊 Análisis por Niveles:")
            print(tree.get_level_summary())
            
            # Calculate complexity from tree summation
            total_complexity, details = tree.calculate_complexity_from_tree()
            
            print(f"\n🧮 Cálculo de Complejidad:")
            print(f"   Método: {details['method']}")
            print(f"   Niveles analizados: {details['levels_analyzed']}")
            print(f"   Fórmula de sumatoria: {details['summation_formula']}")
            print(f"   ✅ Complejidad total: {total_complexity}")
            
        except Exception as e:
            print(f"   ❌ Error procesando {example['name']}: {e}")
        
        print("\n" + "="*60)
    
    # Test with actual code parsing
    print(f"\n🧪 PRUEBA CON CÓDIGO REAL")
    print("=" * 60)
    
    recursive_code = """
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
    
    print(f"📝 Código a analizar:")
    print(recursive_code)
    
    try:
        # Parse the code
        ast = parse_code(recursive_code)
        
        # Generate full recurrence report
        report = dp_analyzer.generate_recurrence_report(ast)
        print(f"\n📋 REPORTE COMPLETO:")
        print(report)
        
    except Exception as e:
        print(f"❌ Error analizando código: {e}")
    
    # Show DP integration benefits
    print(f"\n🚀 BENEFICIOS DE LA INTEGRACIÓN DP + ÁRBOLES")
    print("=" * 60)
    print(f"✅ Visualización clara de la estructura recursiva")
    print(f"✅ Cálculo preciso de complejidad por sumatoria de niveles")
    print(f"✅ Identificación automática de patrones de recurrencia")
    print(f"✅ Cache de árboles calculados para reutilización")
    print(f"✅ Análisis detallado del trabajo en cada nivel")
    print(f"✅ Integración completa con sistema DP existente")
    
    # Final statistics
    stats = dp_analyzer.get_dp_statistics()
    print(f"\n📊 Estadísticas del Sistema:")
    print(f"   🧠 Cache hits: {stats['cache_hits']}")
    print(f"   📤 Cache misses: {stats['cache_misses']}")
    print(f"   🎯 Hit rate: {stats['hit_rate_percentage']}%")
    print(f"   📚 Patrones reconocidos: {stats['patterns_recognized']}")
    print(f"   🗃️ Base de patrones: {stats['known_patterns']} patrones")
    
    print(f"\n🎓 ¡SISTEMA DE ÁRBOLES DE RECURRENCIA COMPLETADO!")
    print(f"   Técnica avanzada implementada exitosamente")

if __name__ == "__main__":
    demo_recurrence_trees()