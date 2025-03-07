import re
from ..token import Token, TokenType

class BrainfuckLexer:
    # Brainfuck has only 8 operations
    OPERATORS = {
        ">": "INCREMENT_POINTER",    # Increment the data pointer
        "<": "DECREMENT_POINTER",    # Decrement the data pointer
        "+": "INCREMENT_VALUE",      # Increment the byte at the data pointer
        "-": "DECREMENT_VALUE",      # Decrement the byte at the data pointer
        ".": "OUTPUT",               # Output the byte at the data pointer
        ",": "INPUT",                # Accept one byte of input
        "[": "JUMP_FORWARD",         # Jump forward to matching ] if byte is 0
        "]": "JUMP_BACKWARD"         # Jump back to matching [ if byte is nonzero
    }
    
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.current_line_start = 0

    def tokenize(self):
        tokens = []
        
        while self.position < len(self.source_code):
            char = self.source_code[self.position]

            # Handle whitespace and newlines
            if char.isspace():
                if char == "\n":
                    # Unlike Ruby, we don't need to tokenize newlines in Brainfuck
                    # but we'll keep track of them for line counting
                    self.line += 1
                    self.column = 1
                    self.current_line_start = self.position + 1
                else:
                    self.column += 1
                self.position += 1
                continue

            # Handle Brainfuck operators
            if char in self.OPERATORS:
                token = Token(TokenType.OPERATOR, char, self.line, self.column)
                tokens.append(token)
                self.position += 1
                self.column += 1
                continue
                
            # Handle comments (everything that's not a Brainfuck operator)
            # In Brainfuck, any character that isn't an operator is treated as a comment
            # We'll collect consecutive comment characters as a single comment token
            if char not in self.OPERATORS:
                comment_token = self.tokenize_comment()
                tokens.append(comment_token)
                continue

        # Add EOF token
        tokens.append(Token(TokenType.EOF, "EOF", self.line, self.column))
        return tokens

    def tokenize_comment(self):
        """Tokenize a comment and return it as a COMMENT token"""
        start_pos = self.position
        start_col = self.column
        
        # Collect all non-operator characters as a comment until we hit an operator or newline
        while (self.position < len(self.source_code) and 
               self.source_code[self.position] not in self.OPERATORS and 
               self.source_code[self.position] != "\n"):
            self.position += 1
            self.column += 1
            
        comment = self.source_code[start_pos:self.position]
        return Token(TokenType.COMMENT, comment, self.line, start_col)
    
    def get_current_line(self):
        """Get the current line of code being processed (for error reporting)"""
        end = self.source_code.find('\n', self.current_line_start)
        if end == -1:
            end = len(self.source_code)
        return self.source_code[self.current_line_start:end]