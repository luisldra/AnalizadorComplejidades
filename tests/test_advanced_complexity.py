"""
Comprehensive tests for the Advanced Complexity Analyzer
========================================================

This test suite validates the complexity analysis for various algorithmic patterns,
ensuring correct calculation of O, Ω, and Θ notations.
"""

import pytest
from src.parser.parser import parse_code
from src.analyzer.advanced_complexity import AdvancedComplexityAnalyzer, ComplexityResult


class TestBasicComplexity:
    """Test basic complexity analysis for fundamental constructs."""
    
    def test_constant_operations(self):
        """Test that constant operations are O(1), Ω(1), Θ(1)."""
        code = """
        function constant_ops(n)
        begin
            x 🡨 5
            y 🡨 x + 10
            return y * 2
        end
        """
        ast = parse_code(code)
        analyzer = AdvancedComplexityAnalyzer()
        result = analyzer.analyze(ast)
        
        assert result.big_o == "1"
        assert result.omega == "1"
        assert result.theta == "1"
        print(f"✅ Constant operations: {result}")

    def test_linear_loop(self):
        """Test simple linear loop - O(n), Ω(n), Θ(n)."""
        code = """
        function linear_sum(n)
        begin
            sum 🡨 0
            for i 🡨 1 to n do
            begin
                sum 🡨 sum + i
            end
            return sum
        end
        """
        ast = parse_code(code)
        analyzer = AdvancedComplexityAnalyzer()
        result = analyzer.analyze(ast)
        
        assert result.big_o == "n"
        assert result.omega == "n"
        assert result.theta == "n"
        print(f"✅ Linear loop: {result}")

    def test_nested_loops(self):
        """Test nested loops - O(n²), Ω(n²), Θ(n²)."""
        code = """
        function matrix_multiply(n)
        begin
            matrix result[n][n]
            for i 🡨 0 to n do
            begin
                for j 🡨 0 to n do
                begin
                    result[i][j] 🡨 0
                end
            end
            return result[0][0]
        end
        """
        ast = parse_code(code)
        analyzer = AdvancedComplexityAnalyzer()
        result = analyzer.analyze(ast)
        
        assert result.big_o == "n^2"
        assert result.omega == "n^2"
        print(f"✅ Nested loops: {result}")

    def test_triple_nested_loops(self):
        """Test triple nested loops - O(n³)."""
        code = """
        function triple_nested(n)
        begin
            for i 🡨 0 to n do
            begin
                for j 🡨 0 to n do
                begin
                    for k 🡨 0 to n do
                    begin
                        x 🡨 i + j + k
                    end
                end
            end
            return x
        end
        """
        ast = parse_code(code)
        analyzer = AdvancedComplexityAnalyzer()
        result = analyzer.analyze(ast)
        
        assert result.big_o == "n^3"  # Triple nested loops
        print(f"✅ Triple nested loops: {result}")


class TestConditionalComplexity:
    """Test complexity analysis for conditional statements."""
    
    def test_if_else_different_complexities(self):
        """Test if-else with different branch complexities."""
        code = """
        function conditional_complexity(n, condition)
        begin
            if (condition) then
            begin
                for i 🡨 0 to n do
                begin
                    x 🡨 i * 2
                end
            end
            else
            begin
                x 🡨 5
            end
            return x
        end
        """
        ast = parse_code(code)
        analyzer = AdvancedComplexityAnalyzer()
        result = analyzer.analyze(ast)
        
        # Worst case: O(n) (if branch), Best case: Ω(1) (else branch)
        assert result.big_o == "n"
        assert result.omega == "1"
        assert result.theta is None  # O ≠ Ω, so no tight bound
        print(f"✅ If-else different complexities: {result}")

    def test_if_without_else(self):
        """Test if statement without else clause."""
        code = """
        function maybe_loop(n, condition)
        begin
            if (condition) then
            begin
                for i 🡨 0 to n do
                begin
                    x 🡨 i
                end
            end
            return x
        end
        """
        ast = parse_code(code)
        analyzer = AdvancedComplexityAnalyzer()
        result = analyzer.analyze(ast)
        
        # Worst case: O(n), Best case: Ω(1) (just condition check)
        assert result.big_o == "n"
        assert result.omega == "1"
        print(f"✅ If without else: {result}")


class TestArrayMatrixComplexity:
    """Test complexity analysis for array and matrix operations."""
    
    def test_array_initialization(self):
        """Test array initialization complexity."""
        code = """
        function init_array(n)
        begin
            array arr[n]
            for i 🡨 0 to n do
            begin
                arr[i] 🡨 i * 2
            end
            return arr[0]
        end
        """
        ast = parse_code(code)
        analyzer = AdvancedComplexityAnalyzer()
        result = analyzer.analyze(ast)
        
        # Array declaration + loop initialization
        assert result.big_o == "n"
        assert result.omega == "n"
        print(f"✅ Array initialization: {result}")

    def test_matrix_operations(self):
        """Test matrix declaration and operations."""
        code = """
        function matrix_ops(n, m)
        begin
            matrix mat[n][m]
            for i 🡨 0 to n do
            begin
                for j 🡨 0 to m do
                begin
                    mat[i][j] 🡨 i + j
                end
            end
            return mat[0][0]
        end
        """
        ast = parse_code(code)
        analyzer = AdvancedComplexityAnalyzer()
        result = analyzer.analyze(ast)
        
        # Matrix declaration + nested loop initialization
        assert result.big_o == "n^2"  # Assuming n ≈ m
        print(f"✅ Matrix operations: {result}")

    def test_array_search(self):
        """Test linear search in array."""
        code = """
        function linear_search(arr_size, target)
        begin
            array numbers[arr_size]
            found 🡨 false
            index 🡨 0

            for i 🡨 0 to arr_size do
            begin
                numbers[i] 🡨 i * 2
            end

            while (index < arr_size and not found) do
            begin
                if (numbers[index] = target) then
                begin
                    found 🡨 true
                end
                else
                begin
                    index 🡨 index + 1
                end
            end

            return found
        end
        """
        ast = parse_code(code)
        analyzer = AdvancedComplexityAnalyzer()
        result = analyzer.analyze(ast)
        
        # Initialization O(n) + Search O(n) in worst case, Ω(1) if found immediately
        assert result.big_o == "n"
        print(f"✅ Array search: {result}")


