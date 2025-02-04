

# Custom Interpreter

## Project description

The project is a tool for source code analysis in a given language, built with the use of `sly` tool. The aim of the project is to create a Scanner, Parser, TypeChecker and Interpreter that can be all combined to analyse given source code. The project constists of the following components:
- **Scanner** (`scanner_sly.py`): tokenizes the source code
- **Parser** (`parser_sly.py`): syntax analysis and Abstract Syntax Tree creation
- **TypeChecker** (`TypeChecker.py`): checks for type correctness

## Requirements

Do uruchomienia projektu wymagane są następujące zależności:

- **Python 3.x**
- **sly**: a tool used for creating lexical and syntax analizers 

## Installation

To install dependencies and run the project, do the following:

1. **Install `sly`**

   It is suggested to dowload it using `pip` (preferably in an virtual environment):

   ```bash
   pip install sly
   ```

2. **Download and clone the project**

   ```bash
   git clone https://github.com/jasiek1212/CompilerTheory.git
   cd CompilerTheory
   ```

3. **Run the project**

   ```bash
   python main.py [filename]
   ```

   where:
   - `[filenmame]` is an optional argument, which specifies the name of the file containing the source code. If it is not supplied, the default will be `example.txt`. This default filename can be changed in `main.py`.

## Project structure

1. **main.py**

    Main file performing the whole analysis. It first reads the source file, tokenizes it, performs syntax analysis and type checking.

2. **parser_sly.py**

    File containing the parser definition. Relies on `sly`.

3. **scanner_sly.py**

    File containing the scanner definition. Relies on `sly` as well.

4. **TreePrinter.py**

    Helper file, containing functionality related to AST printing in the terminal, used for debugging.

5. **TypeChecker.py**

    File containing functionality related to type checking, for example disabling the possibility of performing operations on unsupported types, or preventing out of bounds indexing.

6. **SymbolTable.py**
    File containing variable and scope functionality, helper file for TypeChecker.

7. **AST.py**
    File containing the definition and functionality of the Abstract Syntax Tree.

8. **examples**
    A few .txt files have been suppplied to quickly test the functionality of the program. The first 3 are incorrect programs (accorting to the given laguage), and the rest is correct.


## Usage

1. **Default run**:

    To run the program on the default file, run:

   ```bash
   python main.py
   ```

2. **Selecting different files**:

    To analyse different files, like example2.txt, run:

   ```bash
   python main.py nazwa_pliku.txt
   ```

3. **Result**:

    If all types are correct and all rules met, the program will end by only printing:

    `Parser debuggin for Mparser written to parser.out`

    This is a file for debugging.

    If something goes wrong, an error will be shown along with the line in whcih it was written in:

    `Error at line 3: Unknown type in assignment!`


