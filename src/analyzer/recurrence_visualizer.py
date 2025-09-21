"""
Recurrence Tree Visualizer
=========================

This module is responsible for generating visual representations of recurrence trees.
Following SRP, this module focuses solely on visualization logic.

Classes:
- RecurrenceTreeVisualizer: Generates ASCII visualizations of recurrence trees
"""

from typing import List
from src.analyzer.recurrence_models import RecurrenceTree, RecurrenceTreeNode


class RecurrenceTreeVisualizer:
    """
    Generates ASCII visualizations of recurrence trees.
    
    Responsibility: Create visual representations of tree structures.
    """
    
    @staticmethod
    def visualize(tree: RecurrenceTree, max_width: int = 80) -> str:
        """Create ASCII art representation of the recurrence tree."""
        
        lines = []
        lines.append("Recurrence Tree Visualization")
        lines.append("=" * max_width)
        lines.append(f"Relation: {tree.recurrence_relation}")
        lines.append(f"Pattern: {tree.pattern_type}")
        lines.append(f"Total Complexity: {tree.total_complexity}")
        lines.append("")
        
        # Generate tree structure
        tree_lines = RecurrenceTreeVisualizer._generate_tree_lines(tree.root, "", True)
        lines.extend(tree_lines)
        
        lines.append("")
        lines.append("Level-by-Level Analysis:")
        lines.append("-" * 30)
        
        for i, cost in enumerate(tree.level_costs):
            lines.append(f"Level {i}: {cost}")
        
        return "\n".join(lines)
    
    @staticmethod
    def _generate_tree_lines(node: RecurrenceTreeNode, prefix: str, is_last: bool) -> List[str]:
        """Recursively generate tree lines for ASCII visualization."""
        
        lines = []
        
        # Current node
        connector = "└── " if is_last else "├── "
        node_info = f"T({node.problem_size}) → {node.work_done}"
        lines.append(f"{prefix}{connector}{node_info}")
        
        # Prepare prefix for children
        child_prefix = prefix + ("    " if is_last else "│   ")
        
        # Add children
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            child_lines = RecurrenceTreeVisualizer._generate_tree_lines(child, child_prefix, is_last_child)
            lines.extend(child_lines)
        
        return lines
    
    @staticmethod
    def generate_compact_view(tree: RecurrenceTree) -> str:
        """Generate a compact view showing just the structure."""
        
        lines = []
        lines.append(f"Tree: {tree.recurrence_relation} → {tree.total_complexity}")
        
        # Show level structure
        current_level = [tree.root]
        level = 0
        
        while current_level and level < tree.total_levels:
            level_info = f"L{level}: "
            node_info = []
            
            for node in current_level:
                node_info.append(f"T({node.problem_size})")
            
            level_info += " + ".join(node_info) + f" = {tree.level_costs[level] if level < len(tree.level_costs) else 'O(?)'}"
            lines.append(level_info)
            
            # Get next level
            next_level = []
            for node in current_level:
                next_level.extend(node.children)
            
            current_level = next_level
            level += 1
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_summary_report(tree: RecurrenceTree) -> str:
        """Generate a detailed summary report of the tree."""
        
        lines = []
        lines.append("📊 RECURRENCE TREE ANALYSIS REPORT")
        lines.append("=" * 50)
        lines.append(f"📝 Recurrence Relation: {tree.recurrence_relation}")
        lines.append(f"🏷️  Pattern Type: {tree.pattern_type}")
        lines.append(f"📏 Tree Height: {tree.get_tree_height()} levels")
        lines.append(f"🎯 Final Complexity: {tree.total_complexity}")
        lines.append("")
        
        # Level breakdown
        lines.append("📈 Level-by-Level Breakdown:")
        lines.append("-" * 30)
        
        for level, cost in enumerate(tree.level_costs):
            node_count = tree._count_nodes_at_level(level)
            lines.append(f"  Level {level}: {node_count} nodes → {cost}")
        
        lines.append("")
        
        # Complexity calculation details
        complexity, details = tree.calculate_complexity_from_tree()
        lines.append("🧮 Complexity Calculation:")
        lines.append(f"  Method: {details['method']}")
        lines.append(f"  Formula: {details['summation_formula']}")
        lines.append(f"  Result: {complexity}")
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_simple_tree(tree: RecurrenceTree, max_depth: int = 3) -> str:
        """Generate a simplified tree view with limited depth."""
        
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
        """Generate simplified tree lines with depth limit."""
        
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