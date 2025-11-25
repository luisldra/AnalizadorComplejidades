"""
Visualizador de Árboles de Recurrencia
=========================

Este módulo se encarga de generar representaciones visuales de árboles de recurrencia.

Clases:
- Visualizador de Árboles de Recurrencia: Genera visualizaciones ASCII de árboles de recurrencia
"""

from typing import List
from src.analyzer.recurrence_models import RecurrenceTree, RecurrenceTreeNode


class RecurrenceTreeVisualizer:
    """
    Genera visualizaciones ASCII de árboles de recurrencia.
    """
    
    @staticmethod
    def visualize(tree: RecurrenceTree, max_width: int = 80) -> str:
        """Crear una representación en arte ASCII del árbol de recurrencia."""
        
        lines = []
        lines.append("Visualización del Árbol de Recurrencia")
        lines.append("=" * max_width)
        lines.append(f"Relación: {tree.recurrence_relation}")
        lines.append(f"Patrón: {tree.pattern_type}")
        lines.append(f"Complejidad Total: {tree.total_complexity}")
        lines.append("")
        
        # Generar estructura del árbol
        tree_lines = RecurrenceTreeVisualizer._generate_tree_lines(tree.root, "", True)
        lines.extend(tree_lines)
        
        lines.append("")
        lines.append("Análisis Nivel por Nivel:")
        lines.append("-" * 30)
        
        for i, cost in enumerate(tree.level_costs):
            lines.append(f"Nivel {i}: {cost}")
        
        return "\n".join(lines)
    
    @staticmethod
    def _generate_tree_lines(node: RecurrenceTreeNode, prefix: str, is_last: bool) -> List[str]:
        """Generar recursivamente líneas del árbol para visualización ASCII."""
        
        lines = []
        
        # Nodo actual
        connector = "└── " if is_last else "├── "
        node_info = f"T({node.problem_size}) → {node.work_done}"
        lines.append(f"{prefix}{connector}{node_info}")
        
        # Preparar prefijo para los hijos
        child_prefix = prefix + ("    " if is_last else "│   ")
        
        # Agregar hijos
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            child_lines = RecurrenceTreeVisualizer._generate_tree_lines(child, child_prefix, is_last_child)
            lines.extend(child_lines)
        
        return lines
    
    @staticmethod
    def generate_compact_view(tree: RecurrenceTree) -> str:
        """Generar una vista compacta que muestre solo la estructura."""
        
        lines = []
        lines.append(f"Árbol: {tree.recurrence_relation} → {tree.total_complexity}")
        
        # Mostrar estructura por niveles
        current_level = [tree.root]
        level = 0
        
        while current_level and level < tree.total_levels:
            level_info = f"L{level}: "
            node_info = []
            
            for node in current_level:
                node_info.append(f"T({node.problem_size})")
            
            level_info += " + ".join(node_info) + f" = {tree.level_costs[level] if level < len(tree.level_costs) else 'O(?)'}"
            lines.append(level_info)
            
            # Obtener siguiente nivel
            next_level = []
            for node in current_level:
                next_level.extend(node.children)
            
            current_level = next_level
            level += 1
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_summary_report(tree: RecurrenceTree) -> str:
        """Generar un informe detallado del árbol."""
        
        lines = []
        lines.append("📊 INFORME DE ANÁLISIS DEL ÁRBOL DE RECURRENCIA")
        lines.append("=" * 50)
        lines.append(f"📝 Relación de Recurrencia: {tree.recurrence_relation}")
        lines.append(f"🏷️  Tipo de Patrón: {tree.pattern_type}")
        lines.append(f"📏 Altura del Árbol: {tree.get_tree_height()} niveles")
        lines.append(f"🎯 Complejidad Final: {tree.total_complexity}")
        lines.append("")
        
        # Level breakdown
        lines.append("📈 Desglose Nivel por Nivel:")
        lines.append("-" * 30)
        
        for level, cost in enumerate(tree.level_costs):
            node_count = tree._count_nodes_at_level(level)
            lines.append(f"  Nivel {level}: {node_count} nodos → {cost}")
        
        lines.append("")
        
        # Complexity calculation details
        complexity, details = tree.calculate_complexity_from_tree()
        lines.append("🧮 Cálculo de Complejidad:")
        lines.append(f"  Método: {details['method']}")
        lines.append(f"  Fórmula: {details['summation_formula']}")
        lines.append(f"  Resultado: {complexity}")
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_simple_tree(tree: RecurrenceTree, max_depth: int = 3) -> str:
        """Generar una vista simplificada del árbol con profundidad limitada."""
        
        lines = []
        lines.append(f"🌳 {tree.recurrence_relation}")
        lines.append("")
        
        # Generate simplified tree
        simplified_lines = RecurrenceTreeVisualizer._generate_simple_tree_lines(
            tree.root, "", True, 0, max_depth
        )
        lines.extend(simplified_lines)
        
        if tree.total_levels > max_depth:
            lines.append("    ... (más niveles)")
        
        lines.append("")
        lines.append(f"📊 Total: {tree.total_complexity}")
        
        return "\n".join(lines)
    
    @staticmethod
    def _generate_simple_tree_lines(node: RecurrenceTreeNode, prefix: str, is_last: bool, 
                                   current_depth: int, max_depth: int) -> List[str]:
        """Generar líneas simplificadas del árbol con límite de profundidad."""
        
        if current_depth >= max_depth:
            return []
        
        lines = []
        
        # Current node
        connector = "└── " if is_last else "├── "
        node_info = f"T({node.problem_size})"
        lines.append(f"{prefix}{connector}{node_info}")
        
        # Add children if within depth limit
        if current_depth < max_depth - 1:
            child_prefix = prefix + ("    " if is_last else "│   ")
            
            for i, child in enumerate(node.children):
                is_last_child = (i == len(node.children) - 1)
                child_lines = RecurrenceTreeVisualizer._generate_simple_tree_lines(
                    child, child_prefix, is_last_child, current_depth + 1, max_depth
                )
                lines.extend(child_lines)
        
        return lines