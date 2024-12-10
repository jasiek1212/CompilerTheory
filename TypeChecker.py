from collections import defaultdict
import AST
from SymbolTable import SymbolTable, VariableSymbol
from scanner_sly import Scanner as Sc

# types
ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: "")))

ttype["+"]["int"]["int"] = "int"
ttype["+"]["int"]["float"] = "float"
ttype["+"]["float"]["int"] = "float"
ttype["+"]["float"]["float"] = "float"

ttype["-"]["int"]["int"] = "int"
ttype["-"]["int"]["float"] = "float"
ttype["-"]["float"]["int"] = "float"
ttype["-"]["float"]["float"] = "float"

ttype["*"]["int"]["int"] = "int"
ttype["*"]["int"]["float"] = "float"
ttype["*"]["float"]["int"] = "float"
ttype["*"]["float"]["float"] = "float"

ttype["*"]["int"]["matrix"] = "matrix"
ttype["*"]["float"]["matrix"] = "matrix"
ttype["*"]["matrix"]["int"] = "matrix"
ttype["*"]["matrix"]["float"] = "matrix"
ttype["*"]["matrix"]["matrix"] = "matrix"

ttype["/"]["int"]["int"] = "float"
ttype["/"]["int"]["float"] = "float"
ttype["/"]["float"]["int"] = "float"
ttype["/"]["float"]["float"] = "float"

ttype["/"]["matrix"]["int"] = "matrix"
ttype["/"]["matrix"]["float"] = "matrix"

ttype[".+"]["matrix"]["matrix"] = "matrix"
ttype[".-"]["matrix"]["matrix"] = "matrix"
ttype[".*"]["matrix"]["matrix"] = "matrix"
ttype["./"]["matrix"]["matrix"] = "matrix"

