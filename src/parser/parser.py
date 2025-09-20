from lark import Lark
from src.parser.transformer import ASTTransformer

with open("src/parser/grammar.lark") as f:
    grammar = f.read()

parser = Lark(grammar, start="start", parser="earley")

def parse_code(code):
    tree = parser.parse(code)
    transformer = ASTTransformer()
    return transformer.transform(tree)
