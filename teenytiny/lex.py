import enum
import sys

class Lexer:
    def __init__(self, input_source):
        # source code to lex as a string. Append a newline to
        # simplify lexing/parsing the last token/statement.
        self.source = input_source + '\n'
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
        self.skip_whitespace()
        self.skip_comment()
        token = None

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
            token = self.get_doublechar_token('=', TokenType.EQEQ, TokenType.EQ)
        elif self.current_char == '>':
            # check whether this token is > or >=
            token = self.get_doublechar_token('=', TokenType.GTEQ, TokenType.GT)
        elif self.current_char == '<':
            # check whether this token is < or <=
            token = self.get_doublechar_token('=', TokenType.LTEQ, TokenType.LT)
        elif self.current_char == '!':
            if self.peek() == '=':
                last_char = self.current_char
                self.next_char()
                token = Token(last_char + self.current_char, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
        elif self.current_char == '"':
            # Get characteres between quotations.
            self.next_char()
            start_pos = self.current_pos
            while self.current_char != '"':
                # Don't allow special characters in the string.
                # We will be using C's printf on this string.
                if self.current_char == '\r' or self.current_char == '\n' or\
                    self.current_char == '\t' or self.current_char == '\\' or self.current_char == '%':
                    self.abort('Illegal character in string.')
                self.next_char()

            token_text = self.source[start_pos: self.current_pos] # Get substring.
            token = Token(token_text, TokenType.STRING)
        elif self.current_char.isdigit():
            # Leading char is a digit, so this must be a numebr.
            # Get all consecutive digits and decimal id there is one.
            start_pos = self.current_pos
            self.pick_digits()
            if self.peek() == '.': # Decimal!
                self.next_char()

                # Must have at leat one digit after decimal.
                if not self.peek().isdigit():
                    # Error!
                    self.abort('Illegak character in number.')
                self.pick_digits()

            token_text = self.source[start_pos: self.current_pos + 1] # Get the substring.
            token = Token(token_text, TokenType.NUMBER)

        elif self.current_char =='\n':
            token = Token(self.current_char, TokenType.NEWLINE)
        elif self.current_char == '\0':
            token = Token(self.current_char, TokenType.EOF)
        elif self.current_char.isalpha():
            # Leading character is a letter, so this must be and identifier or a keyword.
            # Get all consecutive alpha numeric chatacters.
            start_pos = self.current_pos
            while self.peek().isalnum():
                self.next_char()

            # Check if the token is in the list of keywords.
            token_text = self.source[start_pos: self.current_pos + 1]
            keyword = Token.check_if_keyword(token_text)
            if keyword is None: # Identifier
                token = Token(token_text, TokenType.IDENT)
            else: # keyword
                token = Token(token_text, keyword)
        else:
            # Unknown token!
            self.abort("Unknown token: " + self.current_char)

        self.next_char()
        return token

    def pick_digits(self):
        ''' Pick all consecutive digits '''
        while self.peek().isdigit():
            self.next_char()

    def get_doublechar_token(self, second_char, double_char_token, single_char_token):
        ''' method to parse double char tokens like ==, <=, etc '''
        if self.peek() == second_char:
            last_char = self.current_char
            self.next_char()
            token = Token(last_char + self.current_char, double_char_token)
        else:
            token = Token(self.current_char, single_char_token)
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

    def skip_comment(self):
        ''' Skip comments in the code '''
        if self.current_char == '#':
            while self.current_char != '\n':
                self.next_char()

class TokenType(enum.Enum):
    '''Token definitions'''
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
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

class Token:
    ''' Token contains the original text and the type of the token'''
    def __init__(self, token_text : str, token_kind: TokenType):
        self.text = token_text
        self.kind = token_kind

    @staticmethod
    def check_if_keyword(token_text):
        for kind in TokenType:
            # Relies on all keywords enum values being 1XX.
            if kind.name == token_text and kind.value >= 100 and kind.value < 200:
                return kind
        return None
