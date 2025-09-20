from src.parser.parser import parse_code
from src.analyzer.complexity import ComplexityAnalyzer

def test_complexity_suma():
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
    analyzer = ComplexityAnalyzer()
    result = analyzer.analyze(ast)
    assert result == "O(n)"
    print("Complejidad:", result)
