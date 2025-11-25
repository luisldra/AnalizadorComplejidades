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
        
        Args:
            ast: AST del algoritmo
            algorithm_type: Tipo de algoritmo detectado
            recurrence_eq: Ecuación de recurrencia detectada (para validar coherencia)
            complexity: Complejidad asintótica calculada (para validar coherencia)
            
        Returns:
            Dict con 'best', 'worst', 'average' casos
        """
        
        return self._build_math_based_cases(recurrence_eq, complexity)

    def _build_math_based_cases(self, recurrence_eq: Optional[str], complexity: Optional[str]) -> Dict[str, CaseAnalysis]:
        """Genera descripciones basadas únicamente en la información matemática disponible."""
        recurrence_text = recurrence_eq or "No se detectó una ecuación de recurrencia (algoritmo iterativo)."
        complexity_text = complexity or "Complejidad no determinada"

        best_case = CaseAnalysis(
            case_type='best',
            complexity=complexity_text,
            scenario="Se alcanza inmediatamente el caso base; no se expande la recurrencia más allá del primer nivel.",
            ejemplo="Evaluar la ecuación con los valores base declarados.",
            explanation=f"La cota proviene directamente del motor matemático.\nEcuación utilizada: {recurrence_text}"
        )

        worst_case = CaseAnalysis(
            case_type='worst',
            complexity=complexity_text,
            scenario="Se expande la recurrencia completa hasta que n alcanza el caso base.",
            ejemplo="Expandir T(n) de forma simbólica aplicando la ecuación derivada hasta n = 1.",
            explanation=f"El costo refleja la expansión total de {recurrence_text}.\nNo se aplican plantillas heurísticas, solo la ecuación obtenida."
        )

        average_case = CaseAnalysis(
            case_type='average',
            complexity=complexity_text,
            scenario="Sin datos estadísticos adicionales, se asume el mismo comportamiento asintótico.",
            ejemplo="Integrar el aporte de cada nivel de la recurrencia y normalizar por el número de configuraciones.",
            explanation=f"El motor matemático no introduce variaciones heurísticas; reporta la misma cota derivada de {recurrence_text}."
        )

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
        # Extraer el nombre de la función para contexto
        func_name = ""
        if hasattr(ast, 'functions') and ast.functions:
            func_name = ast.functions[0].name.lower()
        
        # REGLA 1: Si la complejidad es O(log n) o Θ(log n), ES búsqueda binaria
        if 'log' in complexity.lower() and '2^' not in complexity and 'n log' not in complexity:
            return 'binary_search'
        
        # REGLA 2: Si la ecuación es T(n-1) + T(n-2), ES Fibonacci
        if 'T(n-1)' in recurrence and 'T(n-2)' in recurrence:
            return 'fibonacci'
        
        # REGLA 3: Si la complejidad es O(n log n), ES divide & conquer
        if 'n log' in complexity.lower() or 'nlog' in complexity.lower():
            return 'divide_conquer'
        
        # REGLA 4: Si la complejidad es O(2^n) o exponencial
        if '2^' in complexity or 'φ^' in complexity or 'exponential' in complexity.lower():
            # Verificar si es Fibonacci específicamente
            if 'fib' in func_name or ('T(n-1)' in recurrence and 'T(n-2)' in recurrence):
                return 'fibonacci'
            else:
                return 'recursive'  # Recursión exponencial genérica
        
        # REGLA 5: Si la ecuación tiene 2 llamadas recursivas con división (merge sort)
        if '2T(n/2)' in recurrence or 'T(n/2)' in recurrence:
            # Verificar que NO sea búsqueda binaria (que solo tiene 1 llamada efectiva)
            recursive_calls = self._count_active_recursive_calls(ast)
            if recursive_calls >= 2:
                return 'divide_conquer'
            else:
                return 'binary_search'
        
        # Si no hay inconsistencias claras, mantener el tipo detectado
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
            return 'fibonacci'  # Detectar Fibonacci ANTES de divide_conquer
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
            for func in ast.functions:
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
        """
        Analiza el mejor caso del algoritmo.
        
        Args:
            ast: AST del algoritmo
            algorithm_type: Tipo de algoritmo detectado
            complexity: Complejidad asintótica para validación (opcional)
        """
        
        # Extraer nombre de función para contexto
        func_name = "algoritmo"
        if hasattr(ast, 'functions') and ast.functions:
            func_name = ast.functions[0].name
        
        best_cases = {
            'fibonacci': CaseAnalysis(
                case_type='best',
                complexity='Θ(1)',
                scenario='Caso base alcanzado inmediatamente (n=0 o n=1)',
                ejemplo=f'{func_name}(0) o {func_name}(1) → retorno directo sin recursión',
                explanation='El algoritmo termina sin recursión cuando n es 0 o 1. Sin embargo, para n>1, siempre es exponencial.'
            ),
            'binary_search': CaseAnalysis(
                case_type='best',
                complexity='Θ(1)',
                scenario='El elemento buscado está en la posición central en la primera comparación',
                ejemplo=f'En {func_name}([1,2,3,4,5], 3): El elemento 3 está en el centro, encontrado inmediatamente',
                explanation='La búsqueda binaria termina en O(1) cuando el elemento está exactamente en el punto medio del espacio de búsqueda inicial.'
            ),
            'divide_conquer': CaseAnalysis(
                case_type='best',
                complexity='Θ(n log n)' if complexity and 'n log' in complexity else 'Θ(n)',
                scenario='Divide & Conquer mantiene su complejidad independiente de la distribución de datos',
                ejemplo=f'{func_name} ejecuta siempre el mismo número de divisiones: log₂(n) niveles',
                explanation='Algoritmos como MergeSort dividen el problema en mitades balanceadas siempre, sin importar si los datos están ordenados o no. El mejor caso coincide con el peor caso.'
            ),
            'recursive': CaseAnalysis(
                case_type='best',
                complexity='Θ(1)',
                scenario='Caso base alcanzado inmediatamente',
                ejemplo=f'{func_name}(0) o {func_name}(1) → retorno directo sin recursión',
                explanation='Cuando la recursión alcanza el caso base sin hacer más llamadas recursivas.'
            ),
            'nested_loops': CaseAnalysis(
                case_type='best',
                complexity='Θ(n²)',
                scenario='Bucles anidados sin condiciones de salida temprana',
                ejemplo='Multiplicación de matrices, bubble sort completo',
                explanation='Bucles anidados ejecutan todas las iteraciones sin optimización'
            ),
            'linear_search': CaseAnalysis(
                case_type='best',
                complexity='Θ(1)',
                scenario='Elemento encontrado en la primera iteración o lista vacía',
                ejemplo='buscar_lineal([5,2,3], 5) → encontrado en posición 0',
                explanation='La búsqueda termina inmediatamente si el elemento está al inicio'
            ),
            'linear_processing': CaseAnalysis(
                case_type='best',
                complexity='Θ(n)',
                scenario='El algoritmo debe procesar todos los elementos (sin salida temprana)',
                ejemplo=f'{func_name}(n) → procesa n elementos en todos los casos',
                explanation='Algoritmos de procesamiento (suma, acumulación, transformación) deben completar todas las iteraciones, sin importar los datos. No hay "mejor caso" que evite el trabajo.'
            ),
            'constant': CaseAnalysis(
                case_type='best',
                complexity='Θ(1)',
                scenario='Operación directa sin iteraciones ni recursión',
                ejemplo='acceso a arreglo, asignación simple',
                explanation='Operaciones de tiempo constante'
            )
        }
        
        return best_cases.get(algorithm_type, CaseAnalysis(
            case_type='best',
            complexity='Θ(1)',
            scenario='Caso base o condición trivial',
            ejemplo='N/A',
            explanation='Mejor escenario posible de ejecución'
        ))
    
    def _analyze_worst_case(self, ast, algorithm_type: str, complexity: str = None) -> CaseAnalysis:
        """
        Analiza el peor caso del algoritmo.
        
        Args:
            ast: AST del algoritmo
            algorithm_type: Tipo de algoritmo detectado
            complexity: Complejidad asintótica para validación (opcional)
        """
        
        # Extraer nombre de función para contexto
        func_name = "algoritmo"
        if hasattr(ast, 'functions') and ast.functions:
            func_name = ast.functions[0].name
        
        worst_cases = {
            'fibonacci': CaseAnalysis(
                case_type='worst',
                complexity='Θ(φⁿ) ≈ Θ(2ⁿ)',
                scenario='Cualquier valor n > 1 (el algoritmo es determinista)',
                ejemplo=f'{func_name}(10) genera ~2¹⁰ ≈ 1024 llamadas recursivas en un árbol binario',
                explanation='Fibonacci recursivo sin memoización SIEMPRE es exponencial. La base exacta es φ≈1.618 (número áureo), pero O(2ⁿ) es la cota superior estándar. No hay "mejor o peor entrada", solo depende de n.'
            ),
            'binary_search': CaseAnalysis(
                case_type='worst',
                complexity='Θ(log n)',
                scenario='El elemento no está en el arreglo o está en una posición que requiere log₂(n) comparaciones',
                ejemplo=f'{func_name}([1,2,3,4,5,6,7,8], 9) → log₂(8) = 3 divisiones hasta espacio vacío',
                explanation='La búsqueda binaria divide el espacio de búsqueda a la mitad en cada paso. En el peor caso, necesita log₂(n) divisiones para reducir el espacio a 0.'
            ),
            'divide_conquer': CaseAnalysis(
                case_type='worst',
                complexity='Θ(n log n)' if complexity and 'n log' in complexity else 'Θ(n²)',
                scenario='MergeSort siempre O(n log n). QuickSort puede degradarse a O(n²) con pivotes malos',
                ejemplo=f'{func_name} con datos en orden inverso o pivotes desbalanceados',
                explanation='MergeSort siempre divide en mitades balanceadas (O(n log n) garantizado). QuickSort puede degradarse a O(n²) si el pivote es siempre el peor elemento.'
            ),
            'recursive': CaseAnalysis(
                case_type='worst',
                complexity='Θ(n)' if complexity and ('log' not in complexity and '2^' not in complexity) else 'Θ(2ⁿ)',
                scenario='Recursión lineal (una llamada por nivel) o exponencial (múltiples llamadas)',
                ejemplo=f'{func_name}(n) con recursión hasta n=0, generando n llamadas secuenciales',
                explanation='Recursión lineal: cada llamada genera una sub-llamada (factorial, suma). Recursión exponencial: múltiples llamadas por nivel (sin memoización).'
            ),
            'nested_loops': CaseAnalysis(
                case_type='worst',
                complexity='Θ(n²) o Θ(n³)',
                scenario='Todos los bucles ejecutan n iteraciones completas',
                ejemplo='bubble_sort con arreglo invertido: [5,4,3,2,1]',
                explanation='Cada elemento debe compararse con todos los demás'
            ),
            'linear_search': CaseAnalysis(
                case_type='worst',
                complexity='Θ(n)',
                scenario='Elemento al final del arreglo o no encontrado',
                ejemplo='buscar_lineal([1,2,3,4,5], 5) → n comparaciones',
                explanation='Se recorre toda la estructura hasta el final'
            ),
            'linear_processing': CaseAnalysis(
                case_type='worst',
                complexity='Θ(n)',
                scenario='El algoritmo debe procesar todos los elementos (sin salida temprana)',
                ejemplo=f'{func_name}(n) → procesa exactamente n elementos',
                explanation='Algoritmos de procesamiento deben completar todas las iteraciones. El "peor caso" coincide con el "mejor caso" porque no hay optimización posible - todos los elementos se procesan.'
            ),
            'constant': CaseAnalysis(
                case_type='worst',
                complexity='Θ(1)',
                scenario='Operación directa sin iteraciones',
                ejemplo='suma = a + b',
                explanation='Tiempo constante independiente del tamaño de entrada'
            )
        }
        
        return worst_cases.get(algorithm_type, CaseAnalysis(
            case_type='worst',
            complexity='Θ(n)',
            scenario='Peor escenario de ejecución',
            ejemplo='N/A',
            explanation='Máximo número de operaciones requeridas'
        ))
    
    def _analyze_average_case(self, ast, algorithm_type: str, complexity: str = None) -> CaseAnalysis:
        """
        Analiza el caso promedio del algoritmo.
        
        Args:
            ast: AST del algoritmo
            algorithm_type: Tipo de algoritmo detectado
            complexity: Complejidad asintótica para validación (opcional)
        """
        
        # Extraer nombre de función para contexto
        func_name = "algoritmo"
        if hasattr(ast, 'functions') and ast.functions:
            func_name = ast.functions[0].name
        
        average_cases = {
            'fibonacci': CaseAnalysis(
                case_type='average',
                complexity='Θ(φⁿ) ≈ Θ(2ⁿ)',
                scenario='Cualquier valor n > 1 (no depende de los datos, solo de n)',
                ejemplo=f'{func_name}(n) siempre genera ~φⁿ llamadas, donde φ = 1.618... (proporción áurea)',
                explanation='Fibonacci recursivo es DETERMINISTA: para un n dado, SIEMPRE ejecuta la misma cantidad de operaciones. No tiene "caso promedio" en el sentido tradicional porque no depende de la disposición de datos. La complejidad es Θ(φⁿ) exactamente, aproximada como O(2ⁿ).'
            ),
            'binary_search': CaseAnalysis(
                case_type='average',
                complexity='Θ(log n)',
                scenario='Elemento en una posición aleatoria del arreglo ordenado',
                ejemplo=f'Promedio de log₂(n) comparaciones para encontrar un elemento al azar',
                explanation='En promedio, la búsqueda binaria requiere ~log₂(n) comparaciones. Cada comparación elimina la mitad del espacio, por lo que en promedio se llega al elemento en tiempo logarítmico.'
            ),
            'divide_conquer': CaseAnalysis(
                case_type='average',
                complexity='Θ(n log n)' if complexity and 'n log' in complexity else 'Θ(n)',
                scenario='Datos de entrada distribuidos aleatoriamente',
                ejemplo=f'{func_name} con pivotes aleatorios o división balanceada típica',
                explanation='En promedio, los algoritmos divide & conquer mantienen O(n log n). QuickSort con pivotes aleatorios evita el peor caso O(n²). MergeSort siempre es O(n log n).'
            ),
            'recursive': CaseAnalysis(
                case_type='average',
                complexity='Θ(n)' if complexity and ('log' not in complexity and '2^' not in complexity) else 'Θ(2ⁿ)',
                scenario='Depende del tipo de recursión: lineal (una llamada) o exponencial (múltiples)',
                ejemplo=f'Recursión lineal: {func_name}(n) hace n llamadas. Recursión exponencial: árbol de llamadas',
                explanation='La complejidad promedio depende de la estructura: lineal T(n)=T(n-1)+c es O(n), exponencial sin memoización es O(2ⁿ).'
            ),
            'nested_loops': CaseAnalysis(
                case_type='average',
                complexity='Θ(n²)',
                scenario='Datos de entrada aleatorios',
                ejemplo='Ordenamiento con comparaciones típicas',
                explanation='Número promedio de comparaciones para datos aleatorios'
            ),
            'linear_search': CaseAnalysis(
                case_type='average',
                complexity='Θ(n/2) = Θ(n)',
                scenario='Elemento en posición aleatoria',
                ejemplo='buscar_lineal → elemento en mitad del arreglo',
                explanation='En promedio, se recorre la mitad de la estructura'
            ),
            'linear_processing': CaseAnalysis(
                case_type='average',
                complexity='Θ(n)',
                scenario='El algoritmo debe procesar todos los elementos',
                ejemplo=f'{func_name}(n) → siempre procesa n elementos',
                explanation='No existe variación en el caso promedio. El algoritmo procesa todos los elementos independientemente de sus valores. El "caso promedio" coincide con el mejor y peor caso.'
            ),
            'constant': CaseAnalysis(
                case_type='average',
                complexity='Θ(1)',
                scenario='Operación directa',
                ejemplo='Asignación o acceso directo',
                explanation='Tiempo constante siempre'
            )
        }
        
        return average_cases.get(algorithm_type, CaseAnalysis(
            case_type='average',
            complexity='Θ(n)',
            scenario='Caso promedio de ejecución',
            ejemplo='N/A',
            explanation='Complejidad esperada para datos aleatorios'
        ))
    
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