class TestBooleanExpressionComplexity:
    """Test complexity analysis for boolean expressions."""
    
    def test_boolean_short_circuit(self):
        """Test boolean expressions with short-circuit evaluation."""
        code = """
        function boolean_ops(n, x, y)
        begin
            if (x > 0 and y < n) then
            begin
                for i 🡨 0 to n do
                begin
                    z 🡨 i
                end
            end
            return z
        end
        """
        ast = parse_code(code)
        analyzer = AdvancedComplexityAnalyzer()
        result = analyzer.analyze(ast)
        
        # Boolean condition evaluation + possible loop
        assert result.big_o == "n"
        assert result.omega == "1"
        print(f"✅ Boolean short circuit: {result}")

    def test_complex_boolean_conditions(self):
        """Test complex nested boolean conditions."""
        code = """
        function complex_boolean(x, y, z, n)
        begin
            if ((x > 0 and y > 0) or (x < 0 and y < 0)) then
            begin
                if (not (z = 0)) then
                begin
                    for i 🡨 0 to n do
                    begin
                        result 🡨 i
                    end
                end
            end
            return result
        end
        """
        ast = parse_code(code)
        analyzer = AdvancedComplexityAnalyzer()
        result = analyzer.analyze(ast)
        
        # Complex boolean evaluation + conditional loop
        assert result.big_o == "n"
        assert result.omega == "1"
        print(f"✅ Complex boolean conditions: {result}")


class TestWhileLoopComplexity:
    """Test complexity analysis for while loops."""
    
    def test_while_loop_linear(self):
        """Test while loop with linear iteration pattern."""
        code = """
        function while_countdown(n)
        begin
            counter 🡨 n
            while (counter > 0) do
            begin
                counter 🡨 counter - 1
            end
            return counter
        end
        """
        ast = parse_code(code)
        analyzer = AdvancedComplexityAnalyzer()
        result = analyzer.analyze(ast)
        
        # While loop that decrements from n to 0
        assert result.big_o == "n"
        assert result.omega == "1"  # Best case: n ≤ 0 initially
        print(f"✅ While loop linear: {result}")

    def test_nested_while_loops(self):
        """Test nested while loops."""
        code = """
        function nested_while(n)
        begin
            i 🡨 0
            while (i < n) do
            begin
                j 🡨 0
                while (j < n) do
                begin
                    result 🡨 i + j
                    j 🡨 j + 1
                end
                i 🡨 i + 1
            end
            return result
        end
        """
        ast = parse_code(code)
        analyzer = AdvancedComplexityAnalyzer()
        result = analyzer.analyze(ast)
        
        # Nested while loops - O(n²) in worst case
        assert result.big_o == "n^2"  # Nested while loops
        print(f"✅ Nested while loops: {result}")


class TestMultipleFunctions:
    """Test complexity analysis for programs with multiple functions."""
    
    def test_multiple_functions_max_complexity(self):
        """Test program with multiple functions - should return max complexity."""
        code = """
        function linear_func(n)
        begin
            for i 🡨 0 to n do
            begin
                x 🡨 i
            end
            return x
        end

        function quadratic_func(n)
        begin
            for i 🡨 0 to n do
            begin
                for j 🡨 0 to n do
                begin
                    y 🡨 i * j
                end
            end
            return y
        end

        function constant_func()
        begin
            return 42
        end
        """
        ast = parse_code(code)
        analyzer = AdvancedComplexityAnalyzer()
        result = analyzer.analyze(ast)
        
        # Should return the maximum complexity among all functions
        assert result.big_o == "n^2"  # From quadratic_func
        print(f"✅ Multiple functions: {result}")


def run_all_tests():
    """Run all complexity analysis tests."""
    print("🧪 Running Advanced Complexity Analyzer Tests\n")
    
    # Create test instances
    basic_tests = TestBasicComplexity()
    conditional_tests = TestConditionalComplexity()
    array_tests = TestArrayMatrixComplexity()
    boolean_tests = TestBooleanExpressionComplexity()
    while_tests = TestWhileLoopComplexity()
    multi_tests = TestMultipleFunctions()
    
    try:
        # Basic complexity tests
        print("📊 Basic Complexity Tests:")
        basic_tests.test_constant_operations()
        basic_tests.test_linear_loop()
        basic_tests.test_nested_loops()
        basic_tests.test_triple_nested_loops()
        
        print("\n🔀 Conditional Complexity Tests:")
        conditional_tests.test_if_else_different_complexities()
        conditional_tests.test_if_without_else()
        
        print("\n📚 Array/Matrix Complexity Tests:")
        array_tests.test_array_initialization()
        array_tests.test_matrix_operations()
        array_tests.test_array_search()
        
        print("\n🔢 Boolean Expression Tests:")
        boolean_tests.test_boolean_short_circuit()
        boolean_tests.test_complex_boolean_conditions()
        
        print("\n🔄 While Loop Tests:")
        while_tests.test_while_loop_linear()
        while_tests.test_nested_while_loops()
        
        print("\n📋 Multiple Functions Tests:")
        multi_tests.test_multiple_functions_max_complexity()
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()