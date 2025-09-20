from src.parser import parser

def main():
    code = """
    function suma(n)
    begin
      s 🡨 0
      for i 🡨 1 to n do
        s 🡨 s + i
      end
      return s
    end
    """
    tree = parser.parse_code(code)
    print(tree.pretty())

if __name__ == "__main__":
    main()
