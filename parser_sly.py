from sly import Parser
from scanner_sly import Scanner 

class Mparser(Parser):
    tokens = Scanner.tokens
    literals = Scanner.literals
    keywords = Scanner.keywords

    debugfile = 'parser.out'

    precedence = (
        ('nonassoc', 'JUST_IF'),
        ('nonassoc', 'ELSE'),
        ('nonassoc', 'ELSE_IF'),
        ('nonassoc', 'ASSIGN',  'SUBASSIGN', 'ADDASSIGN', 'MULASSIGN', 'DIVASSIGN'),
        ('left', 'EQ', 'NEQ', 'GT', 'GE', 'LT', 'LE'),
        ("left", 'PLUS', 'MINUS'),
        ("left", 'TIMES', 'DIVIDE'),
        ("left", 'DOTADD', 'DOTSUB'),
        ("left", 'DOTMUL', 'DOTDIV'),
        ("right", 'NEGATE'),
        ("right", 'TRANSPOSE'),
    )

    @_('instructions')
    def program(self, p):
        pass


    @_('instruction',
       'instructions instruction')
    def instructions(self, p):
        pass  


    @_('end_line_instruction ";"',
       'non_end_instruction',
       '"{" instructions "}"')
    def instruction(self, p):
        pass  

    @_('assignment',
       'break_stmt',
       'continue_stmt',
       'return_stmt',
       'print_stmt',
       )
    def end_line_instruction(self, p):
        pass

    @_('if_statement',
       'for_loop',
       'while_loop'
       )
    def non_end_instruction(self, p):
        pass

    @_('ID ASSIGN expression',
       'ID ADDASSIGN expression',
       'ID SUBASSIGN expression',
       'ID MULASSIGN expression',
       'ID DIVASSIGN expression')
    def assignment(self, p):
        pass  

    # Wyrażenie binarne
    @_('expression PLUS term',
       'expression MINUS term',
       'expression DOTADD term',
       'expression DOTSUB term',
       'term',
        )
    def expression_op(self, p):
        pass  

    @_('term TIMES factor',
       'term DIVIDE factor',
       'term DOTMUL factor',
       'term DOTDIV factor',
       'factor'
        )
    def term(self, p):
        pass

    @_('NUMBER',
       'ID',
       'STRING',
       '"(" expression ")"',
       '"[" value_list "]"',
       'matrix_function',
       'expression_transpose TRANSPOSE'
       )
    def factor(self, p):
        pass

    # Wyrażenie relacyjne
    @_('expression GT expression',
       'expression LT expression',
       'expression GE expression',
       'expression LE expression',
       'expression EQ expression',
       'expression NEQ expression')
    def expression_relational(self, p):
        pass  

    # Negacja unarna
    @_('expression %prec NEGATE')
    def expression_negate(self, p):
        pass  

    # Transpozycja macierzy
    @_('factor %prec TRANSPOSE')
    def expression_transpose(self, p):
        pass  

    # Specjalne funkcje macierzowe
    @_('ZEROS "(" expression ")"',
       'ONES "(" expression ")"',
       'EYE "(" expression ")"')
    def matrix_function(self, p):
        pass  


    @_('MINUS expression_negate',
       'expression_op',
       'expression_relational'
    #    'expression_transpose TRANSPOSE'
       )
    def expression(self, p):
        pass  
    
    @_('value_list "," expression',
       'expression')
    def value_list(self, p):
        pass

    @_('IF "(" expression ")" instructions else_if_chain %prec JUST_IF')
    def if_statement(self, p):
        pass

    # Handles else-if chains and else clause
    @_('ELSE_IF "(" expression ")" instructions else_if_chain',
    'ELSE instructions',
    '')
    def else_if_chain(self, p):
        pass


    @_('FOR ID ASSIGN expression RANGE expression instructions')
    def for_loop(self, p):
        pass  

    @_('WHILE "(" expression ")" instructions')
    def while_loop(self, p):
        pass  

    @_('BREAK')
    def break_stmt(self, p):
        pass  

    @_('CONTINUE')
    def continue_stmt(self, p):
        pass  

    @_('RETURN expression')
    def return_stmt(self, p):
        pass  

    @_('PRINT value_list')
    def print_stmt(self, p):
        pass  

    @_('INTNUM',
       'FLOATNUM')
    def NUMBER(self, p):
        pass

    def error(self, p):
        if p:
            print(f"Syntax error at token {p.type}, value {p.value}")
        else:
            print("Syntax error at EOF")

