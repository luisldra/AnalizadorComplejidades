"""
Analizador de Complejidad Asintótica - Análisis Matemático Formal
==============================================================

Este módulo implementa un análisis asintótico riguroso siguiendo la teoría de la complejidad computacional formal. Determina la cota estricta (Theta) cuando es posible, o proporciona cotas Big O y Omega independientes cuando difieren.

Fundamentos Matemáticos:
- Construcción formal de relaciones de recurrencia
- Aplicación del Teorema Maestro
- Método de Sustitución
- Análisis de árboles de recurrencia
- Determinación precisa de cotas asintóticas

"""

from typing import Dict, Optional, Tuple, List, Any
from dataclasses import dataclass
import re
import math
from src.ast.nodes import *

@dataclass
class RecurrenceEquation:
    """Representa una ecuación de recurrencia formal."""
    equation: str           # T(n) = aT(n/b) + f(n) o similar
    a: Optional[int]        # úmero de llamadas recursivas
    b: Optional[int]        # Factor de división
    f_n: str               # Trabajo realizado por llamada
    base_cases: Dict[str, str]  # Definiciones de casos base
    method_used: str       # Método de resolución (Maestro, Sustitución, Árbol)
    
    def __str__(self):
        return self.equation


@dataclass
class AsymptoticBound:
    """Representa la cota de complejidad asintótica."""
    complexity: str         # La clase de complejidad (por ejemplo, "n^2", "2^n")
    notation: str          # "Θ" para cota estricta, "O" para cota superior, "Ω" para cota inferior
    confidence: float      # Nivel de confianza (0.0 a 1.0)
    explanation: str       # Breve explicación de la cota
    
    def __str__(self):
        return f"{self.notation}({self.complexity})"


