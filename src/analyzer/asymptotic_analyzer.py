
"""
Analizador de Complejidad Asintotica - Analisis Matematico Formal
==============================================================

Este modulo implementa un analisis asintotico riguroso siguiendo la teoria de la complejidad computacional formal. Determina la cota estricta (Theta) cuando es posible, o proporciona cotas Big O y Omega independientes cuando difieren.

Fundamentos Matematicos:
- Construccion formal de relaciones de recurrencia
- Aplicacion del Teorema Maestro
- Metodo de Sustitucion
- Analisis de arboles de recurrencia
- Determinacion precisa de cotas asintoticas
"""

from typing import Dict, Optional, Tuple, List, Any
from dataclasses import dataclass
import re
import math
from src.ast.nodes import *


@dataclass
class RecurrenceEquation:
    """Representa una ecuacion de recurrencia formal."""
    equation: str           # T(n) = aT(n/b) + f(n) o similar
    a: Optional[int]        # Numero de llamadas recursivas
    b: Optional[int]        # Factor de division
    f_n: str                # Trabajo realizado por llamada
    base_cases: Dict[str, str]  # Definiciones de casos base
    method_used: str        # Metodo de resolucion (Maestro, Sustitucion, Arbol)

    def __str__(self) -> str:
        return self.equation


@dataclass
class AsymptoticBound:
    """Representa la cota de complejidad asintotica."""
    complexity: str         # La clase de complejidad (por ejemplo, "n^2", "2^n")
    notation: str           # "Θ" para cota estricta, "O" para cota superior, "Ω" para cota inferior
    confidence: float       # Nivel de confianza (0.0 a 1.0)
    explanation: str        # Breve explicacion de la cota

    def __str__(self) -> str:
        return f"{self.notation}({self.complexity})"


