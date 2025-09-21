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
        
        # Find recursive calls
        recursive_calls = self._find_recursive_calls(function_node)
        
        if recursive_calls:
            analysis['has_recursion'] = True
            analysis['recursive_calls'] = recursive_calls
            
            # Analyze the pattern
            pattern_analysis = self._analyze_call_pattern(recursive_calls)
            analysis.update(pattern_analysis)
            
            # Derive recurrence relation
            relation = self._derive_recurrence_relation(function_node, recursive_calls)
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
    
    def _analyze_call_pattern(self, recursive_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the pattern of recursive calls."""
        
        num_calls = len(recursive_calls)
        
        if num_calls == 0:
            return {'pattern_type': 'none'}
        elif num_calls == 1:
            return {'pattern_type': 'linear'}
        elif num_calls == 2:
            return {'pattern_type': 'binary'}
        else:
            return {'pattern_type': 'multiple', 'call_count': num_calls}
    
    def _derive_recurrence_relation(self, function_node: Function, recursive_calls: List[Dict[str, Any]]) -> Optional[str]:
        """Derive recurrence relation from function structure."""
        
        if not recursive_calls:
            return None
        
        num_calls = len(recursive_calls)
        
        # Simple heuristics based on call patterns
        if num_calls == 1:
            return "T(n) = T(n-1) + O(1)"
        elif num_calls == 2:
            # Could be divide & conquer or binary recursion
            # Simple heuristic: assume binary recursion for now
            return "T(n) = T(n-1) + T(n-2) + O(1)"
        else:
            return f"T(n) = {num_calls}T(n-1) + O(1)"
    
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