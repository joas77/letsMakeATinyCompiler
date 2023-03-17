import enum
import sys

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
        self.skip_whitespace()
        if self.current_char == '+':
            token = Token(self.current_char, TokenType.PLUS)
        elif self.current_char == '-':
            token = Token(self.current_char, TokenType.MINUS)
        elif self.current_char == '*':
            token = Token(self.current_char, TokenType.ASTERISK)
        elif self.current_char == '/':
            token = Token(self.current_char, TokenType.SLASH)
        elif self.current_char == '=':
            # check whether this token is = or ==
            if self.peek() == '=':
                last_char = self.current_char
                self.next_char()
                token = Token(last_char + self.current_char, TokenType.EQEQ)
            else:
                token = Token(self.current_char, TokenType.EQ)
        elif self.current_char =='\n':
            token = Token(self.current_char, TokenType.NEWLINE)
        elif self.current_char == '\0':
            token = Token(self.current_char, TokenType.EOF)
        else:
            # Unknown token!
            self.abort("Unknown token: " + self.current_char)

        self.next_char()
        return token

    def abort(self, message):
        ''' Invalid token found, print error message and exit '''
        sys.exit("Lexing error. " + message)

    def skip_whitespace(self):
        '''
        skip whitespace except newlines,
        which we will use to indicate the end of a stament.
        '''
        while self.current_char == ' ' or self.current_char == '\t' or self.current_char == '\r':
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
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # Operators
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
