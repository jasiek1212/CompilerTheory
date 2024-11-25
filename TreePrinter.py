from __future__ import print_function
import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.programNode)
    def printTree(self, indent=0):
        self.instructions.printTree(indent)

    @addToClass(AST.InstructionsNode)
    def printTree(self, indent=0):
        for instr in self.instructions:
            instr.printTree(indent)


    @addToClass(AST.Bin_RelExprNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}{self.op}")
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.IDNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}{self.name}")

    @addToClass(AST.ExpressionNode)
    def printTree(self, indent=0):
        if self.typ == -1:
            print(f"{'|  ' * indent}MINUS")
            self.inside.printTree(indent + 1)
        else:
            self.inside.printTree(indent)

    @addToClass(AST.MatrixFuncNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}{self.func}")
        self.expr.printTree(indent+1)



    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}{self.value}")


    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}{self.value}")


    @addToClass(AST.NegateExprNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}NEGATE")
        self.expr.printTree(indent+1)

    @addToClass(AST.AssignExpression)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}{self.operator}")
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)


    @addToClass(AST.TransposeNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}TRANSPOSE")
        self.factor.printTree(indent + 1)


    @addToClass(AST.ForNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}FOR")
        print(f"{'|  ' * (indent + 1)}{self.ID}")
        print(f"{'|  ' * (indent + 1)}RANGE")
        self.start.printTree(indent + 2)
        self.end.printTree(indent + 2)
        self.body.printTree(indent + 1)

    @addToClass(AST.PrintNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}PRINT")
        self.value.printTree(indent)

    @addToClass(AST.WhileNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}WHILE")
        self.condition.printTree(indent)
        self.body.printTree(indent + 1)

    @addToClass(AST.IfElseNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}IF")
        self.condition.printTree(indent)
        print(f"{'|  ' * indent}THEN")
        self.if_body.printTree(indent + 1)

        if (self.else_body == None):
            return

        print(f"{'|  ' * indent}ELSE")
        self.else_body.printTree(indent + 1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass
        # fill in the body