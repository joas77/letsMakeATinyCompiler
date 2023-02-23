import enum

class Lexer:
    def __init__(self, input):
        # source code to lex as a string. Append a newline to
        # simplify lexing/parsing the last token/statement.
        self.source = input + '\n'
        self.current_char = ''
        self.current_pos = -1
        self.next_char()

    def next_char(self):
        self.current_pos += 1
        if self.current_pos >= len(self.source):
            self.current_char = '\0' # EOF
        else:
            self.current_char = self.source[self.current_pos]

    def peek(self):
        ''' Return the lookahead character'''
        if self.current_pos + 1 >= len(self.source):
            return '\0'
        return self.source[self.current_pos + 1]

    def get_token(self):
        '''
        Return the next token
        Check the first character of this token to see if we can
        decide what it is.
        If it's a multiple character operator (e.g., !=), number, identifier
        or keyword we will process the rest.
        '''
        token = None
        if self.current_char == '+':
            token = Token(self.current_char, TokenType.PLUS)
        elif self.current_char == '-':
            token = Token(self.current_char, TokenType.MINUS)
        elif self.current_char == '*':
            token = Token(self.current_char, TokenType.ASTERISK)
        elif self.current_char == '/':
            token = Token(self.current_char, TokenType.SLASH)
        elif self.current_char =='\n':
            token = Token(self.current_char, TokenType.NEWLINE)
        elif self.current_char == '\0':
            token = Token(self.current_char, TokenType.EOF)
        else:
            # Unknown token!
            pass

        self.next_char()

class Token:
    ''' Token contains the original text and the type of the token'''
    def __init__(self, token_text, token_kind):
        self.text = token_text
        self.kind = token_kind

class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    IDENT = 2
    STRING = 2
    # keywords
    LABEL = 101
    GOTO
    PRINT
    INPUT
    LET
    IF
    THEN
    ENDIF
    WHILE
    REPEAT
    ENDWHILE
    # Operators
    EQ = 201
    PLUS
    MINUS
    ASTERISK
    SLASH
    EQEQ
    NOTEQ
    LT
    LTEQ
    GT
    GTEQ
