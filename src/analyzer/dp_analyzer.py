"""
Dynamic Programming Analyzer - Refactored
=========================================

This module implements the main Dynamic Programming analyzer following SRP.
It coordinates between different specialized components for recurrence analysis.

Following SOLID principles:
- Single Responsibility: Focuses solely on DP-based complexity analysis coordination
- Open/Closed: Extensible through composition of specialized analyzers
- Liskov Substitution: Compatible with existing complexity analysis interfaces
- Interface Segregation: Uses focused interfaces from specialized components
- Dependency Inversion: Depends on abstractions, not concrete implementations
"""

from typing import Dict, List, Optional, Tuple, Any
import hashlib
import json
from src.ast.nodes import *
from src.analyzer.advanced_complexity import ComplexityResult, AdvancedComplexityAnalyzer
from src.analyzer.recurrence_models import RecurrencePattern, RecurrenceTree
from src.analyzer.recurrence_tree_builder import TreeStructure
from src.analyzer.recurrence_visualizer import RecurrenceTreeVisualizer
from src.analyzer.recurrence_solver import RecurrenceSolver, RecursiveAlgorithmAnalyzer


class DynamicProgrammingAnalyzer:
    """
    Main coordinator for Dynamic Programming-based complexity analysis.
    
    Responsibilities:
    - Coordinate between specialized components
    - Manage DP cache for analysis results
    - Provide unified interface for DP analysis
    - Generate comprehensive reports
    
    This class follows SRP by focusing solely on coordination and caching,
    delegating specialized tasks to dedicated components.
    """
    
    def __init__(self):
        # Core DP Cache: Memoization table for analyzed nodes
        self.analysis_cache: Dict[str, ComplexityResult] = {}
        
        # Pattern Cache: Store recognized recurrence patterns
        self.pattern_cache: Dict[str, RecurrencePattern] = {}
        
        # Specialized Components (Dependency Injection)
        self.tree_builder = TreeStructure()
        self.visualizer = RecurrenceTreeVisualizer()
        self.solver = RecurrenceSolver()
        self.recursive_analyzer = RecursiveAlgorithmAnalyzer()
        self.base_analyzer = AdvancedComplexityAnalyzer()
        
        # Statistics for DP performance tracking
        self.cache_hits = 0
        self.cache_misses = 0
        self.patterns_recognized = 0
        
        # Initialize pattern database
        self._initialize_pattern_database()
    
    def _initialize_pattern_database(self):
        """Initialize database of common recurrence patterns using DP principles."""
        
        # Classic DP patterns - this is our "DP table" of known solutions
        patterns = [
            RecurrencePattern(
                pattern_type="linear_recursion",
                base_cases={"T(0)": "1", "T(1)": "1"},
                recurrence_formula="T(n) = T(n-1) + O(1)",
                solution="n",
                confidence=0.95
            ),
            RecurrencePattern(
                pattern_type="binary_recursion",
                base_cases={"T(0)": "1", "T(1)": "1"},
                recurrence_formula="T(n) = 2*T(n-1) + O(1)",
                solution="2^n",
                confidence=0.95
            ),
            RecurrencePattern(
                pattern_type="divide_conquer",
                base_cases={"T(1)": "1"},
                recurrence_formula="T(n) = 2*T(n/2) + O(n)",
                solution="n*log(n)",
                confidence=0.90
            ),
            RecurrencePattern(
                pattern_type="fibonacci_like",
                base_cases={"T(0)": "1", "T(1)": "1"},
                recurrence_formula="T(n) = T(n-1) + T(n-2) + O(1)",
                solution="phi^n",  # Golden ratio
                confidence=0.85
            ),
            RecurrencePattern(
                pattern_type="tree_recursion",
                base_cases={"T(1)": "1"},
                recurrence_formula="T(n) = k*T(n/k) + O(n)",
                solution="n*log(n)",
                confidence=0.85
            )
        ]
        
        for pattern in patterns:
            key = self._generate_pattern_key(pattern.recurrence_formula)
            self.pattern_cache[key] = pattern
    
    def analyze_with_dp(self, node) -> ComplexityResult:
        """
        Main analysis method using Dynamic Programming optimization.
        
        DP Strategy:
        1. Check memoization cache first (overlapping subproblems)
        2. If not cached, perform analysis with pattern recognition
        3. Store result in cache for future use
        4. Use optimal substructure to build complex analyses
        """
        
        # Generate unique key for memoization
        node_key = self._generate_node_key(node)
        
        # Check cache first (DP memoization)
        if node_key in self.analysis_cache:
            self.cache_hits += 1
            return self.analysis_cache[node_key]
        
        self.cache_misses += 1
        
        # Check if this is a recursive function for special handling
        if isinstance(node, Function):
            recursive_analysis = self.recursive_analyzer.analyze_recursive_algorithm(node)
            
            if recursive_analysis['has_recursion']:
                # Use specialized recursive analysis
                result = self._analyze_recursive_function(node, recursive_analysis)
            else:
                # Use standard analysis
                result = self.base_analyzer.analyze(node)
        else:
            # Standard analysis for non-function nodes
            result = self.base_analyzer.analyze(node)
        
        # Store in cache (DP memoization)
        self.analysis_cache[node_key] = result
        return result
    
    def analyze_with_recurrence_tree(self, node, max_levels: int = 4) -> Tuple[ComplexityResult, Optional[RecurrenceTree]]:
        """
        Analyze complexity using both DP cache and recurrence tree visualization.
        
        Returns:
            Tuple of (complexity_result, recurrence_tree)
        """
        
        # Get standard DP analysis
        complexity_result = self.analyze_with_dp(node)
        
        # Try to build recurrence tree if this is a recursive function
        if isinstance(node, Function):
            recursive_analysis = self.recursive_analyzer.analyze_recursive_algorithm(node)
            
            if recursive_analysis['has_recursion'] and recursive_analysis['recurrence_relation']:
                # Build the recurrence tree
                recurrence_tree = self.tree_builder.build_tree(
                    recursive_analysis['recurrence_relation'], 
                    max_levels
                )
                
                # Update complexity result with tree information if more accurate
                tree_complexity = recurrence_tree.get_total_work()
                if tree_complexity and tree_complexity != "O(1)":
                    # Use tree-derived complexity if it's more specific
                    complexity_result.big_o = tree_complexity
                
                return complexity_result, recurrence_tree
        
        # Handle Program nodes - find and analyze recursive functions
        elif isinstance(node, Program) and hasattr(node, 'functions'):
            for function in node.functions:
                if isinstance(function, Function):
                    recursive_analysis = self.recursive_analyzer.analyze_recursive_algorithm(function)
                    
                    if recursive_analysis['has_recursion'] and recursive_analysis['recurrence_relation']:
                        # Build the recurrence tree for the first recursive function found
                        recurrence_tree = self.tree_builder.build_tree(
                            recursive_analysis['recurrence_relation'], 
                            max_levels
                        )
                        
                        # Update complexity result with tree information if more accurate
                        tree_complexity = recurrence_tree.get_total_work()
                        if tree_complexity and tree_complexity != "O(1)":
                            # Use tree-derived complexity if it's more specific
                            complexity_result.big_o = tree_complexity
                        
                        return complexity_result, recurrence_tree
        
        return complexity_result, None
    
    def generate_recurrence_report(self, node) -> str:
        """Generate comprehensive report including recurrence tree analysis."""
        
        complexity_result, recurrence_tree = self.analyze_with_recurrence_tree(node)
        
        report = []
        report.append("🌳 RECURRENCE TREE ANALYSIS REPORT")
        report.append("=" * 50)
        
        report.append(f"\n📊 Complexity Analysis:")
        report.append(f"   Big O (worst case): {complexity_result.big_o}")
        report.append(f"   Omega (best case): {complexity_result.omega}")
        report.append(f"   Theta (tight bound): {complexity_result.theta}")
        
        if recurrence_tree:
            report.append(f"\n🌳 Recurrence Tree:")
            report.append(recurrence_tree.get_level_summary())
            report.append(f"\n📈 Tree Visualization:")
            report.append(self.visualizer.visualize(recurrence_tree))
        else:
            report.append(f"\n⚠️  No recurrence pattern detected - likely non-recursive algorithm")
        
        # Add DP statistics
        stats = self.get_dp_statistics()
        report.append(f"\n🧠 DP Cache Statistics:")
        report.append(f"   Cache hits: {stats['cache_hits']}")
        report.append(f"   Cache misses: {stats['cache_misses']}")
        report.append(f"   Hit rate: {stats['hit_rate_percentage']}%")
        
        return "\n".join(report)
    
    def _analyze_recursive_function(self, function_node: Function, recursive_analysis: Dict) -> ComplexityResult:
        """Analyze a recursive function with DP optimization."""
        
        # Get base analysis
        base_result = self.base_analyzer.analyze_complexity(function_node)
        
        # Try to improve with recurrence pattern recognition
        if recursive_analysis['recurrence_relation']:
            pattern = self._find_matching_pattern(recursive_analysis['recurrence_relation'])
            
            if pattern:
                # Use pattern-based solution
                self.patterns_recognized += 1
                estimated_complexity = self.solver.get_closed_form_solution(pattern)
                
                # Update result with better estimation
                base_result.big_o = estimated_complexity
                base_result.theta = estimated_complexity
        
        return base_result
    
    def _find_matching_pattern(self, recurrence_relation: str) -> Optional[RecurrencePattern]:
        """Find matching pattern in the DP pattern database."""
        
        for pattern in self.pattern_cache.values():
            if pattern.matches_formula(recurrence_relation):
                return pattern
        
        return None
    
    def _generate_node_key(self, node) -> str:
        """Generate unique key for node memoization."""
        
        # Create a hash based on node type and key attributes
        key_data = {
            'type': type(node).__name__,
            'content': str(node)[:100]  # Limit length
        }
        
        # Add specific attributes based on node type
        if hasattr(node, 'name'):
            key_data['name'] = node.name
        
        if hasattr(node, 'body') and node.body:
            key_data['body_length'] = len(node.body)
        
        # Generate hash
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _generate_pattern_key(self, formula: str) -> str:
        """Generate key for pattern caching."""
        return hashlib.md5(formula.encode()).hexdigest()
    
    def get_dp_statistics(self) -> Dict[str, Any]:
        """Get comprehensive DP performance statistics."""
        
        total_accesses = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_accesses * 100) if total_accesses > 0 else 0
        
        return {
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'total_cache_accesses': total_accesses,
            'hit_rate_percentage': round(hit_rate, 2),
            'cache_size': len(self.analysis_cache),
            'patterns_recognized': self.patterns_recognized,
            'known_patterns': len(self.pattern_cache),
            'tree_cache_size': self.tree_builder.get_cache_size(),
            'recursive_analysis_cache': len(self.recursive_analyzer.analysis_cache)
        }
    
    def clear_cache(self):
        """Clear all caches for fresh analysis."""
        self.analysis_cache.clear()
        self.tree_builder.clear_cache()
        self.recursive_analyzer.analysis_cache.clear()
        self.cache_hits = 0
        self.cache_misses = 0
        self.patterns_recognized = 0
    
    def get_optimization_recommendations(self, node) -> List[str]:
        """Get recommendations for optimizing the analyzed algorithm."""
        
        recommendations = []
        
        # Analyze with recurrence tree
        complexity_result, recurrence_tree = self.analyze_with_recurrence_tree(node)
        
        # Check complexity patterns
        if "2^n" in complexity_result.big_o:
            recommendations.append("Exponential complexity detected - consider memoization or DP optimization")
        
        if "n^2" in complexity_result.big_o:
            recommendations.append("Quadratic complexity - look for nested loop optimizations")
        
        if recurrence_tree and recurrence_tree.pattern_type == 'exponential':
            recommendations.append("Exponential recurrence pattern - ideal candidate for DP memoization")
        
        # Check cache efficiency
        stats = self.get_dp_statistics()
        if stats['hit_rate_percentage'] < 50:
            recommendations.append("Low cache hit rate - consider restructuring for better DP optimization")
        
        if not recommendations:
            recommendations.append("Algorithm appears well-optimized for current analysis")
        
        return recommendations