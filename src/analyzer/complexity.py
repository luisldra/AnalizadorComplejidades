from src.ast.nodes import *

class ComplexityAnalyzer:
    def analyze(self, node):
        if isinstance(node, Program):
            return self.combine([self.analyze(f) for f in node.functions])
        
        if isinstance(node, Function):
            return self.combine([self.analyze(stmt) for stmt in node.body])
        
        if isinstance(node, Assignment) or isinstance(node, Return) or isinstance(node, Call):
            return "O(1)"
        
        if isinstance(node, For):
            body_complexity = self.analyze_block(node.body)
            return self.multiply("O(n)", body_complexity)
        
        if isinstance(node, While) or isinstance(node, Repeat):
            body_complexity = self.analyze_block(node.body)
            return self.multiply("O(n)", body_complexity)
        
        if isinstance(node, If):
            then_c = self.analyze_block(node.then_body)
            else_c = self.analyze_block(node.else_body) if node.else_body else "O(1)"
            return self.max_complexity(then_c, else_c)
        
        if isinstance(node, BinOp) or isinstance(node, Var) or isinstance(node, Number):
            return "O(1)"
        
        return "O(1)"

    def analyze_block(self, statements):
        if not statements:
            return "O(1)"
        return self.combine([self.analyze(stmt) for stmt in statements])

    # ---- helpers ----
    def combine(self, complexities):
        """Suma de complejidades → se queda con la dominante"""
        if not complexities:
            return "O(1)"
        return self.max_complexity(*complexities)

    def multiply(self, outer, inner):
        """Multiplica bucles → O(n) * inner"""
        if inner == "O(1)":
            return outer
        if outer == "O(n)" and inner == "O(n)":
            return "O(n^2)"
        return f"{outer}*{inner}"

    def max_complexity(self, *complexities):
        if "O(n^2)" in complexities:
            return "O(n^2)"
        if "O(n)" in complexities:
            return "O(n)"
        return "O(1)"
