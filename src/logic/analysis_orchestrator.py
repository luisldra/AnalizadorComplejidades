import os
import time
from typing import Optional
import sympy as sp
from src.parser.parser import parse_code
from src.analyzer.analysis_result import AnalysisResult
from src.analyzer.math_analyzer import MathematicalAnalyzer
from src.analyzer.asymptotic_analyzer import AsymptoticAnalyzer
from src.analyzer.recurrence_solver import RecursiveAlgorithmAnalyzer
from src.analyzer.recurrence_tree_builder import TreeStructure

try:
    from src.llm.gemini_service import GeminiService
except Exception:
    GeminiService = None


class AnalysisOrchestrator:
    def __init__(self):
        self.math_engine = MathematicalAnalyzer()
        self.heur_engine = AsymptoticAnalyzer()
        self.rec_engine = RecursiveAlgorithmAnalyzer()
        self.tree_builder = TreeStructure(None)
        self._global_cache = {}
        self.llm_service: Optional[GeminiService] = None

    # ----------------- Entrada por archivo -----------------
    def process_file(self, file_path: str) -> AnalysisResult:
        if file_path in self._global_cache:
            return self._global_cache[file_path]

        filename = os.path.basename(file_path)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            result = self.process_code(code, filename)
            self._global_cache[file_path] = result
            return result
        except Exception as e:
            return AnalysisResult(filename=filename, name="Error IO", code="", ast_node=None, error=str(e))

    # ----------------- Entrada en lenguaje natural -----------------
    def process_natural_description(self, description: str, name_hint: str = "NL_Request") -> AnalysisResult:
        """
        Traduce lenguaje natural a pseudocodigo con el LLM y ejecuta el pipeline completo.
        """
        svc = self._get_llm_service()
        if not svc:
            return AnalysisResult(filename=name_hint, name="Error", code="", ast_node=None, error="LLM no disponible")

        code = svc.translate_natural_language(description)
        result = self.process_code(code, name_hint, use_llm=True, llm_service=svc, source_prompt=description)
        return result

    # ----------------- Pipeline principal -----------------
    def process_code(self, code: str, name_hint: str = "IA_Generated", use_llm: bool = False, llm_service=None, source_prompt: str = None) -> AnalysisResult:
        try:
            t0 = time.perf_counter()
            ast = parse_code(code)
            functions = getattr(ast, "functions", [])
            if not functions:
                raise ValueError("No funciones")

            target_func = functions[0]
            raw_name = getattr(target_func, "name", name_hint)
            func_name = str(raw_name.name) if hasattr(raw_name, "name") else str(raw_name)

            # 1. Recursion
            rec_info = self.rec_engine.analyze_recursive_algorithm(target_func)

            # 2. Motor matematico
            solved_results = self.math_engine.analyze(ast)
            math_comp = str(solved_results.get(func_name, "No determinado"))
            raw_results = getattr(self.math_engine, "last_raw_results", {})
            math_expr = str(raw_results.get(func_name, "N/A"))

            # 3. Motor heuristico formal
            heur_rec, heur_bound = self.heur_engine.analyze_function_node(target_func, rec_info)
            level_costs = []
            if rec_info.get("has_recursion") and heur_rec and getattr(heur_rec, "equation", None):
                try:
                    level_costs = self.heur_engine.estimate_level_costs(heur_rec.equation)
                except Exception:
                    level_costs = []

            base_cases_str = "N/A"
            if hasattr(heur_rec, "base_cases") and heur_rec.base_cases:
                base_cases_str = "\n".join([f"   * {k} = {v}" for k, v in heur_rec.base_cases.items()])

            # 4. Arbol de recurrencia
            tree_data = {}
            if rec_info["has_recursion"]:
                eq_source = math_expr if "T(n)" in math_expr else heur_rec.equation
                self.tree_builder.analyze_equation(str(eq_source))
                tree_data = self.tree_builder.get_structure()

            result = AnalysisResult(
                filename=name_hint,
                name=func_name,
                code=code,
                ast_node=target_func,
                math_expression=math_expr,
                math_complexity=math_comp,
                heur_equation=heur_rec.equation,
                heur_base_cases=base_cases_str,
                heur_complexity=f"{heur_bound.notation}({heur_bound.complexity})",
                heur_notation=heur_bound.notation,
                heur_method=getattr(heur_rec, "method_used", "Analisis Estandar"),
                heur_explanation=heur_bound.explanation,
                is_recursive=rec_info["has_recursion"],
                recursion_pattern=rec_info["pattern_type"],
                tree_structure_data=tree_data,
                source_prompt=source_prompt,
                level_costs=level_costs
            )

            # 5. Enriquecimiento opcional via LLM
            if use_llm:
                svc = llm_service or self._get_llm_service()
                if svc:
                    try:
                        result.llm_pattern = svc.classify_pattern(code)
                        result.llm_reasoning = svc.explain_steps(code)
                        result.llm_validation = svc.validate_recurrence(code, heur_rec.equation, result.heur_complexity)
                        result.llm_trace = svc.generate_trace_diagram(code)
                        result.llm_token_usage = svc.last_token_usage or {}
                        result.llm_cost_us = svc.estimate_cost_us(result.llm_token_usage)
                    except Exception as llm_error:
                        print(f"Advertencia LLM: {llm_error}")

            # Registrar tiempo total de análisis
            result.elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)

            return result

        except Exception as e:
            return AnalysisResult(filename=name_hint, name="Error", code=code, ast_node=None, error=str(e))

    # ----------------- Helpers -----------------
    def _get_llm_service(self):
        if self.llm_service:
            return self.llm_service
        if not GeminiService:
            return None
        try:
            self.llm_service = GeminiService()
            return self.llm_service
        except Exception as e:
            print(f"LLM deshabilitado: {e}")
            return None
