from lark import Transformer, v_args
from src.ast.nodes import *

@v_args(inline=True)
class ASTTransformer(Transformer):

    def start(self, *functions):
        return Program(list(functions))

    def function(self, name, *args):
        # Handle optional params: either (name, params, body) or (name, body)
        # Convert name properly - it might be a Var object or string
        func_name = name.name if hasattr(name, 'name') else str(name)
        
        if len(args) == 2:
            params, body = args
            return Function(func_name, params or [], body)
        elif len(args) == 1:
            body = args[0]
            return Function(func_name, [], body)
        else:
            raise ValueError(f"Unexpected arguments for function: {args}")

    def params(self, *params):
        return [str(p) for p in params]

    def block(self, *statements):
        return list(statements)
    
    def statement(self, stmt):
        return stmt

    def assignment(self, name, _assign, expr):
        return Assignment(str(name), expr)

    def for_statement(self, name, _assign, start, end, body):
        return For(str(name), start, end, body)

    def while_statement(self, cond, body):
        return While(cond, body)

    def if_statement(self, cond, then_body, *else_body):
        return If(cond, then_body, else_body[0] if else_body else None)

    def repeat_statement(self, body, cond):
        return Repeat(body, cond)

    def return_statement(self, expr):
        return Return(expr)

    def call_statement(self, name, args=None):
        return Call(str(name), args or [])

    def args(self, *args):
        return list(args)

    # ---- expresiones ----
    def add(self, left, right):
        return BinOp(left, '+', right)

    def sub(self, left, right):
        return BinOp(left, '-', right)

    def mul(self, left, right):
        return BinOp(left, '*', right)

    def div(self, left, right):
        return BinOp(left, '/', right)

    def NAME(self, token):
        return Var(str(token))

    def NUMBER(self, token):
        return Number(token)

    # ---- conditions ----
    def condition(self, left, comparator, right):
        return Condition(left, str(comparator), right)
    
    def comparator(self, *args):
        # Debug: see what we're getting
        if args:
            return str(args[0])
        else:
            # If no args, return a default operator (this shouldn't happen in correct grammar)
            return "<"  # Default fallback

    # ---- call expressions ----
    def call_expr(self, name, args=None):
        return Call(str(name), args or [])

    # ---- arrays ----
    def array_assignment(self, name, index, _assign, expr):
        return Assignment(ArrayAccess(str(name), index), expr)
    
    def array_declaration(self, name, size):
        return ArrayDeclaration(str(name), size)
    
    def array_access(self, name, index):
        return ArrayAccess(str(name), index)

    # ---- matrices ----
    def matrix_assignment(self, name, row_index, col_index, _assign, expr):
        return Assignment(MatrixAccess(str(name), row_index, col_index), expr)
    
    def matrix_declaration(self, name, rows, cols):
        return MatrixDeclaration(str(name), rows, cols)
    
    def matrix_access(self, name, row_index, col_index):
        return MatrixAccess(str(name), row_index, col_index)

    # ---- boolean expressions ----
    def bool_or(self, left, _or, right):
        return BoolOp(left, 'or', right)
    
    def bool_and(self, left, _and, right):
        return BoolOp(left, 'and', right)
    
    def bool_not(self, _not, operand):
        return UnaryOp('not', operand)
    
    def bool_true(self):
        return Boolean(True)
    
    def bool_false(self):
        return Boolean(False)
