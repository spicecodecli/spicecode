from enum import Enum, auto

class TokenType(Enum):
    # Basic token types
    KEYWORD = auto()        # Ruby keywords like 'def', 'if', etc.
    IDENTIFIER = auto()     # Variable and method names
    NUMBER = auto()         # Integer and floating point numbers
    STRING = auto()         # String literals
    BOOLEAN = auto()        # true, false
    OPERATOR = auto()       # +, -, *, /, etc.
    SYMBOL = auto()         # :symbol
    DELIMITER = auto()      # (, ), [, ], {, }
    
    # Special variable types
    INSTANCE_VAR = auto()   # @instance_variable
    CLASS_VAR = auto()      # @@class_variable
    GLOBAL_VAR = auto()     # $global_variable
    CONSTANT = auto()       # CONSTANT
    
    # Method-related
    METHOD_CALL = auto()    # When an identifier is used in a method call
    
    # Structural tokens
    NEWLINE = auto()        # Line breaks
    EOF = auto()            # End of file
    
    # Error handling
    ERROR = auto()          # For lexer errors

class Token:
    def __init__(self, type: TokenType, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
        
    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, {self.line}:{self.column})"
        
    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return (self.type == other.type and 
                self.value == other.value and 
                self.line == other.line and 
                self.column == other.column)
                
    def location(self):
        """Return a string representation of the token's location"""
        return f"line {self.line}, column {self.column}"