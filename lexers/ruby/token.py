from enum import Enum

class TokenType(Enum):
    # Keywords
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    OPERATOR = "OPERATOR"
    SYMBOL = "SYMBOL"
    NEWLINE = "NEWLINE"
    EOF = "EOF"  # End of file

class Token:
    def __init__(self, type: TokenType, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, {self.line}:{self.column})"
