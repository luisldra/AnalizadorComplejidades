# tests/test_math_analyzer.py

import pytest
import sympy
from pathlib import Path

# Add project root to path to allow imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parser.parser import parse_code
from src.analyzer.math_analyzer import MathematicalAnalyzer

# Helper to create a full program string
def make_program(body: str) -> str:
    # A bit of a hack to make sure we always have a function
    if "function" not in body:
        body = f"""
        function main(n)
        begin
            {body}
        end
        """
    return body

# Test cases: tuple of (name, code, expected_complexity)
TEST_CASES = [
    (
        "simple_assignment",
        "a := 1",
        "O(1)"
    ),
    (
        "simple_for_loop",
        """
        for i := 0 to n do
        begin
            a := 1
        end
        """,
        "O(n)"
    ),
    (
        "nested_for_loop",
        """
        for i := 0 to n do
        begin
            for j := 0 to n do
            begin
                a := 1
            end
        end
        """,
        "O(n**2)"
    ),
    (
        "sequential_for_loops",
        """
        for i := 0 to n do
        begin
            a := 1
        end
        for j := 0 to n do
        begin
            b := 1
        end
        """,
        "O(n)" # O(n + n) = O(n)
    ),
    (
        "factorial_recursive",
        """
        function factorial(n)
        begin
            if n <= 1 then
            begin
                return 1
            end
            else
            begin
                return n * call factorial(n - 1)
            end
        end
        """,
        "O(n)" # T(n) = T(n-1) + c
    ),
    (
        "fibonacci_recursive",
        """
        function fib(n)
        begin
            if n <= 1 then
            begin
                return n
            end
            else
            begin
                a := call fib(n-1)
                b := call fib(n-2)
                return a + b
            end
        end
        """,
        "O(2**n)" # T(n) = T(n-1) + T(n-2) + c
    ),
    (
        "binary_search_recursive",
        """
        function binary_search(n)
        begin
            if n <= 1 then
            begin
                return 1
            end
            else
            begin
                return call binary_search(n/2)
            end
        end
        """,
        "O(log(n))" # T(n) = T(n/2) + c
    ),
    (
        "merge_sort_like",
        """
        function merge_sort(n)
        begin
            if n <= 1 then
            begin
                return 1
            end
            
            call merge_sort(n/2)
            call merge_sort(n/2)
            
            for i := 0 to n do
            begin
                a := 1
            end
        end
        """,
        "O(n*log(n))" # T(n) = 2*T(n/2) + n
    )
]

def normalize_complexity_string(value: str) -> str:
    """Normalize equivalent Big-O strings for reliable comparisons."""
    replacements = {
        "log(1/n)": "log(n)",
        "log(1/n**1)": "log(n)"
    }
    normalized = value
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    return normalized


@pytest.mark.parametrize("name, code, expected", TEST_CASES)
def test_mathematical_analyzer(name, code, expected):
    """
    Tests the MathematicalAnalyzer with a variety of algorithms.
    """
    # 1. Parse the code
    program_code = make_program(code)
    ast = parse_code(program_code)
    
    # 2. Analyze the AST
    analyzer = MathematicalAnalyzer()
    results = analyzer.analyze(ast)
    
    # 3. Find the main function's complexity
    # Assuming the first function is the one we want to test
    main_func_name = ast.functions[0].name
    complexity_result = results.get(main_func_name)
    
    assert complexity_result is not None, f"No complexity result for function '{main_func_name}'"
    
    # 4. Compare with expected result
    # The result from the analyzer is a sympy.O object.
    # We rebuild the string to avoid issues with sympy's internal representation like O(n, (n, oo))
    if isinstance(complexity_result, sympy.Order):
        actual_complexity_str = f"O({str(complexity_result.expr)})"
    else:
        actual_complexity_str = str(complexity_result)
    
    # Sympy might produce different but equivalent string representations,
    # so we do a simple normalization (remove spaces).
    # A more robust solution would parse both and compare symbolically.
    actual_norm = normalize_complexity_string(actual_complexity_str).replace(" ", "")
    expected_norm = normalize_complexity_string(expected).replace(" ", "")
    assert actual_norm == expected_norm, \
           f"Test case '{name}' failed."


def test_math_analyzer_linear_tree_text():
    """
    The textual tree analysis should describe linear recurrences.
    """
    analyzer = MathematicalAnalyzer()
    eq = sympy.Eq(analyzer.T(analyzer.n), analyzer.T(analyzer.n - 1) + sympy.Integer(1))
    text = analyzer._generate_tree_textual_analysis(eq)
    assert "Recursión lineal" in text or "lineal" in text.lower()
    assert "T(n - 1)" in text


def test_math_analyzer_busqueda_binaria_example():
    """
    The Spanish binary search example should yield logarithmic complexity.
    """
    base_path = Path(__file__).resolve().parent.parent
    code = (base_path / "examples" / "busqueda_binaria.txt").read_text(encoding="utf-8")
    ast = parse_code(code)
    analyzer = MathematicalAnalyzer()
    results = analyzer.analyze(ast)
    complexity = results.get('busqueda_binaria')
    assert complexity is not None
    assert isinstance(complexity, sympy.Order)
    assert 'log' in str(complexity.expr)
