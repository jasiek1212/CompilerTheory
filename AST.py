class Node(object):
    def __init__(self, lineno):
        self.lineno = lineno

    pass


class InstructionsNode(Node):
    def __init__(self, instructions, lineno):
        super().__init__(lineno)
        self.instructions = instructions




class programNode(Node):
    def __init__(self, instructions, lineno):
        super().__init__(lineno)
        self.instructions = instructions


class End_InstructionNode(Node):
    def __init__(self, instruction, lineno):
        super().__init__(lineno)
        self.instruction = instruction



class NonEnd_InstructionNode(Node):
    def __init__(self, instruction, lineno):
        super().__init__(lineno)
        self.instruction = instruction

    pass


class AssignExpression(Node):
    def __init__(self, left, operator, right, lineno):
        super().__init__(lineno)
        self.left = left
        self.operator = operator
        self.right = right

    pass


class FactorNode(Node):
    def __init__(self, op, data, lineno):
        super().__init__(lineno)
        self.op = op
        self.data = data

    pass


class Bin_RelExprNode(Node):
    def __init__(self, op, left, right, lineno):
        super().__init__(lineno)
        self.op = op
        self.left = left
        self.right = right

    pass


class NegateExprNode(Node):
    def __init__(self, expr, lineno):
        super().__init__(lineno)
        self.expr = expr

    pass


class TransposeNode(Node):
    def __init__(self, factor, lineno):
        super().__init__(lineno)
        self.factor = factor

    pass


class MatrixFuncNode(Node):
    def __init__(self, func, expr, lineno):
        super.__init__(lineno)
        self.func = func
        self.expr = expr

    pass


class ExpressionNode(Node):
    def __init__(self, typ, inside, lineno):
        super().__init__(lineno)
        self.typ = typ
        self.inside = inside

    pass


class BreakStatement(Node):
    def __init__(self, lineno):
        super().__init__(lineno)

    pass


class ContinueStatement(Node):
    def __init__(self, lineno):
        super().__init__(lineno)

    pass


class ReturnStatement(Node):
    def __init__(self, expr, lineno):
        super().__init__(lineno)
        self.expr = expr

    pass


class BlankStatement(Node):
    def __init__(self, lineno):
        super().__init__(lineno)

    pass


class NumberNode(Node):
    def __init__(self, number, lineno):
        super().__init__(lineno)
        self.number = number

    pass


class IntNum(Node):
    def __init__(self, value, lineno):
        super().__init__(lineno)
        self.value = value


class FloatNum(Node):
    def __init__(self, value, lineno):
        super().__init__(lineno)
        self.value = value


class IDNode(Node):
    def __init__(self, name, lineno):
        super().__init__(lineno)
        self.name = name


class ValueListNode(Node):
    def __init__(self, values, lineno):
        super().__init__(lineno)
        self.values = values


class WhileNode(Node):
    def __init__(self, condition, body, lineno):
        super().__init__(lineno)
        self.condition = condition
        self.body = body


class ForNode(Node):
    def __init__(self, ID, start, end, body, lineno):
        super().__init__(lineno)
        self.ID = ID
        self.start = start
        self.end = end
        self.body = body


class IfElseNode(Node):
    def __init__(self, condition, if_body, else_body=None, lineno=0):
        super().__init__(lineno)
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body


class StringNode(Node):
    def __init__(self, name, lineno):
        super().__init__(lineno)
        self.name = name.strip("\"")


class PrintNode(Node):
    def __init__(self, value, lineno):
        super().__init__(lineno)
        self.value = value


class Error(Node):
    def __init__(self, lineno):
        super().__init__(lineno)
        pass
