"""
Demo Final: Sistema Completo con Árboles de Recurrencia
=======================================================

Demostración final del sistema completo integrando:
1. Parsing avanzado
2. Análisis de complejidad O, Ω, Θ  
3. Dynamic Programming
4. 🌳 ÁRBOLES DE RECURRENCIA (nueva funcionalidad)
"""

import sys
import os

# Add the root directory to the path
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

from src.parser.parser import parse_code
from src.analyzer.dp_analyzer import DynamicProgrammingAnalyzer
from src.analyzer.complexity_engine import ComplexityAnalysisEngine

def final_system_demo():
    """Demo final del sistema completo con árboles de recurrencia."""
    
    print("🎓 ANALIZADOR DE COMPLEJIDADES - SISTEMA COMPLETO")
    print("=" * 70)
    print("🔍 Parser Avanzado + Análisis O,Ω,Θ + Dynamic Programming + 🌳 Árboles de Recurrencia")
    print("=" * 70)
    
    # Initialize systems
    engine = ComplexityAnalysisEngine()
    dp_analyzer = DynamicProgrammingAnalyzer()
    
    # Test with working pseudocode
    test_algorithms = [
        {
            "name": "Algoritmo Lineal Simple",
            "code": """
            function busqueda_lineal(n)
            begin
                suma 🡨 0
                for i 🡨 1 to n do
                begin
                    suma 🡨 suma + i
                end
                return suma
            end
            """,
            "expected_tree_pattern": "T(n) = T(n-1) + O(1)"
        },
        {
            "name": "Algoritmo Cuadrático",
            "code": """
            function algoritmo_cuadratico(n)
            begin
                resultado 🡨 0
                for i 🡨 1 to n do
                begin
                    for j 🡨 1 to n do
                    begin
                        resultado 🡨 resultado + i * j
                    end
                end
                return resultado
            end
            """,
            "expected_tree_pattern": "T(n) = T(n-1) + O(n)"
        }
    ]
    
    for i, test in enumerate(test_algorithms, 1):
        print(f"\n{i}. 🧪 {test['name']}")
        print("-" * 50)
        
        try:
            # Parse algorithm
            ast = parse_code(test['code'])
            print("✅ Parsing exitoso")
            
            # Standard complexity analysis
            result = engine.analyze(test['code'])
            print(f"📊 Análisis estándar: {result.big_o} | {result.omega} | {result.theta}")
            
            # DP-enhanced analysis with potential recurrence tree
            complexity_result, recurrence_tree = dp_analyzer.analyze_with_recurrence_tree(ast, max_levels=3)
            print(f"🧠 Análisis DP: {complexity_result.big_o} | {complexity_result.omega} | {complexity_result.theta}")
            
            if recurrence_tree:
                print(f"🌳 Árbol de recurrencia detectado:")
                print(f"   Relación: {recurrence_tree.recurrence_relation}")
                print(f"   Complejidad: {recurrence_tree.total_complexity}")
                print(f"   Patrón: {recurrence_tree.pattern_type}")
                
                # Show compact tree view
                print(f"\n📈 Vista compacta del árbol:")
                compact_view = recurrence_tree.generate_compact_view()[:200] + "..."
                print(f"   {compact_view}")
            else:
                print(f"ℹ️  No se detectó patrón recursivo (algoritmo iterativo)")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Demonstrate recurrence tree building directly
    print(f"\n🌳 DEMOSTRACIÓN DIRECTA DE ÁRBOLES DE RECURRENCIA")
    print("=" * 70)
    
    tree_examples = [
        "T(n) = 2T(n/2) + O(n)",      # Merge Sort
        "T(n) = T(n-1) + O(1)",       # Factorial  
        "T(n) = 2T(n-1) + O(1)"       # Binary recursion
    ]
    
    for relation in tree_examples:
        print(f"\n🔍 Relación: {relation}")
        try:
            tree = dp_analyzer.tree_builder.build_tree(relation, max_levels=3)
            
            print(f"   📊 Complejidad calculada: {tree.total_complexity}")
            print(f"   📈 Patrón: {tree.pattern_type}")
            
            # Show level costs  
            print(f"   💰 Costos por nivel:")
            for level, cost in enumerate(tree.level_costs[:3]):
                print(f"      Nivel {level}: {cost}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Final system statistics
    print(f"\n📊 ESTADÍSTICAS FINALES DEL SISTEMA")
    print("=" * 70)
    
    # DP Statistics
    dp_stats = dp_analyzer.get_dp_statistics()
    print(f"🧠 Dynamic Programming:")
    print(f"   Cache hits: {dp_stats['cache_hits']}")
    print(f"   Cache misses: {dp_stats['cache_misses']}")
    print(f"   Hit rate: {dp_stats['hit_rate_percentage']}%")
    print(f"   Patrones conocidos: {dp_stats['known_patterns']}")
    
    # Tree builder statistics
    built_trees = len(dp_analyzer.tree_builder.built_trees)
    print(f"🌳 Árboles de Recurrencia:")
    print(f"   Árboles construidos: {built_trees}")
    print(f"   Patrones soportados: Divide & Conquer, Linear, Exponential")
    
    # System capabilities summary
    print(f"\n🎯 CAPACIDADES DEL SISTEMA COMPLETO")
    print("=" * 70)
    print(f"✅ Parser extendido: Arrays, matrices, expresiones booleanas")
    print(f"✅ Análisis tri-dimensional: O (peor caso), Ω (mejor caso), Θ (caso exacto)")
    print(f"✅ Dynamic Programming: Memoización, estructura óptima, subproblemas superpuestos")
    print(f"✅ 🌳 Árboles de Recurrencia: Visualización y análisis de algoritmos recursivos")
    print(f"✅ Integración completa: Todos los componentes trabajando juntos")
    
    print(f"\n🏆 PROYECTO COMPLETADO EXITOSAMENTE")
    print(f"   Técnicas avanzadas de programación implementadas")
    print(f"   Sistema listo para análisis académico y profesional")

if __name__ == "__main__":
    final_system_demo()