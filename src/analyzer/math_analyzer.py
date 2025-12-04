"""
Analizador de Complejidad Matemática
================================

Este módulo implementa un analizador de complejidad basado en la derivación matemática formal de funciones de costo a partir del AST del algoritmo. Utiliza matemáticas simbólicas para construir y resolver ecuaciones de costo.
"""

import re
import sympy
from src.ast.nodes import *
from typing import Dict, Any, Optional, List

from src.analyzer.recurrence_solver import RecursiveAlgorithmAnalyzer

class MathematicalAnalyzer:
    """
    Realiza el análisis de complejidad recorriendo el AST y construyendo una
    función de costo simbólica. Actúa como “fuente algebraica” del sistema:
    deduce expresiones/recurrencias y luego las simplifica a Big-O.
    """
    def __init__(self):
        self.n = sympy.Symbol('n', positive=True)
        self.T = sympy.Function('T')
        self.function_costs: Dict[str, sympy.Expr] = {}
        self.symbol_tables: Dict[str, Dict[str, sympy.Expr]] = {}
        self.function_metadata: Dict[str, Dict[str, Any]] = {}
        self.recursive_analyzer = RecursiveAlgorithmAnalyzer()
        self.current_function: Optional[str] = None
        self.last_raw_results: Dict[str, Any] = {}

    def analyze(self, program_node: Program) -> Dict[str, Any]:
        if not isinstance(program_node, Program):
            raise TypeError("Se esperaba un nodo Program.")

        for func in program_node.functions:
            self.function_costs[func.name] = sympy.Function(f"T_{func.name}")(self.n)
            self.symbol_tables[func.name] = {}
            self.function_metadata[func.name] = self.recursive_analyzer.analyze_recursive_algorithm(func)

        raw_results: Dict[str, Any] = {}
        for func in program_node.functions:
            self.current_function = func.name
            cost_or_eq = self._get_cost(func, current_func_name=func.name)
            normalized = self._normalize_recursive_terms(cost_or_eq, func.name)
            raw_results[func.name] = normalized

        # Segunda pasada: resolver las ecuaciones
        self.last_raw_results = raw_results.copy()
        final_complexities: Dict[str, Any] = {}
        for name, result in raw_results.items():
            final_complexities[name] = self.solve(result, func_name=name)

        return final_complexities

    def solve(self, expr_or_eq: Any, func_name: Optional[str] = None) -> Any:
        """
        Resuelve la expresión simbólica o ecuación para encontrar la
        complejidad asintótica (Big O).
        """
        try:
            if isinstance(expr_or_eq, sympy.Eq):
                return self.solve_recurrence(expr_or_eq, func_name=func_name)
            
            elif isinstance(expr_or_eq, sympy.Expr):
                simplified = self._normalize_order_expr(sympy.simplify(expr_or_eq))
                return self._safe_big_o(simplified)
            
            else:
                return "Tipo de resultado desconocido"
        except Exception as e:
            return f"Error durante la resolución: {e}"

    def solve_recurrence(self, eq: sympy.Eq, func_name: Optional[str] = None) -> Any:
        """
        Resuelve una ecuación de relación de recurrencia.
        Intenta una solución simbólica directa con rsolve, y recurre al
        Teorema Maestro para recurrencias de divide y vencerás.
        """
        try:
            try:
                replacements = {f: self.n for f in eq.atoms(sympy.Function) if f.func != self.T}
                if replacements:
                    eq = eq.xreplace(replacements)
            except Exception:
                pass

            # Primero, intente resolver con rsolve para recurrencias lineales
            solution = sympy.rsolve(eq, self.T(self.n))
            if solution:
                try:
                    # Reemplazar constantes de integración (C0, C1, ...) por 1 para evitar problemas en O()
                    solution_clean = solution
                    for sym in solution.free_symbols:
                        if sym.name.startswith("C"):
                            solution_clean = solution_clean.subs(sym, 1)

                    simplified = self._normalize_order_expr(sympy.simplify(solution_clean.expand()))
                    return self._safe_big_o(simplified)
                except NotImplementedError:
                    fallback_eq = self._fallback_from_equation(eq, func_name=func_name)
                    if fallback_eq:
                        return fallback_eq
                    fallback = self._fallback_complexity(func_name)
                    if fallback:
                        return fallback
        except (ValueError, NotImplementedError):
            # Pasar al Teorema Maestro si rsolve falla (por ejemplo, para T(n/2))
            pass

        # Intentar Teorema Maestro para Divide y Vencerás
        a, b, f_n, is_div_conquer = self._extract_master_theorem_params(eq)

        if not is_div_conquer:
            fallback_eq = self._fallback_from_equation(eq, func_name=func_name)
            if fallback_eq:
                return fallback_eq
            fallback = self._fallback_complexity(func_name)
            if fallback:
                return fallback
            return "La recurrencia no está en una forma resoluble (lineal o D&C)"

        if a < 1 or b <= 1:
            fallback_eq = self._fallback_from_equation(eq, func_name=func_name)
            if fallback_eq:
                return fallback_eq
            fallback = self._fallback_complexity(func_name)
            if fallback:
                return fallback
            return "Parámetros inválidos para el Teorema Maestro (a>=1, b>1)"

        try:
            log_b_a = sympy.log(a, b)
            
            # Determinar el exponente crítico
            critical_exponent = sympy.sympify(log_b_a)

            # Comparar f(n) con n^log_b(a)
            # Usamos límites para determinar la relación
            ratio_limit = sympy.limit(f_n / (self.n**critical_exponent), self.n, sympy.oo)

            if ratio_limit == 0:
                # Caso 1: f(n) es polinomialmente menor
                return sympy.O(self.n**critical_exponent, (self.n, sympy.oo))
            
            elif ratio_limit.is_finite and ratio_limit > 0:
                # Caso 2: f(n) es del mismo orden
                return sympy.O(self.n**critical_exponent * sympy.log(self.n), (self.n, sympy.oo))

            elif ratio_limit == sympy.oo:
                # Caso 3: f(n) es polinomialmente mayor
                # Deberíamos verificar la condición de regularidad a*f(n/b) <= c*f(n) para c < 1
                # pero asumiremos que se cumple para esta implementación.
                return sympy.O(f_n, (self.n, sympy.oo))
            
            else:
                return f"No se pudo determinar el caso del Teorema Maestro para el límite={ratio_limit}"

        except Exception as e:
            fallback_eq = self._fallback_from_equation(eq, func_name=func_name)
            if fallback_eq:
                return fallback_eq
            fallback = self._fallback_complexity(func_name)
            if fallback:
                return fallback
            return f"Error aplicando el Teorema Maestro: {e}"

    def _generate_tree_textual_analysis(self, eq: sympy.Eq) -> str:
        """
        Genera un análisis textual del árbol de recurrencia.
        """
        analysis = ""
        
        a_val, b_val, f_n, is_div_conquer = self._extract_master_theorem_params(eq)

        if is_div_conquer:
            log_b_a = sympy.log(a_val, b_val)
            
            analysis += "  REPRESENTACIÓN TEXTUAL DE LOS PRIMEROS 3 NIVELES:\n"
            analysis += "  " + "─" * 114 + "\n\n"
            
            # Nivel 0
            analysis += f"  Nivel 0 (Raíz): T(n)                                     │ Costo: {f_n}\n"
            
            # Nivel 1
            cost_l1 = f_n.subs(self.n, self.n/b_val)
            analysis += f"  Nivel 1: {a_val} nodos T(n/{b_val})                      │ Costo Total: {a_val} * {cost_l1}\n"
            
            # Nivel 2
            cost_l2 = f_n.subs(self.n, self.n/(b_val**2))
            analysis += f"  Nivel 2: {a_val**2} nodos T(n/{b_val**2})                  │ Costo Total: {a_val**2} * {cost_l2}\n\n"
            
            analysis += "  " + "─" * 114 + "\n\n"
            
            # Generalización
            k = sympy.Symbol('k')
            analysis += "  GENERALIZACIÓN - Nivel k-ésimo:\n"
            analysis += f"    • Número de nodos: {a_val}^k\n"
            analysis += f"    • Tamaño del problema por nodo: n / ({b_val}^k)\n"
            cost_per_node_k = f_n.subs(self.n, self.n/(b_val**k))
            cost_total_k = (a_val**k) * cost_per_node_k
            analysis += f"    • Costo por nodo: {cost_per_node_k}\n"
            analysis += f"    • Costo total en nivel k: {cost_total_k}\n\n"
            
            # Altura
            analysis += "  ALTURA DEL ÁRBOL (h):\n"
            analysis += f"    • h = log_{b_val}(n)\n\n"
            
            # Costo total
            analysis += "  COSTO TOTAL:\n"
            if sympy.Abs(log_b_a - sympy.log(a_val,b_val)).evalf() < 1e-9:
                 analysis += f"    • Caso 1 del Teorema Maestro: T(n) = Θ({self.n}**{log_b_a})\n"
            elif sympy.Abs(log_b_a - sympy.log(a_val,b_val)).evalf() > 1e-9:
                 analysis += f"    • Caso 3 del Teorema Maestro: T(n) = Θ({f_n})\n"
            else:
                 analysis += f"    • Caso 2 del Teorema Maestro: T(n) = Θ({self.n}**{log_b_a} * log(n))\n"

        else:
            linear_params = self._extract_linear_recurrence_params(eq)
            if linear_params:
                dec = linear_params['decrement']
                work = linear_params['work']
                analysis += "  REPRESENTACIÓN TEXTUAL DE LOS PRIMEROS NIVELES (Recursión lineal):\n"
                analysis += "  " + "─" * 114 + "\n\n"
                cost_level0 = work
                analysis += f"  Nivel 0 (Raíz): T(n)                                     │ Costo: {cost_level0}\n"
                max_levels = 3
                for level in range(1, max_levels):
                    size = sympy.simplify(self.n - dec * level)
                    cost = work.subs(self.n, size) if work.has(self.n) else work
                    size_str = f"T(n - {dec*level})"
                    spacing = max(1, 38 - len(size_str))
                    analysis += f"  Nivel {level}: {size_str}{' ' * spacing}│ Costo: {cost}\n"
                analysis += "\n"
                analysis += "  GENERALIZACIÓN - Nivel k-ésimo:\n"
                analysis += f"    • Tamaño del subproblema: n - k*{dec}\n"
                analysis += f"    • Costo por nodo: {work.subs(self.n, self.n - sympy.Symbol('k')*dec) if work.has(self.n) else work}\n"
                analysis += f"    • Número de niveles (h) ≈ n/{dec}\n"
                analysis += f"    • Nodos totales ≈ n/{dec}\n\n"
                analysis += "  COSTO TOTAL:\n"
                analysis += f"    • Se expanden ≈ n/{dec} niveles; el trabajo acumulado es Σ f(n - i*{dec}).\n"
                analysis += "    • El motor matemático resuelve la recurrencia para obtener la cota final.\n"
            else:
                analysis = "El análisis textual del árbol de recurrencia solo está disponible para recurrencias de 'divide y vencerás' o lineales simples."

        return analysis

    def _extract_master_theorem_params(self, eq: sympy.Eq) -> tuple:
        """
        Ayuda para extraer a, b y f(n) de una relación de recurrencia. 
        Extrae los parámetros del Teorema Maestro: 
        T(n) = a*T(n/b) + f(n)
        """
        a_val, b_val, f_n = sympy.S(1), sympy.S(1), sympy.S(0)
        is_div_conquer = False
        
        rhs = eq.rhs
        terms = sympy.Add.make_args(rhs) if isinstance(rhs, sympy.Add) else [rhs]
        
        rec_terms = [t for t in terms if t.has(self.T)]
        non_rec_terms = [t for t in terms if not t.has(self.T)]
        f_n = sympy.Add(*non_rec_terms) if non_rec_terms else sympy.S(0)

        if rec_terms:
            # Suma todos los coeficientes de los términos recursivos para obtener 'a'
            a_val = sympy.S(0)
            b_val = None
            
            for rec_term in rec_terms:
                if rec_term.is_Mul:
                    coeff, rec_func = rec_term.as_coeff_Mul()
                else:
                    coeff, rec_func = sympy.S(1), rec_term
                
                a_val += coeff
                
                # Extraer b del argumento de la llamada recursiva
                if isinstance(rec_func, sympy.Function) and rec_func.func == self.T and rec_func.args:
                    arg_expr = rec_func.args[0]
                    
                    # Manejar el caso T(n/b): arg_expr = n/b = n * (1/b)
                    if arg_expr.is_Mul and self.n in arg_expr.free_symbols:
                        n_coeff = arg_expr.coeff(self.n)
                        if n_coeff.is_Rational or n_coeff.is_Number:
                            # n_coeff = 1/b, so b = 1/n_coeff
                            candidate_b = 1 / n_coeff
                            if b_val is None:
                                b_val = candidate_b
                            elif b_val != candidate_b:
                                # Diferentes valores de b, no es un caso estándar de divide y vencerás
                                is_div_conquer = False
                                break
                            is_div_conquer = candidate_b > 1
                    # Manejar el caso T(n^c) (menos común)
                    elif arg_expr.is_Pow and arg_expr.base == self.n:
                        exp = arg_expr.exp
                        if exp.is_Rational and exp < 1:
                            # n^exp = n^(1/b), so b = 1/exp
                            candidate_b = 1 / exp
                            if b_val is None:
                                b_val = candidate_b
                            elif b_val != candidate_b:
                                is_div_conquer = False
                                break
                            is_div_conquer = candidate_b > 1
                    else:
                        # No es una forma de divide y vencerás (por ejemplo, T(n-1))
                        is_div_conquer = False
                        break
            
            if b_val is None:
                is_div_conquer = False

        return a_val, b_val, f_n, is_div_conquer

    def _extract_linear_recurrence_params(self, eq: sympy.Eq) -> Optional[Dict[str, sympy.Expr]]:
        """Detecta recurrencias lineales de la forma T(n) = T(n - k) + f(n)."""
        if not isinstance(eq, sympy.Eq):
            return None

        rhs = eq.rhs
        terms = sympy.Add.make_args(rhs) if isinstance(rhs, sympy.Add) else [rhs]

        rec_terms = [t for t in terms if t.has(self.T)]
        if len(rec_terms) != 1:
            return None

        rec_term = rec_terms[0]
        if rec_term.is_Mul:
            coeff, rec_func = rec_term.as_coeff_Mul()
        else:
            coeff, rec_func = sympy.S(1), rec_term

        if coeff != 1 or not isinstance(rec_func, sympy.Function) or rec_func.func != self.T:
            return None

        arg_expr = rec_func.args[0]
        decrement = sympy.simplify(self.n - arg_expr)
        if not (decrement.is_Number and decrement > 0):
            return None

        work_terms = [t for t in terms if not t.has(self.T)]
        work = sympy.Add(*work_terms) if work_terms else sympy.Integer(0)

        return {"decrement": decrement, "work": work}

    def _expr_has_recurrence(self, expr: Any) -> bool:
        """Ayuda para detectar si una expresión contiene la recurrencia T()."""
        if expr is None:
            return False
        try:
            for subexpr in sympy.preorder_traversal(expr):
                if isinstance(subexpr, sympy.Function) and subexpr.func == self.T:
                    return True
        except Exception:
            # Recurso alternativo: detección basada en cadenas si la traversa falla
            return 'T(' in str(expr)
        return False

    def _get_cost(self, node: Node, current_func_name: Optional[str] = None) -> sympy.Expr:
        """Visitante genérico de costo que despacha a métodos específicos por tipo de nodo."""
        method_name = f'_get_cost_{type(node).__name__}'
        visitor = getattr(self, method_name, self._get_cost_default)
        
        # Pasar el contexto si el visitante lo acepta
        import inspect
        sig = inspect.signature(visitor)
        if 'current_func_name' in sig.parameters:
            return visitor(node, current_func_name=current_func_name)
        else:
            return visitor(node)

    def _get_cost_default(self, node: Node) -> sympy.Expr:
        return sympy.Integer(1)

    def _safe_sum(self, costs: list) -> sympy.Expr:
        """Suma de forma segura una lista de expresiones sympy, ignorando los Nones."""
        return sum(c for c in costs if c is not None)

    def _get_cost_Function(self, node: Function, current_func_name: str) -> sympy.Expr:
        body_cost = self._safe_sum(self._get_cost(stmt, current_func_name=current_func_name) for stmt in node.body)
        
        # Verificar si el costo del cuerpo contiene una llamada recursiva (un término T())
        is_recursive = self._expr_has_recurrence(body_cost)
        
        if is_recursive:
            # Esta es una relación de recurrencia: T(n) = body_cost
            return sympy.Eq(self.T(self.n), body_cost)
        else:
            # Esta es una expresión de costo simple
            return body_cost

    def _get_cost_If(self, node: If, current_func_name: str) -> sympy.Expr:
        condition_cost = self._get_cost(node.condition, current_func_name=current_func_name)
        then_cost = self._safe_sum(self._get_cost(stmt, current_func_name=current_func_name) for stmt in node.then_body)
        else_cost = self._safe_sum(self._get_cost(stmt, current_func_name=current_func_name) for stmt in node.else_body) if node.else_body else sympy.Integer(0)

        then_has_rec = self._expr_has_recurrence(then_cost)
        else_has_rec = self._expr_has_recurrence(else_cost)

        if then_has_rec and else_has_rec:
            branch_cost = sympy.Max(then_cost, else_cost)
        elif then_has_rec:
            branch_cost = then_cost
        elif else_has_rec:
            branch_cost = else_cost
        else:
            # Para ramas puramente iterativas, mantener el peor caso (Max)
            try:
                branch_cost = sympy.Max(then_cost, else_cost)
            except Exception:
                branch_cost = then_cost + else_cost

        return condition_cost + branch_cost

    def _get_cost_For(self, node: For, current_func_name: str) -> sympy.Expr:
        loop_var = sympy.Symbol(node.var)
        start_val = self._get_value(node.start)
        end_val = self._get_value(node.end)
        body_cost = self._safe_sum(self._get_cost(stmt, current_func_name=current_func_name) for stmt in node.body)
        
        if body_cost == 0:
            return sympy.Integer(0)

        # Calcular el número de iteraciones: end - start + 1 (si ambos son números)
        # Para límites simbólicos, usar Sum
        try:
            if isinstance(start_val, sympy.Number) and isinstance(end_val, sympy.Number):
                num_iterations = end_val - start_val + 1
                total_cost = num_iterations * body_cost
            else:
                # Límites simbólicos: usar Sum
                total_cost = sympy.Sum(body_cost, (loop_var, start_val, end_val)).doit()
        except:
            # Fallback: usar Sum para cualquier caso
            total_cost = sympy.Sum(body_cost, (loop_var, start_val, end_val)).doit()
        
        bounds_cost = self._get_cost(node.start, current_func_name) + self._get_cost(node.end, current_func_name)
        return total_cost + bounds_cost

    def _get_cost_While(self, node: While, current_func_name: str) -> sympy.Expr:
        # Los bucles While son más difíciles de analizar estáticamente
        # Devolvemos una expresión simbólica con k (número de iteraciones)
        # El análisis real necesitaría entender la condición del bucle
        k = sympy.Symbol('k', real=True, positive=True)
        condition_cost = self._get_cost(node.condition, current_func_name=current_func_name)
        body_cost = self._safe_sum(self._get_cost(stmt, current_func_name=current_func_name) for stmt in node.body)
        # Devolver k * (condición + cuerpo) - esto representa el peor caso de iteraciones
        return k * (condition_cost + body_cost)

    def _get_cost_Assignment(self, node: Assignment, current_func_name: str) -> sympy.Expr:
        return self._get_cost(node.expr, current_func_name=current_func_name) + 1

    def _get_cost_Return(self, node: Return, current_func_name: str) -> sympy.Expr:
        if node.expr:
            return self._get_cost(node.expr, current_func_name=current_func_name)
        return sympy.Integer(1)

    def _get_cost_BinOp(self, node: BinOp, current_func_name: str) -> sympy.Expr:
        return self._get_cost(node.left, current_func_name) + self._get_cost(node.right, current_func_name) + 1

    def _get_cost_Condition(self, node: Condition, current_func_name: str) -> sympy.Expr:
        return self._get_cost(node.left, current_func_name) + self._get_cost(node.right, current_func_name) + 1

    def _get_cost_Call(self, node: Call, current_func_name: str) -> sympy.Expr:
        arg_costs = self._safe_sum(self._get_cost(arg, current_func_name=current_func_name) for arg in node.args)
        
        # Comprobar recursión
        if node.name == current_func_name:
            # Es una llamada recursiva. Representarla simbólicamente.
            # Asumimos un solo argumento para simplificar por ahora.
            if node.args:
                symbolic_arg = self._get_value(node.args[0])
                return arg_costs + self.T(symbolic_arg)
            else:
                # Recursión sin cambio de argumento, por ejemplo, T(n) = ... + T(n)
                return arg_costs + self.T(self.n)
        else:
            # Es una llamada a otra función. Buscar su costo.
            # Esto es una simplificación; un análisis completo sustituiría la función de costo de la otra función.
            return arg_costs + self.function_costs.get(node.name, sympy.Integer(1))


    def _get_cost_Var(self, node: Var) -> sympy.Expr:
        return sympy.Integer(1)

    def _get_cost_Number(self, node: Number) -> sympy.Expr:
        return sympy.Integer(1)
        
    def _get_cost_Program(self, node: Program, current_func_name: Optional[str] = None) -> sympy.Expr:
        return self._safe_sum(self._get_cost(func, current_func_name=func.name) for func in node.functions)


    def _get_value(self, node: Node) -> Any:
        """Visitante genérico de valores que despacha a métodos específicos de nodos."""
        method_name = f'_get_value_{type(node).__name__}'
        visitor = getattr(self, method_name, self._get_value_default)
        return visitor(node)

    def _get_value_default(self, node: Node) -> Any:
        return sympy.Symbol(f"val_{type(node).__name__}")

    def _get_value_BinOp(self, node: BinOp) -> sympy.Expr:
        left = self._get_value(node.left)
        right = self._get_value(node.right)
        
        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            return left / right
        else:
            # Operador desconocido, por defecto suma
            return left + right

    def _get_value_Var(self, node: Var) -> sympy.Symbol:
        if node.name == 'n':
            return self.n
        return sympy.Symbol(node.name)

    def _get_value_Number(self, node: Number) -> sympy.Integer:
        return sympy.Integer(node.value)


    def _normalize_recursive_terms(self, expr: Any, func_name: Optional[str]) -> Any:
        if not isinstance(expr, sympy.Eq) or not func_name:
            return expr

        rhs = expr.rhs
        recursive_terms: List[sympy.Function] = []
        for subexpr in sympy.preorder_traversal(rhs):
            if isinstance(subexpr, sympy.Function) and subexpr.func == self.T:
                recursive_terms.append(subexpr)

        if not recursive_terms:
            return expr

        inferred_args = self._get_recurrence_args_from_metadata(func_name, len(recursive_terms))
        replacements = {}
        for idx, term in enumerate(recursive_terms):
            arg = term.args[0]
            if arg.has(self.n):
                continue
            normalized_arg = inferred_args[idx] if idx < len(inferred_args) else self.n
            replacements[term] = self.T(normalized_arg)

        if replacements:
            rhs = rhs.xreplace(replacements)
            return sympy.Eq(expr.lhs, rhs, evaluate=False)
        return expr

    def _get_recurrence_args_from_metadata(self, func_name: str, count: int) -> List[sympy.Expr]:
        metadata = self.function_metadata.get(func_name, {})
        relation = metadata.get('recurrence_relation')
        if not relation:
            return []

        clean = relation.replace(" ", "")
        args: List[sympy.Expr] = []
        pattern = re.compile(r'T\(n(?:(/)(\d+)|-(\d+))?\)')
        for match in pattern.finditer(clean):
            slash, divisor, decrement = match.groups()
            if slash and divisor:
                args.append(self.n / int(divisor))
            elif decrement:
                args.append(self.n - int(decrement))
            else:
                args.append(self.n)

        if args:
            # El primer término corresponde al lado izquierdo T(n); descartarlo
            args = args[1:]

        if not args:
            args.append(self.n)

        while len(args) < count:
            args.append(args[-1])

        return args

    def _normalize_recursive_argument(self, arg_expr: sympy.Expr, func_name: str) -> sympy.Expr:
        if arg_expr.has(self.n):
            return arg_expr
        inferred_args = self._get_recurrence_args_from_metadata(func_name, 1)
        if inferred_args:
            return inferred_args[0]
        return self.n

    def _normalize_order_expr(self, expr: Any) -> Any:
        """
        Normaliza expresiones antes de calcular Big-O.
        Cosas que arregla:
        - O(log(1/n))  -> O(log n)
        - O(1/log(n))  -> O(1/log n)   (sin cambios en orden, solo forma)
        - Signos negativos delante de log: -log(n) -> log(n)
        """

        import sympy as sp

        try:
            n = self.n

            # 1) Expandir un poco la expresión
            expr = sp.simplify(expr)

            # 2) Reemplazar log(1/n) por -log(n)
            #    sympy representa log(1/n) literalmente como log(1/n)
            expr = expr.xreplace({
                sp.log(1 / n): -sp.log(n)
            })

            # 3) Si la expresión es -log(n) o -k*log(n) -> |coef|*log(n)
            if expr.is_Mul:
                coef, rest = expr.as_coeff_Mul()
                if coef < 0 and rest.has(sp.log(n)):
                    expr = abs(coef) * rest

            # 4) Si es directamente -log(n)
            if expr == -sp.log(n):
                expr = sp.log(n)

            return expr
        except Exception:
            return expr

    def _safe_big_o(self, expr: Any) -> Any:
        """
        Calcula O(expr) evitando fallos por expresiones como Max o series no soportadas.
        """
        import sympy as sp

        # Si hay Max en la expresion, reemplazar por el argumento dominante en n
        if hasattr(expr, "has") and expr.has(sp.Max):
            max_terms = list(expr.atoms(sp.Max))
            for m in max_terms:
                best = None
                best_degree = None
                for arg in m.args:
                    try:
                        deg = sp.degree(sp.Poly(arg, self.n))
                    except Exception:
                        deg = None
                    if best is None or (deg is not None and (best_degree is None or deg > best_degree)):
                        best = arg
                        best_degree = deg
                if best is not None:
                    expr = expr.xreplace({m: best})

        try:
            return sp.O(expr, (self.n, sp.oo))
        except Exception:
            # Fallback genérico
            try:
                return sp.O(sp.simplify(expr), (self.n, sp.oo))
            except Exception:
                # Heurística para combinaciones exponenciales (e.g., Fibonacci)
                pow_terms = [p for p in expr.atoms(sp.Pow) if p.exp == self.n or (hasattr(p.exp, "has") and p.exp.has(self.n))]
                if pow_terms:
                    try:
                        bases = []
                        for p in pow_terms:
                            if p.exp == self.n:
                                bases.append(sp.Abs(p.base))
                        if bases:
                            dominant = max(bases)
                            return sp.O(dominant**self.n, (self.n, sp.oo))
                    except Exception:
                        pass
                return "O(?)"

        # Si no pudimos calcular nada, devolvemos la expresión original como string
        return "O(?)"

    def _fallback_complexity(self, func_name: Optional[str]) -> Optional[str]:
        if not func_name:
            return None

        metadata = self.function_metadata.get(func_name, {})
        relation = (metadata.get('recurrence_relation') or "").replace(" ", "")
        pattern = metadata.get('pattern_type')

        if pattern == 'binary':
            return "O(2**n)"

        if pattern == 'binary_exclusive':
            return "O(log(n))"

        if pattern == 'linear':
            return "O(n)"

        if pattern == 'divide_conquer':
            if re.search(r'2T\(n/2\)', relation):
                if 'O(n)' in relation:
                    return "O(n*log(n))"
                return "O(n)"
            if re.search(r'T\(n/2\)', relation):
                return "O(log(n))"

        return None

    def _fallback_from_equation(self, eq: Any, func_name: Optional[str] = None) -> Optional[str]:
        """
        Heurísticos por patrón cuando Sympy no puede resolver bien la recurrencia.
        """
        import sympy as sp
        
        try:
            if not isinstance(eq, sp.Eq):
                return None

            lhs, rhs = eq.lhs, eq.rhs

            # Asegurarnos de que es T(n) = ...
            if lhs.func != self.T:
                return None

            # Caso 1: T(n) = T(n - k) + c  -> O(n)
            # (recursión lineal tipo factorial)
            n = self.n
            if rhs.has(self.T(n - 1)) or rhs.has(self.T(n - sp.Integer(1))):
                return "O(n)"

            # Caso 2: T(n) = T(n/2) + c    -> O(log n)  (búsqueda binaria)
            if rhs.has(self.T(n / 2)):
                # Confirmar que sólo hay UNA llamada recursiva
                calls = [arg for arg in rhs.atoms(sp.Function) if arg.func == self.T]
                if len(calls) == 1:
                    return "O(log(n))"

            # Caso 3: T(n) = 2*T(n/2) + f(n)  -> típicamente O(n log n)
            # (merge sort / divide & conquer balanceado)
            if rhs.has(2 * self.T(n / 2)):
                return "O(n*log(n))"

            # Caso 4: T(n) = T(n-1) + T(n-2) + c  -> O(2^n) (Fibonacci)
            if rhs.has(self.T(n - 1)) and rhs.has(self.T(n - 2)):
                return "O(2**n)"

            return None

        except Exception:
            return None
