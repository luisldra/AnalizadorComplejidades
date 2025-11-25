"""
Analizador de Complejidad Avanzado
============================

Este módulo proporciona un análisis de complejidad completo para algoritmos de pseudocódigo, compatible con las notaciones Big O (peor caso), Omega (mejor caso) y Theta (límite estricto).

El analizador recorre el AST y aplica reglas de análisis de complejidad basadas en construcciones algorítmicas como bucles, condicionales, recursión y operaciones con estructuras de datos.
"""

from src.ast.nodes import *
from dataclasses import dataclass
from typing import Dict, List, Optional, Union
import re


@dataclass
class ComplexityResult:
    """Representa el resultado del análisis de complejidad con notaciones O, Ω y Θ."""
    big_o: str          # Peor caso (cota superior)
    omega: str          # Mejor caso (cota inferior)  
    theta: Optional[str] = None  # Cota estricta (cuando O = Ω)
    
    def __post_init__(self):
        """Calcular Theta si O y Omega son iguales."""
        if self.big_o == self.omega:
            self.theta = self.big_o
    
    def __str__(self):
        result = f"O({self.big_o}), Ω({self.omega})"
        if self.theta:
            result += f", Θ({self.theta})"
        return result


class ComplexityFunction:
    """Representa una función de complejidad para operaciones matemáticas."""
    
    def __init__(self, expression: str):
        self.expression = expression
        self.degree = self._calculate_degree()
    
    def _calculate_degree(self) -> int:
        """Calcular el grado polinomial de la función de complejidad."""
        if "log" in self.expression:
            return 0.5  # log n crece más lento que lineal
        elif "^" in self.expression:
            # Extraer la potencia más alta
            powers = re.findall(r'\^(\d+)', self.expression)
            return max(int(p) for p in powers) if powers else 1
        elif "n" in self.expression:
            return 1
        else:
            return 0  # constante
    
    def __str__(self):
        return self.expression
    
    def __eq__(self, other):
        return isinstance(other, ComplexityFunction) and self.expression == other.expression
    
    def __lt__(self, other):
        return self.degree < other.degree


