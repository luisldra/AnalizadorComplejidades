"""
Recurrence Analysis Data Models
==============================

This module contains the data models used for recurrence tree analysis.
Following SRP (Single Responsibility Principle), this module is solely
responsible for defining the data structures.

Classes:
- RecurrencePattern: Represents a recurrence relation pattern
- RecurrenceTreeNode: Individual node in a recurrence tree
- RecurrenceTree: Complete recurrence tree with analysis capabilities
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import re


@dataclass
class RecurrencePattern:
    """
    Represents a recurrence relation pattern for dynamic programming analysis.
    
    Responsibility: Hold pattern data and provide basic pattern operations.
    """
    
    pattern_type: str  # 'linear', 'divide_conquer', 'tree', 'exponential'
    base_cases: Dict[str, str]  # Base case complexities
    recurrence_formula: str  # Mathematical formula
    solution: str  # Closed-form solution
    confidence: float  # Confidence in the pattern recognition
    
    def __str__(self):
        return f"{self.pattern_type}: {self.recurrence_formula} → {self.solution}"
    
    def matches_formula(self, formula: str) -> bool:
        """Check if a given formula matches this pattern."""
        # Simple matching - could be enhanced with regex
        return self.recurrence_formula.lower() in formula.lower()


@dataclass
class RecurrenceTreeNode:
    """
    Represents a node in a recurrence tree for recursive analysis.
    
    Responsibility: Hold node data and provide basic node operations.
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
        """Make node hashable using its unique ID."""
        return hash(self.node_id)
    
    def __eq__(self, other):
        """Check equality based on node ID."""
        if not isinstance(other, RecurrenceTreeNode):
            return False
        return self.node_id == other.node_id
    
    def add_child(self, child: 'RecurrenceTreeNode'):
        """Add a child node."""
        self.children.append(child)
    
    def get_children_count(self) -> int:
        """Get the number of direct children."""
        return len(self.children)
    
    def is_leaf(self) -> bool:
        """Check if this is a leaf node."""
        return len(self.children) == 0


@dataclass 
class RecurrenceTree:
    """
    Complete recurrence tree with analysis capabilities.
    
    Responsibility: Hold tree data and provide tree-level operations.
    """
    
    root: RecurrenceTreeNode
    total_levels: int
    recurrence_relation: str  # Original relation like "T(n) = 2T(n/2) + O(n)"
    pattern_type: str        # 'divide_conquer', 'linear', 'tree', etc.
    total_complexity: str    # Final calculated complexity
    level_costs: List[str]   # Cost at each level
    
    def get_tree_height(self) -> int:
        """Calculate the height of the recurrence tree."""
        return self.total_levels
    
    def get_total_work(self) -> str:
        """Calculate total work done across all levels."""
        return self.total_complexity
    
    def get_level_summary(self) -> str:
        """Get a summary of costs at each level."""
        summary = f"Recurrence Tree Analysis: {self.recurrence_relation}\n"
        summary += "=" * 50 + "\n"
        
        for i, cost in enumerate(self.level_costs):
            summary += f"Level {i}: {cost}\n"
        
        summary += "-" * 50 + "\n"
        summary += f"Total Complexity: {self.total_complexity}\n"
        return summary
        
    def calculate_complexity_from_tree(self) -> Tuple[str, Dict[str, Any]]:
        """
        Calculate total complexity by summing all levels of the recurrence tree.
        
        Returns:
            Tuple of (total_complexity, calculation_details)
        """
        
        details = {
            'method': 'tree_summation',
            'levels_analyzed': self.total_levels,
            'level_contributions': [],
            'summation_formula': '',
            'final_result': self.total_complexity
        }
        
        # Analyze each level's contribution
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
        
        # Create summation formula
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
        """Count the number of nodes at a specific level."""
        if level == 0:
            return 1
        
        # Use BFS to count nodes at specific level
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
        """Extract the work done per node from cost description."""
        # Simple parsing - in practice would be more sophisticated
        if 'O(' in cost_description:
            match = re.search(r'O\(([^)]+)\)', cost_description)
            if match:
                return f"O({match.group(1)})"
        return "O(1)"
    
    def visualize_tree(self, max_width: int = 80) -> str:
        """Generate ASCII visualization of the recurrence tree."""
        from src.analyzer.recurrence_visualizer import RecurrenceTreeVisualizer
        return RecurrenceTreeVisualizer.visualize(self, max_width)
    
    def get_compact_summary(self) -> str:
        """Get a compact summary of the recurrence tree."""
        from src.analyzer.recurrence_visualizer import RecurrenceTreeVisualizer
        return RecurrenceTreeVisualizer.get_compact_view(self)