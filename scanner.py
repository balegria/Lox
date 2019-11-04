from tokens import Token
from tokentype import TokenType

class Scanner():
    def __init__(self, source, errCallback):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 0
        self.error = errCallback

    def scan_tokens(self):
        while not self.is_at_end:
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        #TODO: large elif chainge -> move to a switch-like if perf ever matters

        if c == '(': self.add_token(TokenType.LEFT_PAREN)
        elif c == ')': self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{': self.add_token(TokenType.LEFT_BRACE)
        elif c == '}': self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',': self.add_token(TokenType.COMMA)
        elif c == '.': self.add_token(TokenType.DOT)
        elif c == '-': self.add_token(TokenType.MINUS)
        elif c == '+': self.add_token(TokenType.PLUS)
        elif c == ';': self.add_token(TokenType.SEMICOLON)
        elif c == '*': self.add_token(TokenType.STAR)
        elif c == '!': self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif c == '=': self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif c == '<': self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif c == '>': self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)

        elif c == '/':
            if self.match('/'):
                # then this is a (c-style) line comment
                while self.peek() != '\n' and not self.is_at_end:
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)

        elif c in {' ', '\r', '\t'}:
            pass
        elif c == '\n':
            self.line += 1

        elif c == '"': self.string()
        elif c.isnumeric(): self.number()
        elif c.isalpha(): self.identifier()


        else:
            self.error(self.line, "unexpected character: {}".format(c))

    def string(self):
        while self.peek() != '"' and not self.is_at_end:
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end:
            self.error(self.line, "Unterminated string")
            return

        self.advance()

        self.add_token(TokenType.STRING, self.source[self.start+1:self.current-1])

    def number(self):
        while self.peek().isnumeric():
            self.advance()

        if self.peek() == '.' and self.peek(1).isdigit():
            self.advance()

            while self.peek().isnumeric():
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def identifier(self):
        while self.peek().isalnum():
            self.advance()

        text = self.source[self.start:self.current]
        if text.lower() == text and text.upper() in TokenType.__members__:
            self.add_token(TokenType[text.upper()])
        else:
            self.add_token(TokenType.IDENTIFIER)

    def match(self, expected):
        if self.is_at_end: return False
        if self.source[self.current] != expected: return False

        self.current += 1
        return True

    def peek(self, ahead=0):
        if self.current + ahead >= len(self.source):
            return '\0'
        return self.source[self.current]

    def add_token(self, token_type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    @property
    def is_at_end(self):
        return self.current >= len(self.source)