class AdvancedComplexityAnalyzer:
    """
    Analizador de complejidad avanzado compatible con las notaciones O, Ω y Θ.

    Reglas de análisis:
    - Constantes: O(1), Ω(1), Θ(1)
    - Bucles simples: O(n), Ω(n), Θ(n)
    - Bucles anidados: O(n^k), donde k es la profundidad de anidación
    - Condicionales: max(ramas) para O, min(ramas) para Ω
    - Matrices: depende del patrón de acceso
    - Recursión: análisis basado en relaciones de recurrencia
    """
    
    def __init__(self):
        self.loop_depth = 0
        self.recursive_calls = {}
        
    def analyze(self, node) -> ComplexityResult:
        """Punto de entrada principal para el análisis de complejidad."""
        # Primero, detectar funciones recursivas
        self._detect_recursive_functions(node)
        return self._analyze_node(node)
    
    def _analyze_node(self, node) -> ComplexityResult:
        """Despachar al método de análisis apropiado según el tipo de nodo."""
        method_name = f"_analyze_{type(node).__name__.lower()}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(node)
        else:
            # Caso por defecto para nodos desconocidos
            return ComplexityResult("1", "1")
    
    # ========== Análisis de Estructura del Programa ==========
    
    def _analyze_program(self, node: Program) -> ComplexityResult:
        """Analizar programa completo - combina las complejidades de todas las funciones."""
        if not node.functions:
            return ComplexityResult("1", "1")
        
        # Para programas con múltiples funciones, típicamente analizamos la función principal
        # o retornamos la complejidad máxima entre todas las funciones
        results = [self._analyze_node(func) for func in node.functions]
        return self._combine_parallel(results)
    
    def _analyze_function(self, node: Function) -> ComplexityResult:
        """Analizar cuerpo de función - maneja funciones recursivas especialmente."""
        if not node.body:
            return ComplexityResult("1", "1")
        
        # Verificar si esta es una función recursiva
        if node.name and node.name in self.recursive_calls:
            return self._analyze_recursive_function(node)
        
        # Función no recursiva - combinar declaraciones secuencialmente
        results = [self._analyze_node(stmt) for stmt in node.body]
        return self._combine_sequential(results)
    
    # ========== Análisis de Sentencias ==========
    
    def _analyze_assignment(self, node: Assignment) -> ComplexityResult:
        """Analizar asignación - depende de la complejidad de la expresión RHS."""
        rhs_complexity = self._analyze_node(node.expr)
        
        # Verificar si LHS es acceso a arreglo/matriz (afecta la complejidad)
        if isinstance(node.name, (ArrayAccess, MatrixAccess)):
            access_complexity = self._analyze_node(node.name)
            return self._combine_sequential([rhs_complexity, access_complexity])
        
        return rhs_complexity
    
    def _analyze_for(self, node: For) -> ComplexityResult:
        """Analizar bucle for - multiplica el número de iteraciones por la complejidad del cuerpo."""
        self.loop_depth += 1
        
        # Analizar los límites del bucle para determinar el número de iteraciones
        start_complexity = self._analyze_node(node.start)
        end_complexity = self._analyze_node(node.end)
        
        # Analizar la complejidad del cuerpo
        body_results = [self._analyze_node(stmt) for stmt in node.body]
        body_complexity = self._combine_sequential(body_results)
        
        # Para bucles simples (0 a n), el número de iteraciones es O(n)
        # Límites más complejos requerirían un análisis diferente
        loop_iterations = ComplexityFunction("n")
        
        # Multiplicar el número de iteraciones del bucle por la complejidad del cuerpo
        result = self._multiply_complexity(loop_iterations, body_complexity)
        
        self.loop_depth -= 1
        return result
    
    def _analyze_while(self, node: While) -> ComplexityResult:
        """Analizar bucle while - estimaciones basadas en condición y cuerpo."""
        self.loop_depth += 1
        
        # Analizar la complejidad de la condición
        condition_complexity = self._analyze_node(node.condition)
        
        # Analizar la complejidad del cuerpo
        body_results = [self._analyze_node(stmt) for stmt in node.body]
        body_complexity = self._combine_sequential(body_results)
        
        # Los bucles while son más difíciles de analizar - hacemos estimaciones conservadoras
        # Mejor caso: condición falsa inmediatamente (Ω(1))
        # Peor caso: asumir O(n) iteraciones (podría ser más dependiendo del algoritmo)
        worst_case = self._multiply_complexity(ComplexityFunction("n"), body_complexity)
        best_case = ComplexityResult("1", "1")
        
        self.loop_depth -= 1
        return ComplexityResult(worst_case.big_o, best_case.omega)
    
    def _analyze_repeat(self, node: Repeat) -> ComplexityResult:
        """Analizar bucle repeat-until - similar a while pero se ejecuta al menos una vez."""
        self.loop_depth += 1
        
        body_results = [self._analyze_node(stmt) for stmt in node.body]
        body_complexity = self._combine_sequential(body_results)
        condition_complexity = self._analyze_node(node.condition)
        
        # Los bucles repeat se ejecutan al menos una vez
        # Mejor caso: una iteración
        # Peor caso: asumir O(n) iteraciones
        worst_case = self._multiply_complexity(ComplexityFunction("n"), body_complexity)
        best_case = body_complexity
        
        self.loop_depth -= 1
        return ComplexityResult(worst_case.big_o, best_case.omega)
    
    def _analyze_if(self, node: If) -> ComplexityResult:
        """Analizar condicional - el peor caso toma la rama máxima, el mejor caso toma la mínima."""
        then_result = self._combine_sequential([self._analyze_node(stmt) for stmt in node.then_body])
        
        if node.else_body:
            else_result = self._combine_sequential([self._analyze_node(stmt) for stmt in node.else_body])
            # Peor caso: máximo de las ramas, Mejor caso: mínimo de las ramas
            worst_case = self._max_complexity(then_result.big_o, else_result.big_o)
            best_case = self._min_complexity(then_result.omega, else_result.omega)
            return ComplexityResult(worst_case, best_case)
        else:
            # No hay rama else - el mejor caso es O(1) (solo la comprobación de la condición)
            return ComplexityResult(then_result.big_o, "1")
    
    def _analyze_return(self, node: Return) -> ComplexityResult:
        """Analizar sentencia return - depende de la complejidad de la expresión."""
        return self._analyze_node(node.expr)
    
    def _analyze_call(self, node: Call) -> ComplexityResult:
        """Analizar llamada a función - depende de la función llamada y los argumentos."""
        # Analizar complejidades de los argumentos
        arg_results = [self._analyze_node(arg) for arg in node.args] if node.args else []
        arg_complexity = self._combine_sequential(arg_results) if arg_results else ComplexityResult("1", "1")
        
        # Para llamadas recursivas, necesitamos un manejo especial
        if node.name in self.recursive_calls:
            return self._analyze_recursion(node)
        
        # Para funciones integradas o desconocidas, asumir O(1) a menos que tengamos conocimiento específico
        # Esto podría extenderse con una base de datos de complejidad de funciones
        return self._combine_sequential([arg_complexity, ComplexityResult("1", "1")])
    
    # ========== Análisis de Expresiones ==========
    
    def _analyze_binop(self, node: BinOp) -> ComplexityResult:
        """Analizar operación binaria - combina complejidades de operandos."""
        left_result = self._analyze_node(node.left)
        right_result = self._analyze_node(node.right)
        
        # Operaciones aritméticas básicas son O(1) una vez que los operandos se han calculado
        return self._combine_sequential([left_result, right_result, ComplexityResult("1", "1")])
    
    def _analyze_var(self, node: Var) -> ComplexityResult:
        """Acceso a variable es O(1)."""
        return ComplexityResult("1", "1")
    
    def _analyze_number(self, node: Number) -> ComplexityResult:
        """Literales numéricos son O(1)."""
        return ComplexityResult("1", "1")
    
    def _analyze_condition(self, node: Condition) -> ComplexityResult:
        """Analizar condición - combina complejidades de operandos más comparación."""
        left_result = self._analyze_node(node.left)
        right_result = self._analyze_node(node.right)
        
        # Operaciones de comparación son O(1) una vez que los operandos se han calculado
        return self._combine_sequential([left_result, right_result, ComplexityResult("1", "1")])
    
    # ========== Análisis de Arreglos/Matrices ==========
    
    def _analyze_arrayaccess(self, node: ArrayAccess) -> ComplexityResult:
        """Acceso a arreglo - O(1) para el cálculo del índice + O(1) para el acceso."""
        index_complexity = self._analyze_node(node.index)
        return self._combine_sequential([index_complexity, ComplexityResult("1", "1")])
    
    def _analyze_matrixaccess(self, node: MatrixAccess) -> ComplexityResult:
        """Acceso a matriz - O(1) para ambos índices + O(1) para el acceso."""
        row_complexity = self._analyze_node(node.row_index)
        col_complexity = self._analyze_node(node.col_index)
        return self._combine_sequential([row_complexity, col_complexity, ComplexityResult("1", "1")])
    
    def _analyze_arraydeclaration(self, node: ArrayDeclaration) -> ComplexityResult:
        """Declaración de arreglo - depende del tamaño y la inicialización."""
        size_complexity = self._analyze_node(node.size)
        # La declaración en sí podría requerir O(tamaño) para la inicialización
        return ComplexityResult("n", "n")  # Asumiendo inicialización al tamaño
    
    def _analyze_matrixdeclaration(self, node: MatrixDeclaration) -> ComplexityResult:
        """Declaración de matriz - O(filas * columnas) para la inicialización."""
        rows_complexity = self._analyze_node(node.rows)
        cols_complexity = self._analyze_node(node.cols)
        return ComplexityResult("n^2", "n^2")  # Asumiendo matriz n x n
    
    # ========== Análisis de Expresiones Booleanas ==========
    
    def _analyze_boolop(self, node: BoolOp) -> ComplexityResult:
        """Analizar operación booleana - considera evaluación de cortocircuito."""
        left_result = self._analyze_node(node.left)
        right_result = self._analyze_node(node.right)
        
        if node.op == 'and':
            # Cortocircuito: el mejor caso solo evalúa el operando izquierdo
            worst_case = self._combine_sequential([left_result, right_result])
            return ComplexityResult(worst_case.big_o, left_result.omega)
        elif node.op == 'or':
            # Cortocircuito: el mejor caso solo evalúa el operando izquierdo  
            worst_case = self._combine_sequential([left_result, right_result])
            return ComplexityResult(worst_case.big_o, left_result.omega)
        
        return self._combine_sequential([left_result, right_result])
    
    def _analyze_unaryop(self, node: UnaryOp) -> ComplexityResult:
        """Analizar operación unaria (como 'not')."""
        operand_result = self._analyze_node(node.operand)
        return self._combine_sequential([operand_result, ComplexityResult("1", "1")])
    
    def _analyze_boolean(self, node: Boolean) -> ComplexityResult:
        """Los literales booleanos son O(1)."""
        return ComplexityResult("1", "1")
    
    # ========== Métodos Auxiliares ==========
    
    def _combine_sequential(self, results: List[ComplexityResult]) -> ComplexityResult:
        """Combinar complejidades para ejecución secuencial (suma)."""
        if not results:
            return ComplexityResult("1", "1")
        
        # Para ejecución secuencial, tomamos la complejidad máxima
        big_o = self._max_complexity(*[r.big_o for r in results])
        omega = self._max_complexity(*[r.omega for r in results])
        
        return ComplexityResult(big_o, omega)
    
    def _combine_parallel(self, results: List[ComplexityResult]) -> ComplexityResult:
        """Combinar complejidades para ejecución paralela/alternativa."""
        if not results:
            return ComplexityResult("1", "1")
        
        # Para alternativas, el peor caso es el máximo, el mejor caso es el mínimo
        big_o = self._max_complexity(*[r.big_o for r in results])
        omega = self._min_complexity(*[r.omega for r in results])
        
        return ComplexityResult(big_o, omega)
    
    def _multiply_complexity(self, factor: ComplexityFunction, complexity: ComplexityResult) -> ComplexityResult:
        """Multiplicar complejidad por un factor (para bucles)."""
        big_o = self._multiply_expressions(str(factor), complexity.big_o)
        omega = self._multiply_expressions(str(factor), complexity.omega)
        
        return ComplexityResult(big_o, omega)
    
    def _multiply_expressions(self, factor: str, complexity: str) -> str:
        """Multiplicar dos expresiones de complejidad."""
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
        
        # Caso por defecto - podría necesitar un análisis más sofisticado
        return f"{factor}*{complexity}"
    
    def _max_complexity(self, *complexities: str) -> str:
        """Devolver la complejidad máxima (dominante)."""
        complexity_order = self._sort_complexities(complexities)
        return complexity_order[-1]  # Devolver la mayor
    
    def _min_complexity(self, *complexities: str) -> str:
        """Devolver la complejidad mínima."""
        complexity_order = self._sort_complexities(complexities)
        return complexity_order[0]  # Devolver la menor
    
    def _sort_complexities(self, complexities: tuple) -> List[str]:
        """Ordenar complejidades por tasa de crecimiento."""
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
            # Manejar expresiones de potencia
            if "^" in comp:
                power_match = re.search(r'n\^(\d+)', comp)
                if power_match:
                    return 2 + int(power_match.group(1))
            
            return complexity_map.get(comp, 2)  # Por defecto lineal si es desconocido
        
        return sorted(complexities, key=complexity_weight)
    
    def _analyze_recursion(self, node: Call) -> ComplexityResult:
        """Analizar llamadas recursivas basadas en el patrón detectado."""
        if node.name not in self.recursive_calls:
            return ComplexityResult("1", "1")
        
        pattern_info = self.recursive_calls[node.name]
        pattern = pattern_info['pattern']
        
        if pattern == 'linear':
            # Recursión lineal: T(n) = T(n-1) + O(1) -> O(n)
            return ComplexityResult("n", "n")
        elif pattern == 'binary':
            # Recursión binaria: T(n) = T(n-1) + T(n-2) + O(1) -> O(2^n)
            return ComplexityResult("2^n", "2^n")
        elif pattern == 'multiple':
            # últiples llamadas recursivas - crecimiento exponencial
            num_calls = pattern_info['count']
            return ComplexityResult(f"{num_calls}^n", f"{num_calls}^n")
        else:
            # Estimación conservadora para patrones desconocidos
            return ComplexityResult("n", "n")
    
    def _analyze_recursive_function(self, node: Function) -> ComplexityResult:
        """
        Analizar una función recursiva determinando su relación de recurrencia.
        """
        if node.name not in self.recursive_calls:
            return ComplexityResult("1", "1")
        
        pattern_info = self.recursive_calls[node.name]
        pattern = pattern_info['pattern']
        
        if pattern == 'linear':
            # Recursión lineal: T(n) = T(n-1) + O(1) -> O(n)
            return ComplexityResult("n", "n")
        elif pattern == 'binary':
            # Recursión binaria como Fibonacci: T(n) = T(n-1) + T(n-2) + O(1) -> O(2^n)
            return ComplexityResult("2^n", "2^n")
        elif pattern == 'multiple':
            # Últiples llamadas recursivas - crecimiento exponencial
            num_calls = pattern_info['count']
            return ComplexityResult(f"{num_calls}^n", f"{num_calls}^n")
        else:
            # Estimación conservadora para patrones desconocidos
            return ComplexityResult("n", "n")
    
    def _detect_recursive_functions(self, node):
        """
        Detecta qué funciones son recursivas buscando autollamadas.
        Rellena el diccionario recursive_calls con los nombres de las funciones y sus patrones de recursión.
        """
        if isinstance(node, Program):
            # Escanear todas las funciones en el programa
            for func in node.functions:
                self._scan_function_for_recursion(func)
        elif isinstance(node, Function):
            # Escanear una sola función
            self._scan_function_for_recursion(node)
    
    def _scan_function_for_recursion(self, func: Function):
        """
        Escanea una función en busca de llamadas recursivas a sí misma.
        """
        if not func or not func.name:
            return
            
        func_name = func.name
        recursive_calls = []
        
        # Escanea recursivamente el cuerpo de la función en busca de llamadas a sí misma
        def scan_node(node):
            if isinstance(node, Call) and node.name == func_name:
                recursive_calls.append(node)
            
            # Escanea recursivamente TODOS los atributos que podrían contener nodos
            if hasattr(node, '__dict__'):
                for attr_name, attr_value in node.__dict__.items():
                    if attr_value is not None:
                        if isinstance(attr_value, list):
                            for child in attr_value:
                                if hasattr(child, '__dict__'):  # Verifica si es un nodo
                                    scan_node(child)
                        elif hasattr(attr_value, '__dict__'):  # Verifica si es un nodo
                            scan_node(attr_value)
        
        # Escanea el cuerpo de la función
        if func.body:
            for stmt in func.body:
                scan_node(stmt)
        
        # Si se encuentran llamadas recursivas, clasifica el patrón de recursión
        if recursive_calls:
            pattern = self._classify_recursion_pattern(func_name, recursive_calls)
            self.recursive_calls[func_name] = {
                'calls': recursive_calls,
                'pattern': pattern,
                'count': len(recursive_calls)
            }
    
    def _classify_recursion_pattern(self, func_name: str, calls: List[Call]) -> str:
        """
        Clasifica el tipo de recursión basado en las llamadas recursivas encontradas.
        """
        num_calls = len(calls)
        
        if num_calls == 0:
            return 'none'
        elif num_calls == 1:
            return 'linear'  # T(n) = T(n-1) + O(1) -> O(n)
        elif num_calls == 2:
            return 'binary'  # T(n) = T(n-1) + T(n-2) + O(1) -> O(2^n) 
        else:
            return 'multiple'  # Múltiples llamadas recursivas