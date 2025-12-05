"""
Solucionador de Recurrencia
================

Este módulo se encarga de resolver relaciones de recurrencia mediante Programación Dinámica.

Clases:
- Solucionador de Recurrencia: Resuelve relaciones de recurrencia mediante técnicas de Programación Dinámica.
- Analizador de Algoritmos Recursivos: Analiza algoritmos recursivos en busca de patrones.
"""

from typing import Dict, List, Optional, Any
from functools import lru_cache
from src.analyzer.recurrence_models import RecurrencePattern
from src.ast.nodes import *
from src.analyzer.advanced_complexity import ComplexityResult


class RecurrenceSolver:
    """
    Resuelve relaciones de recurrencia utilizando técnicas de Programación Dinámica.
    """
    
    @lru_cache(maxsize=1000)  # DP memoization decorator
    def solve_recurrence(self, formula: str, n: int) -> int:
        """
        Resolver relación de recurrencia para un valor específico usando DP.
        
        Este es un solucionador simplificado que demuestra principios de DP.
        Una implementación completa analizaría expresiones matemáticas.
        """
        
        # Casos base (fundamento de DP)
        if n <= 1:
            return 1
        
        # Soluciones basadas en patrones (tabla DP)
        if "T(n-1)" in formula and "2*T(n-1)" not in formula:
            # Linear recurrence: T(n) = T(n-1) + c
            return n  # O(n) solution
        
        elif "2*T(n-1)" in formula:
            # Exponential: T(n) = 2*T(n-1) + c
            return 2 ** n  # O(2^n) solution
        
        elif "T(n/2)" in formula:
            # Divide & conquer: T(n) = a*T(n/2) + f(n)
            import math
            return n * int(math.log2(n))  # O(n log n) approximation
        
        # Default case
        return n
    
    def get_closed_form_solution(self, pattern: RecurrencePattern) -> str:
        """
        Obtener la solución en forma cerrada para un patrón de recurrencia.
        
        Esto utiliza principios de DP para buscar soluciones conocidas.
        """
        
        # Base de datos de soluciones conocidas (tabla DP)
        known_solutions = {
            "T(n) = T(n-1) + O(1)": "O(n)",
            "T(n) = 2T(n-1) + O(1)": "O(2^n)",
            "T(n) = T(n-1) + T(n-2) + O(1)": "O(2^n)", 
            "T(n) = 2T(n/2) + O(n)": "O(n log n)",
            "T(n) = 2T(n/2) + O(1)": "O(n)",
            "T(n) = T(n/2) + O(1)": "O(log n)"
        }
        
        # Búsqueda directa
        if pattern.recurrence_formula in known_solutions:
            return known_solutions[pattern.recurrence_formula]
        
        # Coincidencia de patrones para variaciones
        formula = pattern.recurrence_formula.lower()
        
        if "t(n-1)" in formula and "2t(n-1)" not in formula:
            return "O(n)"
        elif "2t(n-1)" in formula or "t(n-1) + t(n-2)" in formula:
            return "O(2^n)"
        elif "t(n/2)" in formula and "+ o(n)" in formula:
            return "O(n log n)"
        elif "t(n/2)" in formula and "+ o(1)" in formula:
            return "O(n)"
        
        return pattern.solution  # Fallback to provided solution


