from src.ast.nodes import *

class ComplexityAnalyzer:
    """
    Analizador estático de complejidad temporal asintótica (Big O).

    Esta clase recorre un Árbol de Sintaxis Abstracta (AST) para estimar
    la complejidad temporal del algoritmo representado, aplicando reglas
    de suma para secuencias y reglas de producto para bucles anidados.
    """

    def analyze(self, node) -> str:
        """
        Determina la complejidad de un nodo específico del AST.

        Actúa como un despachador (dispatcher), identificando el tipo de nodo
        y delegando el cálculo o retornando un valor base.

        Args:
            node: El nodo del AST a analizar (puede ser Program, Function, For, If, etc.).

        Returns:
            str: Una cadena representando la complejidad (ej. "O(1)", "O(n)", "O(n^2)").
        """
        if isinstance(node, Program):
            # Analiza todas las funciones y retorna la mayor complejidad encontrada
            return self.combine([self.analyze(f) for f in node.functions])
        
        if isinstance(node, Function):
            # Analiza el cuerpo de la función
            return self.combine([self.analyze(stmt) for stmt in node.body])
        
        if isinstance(node, (Assignment, Return, Call)):
            # Operaciones básicas se consideran tiempo constante
            return "O(1)"
        
        if isinstance(node, For):
            # Regla del producto: Complejidad del bucle * Complejidad del cuerpo
            # Se asume que el bucle itera N veces.
            body_complexity = self.analyze_block(node.body)
            return self.multiply("O(n)", body_complexity)
        
        if isinstance(node, (While, Repeat)):
            # Similar al For, se asume peor caso de N iteraciones
            body_complexity = self.analyze_block(node.body)
            return self.multiply("O(n)", body_complexity)
        
        if isinstance(node, If):
            # Ramificación: Se toma el peor caso (máximo) entre el bloque 'then' y 'else'
            then_c = self.analyze_block(node.then_body)
            else_c = self.analyze_block(node.else_body) if node.else_body else "O(1)"
            return self.max_complexity(then_c, else_c)
        
        if isinstance(node, (BinOp, Var, Number)):
            # Expresiones simples
            return "O(1)"
        
        # Caso por defecto
        return "O(1)"

    def analyze_block(self, statements: list) -> str:
        """
        Analiza una lista de sentencias secuenciales.

        Args:
            statements (list): Lista de nodos del AST.

        Returns:
            str: La complejidad dominante del bloque.
        """
        if not statements:
            return "O(1)"
        return self.combine([self.analyze(stmt) for stmt in statements])

    # ---- Helpers (Métodos auxiliares) ----

    def combine(self, complexities: list) -> str:
        """
        Aplica la regla de la suma para una lista de complejidades.

        En notación Big O, O(A) + O(B) es equivalente a max(O(A), O(B)).
        
        Args:
            complexities (list): Lista de strings de complejidad.

        Returns:
            str: La complejidad dominante de la lista.
        """
        if not complexities:
            return "O(1)"
        return self.max_complexity(*complexities)

    def multiply(self, outer: str, inner: str) -> str:
        """
        Aplica la regla del producto para bucles anidados.

        Calcula la complejidad resultante de envolver una complejidad interna
        dentro de un bucle externo.

        Args:
            outer (str): Complejidad del bucle externo (usualmente "O(n)").
            inner (str): Complejidad del cuerpo del bucle.

        Returns:
            str: El producto de las complejidades (ej. "O(n^2)").
        """
        if inner == "O(1)":
            return outer
        if outer == "O(n)" and inner == "O(n)":
            return "O(n^2)"
        # Nota: Esto es una simplificación, podría requerir un parser de polinomios
        # para casos más complejos (ej. O(n^3)).
        return f"{outer}*{inner}"

    def max_complexity(self, *complexities) -> str:
        """
        Determina la complejidad más alta entre un conjunto de valores.

        Utiliza una jerarquía simple hardcodeada: O(n^2) > O(n) > O(1).

        Args:
            *complexities: Argumentos variables con strings de complejidad.

        Returns:
            str: La complejidad mayor encontrada.
        """
        # La verificación se hace por orden de dominancia
        if "O(n^2)" in complexities:
            return "O(n^2)"
        if "O(n)" in complexities:
            return "O(n)"
        return "O(1)"
    