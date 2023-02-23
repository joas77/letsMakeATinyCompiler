from lex import *

def main():
    input = "LET foobar = 123"
    lexer = Lexer(input)

    while lexer.peek() != '\0':
        print(lexer.current_char)
        lexer.next_char()

if __name__ == '__main__':
    main()