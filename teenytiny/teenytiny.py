from lex import *

def main():
    source = '''+- "this is a string"# This is a comment\n*/>>==!=
    123 9.81 */
    IF foo THEN
    '''
    lexer = Lexer(source)

    token = lexer.get_token()
    while token.kind != TokenType.EOF:
        print(token.kind)
        token = lexer.get_token()

if __name__ == '__main__':
    main()
