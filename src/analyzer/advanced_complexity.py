"""
Advanced Complexity Analyzer
============================

This module provides comprehensive complexity analysis for pseudocode algorithms,
supporting Big O (worst case), Omega (best case), and Theta (tight bound) notations.

The analyzer traverses the AST and applies complexity analysis rules based on
algorithmic constructs like loops, conditionals, recursion, and data structure operations.
"""

from src.ast.nodes import *
from dataclasses import dataclass
from typing import Dict, List, Optional, Union
import re


@dataclass
class ComplexityResult:
    """Represents the complexity analysis result with O, Ω, and Θ notations."""
    big_o: str          # Worst case (upper bound)
    omega: str          # Best case (lower bound)  
    theta: Optional[str] = None  # Tight bound (when O = Ω)
    
    def __post_init__(self):
        """Calculate Theta if O and Omega are equal."""
        if self.big_o == self.omega:
            self.theta = self.big_o
    
    def __str__(self):
        result = f"O({self.big_o}), Ω({self.omega})"
        if self.theta:
            result += f", Θ({self.theta})"
        return result


class ComplexityFunction:
    """Represents a complexity function for mathematical operations."""
    
    def __init__(self, expression: str):
        self.expression = expression
        self.degree = self._calculate_degree()
    
    def _calculate_degree(self) -> int:
        """Calculate the polynomial degree of the complexity function."""
        if "log" in self.expression:
            return 0.5  # log n grows slower than linear
        elif "^" in self.expression:
            # Extract highest power
            powers = re.findall(r'\^(\d+)', self.expression)
            return max(int(p) for p in powers) if powers else 1
        elif "n" in self.expression:
            return 1
        else:
            return 0  # constant
    
    def __str__(self):
        return self.expression
    
    def __eq__(self, other):
        return isinstance(other, ComplexityFunction) and self.expression == other.expression
    
    def __lt__(self, other):
        return self.degree < other.degree


