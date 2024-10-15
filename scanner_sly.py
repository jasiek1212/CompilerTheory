import sys
from sly import Lexer

class Scanner(Lexer):
    
    keywords = {
        'if': 'IF',
        'else': 'ELSE',
        'for': 'FOR',
        'while': 'WHILE',
        'break': 'BREAK',
        'continue': 'CONTINUE',
        'return': 'RETURN',
        'eye': 'EYE',
        'zeros': 'ZEROS',
        'ones': 'ONES',
        'print': 'PRINT'
    }
    
    tokens = [ 'ID', 'EQ', 'NEQ', 'LE', 'GE', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'DOTADD', 'DOTSUB', 
               'DOTMUL', 'DOTDIV', 'ASSIGN', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN', 
               'LT', 'GT', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'RANGE', 
               'TRANSPOSE', 'COMMA', 'SEMICOLON', 'INTNUM', 'FLOATNUM', 'STRING' ] + list(keywords.values())

    ignore = ' \t'
    ignore_comment = r'\#.*'
    
    PLUS        = r'\+'
    MINUS       = r'-'
    TIMES       = r'\*'
    DIVIDE      = r'/'
    
    DOTADD      = r'\.\+'
    DOTSUB      = r'\.-'
    DOTMUL      = r'\.\*'
    DOTDIV      = r'\./'
    
    ASSIGN      = r'='
    ADDASSIGN   = r'\+='
    SUBASSIGN   = r'-='
    MULASSIGN   = r'\*='
    DIVASSIGN   = r'/='
    
    LT          = r'<'
    GT          = r'>'
    LE          = r'<='
    GE          = r'>='
    NEQ         = r'!='
    EQ          = r'=='

    LPAREN      = r'\('
    RPAREN      = r'\)'
    LBRACKET    = r'\['
    RBRACKET    = r'\]'
    LBRACE      = r'\{'
    RBRACE      = r'\}'
    
    RANGE       = r':'
    TRANSPOSE   = r"'"
    COMMA       = r','
    SEMICOLON   = r';'

    
    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
        t.type = self.keywords.get(t.value, 'ID')
        return t

    @_(r'\d*\.\d+(E-?\d+)?')
    def FLOATNUM(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INTNUM(self, t):
        t.value = int(t.value)
        return t

    @_(r'\".*?\"')
    def STRING(self, t):
        t.value = t.value[1:-1]
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()
    
    for tok in lexer.tokenize(text):
        print(f"({tok.lineno}): {tok.type}({tok.value})")
