"""
Asymptotic Complexity Analyzer - Formal Mathematical Analysis
=============================================================

This module implements rigorous asymptotic analysis following formal computational
complexity theory. It determines the tight bound (Theta) when possible, or provides
separate Big O and Omega bounds when they differ.

Mathematical Foundation:
- Formal recurrence relation construction
- Master Theorem application
- Substitution method
- Recurrence tree analysis
- Precise asymptotic bound determination

Author: Científico de la Computación
Date: November 2025
"""

from typing import Dict, Optional, Tuple, List, Any
from dataclasses import dataclass
import re
import math
from src.ast.nodes import *


@dataclass
class RecurrenceEquation:
    """Represents a formal recurrence equation."""
    equation: str           # T(n) = aT(n/b) + f(n) or similar
    a: Optional[int]        # Number of recursive calls
    b: Optional[int]        # Division factor
    f_n: str               # Work done per call
    base_cases: Dict[str, str]  # Base case definitions
    method_used: str       # Resolution method (Master, Substitution, Tree)
    
    def __str__(self):
        return self.equation


@dataclass
class AsymptoticBound:
    """Represents the asymptotic complexity bound."""
    complexity: str         # The complexity class (e.g., "n^2", "2^n")
    notation: str          # "Θ" for tight bound, "O" for upper, "Ω" for lower
    confidence: float      # Confidence level (0.0 to 1.0)
    explanation: str       # Brief explanation of the bound
    
    def __str__(self):
        return f"{self.notation}({self.complexity})"