class AdvancedComplexityAnalyzer:
    """
    Advanced complexity analyzer supporting O, Ω, and Θ notations.
    
    Analysis Rules:
    - Constants: O(1), Ω(1), Θ(1)
    - Simple loops: O(n), Ω(n), Θ(n)  
    - Nested loops: O(n^k) where k is nesting depth
    - Conditionals: max(branches) for O, min(branches) for Ω
    - Arrays/Matrices: depends on access pattern
    - Recursion: analyzed based on recurrence relations
    """
    
    def __init__(self):
        self.loop_depth = 0
        self.recursive_calls = {}
        
    def analyze(self, node) -> ComplexityResult:
        """Main entry point for complexity analysis."""
        return self._analyze_node(node)
    
    def _analyze_node(self, node) -> ComplexityResult:
        """Dispatch to appropriate analysis method based on node type."""
        method_name = f"_analyze_{type(node).__name__.lower()}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(node)
        else:
            # Default case for unknown nodes
            return ComplexityResult("1", "1")
    
    # ========== Program Structure Analysis ==========
    
    def _analyze_program(self, node: Program) -> ComplexityResult:
        """Analyze entire program - combines all function complexities."""
        if not node.functions:
            return ComplexityResult("1", "1")
        
        # For programs with multiple functions, we typically analyze the main function
        # or return the maximum complexity among all functions
        results = [self._analyze_node(func) for func in node.functions]
        return self._combine_parallel(results)
    
    def _analyze_function(self, node: Function) -> ComplexityResult:
        """Analyze function body - combines all statements sequentially."""
        if not node.body:
            return ComplexityResult("1", "1")
        
        results = [self._analyze_node(stmt) for stmt in node.body]
        return self._combine_sequential(results)
    
    # ========== Statement Analysis ==========
    
    def _analyze_assignment(self, node: Assignment) -> ComplexityResult:
        """Analyze assignment - depends on RHS expression complexity."""
        rhs_complexity = self._analyze_node(node.expr)
        
        # Check if LHS is array/matrix access (affects complexity)
        if isinstance(node.name, (ArrayAccess, MatrixAccess)):
            access_complexity = self._analyze_node(node.name)
            return self._combine_sequential([rhs_complexity, access_complexity])
        
        return rhs_complexity
    
    def _analyze_for(self, node: For) -> ComplexityResult:
        """Analyze for loop - multiplies iteration count by body complexity."""
        self.loop_depth += 1
        
        # Analyze loop bounds to determine iteration count
        start_complexity = self._analyze_node(node.start)
        end_complexity = self._analyze_node(node.end)
        
        # Analyze body complexity
        body_results = [self._analyze_node(stmt) for stmt in node.body]
        body_complexity = self._combine_sequential(body_results)
        
        # For simple loops (0 to n), the iteration count is O(n)
        # More complex bounds would require different analysis
        loop_iterations = ComplexityFunction("n")
        
        # Multiply loop iterations by body complexity
        result = self._multiply_complexity(loop_iterations, body_complexity)
        
        self.loop_depth -= 1
        return result
    
    def _analyze_while(self, node: While) -> ComplexityResult:
        """Analyze while loop - estimates based on condition and body."""
        self.loop_depth += 1
        
        # Analyze condition complexity
        condition_complexity = self._analyze_node(node.condition)
        
        # Analyze body complexity  
        body_results = [self._analyze_node(stmt) for stmt in node.body]
        body_complexity = self._combine_sequential(body_results)
        
        # While loops are harder to analyze - we make conservative estimates
        # Best case: condition false immediately (Ω(1))
        # Worst case: assume O(n) iterations (could be more depending on algorithm)
        worst_case = self._multiply_complexity(ComplexityFunction("n"), body_complexity)
        best_case = ComplexityResult("1", "1")
        
        self.loop_depth -= 1
        return ComplexityResult(worst_case.big_o, best_case.omega)
    
    def _analyze_repeat(self, node: Repeat) -> ComplexityResult:
        """Analyze repeat-until loop - similar to while but executes at least once."""
        self.loop_depth += 1
        
        body_results = [self._analyze_node(stmt) for stmt in node.body]
        body_complexity = self._combine_sequential(body_results)
        condition_complexity = self._analyze_node(node.condition)
        
        # Repeat loops execute at least once
        # Best case: one iteration
        # Worst case: assume O(n) iterations
        worst_case = self._multiply_complexity(ComplexityFunction("n"), body_complexity)
        best_case = body_complexity
        
        self.loop_depth -= 1
        return ComplexityResult(worst_case.big_o, best_case.omega)
    
    def _analyze_if(self, node: If) -> ComplexityResult:
        """Analyze conditional - worst case takes max branch, best case takes min."""
        then_result = self._combine_sequential([self._analyze_node(stmt) for stmt in node.then_body])
        
        if node.else_body:
            else_result = self._combine_sequential([self._analyze_node(stmt) for stmt in node.else_body])
            # Worst case: max of branches, Best case: min of branches
            worst_case = self._max_complexity(then_result.big_o, else_result.big_o)
            best_case = self._min_complexity(then_result.omega, else_result.omega)
            return ComplexityResult(worst_case, best_case)
        else:
            # No else branch - best case is O(1) (condition check only)
            return ComplexityResult(then_result.big_o, "1")
    
    def _analyze_return(self, node: Return) -> ComplexityResult:
        """Analyze return statement - depends on expression complexity."""
        return self._analyze_node(node.expr)
    
    def _analyze_call(self, node: Call) -> ComplexityResult:
        """Analyze function call - depends on called function and arguments."""
        # Analyze argument complexities
        arg_results = [self._analyze_node(arg) for arg in node.args] if node.args else []
        arg_complexity = self._combine_sequential(arg_results) if arg_results else ComplexityResult("1", "1")
        
        # For recursive calls, we need special handling
        if node.name in self.recursive_calls:
            return self._analyze_recursion(node)
        
        # For built-in or unknown functions, assume O(1) unless we have specific knowledge
        # This could be extended with a function complexity database
        return self._combine_sequential([arg_complexity, ComplexityResult("1", "1")])
    
    # ========== Expression Analysis ==========
    
    def _analyze_binop(self, node: BinOp) -> ComplexityResult:
        """Analyze binary operation - combines operand complexities."""
        left_result = self._analyze_node(node.left)
        right_result = self._analyze_node(node.right)
        
        # Basic arithmetic operations are O(1) once operands are computed
        return self._combine_sequential([left_result, right_result, ComplexityResult("1", "1")])
    
    def _analyze_var(self, node: Var) -> ComplexityResult:
        """Variable access is O(1)."""
        return ComplexityResult("1", "1")
    
    def _analyze_number(self, node: Number) -> ComplexityResult:
        """Number literals are O(1)."""
        return ComplexityResult("1", "1")
    
    def _analyze_condition(self, node: Condition) -> ComplexityResult:
        """Analyze condition - combines operand complexities plus comparison."""
        left_result = self._analyze_node(node.left)
        right_result = self._analyze_node(node.right)
        
        # Comparison operations are O(1) once operands are computed
        return self._combine_sequential([left_result, right_result, ComplexityResult("1", "1")])
    
    # ========== Array/Matrix Analysis ==========
    
    def _analyze_arrayaccess(self, node: ArrayAccess) -> ComplexityResult:
        """Array access - O(1) for index computation + O(1) for access."""
        index_complexity = self._analyze_node(node.index)
        return self._combine_sequential([index_complexity, ComplexityResult("1", "1")])
    
    def _analyze_matrixaccess(self, node: MatrixAccess) -> ComplexityResult:
        """Matrix access - O(1) for both indices + O(1) for access."""
        row_complexity = self._analyze_node(node.row_index)
        col_complexity = self._analyze_node(node.col_index)
        return self._combine_sequential([row_complexity, col_complexity, ComplexityResult("1", "1")])
    
    def _analyze_arraydeclaration(self, node: ArrayDeclaration) -> ComplexityResult:
        """Array declaration - depends on size and initialization."""
        size_complexity = self._analyze_node(node.size)
        # Declaration itself might require O(size) for initialization
        return ComplexityResult("n", "n")  # Assuming initialization to size
    
    def _analyze_matrixdeclaration(self, node: MatrixDeclaration) -> ComplexityResult:
        """Matrix declaration - O(rows * cols) for initialization."""
        rows_complexity = self._analyze_node(node.rows)
        cols_complexity = self._analyze_node(node.cols)
        return ComplexityResult("n^2", "n^2")  # Assuming n x n matrix
    
    # ========== Boolean Expression Analysis ==========
    
    def _analyze_boolop(self, node: BoolOp) -> ComplexityResult:
        """Analyze boolean operation - considers short-circuit evaluation."""
        left_result = self._analyze_node(node.left)
        right_result = self._analyze_node(node.right)
        
        if node.op == 'and':
            # Short-circuit: best case only evaluates left operand
            worst_case = self._combine_sequential([left_result, right_result])
            return ComplexityResult(worst_case.big_o, left_result.omega)
        elif node.op == 'or':
            # Short-circuit: best case only evaluates left operand  
            worst_case = self._combine_sequential([left_result, right_result])
            return ComplexityResult(worst_case.big_o, left_result.omega)
        
        return self._combine_sequential([left_result, right_result])
    
    def _analyze_unaryop(self, node: UnaryOp) -> ComplexityResult:
        """Analyze unary operation (like 'not')."""
        operand_result = self._analyze_node(node.operand)
        return self._combine_sequential([operand_result, ComplexityResult("1", "1")])
    
    def _analyze_boolean(self, node: Boolean) -> ComplexityResult:
        """Boolean literals are O(1)."""
        return ComplexityResult("1", "1")
    
    # ========== Helper Methods ==========
    
    def _combine_sequential(self, results: List[ComplexityResult]) -> ComplexityResult:
        """Combine complexities for sequential execution (addition)."""
        if not results:
            return ComplexityResult("1", "1")
        
        # For sequential execution, we take the maximum complexity
        big_o = self._max_complexity(*[r.big_o for r in results])
        omega = self._max_complexity(*[r.omega for r in results])
        
        return ComplexityResult(big_o, omega)
    
    def _combine_parallel(self, results: List[ComplexityResult]) -> ComplexityResult:
        """Combine complexities for parallel/alternative execution."""
        if not results:
            return ComplexityResult("1", "1")
        
        # For alternatives, worst case is max, best case is min
        big_o = self._max_complexity(*[r.big_o for r in results])
        omega = self._min_complexity(*[r.omega for r in results])
        
        return ComplexityResult(big_o, omega)
    
    def _multiply_complexity(self, factor: ComplexityFunction, complexity: ComplexityResult) -> ComplexityResult:
        """Multiply complexity by a factor (for loops)."""
        big_o = self._multiply_expressions(str(factor), complexity.big_o)
        omega = self._multiply_expressions(str(factor), complexity.omega)
        
        return ComplexityResult(big_o, omega)
    
    def _multiply_expressions(self, factor: str, complexity: str) -> str:
        """Multiply two complexity expressions."""
        if complexity == "1":
            return factor
        if factor == "1":
            return complexity
        if factor == "n" and complexity == "n":
            return "n^2"
        if factor == "n" and "^" in complexity:
            power = re.search(r'n\^(\d+)', complexity)
            if power:
                new_power = int(power.group(1)) + 1
                return f"n^{new_power}"
        
        # Default case - might need more sophisticated parsing
        return f"{factor}*{complexity}"
    
    def _max_complexity(self, *complexities: str) -> str:
        """Return the maximum (dominant) complexity."""
        complexity_order = self._sort_complexities(complexities)
        return complexity_order[-1]  # Return the largest
    
    def _min_complexity(self, *complexities: str) -> str:
        """Return the minimum complexity."""
        complexity_order = self._sort_complexities(complexities)
        return complexity_order[0]  # Return the smallest
    
    def _sort_complexities(self, complexities: tuple) -> List[str]:
        """Sort complexities by growth rate."""
        complexity_map = {
            "1": 0,
            "log n": 1,
            "n": 2,
            "n log n": 3,
            "n^2": 4,
            "n^3": 5,
            "2^n": 6,
            "n!": 7
        }
        
        def complexity_weight(comp: str) -> float:
            # Handle power expressions
            if "^" in comp:
                power_match = re.search(r'n\^(\d+)', comp)
                if power_match:
                    return 2 + int(power_match.group(1))
            
            return complexity_map.get(comp, 2)  # Default to linear if unknown
        
        return sorted(complexities, key=complexity_weight)
    
    def _analyze_recursion(self, node: Call) -> ComplexityResult:
        """Analyze recursive function calls."""
        # This is a simplified recursion analysis
        # More sophisticated analysis would solve recurrence relations
        
        # For now, assume common recursive patterns:
        # - Linear recursion (like factorial): O(n)
        # - Binary recursion (like fibonacci): O(2^n)
        # - Divide-and-conquer (like mergesort): O(n log n)
        
        # This would need to be extended based on specific recursion patterns
        return ComplexityResult("n", "n")  # Conservative estimate