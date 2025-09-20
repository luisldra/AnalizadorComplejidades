import pytest
from src.parser.parser import parse_code

def test_arrays():
    """Test array declaration, access, and assignment"""
    code = """
    function test_arrays(n)
    begin
        array arr[10]
        arr[0] 🡨 5
        arr[1] 🡨 arr[0] + 1
        return arr[1]
    end
    """
    ast = parse_code(code)
    assert ast is not None
    assert len(ast.functions) == 1
    print("✅ Arrays test passed")

def test_matrices():
    """Test matrix declaration, access, and assignment"""
    code = """
    function test_matrices(n, m)
    begin
        matrix mat[n][m]
        mat[0][0] 🡨 1
        mat[0][1] 🡨 mat[0][0] * 2
        return mat[0][1]
    end
    """
    ast = parse_code(code)
    assert ast is not None
    assert len(ast.functions) == 1
    print("✅ Matrices test passed")

def test_boolean_expressions():
    """Test boolean operators: and, or, not"""
    code = """
    function test_booleans(a, b, c)
    begin
        x 🡨 true
        y 🡨 false
        z 🡨 x and y
        w 🡨 x or y
        v 🡨 not x
        if (a > b and b < c) then
        begin
            return true
        end
        else
        begin
            return false
        end
    end
    """
    ast = parse_code(code)
    assert ast is not None
    assert len(ast.functions) == 1
    print("✅ Boolean expressions test passed")

def test_multiple_functions():
    """Test multiple function declarations in one file"""
    code = """
    function factorial(n)
    begin
        if (n <= 1) then
        begin
            return 1
        end
        else
        begin
            return n * call factorial(n - 1)
        end
    end

    function fibonacci(n)
    begin
        if (n <= 1) then
        begin
            return n
        end
        else
        begin
            return call fibonacci(n - 1) + call fibonacci(n - 2)
        end
    end

    function main()
    begin
        x 🡨 call factorial(5)
        y 🡨 call fibonacci(10)
        return x + y
    end
    """
    ast = parse_code(code)
    assert ast is not None
    assert len(ast.functions) == 3
    
    function_names = [func.name for func in ast.functions]
    assert "factorial" in function_names
    assert "fibonacci" in function_names
    assert "main" in function_names
    print("✅ Multiple functions test passed")

def test_complex_array_operations():
    """Test complex operations with arrays and boolean logic"""
    code = """
    function array_search(arr_size, target)
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
    assert ast is not None
    assert len(ast.functions) == 1
    print("✅ Complex array operations test passed")

def test_matrix_multiplication():
    """Test matrix operations with nested loops"""
    code = """
    function matrix_multiply(n)
    begin
        matrix a[n][n]
        matrix b[n][n] 
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
    ast = parse_code(code)
    assert ast is not None
    assert len(ast.functions) == 1
    print("✅ Matrix multiplication test passed")

def test_boolean_conditions_complex():
    """Test complex boolean conditions"""
    code = """
    function complex_conditions(x, y, z)
    begin
        if ((x > 0 and y > 0) or (x < 0 and y < 0)) then
        begin
            if (not (z = 0)) then
            begin
                return true and not false
            end
        end
        return false or (true and false)
    end
    """
    ast = parse_code(code)
    assert ast is not None
    assert len(ast.functions) == 1
    print("✅ Complex boolean conditions test passed")