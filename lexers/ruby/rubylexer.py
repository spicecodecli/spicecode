import re
from .token import Token, TokenType

class RubyLexer:
    # Expanded keywords list to include more Ruby keywords
    KEYWORDS = {
        "def", "end", "if", "else", "elsif", "unless", "while", "until", "for", "do", 
        "return", "break", "next", "class", "module", "begin", "rescue", "ensure", 
        "yield", "self", "nil", "true", "false", "super", "then", "case", "when"
    }
    
    # Expanded operators list to include more Ruby operators
    OPERATORS = {
        "+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=", "&&", "||", 
        "+=", "-=", "*=", "/=", "%=", "**", "**=", "&", "|", "^", "~", "<<", ">>", 
        "and", "or", "not", "=>", "..", "...", "!~", "=~"
    }
    
    # Enhanced regex patterns
    SYMBOL_PATTERN = re.compile(r":([a-zA-Z_][a-zA-Z0-9_]*|[-+/*!%^&*=<>?]|\[\]=?|<<|>>)")
    NUMBER_PATTERN = re.compile(r"\d+(\.\d+)?([eE][+-]?\d+)?")
    
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

            # Handle whitespace
            if char.isspace():
                if char == "\n":
                    tokens.append(Token(TokenType.NEWLINE, "\\n", self.line, self.column))
                    self.line += 1
                    self.column = 1
                    self.current_line_start = self.position + 1
                else:
                    self.column += 1
                self.position += 1
                continue

            # Handle comments
            if char == "#":
                self.skip_comment()
                continue

            # Handle numbers
            if char.isdigit():
                token = self.tokenize_number()
                tokens.append(token)
                continue

            # Handle strings with interpolation awareness
            if char in {'"', "'"}:
                token = self.tokenize_string()
                tokens.append(token)
                continue

            # Handle identifiers and keywords
            if char.isalpha() or char == "_":
                token = self.tokenize_identifier()
                tokens.append(token)
                continue

            # Handle special delimiters used in blocks
            if char in "({[]})" and self.position < len(self.source_code):
                tokens.append(Token(TokenType.DELIMITER, char, self.line, self.column))
                self.position += 1
                self.column += 1
                continue

            # Handle operators
            if match := self.match_operator():
                tokens.append(match)
                continue

            # Handle symbols
            if char == ':':
                symbol_match = self.SYMBOL_PATTERN.match(self.source_code[self.position:])
                if symbol_match:
                    symbol = symbol_match.group(0)
                    tokens.append(Token(TokenType.SYMBOL, symbol, self.line, self.column))
                    self.position += len(symbol)
                    self.column += len(symbol)
                    continue

            # Handle special cases like instance variables (@var) and class variables (@@var)
            if char == '@' and self.position + 1 < len(self.source_code):
                start_pos = self.position
                self.position += 1  # Skip @
                self.column += 1
                
                # Check for class variable (@@)
                if self.position < len(self.source_code) and self.source_code[self.position] == '@':
                    self.position += 1
                    self.column += 1
                
                # Parse the variable name
                if self.position < len(self.source_code) and (self.source_code[self.position].isalpha() or self.source_code[self.position] == '_'):
                    while self.position < len(self.source_code) and (self.source_code[self.position].isalnum() or self.source_code[self.position] == '_'):
                        self.position += 1
                        self.column += 1
                    tokens.append(Token(TokenType.INSTANCE_VAR, self.source_code[start_pos:self.position], self.line, self.column))
                    continue

            # Handle global variables ($var)
            if char == '$' and self.position + 1 < len(self.source_code):
                start_pos = self.position
                self.position += 1  # Skip $
                self.column += 1
                
                # Parse the variable name or special global variable
                if self.position < len(self.source_code) and (self.source_code[self.position].isalnum() or self.source_code[self.position] in '_!@&+`\'=~/\\,;.<>*$?:'):
                    while self.position < len(self.source_code) and (self.source_code[self.position].isalnum() or self.source_code[self.position] == '_'):
                        self.position += 1
                        self.column += 1
                    tokens.append(Token(TokenType.GLOBAL_VAR, self.source_code[start_pos:self.position], self.line, self.column))
                    continue

            # Unknown character - emit an error token but continue processing
            error_char = self.source_code[self.position]
            tokens.append(Token(TokenType.ERROR, error_char, self.line, self.column))
            self.position += 1
            self.column += 1

        tokens.append(Token(TokenType.EOF, "EOF", self.line, self.column))
        return tokens

    def tokenize_number(self):
        start_pos = self.position
        
        # Use regex to match complex number patterns
        match = self.NUMBER_PATTERN.match(self.source_code[self.position:])
        if match:
            number = match.group(0)
            self.position += len(number)
            self.column += len(number)
            return Token(TokenType.NUMBER, number, self.line, self.column - len(number))
        
        # Fallback to simple digit parsing
        while self.position < len(self.source_code) and self.source_code[self.position].isdigit():
            self.position += 1
            self.column += 1
        
        # Check for decimal point followed by digits
        if self.position < len(self.source_code) and self.source_code[self.position] == '.' and \
           self.position + 1 < len(self.source_code) and self.source_code[self.position + 1].isdigit():
            self.position += 1  # Skip decimal point
            self.column += 1
            while self.position < len(self.source_code) and self.source_code[self.position].isdigit():
                self.position += 1
                self.column += 1
        
        return Token(TokenType.NUMBER, self.source_code[start_pos:self.position], self.line, self.column - (self.position - start_pos))

    def tokenize_identifier(self):
        start_pos = self.position
        start_col = self.column
        
        while self.position < len(self.source_code) and (self.source_code[self.position].isalnum() or self.source_code[self.position] == "_" or self.source_code[self.position] == "?"):
            self.position += 1
            self.column += 1
            
        word = self.source_code[start_pos:self.position]
        
        # Check if it's a keyword or a boolean literal
        if word in self.KEYWORDS:
            token_type = TokenType.KEYWORD
        elif word in ["true", "false", "nil"]:
            token_type = TokenType.BOOLEAN
        else:
            token_type = TokenType.IDENTIFIER
            
        # Check for method calls (identifier followed by a dot)
        if (token_type == TokenType.IDENTIFIER and 
            self.position < len(self.source_code) and 
            self.source_code[self.position] == '.'):
            return Token(TokenType.METHOD_CALL, word, self.line, start_col)
            
        return Token(token_type, word, self.line, start_col)

    def tokenize_string(self):
        quote_char = self.source_code[self.position]
        start_pos = self.position
        start_col = self.column
        self.position += 1  # Skip opening quote
        self.column += 1
        
        # Flag to track if we're handling string interpolation
        in_interpolation = False
        
        while self.position < len(self.source_code):
            char = self.source_code[self.position]
            
            # Handle string interpolation
            if quote_char == '"' and char == '#' and self.position + 1 < len(self.source_code) and self.source_code[self.position + 1] == '{':
                in_interpolation = True
                self.position += 2  # Skip #{
                self.column += 2
                continue
                
            if in_interpolation and char == '}':
                in_interpolation = False
                self.position += 1
                self.column += 1
                continue
                
            # Handle escape sequences
            if char == '\\' and self.position + 1 < len(self.source_code):
                self.position += 2  # Skip the escape sequence
                self.column += 2
                continue
                
            # Check for closing quote (but not if we're inside interpolation)
            if char == quote_char and not in_interpolation:
                self.position += 1  # Skip closing quote
                self.column += 1
                return Token(TokenType.STRING, self.source_code[start_pos:self.position], self.line, start_col)
                
            # Handle newlines in strings
            if char == '\n':
                self.line += 1
                self.column = 1
                self.current_line_start = self.position + 1
            else:
                self.column += 1
                
            self.position += 1

        # Handle unclosed strings - this is an error condition
        return Token(TokenType.ERROR, f"Unclosed string: {self.source_code[start_pos:self.position]}", self.line, start_col)

    def match_operator(self):
        # Sort operators by length to match longest first
        for op in sorted(self.OPERATORS, key=len, reverse=True):
            if self.source_code[self.position:self.position + len(op)] == op:
                token = Token(TokenType.OPERATOR, op, self.line, self.column)
                self.position += len(op)
                self.column += len(op)
                return token
        return None

    def skip_comment(self):
        while self.position < len(self.source_code) and self.source_code[self.position] != "\n":
            self.position += 1
            self.column += 1
        # Newline will be handled in the main loop
        
    def get_current_line(self):
        """Get the current line of code being processed (for error reporting)"""
        end = self.source_code.find('\n', self.current_line_start)
        if end == -1:
            end = len(self.source_code)
        return self.source_code[self.current_line_start:end]