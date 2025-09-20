import pytest
from src.parser import parser

# --- util para imprimir el árbol ---
def parse_and_show(code):
    ast = parser.parse_code(code)
    print(f"AST: {type(ast).__name__} with {len(ast.functions)} function(s)")  # para verificar la estructura del AST
    return ast


def test_asignacion_simple():
    code = """
    function identidad(n)
    begin
        x 🡨 n
        return x
    end
    """
    tree = parse_and_show(code)
    assert tree is not None


def test_for_loop():
    code = """
    function suma(n)
    begin
        s 🡨 0
        for i 🡨 1 to n do
        begin
            s 🡨 s + i
        end
        return s
    end
    """
    tree = parse_and_show(code)
    assert tree is not None


def test_while_loop():
    code = """
    function cuenta(n)
    begin
        i 🡨 0
        while (i < n) do
        begin
            i 🡨 i + 1
        end
        return i
    end
    """
    tree = parse_and_show(code)
    assert tree is not None


def test_repeat_until():
    code = """
    function contar(n)
    begin
        i 🡨 0
        repeat
        begin
            i 🡨 i + 1
        end
        until (i = n)
        return i
    end
    """
    tree = parse_and_show(code)
    assert tree is not None


def test_if_else():
    code = """
    function maximo(a, b)
    begin
        if (a > b) then
        begin
            return a
        end
        else
        begin
            return b
        end
    end
    """
    tree = parse_and_show(code)
    assert tree is not None


def test_function_call():
    code = """
    function cuadrado(n)
    begin
        return n * n
    end

    function suma_cuadrados(n, m)
    begin
        x 🡨 call cuadrado(n)
        y 🡨 call cuadrado(m)
        return x + y
    end
    """
    tree = parse_and_show(code)
    assert tree is not None


def test_nested_loops():
    code = """
    function nested(n)
    begin
        s 🡨 0
        for i 🡨 1 to n do
        begin
            for j 🡨 1 to n do
            begin
                s 🡨 s + 1
            end
        end
        return s
    end
    """
    tree = parse_and_show(code)
    assert tree is not None
