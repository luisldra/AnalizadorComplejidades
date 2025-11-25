"""
Analizador de Programación Dinámica - Refactorizado
==========================================

Este módulo implementa el analizador de Programación Dinámica principal siguiendo SRP.
Se coordina entre diferentes componentes especializados para el análisis de recurrencia.
"""

from typing import Dict, List, Optional, Tuple, Any
import hashlib
import json
from src.ast.nodes import *
from src.analyzer.advanced_complexity import ComplexityResult, AdvancedComplexityAnalyzer
from src.analyzer.recurrence_models import RecurrencePattern, RecurrenceTree
from src.analyzer.recurrence_tree_builder import TreeStructure
from src.analyzer.recurrence_visualizer import RecurrenceTreeVisualizer
from src.analyzer.recurrence_solver import RecurrenceSolver, RecursiveAlgorithmAnalyzer


class DynamicProgrammingAnalyzer:
    """
    Coordinador principal para el análisis de complejidad basado en Programación Dinámica.
    
    Responsabilidades:
    - Coordinar entre componentes especializados
    - Gestionar la caché de PD para resultados de análisis
    - Proporcionar una interfaz unificada para el análisis de PD
    - Generar informes comprensivos
    """
    
    def __init__(self):
        # Caché de PD principal: tabla de memorización para los nodos analizados
        self.analysis_cache: Dict[str, ComplexityResult] = {}
        
        # Caché de patrones: almacena patrones de recurrencia reconocidos
        self.pattern_cache: Dict[str, RecurrencePattern] = {}
        
        # Componentes especializados (Inyección de Dependencias)
        self.tree_builder = TreeStructure()
        self.visualizer = RecurrenceTreeVisualizer()
        self.solver = RecurrenceSolver()
        self.recursive_analyzer = RecursiveAlgorithmAnalyzer()
        self.base_analyzer = AdvancedComplexityAnalyzer()
        
        # Estadísticas para el seguimiento del rendimiento de PD
        self.cache_hits = 0
        self.cache_misses = 0
        self.patterns_recognized = 0
        
        # Inicializar base de datos de patrones
        self._initialize_pattern_database()
    
    def _initialize_pattern_database(self):
        """Inicializar base de datos de patrones comunes de recurrencia usando principios de PD."""
        
        # Patrones clásicos de PD - esta es nuestra "tabla de PD" de soluciones conocidas
        patterns = [
            RecurrencePattern(
                pattern_type="linear_recursion",
                base_cases={"T(0)": "1", "T(1)": "1"},
                recurrence_formula="T(n) = T(n-1) + O(1)",
                solution="n",
                confidence=0.95
            ),
            RecurrencePattern(
                pattern_type="binary_recursion",
                base_cases={"T(0)": "1", "T(1)": "1"},
                recurrence_formula="T(n) = 2*T(n-1) + O(1)",
                solution="2^n",
                confidence=0.95
            ),
            RecurrencePattern(
                pattern_type="divide_conquer",
                base_cases={"T(1)": "1"},
                recurrence_formula="T(n) = 2*T(n/2) + O(n)",
                solution="n*log(n)",
                confidence=0.90
            ),
            RecurrencePattern(
                pattern_type="fibonacci_like",
                base_cases={"T(0)": "1", "T(1)": "1"},
                recurrence_formula="T(n) = T(n-1) + T(n-2) + O(1)",
                solution="phi^n",  # Golden ratio
                confidence=0.85
            ),
            RecurrencePattern(
                pattern_type="tree_recursion",
                base_cases={"T(1)": "1"},
                recurrence_formula="T(n) = k*T(n/k) + O(n)",
                solution="n*log(n)",
                confidence=0.85
            )
        ]
        
        for pattern in patterns:
            key = self._generate_pattern_key(pattern.recurrence_formula)
            self.pattern_cache[key] = pattern
    
    def analyze_with_dp(self, node) -> ComplexityResult:
        """
        Método principal de análisis mediante optimización de Programación Dinámica (PD).

        Estrategia PD:
        1. Verificar primero la caché de memorización (subproblemas superpuestos).
        2. Si no está en caché, realizar análisis con reconocimiento de patrones.
        3. Almacenar el resultado en caché para uso futuro.
        4. Utilizar la subestructura óptima para generar análisis complejos.
        """
        
        # Generar clave única para memorización
        node_key = self._generate_node_key(node)
        
        # Verificar caché primero (memorización PD)
        if node_key in self.analysis_cache:
            self.cache_hits += 1
            return self.analysis_cache[node_key]
        
        self.cache_misses += 1
        
        # Compruebe si esta es una función recursiva para un manejo especial
        if isinstance(node, Function):
            recursive_analysis = self.recursive_analyzer.analyze_recursive_algorithm(node)
            
            if recursive_analysis['has_recursion']:
                # Utilice análisis recursivo especializado
                result = self._analyze_recursive_function(node, recursive_analysis)
            else:
                # Utilice análisis estándar
                result = self.base_analyzer.analyze(node)
        else:
            # Análisis estándar para nodos que no son funciones
            result = self.base_analyzer.analyze(node)
        
        # Almacenar en caché (memorización PD)
        self.analysis_cache[node_key] = result
        return result
    
    def analyze_with_recurrence_tree(self, node, max_levels: int = 4) -> Tuple[ComplexityResult, Optional[RecurrenceTree]]:
        """
        Analiza la complejidad utilizando tanto la caché de PD como la visualización del árbol de recurrencia.
        
        Returns:
            Tupla de (complexity_result, recurrence_tree)
        """
        
        # Obtener análisis estándar de PD
        complexity_result = self.analyze_with_dp(node)
        
        # Intentar construir el árbol de recurrencia si esta es una función recursiva
        if isinstance(node, Function):
            recursive_analysis = self.recursive_analyzer.analyze_recursive_algorithm(node)
            
            if recursive_analysis['has_recursion'] and recursive_analysis['recurrence_relation']:
                # Construir el árbol de recurrencia
                recurrence_tree = self.tree_builder.build_tree(
                    recursive_analysis['recurrence_relation'], 
                    max_levels
                )
                
                # Actualizar resultado de complejidad con información del árbol si es más preciso
                tree_complexity = recurrence_tree.get_total_work()
                if tree_complexity and tree_complexity != "O(1)":
                    # Utilice la complejidad derivada del árbol si es más específica
                    complexity_result.big_o = tree_complexity
                
                return complexity_result, recurrence_tree
        
        # Manejar nodos de Programa - encontrar y analizar funciones recursivas
        elif isinstance(node, Program) and hasattr(node, 'functions'):
            for function in node.functions:
                if isinstance(function, Function):
                    recursive_analysis = self.recursive_analyzer.analyze_recursive_algorithm(function)
                    
                    if recursive_analysis['has_recursion'] and recursive_analysis['recurrence_relation']:
                        # Construir el árbol de recurrencia para la primera función recursiva encontrada
                        recurrence_tree = self.tree_builder.build_tree(
                            recursive_analysis['recurrence_relation'], 
                            max_levels
                        )
                        
                        # Actualizar resultado de complejidad con información del árbol si es más preciso
                        tree_complexity = recurrence_tree.get_total_work()
                        if tree_complexity and tree_complexity != "O(1)":
                            # Utilice la complejidad derivada del árbol si es más específica
                            complexity_result.big_o = tree_complexity
                        
                        return complexity_result, recurrence_tree
        
        return complexity_result, None
    
    def generate_recurrence_report(self, node) -> str:
        """Generar un informe completo que incluya el análisis del árbol de recurrencia."""
        
        complexity_result, recurrence_tree = self.analyze_with_recurrence_tree(node)
        
        report = []
        report.append("🌳 INFORME DE ANÁLISIS DEL ÁRBOL DE RECURRENCIA")
        report.append("=" * 50)
        
        report.append(f"\n📊 Análisis de Complejidad:")
        report.append(f"   Big O (peor caso): {complexity_result.big_o}")
        report.append(f"   Omega (mejor caso): {complexity_result.omega}")
        report.append(f"   Theta (cota ajustada): {complexity_result.theta}")
        
        if recurrence_tree:
            report.append(f"\n🌳 Árbol de Recurrencia:")
            report.append(recurrence_tree.get_level_summary())
            report.append(f"\n📈 Visualización del Árbol:")
            report.append(self.visualizer.visualize(recurrence_tree))
        else:
            report.append(f"\n⚠️  No se detectó un patrón de recurrencia - probablemente un algoritmo no recursivo")
        
        # Agregar estadísticas de DP
        stats = self.get_dp_statistics()
        report.append(f"\n🧠 Estadísticas de Caché DP:")
        report.append(f"   Acertijos de caché: {stats['cache_hits']}")
        report.append(f"   Fallos de caché: {stats['cache_misses']}")
        report.append(f"   Tasa de aciertos: {stats['hit_rate_percentage']}%")
        
        return "\n".join(report)
    
    def _analyze_recursive_function(self, function_node: Function, recursive_analysis: Dict) -> ComplexityResult:
        """Analizar una función recursiva con optimización DP."""
        
        # Obtener análisis base
        base_result = self.base_analyzer.analyze_complexity(function_node)
        
        # Intentar mejorar con reconocimiento de patrón de recurrencia
        if recursive_analysis['recurrence_relation']:
            pattern = self._find_matching_pattern(recursive_analysis['recurrence_relation'])
            
            if pattern:
                # Usar solución basada en patrón
                self.patterns_recognized += 1
                estimated_complexity = self.solver.get_closed_form_solution(pattern)
                
                # Actualizar resultado con mejor estimación
                base_result.big_o = estimated_complexity
                base_result.theta = estimated_complexity
        
        return base_result
    
    def _find_matching_pattern(self, recurrence_relation: str) -> Optional[RecurrencePattern]:
        """Buscar patrón coincidente en la base de datos de patrones DP."""
        
        for pattern in self.pattern_cache.values():
            if pattern.matches_formula(recurrence_relation):
                return pattern
        
        return None
    
    def _generate_node_key(self, node) -> str:
        """Generar clave única para la memoización del nodo."""
        
        # Crear un hash basado en el tipo de nodo y atributos clave
        key_data = {
            'type': type(node).__name__,
            'content': str(node)[:100]  # Limitar longitud
        }
        
        # Agregar atributos específicos según el tipo de nodo
        if hasattr(node, 'name'):
            key_data['name'] = node.name
        
        if hasattr(node, 'body') and node.body:
            key_data['body_length'] = len(node.body)
        
        # Generar hash
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _generate_pattern_key(self, formula: str) -> str:
        """Generar clave para el almacenamiento en caché de patrones."""
        return hashlib.md5(formula.encode()).hexdigest()
    
    def get_dp_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas completas de rendimiento de DP."""
        
        total_accesses = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_accesses * 100) if total_accesses > 0 else 0
        
        return {
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'total_cache_accesses': total_accesses,
            'hit_rate_percentage': round(hit_rate, 2),
            'cache_size': len(self.analysis_cache),
            'patterns_recognized': self.patterns_recognized,
            'known_patterns': len(self.pattern_cache),
            'tree_cache_size': self.tree_builder.get_cache_size(),
            'recursive_analysis_cache': len(self.recursive_analyzer.analysis_cache)
        }
    
    def clear_cache(self):
        """Clear all caches for fresh analysis."""
        self.analysis_cache.clear()
        self.tree_builder.clear_cache()
        self.recursive_analyzer.analysis_cache.clear()
        self.cache_hits = 0
        self.cache_misses = 0
        self.patterns_recognized = 0
    
    def get_optimization_recommendations(self, node) -> List[str]:
        """Obtener recomendaciones para optimizar el algoritmo analizado."""
        
        recommendations = []
        
        # Analizar con árbol de recurrencia
        complexity_result, recurrence_tree = self.analyze_with_recurrence_tree(node)
        
        # Verificar patrones de complejidad
        if "2^n" in complexity_result.big_o:
            recommendations.append("Complejidad exponencial detectada - considerar memoización u optimización DP")
        
        if "n^2" in complexity_result.big_o:
            recommendations.append("Complejidad cuadrática detectada - buscar optimizaciones en bucles anidados")
        
        if recurrence_tree and recurrence_tree.pattern_type == 'exponential':
            recommendations.append("Patrón de recurrencia exponencial - candidato ideal para memoización DP")
        
        # Verificar eficiencia de caché
        stats = self.get_dp_statistics()
        if stats['hit_rate_percentage'] < 50:
            recommendations.append("Baja tasa de aciertos en caché - considerar reestructuración para mejor optimización DP")
        
        if not recommendations:
            recommendations.append("El algoritmo parece estar bien optimizado para el análisis actual")
        
        return recommendations