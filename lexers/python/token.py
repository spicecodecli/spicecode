from enum import Enum, auto

class TokenType(Enum):
    # basic tokens
    IDENTIFIER = auto()
    KEYWORD = auto()
    OPERATOR = auto()
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    SYMBOL = auto()
    DELIMITER = auto()
    
    # special token types
    NEWLINE = auto()
    COMMENT = auto()
    INSTANCE_VAR = auto()
    GLOBAL_VAR = auto()
    METHOD_CALL = auto()
    
    # ertror handling
    ERROR = auto()
    EOF = auto()

class Token:
    def __init__(self, token_type, value, line, column):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', {self.line}:{self.column})"