class AsymptoticAnalyzer:
    """
    Realiza un análisis asintótico formal de algoritmos.
    
    Este analizador determina:
    1. La relación de recurrencia precisa
    2. El método de solución apropiado
    3. La cota estricta (Theta) cuando coinciden el mejor y peor caso
    4. Cotizaciones separadas cuando difieren
    """
    
    def __init__(self):
        self.analysis_cache: Dict[str, AsymptoticBound] = {}
        
    def analyze(self, node, recursive_info: Optional[Dict] = None) -> Tuple[RecurrenceEquation, AsymptoticBound]:
        """
        Realiza un análisis asintótico completo.
        
        Args:
            node: Nodo AST a analizar
            recursive_info: Análisis recursivo opcional desde RecursiveAlgorithmAnalyzer
            
        Returns:
            Tupla de (RecurrenceEquation, AsymptoticBound)
        """
        
        # Paso 1: Construir la ecuación de recurrencia formal
        recurrence = self._construct_recurrence(node, recursive_info)
        
        # Paso 2: Resolver usando el método apropiado
        bound = self._solve_recurrence(recurrence)
        
        return recurrence, bound
    
    def _construct_recurrence(self, node, recursive_info: Optional[Dict]) -> RecurrenceEquation:
        """
        Construir la relación de recurrencia formal.
        
        Para algoritmos recursivos:
        - Identificar el número de llamadas recursivas (a)
        - Identificar la reducción del tamaño del problema (b en T(n/b))
        - Identificar el trabajo por nivel f(n)
        - Definir casos base
        """
        
        if not recursive_info or not recursive_info.get('has_recursion'):
            # Algoritmo no recursivo
            return self._analyze_iterative(node)
        
        # Algoritmo recursivo - construir recurrencia
        num_calls = len(recursive_info.get('recursive_calls', []))
        pattern_type = recursive_info.get('pattern_type', 'linear')
        
        # Determinar parámetros de recurrencia
        if pattern_type == 'linear':
            # T(n) = T(n-1) + c
            return RecurrenceEquation(
                equation="T(n) = T(n-1) + c",
                a=1,
                b=None,  # Decremento, no división
                f_n="c",
                base_cases={"T(0)": "c", "T(1)": "c"},
                method_used="Substitution"
            )
            
        elif pattern_type == 'binary':
            # CRÍTICO: "binary" puede significar DOS cosas diferentes:
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
            # Divide y venceras: T(n) = aT(n/b) + f(n)
            # Analizar desde recursive_info si está disponible
            relation = recursive_info.get('recurrence_relation', '')
            
            # Intente extraer a y b de la relación
            match = re.search(r'(\d+)T\(n/(\d+)\)', relation)
            if match:
                a = int(match.group(1))
                b = int(match.group(2))
            else:
                # Por defecto: división binaria
                a = num_calls
                b = 2
            
            # Determinar f(n) - trabajo por nivel
            # Verificar si hay bucles o trabajo lineal en la función
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
            # Múltiples llamadas - generalmente exponencial
            return RecurrenceEquation(
                equation=f"T(n) = {num_calls}T(n-1) + c",
                a=num_calls,
                b=None,
                f_n="c",
                base_cases={"T(0)": "c", "T(1)": "c"},
                method_used="Substitution"
            )
    
    def _analyze_iterative(self, node) -> RecurrenceEquation:
        """Analizar algoritmo iterativo (no recursivo)."""
        
        # Analizar estructura de bucles
        loop_depth = self._count_loop_depth(node)
        
        if loop_depth == 0:
            # Sin bucles - tiempo constante
            equation = "T(n) = c"
            complexity = "1"
        elif loop_depth == 1:
            # Un solo bucle - tiempo lineal
            equation = "T(n) = cn"
            complexity = "n"
        elif loop_depth == 2:
            # Bucles anidados - tiempo cuadrático
            equation = "T(n) = cn²"
            complexity = "n^2"
        else:
            # Múltiples bucles anidados
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
        """Contar la profundidad máxima de anidamiento de bucles."""
        
        max_depth = current_depth
        
        if isinstance(node, (For, While, Repeat)):
            # Esto es un bucle - incrementar profundidad
            body_depth = current_depth + 1
            
            # Verificar profundidad en el cuerpo del bucle
            if hasattr(node, 'body') and node.body:
                for stmt in node.body:
                    depth = self._count_loop_depth(stmt, body_depth)
                    max_depth = max(max_depth, depth)
        
        elif isinstance(node, (Function, Program)):
            # Verificar todas las declaraciones/funciones
            items = node.body if hasattr(node, 'body') else node.functions
            if items:
                for item in items:
                    depth = self._count_loop_depth(item, current_depth)
                    max_depth = max(max_depth, depth)
        
        elif isinstance(node, If):
            # Verificar ambas ramas
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
        
        # Búsqueda recursiva en hijos
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
        Resolver la ecuación de recurrencia utilizando el método adecuado.

        Métodos:
        1. Teorema maestro de "divide y vencerás"
        2. Sustitución para recursividad lineal
        3. Árbol de recurrencia para patrones complejos
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
        Aplicar Teorema Maestro para recurrencias de la forma T(n) = aT(n/b) + f(n).
        
        Casos:
        1. Si f(n) = O(n^c) donde c < log_b(a): T(n) = Θ(n^log_b(a))
        2. Si f(n) = Θ(n^c) donde c = log_b(a): T(n) = Θ(n^c log n)
        3. Si f(n) = Ω(n^c) donde c > log_b(a): T(n) = Θ(f(n))
        """
        
        a = rec.a
        b = rec.b
        f_n = rec.f_n
        
        if a is None or b is None:
            return AsymptoticBound("n", "Θ", 0.7, "Teorema Maestro no aplicable")
        
        # Calcular log_b(a)
        log_b_a = math.log(a) / math.log(b)
        
        # Determinar c a partir de f(n)
        if f_n == "c" or f_n == "1":
            c = 0
        elif f_n == "n":
            c = 1
        elif f_n == "n^2":
            c = 2
        else:
            # Intentar extraer de f_n
            match = re.search(r'n\^(\d+)', f_n)
            c = int(match.group(1)) if match else 1
        
        # Aplicar casos del Teorema Maestro
        epsilon = 0.01
        
        if c < log_b_a - epsilon:
            # Caso 1: f(n) crece polinomialmente más lento que n^log_b(a)
            complexity = self._format_complexity(log_b_a)
            explanation = f"Teorema Maestro Caso 1: f(n) < n^{log_b_a:.2f}"
            
        elif abs(c - log_b_a) < epsilon:
            # Caso 2: f(n) y n^log_b(a) crecen a la misma tasa
            if c == 0:
                complexity = "log n"
            elif c == 1:
                complexity = "n log n"
            else:
                complexity = f"n^{int(c)} log n"
            explanation = f"Teorema Maestro Caso 2: f(n) = Θ(n^{log_b_a:.2f})"
            
        else:  # c > log_b_a
            # Caso 3: f(n) crece polinomialmente más rápido que n^log_b(a)
            if c == 1:
                complexity = "n"
            else:
                complexity = f"n^{int(c)}"
            explanation = f"Teorema Maestro Caso 3: f(n) > n^{log_b_a:.2f}"
        
        return AsymptoticBound(
            complexity=complexity,
            notation="Θ",
            confidence=0.95,
            explanation=explanation
        )
    
    def _apply_substitution(self, rec: RecurrenceEquation) -> AsymptoticBound:
        """
        Aplicar método de sustitución para recurrencias como T(n) = T(n-1) + c.
        
        Para T(n) = T(n-1) + c:
        T(n) = T(n-1) + c
             = T(n-2) + c + c
             = T(n-3) + 3c
             ...
             = T(0) + nc
             = Θ(n)
        
        Para T(n) = aT(n-1) + c con a > 1:
        T(n) = aT(n-1) + c
             = a(aT(n-2) + c) + c = a²T(n-2) + ac + c
             = a³T(n-3) + a²c + ac + c
             ...
             = a^n·T(0) + c(a^(n-1) + ... + a + 1)
             = Θ(a^n)
        """
        
        a = rec.a if rec.a else 1
        
        if a == 1:
            # Recursión lineal: T(n) = T(n-1) + c → Θ(n)
            complexity = "n"
            explanation = "Sustitución: T(n) = T(n-1) + c se expande a nc"
        else:
            # Exponencial: T(n) = aT(n-1) + c → Θ(a^n)
            complexity = f"{a}^n"
            explanation = f"Sustitución: T(n) = {a}T(n-1) + c se expande a {a}^n"
        
        return AsymptoticBound(
            complexity=complexity,
            notation="Θ",
            confidence=0.95,
            explanation=explanation
        )
    
    def _apply_tree_method(self, rec: RecurrenceEquation) -> AsymptoticBound:
        """
        Aplicar el método del árbol de recurrencia para recursiones complejas.

        Para recursiones similares a Fibonacci: T(n) = T(n-1) + T(n-2) + c

        El árbol tiene nodos exponenciales, dominados por el crecimiento de Fibonacci.
        Número de nodos ≈ φ^n, donde φ = (1+√5)/2 ≈ 1,618

        Como φ^n < 2^n, utilizamos Θ(2^n) como límite estricto para simplificar.
        """
        
        equation = rec.equation
        
        if "T(n-1) + T(n-2)" in equation:
            # Patrón Fibonacci
            complexity = "2^n"
            explanation = "Método del árbol: Ramificación binaria da nodos exponenciales ≈ φ^n ≈ Θ(2^n)"
            
        elif rec.a and rec.a > 1:
            # Ramificación múltiple
            complexity = f"{rec.a}^n"
            explanation = f"Método del árbol: Ramificación {rec.a} da Θ({rec.a}^n)"
        else:
            # Default to linear
            complexity = "n"
            explanation = "Método del árbol: Profundidad lineal de recursión"
        
        return AsymptoticBound(
            complexity=complexity,
            notation="Θ",
            confidence=0.90,
            explanation=explanation
        )
    
    def _analyze_loops(self, rec: RecurrenceEquation) -> AsymptoticBound:
        """Analizar algoritmos iterativos basados en la estructura de bucles."""
        
        # Extraer complejidad de la ecuación
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
            explanation="Análisis de bucles: Determinado a partir de la estructura de iteración"
        )
    
    def _format_complexity(self, value: float) -> str:
        """Formatear la complejidad en punto flotante a una forma legible."""
        
        if abs(value - round(value)) < 0.01:
            # Cercano a entero
            int_val = int(round(value))
            if int_val == 0:
                return "1"
            elif int_val == 1:
                return "n"
            else:
                return f"n^{int_val}"
        else:
            # Exponente no entero
            return f"n^{value:.2f}"
    
    def _has_loop(self, node) -> bool:
        """Verificar si un nodo contiene alguna estructura de bucle."""
        
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
        Formatear la salida del análisis para su visualización.
        
        Formato:
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
    
    def analyze_function_node(self, func_node, recursive_info):
        """
        Analiza la complejidad asintótica de UNA función específica (nodo AST).
        Este método es vital para el análisis multi-algoritmo de la nueva interfaz.
        
        Args:
            func_node: El nodo FunctionDef del AST.
            recursive_info: Diccionario con info de recursión (has_recursion, pattern_type, etc).
            
        Returns:
            Una tupla (recurrence_obj, bound_obj) compatible con la interfaz gráfica.
        """
        
        # 1. Construir la ecuación (Lógica existente)
        recurrence = self._construct_recurrence(func_node, recursive_info)
        
        # 2. Resolver la complejidad (Lógica existente)
        bound = self._solve_recurrence(recurrence)
        
        # --- CORRECCIÓN DE SEGURIDAD (El cambio clave) ---
        # Si detectamos un patrón lineal recursivo, aseguramos que la complejidad sea "n".
        # Esto evita que salga solo "Θ" sin la "n" en el reporte.
        if recursive_info and recursive_info.get('pattern_type') == 'linear':
             if bound.complexity == "1" or not bound.complexity:
                 bound.complexity = "n"
                 bound.notation = "Θ"
        
        return recurrence, bound