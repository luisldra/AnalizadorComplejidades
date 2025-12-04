from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class AnalysisResult:
    """
    Contenedor unificado de resultados: captura la entrada original, AST,
    salidas de los analizadores (matemático/heurístico), árbol de recurrencia
    y metadatos LLM opcionales para presentarlos en CLI/GUI.
    """
    filename: str
    name: str
    code: str
    ast_node: Any
    math_expression: str = "N/A"
    math_complexity: str = "N/A"
    heur_equation: str = "N/A"
    heur_base_cases: str = "N/A"
    heur_complexity: str = "N/A"
    heur_notation: str = "O(?)"
    heur_method: str = "N/A"
    heur_explanation: str = ""
    is_recursive: bool = False
    recursion_pattern: str = "iterative"
    tree_structure_data: Dict = field(default_factory=dict)
    error: Optional[str] = None
    
    # Campos enriquecidos por LLM
    llm_reasoning: str = ""
    llm_pattern: str = ""
    llm_validation: str = ""
    llm_trace: str = ""
    llm_token_usage: Dict[str, int] = field(default_factory=dict)
    llm_cost_us: Optional[int] = None
    source_prompt: Optional[str] = None  # descripcion en lenguaje natural, si aplica
    
    # Costos por nivel para algoritmos recursivos
    level_costs: list = field(default_factory=list)
    
    # Métrica de tiempo (ms) para el análisis de este algoritmo
    elapsed_ms: Optional[float] = None