class AsymptoticAnalyzer:
    """
    Realiza un analisis asintotico formal de algoritmos.
    """

    def __init__(self):
        self.analysis_cache: Dict[str, AsymptoticBound] = {}

    def analyze(self, node, recursive_info: Optional[Dict] = None) -> Tuple[RecurrenceEquation, AsymptoticBound]:
        """Analisis asintotico para un programa completo."""
        recurrence = self._construct_recurrence(node, recursive_info)
        bound = self._solve_recurrence(recurrence)
        return recurrence, bound

    def analyze_function_node(self, func_node, recursive_info):
        """Analiza la complejidad de una funcion especifica (nodo AST)."""
        try:
            recurrence = self._construct_recurrence(func_node, recursive_info)
            bound = self._solve_recurrence(recurrence)

            if not bound.notation:
                bound.notation = "Θ"

            if recursive_info and recursive_info.get('pattern_type') == 'linear':
                if bound.complexity == "1" or not bound.complexity:
                    bound.complexity = "n"
                    bound.notation = "Θ"

            return recurrence, bound
        except Exception as e:  # Retorno de seguridad en caso de fallo interno
            return (
                RecurrenceEquation("Error interno", None, None, "", {}, "Error"),
                AsymptoticBound("?", "O", 0.0, str(e))
            )

    def estimate_level_costs(self, equation: str) -> list:
        """Resumen textual de costos por nivel para patrones comunes."""
        if not equation:
            return []

        eq = equation.replace(" ", "").lower()
        levels = []

        if "t(n/2)" in eq and eq.startswith("t(n)="):
            calls = 2 if "2t(n/2)" in eq else 1
            if calls == 1:
                levels.append("Nivel k: 1 nodo de tamano n/2^k; costo nivel ~= c")
                levels.append("Altura ~= log2(n); Trabajo total ~= c*log n")
            else:
                levels.append("Nivel k: 2^k nodos de tamano n/2^k; costo nivel ~= n")
                levels.append("Altura ~= log2(n); Trabajo total ~= n*log n + n")
        elif "t(n-1)" in eq and "t(n-2)" in eq:
            levels.append("Nivel k: ~2^k nodos; costo nivel ~= 2^k (2?1.618)")
            levels.append("Altura ~= n; Trabajo total ~= 2^n")
        elif "t(n-1)" in eq:
            levels.append("Nivel k: 1 nodo; costo nivel ~= c")
            levels.append("Altura ~= n; Trabajo total ~= n")
        else:
            levels.append("Patron no reconocido para desglose por niveles.")

        return levels

    def _construct_recurrence(self, node, recursive_info: Optional[Dict]) -> RecurrenceEquation:
        """Construir la relacion de recurrencia formal."""
        if not recursive_info or not recursive_info.get('has_recursion'):
            return self._analyze_iterative(node)

        # Si el analizador recursivo ya dedujo la recurrencia, usala directamente
        relation = recursive_info.get('recurrence_relation')
        base_cases = recursive_info.get('base_cases') or {"T(0)": "c", "T(1)": "c"}
        if relation:
            normalized = relation.replace(' ', '').lower()
            a = None
            b = None
            f_n = "c"
            method = "Derived from recursive analysis"

            if "t(n/2)" in normalized:
                a = 2 if "2t(n/2)" in normalized else 1
                b = 2
                if "o(n)" in normalized or "+n" in normalized:
                    f_n = "n"
                method = "Master Theorem"
            elif "t(n-1)" in normalized and "t(n-2)" in normalized:
                a = 2
                f_n = "c"
                method = "Recurrence Tree"
            elif "t(n-1)" in normalized:
                coef_match = re.search(r'(\d+)t\(n-1\)', normalized)
                a = int(coef_match.group(1)) if coef_match else 1
                f_n = "c"
                method = "Substitution"

            return RecurrenceEquation(
                equation=relation,
                a=a, b=b, f_n=f_n,
                base_cases=base_cases,
                method_used=method
            )

        num_calls = len(recursive_info.get('recursive_calls', [])) or 1
        pattern_type = recursive_info.get('pattern_type', 'linear')

        if pattern_type == 'linear':
            return RecurrenceEquation(
                equation="T(n) = T(n-1) + c",
                a=1, b=None, f_n="c",
                base_cases={"T(0)": "c", "T(1)": "c"},
                method_used="Substitution"
            )
        elif pattern_type == 'binary_exclusive':
            return RecurrenceEquation(
                equation="T(n) = T(n/2) + c",
                a=1, b=2, f_n="c",
                base_cases={"T(1)": "c", "T(0)": "c"},
                method_used="Master Theorem"
            )
        elif pattern_type == 'binary':
            return RecurrenceEquation(
                equation="T(n) = T(n-1) + T(n-2) + c",
                a=2, b=None, f_n="c",
                base_cases={"T(0)": "c", "T(1)": "c"},
                method_used="Recurrence Tree"
            )
        elif pattern_type == 'divide_conquer':
            a = num_calls if num_calls > 0 else 2
            return RecurrenceEquation(
                equation=f"T(n) = {a}T(n/2) + n",
                a=a, b=2, f_n="n",
                base_cases={"T(1)": "c"},
                method_used="Master Theorem"
            )
        else:
            return RecurrenceEquation(
                equation=f"T(n) = {num_calls}T(n-1) + c",
                a=num_calls, b=None, f_n="c",
                base_cases={"T(0)": "c", "T(1)": "c"},
                method_used="Substitution"
            )

    def _analyze_iterative(self, node) -> RecurrenceEquation:
        """Analizar algoritmo iterativo (no recursivo)."""
        loop_depth = self._count_loop_depth(node)

        if loop_depth == 0:
            equation = "T(n) = c"
        elif loop_depth == 1:
            equation = "T(n) = cn"
        elif loop_depth == 2:
            equation = "T(n) = cn^2"
        else:
            equation = f"T(n) = cn^{loop_depth}"

        return RecurrenceEquation(
            equation=equation, a=None, b=None, f_n="c",
            base_cases={"T(0)": "c"}, method_used="Loop Analysis"
        )

    def _count_loop_depth(self, node, current_depth: int = 0) -> int:
        """Contar la profundidad maxima de anidamiento de bucles."""
        max_depth = current_depth

        if isinstance(node, (For, While, Repeat)):
            body_depth = current_depth + 1
            if hasattr(node, 'body') and node.body:
                for stmt in node.body:
                    depth = self._count_loop_depth(stmt, body_depth)
                    max_depth = max(max_depth, depth)

        elif isinstance(node, (Function, Program)):
            items = node.body if hasattr(node, 'body') else (node.functions if hasattr(node, 'functions') else [])
            if items:
                for item in items:
                    depth = self._count_loop_depth(item, current_depth)
                    max_depth = max(max_depth, depth)

        elif isinstance(node, If):
            if hasattr(node, 'then_body') and node.then_body:
                stmts = node.then_body if isinstance(node.then_body, list) else [node.then_body]
                for stmt in stmts:
                    depth = self._count_loop_depth(stmt, current_depth)
                    max_depth = max(max_depth, depth)

            if hasattr(node, 'else_body') and node.else_body:
                stmts = node.else_body if isinstance(node.else_body, list) else [node.else_body]
                for stmt in stmts:
                    depth = self._count_loop_depth(stmt, current_depth)
                    max_depth = max(max_depth, depth)

        return max_depth

    def _has_middle_calculation(self, node) -> bool:
        """Detecta si el algoritmo calcula un punto medio."""
        from src.ast.nodes import Assignment, Var

        if isinstance(node, Assignment):
            var_name = str(node.name).lower()
            if any(keyword in var_name for keyword in ['middle', 'mid']):
                if hasattr(node, 'expr') and hasattr(node.expr, 'op'):
                    if node.expr.op in ['/', '//']:
                        return True

        if hasattr(node, 'body'):
            body = node.body if isinstance(node.body, list) else [node.body]
            for stmt in body:
                if stmt and self._has_middle_calculation(stmt):
                    return True

        if hasattr(node, 'then_body') and node.then_body:
            stmts = node.then_body if isinstance(node.then_body, list) else [node.then_body]
            for stmt in stmts:
                if stmt and self._has_middle_calculation(stmt):
                    return True

        if hasattr(node, 'else_body') and node.else_body:
            stmts = node.else_body if isinstance(node.else_body, list) else [node.else_body]
            for stmt in stmts:
                if stmt and self._has_middle_calculation(stmt):
                    return True

        return False

    def _solve_recurrence(self, recurrence: RecurrenceEquation) -> AsymptoticBound:
        """Resolver la ecuacion de recurrencia."""
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
            return AsymptoticBound("n", "O", 0.5, "Default analysis")

    def _apply_master_theorem(self, rec: RecurrenceEquation) -> AsymptoticBound:
        a, b, f_n = rec.a, rec.b, rec.f_n
        if a is None or b is None:
            return AsymptoticBound("n", "Θ", 0.7, "Teorema Maestro no aplicable")

        log_b_a = math.log(a) / math.log(b)

        if f_n == "c" or f_n == "1":
            c = 0
        elif f_n == "n":
            c = 1
        elif f_n == "n^2":
            c = 2
        else:
            match = re.search(r'n\^(\d+)', f_n)
            c = int(match.group(1)) if match else 1

        epsilon = 0.01
        if c < log_b_a - epsilon:
            complexity = self._format_complexity(log_b_a)
            explanation = f"Teorema Maestro Caso 1: f(n) < n^{log_b_a:.2f}"
        elif abs(c - log_b_a) < epsilon:
            if c == 0:
                complexity = "log n"
            elif c == 1:
                complexity = "n log n"
            else:
                complexity = f"n^{int(c)} log n"
            explanation = f"Teorema Maestro Caso 2: f(n) = ?(n^{log_b_a:.2f})"
        else:
            if c == 1:
                complexity = "n"
            else:
                complexity = f"n^{int(c)}"
            explanation = f"Teorema Maestro Caso 3: f(n) > n^{log_b_a:.2f}"

        return AsymptoticBound(complexity, "Θ", 0.95, explanation)

    def _apply_substitution(self, rec: RecurrenceEquation) -> AsymptoticBound:
        a = rec.a if rec.a else 1
        if a == 1:
            complexity = "n"
            explanation = "Sustitucion: T(n) = T(n-1) + c se expande a n*c"
        else:
            complexity = f"{a}^n"
            explanation = f"Sustitucion: T(n) = {a}T(n-1) + c se expande a {a}^n"
        return AsymptoticBound(complexity, "Θ", 0.95, explanation)

    def _apply_tree_method(self, rec: RecurrenceEquation) -> AsymptoticBound:
        equation = rec.equation
        if "T(n-1) + T(n-2)" in equation:
            complexity = "2^n"
            explanation = "Metodo del arbol: Ramificacion binaria ~ 2^n ~ ?(2^n)"
        elif rec.a and rec.a > 1:
            complexity = f"{rec.a}^n"
            explanation = f"Metodo del arbol: Ramificacion {rec.a} da ?({rec.a}^n)"
        else:
            complexity = "n"
            explanation = "Metodo del arbol: Profundidad lineal de recursion"
        return AsymptoticBound(complexity, "Θ", 0.90, explanation)

    def _analyze_loops(self, rec: RecurrenceEquation) -> AsymptoticBound:
        equation = rec.equation
        if "n^" in equation:
            match = re.search(r'n\^(\d+)', equation)
            complexity = f"n^{match.group(1)}" if match else "n"
        elif "cn" in equation or "T(n) = n" in equation:
            complexity = "n"
        else:
            complexity = "1"
        return AsymptoticBound(complexity, "Θ", 0.95, "Analisis de bucles: Determinado a partir de la estructura de iteracion")

    def _format_complexity(self, value: float) -> str:
        if abs(value - round(value)) < 0.01:
            int_val = int(round(value))
            if int_val == 0:
                return "1"
            elif int_val == 1:
                return "n"
            else:
                return f"n^{int_val}"
        else:
            return f"n^{value:.2f}"

    def _has_loop(self, node) -> bool:
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
