import argparse
from parser import Parser
from lex import Lexer

# from parse import *

def main():
    '''main function'''
    NAME = 'Teeny Tiny Compiler'
    parser = argparse.ArgumentParser(
        prog=NAME,
        description='small compiler of toy language'
    )

    parser.add_argument('inputfile')
    args = parser.parse_args()
    print(NAME)

    with open(args.inputfile, 'r') as infile:
        source = infile.read()

    # initialize the lexer and parser
    lexer = Lexer(source)
    parser = Parser(lexer)
    parser.program()
    print('Parsing completed.')

if __name__ == '__main__':
    main()
