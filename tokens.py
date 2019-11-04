from tokentype import TokenType
from collections import namedtuple

class Token(namedtuple('Token', ['type', 'lexeme', 'literal', 'line'])):
    def str(self):
        return f"{self.type} {self.lexeme} {self.literal}"

