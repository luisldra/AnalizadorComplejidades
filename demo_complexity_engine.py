"""
Demo for the Complexity Analysis Engine
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.parser.parser import parse_code
from src.analyzer.advanced_complexity import AdvancedComplexityAnalyzer
from src.analyzer.complexity_engine import ComplexityAnalysisEngine

def demo_basic_analysis():
    """Simple demo of the complexity analysis."""
    
    print("🔬 Advanced Complexity Analysis Demo")
    print("=" * 50)
    
    # Test algorithms
    algorithms = [
        {
            "name": "Constant Time",
            "code": """
            function constant_time(n)
            begin
                x 🡨 5
                y 🡨 x + 10
                return y
            end
            """
        },
        {
            "name": "Linear Search",
            "code": """
            function linear_search(n)
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
            "name": "Nested Loops (Quadratic)",
            "code": """
            function matrix_init(n)
            begin
                for i 🡨 0 to n do
                begin
                    for j 🡨 0 to n do
                    begin
                        matrix[i][j] 🡨 0
                    end
                end
            end
            """
        },
        {
            "name": "Conditional Complexity",
            "code": """
            function conditional_work(n, condition)
            begin
                if (condition) then
                begin
                    for i 🡨 0 to n do
                    begin
                        work 🡨 i * 2
                    end
                end
                else
                begin
                    work 🡨 42
                end
                return work
            end
            """
        }
    ]
    
    engine = ComplexityAnalysisEngine()
    
    for i, algorithm in enumerate(algorithms, 1):
        print(f"\n{i}. {algorithm['name']}")
        print("-" * 40)
        
        try:
            # Get detailed analysis
            result = engine.analyze_code(algorithm["code"], detailed=True)
            
            print(f"📊 Complexity Analysis:")
            print(f"   • Big O (worst case): O({result.big_o})")
            print(f"   • Omega (best case): Ω({result.omega})")
            if result.theta:
                print(f"   • Theta (tight bound): Θ({result.theta})")
            else:
                print(f"   • Theta: No tight bound (O ≠ Ω)")
            
            print(f"   • Summary: {result}")
            
            # Get simple analysis (backwards compatibility)
            simple = engine.analyze_code(algorithm["code"], detailed=False)
            print(f"   • Simple notation: {simple}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

def demo_comprehensive_report():
    """Demo of comprehensive analysis report."""
    
    print("\n\n🔍 Comprehensive Analysis Report Demo")
    print("=" * 50)
    
    algorithm = """
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
    
    engine = ComplexityAnalysisEngine()
    
    try:
        report = engine.generate_report(algorithm)
        
        print("📋 Algorithm: Bubble Sort")
        print(f"📊 Complexity: {report['complexity']['summary']}")
        print(f"🏗️  Characteristics:")
        chars = report['characteristics']
        print(f"   • Functions: {chars['function_count']}")
        print(f"   • Has loops: {chars['has_loops']}")
        print(f"   • Has nested loops: {chars['has_nested_loops']}")
        print(f"   • Loop depth: {chars['loop_depth']}")
        print(f"   • Has conditionals: {chars['has_conditionals']}")
        print(f"   • Uses arrays: {chars['has_arrays']}")
        print(f"   • Uses matrices: {chars['has_matrices']}")
        
        print("💡 Analysis Notes:")
        for note in report['analysis_notes']:
            print(f"   • {note}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_basic_analysis()
    demo_comprehensive_report()