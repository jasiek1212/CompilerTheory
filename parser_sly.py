from sly import Parser
from scanner_sly import Scanner  # zakładamy, że masz już gotowy skaner

class Mparser(Parser):
    tokens = Scanner.tokens

    # Plik do zapisu wyników debugowania
    debugfile = 'parser.out'

    # Precedencja operatorów (od najniższego do najwyższego priorytetu)
    precedence = (
        ("left", 'PLUS', 'MINUS'),
        ("left", 'TIMES', 'DIVIDE'),
        ("left", 'DOTADD', 'DOTSUB'),
        ("left", 'DOTMUL', 'DOTDIV'),
        ("right", 'NEGATE'),
        ("right", 'TRANSPOSE'),
    )

    # Program składa się z opcjonalnej listy instrukcji
    @_('instructions_opt')
    def program(self, p):
        pass  # Pusta produkcja

    # Opcjonalne instrukcje (pusta lista lub lista instrukcji)
    @_('instructions')
    def instructions_opt(self, p):
        pass  # Pusta produkcja

    @_('instruction')
    def instructions(self, p):
        pass  # Pusta produkcja

    # Lista instrukcji
    @_('instructions instruction')
    def instructions(self, p):
        pass  # Pusta produkcja


    # Instrukcja może być przypisaniem, wyrażeniem, pętlą, itp.
    @_('assignment',
       'expression SEMICOLON',
       'if_statement',
       'for_loop',
       'while_loop',
       'break_stmt',
       'continue_stmt',
       'return_stmt',
       'print_stmt',
       'block')
    def instruction(self, p):
        pass  # Pusta produkcja

    # Instrukcja przypisania
    @_('ID ASSIGN expression SEMICOLON',
       'ID ADDASSIGN expression SEMICOLON',
       'ID SUBASSIGN expression SEMICOLON',
       'ID MULASSIGN expression SEMICOLON',
       'ID DIVASSIGN expression SEMICOLON')
    def assignment(self, p):
        pass  # Pusta produkcja

    # Wyrażenie binarne
    @_('expression PLUS expression',
       'expression MINUS expression',
       'expression TIMES expression',
       'expression DIVIDE expression',
       'expression DOTADD expression',
       'expression DOTSUB expression',
       'expression DOTMUL expression',
       'expression DOTDIV expression')
    def expression_binop(self, p):
        pass  # Pusta produkcja

    # Wyrażenie relacyjne
    @_('expression GT expression',
       'expression LT expression',
       'expression GE expression',
       'expression LE expression',
       'expression EQ expression',
       'expression NEQ expression')
    def expression_relational(self, p):
        pass  # Pusta produkcja

    # Negacja unarna
    @_('MINUS expression %prec NEGATE')
    def expression_negate(self, p):
        pass  # Pusta produkcja

    # Transpozycja macierzy
    @_('expression TRANSPOSE %prec TRANSPOSE')
    def expression_transpose(self, p):
        pass  # Pusta produkcja

    # Specjalne funkcje macierzowe
    @_('ZEROS LPAREN expression RPAREN',
       'ONES LPAREN expression RPAREN',
       'EYE LPAREN expression RPAREN')
    def matrix_function(self, p):
        pass  # Pusta produkcja

    # Warunek if-else
    @_('IF LPAREN expression RPAREN instruction ELSE instruction',
       'IF LPAREN expression RPAREN instruction')
    def if_statement(self, p):
        pass  # Pusta produkcja

    # Pętla for
    @_('FOR ID EQ expression RANGE expression instruction')
    def for_loop(self, p):
        pass  # Pusta produkcja

    # Pętla while
    @_('WHILE LPAREN expression RPAREN instruction')
    def while_loop(self, p):
        pass  # Pusta produkcja

    # Instrukcja break
    @_('BREAK SEMICOLON')
    def break_stmt(self, p):
        pass  # Pusta produkcja

    # Instrukcja continue
    @_('CONTINUE SEMICOLON')
    def continue_stmt(self, p):
        pass  # Pusta produkcja

    # Instrukcja return
    @_('RETURN expression SEMICOLON')
    def return_stmt(self, p):
        pass  # Pusta produkcja

    # Instrukcja print
    @_('PRINT expression SEMICOLON')
    def print_stmt(self, p):
        pass  # Pusta produkcja

    # Blok instrukcji
    @_('"{" instructions_opt "}"')
    def block(self, p):
        pass  # Pusta produkcja

    # Wyrażenia – liczby, zmienne, wyrażenia w nawiasach
    @_('NUMBER',
       'ID',
       'LPAREN expression RPAREN')
    def expression(self, p):
        pass  # Pusta produkcja

    @_('INTNUM',
       'FLOATNUM')
    def NUMBER(self, p):
        pass

    # Obsługa błędów
    def error(self, p):
        if p:
            print(f"Syntax error at token {p.type}, value {p.value}")
        else:
            print("Syntax error at EOF")

