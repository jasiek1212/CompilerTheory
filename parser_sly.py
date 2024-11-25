from sly import Parser
from scanner_sly import Scanner
import AST
from TreePrinter import *


class Mparser(Parser):
    tokens = Scanner.tokens
    # literals = Scanner.literals
    # keywords = Scanner.keywords

    debugfile = 'parser.out'

    precedence = (
        ('nonassoc', 'JUST_IF'),
        ('nonassoc', 'ELSE'),
        ('left', 'EQ', 'NEQ', 'GT', 'GE', 'LT', 'LE'),
        ("left", 'PLUS', 'MINUS'),
        ("left", 'DOTADD', 'DOTSUB'),
        ("left", 'TIMES', 'DIVIDE'),
        ("left", 'DOTMUL', 'DOTDIV'),
        ("right", 'NEGATE'),
        ("right", 'TRANSPOSE'),
    )

    @_('instructions')
    def program(self, p):
        return p[0]

    @_('instruction',
       'instructions instruction')
    def instructions(self, p):

        if len(p) == 1:
            return AST.InstructionsNode([p[0]], lineno=p.lineno)

        instructions = p[0].instructions.copy()
        instructions.append(p[1])

        return AST.InstructionsNode(instructions, lineno=p.lineno)

    @_('end_line_instruction',
       'non_end_instruction',
       '"{" instructions "}"')
    def instruction(self, p):
        if len(p) == 1:
            return p[0]
        return p[1]

    @_('";"',
       'assignment',
       'BREAK ";"',
       'CONTINUE ";"',
       'print_stmt',
       'RETURN expression ";"'
       )
    def end_line_instruction(self, p):
        try:
            if p.BREAK:
                return AST.BreakStatement(lineno=p.lineno)
        except:
            pass
        try:
            if p.CONTINUE:
                return AST.ContinueStatement(lineno=p.lineno)
        except:
            pass
        try:
            if p.RETURN:
                return AST.ReturnStatement(p[1], lineno=p.lineno)
        except:
            pass

        if p[0] == ";":
            return AST.BlankStatement(lineno=p.lineno)
        return p[0]

    @_('if_statement',
       'for_loop',
       'while_loop'
       )
    def non_end_instruction(self, p):
        return p[0]

    @_('ID ASSIGN expression ";"',
       'ID ADDASSIGN expression ";"',
       'ID SUBASSIGN expression ";"',
       'ID MULASSIGN expression ";"',
       'ID DIVASSIGN expression ";"')
    def assignment(self, p):
        myID = AST.IDNode(p[0], lineno=p.lineno)
        return AST.AssignExpression(myID, p[1], p[2], lineno=p.lineno)

    @_('NUMBER',
       'ID',
       'STRING',
       '"(" expression ")"',
       '"[" value_list "]"',
       'matrix_function',
       'expression_transpose TRANSPOSE'
       )
    def factor(self, p):
        try:
            if p.ID:
                return AST.IDNode(p[0], lineno=p.lineno)
        except:
            pass
        try:
            if p.STRING:
                return AST.StringNode(p[0], lineno=p.lineno)
        except:
            pass
        if len(p) == 1 or len(p) == 2:
            return p[0]
        return p[1]

    @_('expression PLUS expression',
       'expression MINUS expression',
       'expression DOTADD expression',
       'expression DOTSUB expression',
       'expression TIMES expression',
       'expression DIVIDE expression',
       'expression DOTMUL expression',
       'expression DOTDIV expression',
       'expression GT expression',
       'expression LT expression',
       'expression GE expression',
       'expression LE expression',
       'expression EQ expression',
       'expression NEQ expression'
       )
    def expression_bin(self, p):
        return AST.Bin_RelExprNode(p[1], p[0], p[2], lineno=p.lineno)

    @_('expression %prec NEGATE')
    def expression_negate(self, p):
        return AST.NegateExprNode(p[0], lineno=p.lineno)

    @_('factor %prec TRANSPOSE')
    def expression_transpose(self, p):
        return AST.TransposeNode(p[0], lineno=p.lineno)

    @_('ZEROS "(" expression ")"',
       'ONES "(" expression ")"',
       'EYE "(" expression ")"')
    def matrix_function(self, p):
        func_name = p[0]
        arg = p[2]
        return AST.MatrixFuncNode(func_name, arg, lineno=p.lineno)

    @_('MINUS expression_negate',
       'expression_bin',
       'factor'
       )
    def expression(self, p):
        if (len(p) == 2):
            return -p[1]
        return p[0]

    @_('value_list "," expression',
       'expression')
    def value_list(self, p):

        if len(p) == 1:
            values = [p[0]]
        else:
            values = p[0].values.copy()
            values.append(p[2])

        return AST.ValueListNode(values, lineno=p.lineno)

    @_('IF "(" expression ")" instruction %prec JUST_IF',
       'IF "(" expression ")" instruction ELSE instruction')
    def if_statement(self, p):

        condition = p[2]
        if_body = p[4]
        has_else = len(p) == 7
        else_body = p[6] if has_else else None

        return AST.IfElseNode(condition, if_body, has_else, else_body, lineno=p.lineno)

    @_('FOR ID ASSIGN expression RANGE expression instruction')
    def for_loop(self, p):
        myID = AST.IDNode(p[1], lineno=p.lineno)
        start = p[3]
        end = p[5]
        body = p[6]

        return AST.ForNode(myID, start, end, body, lineno=p.lineno)

    @_('WHILE "(" expression ")" instruction')
    def while_loop(self, p):
        return AST.WhileNode(p[2], p[4], lineno=p.lineno)

    @_('PRINT value_list ";"')
    def print_stmt(self, p):
        return AST.PrintNode(p[1], lineno=p.lineno)

    @_('INTNUM',
       'FLOATNUM')
    def NUMBER(self, p):
        if isinstance(p[0], float):
            return AST.FloatNum(p[0], lineno=p.lineno)
        return AST.IntNum(p[0], lineno=p.lineno)

    def error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}: Unexpected token '{p.value}' of type '{p.type}'")
        else:
            print("Syntax error at EOF: Unexpected end of input")