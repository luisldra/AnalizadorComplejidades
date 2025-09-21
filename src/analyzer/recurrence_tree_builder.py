"""
Recurrence Tree Builder
======================

This module is responsible for constructing recurrence trees from mathematical relations.
Following SRP, this module focuses solely on tree construction logic.

Classes:
- RecurrenceTreeBuilder: Constructs recurrence trees from mathematical relations
"""

from typing import Dict, List, Optional, Tuple, Any
import re
import math
from src.analyzer.recurrence_models import RecurrenceTree, RecurrenceTreeNode, RecurrencePattern


class RecurrenceTreeBuilder:
    """
    Constructs recurrence trees from mathematical relations for visualization and analysis.
    
    Responsibility: Build and construct recurrence trees from mathematical formulas.
    """
    
    def __init__(self):
        self.built_trees: Dict[str, RecurrenceTree] = {}
    
    def build_tree(self, recurrence_relation: str, max_levels: int = 5) -> RecurrenceTree:
        """
        Build a recurrence tree from a mathematical relation.
        
        Args:
            recurrence_relation: String like "T(n) = 2T(n/2) + O(n)"
            max_levels: Maximum depth to build the tree
            
        Returns:
            Complete RecurrenceTree with all levels and costs calculated
        """
        
        # Check cache first
        cache_key = f"{recurrence_relation}_{max_levels}"
        if cache_key in self.built_trees:
            return self.built_trees[cache_key]
        
        # Parse the recurrence relation
        pattern_info = self._parse_recurrence(recurrence_relation)
        
        if not pattern_info:
            # Create a simple linear tree as fallback
            tree = self._build_linear_tree(max_levels)
        else:
            # Build the tree based on pattern type
            if pattern_info['type'] == 'divide_conquer':
                tree = self._build_divide_conquer_tree(pattern_info, max_levels)
            elif pattern_info['type'] == 'linear':
                tree = self._build_linear_recurrence_tree(pattern_info, max_levels)
            elif pattern_info['type'] == 'exponential':
                tree = self._build_exponential_tree(pattern_info, max_levels)
            else:
                tree = self._build_generic_tree(pattern_info, max_levels)
        
        # Cache the result
        self.built_trees[cache_key] = tree
        return tree
    
    def _parse_recurrence(self, relation: str) -> Optional[Dict]:
        """Parse recurrence relation string into components."""
        
        # Common patterns to recognize
        patterns = {
            'divide_conquer': r'T\(n\)\s*=\s*(\d+)T\(n/(\d+)\)\s*\+\s*O\((.+?)\)',
            'linear': r'T\(n\)\s*=\s*T\(n-(\d+)\)\s*\+\s*O\((.+?)\)',
            'exponential': r'T\(n\)\s*=\s*(\d+)T\(n-(\d+)\)\s*\+\s*O\((.+?)\)'
        }
        
        for pattern_type, regex in patterns.items():
            match = re.match(regex, relation.replace(' ', ''))
            if match:
                if pattern_type == 'divide_conquer':
                    return {
                        'type': pattern_type,
                        'branches': int(match.group(1)),
                        'division_factor': int(match.group(2)),
                        'work_per_level': match.group(3),
                        'original': relation
                    }
                elif pattern_type == 'linear':
                    return {
                        'type': pattern_type,
                        'decrement': int(match.group(1)),
                        'work_per_call': match.group(2),
                        'original': relation
                    }
                elif pattern_type == 'exponential':
                    return {
                        'type': pattern_type,
                        'branches': int(match.group(1)),
                        'decrement': int(match.group(2)),
                        'work_per_call': match.group(3),
                        'original': relation
                    }
        
        return None
    
    def _build_divide_conquer_tree(self, pattern_info: Dict, max_levels: int) -> RecurrenceTree:
        """Build tree for divide & conquer recurrences like T(n) = 2T(n/2) + O(n)."""
        
        branches = pattern_info['branches']
        division_factor = pattern_info['division_factor']
        work_per_level = pattern_info['work_per_level']
        
        # Calculate tree height: log_division_factor(n)
        tree_height = max_levels
        
        # Build the root
        root = RecurrenceTreeNode(
            problem_size="n",
            work_done=f"O({work_per_level})",
            level=0,
            cost_at_level=f"O({work_per_level})"
        )
        
        # Build levels recursively
        self._build_dc_level(root, branches, division_factor, work_per_level, 1, max_levels)
        
        # Calculate level costs
        level_costs = []
        for level in range(tree_height):
            nodes_at_level = branches ** level
            if work_per_level == 'n':
                cost = f"{nodes_at_level} × O(n/{division_factor**level}) = O(n)"
            elif work_per_level == '1':
                cost = f"{nodes_at_level} × O(1) = O({nodes_at_level})"
            else:
                cost = f"{nodes_at_level} × O({work_per_level})"
            level_costs.append(cost)
        
        # Determine total complexity
        if work_per_level == 'n':
            total_complexity = "O(n log n)"
        elif work_per_level == '1':
            total_complexity = f"O(n^{math.log(branches, division_factor):.2f})"
        else:
            total_complexity = "O(n log n)"  # Generic case
        
        return RecurrenceTree(
            root=root,
            total_levels=tree_height,
            recurrence_relation=pattern_info['original'],
            pattern_type='divide_conquer',
            total_complexity=total_complexity,
            level_costs=level_costs
        )
    
    def _build_dc_level(self, parent: RecurrenceTreeNode, branches: int, division_factor: int, 
                       work: str, current_level: int, max_levels: int):
        """Recursively build divide & conquer tree levels."""
        
        if current_level >= max_levels:
            return
        
        for i in range(branches):
            child_size = f"{parent.problem_size}/{division_factor}"
            if parent.problem_size == "n":
                if current_level == 1:
                    child_size = f"n/{division_factor}"
                else:
                    child_size = f"n/{division_factor**current_level}"
            
            child = RecurrenceTreeNode(
                problem_size=child_size,
                work_done=f"O({work})",
                level=current_level,
                cost_at_level=f"O({work})"
            )
            
            parent.add_child(child)
            self._build_dc_level(child, branches, division_factor, work, current_level + 1, max_levels)
    
    def _build_linear_tree(self, max_levels: int) -> RecurrenceTree:
        """Build a simple linear recurrence tree."""
        
        root = RecurrenceTreeNode(
            problem_size="n",
            work_done="O(1)",
            level=0,
            cost_at_level="O(1)"
        )
        
        current = root
        for level in range(1, max_levels):
            child = RecurrenceTreeNode(
                problem_size=f"n-{level}",
                work_done="O(1)",
                level=level,
                cost_at_level="O(1)"
            )
            current.add_child(child)
            current = child
        
        level_costs = ["O(1)"] * max_levels
        
        return RecurrenceTree(
            root=root,
            total_levels=max_levels,
            recurrence_relation="T(n) = T(n-1) + O(1)",
            pattern_type='linear',
            total_complexity="O(n)",
            level_costs=level_costs
        )
    
    def _build_linear_recurrence_tree(self, pattern_info: Dict, max_levels: int) -> RecurrenceTree:
        """Build tree for linear recurrences like T(n) = T(n-1) + O(1)."""
        return self._build_linear_tree(max_levels)
    
    def _build_exponential_tree(self, pattern_info: Dict, max_levels: int) -> RecurrenceTree:
        """Build tree for exponential recurrences like T(n) = 2T(n-1) + O(1)."""
        
        branches = pattern_info['branches']
        work = pattern_info['work_per_call']
        
        root = RecurrenceTreeNode(
            problem_size="n",
            work_done=f"O({work})",
            level=0,
            cost_at_level=f"O({work})"
        )
        
        self._build_exp_level(root, branches, work, 1, max_levels)
        
        level_costs = []
        for level in range(max_levels):
            nodes_at_level = branches ** level
            cost = f"{nodes_at_level} × O({work}) = O({nodes_at_level})"
            level_costs.append(cost)
        
        return RecurrenceTree(
            root=root,
            total_levels=max_levels,
            recurrence_relation=pattern_info['original'],
            pattern_type='exponential',
            total_complexity=f"O({branches}^n)",
            level_costs=level_costs
        )
    
    def _build_exp_level(self, parent: RecurrenceTreeNode, branches: int, work: str,
                        current_level: int, max_levels: int):
        """Recursively build exponential tree levels."""
        
        if current_level >= max_levels:
            return
        
        for i in range(branches):
            child = RecurrenceTreeNode(
                problem_size=f"n-{current_level}",
                work_done=f"O({work})",
                level=current_level,
                cost_at_level=f"O({work})"
            )
            parent.add_child(child)
            self._build_exp_level(child, branches, work, current_level + 1, max_levels)
    
    def _build_generic_tree(self, pattern_info: Dict, max_levels: int) -> RecurrenceTree:
        """Build a generic tree structure."""
        return self._build_linear_tree(max_levels)
    
    def clear_cache(self):
        """Clear the built trees cache."""
        self.built_trees.clear()
    
    def get_cache_size(self) -> int:
        """Get the number of cached trees."""
        return len(self.built_trees)