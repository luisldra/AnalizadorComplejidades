"""
Case Analyzer
=============

Analiza el mejor caso, peor caso y caso promedio de algoritmos.

Este módulo identifica y analiza diferentes escenarios de ejecución:
- Mejor caso: Cuando el algoritmo termina en menos tiempo
- Peor caso: Cuando el algoritmo toma el máximo tiempo
- Caso promedio: Cuando el algoritmo procesa datos aleatorios

Classes:
- CaseAnalyzer: Analiza diferentes casos de complejidad
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import sys
import os

# Asegurar que los imports funcionen
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.ast.nodes import (
    Function, Call, For, While, If, Return,
    Assignment, BinOp, Number, Var
)


@dataclass
class CaseAnalysis:
    """Representa el análisis de un caso específico."""
    case_type: str  # 'best', 'worst', 'average'
    complexity: str
    scenario: str  # Descripción del escenario
    ejemplo: str  # Ejemplo concreto
    explanation: str  # Explicación detallada


class CaseAnalyzer:
    """
    Analiza el mejor, peor y caso promedio de algoritmos.
    
    Identifica patrones comunes y escenarios típicos para diferentes
    estructuras algorítmicas.
    """
    
    def __init__(self):
        """Inicializa el analizador de casos."""
        self.analysis_cache: Dict[str, Dict[str, CaseAnalysis]] = {}
    
    def analyze_all_cases(self, ast, algorithm_type: str = 'unknown', 
                      recurrence_eq: str = None, complexity: str = None) -> Dict[str, CaseAnalysis]:
        """
        Analiza todos los casos (mejor, peor, promedio) de un algoritmo.

        Orden de prioridad:
        1) Patrón estructural en el AST (más fiable para casos concretos).
        2) Ecuación de recurrencia / complejidad matemática (para afinar tipo).
        3) Fallback puramente matemático si no hay nada más.
        """
        func_name = ""
        if hasattr(ast, 'functions') and ast.functions:
            func_name = ast.functions[0].name.lower()
        elif hasattr(ast, 'name'):
            func_name = str(ast.name).lower()

        # --- 1) Siempre intentamos detectar el tipo desde el AST ---
        detected_type = 'unknown'
        try:
            detected_type = self._detect_algorithm_type(ast)
        except Exception:
            pass

        # El tipo base es: lo que detectamos en el AST, luego lo que venga de fuera
        algorithm_type = detected_type if detected_type != 'unknown' else (algorithm_type or 'unknown')

        # --- 2) Refinar con recurrencia / complejidad matemática si están disponibles ---
        rec_str = recurrence_eq or ""
        comp_str = complexity or ""
        try:
            if rec_str or comp_str:
                algorithm_type = self._validate_and_refine_type(
                    algorithm_type,
                    rec_str,
                    comp_str,
                    ast
                )
        except Exception:
            # Si algo falla en el refinamiento, seguimos con el tipo que teníamos
            pass

        # Si no tenemos nada de info matemática, usamos el fallback puramente matemático ---
        if not complexity and not recurrence_eq:
            return self._build_math_based_cases(recurrence_eq, complexity)

        # Construir los tres casos en función del tipo que quedó ---
        best_case = self._analyze_best_case(ast, algorithm_type, comp_str)
        worst_case = self._analyze_worst_case(ast, algorithm_type, comp_str)
        average_case = self._analyze_average_case(ast, algorithm_type, comp_str)

        return {
            'best': best_case,
            'worst': worst_case,
            'average': average_case
        }

    
    def _validate_and_refine_type(self, detected_type: str, recurrence: str,
                                  complexity: str, ast) -> str:
        """
        Valida que el tipo detectado sea coherente con la ecuación y complejidad.
        Refina el tipo si hay inconsistencias.
        """
        recurrence = (recurrence or "").replace(" ", "")
        complexity_low = (complexity or "").lower()

        # --- FIBONACCI / EXPONENCIAL ---
        if "t(n-1)" in recurrence and "t(n-2)" in recurrence:
            return "fibonacci"

        # --- BÚSQUEDA BINARIA ---
        # Patrones típicos:
        #  - recurrencia con T(n/2)
        #  - complejidad logarítmica
        if "t(n/2)" in recurrence or "t(n/2)+o(1)" in recurrence:
            if "log" in complexity_low and "nlog" not in complexity_low and "2^" not in complexity_low:
                return "binary_search"

        if self._has_binary_search_pattern(ast):
            return "binary_search"

        # --- DIVIDE & CONQUER GENERAL (merge sort, quick sort bueno, etc.) ---
        if "nlog" in complexity_low or "n*log" in complexity_low:
            return "divide_conquer"

        # --- EXPONENCIAL GENERAL ---
        if "2^" in complexity_low or "exp(" in complexity_low or "2" in complexity_low:
            # Si el patrón AST es fibonacciesco pero el nombre no lo dice
            recursive_calls = self._count_active_recursive_calls(ast)
            if recursive_calls >= 2:
                return "fibonacci"
            return "recursive"

        # Si nada de lo anterior aplica, nos quedamos con el tipo detectado por estructuras
        return detected_type


    
    def _count_active_recursive_calls(self, ast) -> int:
        """
        Cuenta llamadas recursivas que REALMENTE se ejecutan (no en ramas exclusivas de if).
        """
        if hasattr(ast, 'functions') and ast.functions:
            func = ast.functions[0]
            return self._count_recursive_calls(func, func.name)
        return 0
    
    def _detect_algorithm_type(self, ast) -> str:
        """Detecta el tipo de algoritmo a partir del AST."""
        
        # Buscar patrones conocidos
        has_recursion = self._has_recursion(ast)
        has_loops = self._has_loops(ast)
        has_divide_conquer = self._has_divide_conquer_pattern(ast)
        has_binary_search = self._has_binary_search_pattern(ast)
        is_fibonacci = self._is_fibonacci_pattern(ast)
        
        if has_binary_search:
            return 'binary_search'
        elif is_fibonacci:
            return 'fibonacci' 
        elif has_divide_conquer:
            return 'divide_conquer'
        elif has_recursion:
            return 'recursive'
        elif has_loops:
            nested_level = self._count_nested_loops(ast)
            if nested_level >= 2:
                return 'nested_loops'
            else:
                # Distinguir búsqueda (puede terminar early) de procesamiento (debe completar)
                has_early_return = self._has_early_return_in_loop(ast)
                if has_early_return:
                    return 'linear_search'  # Búsqueda lineal
                else:
                    return 'linear_processing'  # Procesamiento lineal (suma, acumulación, etc.)
        else:
            return 'constant'
    
    def _has_recursion(self, node) -> bool:
        """Verifica si hay llamadas recursivas."""
        if isinstance(node, Function):
            return self._check_recursive_calls(node, node.name)
        elif hasattr(node, 'functions'):
            for func in node.functions:
                if self._check_recursive_calls(func, func.name):
                    return True
        return False
    
    def _check_recursive_calls(self, node, func_name: str) -> bool:
        """Busca llamadas recursivas en un nodo."""
        if isinstance(node, Call) and node.name == func_name:
            return True
        
        # Buscar en atributos
        for attr_name in dir(node):
            if attr_name.startswith('_'):
                continue
            attr = getattr(node, attr_name)
            if isinstance(attr, (list, tuple)):
                for item in attr:
                    if hasattr(item, '__dict__') and self._check_recursive_calls(item, func_name):
                        return True
            elif hasattr(attr, '__dict__'):
                if self._check_recursive_calls(attr, func_name):
                    return True
        
        return False
    
    def _has_loops(self, node) -> bool:
        """Verifica si hay bucles en el código."""
        if isinstance(node, (For, While)):
            return True
        
        for attr_name in dir(node):
            if attr_name.startswith('_'):
                continue
            attr = getattr(node, attr_name)
            if isinstance(attr, (list, tuple)):
                for item in attr:
                    if hasattr(item, '__dict__') and self._has_loops(item):
                        return True
            elif hasattr(attr, '__dict__'):
                if self._has_loops(attr):
                    return True
        
        return False
    
    def _has_early_return_in_loop(self, node) -> bool:
        """
        Detecta si hay retornos dentro de bucles (patrón de búsqueda).
        Un algoritmo de búsqueda puede terminar antes si encuentra el elemento.
        Un algoritmo de procesamiento debe completar todas las iteraciones.
        """
        if isinstance(node, (For, While)):
            # Estamos dentro de un bucle, buscar Return en el cuerpo
            if hasattr(node, 'body'):
                for stmt in node.body:
                    if isinstance(stmt, Return):
                        return True
                    # Buscar Return dentro de if dentro del bucle
                    if isinstance(stmt, If):
                        if self._has_return_in_if(stmt):
                            return True
        
        # Buscar recursivamente en otros nodos
        for attr_name in dir(node):
            if attr_name.startswith('_'):
                continue
            attr = getattr(node, attr_name)
            if isinstance(attr, (list, tuple)):
                for item in attr:
                    if hasattr(item, '__dict__') and self._has_early_return_in_loop(item):
                        return True
            elif hasattr(attr, '__dict__'):
                if self._has_early_return_in_loop(attr):
                    return True
        
        return False
    
    def _has_return_in_if(self, if_node: If) -> bool:
        """Verifica si un nodo If contiene un Return."""
        if if_node.then_block:
            for stmt in if_node.then_block:
                if isinstance(stmt, Return):
                    return True
        if if_node.else_block:
            for stmt in if_node.else_block:
                if isinstance(stmt, Return):
                    return True
        return False
    
    def _count_nested_loops(self, node, depth: int = 0) -> int:
        """Cuenta el nivel de anidamiento de bucles."""
        max_depth = depth
        
        if isinstance(node, (For, While)):
            depth += 1
            max_depth = depth
            
            # Analizar el cuerpo del bucle
            if hasattr(node, 'body'):
                for stmt in node.body:
                    nested = self._count_nested_loops(stmt, depth)
                    max_depth = max(max_depth, nested)
        else:
            # Buscar en atributos
            for attr_name in dir(node):
                if attr_name.startswith('_'):
                    continue
                attr = getattr(node, attr_name)
                if isinstance(attr, (list, tuple)):
                    for item in attr:
                        if hasattr(item, '__dict__'):
                            nested = self._count_nested_loops(item, depth)
                            max_depth = max(max_depth, nested)
                elif hasattr(attr, '__dict__'):
                    nested = self._count_nested_loops(attr, depth)
                    max_depth = max(max_depth, nested)
        
        return max_depth
    
    def _has_divide_conquer_pattern(self, ast) -> bool:
        """Detecta patrón de dividir y conquistar."""
        # Buscar funciones con llamadas recursivas múltiples y división del problema
        if hasattr(ast, 'functions'):
            funcs = ast.functions
        elif isinstance(ast, Function):
            funcs = [ast]
        else:
            funcs = []

        for func in funcs:
            recursive_calls = self._count_recursive_calls(func, func.name)
            if recursive_calls >= 2:  # Merge sort, quicksort, etc.
                return True
        return False
    
    def _count_recursive_calls(self, node, func_name: str) -> int:
        """Cuenta el número de llamadas recursivas."""
        count = 0
        
        if isinstance(node, Call) and node.name == func_name:
            count += 1
        
        for attr_name in dir(node):
            if attr_name.startswith('_'):
                continue
            attr = getattr(node, attr_name)
            if isinstance(attr, (list, tuple)):
                for item in attr:
                    if hasattr(item, '__dict__'):
                        count += self._count_recursive_calls(item, func_name)
            elif hasattr(attr, '__dict__'):
                count += self._count_recursive_calls(attr, func_name)
        
        return count
    
    def _has_binary_search_pattern(self, ast) -> bool:
        """Detecta patrón de búsqueda binaria."""
        # Buscar división repetida del espacio de búsqueda
        if hasattr(ast, 'functions'):
            for func in ast.functions:
                if self._check_binary_division(func):
                    return True
        return False
    
    def _check_binary_division(self, node) -> bool:
        """Verifica si hay división binaria del problema."""
        # Buscar patrones como mid = (left + right) / 2
        if isinstance(node, Assignment):
            if hasattr(node, 'value') and isinstance(node.value, BinOp):
                if node.value.op == '/':
                    return True
        
        for attr_name in dir(node):
            if attr_name.startswith('_'):
                continue
            attr = getattr(node, attr_name)
            if isinstance(attr, (list, tuple)):
                for item in attr:
                    if hasattr(item, '__dict__') and self._check_binary_division(item):
                        return True
            elif hasattr(attr, '__dict__'):
                if self._check_binary_division(attr):
                    return True
        
        return False
    
    def _is_fibonacci_pattern(self, ast) -> bool:
        """
        Detecta el patrón específico de Fibonacci: T(n) = T(n-1) + T(n-2).
        
        Características:
        - 2 llamadas recursivas
        - Argumentos con decrementos de 1 y 2
        - Nombre típico: fibonacci, fib
        """
        if hasattr(ast, 'functions'):
            for func in ast.functions:
                # Verificar nombre
                func_name = func.name.lower()
                if 'fib' in func_name:
                    # Contar llamadas recursivas
                    recursive_calls = self._count_recursive_calls(func, func.name)
                    if recursive_calls == 2:
                        return True
                
                # Verificar patrón sin importar el nombre
                elif self._count_recursive_calls(func, func.name) == 2:
                    # Verificar que tenga patrón de decremento característico
                    if self._has_fibonacci_decrement_pattern(func):
                        return True
        
        return False
    
    def _is_prime_like_pattern(self, ast) -> bool:

        if hasattr(ast, 'functions') and ast.functions:
            func = ast.functions[0]
            name = func.name.lower()
            if 'primo' in name or 'prime' in name:
                return True

        return self._has_modulo_guard_with_return(ast)

    def _has_modulo_guard_with_return(self, node) -> bool:
        """
        Busca un patrón 'if (algo % algo == 0) then return ...' dentro de un bucle.
        """
        # Si es un bucle, miramos su cuerpo
        if isinstance(node, (For, While)):
            body = getattr(node, 'body', []) or []
            for stmt in body:
                # if (...) { ... return ... }
                if isinstance(stmt, If):
                    if self._condition_has_modulo(stmt.condition) and self._has_return_in_if(stmt):
                        return True

        # Recorrer recursivamente el resto del AST
        for attr_name in dir(node):
            if attr_name.startswith('_'):
                continue
            attr = getattr(node, attr_name)
            if isinstance(attr, (list, tuple)):
                for item in attr:
                    if hasattr(item, '__dict__'):
                        if self._has_modulo_guard_with_return(item):
                            return True
            elif hasattr(attr, '__dict__'):
                if self._has_modulo_guard_with_return(attr):
                    return True

        return False

    def _is_prime_like_pattern_safe(self, ast) -> bool:
        """
        Wrapper seguro para detectar el patrón de primalidad evitando errores de metadatos.
        """
        try:
            return self._is_prime_like_pattern(ast)
        except Exception:
            return False

    def _condition_has_modulo(self, cond) -> bool:
        """
        Devuelve True si la condición (o sub-expresiones) contiene una operación módulo '%'.
        """
        if isinstance(cond, BinOp) and getattr(cond, 'op', None) == '%':
            return True

        # Buscar recursivamente en subexpresiones
        for attr_name in dir(cond):
            if attr_name.startswith('_'):
                continue
            attr = getattr(cond, attr_name)
            if isinstance(attr, (list, tuple)):
                for item in attr:
                    if hasattr(item, '__dict__') and self._condition_has_modulo(item):
                        return True
            elif hasattr(attr, '__dict__'):
                if self._condition_has_modulo(attr):
                    return True

        return False

    
    def _has_fibonacci_decrement_pattern(self, node) -> bool:
        """
        Verifica si las llamadas recursivas tienen el patrón n-1 y n-2.
        """
        # Buscar patrones BinOp con '-' y valores 1 y 2
        decrements = []
        
        if isinstance(node, Call):
            for arg in node.args:
                if isinstance(arg, BinOp) and arg.op == '-':
                    if isinstance(arg.right, Number):
                        decrements.append(arg.right.value)
        
        for attr_name in dir(node):
            if attr_name.startswith('_'):
                continue
            attr = getattr(node, attr_name)
            if isinstance(attr, (list, tuple)):
                for item in attr:
                    if hasattr(item, '__dict__'):
                        if self._has_fibonacci_decrement_pattern(item):
                            return True
            elif hasattr(attr, '__dict__'):
                if self._has_fibonacci_decrement_pattern(attr):
                    return True
        
        # Verificar si encontramos los decrementos 1 y 2
        return 1 in decrements and 2 in decrements
    
    def _analyze_best_case(self, ast, algorithm_type: str, complexity: str = None) -> CaseAnalysis:
        func_name = "algoritmo"
        if hasattr(ast, 'functions') and ast.functions:
            func_name = ast.functions[0].name

        comp = complexity or ""

        best_cases = {
            "fibonacci": CaseAnalysis(
                case_type="best",
                complexity=comp or "Θ(2ⁿ)",
                scenario="Para n > 1 el árbol recursivo completo siempre se genera; no hay entradas “más fáciles”.",
                ejemplo=f"{func_name}(n) con n > 1 ejecuta siempre el mismo patrón de llamadas.",
                explanation=(
                    "Fibonacci recursivo sin memoización es determinista: para cada n > 1 el número de llamadas está fijado. "
                    "Asintóticamente, mejor, peor y promedio coinciden en Θ(2ⁿ). Para n = 0 o n = 1 el coste se reduce a Θ(1)."
                ),
            ),
            'binary_search': CaseAnalysis(
                case_type='best',
                complexity='Θ(1)',
                scenario='El elemento buscado está justo en la posición central en la primera comparación.',
                ejemplo=f'{func_name}([1,2,3,4,5], 3) → se encuentra en el primer intento.',
                explanation='En el mejor caso sólo se realiza una comparación antes de retornar el resultado.'
            ),
            'prime_test': CaseAnalysis(
                case_type='best',
                complexity='Θ(1)',
                scenario='Se detecta un caso trivial (n ≤ 1) o un divisor muy pequeño en la primera iteración.',
                ejemplo=f'{func_name}(1), {func_name}(0) o {func_name}(4) → se devuelve enseguida.',
                explanation=('El mejor caso ocurre cuando se sale por el caso base n ≤ 1 o cuando el primer divisor probado '
                             'divide a n (por ejemplo i = 2 en un bucle que prueba divisores).')
            ),
            "recursive": CaseAnalysis(
                case_type="best",
                complexity=comp or "Θ(n)",
                scenario="Recursión determinista sin ramas de salida temprana dependientes de los datos.",
                ejemplo=f"{func_name}(n) recorre siempre la misma profundidad de recursión para ese n (como factorial).",
                explanation=(
                    "Cuando la recursión sólo depende del parámetro de tamaño (ej. factorial), "
                    "todas las entradas de tamaño n inducen el mismo trabajo. "
                    "Asintóticamente, la mejor cota coincide con la peor y la promedio."
                ),
            ),
            "binary_search": CaseAnalysis(
                case_type="best",
                complexity="Θ(1)",
                scenario="El elemento buscado está exactamente en la posición central en la primera comparación.",
                ejemplo=f"{func_name}([1,2,3,4,5], 3) → se encuentra en la primera comparación.",
                explanation="En el mejor caso la búsqueda binaria termina tras una sola comparación.",
            ),
            "linear_search": CaseAnalysis(
                case_type="best",
                complexity="Θ(1)",
                scenario="El elemento buscado aparece en la primera posición o la estructura está vacía.",
                ejemplo="buscar_lineal([5,2,3], 5) → encontrado en el índice 0.",
                explanation="La búsqueda lineal puede terminar tras revisar únicamente el primer elemento.",
            ),
            "linear_processing": CaseAnalysis(
                case_type="best",
                complexity=comp or "Θ(n)",
                scenario="El algoritmo debe procesar todos los elementos sin posibilidad de cortar antes.",
                ejemplo=f"{func_name}(n) → recorre todos los elementos (por ejemplo, suma de un arreglo).",
                explanation=(
                    "En algoritmos de procesamiento puro (suma, acumulación, transformación), "
                    "no hay condición de salida temprana: siempre se recorre toda la entrada."
                ),
            ),
            "constant": CaseAnalysis(
                case_type="best",
                complexity="Θ(1)",
                scenario="Operación directa sin iteraciones ni recursión.",
                ejemplo="asignación simple, acceso a una posición de un arreglo.",
                explanation="El tiempo de ejecución no depende del tamaño de la entrada.",
            ),
        }

        # Algoritmos divide & conquer tipo MergeSort / QuickSort (mejor caso)
        if algorithm_type == "divide_conquer":
            return CaseAnalysis(
                case_type="best",
                complexity="Θ(n log n)",
                scenario="La estrategia divide-y-vencerás se aplica con particiones razonablemente balanceadas.",
                ejemplo=f"{func_name}(n) realiza ~log₂(n) niveles de división con trabajo lineal por nivel.",
                explanation=(
                    "En algoritmos como MergeSort y QuickSort (con pivote razonable), el número de niveles es O(log n) "
                    "y cada nivel hace trabajo O(n), dando lugar a Θ(n log n) incluso en el mejor caso asintótico."
                ),
            )

        # Bucles anidados sin early break: mejor caso = mismo orden que el peor
        if algorithm_type == "nested_loops":
            return CaseAnalysis(
                case_type="best",
                complexity=comp or "Θ(n²)",
                scenario="Bucles anidados sin corte anticipado; los rangos se recorren completos.",
                ejemplo="Triple bucle, multiplicación de matrices, bubble_sort sin optimizaciones.",
                explanation=(
                    "Si no hay break / return de salida temprana, el número de iteraciones de los bucles anidados "
                    "depende sólo de n. El mejor caso es del mismo orden que el peor."
                ),
            )

        # Si tenemos un caso específico en el diccionario, lo usamos
        if algorithm_type in best_cases:
            return best_cases[algorithm_type]

        # Fallback genérico
        return CaseAnalysis(
            case_type="best",
            complexity=comp or "Θ(1)",
            scenario="Caso base o condición trivial.",
            ejemplo="N/A",
            explanation="Mejor escenario posible de ejecución.",
        )

    
    def _analyze_worst_case(self, ast, algorithm_type: str, complexity: str = None) -> CaseAnalysis:
        """Analiza el peor caso del algoritmo."""
        func_name = "algoritmo"
        if hasattr(ast, 'functions') and ast.functions:
            func_name = ast.functions[0].name

        comp = complexity or ""

        # nested_loops: el peor caso es exactamente la cota que dio el motor matemático
        if algorithm_type == "nested_loops":
            return CaseAnalysis(
                case_type="worst",
                complexity=comp or "Θ(n²)",
                scenario="Todos los bucles anidados recorren su rango completo.",
                ejemplo="bubble_sort con arreglo invertido; triple bucle sobre n.",
                explanation=(
                    "El motor matemático determinó la expresión de coste y su orden dominante; "
                    "el peor caso coincide con esa cota (por ejemplo Θ(n²), Θ(n³), etc.)."
                ),
            )

        # divide_conquer: diferenciamos entre MergeSort y QuickSort aproximando via AST
        if algorithm_type == "divide_conquer":
            # Heurística simple: si el nombre de la función o variables contienen 'quick' o 'pivot',
            # asumimos QuickSort (peor caso n²); en otro caso, MergeSort-like (n log n).
            func_lower = func_name.lower()
            is_quick = "quick" in func_lower or "qsort" in func_lower

            # Buscar identificadores tipo 'pivot' / 'pivote' en el AST
            if hasattr(ast, "functions") and ast.functions:
                for f in ast.functions:
                    for attr_name in dir(f):
                        if attr_name.startswith("_"):
                            continue
                        attr = getattr(f, attr_name)
                        if isinstance(attr, Var):
                            name = getattr(attr, "name", "").lower()
                            if "pivot" in name or "pivote" in name:
                                is_quick = True

            if is_quick:
                return CaseAnalysis(
                    case_type="worst",
                    complexity="Θ(n²)",
                    scenario="Particiones extremadamente desbalanceadas (pivote siempre el mínimo o máximo).",
                    ejemplo=f"{func_name} sobre un arreglo ya ordenado usando siempre el primer elemento como pivote.",
                    explanation=(
                        "En QuickSort, si el pivote parte el arreglo en 1 y n-1 elementos en cada llamada, "
                        "se obtiene la recurrencia T(n) = T(n-1) + O(n), cuya solución es Θ(n²)."
                    ),
                )
            else:
                return CaseAnalysis(
                    case_type="worst",
                    complexity=comp or "Θ(n log n)",
                    scenario="División razonablemente balanceada en cada nivel de recursión.",
                    ejemplo=f"{func_name}(n) tipo MergeSort con particiones en mitades.",
                    explanation=(
                        "Cuando la estrategia de división no depende adversamente de la distribución de datos, "
                        "la recurrencia T(n) = 2T(n/2) + O(n) se resuelve como Θ(n log n)."
                    ),
                )

        if algorithm_type == "recursive":
            return CaseAnalysis(
                case_type="worst",
                complexity=comp or "Θ(n)",
                scenario="Profundidad de recursión máxima para entradas de tamaño n.",
                ejemplo=f"{func_name}(n) recursivo sin poda ni memoización.",
                explanation=(
                    "La cota asintótica del peor caso coincide con la que devuelve el motor matemático "
                    "(por ejemplo Θ(n) para factorial, Θ(2ⁿ) para recursiones exponenciales)."
                ),
            )

        worst_cases = {
            "fibonacci": CaseAnalysis(
                case_type="worst",
                complexity="Θ(2ⁿ) ≈ Θ(2ⁿ)",
                scenario="Cualquier valor n > 1 (el algoritmo es determinista).",
                ejemplo=f"{func_name}(10) genera ~2¹⁰ ≈ 1024 llamadas recursivas en un árbol binario.",
                explanation=(
                    "Fibonacci recursivo sin memoización SIEMPRE es exponencial. La base exacta es 2≈1.618, "
                    "pero O(2ⁿ) es la cota superior estándar. No hay 'mejor o peor entrada', sólo depende de n."
                ),
            ),
            'binary_search': CaseAnalysis(
                case_type='worst',
                complexity='Θ(log n)',
                scenario='El elemento no está en el arreglo o se encuentra tras descartar casi todos los subarreglos.',
                ejemplo=f'{func_name}([1,2,3,4,5,6,7,8], 9) → se exploran ~log₂(n) divisiones.',
                explanation=('Cada comparación reduce el espacio de búsqueda a la mitad. '
                             'En el peor caso se requieren O(log n) pasos antes de determinar la posición o ausencia.')
            ),
            'prime_test': CaseAnalysis(
                case_type='worst',
                complexity='Θ(n)',
                scenario='n es primo o no tiene divisores pequeños; el bucle recorre todos los candidatos.',
                ejemplo=f'{func_name}(p) donde p es primo grande → se prueban todos los i desde 2 hasta n-1.',
                explanation=('En el peor caso se comprueban todos los posibles divisores hasta n-1, '
                             'lo que implica un número lineal de iteraciones en n.')
            ),
            "binary_search": CaseAnalysis(
                case_type="worst",
                complexity="Θ(log n)",
                scenario="El elemento no está en el arreglo o está en una posición que requiere todas las divisiones.",
                ejemplo=f"{func_name}([1,2,3,4,5,6,7,8], 9) → log₂(8) divisiones hasta espacio vacío.",
                explanation=(
                    "La búsqueda binaria divide el espacio de búsqueda a la mitad en cada paso. "
                    "En el peor caso necesita Θ(log n) comparaciones."
                ),
            ),
            "linear_search": CaseAnalysis(
                case_type="worst",
                complexity="Θ(n)",
                scenario="Elemento al final del arreglo o no encontrado.",
                ejemplo="buscar_lineal([1,2,3,4,5], 5) → n comparaciones.",
                explanation="Se recorre toda la estructura hasta el final.",
            ),
            "linear_processing": CaseAnalysis(
                case_type="worst",
                complexity=comp or "Θ(n)",
                scenario="El algoritmo debe procesar todos los elementos (sin salida temprana).",
                ejemplo=f"{func_name}(n) → procesa exactamente n elementos.",
                explanation=(
                    "Algoritmos de procesamiento deben completar todas las iteraciones. "
                    "El 'peor caso' coincide con el 'mejor caso' porque no hay optimización posible."
                ),
            ),
            "constant": CaseAnalysis(
                case_type="worst",
                complexity="Θ(1)",
                scenario="Operación directa sin iteraciones ni recursión.",
                ejemplo="suma = a + b.",
                explanation="Tiempo constante independiente del tamaño de entrada.",
            ),
        }

        return worst_cases.get(
            algorithm_type,
            CaseAnalysis(
                case_type="worst",
                complexity=comp or "Θ(n)",
                scenario="Peor escenario de ejecución.",
                ejemplo="N/A",
                explanation="Máximo número de operaciones requeridas.",
            ),
        )

    
    def _analyze_average_case(self, ast, algorithm_type: str, complexity: str = None) -> CaseAnalysis:
        """Analiza el caso promedio del algoritmo."""
        func_name = "algoritmo"
        if hasattr(ast, 'functions') and ast.functions:
            func_name = ast.functions[0].name

        comp = complexity or ""

        average_cases = {
            "fibonacci": CaseAnalysis(
                case_type="average",
                complexity="Θ(2ⁿ) ≈ Θ(2ⁿ)",
                scenario="Cualquier valor n > 1 (no depende de los datos, solo de n).",
                ejemplo=f"{func_name}(n) siempre genera ~2ⁿ llamadas, donde 2 = 1.618...",
                explanation=(
                    "Fibonacci recursivo es determinista: para un n dado, siempre ejecuta la misma cantidad de operaciones. "
                    "No tiene 'caso promedio' en el sentido tradicional porque no depende de la disposición de datos."
                ),
            ),
            'binary_search': CaseAnalysis(
                case_type='average',
                complexity='Θ(log n)',
                scenario='El elemento buscado está en una posición aleatoria del arreglo ordenado o puede no estar.',
                ejemplo='En promedio se realizan ~log₂(n) comparaciones.',
                explanation=('Cada comparación descarta la mitad del espacio; para claves aleatorias o presencia/ausencia '
                             'aleatoria, el número esperado de pasos es proporcional a log n.')
            ),
            'prime_test': CaseAnalysis(
                case_type='average',
                complexity='Θ(n)',
                scenario='n es un entero cualquiera, sin sesgo especial hacia primos o compuestos fáciles.',
                ejemplo=f'En promedio se comprueba una fracción de los posibles divisores antes de encontrar uno o concluir primalidad.',
                explanation=('Aunque muchas entradas compuestas se descartan antes de probar todos los divisores, '
                             'asintóticamente la cantidad esperada de iteraciones sigue siendo lineal en n.')
            ),
            "divide_conquer": CaseAnalysis(
                case_type="average",
                complexity="Θ(n log n)",
                scenario="Datos de entrada distribuidos aleatoriamente.",
                ejemplo=f"{func_name} con pivotes aleatorios o divisiones razonablemente balanceadas.",
                explanation=(
                    "En promedio, los algoritmos divide & conquer mantienen Θ(n log n). "
                    "QuickSort con pivotes aleatorios evita el peor caso Θ(n²); MergeSort siempre es Θ(n log n)."
                ),
            ),
            "recursive": CaseAnalysis(
                case_type="average",
                complexity=comp or "Θ(n)",
                scenario="Depende del tipo de recursión: lineal (una llamada) o exponencial (múltiples).",
                ejemplo=f"Recursión lineal: {func_name}(n) hace n llamadas; recursión exponencial: árbol de llamadas completo.",
                explanation=(
                    "La complejidad promedio depende de la estructura: lineal T(n)=T(n-1)+c es Θ(n), "
                    "exponencial sin memoización es Θ(2ⁿ)."
                ),
            ),
            "nested_loops": CaseAnalysis(
                case_type="average",
                complexity=comp or "Θ(n²)",
                scenario="Datos de entrada aleatorios sin cambios en los límites de los bucles.",
                ejemplo="Ordenamientos y algoritmos con bucles anidados que siempre recorren sus rangos completos.",
                explanation=(
                    "Si los límites de los bucles no dependen de la distribución de datos, "
                    "el caso promedio tiene el mismo orden que el peor y el mejor caso."
                ),
            ),
            "linear_search": CaseAnalysis(
                case_type="average",
                complexity="Θ(n/2) = Θ(n)",
                scenario="Elemento en posición aleatoria.",
                ejemplo="buscar_lineal → elemento en mitad del arreglo en promedio.",
                explanation="En promedio, se recorre la mitad de la estructura.",
            ),
            "linear_processing": CaseAnalysis(
                case_type="average",
                complexity=comp or "Θ(n)",
                scenario="El algoritmo procesa todos los elementos independientemente de sus valores.",
                ejemplo=f"{func_name}(n) → siempre procesa n elementos.",
                explanation=(
                    "No existe variación relevante en el caso promedio: el algoritmo procesa todos los elementos "
                    "independientemente de su contenido."
                ),
            ),
            "constant": CaseAnalysis(
                case_type="average",
                complexity="Θ(1)",
                scenario="Operación directa.",
                ejemplo="Asignación o acceso directo.",
                explanation="Tiempo constante siempre.",
            ),
        }

        return average_cases.get(
            algorithm_type,
            CaseAnalysis(
                case_type="average",
                complexity=comp or "Θ(n)",
                scenario="Caso promedio de ejecución.",
                ejemplo="N/A",
                explanation="Complejidad esperada para datos aleatorios.",
            ),
        )

    def get_case_comparison_summary(self, cases: Dict[str, CaseAnalysis]) -> str:
        """
        Genera un resumen comparativo de todos los casos.
        
        Args:
            cases: Dict con análisis de mejor, peor y caso promedio
            
        Returns:
            String con resumen formateado
        """
        
        summary = "═" * 70 + "\n"
        summary += "ANÁLISIS COMPARATIVO DE CASOS\n"
        summary += "═" * 70 + "\n\n"
        
        for case_name, analysis in cases.items():
            summary += f"{'━' * 70}\n"
            summary += f"{case_name.upper()} CASO ({analysis.case_type.upper()})\n"
            summary += f"{'━' * 70}\n"
            summary += f"📊 Complejidad:  {analysis.complexity}\n"
            summary += f"📋 Escenario:    {analysis.scenario}\n"
            summary += f"💡 Ejemplo:      {analysis.ejemplo}\n"
            summary += f"📖 Explicación:  {analysis.explanation}\n\n"
        
        summary += "═" * 70 + "\n"
        
        return summary
