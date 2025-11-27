import os
import sympy as sp
from src.parser.parser import parse_code
from src.analyzer.analysis_result import AnalysisResult
from src.analyzer.math_analyzer import MathematicalAnalyzer
from src.analyzer.asymptotic_analyzer import AsymptoticAnalyzer
from src.analyzer.recurrence_solver import RecursiveAlgorithmAnalyzer
from src.analyzer.recurrence_tree_builder import TreeStructure

class AnalysisOrchestrator:
    def __init__(self):
        self.math_engine = MathematicalAnalyzer()
        self.heur_engine = AsymptoticAnalyzer()
        self.rec_engine = RecursiveAlgorithmAnalyzer()
        self.tree_builder = TreeStructure(None)
        self._global_cache = {}

    def process_file(self, file_path: str) -> AnalysisResult:
        if file_path in self._global_cache:
            return self._global_cache[file_path]

        filename = os.path.basename(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            result = self.process_code(code, filename)
            self._global_cache[file_path] = result
            return result
        except Exception as e:
            return AnalysisResult(filename=filename, name="Error IO", code="", ast_node=None, error=str(e))

    def process_code(self, code: str, name_hint: str = "IA_Generated") -> AnalysisResult:
        try:
            ast = parse_code(code)
            functions = getattr(ast, 'functions', [])
            if not functions: raise ValueError("No funciones")
            
            target_func = functions[0]
            raw_name = getattr(target_func, 'name', name_hint)
            func_name = str(raw_name.name) if hasattr(raw_name, 'name') else str(raw_name)
            
            # 1. Recursión
            rec_info = self.rec_engine.analyze_recursive_algorithm(target_func)
            
            # 2. Matemático
            solved_results = self.math_engine.analyze(ast) 
            math_comp = str(solved_results.get(func_name, "No determinado"))
            raw_results = getattr(self.math_engine, 'last_raw_results', {})
            math_expr = str(raw_results.get(func_name, "N/A"))

            # 3. Heurístico
            heur_rec, heur_bound = self.heur_engine.analyze_function_node(target_func, rec_info)
            
            base_cases_str = "N/A"
            if hasattr(heur_rec, 'base_cases') and heur_rec.base_cases:
                base_cases_str = "\n".join([f"   • {k} = {v}" for k, v in heur_rec.base_cases.items()])

            # 4. Árbol
            tree_data = {}
            if rec_info['has_recursion']:
                eq_source = math_expr if "T(n)" in math_expr else heur_rec.equation
                self.tree_builder.analyze_equation(str(eq_source))
                tree_data = self.tree_builder.get_structure()

            # Crear Resultado
            return AnalysisResult(
                filename=name_hint,
                name=func_name,
                code=code,
                ast_node=target_func,
                
                math_expression=math_expr,
                math_complexity=math_comp,
                
                heur_equation=heur_rec.equation,
                heur_base_cases=base_cases_str,
                
                # AQUÍ ESTABA EL CAMBIO CLAVE:
                heur_complexity=f"{heur_bound.notation}({heur_bound.complexity})",
                heur_notation=heur_bound.notation,  # <--- ¡ESTO FALTABA!
                
                heur_method=getattr(heur_rec, 'method_used', 'Análisis Estándar'),
                heur_explanation=heur_bound.explanation,
                
                is_recursive=rec_info['has_recursion'],
                recursion_pattern=rec_info['pattern_type'],
                tree_structure_data=tree_data
            )

        except Exception as e:
            return AnalysisResult(filename=name_hint, name="Error", code=code, ast_node=None, error=str(e))