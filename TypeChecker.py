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
ttype["+"]["matrix"]["matrix"] = "matrix"

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
        for instruction in node.instructions:
                self.visit(instruction)

    def visit_AssignExpression(self, node):
        var_type = None
        size = None

        type = self.visit(node.right)

        if isinstance(node.left, AST.MatrixRefNode):
            return

        var_name = node.left.name
        var_type = type

        if type == 'matrix':
            node.left.size = node.right.size
            size = node.right.size            


        if var_type is None:
            self.new_error(node.lineno, "Unknown type in assignment!")
            return

        var = VariableSymbol(var_name, var_type, size)

        self.current_scope.put(var_name, var)

    def visit_Bin_RelExprNode(self, node):
        if node.op in [Sc.EQ, Sc.GE, Sc.LT, Sc.LE, Sc.GT, Sc.NEQ]:
            self.visit(node.left)
            self.visit(node.right)
            return "int"
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        type = ttype[op][type1][type2]

        if type == "":
            self.new_error(node.lineno, f"Unsuppported operation: {op} on types: {type1} and {type2}!")

        if (type != "" and type1 == "matrix" and type2 == "matrix"):
            m1, m2 = node.left, node.right
            if isinstance(node.left, AST.IDNode):
                m1 = self.current_scope.get(node.left.name)
            if isinstance(node.right, AST.IDNode):
                m2 = self.current_scope.get(node.right.name)
            if m1.size != m2.size and (op == ".+" or op == ".-" or op == ".*" or op =="./" or op=="+"):
                self.new_error(
                    node.lineno, "Operations (.+|.-|.*|./) on matrices with unequal sizes!")
            if (len(m1.size) > 2 or len(m2.size) > 2 or m1.size[1] != m2.size[0]) and (op == "*"):
               self.new_error(
                    node.lineno, "Operations (*) on matrices with unequal sizes!")
            node.size = m1.size
        return type
    
    def visit_MatrixFuncNode(self, node):
        expr_type = self.visit(node.expr)

        if expr_type not in ["int", "float"]:
            self.new_error(node.lineno, f"Invalid argument type for {node.func}: {expr_type}")
            return None

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

    def visit_IDRefNode(self, node):
        var = self.current_scope.get(node.value)
        if (var == None):
            self.new_error(
                node.lineno, "Variable does not exist in this scope!")

    def visit_ExpressionNode(self, node):
        return self.visit(node.expr)

    def visit_ValueListNode(self, node):
        same_rows_size = True
        matrix_size = None
        is_3d = False
        for value in node.values:
            if isinstance(value, AST.MatrixFuncNode):
                is_3d = True
                size = value.size
                
                rows = size[0]
                cols = size[1]

                if matrix_size is None:
                    matrix_size = (rows, cols)
                elif matrix_size != (rows, cols):
                    same_rows_size = False
                    break
            elif isinstance(value, AST.ValueListNode):
                rows = len(value.values)
                cols = len(value.values[0].values) if isinstance(value.values, AST.ValueListNode) else 1 # Zakładając, że pierwsza 'wiersz' nie jest pusty
                if cols > 1: 
                    is_3d = True
                if matrix_size is None:
                    matrix_size = (rows, cols)
                elif matrix_size != (rows, cols):
                    same_rows_size = False
                    break
            else:
                if matrix_size is None:
                    matrix_size = 0
                elif matrix_size != 0:
                    same_rows_size = False
                    break

        if not same_rows_size:
            self.new_error(node.lineno, f"Matrix dimensions mismatch in value list at line {node.lineno}")
            return None
        if is_3d:
            node.size = (len(node.values), matrix_size[0], matrix_size[1])
        else:
            node.size = (len(node.values), rows) if matrix_size else (1, len(node.values))
        print(node.size)
        return 'matrix'
        

    def visit_StringOfNumNode(self, node):
        pass

    def visit_MatrixRefNode(self, node):
        self.visit(node.slices)
        if len(node.slices.ints) > 2:
            self.new_error(node.lineno, "Matrix reference of 3-or more- dimensional matrices is unsupported!")

        matrix = self.current_scope.get(node.ID.name)
        if not matrix:
            self.new_error(node.lineno, "Unknown variable!")
            return

        if matrix.type != "matrix":
            self.new_error(node.lineno, "Variable type error!")
            return

        args = node.slices.ints
        if (len(args) == 1):
            if args[0].value >= matrix.size[0]:
                self.new_error(node.lineno, "Out of array scope!")
        elif len(args) == 2:
            if args[0].value >= matrix.size[0]:
                self.new_error(node.lineno, "Out of array scope!")
            elif args[1].value >= matrix.size[1]:
                self.new_error(node.lineno, "Out of array scope!")
        node.size = node.slices.ints
        print(node.size[0].value, node.size[1].value)
        return 'matrix'

    def visit_IntNum(self, node):
        return "int"

    def visit_FloatNum(self, node):
        return "float"

    def visit_NegateExprNode(self, node):
        type = self.visit(node.expr)
        if type == 'matrix':
            node.size = node.expr.size
        return type
            

    def visit_IDNode(self, node):
        var = self.current_scope.get(node.name)
        if (var == None):
            self.new_error(node.lineno, "Unknown variable!")
        if var.type == 'matrix':
            node.size = var.size
        return var.type

    def visit_TransposeNode(self, node):
        type = self.visit(node.factor)
        if type != 'matrix':
            self.new_error(node.lineno, "Transposition of not a matrix!")
        if len(node.factor.size) > 2:
            self.new_error(node.lineno, "Cannot transpose matrix of more dimensions than 2!")
        node.size = node.factor.size[1], node.factor.size[0]
        return 'matrix'


    def visit_ForNode(self, node):
        self.current_scope = self.current_scope.pushScope("for")
        
        var = VariableSymbol(node.ID, "int", None, [])
        self.current_scope.put(node.ID.name, var)

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

        if node.else_body is None:
            return

        self.current_scope = self.current_scope.pushScope("else")
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
        reached_scope = self.current_scope
        while reached_scope is not None:
            if (reached_scope.name == "for" or reached_scope.name == "while"):
                return
            reached_scope = reached_scope.parent
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
        if isinstance(node, AST.IntNum):
            return node.value
        elif isinstance(node, AST.Bin_RelExprNode):
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