from lex import *
import sys

class Parser:
    '''
    Parser object keeps track of current token and checks if
    the code matches the grammar.
    '''
    def __init__(self, lexer : Lexer) -> None:
        self.lexer = lexer
        self.current_token : Token = None
        self.peek_token : Token = None
        # call this twice to initialize current and peek
        self.next_token()
        self.next_token()

    def next_token(self):
        ''' Advances the current token. '''
        self.current_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def check_token(self, kind) -> bool:
        '''Return true if the current token matches.'''
        return kind == self.current_token.kind

    def check_peek(self, kind) -> bool:
        '''Return true if the next token matches.'''
        return kind == self.peek_token.kind

    def match(self, kind):
        '''Try to match token. If not, error. Advances the current token.'''
        if not self.check_token(kind):
            self.abort(f'Expected {kind.name}, got {self.current_token.kind}')
        self.next_token()

    def abort(self, message : str):
        sys.exit(f'Error. {message}')

    # Production rules

    def program(self):
        '''program ::= {statement}'''
        print('PROGRAM')

        # Since some newlines are requiered in our grammar,
        # need to skip the excess.
        while self.check_token(TokenType.NEWLINE):
            self.next_token()

        # Parse all the statements in the program.
        while not self.check_token(TokenType.EOF):
            self.statement()

    # One of the following statements...
    def statement(self):
        '''
        statement ::= "PRINT" (expression | string) nl
                    | "IF"  comparision "THEN" nl {statement} "ENDIF" nl
                    | "WHILE" comparision "REPEAT" nl {statement} "ENDWHILE nl
                    | "LABEL" ident nl
                    | "GOTO" ident "=" expression nl
                    | "INPUT" ident nl
        Check the first token to see what kind of statement this is.
        '''

        # 'PRINT' (expression | string)
        if self.check_token(TokenType.PRINT):
            print('STATEMENT-PRINT')
            self.next_token()

            if self.check_token(TokenType.STRING):
                # Simple string.
                self.next_token()
            else:
                # Expect an expression
                self.expression()
        elif self.check_token(TokenType.IF):
            print('STATEMENT-IF')
            self.next_token()
            self.comparision()

            self.match(TokenType.THEN)
            self.nl()

            # zero or more statements in the body.
            while not self.check_token(TokenType.ENDIF):
                self.statement()

            self.match(TokenType.ENDIF)
        elif self.check_token(TokenType.WHILE):
            print('STATEMENT-WHILE')
            self.next_token()
            self.comparision()

            self.match(TokenType.REPEAT)
            self.nl()

            # zero or more statements in the loop body
            while not self.check_token(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)

        # "LABEL" ident
        elif self.check_token(TokenType.LABEL):
            print('STATEMENT-LABEL')
            self.next_token()
            self.match(TokenType.IDENT)

        # "GOTO" ident
        elif self.check_token(TokenType.GOTO):
            print('STATEMENT-GOTO')
            self.next_token()
            self.match(TokenType.IDENT)

        # "LET" ident "=" expression
        elif self.check_token(TokenType.GOTO):
            print('STATEMENT-LET')
            self.next_token()
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()

        # "INPUT" ident
        elif self.check_token(TokenType.INPUT):
            print('STATEMENT-INPUT')
            self.next_token()
            self.match(TokenType.IDENT)

        # This is not a valid statement. Error!
        else:
            self.abort(f'Invalid statement at {self.current_token.text} ({self.current_token.kind.name})')

        # Newline
        self.nl()

    def nl(self):
        '''nl::= '\n'+'''
        print('NEWLINE')

        # Require at leat one newline.
        self.match(TokenType.NEWLINE)
        # But we allow extra newlines too, of course.
        while self.check_token(TokenType.NEWLINE):
            self.next_token()

    def expression(self):
        pass

    def comparision(self):
        pass