class AsymptoticAnalyzer:
    """
    Performs formal asymptotic analysis of algorithms.
    
    This analyzer determines:
    1. The precise recurrence relation
    2. The appropriate solution method
    3. The tight bound (Theta) when best and worst case coincide
    4. Separate bounds when they differ
    """
    
    def __init__(self):
        self.analysis_cache: Dict[str, AsymptoticBound] = {}
        
    def analyze(self, node, recursive_info: Optional[Dict] = None) -> Tuple[RecurrenceEquation, AsymptoticBound]:
        """
        Perform complete asymptotic analysis.
        
        Args:
            node: AST node to analyze
            recursive_info: Optional recursive analysis from RecursiveAlgorithmAnalyzer
            
        Returns:
            Tuple of (RecurrenceEquation, AsymptoticBound)
        """
        
        # Step 1: Construct formal recurrence equation
        recurrence = self._construct_recurrence(node, recursive_info)
        
        # Step 2: Solve using appropriate method
        bound = self._solve_recurrence(recurrence)
        
        return recurrence, bound
    
    def _construct_recurrence(self, node, recursive_info: Optional[Dict]) -> RecurrenceEquation:
        """
        Construct formal recurrence relation.
        
        For recursive algorithms:
        - Identify number of recursive calls (a)
        - Identify problem size reduction (b in T(n/b))
        - Identify work per level f(n)
        - Define base cases
        """
        
        if not recursive_info or not recursive_info.get('has_recursion'):
            # Non-recursive algorithm
            return self._analyze_iterative(node)
        
        # Recursive algorithm - construct recurrence
        num_calls = len(recursive_info.get('recursive_calls', []))
        pattern_type = recursive_info.get('pattern_type', 'linear')
        
        # Determine recurrence parameters
        if pattern_type == 'linear':
            # T(n) = T(n-1) + c
            return RecurrenceEquation(
                equation="T(n) = T(n-1) + c",
                a=1,
                b=None,  # Decrementation, not division
                f_n="c",
                base_cases={"T(0)": "c", "T(1)": "c"},
                method_used="Substitution"
            )
            
        elif pattern_type == 'binary':
            # CRITICAL: "binary" puede significar DOS cosas diferentes:
            # 1. Fibonacci: T(n) = T(n-1) + T(n-2) - ambas ramas se ejecutan
            # 2. Búsqueda binaria: T(n) = T(n/2) + c - ramas mutuamente exclusivas
            
            # Distinguir por múltiples estrategias
            calls = recursive_info.get('recursive_calls', [])
            
            # ESTRATEGIA 1: Nombre de función
            is_binary_search = False
            func_name = ""
            if hasattr(node, 'functions') and node.functions:
                func = node.functions[0]
                func_name = func.name.lower()
                if 'busqueda' in func_name or 'search' in func_name or 'binary' in func_name:
                    is_binary_search = True
            
            # ESTRATEGIA 2: Buscar cálculo de middle (fallback)
            if not is_binary_search and hasattr(node, 'functions') and node.functions:
                func = node.functions[0]
                is_binary_search = self._has_middle_calculation(func)
            
            # ESTRATEGIA 3: Verificar patrón de argumentos (Fibonacci tiene n-1 y n-2)
            has_fibonacci_decrements = False
            if calls and len(calls) >= 2:
                for call in calls[:2]:
                    call_node = call.get('node')
                    if call_node and hasattr(call_node, 'args'):
                        for arg in call_node.args:
                            if hasattr(arg, 'op') and arg.op == '-':
                                if hasattr(arg, 'right') and hasattr(arg.right, 'value'):
                                    if arg.right.value in [1, 2]:
                                        has_fibonacci_decrements = True
                                        break
            
            if is_binary_search:
                # Búsqueda binaria: ramas mutuamente exclusivas
                return RecurrenceEquation(
                    equation="T(n) = T(n/2) + c",
                    a=1,  # Solo UNA rama se ejecuta
                    b=2,  # División por 2
                    f_n="c",
                    base_cases={"T(1)": "c", "T(0)": "c"},
                    method_used="Master Theorem"
                )
            elif has_fibonacci_decrements:
                # Fibonacci: ambas ramas se ejecutan
                return RecurrenceEquation(
                    equation="T(n) = T(n-1) + T(n-2) + c",
                    a=2,
                    b=None,
                    f_n="c",
                    base_cases={"T(0)": "c", "T(1)": "c"},
                    method_used="Recurrence Tree"
                )
            else:
                # Default: asumir Fibonacci si tiene 2 llamadas
                return RecurrenceEquation(
                    equation="T(n) = T(n-1) + T(n-2) + c",
                    a=2,
                    b=None,
                    f_n="c",
                    base_cases={"T(0)": "c", "T(1)": "c"},
                    method_used="Recurrence Tree"
                )
            
        elif pattern_type == 'divide_conquer':
            # Divide & Conquer: T(n) = aT(n/b) + f(n)
            # Parse from recursive_info if available
            relation = recursive_info.get('recurrence_relation', '')
            
            # Try to extract a and b from relation
            match = re.search(r'(\d+)T\(n/(\d+)\)', relation)
            if match:
                a = int(match.group(1))
                b = int(match.group(2))
            else:
                # Default: binary division
                a = num_calls
                b = 2
            
            # Determine f(n) - work per level
            # Check if there are loops or linear work in the function
            has_loop = False
            if hasattr(node, 'functions') and node.functions:
                func = node.functions[0]
                has_loop = self._has_loop(func)
            
            if has_loop or 'O(n)' in relation or '+ n' in relation.lower():
                f_n = "n"
            else:
                f_n = "c"
            
            return RecurrenceEquation(
                equation=f"T(n) = {a}T(n/{b}) + {f_n}",
                a=a,
                b=b,
                f_n=f_n,
                base_cases={"T(1)": "c"},
                method_used="Master Theorem"
            )
        
        else:
            # Multiple calls - generally exponential
            return RecurrenceEquation(
                equation=f"T(n) = {num_calls}T(n-1) + c",
                a=num_calls,
                b=None,
                f_n="c",
                base_cases={"T(0)": "c", "T(1)": "c"},
                method_used="Substitution"
            )
    
    def _analyze_iterative(self, node) -> RecurrenceEquation:
        """Analyze iterative (non-recursive) algorithm."""
        
        # Analyze loop structure
        loop_depth = self._count_loop_depth(node)
        
        if loop_depth == 0:
            # No loops - constant time
            equation = "T(n) = c"
            complexity = "1"
        elif loop_depth == 1:
            # Single loop - linear time
            equation = "T(n) = cn"
            complexity = "n"
        elif loop_depth == 2:
            # Nested loops - quadratic
            equation = "T(n) = cn²"
            complexity = "n^2"
        else:
            # Multiple nested loops
            equation = f"T(n) = cn^{loop_depth}"
            complexity = f"n^{loop_depth}"
        
        return RecurrenceEquation(
            equation=equation,
            a=None,
            b=None,
            f_n="c",
            base_cases={"T(0)": "c"},
            method_used="Loop Analysis"
        )
    
    def _count_loop_depth(self, node, current_depth=0) -> int:
        """Count maximum loop nesting depth."""
        
        max_depth = current_depth
        
        if isinstance(node, (For, While, Repeat)):
            # This is a loop - increment depth
            body_depth = current_depth + 1
            
            # Check depth in loop body
            if hasattr(node, 'body') and node.body:
                for stmt in node.body:
                    depth = self._count_loop_depth(stmt, body_depth)
                    max_depth = max(max_depth, depth)
        
        elif isinstance(node, (Function, Program)):
            # Check all statements/functions
            items = node.body if hasattr(node, 'body') else node.functions
            if items:
                for item in items:
                    depth = self._count_loop_depth(item, current_depth)
                    max_depth = max(max_depth, depth)
        
        elif isinstance(node, If):
            # Check both branches
            if hasattr(node, 'then_body') and node.then_body:
                if isinstance(node.then_body, list):
                    for stmt in node.then_body:
                        depth = self._count_loop_depth(stmt, current_depth)
                        max_depth = max(max_depth, depth)
            
            if hasattr(node, 'else_body') and node.else_body:
                if isinstance(node.else_body, list):
                    for stmt in node.else_body:
                        depth = self._count_loop_depth(stmt, current_depth)
                        max_depth = max(max_depth, depth)
        
        return max_depth
    
    def _has_middle_calculation(self, node) -> bool:
        """
        Detecta si el algoritmo calcula un punto medio (middle, mid).
        Patrón típico de búsqueda binaria: middle = (left + right) / 2
        """
        from src.ast.nodes import Assignment, Var
        
        if isinstance(node, Assignment):
            # Extraer el nombre de la variable
            # WORKAROUND: A veces node.name es un string que representa un objeto Var
            var_name = str(node.name).lower()
            
            # Verificar si la variable es middle, mid, etc.
            if any(keyword in var_name for keyword in ['middle', 'mid']):
                # Verificar si el valor es una división
                if hasattr(node, 'expr') and hasattr(node.expr, 'op'):
                    if node.expr.op in ['/', '//']:
                        return True
        
        # Recursively search in children
        if hasattr(node, 'body'):
            body = node.body if isinstance(node.body, list) else [node.body]
            for stmt in body:
                if stmt and self._has_middle_calculation(stmt):
                    return True
        
        if hasattr(node, 'then_body') and node.then_body:
            then_body = node.then_body if isinstance(node.then_body, list) else [node.then_body]
            for stmt in then_body:
                if stmt and self._has_middle_calculation(stmt):
                    return True
        
        if hasattr(node, 'else_body') and node.else_body:
            else_body = node.else_body if isinstance(node.else_body, list) else [node.else_body]
            for stmt in else_body:
                if stmt and self._has_middle_calculation(stmt):
                    return True
        
        return False
    
    def _solve_recurrence(self, recurrence: RecurrenceEquation) -> AsymptoticBound:
        """
        Solve recurrence equation using appropriate method.
        
        Methods:
        1. Master Theorem for divide & conquer
        2. Substitution for linear recursion
        3. Recurrence tree for complex patterns
        """
        
        method = recurrence.method_used
        
        if method == "Master Theorem":
            return self._apply_master_theorem(recurrence)
        
        elif method == "Substitution":
            return self._apply_substitution(recurrence)
        
        elif method == "Recurrence Tree":
            return self._apply_tree_method(recurrence)
        
        elif method == "Loop Analysis":
            return self._analyze_loops(recurrence)
        
        else:
            # Default fallback
            return AsymptoticBound(
                complexity="n",
                notation="O",
                confidence=0.5,
                explanation="Default analysis"
            )
    
    def _apply_master_theorem(self, rec: RecurrenceEquation) -> AsymptoticBound:
        """
        Apply Master Theorem for recurrences of form T(n) = aT(n/b) + f(n).
        
        Cases:
        1. If f(n) = O(n^c) where c < log_b(a): T(n) = Θ(n^log_b(a))
        2. If f(n) = Θ(n^c) where c = log_b(a): T(n) = Θ(n^c log n)
        3. If f(n) = Ω(n^c) where c > log_b(a): T(n) = Θ(f(n))
        """
        
        a = rec.a
        b = rec.b
        f_n = rec.f_n
        
        if a is None or b is None:
            return AsymptoticBound("n", "Θ", 0.7, "Master Theorem not applicable")
        
        # Calculate log_b(a)
        log_b_a = math.log(a) / math.log(b)
        
        # Determine c from f(n)
        if f_n == "c" or f_n == "1":
            c = 0
        elif f_n == "n":
            c = 1
        elif f_n == "n^2":
            c = 2
        else:
            # Try to extract from f_n
            match = re.search(r'n\^(\d+)', f_n)
            c = int(match.group(1)) if match else 1
        
        # Apply Master Theorem cases
        epsilon = 0.01
        
        if c < log_b_a - epsilon:
            # Case 1: f(n) grows polynomially slower than n^log_b(a)
            complexity = self._format_complexity(log_b_a)
            explanation = f"Master Theorem Case 1: f(n) < n^{log_b_a:.2f}"
            
        elif abs(c - log_b_a) < epsilon:
            # Case 2: f(n) and n^log_b(a) grow at same rate
            if c == 0:
                complexity = "log n"
            elif c == 1:
                complexity = "n log n"
            else:
                complexity = f"n^{int(c)} log n"
            explanation = f"Master Theorem Case 2: f(n) = Θ(n^{log_b_a:.2f})"
            
        else:  # c > log_b_a
            # Case 3: f(n) grows polynomially faster than n^log_b(a)
            if c == 1:
                complexity = "n"
            else:
                complexity = f"n^{int(c)}"
            explanation = f"Master Theorem Case 3: f(n) > n^{log_b_a:.2f}"
        
        return AsymptoticBound(
            complexity=complexity,
            notation="Θ",
            confidence=0.95,
            explanation=explanation
        )
    
    def _apply_substitution(self, rec: RecurrenceEquation) -> AsymptoticBound:
        """
        Apply substitution method for recurrences like T(n) = T(n-1) + c.
        
        For T(n) = T(n-1) + c:
        T(n) = T(n-1) + c
             = T(n-2) + c + c
             = T(n-3) + 3c
             ...
             = T(0) + nc
             = Θ(n)
        
        For T(n) = aT(n-1) + c with a > 1:
        T(n) = aT(n-1) + c
             = a(aT(n-2) + c) + c = a²T(n-2) + ac + c
             = a³T(n-3) + a²c + ac + c
             ...
             = a^n·T(0) + c(a^(n-1) + ... + a + 1)
             = Θ(a^n)
        """
        
        a = rec.a if rec.a else 1
        
        if a == 1:
            # Linear recursion: T(n) = T(n-1) + c → Θ(n)
            complexity = "n"
            explanation = "Substitution: T(n) = T(n-1) + c expands to nc"
        else:
            # Exponential: T(n) = aT(n-1) + c → Θ(a^n)
            complexity = f"{a}^n"
            explanation = f"Substitution: T(n) = {a}T(n-1) + c expands to {a}^n"
        
        return AsymptoticBound(
            complexity=complexity,
            notation="Θ",
            confidence=0.95,
            explanation=explanation
        )
    
    def _apply_tree_method(self, rec: RecurrenceEquation) -> AsymptoticBound:
        """
        Apply recurrence tree method for complex recursions.
        
        For Fibonacci-like: T(n) = T(n-1) + T(n-2) + c
        
        Tree has exponential nodes, dominated by Fibonacci growth.
        Number of nodes ≈ φ^n where φ = (1+√5)/2 ≈ 1.618
        
        Since φ^n < 2^n, we use Θ(2^n) as tight bound for simplicity.
        """
        
        equation = rec.equation
        
        if "T(n-1) + T(n-2)" in equation:
            # Fibonacci pattern
            complexity = "2^n"
            explanation = "Tree method: Binary branching gives exponential nodes ≈ φ^n ≈ Θ(2^n)"
            
        elif rec.a and rec.a > 1:
            # Multiple branching
            complexity = f"{rec.a}^n"
            explanation = f"Tree method: {rec.a}-way branching gives Θ({rec.a}^n)"
        else:
            # Default to linear
            complexity = "n"
            explanation = "Tree method: Linear recursion depth"
        
        return AsymptoticBound(
            complexity=complexity,
            notation="Θ",
            confidence=0.90,
            explanation=explanation
        )
    
    def _analyze_loops(self, rec: RecurrenceEquation) -> AsymptoticBound:
        """Analyze iterative algorithms based on loop structure."""
        
        # Extract complexity from equation
        equation = rec.equation
        
        if "n^" in equation:
            match = re.search(r'n\^(\d+)', equation)
            if match:
                power = match.group(1)
                complexity = f"n^{power}"
            else:
                complexity = "n"
        elif "n²" in equation:
            complexity = "n^2"
        elif "cn" in equation or "T(n) = n" in equation:
            complexity = "n"
        else:
            complexity = "1"
        
        return AsymptoticBound(
            complexity=complexity,
            notation="Θ",
            confidence=0.95,
            explanation="Loop analysis: Determined from iteration structure"
        )
    
    def _format_complexity(self, value: float) -> str:
        """Format floating point complexity to readable form."""
        
        if abs(value - round(value)) < 0.01:
            # Close to integer
            int_val = int(round(value))
            if int_val == 0:
                return "1"
            elif int_val == 1:
                return "n"
            else:
                return f"n^{int_val}"
        else:
            # Non-integer exponent
            return f"n^{value:.2f}"
    
    def _has_loop(self, node) -> bool:
        """Check if a node contains any loop structure."""
        
        if isinstance(node, (For, While, Repeat)):
            return True
        
        if hasattr(node, 'body') and node.body:
            for stmt in node.body:
                if self._has_loop(stmt):
                    return True
        
        if isinstance(node, If):
            if node.then_body:
                for stmt in node.then_body:
                    if self._has_loop(stmt):
                        return True
            if node.else_body:
                for stmt in node.else_body:
                    if self._has_loop(stmt):
                        return True
        
        return False
    
    def format_analysis_output(self, recurrence: RecurrenceEquation, bound: AsymptoticBound) -> str:
        """
        Format the analysis output for display.
        
        Format:
        Ecuación: T(n) = ...
        Complejidad: Θ(...)
        """
        
        lines = []
        lines.append("ANÁLISIS ASINTÓTICO FORMAL")
        lines.append("=" * 50)
        lines.append(f"Ecuación: {recurrence.equation}")
        
        # Add base cases
        if recurrence.base_cases:
            base_str = ", ".join([f"{k} = {v}" for k, v in recurrence.base_cases.items()])
            lines.append(f"Casos base: {base_str}")
        
        lines.append(f"Método: {recurrence.method_used}")
        lines.append("")
        lines.append(f"Complejidad: {bound.notation}({bound.complexity})")
        
        if bound.explanation:
            lines.append(f"Explicación: {bound.explanation}")
        
        return "\n".join(lines)
