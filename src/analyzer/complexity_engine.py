"""
Integration module for the Advanced Complexity Analyzer
=======================================================

This module provides a clean interface to integrate the advanced complexity analyzer
with the existing parser system, maintaining backwards compatibility while adding
enhanced analysis capabilities.
"""

from src.parser.parser import parse_code
from src.analyzer.advanced_complexity import AdvancedComplexityAnalyzer, ComplexityResult
from typing import Union, Dict, Any


class ComplexityAnalysisEngine:
    """
    Main engine for complexity analysis that integrates parsing and analysis.
    Provides both simple and detailed analysis modes.
    """
    
    def __init__(self):
        self.analyzer = AdvancedComplexityAnalyzer()
    
    def analyze_code(self, pseudocode: str, detailed: bool = True) -> Union[str, ComplexityResult]:
        """
        Analyze pseudocode and return complexity analysis.
        
        Args:
            pseudocode: The pseudocode string to analyze
            detailed: If True, return ComplexityResult with O, Ω, Θ. If False, return just O notation.
        
        Returns:
            ComplexityResult object if detailed=True, otherwise just the O notation string
        """
        try:
            # Parse the pseudocode into AST
            ast = parse_code(pseudocode)
            
            # Analyze the AST
            result = self.analyzer.analyze(ast)
            
            if detailed:
                return result
            else:
                return f"O({result.big_o})"  # Backwards compatibility
                
        except Exception as e:
            raise ValueError(f"Error analyzing pseudocode: {e}")
    
    def analyze_file(self, filepath: str, detailed: bool = True) -> Union[str, ComplexityResult]:
        """
        Analyze pseudocode from a file.
        
        Args:
            filepath: Path to the pseudocode file
            detailed: If True, return ComplexityResult with O, Ω, Θ. If False, return just O notation.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                pseudocode = f.read()
            return self.analyze_code(pseudocode, detailed)
        except FileNotFoundError:
            raise FileNotFoundError(f"Pseudocode file not found: {filepath}")
        except Exception as e:
            raise ValueError(f"Error reading or analyzing file {filepath}: {e}")
    
    def generate_report(self, pseudocode: str) -> Dict[str, Any]:
        """
        Generate a comprehensive analysis report.
        
        Args:
            pseudocode: The pseudocode string to analyze
            
        Returns:
            Dictionary containing detailed analysis information
        """
        result = self.analyze_code(pseudocode, detailed=True)
        
        # Extract algorithm characteristics
        ast = parse_code(pseudocode)
        characteristics = self._analyze_algorithm_characteristics(ast)
        
        return {
            "complexity": {
                "big_o": result.big_o,
                "omega": result.omega,
                "theta": result.theta,
                "summary": str(result)
            },
            "characteristics": characteristics,
            "pseudocode": pseudocode.strip(),
            "analysis_notes": self._generate_analysis_notes(result, characteristics)
        }
    
    def _analyze_algorithm_characteristics(self, ast) -> Dict[str, Any]:
        """Analyze structural characteristics of the algorithm."""
        characteristics = {
            "has_loops": False,
            "has_nested_loops": False,
            "has_recursion": False,
            "has_conditionals": False,
            "has_arrays": False,
            "has_matrices": False,
            "loop_depth": 0,
            "function_count": 0
        }
        
        def analyze_node(node, depth=0):
            if hasattr(node, '__class__'):
                node_type = node.__class__.__name__
                
                if node_type == 'Program':
                    characteristics["function_count"] = len(node.functions)
                    for func in node.functions:
                        analyze_node(func, depth)
                        
                elif node_type == 'Function':
                    for stmt in node.body:
                        analyze_node(stmt, depth)
                        
                elif node_type in ['For', 'While', 'Repeat']:
                    characteristics["has_loops"] = True
                    current_depth = depth + 1
                    characteristics["loop_depth"] = max(characteristics["loop_depth"], current_depth)
                    
                    if current_depth > 1:
                        characteristics["has_nested_loops"] = True
                    
                    # Analyze loop body
                    if hasattr(node, 'body'):
                        for stmt in node.body:
                            analyze_node(stmt, current_depth)
                            
                elif node_type == 'If':
                    characteristics["has_conditionals"] = True
                    for stmt in node.then_body:
                        analyze_node(stmt, depth)
                    if node.else_body:
                        for stmt in node.else_body:
                            analyze_node(stmt, depth)
                            
                elif node_type == 'Call':
                    # Simple heuristic for recursion detection
                    # In a more sophisticated version, we'd track function names
                    pass
                    
                elif node_type in ['ArrayAccess', 'ArrayDeclaration']:
                    characteristics["has_arrays"] = True
                    
                elif node_type in ['MatrixAccess', 'MatrixDeclaration']:
                    characteristics["has_matrices"] = True
                
                # Recursively analyze child nodes
                if hasattr(node, '__dict__'):
                    for attr_value in node.__dict__.values():
                        if isinstance(attr_value, list):
                            for item in attr_value:
                                analyze_node(item, depth)
                        elif hasattr(attr_value, '__class__') and hasattr(attr_value.__class__, '__name__'):
                            analyze_node(attr_value, depth)
        
        analyze_node(ast)
        return characteristics
    
    def _generate_analysis_notes(self, result: ComplexityResult, characteristics: Dict[str, Any]) -> list:
        """Generate human-readable analysis notes."""
        notes = []
        
        # Complexity interpretation
        if result.theta:
            notes.append(f"Tight complexity bound: Θ({result.theta}) - algorithm has exact complexity")
        else:
            notes.append(f"Complexity range: O({result.big_o}) worst case, Ω({result.omega}) best case")
        
        # Structural analysis
        if characteristics["has_nested_loops"]:
            notes.append(f"Contains nested loops (depth: {characteristics['loop_depth']}) - likely polynomial complexity")
        elif characteristics["has_loops"]:
            notes.append("Contains loops - likely linear or higher complexity")
        
        if characteristics["has_conditionals"]:
            notes.append("Contains conditional statements - complexity may vary based on input")
        
        if characteristics["has_arrays"] or characteristics["has_matrices"]:
            data_structures = []
            if characteristics["has_arrays"]:
                data_structures.append("arrays")
            if characteristics["has_matrices"]:
                data_structures.append("matrices")
            notes.append(f"Uses {', '.join(data_structures)} - memory access patterns affect performance")
        
        # Performance insights
        if result.big_o in ["1"]:
            notes.append("Excellent performance - constant time complexity")
        elif result.big_o in ["n", "log n"]:
            notes.append("Good performance - scales well with input size")
        elif result.big_o in ["n^2"]:
            notes.append("Moderate performance - quadratic scaling may be problematic for large inputs")
        elif "^" in result.big_o and int(result.big_o.split("^")[1]) > 2:
            notes.append("Poor performance - polynomial complexity with high degree")
        elif "2^" in result.big_o:
            notes.append("Very poor performance - exponential complexity")
            
        return notes


def demo_analysis():
    """Demonstrate the complexity analysis engine with various algorithms."""
    
    engine = ComplexityAnalysisEngine()
    
    algorithms = [
        {
            "name": "Linear Search",
            "code": """
            function linear_search(n, target)
            begin
                for i 🡨 0 to n do
                begin
                    if (arr[i] = target) then
                    begin
                        return i
                    end
                end
                return -1
            end
            """
        },
        {
            "name": "Bubble Sort",
            "code": """
            function bubble_sort(n)
            begin
                for i 🡨 0 to n do
                begin
                    for j 🡨 0 to n - i do
                    begin
                        if (arr[j] > arr[j + 1]) then
                        begin
                            temp 🡨 arr[j]
                            arr[j] 🡨 arr[j + 1]
                            arr[j + 1] 🡨 temp
                        end
                    end
                end
            end
            """
        },
        {
            "name": "Matrix Multiplication",
            "code": """
            function matrix_multiply(n)
            begin
                matrix result[n][n]
                for i 🡨 0 to n do
                begin
                    for j 🡨 0 to n do
                    begin
                        result[i][j] 🡨 0
                        for k 🡨 0 to n do
                        begin
                            result[i][j] 🡨 result[i][j] + a[i][k] * b[k][j]
                        end
                    end
                end
                return result[0][0]
            end
            """
        }
    ]
    
    print("🔬 Complexity Analysis Engine Demo")
    print("=" * 50)
    
    for i, algorithm in enumerate(algorithms, 1):
        print(f"\n{i}. {algorithm['name']}")
        print("-" * 30)
        
        try:
            report = engine.generate_report(algorithm["code"])
            
            print(f"📊 Complexity: {report['complexity']['summary']}")
            print(f"🏗️  Structure: ", end="")
            chars = report['characteristics']
            structure_info = []
            if chars['has_nested_loops']:
                structure_info.append(f"nested loops (depth {chars['loop_depth']})")
            elif chars['has_loops']:
                structure_info.append("loops")
            if chars['has_conditionals']:
                structure_info.append("conditionals")
            if chars['has_arrays']:
                structure_info.append("arrays")
            if chars['has_matrices']:
                structure_info.append("matrices")
            print(", ".join(structure_info) if structure_info else "simple operations")
            
            print("💡 Analysis Notes:")
            for note in report['analysis_notes']:
                print(f"   • {note}")
                
        except Exception as e:
            print(f"❌ Error analyzing {algorithm['name']}: {e}")


if __name__ == "__main__":
    demo_analysis()