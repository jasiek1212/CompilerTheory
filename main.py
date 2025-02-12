
import sys
from parser_sly import Mparser
from scanner_sly import Scanner
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example4.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser()
    lexer = Scanner()
    text = file.read()
    ast = parser.parse(lexer.tokenize(text))
    typeChecker = TypeChecker()
    #uncomment the following lines to print the AST:
    #ast.printTree()

    typeChecker.visit(ast)
    if typeChecker.errors:
        print("- TYPE CHECKER ERROR -")
        typeChecker.print_errors()
