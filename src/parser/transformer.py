from lark import Transformer, v_args
from src.ast.nodes import *

@v_args(inline=True)
class ASTTransformer(Transformer):

    def start(self, *functions):
        return Program(list(functions))

    def function(self, function_token, name, *args):
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

    def block(self, begin_token, *statements_and_end):
        # Remove the END token from the end
        statements = statements_and_end[:-1] if statements_and_end else []
        return list(statements)
    
    def statement(self, stmt):
        return stmt

    def assignment(self, name, _assign, expr):
        return Assignment(str(name), expr)

    def for_statement(self, _for, name, _assign, start, _to, end, _do, body):
        return For(str(name), start, end, body)

    def while_statement(self, *args):
        """
        Normaliza las distintas formas de while:
        WHILE cond block
        WHILE (cond) block
        WHILE cond DO block
        WHILE (cond) DO block
        Con @v_args(inline=True) pueden llegar tokens extra; tomamos los dos
        últimos elementos como (cond, body).
        """
        cond = args[-2]
        body = args[-1]
        return While(cond, body)

    def if_statement(self, *args):
        # Handle different if statement formats
        if len(args) == 6:
            # IF cond THEN body ELSE body
            if_token, cond, then_token, then_body, else_token, else_body = args
            return If(cond, then_body, else_body)
        elif len(args) == 5:
            # IF cond body ELSE body
            if_token, cond, then_body, else_token, else_body = args
            return If(cond, then_body, else_body)
        elif len(args) == 4:
            # IF cond THEN body
            if_token, cond, then_token, then_body = args
            return If(cond, then_body, None)
        elif len(args) == 3:
            # IF cond body
            if_token, cond, then_body = args
            return If(cond, then_body, None)
        else:
            raise ValueError(f"Unexpected if_statement arguments: {args}")

    def repeat_statement(self, body, cond):
        return Repeat(body, cond)

    def return_statement(self, return_token, expr):
        return Return(expr)

    def call_statement(self, call_token, name, *args):
        # CALL NAME "(" args? ")" generates: CALL, NAME, and optionally args
        # Handle name properly - it might be a Var object or string
        call_name = name.name if hasattr(name, 'name') else str(name)
        # args is either empty tuple or tuple with single args list
        arg_list = args[0] if args else []
        return Call(call_name, arg_list)

    def args(self, *args):
        return list(args)

    # ---- expresiones ----
    def add(self, left, right):
        return BinOp(left, '+', right)

    def sub(self, left, right):
        return BinOp(left, '-', right)

    def neg(self, value):
        if isinstance(value, Number):
            return Number(-value.value)
        return BinOp(Number(0), '-', value)

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
    
    def var_condition(self, var, comparator, expr):
        return Condition(Var(str(var)), str(comparator), expr)
    
    def expr_var_condition(self, expr, comparator, var):
        return Condition(expr, str(comparator), Var(str(var)))
    
    def var_bool(self, var):
        return Var(str(var))
    
    def comparator(self, *args):
        # Debug: see what we're getting
        if args:
            return str(args[0])
        else:
            # If no args, return a default operator (this shouldn't happen in correct grammar)
            return "<"  # Default fallback

    # ---- call expressions ----
    def call_expr(self, call_token, name, args=None):
        # Handle name properly - it might be a Var object or string
        call_name = name.name if hasattr(name, 'name') else str(name)
        return Call(call_name, args or [])

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
