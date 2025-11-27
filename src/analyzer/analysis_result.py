from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class AnalysisResult:
    filename: str
    name: str
    code: str
    ast_node: Any
    math_expression: str = "N/A"
    math_complexity: str = "N/A"
    heur_equation: str = "N/A"
    heur_base_cases: str = "N/A"
    heur_complexity: str = "N/A"
    heur_notation: str = "O(?)"   # <--- ESTE ES EL CAMPO QUE FALTABA
    heur_method: str = "N/A"
    heur_explanation: str = ""
    is_recursive: bool = False
    recursion_pattern: str = "iterative"
    tree_structure_data: Dict = field(default_factory=dict)
    error: Optional[str] = None