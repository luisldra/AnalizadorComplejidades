"""
Recurrence Solver
================

This module is responsible for solving recurrence relations using Dynamic Programming.
Following SRP, this module focuses solely on mathematical solving logic.

Classes:
- RecurrenceSolver: Solves recurrence relations using DP techniques
- RecursiveAlgorithmAnalyzer: Analyzes recursive algorithms for patterns
"""

from typing import Dict, List, Optional, Any
from functools import lru_cache
from src.analyzer.recurrence_models import RecurrencePattern
from src.ast.nodes import *
from src.analyzer.advanced_complexity import ComplexityResult


class RecurrenceSolver:
    """
    Solves recurrence relations using Dynamic Programming techniques.
    
    Responsibility: Mathematical solving of recurrence relations.
    """
    
    @lru_cache(maxsize=1000)  # DP memoization decorator
    def solve_recurrence(self, formula: str, n: int) -> int:
        """
        Solve recurrence relation for specific value using DP.
        
        This is a simplified solver that demonstrates DP principles.
        A full implementation would parse mathematical expressions.
        """
        
        # Base cases (DP foundation)
        if n <= 1:
            return 1
        
        # Pattern-based solutions (DP table lookup)
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
        Get closed-form solution for a recurrence pattern.
        
        This uses DP principles to look up known solutions.
        """
        
        # Known solutions database (DP table)
        known_solutions = {
            "T(n) = T(n-1) + O(1)": "O(n)",
            "T(n) = 2T(n-1) + O(1)": "O(2^n)",
            "T(n) = T(n-1) + T(n-2) + O(1)": "O(φ^n)",  # Fibonacci
            "T(n) = 2T(n/2) + O(n)": "O(n log n)",
            "T(n) = 2T(n/2) + O(1)": "O(n)",
            "T(n) = T(n/2) + O(1)": "O(log n)"
        }
        
        # Direct lookup
        if pattern.recurrence_formula in known_solutions:
            return known_solutions[pattern.recurrence_formula]
        
        # Pattern matching for variations
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
    Analyzes recursive algorithms to identify patterns and derive recurrence relations.
    
    Responsibility: Analysis of recursive algorithm structures.
    """
    
    def __init__(self):
        self.solver = RecurrenceSolver()
        self.analysis_cache: Dict[str, Dict] = {}
    
    def analyze_recursive_algorithm(self, function_node: Function) -> Dict[str, Any]:
        """
        Analyze a recursive function to identify its recurrence pattern.
        
        Returns comprehensive analysis including:
        - Recursive call patterns
        - Work done per call
        - Derived recurrence relation
        - Complexity estimation
        """
        
        # Generate cache key
        func_key = self._generate_function_key(function_node)
        
        # Check cache first
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
        
        # Find recursive calls and detect mutually exclusive branches
        recursive_calls = self._find_recursive_calls(function_node)
        exclusive_calls = self._has_mutually_exclusive_recursive_returns(function_node)
        
        if recursive_calls:
            analysis['has_recursion'] = True
            analysis['recursive_calls'] = recursive_calls
            
            # Analyze the pattern
            pattern_analysis = self._analyze_call_pattern(recursive_calls, exclusive_calls)
            analysis.update(pattern_analysis)
            
            # Derive recurrence relation
            relation = self._derive_recurrence_relation(function_node, recursive_calls, exclusive_calls)
            analysis['recurrence_relation'] = relation
            
            # Estimate complexity
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
    
    def _find_recursive_calls(self, function_node: Function) -> List[Dict[str, Any]]:
        """Find all recursive calls in a function."""
        
        recursive_calls = []
        
        def traverse(node, depth=0):
            if node is None:
                return
                
            # Check if this is a recursive call
            if isinstance(node, Call):
                call_name = None
                if hasattr(node.name, 'name'):  # node.name is a Var object
                    call_name = node.name.name
                elif isinstance(node.name, str):  # node.name is a string
                    call_name = node.name
                
                if call_name == function_node.name:
                    # Found recursive call
                    call_info = {
                        'depth': depth,
                        'arguments': len(node.args) if hasattr(node, 'args') and node.args else 0,
                        'location': f"depth_{depth}",
                        'node': node
                    }
                    recursive_calls.append(call_info)
            
            # Handle specific node types systematically
            if isinstance(node, Function):
                if hasattr(node, 'body') and node.body:
                    for stmt in node.body:
                        traverse(stmt, depth + 1)
            
            elif isinstance(node, If):
                # Traverse condition
                traverse(node.condition, depth + 1)
                # Traverse then_body
                if hasattr(node, 'then_body') and node.then_body:
                    if isinstance(node.then_body, list):
                        for stmt in node.then_body:
                            traverse(stmt, depth + 1)
                    else:
                        traverse(node.then_body, depth + 1)
                # Traverse else_body
                if hasattr(node, 'else_body') and node.else_body:
                    if isinstance(node.else_body, list):
                        for stmt in node.else_body:
                            traverse(stmt, depth + 1)
                    else:
                        traverse(node.else_body, depth + 1)
            
            elif isinstance(node, (While, For, Repeat)):
                if hasattr(node, 'body') and node.body:
                    for stmt in node.body:
                        traverse(stmt, depth + 1)
                if hasattr(node, 'condition'):
                    traverse(node.condition, depth + 1)
            
            elif isinstance(node, Return):
                if hasattr(node, 'expr') and node.expr:
                    traverse(node.expr, depth + 1)
                elif hasattr(node, 'value') and node.value:
                    traverse(node.value, depth + 1)
            
            elif isinstance(node, Assignment):
                if hasattr(node, 'value') and node.value:
                    traverse(node.value, depth + 1)
            
            elif isinstance(node, BinOp):
                traverse(node.left, depth + 1)
                traverse(node.right, depth + 1)
            
            elif isinstance(node, Call):
                # Already handled above for recursive calls
                if hasattr(node, 'args') and node.args:
                    for arg in node.args:
                        traverse(arg, depth + 1)
            
            elif isinstance(node, list):
                for item in node:
                    traverse(item, depth + 1)
        
        traverse(function_node)
        return recursive_calls
    
    def _analyze_call_pattern(self, recursive_calls: List[Dict[str, Any]], exclusive_branch_calls: bool = False) -> Dict[str, Any]:
        """Analyze the pattern of recursive calls based on argument structure."""
        
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
                return {'pattern_type': 'divide_conquer'}  # T(n) = T(n/2) + c
            else:
                return {'pattern_type': 'linear'}  # T(n) = T(n-1) + c
        
        elif num_calls == 2:
            if exclusive_branch_calls:
                return {'pattern_type': 'binary_exclusive'}
            if has_multiple_subtractions:
                # Fibonacci: T(n) = T(n-1) + T(n-2)
                return {'pattern_type': 'binary'}
            elif has_division:
                # Merge Sort: T(n) = 2T(n/2) + n
                return {'pattern_type': 'divide_conquer'}
            elif no_operators_in_args or has_mid_variable:
                # No hay operadores en argumentos - probablemente divide & conquer con variables
                # (como merge_sort que usa middle = (left + right) / 2)
                # Asumir divide_conquer para 2 llamadas sin decrementos obvios
                return {'pattern_type': 'divide_conquer'}
            else:
                # Otros casos binarios
                return {'pattern_type': 'binary'}
        
        else:
            return {'pattern_type': 'multiple', 'call_count': num_calls}
    
    def _derive_recurrence_relation(self, function_node: Function, recursive_calls: List[Dict[str, Any]], exclusive_branch_calls: bool) -> Optional[str]:
        """Derive recurrence relation from function structure."""
        
        if not recursive_calls:
            return None
        
        num_calls = len(recursive_calls)
        
        # Usar pattern analysis mejorado
        pattern_info = self._analyze_call_pattern(recursive_calls, exclusive_branch_calls)
        pattern_type = pattern_info.get('pattern_type', 'none')
        
        # Generar relación basada en el patrón detectado
        if pattern_type == 'linear':
            return "T(n) = T(n-1) + O(1)"
        elif pattern_type == 'binary':
            # Fibonacci pattern
            return "T(n) = T(n-1) + T(n-2) + O(1)"
        elif pattern_type == 'binary_exclusive':
            return "T(n) = T(n/2) + O(1)"
        elif pattern_type == 'divide_conquer':
            # Divide & Conquer pattern
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
        """Detects IF structures where each branch returns a recursive call."""
        if not hasattr(function_node, 'body') or not function_node.body:
            return False

        def traverse(node) -> bool:
            if isinstance(node, If):
                then_has = self._branch_has_recursive_return(node.then_body, function_node.name)
                else_has = self._branch_has_recursive_return(node.else_body, function_node.name)
                if then_has and else_has:
                    return True
                # Continue searching nested conditionals
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
        """Detects whether an argument references a midpoint helper variable."""
        if isinstance(arg, Var):
            return 'mid' in arg.name.lower()
        if isinstance(arg, BinOp):
            return self._argument_mentions_midpoint(arg.left) or self._argument_mentions_midpoint(arg.right)
        return False
    
    def _generate_function_key(self, function_node: Function) -> str:
        """Generate a unique key for function caching."""
        
        # Simple key based on function name and body structure
        key_parts = [function_node.name]
        
        # Add some structure information
        if hasattr(function_node, 'body'):
            key_parts.append(f"body_{len(function_node.body)}")
        
        return "_".join(key_parts)
    
    def get_analysis_statistics(self) -> Dict[str, Any]:
        """Get statistics about the analysis performed."""
        
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