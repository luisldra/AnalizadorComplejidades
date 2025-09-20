# src/ast/nodes.py

class Node:
    pass

class Program(Node):
    def __init__(self, functions):
        self.functions = functions

class Function(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body  # lista de statements

class Assignment(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class For(Node):
    def __init__(self, var, start, end, body):
        self.var = var
        self.start = start
        self.end = end
        self.body = body

class While(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class If(Node):
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

class Repeat(Node):
    def __init__(self, body, condition):
        self.body = body
        self.condition = condition

class Return(Node):
    def __init__(self, expr):
        self.expr = expr

class Call(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args

# ---- Expresiones ----
class BinOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Var(Node):
    def __init__(self, name):
        self.name = name

class Number(Node):
    def __init__(self, value):
        self.value = int(value)

class Condition(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

# ---- Arrays y Matrices ----
class ArrayAccess(Node):
    def __init__(self, name, index):
        self.name = name
        self.index = index

class MatrixAccess(Node):
    def __init__(self, name, row_index, col_index):
        self.name = name
        self.row_index = row_index
        self.col_index = col_index

class ArrayDeclaration(Node):
    def __init__(self, name, size):
        self.name = name
        self.size = size

class MatrixDeclaration(Node):
    def __init__(self, name, rows, cols):
        self.name = name
        self.rows = rows
        self.cols = cols

# ---- Expresiones Booleanas ----
class BoolOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op  # 'and', 'or'
        self.right = right

class UnaryOp(Node):
    def __init__(self, op, operand):
        self.op = op  # 'not'
        self.operand = operand

class Boolean(Node):
    def __init__(self, value):
        self.value = bool(value)
