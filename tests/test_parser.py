from src.parser.parser import parse_code

def test_simple_function():
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
    ast = parse_code(code)
    assert ast is not None
    print(ast)  # Deberías ver un objeto Program con Function → For → Return
