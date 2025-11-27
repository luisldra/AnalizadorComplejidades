from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class AnalysisResult:
    """
    DTO con TODOS los detalles necesarios para el reporte completo.
    """
    filename: str
    name: str
    code: str
    ast_node: Any
    
    # --- Motor Matemático ---
    math_expression: str = "N/A"
    math_complexity: str = "N/A"
    
    # --- Motor Heurístico ---
    heur_equation: str = "N/A"
    heur_base_cases: str = "N/A"
    heur_complexity: str = "N/A"      # Ej: "Θ(n)"
    heur_notation: str = "O(?)"       # Ej: "Θ" (ESTE FALTABA)
    heur_method: str = "N/A"
    heur_explanation: str = ""
    
    # --- Estructural ---
    is_recursive: bool = False
    recursion_pattern: str = "iterative"
    
    # --- Gráficos ---
    tree_structure_data: Dict = field(default_factory=dict)
    
    # --- Error ---
    error: Optional[str] = None