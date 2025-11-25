"""
Modelos de Datos para el Análisis de Recurrencia
==============================

Este módulo contiene los modelos de datos utilizados para el análisis de árboles de recurrencia.

Clases:
- RecurrencePattern: Representa un patrón de relación de recurrencia
- RecurrenceTreeNode: Nodo individual en un árbol de recurrencia
- RecurrenceTree: Árbol de recurrencia completo con funciones de análisis
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import re


@dataclass
class RecurrencePattern:
    """
    Representa un patrón de relación de recurrencia para el análisis de programación dinámica.
    
    Responsabilidad: Mantener datos del patrón y proporcionar operaciones básicas del patrón.
    """
    
    pattern_type: str  # 'linear', 'divide_conquer', 'tree', 'exponential'
    base_cases: Dict[str, str]  # Base case complexities
    recurrence_formula: str  # Mathematical formula
    solution: str  # Closed-form solution
    confidence: float  # Confidence in the pattern recognition
    
    def __str__(self):
        return f"{self.pattern_type}: {self.recurrence_formula} → {self.solution}"
    
    def matches_formula(self, formula: str) -> bool:
        """Verifica si una fórmula dada coincide con este patrón."""
        # Coincidencia simple - podría mejorarse con expresiones regulares
        return self.recurrence_formula.lower() in formula.lower()


@dataclass
class RecurrenceTreeNode:
    """
    Representa un nodo en un árbol de recurrencia para el análisis recursivo.
    
    Responsabilidad: Mantener datos del nodo y proporcionar operaciones básicas del nodo.
    """
    
    problem_size: str  # 'n', 'n/2', 'n-1', etc.
    work_done: str     # 'O(n)', 'O(1)', etc.
    level: int         # Level in the tree (0 = root)
    children: List['RecurrenceTreeNode'] = None
    cost_at_level: str = ""  # Cost contribution at this level
    node_id: int = 0   # Unique identifier for hashing
    
    _id_counter = 0  # Class variable for generating unique IDs
    
    def __post_init__(self):
        if self.children is None:
            self.children = []
        # Generate unique ID if not set
        if self.node_id == 0:
            RecurrenceTreeNode._id_counter += 1
            object.__setattr__(self, 'node_id', RecurrenceTreeNode._id_counter)
    
    def __hash__(self):
        """Hacer que el nodo sea hashable usando su ID único."""
        return hash(self.node_id)
    
    def __eq__(self, other):
        """Verificar igualdad basada en el ID del nodo."""
        if not isinstance(other, RecurrenceTreeNode):
            return False
        return self.node_id == other.node_id
    
    def add_child(self, child: 'RecurrenceTreeNode'):
        """Agregar un nodo hijo."""
        self.children.append(child)
    
    def get_children_count(self) -> int:
        """Obtener el número de hijos directos."""
        return len(self.children)
    
    def is_leaf(self) -> bool:
        """Verificar si este es un nodo hoja."""
        return len(self.children) == 0


@dataclass 
class RecurrenceTree:
    """
    Árbol de recurrencia completo con capacidades de análisis.
    
    Responsabilidad: Mantener datos del árbol y proporcionar operaciones a nivel de árbol.
    """
    
    root: RecurrenceTreeNode
    total_levels: int
    recurrence_relation: str  # Original relation like "T(n) = 2T(n/2) + O(n)"
    pattern_type: str        # 'divide_conquer', 'linear', 'tree', etc.
    total_complexity: str    # Final calculated complexity
    level_costs: List[str]   # Cost at each level
    
    def get_tree_height(self) -> int:
        """Calcular la altura del árbol de recurrencia."""
        return self.total_levels
    
    def get_total_work(self) -> str:
        """Calcular el trabajo total realizado en todos los niveles."""
        return self.total_complexity
    
    def get_level_summary(self) -> str:
        """Obtener un resumen de los costos en cada nivel."""
        summary = f"Análisis del Árbol de Recurrencia: {self.recurrence_relation}\n"
        summary += "=" * 50 + "\n"
        
        for i, cost in enumerate(self.level_costs):
            summary += f"Nivel {i}: {cost}\n"
        
        summary += "-" * 50 + "\n"
        summary += f"Complejidad Total: {self.total_complexity}\n"
        return summary
        
    def calculate_complexity_from_tree(self) -> Tuple[str, Dict[str, Any]]:
        """
        Calcular la complejidad total sumando todos los niveles del árbol de recurrencia.
        
        Returns:
            Tupla de (complejidad_total, detalles_del_cálculo)
        """
        
        details = {
            'method': 'tree_summation',
            'levels_analyzed': self.total_levels,
            'level_contributions': [],
            'summation_formula': '',
            'final_result': self.total_complexity
        }
        
        # Analizar la contribución de cada nivel
        total_work_parts = []
        
        for level, cost in enumerate(self.level_costs):
            level_info = {
                'level': level,
                'nodes_count': self._count_nodes_at_level(level),
                'work_per_node': self._extract_work_per_node(cost),
                'total_level_cost': cost
            }
            details['level_contributions'].append(level_info)
            total_work_parts.append(cost)
        
        # Crear fórmula de sumatoria
        if self.pattern_type == 'divide_conquer':
            if 'n log n' in self.total_complexity.lower():
                details['summation_formula'] = 'Σ(level=0 to log n) O(n) = O(n log n)'
            else:
                details['summation_formula'] = f'Σ(level=0 to {self.total_levels-1}) {" + ".join(total_work_parts[:3])}... = {self.total_complexity}'
        elif self.pattern_type == 'exponential':
            details['summation_formula'] = f'Σ(level=0 to n) O(branches^level) = {self.total_complexity}'
        else:
            details['summation_formula'] = f'Σ(level=0 to n) O(1) = O(n)'
        
        return self.total_complexity, details
    
    def _count_nodes_at_level(self, level: int) -> int:
        """Contar el número de nodos en un nivel específico."""
        if level == 0:
            return 1
        
        # Usar BFS para contar nodos en un nivel específico
        current_level_nodes = [self.root]
        current_level = 0
        
        while current_level < level and current_level_nodes:
            next_level_nodes = []
            for node in current_level_nodes:
                next_level_nodes.extend(node.children)
            current_level_nodes = next_level_nodes
            current_level += 1
        
        return len(current_level_nodes)
    
    def _extract_work_per_node(self, cost_description: str) -> str:
        """Extraer el trabajo realizado por nodo a partir de la descripción del costo."""
        # Análisis simple - en la práctica sería más sofisticado
        if 'O(' in cost_description:
            match = re.search(r'O\(([^)]+)\)', cost_description)
            if match:
                return f"O({match.group(1)})"
        return "O(1)"
    
    def visualize_tree(self, max_width: int = 80) -> str:
        """Generar visualización ASCII del árbol de recurrencia."""
        from src.analyzer.recurrence_visualizer import RecurrenceTreeVisualizer
        return RecurrenceTreeVisualizer.visualize(self, max_width)
    
    def get_compact_summary(self) -> str:
        """Obtener un resumen compacto del árbol de recurrencia."""
        from src.analyzer.recurrence_visualizer import RecurrenceTreeVisualizer
        return RecurrenceTreeVisualizer.get_compact_view(self)