class RecursiveAlgorithmAnalyzer:
    """
    Analiza algoritmos recursivos para identificar patrones y derivar relaciones de recurrencia.
    
    Responsabilidad: Análisis de estructuras de algoritmos recursivos.
    """
    
    def __init__(self):
        self.solver = RecurrenceSolver()
        self.analysis_cache: Dict[str, Dict] = {}
    
    def analyze_recursive_algorithm(self, function_node: Function) -> Dict[str, Any]:
        """
        Analiza una función recursiva para identificar su patrón de recurrencia.
        
        Devuelve un análisis completo que incluye:
        - Patrones de llamadas recursivas
        - Trabajo realizado por llamada
        - Relación de recurrencia derivada
        - Estimación de complejidad
        """
        
        # Generar clave de caché
        func_key = self._generate_function_key(function_node)
        
        # Verificar caché primero
        if func_key in self.analysis_cache:
            return self.analysis_cache[func_key]
        
        analysis = {
            'function_name': function_node.name,
            'has_recursion': False,
            'recursive_calls': [],
            'base_cases': [],
            'work_per_call': 'O(1)',
            'recurrence_relation': None,
            'estimated_complexity': 'O(1)',
            'pattern_type': 'none'
        }
        
        # Encontrar llamadas recursivas y detectar ramas mutuamente exclusivas
        recursive_calls = self._find_recursive_calls(function_node, function_node.name)
        exclusive_calls = self._has_mutually_exclusive_recursive_returns(function_node)
        
        if recursive_calls:
            analysis['has_recursion'] = True
            analysis['recursive_calls'] = recursive_calls
            
            # Analizar el patrón
            pattern_analysis = self._analyze_call_pattern(recursive_calls, exclusive_calls)
            analysis.update(pattern_analysis)
            
            # Derivar la relación de recurrencia
            relation = self._derive_recurrence_relation(function_node, recursive_calls, exclusive_calls)
            analysis['recurrence_relation'] = relation
            
            # Estimar la complejidad
            if relation:
                pattern = RecurrencePattern(
                    pattern_type=analysis['pattern_type'],
                    base_cases={},
                    recurrence_formula=relation,
                    solution='',
                    confidence=0.8
                )
                complexity = self.solver.get_closed_form_solution(pattern)
                analysis['estimated_complexity'] = complexity
        
        analysis['exclusive_branch_calls'] = exclusive_calls

        # Cache the result
        self.analysis_cache[func_key] = analysis
        return analysis
    
    def _find_recursive_calls(self, function_node, func_name):
        recursive_calls = []
        
        def traverse(node, depth=0):
            if node is None: return
                
            # 1. DETECCIÓN DIRECTA (Call)
            if isinstance(node, Call):
                call_name = None
                # Soporte para distintos tipos de nombres en el AST
                if hasattr(node, 'func_name'):
                     call_name = node.func_name.name if hasattr(node.func_name, 'name') else node.func_name
                elif hasattr(node, 'name'):
                    call_name = node.name.name if hasattr(node.name, 'name') else node.name
                
                if str(call_name) == str(func_name):
                    recursive_calls.append({
                        'depth': depth, 
                        'arguments': len(node.args) if hasattr(node, 'args') else 0,
                        'location': f"depth_{depth}", 
                        'node': node
                    })
            
            # 2. RECORRIDO (Visitor Pattern)
            
            # Listas
            if isinstance(node, list):
                for item in node: traverse(item, depth)
                
            # Estructuras con 'body' (Function, While, For)
            elif hasattr(node, 'body'):
                traverse(node.body, depth + 1)
                
            # Estructuras condicionales
            if isinstance(node, If):
                traverse(getattr(node, 'condition', None), depth)
                traverse(getattr(node, 'then_body', None), depth + 1)
                traverse(getattr(node, 'else_body', None), depth + 1)
            
            # Retornos 
            elif isinstance(node, Return):
                # Tu parser usa 'expr', otros usan 'value'. Buscamos ambos.
                traverse(getattr(node, 'expr', None), depth)
                traverse(getattr(node, 'value', None), depth)
            
            # Asignaciones
            elif isinstance(node, Assignment):
                # Tu parser usa 'expr', otros usan 'value'. Buscamos ambos.
                traverse(getattr(node, 'expr', None), depth)
                traverse(getattr(node, 'value', None), depth)
            
            # Operaciones Binarias
            elif isinstance(node, BinOp):
                traverse(node.left, depth)
                traverse(node.right, depth)
                
            # Argumentos de llamadas
            elif isinstance(node, Call):
                if hasattr(node, 'args'):
                    for arg in node.args: traverse(arg, depth)

        traverse(function_node)
        return recursive_calls
    
    def _analyze_call_pattern(self, recursive_calls: List[Dict[str, Any]], exclusive_branch_calls: bool = False) -> Dict[str, Any]:
        """Analizar el patrón de llamadas recursivas basado en la estructura de argumentos."""
        
        num_calls = len(recursive_calls)
        
        if num_calls == 0:
            return {'pattern_type': 'none'}
        
        # Analizar estructura de argumentos de las llamadas recursivas
        has_division = False      # n/2, n/k (división)
        has_subtraction = False   # n-1, n-2 (resta)
        has_multiple_subtractions = False  # n-1 Y n-2 (Fibonacci pattern)
        has_mid_variable = False  # uso explícito de midpoint
        
        subtraction_values = []
        
        for call_info in recursive_calls:
            call_node = call_info.get('node')
            if not call_node or not hasattr(call_node, 'args'):
                continue
                
            for arg in call_node.args:
                # Detectar división (n/2, n/k)
                if hasattr(arg, 'op') and arg.op == '/':
                    has_division = True
                
                # Detectar resta (n-1, n-2, etc.)
                elif hasattr(arg, 'op') and arg.op == '-':
                    has_subtraction = True
                    if hasattr(arg, 'right') and hasattr(arg.right, 'value'):
                        subtraction_values.append(arg.right.value)
                
                if self._argument_mentions_midpoint(arg):
                    has_mid_variable = True
        
        # Detectar patrón Fibonacci: múltiples restas con valores diferentes (n-1, n-2)
        if len(subtraction_values) >= 2:
            unique_subtractions = len(set(subtraction_values))
            if unique_subtractions >= 2:
                has_multiple_subtractions = True
        
        # IMPORTANTE: Si hay 2 llamadas pero NO hay operadores en argumentos,
        # puede ser divide & conquer con variables (como merge_sort que usa middle)
        no_operators_in_args = not has_division and not has_subtraction
        
        # Clasificar patrón basado en estructura de argumentos
        if num_calls == 1:
            if has_division:
                return {'pattern_type': 'divide_conquer', 'has_division': has_division, 'has_subtraction': has_subtraction, 'has_multiple_subtractions': has_multiple_subtractions}
            else:
                return {'pattern_type': 'linear', 'has_division': has_division, 'has_subtraction': has_subtraction, 'has_multiple_subtractions': has_multiple_subtractions}
        
        elif num_calls == 2:
            if exclusive_branch_calls:
                return {'pattern_type': 'binary_exclusive', 'has_division': has_division, 'has_subtraction': has_subtraction, 'has_multiple_subtractions': has_multiple_subtractions}
            if has_multiple_subtractions:
                # Fibonacci: T(n) = T(n-1) + T(n-2)
                return {'pattern_type': 'binary', 'has_division': has_division, 'has_subtraction': has_subtraction, 'has_multiple_subtractions': has_multiple_subtractions}
            elif has_division:
                # Merge Sort: T(n) = 2T(n/2) + n
                return {'pattern_type': 'divide_conquer', 'has_division': has_division, 'has_subtraction': has_subtraction, 'has_multiple_subtractions': has_multiple_subtractions}
            elif no_operators_in_args or has_mid_variable:
                # No hay operadores en argumentos - probablemente divide & conquer con variables
                # (como merge_sort que usa middle = (left + right) / 2)
                # Asumir divide_conquer para 2 llamadas sin decrementos obvios
                return {'pattern_type': 'divide_conquer', 'has_division': has_division, 'has_subtraction': has_subtraction, 'has_multiple_subtractions': has_multiple_subtractions}
            else:
                # Con dos llamadas y restas iguales (e.g. quick_sort con pi-1 y pi+1) asumimos divide & conquer
                return {'pattern_type': 'divide_conquer', 'has_division': has_division, 'has_subtraction': has_subtraction, 'has_multiple_subtractions': has_multiple_subtractions}
        
        else:
            return {'pattern_type': 'multiple', 'call_count': num_calls, 'has_division': has_division, 'has_subtraction': has_subtraction, 'has_multiple_subtractions': has_multiple_subtractions}
    
    def _derive_recurrence_relation(self, function_node: Function, recursive_calls: List[Dict[str, Any]], exclusive_branch_calls: bool) -> Optional[str]:
        """Derivar la relación de recurrencia a partir de la estructura de la función."""
        
        if not recursive_calls:
            return None
        
        # Si las llamadas recursivas están en ramas mutuamente exclusivas (p.ej. búsqueda binaria),
        # sólo se ejecuta una llamada por nivel: T(n) = T(n/2) + O(1)
        if exclusive_branch_calls:
            return "T(n) = T(n/2) + O(1)"

        num_calls = len(recursive_calls)
        
        # Usar análisis de patrones mejorado
        pattern_info = self._analyze_call_pattern(recursive_calls, exclusive_branch_calls)
        pattern_type = pattern_info.get('pattern_type', 'none')
        has_division = pattern_info.get('has_division', False)
        has_subtraction = pattern_info.get('has_subtraction', False)
        has_multiple_subtractions = pattern_info.get('has_multiple_subtractions', False)
        uses_size_param = self._calls_use_size_param(recursive_calls, function_node)
        
        # Generar relación basada en el patrón detectado
        if pattern_type == 'linear':
            return "T(n) = T(n-1) + O(1)"
        elif pattern_type == 'binary':
            # Si no hay restas múltiples ni división, asumimos ramas exclusivas (ej. búsqueda binaria) -> 1 llamada por nivel
            if not has_multiple_subtractions:
                # trabajo adicional lineal si no se detecta otra cosa
                return "T(n) = T(n/2) + O(n)"
            return "T(n) = T(n-1) + T(n-2) + O(1)"
        elif pattern_type == 'binary_exclusive':
            return "T(n) = T(n/2) + O(1)"
        elif pattern_type == 'divide_conquer':
            # Divide & Conquer pattern
            # Caso especial: dos llamadas con n-1 (torres de Hanoi) -> exponencial
            if num_calls == 2 and has_subtraction and not has_division and uses_size_param:
                return "T(n) = 2T(n-1) + O(1)"
            if num_calls == 1:
                return "T(n) = T(n/2) + O(1)"
            elif num_calls == 2:
                return "T(n) = 2T(n/2) + O(n)"
            else:
                return f"T(n) = {num_calls}T(n/{num_calls}) + O(n)"
        elif pattern_type == 'multiple':
            call_count = pattern_info.get('call_count', num_calls)
            return f"T(n) = {call_count}T(n-1) + O(1)"
        else:
            # Fallback genérico
            if num_calls == 1:
                return "T(n) = T(n-1) + O(1)"
            else:
                return f"T(n) = {num_calls}T(n-1) + O(1)"

    def _has_mutually_exclusive_recursive_returns(self, function_node: Function) -> bool:
        """Detecta estructuras IF donde cada rama retorna una llamada recursiva."""
        if not hasattr(function_node, 'body') or not function_node.body:
            return False

        def traverse(node) -> bool:
            if isinstance(node, If):
                then_has = self._branch_has_recursive_return(node.then_body, function_node.name)
                else_has = self._branch_has_recursive_return(node.else_body, function_node.name)
                if then_has and else_has:
                    return True
                # Continuar buscando condicionales anidados
                nested_then = node.then_body if isinstance(node.then_body, list) else ([node.then_body] if node.then_body else [])
                nested_else = node.else_body if isinstance(node.else_body, list) else ([node.else_body] if node.else_body else [])
                for branch in nested_then:
                    if traverse(branch):
                        return True
                for branch in nested_else:
                    if traverse(branch):
                        return True
            elif isinstance(node, list):
                for stmt in node:
                    if traverse(stmt):
                        return True
            elif hasattr(node, 'body'):
                for stmt in node.body:
                    if traverse(stmt):
                        return True
            return False

        for stmt in function_node.body:
            if traverse(stmt):
                return True
        return False

    def _branch_has_recursive_return(self, block, func_name: str) -> bool:
        if not block:
            return False
        nodes = block if isinstance(block, list) else [block]
        for node in nodes:
            if self._node_contains_recursive_return(node, func_name):
                return True
        return False

    def _node_contains_recursive_return(self, node, func_name: str) -> bool:
        if node is None:
            return False

        if isinstance(node, Return):
            expr = getattr(node, 'expr', getattr(node, 'value', None))
            if self._is_recursive_call(expr, func_name):
                return True

        if isinstance(node, If):
            return (
                self._branch_has_recursive_return(node.then_body, func_name) or
                self._branch_has_recursive_return(node.else_body, func_name)
            )

        if hasattr(node, 'body') and node.body:
            for stmt in node.body:
                if self._node_contains_recursive_return(stmt, func_name):
                    return True

        if hasattr(node, 'expr') and self._is_recursive_call(node.expr, func_name):
            return True

        return False

    def _is_recursive_call(self, expr, func_name: str) -> bool:
        if not isinstance(expr, Call):
            return False
        call_name = expr.name.name if hasattr(expr.name, 'name') else expr.name
        return call_name == func_name

    def _argument_mentions_midpoint(self, arg) -> bool:
        """Detecta si un argumento hace referencia a una variable auxiliar de punto medio."""
        if isinstance(arg, Var):
            return 'mid' in arg.name.lower()
        if isinstance(arg, BinOp):
            return self._argument_mentions_midpoint(arg.left) or self._argument_mentions_midpoint(arg.right)
        return False

    def _calls_use_size_param(self, recursive_calls: List[Dict[str, Any]], function_node: Function) -> bool:
        """Detecta si las llamadas recursivas restan sobre el parametro de tamano (e.g., n-1)."""
        param_names = []
        try:
            param_names = [str(p.name if hasattr(p, 'name') else p) for p in getattr(function_node, 'params', [])]
        except Exception:
            param_names = []

        for info in recursive_calls:
            call_node = info.get('node')
            if not call_node or not hasattr(call_node, 'args'):
                continue
            for arg in call_node.args:
                if isinstance(arg, BinOp) and getattr(arg, 'op', None) == '-':
                    if isinstance(arg.left, Var):
                        left_name = str(getattr(arg.left, 'name', '')).lower()
                        if left_name in [p.lower() for p in param_names] or left_name == 'n':
                            return True
        return False
    
    def _generate_function_key(self, function_node: Function) -> str:
        """Genera una clave única para el almacenamiento en caché de funciones."""
        
        # Clave simple basada en el nombre de la función y la estructura del cuerpo
        key_parts = [function_node.name]
        
        # Agregar información de estructura
        if hasattr(function_node, 'body'):
            key_parts.append(f"body_{len(function_node.body)}")
        
        return "_".join(key_parts)
    
    def get_analysis_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas sobre el análisis realizado."""
        
        total_analyzed = len(self.analysis_cache)
        recursive_functions = sum(1 for analysis in self.analysis_cache.values() 
                                if analysis['has_recursion'])
        
        pattern_types = {}
        for analysis in self.analysis_cache.values():
            pattern = analysis['pattern_type']
            pattern_types[pattern] = pattern_types.get(pattern, 0) + 1
        
        return {
            'total_functions_analyzed': total_analyzed,
            'recursive_functions_found': recursive_functions,
            'pattern_distribution': pattern_types,
            'cache_size': total_analyzed
        }