ttype["+"]["string"]["string"] = "string"
ttype["*"]["string"]["int"] = "string"
ttype["*"]["int"]["string"] = "string"


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for _, value in node.__dict__.items():
            if isinstance(value, list):  # xd
                for item in value:
                    if isinstance(item, AST.Node):
                        self.visit(item)
            elif isinstance(value, AST.Node):
                self.visit(value)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.errors = []
        self.current_scope = SymbolTable(None, "program")

    def new_error(self, line, message):
        self.errors.append(f"Error at line {line}: {message}")

    def visit_InstructionsNode(self, node):
        try:
            for instruction in node.instructions:
                self.visit(instruction)
        except:
            print("Tu sie wywala: ", instruction, node.lineno)

    # def visit_AssignExpression(self, node):
    #     type = self.visit(node.right)

    #     if (isinstance(node.left, AST.MatrixRefNode)):
    #         return  # to jest coś typu x[1] = 0;

    #     var_name = node.left.value
    #     var_type = "var"
    #     size = None
    #     row_sizes = []
    #     # z jakiegoś powodu MatrixNode nie jest z ExpressionNode a reszta tak
    #     if (isinstance(node.right, AST.MatrixNode)):
    #         var_type = "matrix"
    #         size = len(node.right.values.values)
    #         for row in node.right.values.values:
    #             if (isinstance(row, AST.StringOfNumNode)):
    #                 row_sizes.append(len(row.values))

    #     elif (isinstance(node.right, AST.BinExpr)):
    #         var_type = type

    #     elif (isinstance(node.right.expr, AST.IntNum)):
    #         var_type = "int"
    #     elif (isinstance(node.right.expr, AST.FloatNum)):
    #         var_type = "float"
    #     elif (isinstance(node.right.expr, AST.StringNode)):
    #         var_type = "string"
    #     elif (isinstance(node.right.expr, AST.MatrixFuncNode)):
    #         var_type = "matrix"
    #         size = node.right.expr.arg
    #         for row in range(size):
    #             row_sizes.append(size)

    #     # MATRIX INITIALIZATION CHECK
    #     if (isinstance(node.right, AST.MatrixNode)):
    #         row_len = -1
    #         if (isinstance(node.right.values, AST.MatrixRowsNode)):
    #             for row in node.right.values.values:  # xd2
    #                 if (row_len == -1):
    #                     row_len = len(row.values)
    #                 elif (len(row.values) != row_len):
    #                     self.new_error(
    #                         node.lineno, "Incorrect size of matrix rows!")
    #                     return
    #     # -----------------------------

    #     var = VariableSymbol(var_name, var_type, size, row_sizes)

    #     if var_type != "":
    #         self.current_scope.put(var_name, var)
    #         self.visit(node.left)

    def visit_AssignExpression(self, node):
        var_type = None
        size = None
        row_sizes = []

        type = self.visit(node.right)

        if isinstance(node.left, AST.MatrixRefNode):
            return

        var_name = node.left.name

        if type == 'matrix':
            var_type = 'matrix'

            size = node.right.size
            if isinstance(node.right, AST.MatrixFuncNode):
                node.left.size = size
                print(size)
            else:
                #from here on i dont know if it works
                for row in node.right.values.values:
                    if isinstance(row, AST.StringOfIntsNode):
                        row_sizes.append(len(row.ints))

                # Sprawdzenie poprawności inicjalizacji macierzy
                row_len = -1
                for row in node.right.values.values:
                    if row_len == -1:
                        row_len = len(row.ints)
                    elif len(row.ints) != row_len:
                        self.new_error(node.lineno, "Incorrect size of matrix rows!")
                        return

        elif isinstance(node.right, AST.Bin_RelExprNode):
            var_type = type

        elif isinstance(node.right, AST.IntNum):
            var_type = "int"

        elif isinstance(node.right, AST.FloatNum):
            var_type = "float"

        elif isinstance(node.right, AST.StringNode):
            var_type = "string"


        if var_type is None:
            self.new_error(node.lineno, "Unknown type in assignment!")
            return

        var = VariableSymbol(var_name, var_type, size)

        self.current_scope.put(var_name, var)

    def visit_Bin_RelExprNode(self, node):
        if node.op in [Sc.EQ, Sc.GE, Sc.LT, Sc.LT, Sc.GT, Sc.NEQ]:
            return self.visit_RelationExpression(self, node)
        return self.visit_BinExpr(self, node)
    
    def visit_MatrixFuncNode(self, node):
        # Sprawdź, czy argument wyrażenia `node.expr` jest poprawny
        expr_type = self.visit(node.expr)
        print(expr_type)

        if expr_type not in ["int", "float"]:
            self.new_error(node.lineno, f"Invalid argument type for {node.func}: {expr_type}")
            return None

        # Wylicz wielkość macierzy
        if isinstance(node.expr, AST.IntNum):
            size = node.expr.value
        elif isinstance(node.expr, AST.Bin_RelExprNode):
            size = self.evaluate_constant_expression(node.expr)
            if size is None or size <= 0:
                self.new_error(node.lineno, f"Invalid dimensions for {node.func}: {node.expr}")
                return None
        else:
            self.new_error(node.lineno, f"Unsupported expression for {node.func}: {node.expr}")
            return None

        node.size = (size, size)
        return "matrix"

    def visit_RelationExpression(self, node):
        self.visit(node.left)
        self.visit(node.right)
        return "int"  # 0/1

    def visit_IDRefNode(self, node):
        # VARIABLE IN SCOPE CHECK
        var = self.current_scope.get(node.value)
        if (var == None):
            self.new_error(
                node.lineno, "Variable does not exist in this scope!")

    def visit_ExpressionNode(self, node):
        return self.visit(node.expr)

    def visit_ZerosNode(self, node):
        return "matrix"

    def visit_OnesNode(self, node):
        return "matrix"

    def visit_EyeNode(self, node):
        return "matrix"

    def visit_ValueListNode(self, node):
        node.size = len(node.values)
        self.visit(node.values)

    def visit_MatrixRowsNode(self, node):
        for value in node.values:
            self.visit(value)

    def visit_StringOfNumNode(self, node):
        pass

    def visit_MatrixRefNode(self, node):
        self.visit(node.values)

        # VARIABLE IN SCOPE CHECK
        matrix = self.current_scope.get(node.id)
        if (not matrix):
            self.new_error(node.lineno, "Unknown variable!")
            return

        # MATRIX BOUNDS CHCECK
        if (matrix.size == None):
            self.new_error(node.lineno, "Variable type error!")

        args = node.values.values
        if (len(args) == 1):
            if (args[0] >= matrix.size):
                self.new_error(node.lineno, "Out of array scope!")
        elif (len(args) == 2):
            if (args[0] >= matrix.size):
                self.new_error(node.lineno, "Out of array scope!")
            elif (args[1] >= matrix.row_sizes[args[0]]):
                self.new_error(node.lineno, "Out of array scope!")

    def visit_IntNum(self, node):
        return "int"

    def visit_FloatNum(self, node):
        return "float"

    def visit_NegateExprNode(self, node):
        return self.visit(node.expr)

    def visit_IDNode(self, node):
        var = self.current_scope.get(node.name)
        if (var == None):
            self.new_error(node.lineno, "Unknown variable!")
        return var.type

    def visit_TransposeNode(self, node):
        return self.visit(node.expr)

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op

        type = ttype[op][type1][type2]

        if type == "":
            self.new_error(node.lineno, "Unknown type!")

        if (type != "" and type1 == "matrix" and type2 == "matrix" 
            and isinstance(node.left.expr, AST.IDNode) and isinstance(node.right.expr, AST.IDNode)): # x d   X D
            m1 = self.current_scope.get(node.left.expr.name)
            m2 = self.current_scope.get(node.right.expr.name)

            if m1.row_sizes != m2.row_sizes and (op == ".+" or op == ".-" or op == ".*" or op =="./"):
                self.new_error(
                    node.lineno, "Operations (.+|.-|.*|./) on matrices with unequal sizes!")

            if m1.size == 0 or m2.size == 0:
                self.new_error(
                    node.lineno, "Can not perform multiplication on empty matrix!")
            elif m1.size != m2.row_sizes[0] and op == "*":
                self.new_error(
                    node.lineno, "Operation (*) on matrices with incorrect sizes!")

        return type

    def visit_ForNode(self, node):
        self.current_scope = self.current_scope.pushScope("for")
        
        var = VariableSymbol(node.ID, "int", None, [])
        self.current_scope.put(node.ID, var)

        self.visit(node.start)
        self.visit(node.end)
        self.visit(node.body)

        self.current_scope = self.current_scope.popScope()

    def visit_PrintNode(self, node):
        self.visit(node.value)

    def visit_PrintRekNode(self, node):
        for value in node.values:
            self.visit(value)

    def visit_WhileNode(self, node):
        self.current_scope = self.current_scope.pushScope("while")

        self.visit(node.condition)
        self.visit(node.body)

        self.current_scope = self.current_scope.popScope()

    def visit_IfElseNode(self, node):
        self.current_scope = self.current_scope.pushScope("if")

        self.visit(node.condition)
        self.visit(node.if_body)

        self.current_scope = self.current_scope.parent
        if (node.else_body == None):
            return

        self.current_scope = self.current_scope.popScope()

        self.visit(node.else_body)

        self.current_scope = self.current_scope.parent

    def visit_BreakStatement(self, node):
        # IN LOOP CHECK
        scope = self.current_scope
        while (scope.name != "program"):
            if (scope.name == "for" or scope.name == "while"):
                return
            scope = scope.parent
        self.new_error(node.lineno, "Incorrect break statement use!")

    def visit_ContinueStatement(self, node):
        if (not (self.current_scope.name == "for" or
           self.current_scope.name == "while")):
            self.new_error(node.lineno, "Incorrect continue statement use!")

    def visit_ReturnStatement(self, node):
        pass

    # ------------------------------------

    def print_errors(self):
        for error in self.errors:
            print(error)

    def print_symbols(self, scope):
        if (scope.parent != None):
            self.print_symbols(self, scope.parent)
        for name, symbol in scope.symbols.items():
            if (symbol.type == "matrix"):
                print(
                    f"{scope.name.upper()} -> name: {name}, type: {symbol.type}, size: {symbol.size}, rows: {symbol.row_sizes}")
            else:
                print(f"{scope.name.upper()} -> name: {name}, type: {symbol.type}")

    def evaluate_constant_expression(self, node):
        """Prosta metoda do obliczania wartości wyrażeń stałych."""
        if isinstance(node, AST.IntNum):
            return node.value
        elif isinstance(node, AST.BinExpr):
            left = self.evaluate_constant_expression(node.left)
            right = self.evaluate_constant_expression(node.right)
            if left is not None and right is not None:
                if node.op == "+":
                    return left + right
                elif node.op == "-":
                    return left - right
                elif node.op == "*":
                    return left * right
                elif node.op == "/":
                    return left // right if right != 0 else None
        return None