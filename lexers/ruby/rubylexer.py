import re
from ..token import Token, TokenType

class RubyLexer:
    # Ruby keywords
    KEYWORDS = {
        "def", "end", "if", "else", "elsif", "unless", "while", "until", "for", "do", 
        "return", "break", "next", "class", "module", "begin", "rescue", "ensure", 
        "yield", "self", "nil", "true", "false", "super", "then", "case", "when"
    }
    
    # Ruby operators carlos sainz smooth operator as a LH fan i thank you for your sacrifice
    OPERATORS = {
        "+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=", "&&", "||", 
        "+=", "-=", "*=", "/=", "%=", "**", "**=", "&", "|", "^", "~", "<<", ">>", 
        "and", "or", "not", "=>", "..", "...", "!~", "=~"
    }
    
    # i have NO CLUE what any of this means or how it works so dont ask me use chatgpt or claude or something
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

            # handle whitespace
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

            # handle comments
            if char == "#":
                comment_token = self.tokenize_comment()
                tokens.append(comment_token)
                continue

            # handle numbers
            if char.isdigit():
                token = self.tokenize_number()
                tokens.append(token)
                continue

            # handle strings with something called interpolation awareness whatever that means
            if char in {'"', "'"}:
                token = self.tokenize_string()
                tokens.append(token)
                continue

            # handle identifiers and keywords
            if char.isalpha() or char == "_":
                token = self.tokenize_identifier()
                tokens.append(token)
                continue

            # handle special delimiters used in blocks
            if char in "({[]})" and self.position < len(self.source_code):
                tokens.append(Token(TokenType.DELIMITER, char, self.line, self.column))
                self.position += 1
                self.column += 1
                continue

            # handle operators
            if match := self.match_operator():
                tokens.append(match)
                continue

            # handle symbols
            if char == ':':
                symbol_match = self.SYMBOL_PATTERN.match(self.source_code[self.position:])
                if symbol_match:
                    symbol = symbol_match.group(0)
                    tokens.append(Token(TokenType.SYMBOL, symbol, self.line, self.column))
                    self.position += len(symbol)
                    self.column += len(symbol)
                    continue

            # handle special for like instance variables (@var) and class variables (@@var)
            if char == '@' and self.position + 1 < len(self.source_code):
                start_pos = self.position
                self.position += 1  # sjip @
                self.column += 1
                
                # check for class variable (@@)
                if self.position < len(self.source_code) and self.source_code[self.position] == '@':
                    self.position += 1
                    self.column += 1
                
                # parse  variable name
                if self.position < len(self.source_code) and (self.source_code[self.position].isalpha() or self.source_code[self.position] == '_'):
                    while self.position < len(self.source_code) and (self.source_code[self.position].isalnum() or self.source_code[self.position] == '_'):
                        self.position += 1
                        self.column += 1
                    tokens.append(Token(TokenType.INSTANCE_VAR, self.source_code[start_pos:self.position], self.line, self.column))
                    continue

            # handle global variables ($var)
            if char == '$' and self.position + 1 < len(self.source_code):
                start_pos = self.position
                self.position += 1  # skip $
                self.column += 1
                
                # parase variable name or special global variable
                if self.position < len(self.source_code) and (self.source_code[self.position].isalnum() or self.source_code[self.position] in '_!@&+`\'=~/\\,;.<>*$?:'):
                    while self.position < len(self.source_code) and (self.source_code[self.position].isalnum() or self.source_code[self.position] == '_'):
                        self.position += 1
                        self.column += 1
                    tokens.append(Token(TokenType.GLOBAL_VAR, self.source_code[start_pos:self.position], self.line, self.column))
                    continue

            # unknown character - emit an error token but continue processing keep going never stop
            error_char = self.source_code[self.position]
            tokens.append(Token(TokenType.ERROR, error_char, self.line, self.column))
            self.position += 1
            self.column += 1

        tokens.append(Token(TokenType.EOF, "EOF", self.line, self.column))
        return tokens

    def tokenize_comment(self):
        """Tokenize a comment and return it as a COMMENT token instead of skipping it"""
        start_pos = self.position
        start_col = self.column
        
        while self.position < len(self.source_code) and self.source_code[self.position] != "\n":
            self.position += 1
            self.column += 1
            
        comment = self.source_code[start_pos:self.position]
        return Token(TokenType.COMMENT, comment, self.line, start_col)

    def tokenize_number(self):
        start_pos = self.position
        
        # use regex to match complex number patterns
        match = self.NUMBER_PATTERN.match(self.source_code[self.position:])
        if match:
            number = match.group(0)
            self.position += len(number)
            self.column += len(number)
            return Token(TokenType.NUMBER, number, self.line, self.column - len(number))
        
        # fallback to simple digit parsing
        while self.position < len(self.source_code) and self.source_code[self.position].isdigit():
            self.position += 1
            self.column += 1
        
        # check for decimal point followed by digits
        if self.position < len(self.source_code) and self.source_code[self.position] == '.' and \
           self.position + 1 < len(self.source_code) and self.source_code[self.position + 1].isdigit():
            self.position += 1  # skip decimal point
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
        
        # check if it's a keyword or a boolean literal
        if word in self.KEYWORDS:
            token_type = TokenType.KEYWORD
        elif word in ["true", "false", "nil"]:
            token_type = TokenType.BOOLEAN
        else:
            token_type = TokenType.IDENTIFIER
            
        # check for method calls (identifier followed by dot)
        if (token_type == TokenType.IDENTIFIER and 
            self.position < len(self.source_code) and 
            self.source_code[self.position] == '.'):
            return Token(TokenType.METHOD_CALL, word, self.line, start_col)
            
        return Token(token_type, word, self.line, start_col)

    def tokenize_string(self):
        quote_char = self.source_code[self.position]
        start_pos = self.position
        start_col = self.column
        self.position += 1  # skip opening quote
        self.column += 1
        
        # flag to track if its handling string interpolation
        in_interpolation = False
        
        while self.position < len(self.source_code):
            char = self.source_code[self.position]
            
            # handle string interpolation
            if quote_char == '"' and char == '#' and self.position + 1 < len(self.source_code) and self.source_code[self.position + 1] == '{':
                in_interpolation = True
                self.position += 2  # skip #{
                self.column += 2
                continue
                
            if in_interpolation and char == '}':
                in_interpolation = False
                self.position += 1
                self.column += 1
                continue
                
            # handle escape sequences
            if char == '\\' and self.position + 1 < len(self.source_code):
                self.position += 2  # skip the escape sequence
                self.column += 2
                continue
                
            # chec for closing quote (but not if inside interpolation)
            if char == quote_char and not in_interpolation:
                self.position += 1  # sjip closing quote
                self.column += 1
                return Token(TokenType.STRING, self.source_code[start_pos:self.position], self.line, start_col)
                
            # handle newlines in strings
            if char == '\n':
                self.line += 1
                self.column = 1
                self.current_line_start = self.position + 1
            else:
                self.column += 1
                
            self.position += 1

        # handle unclosed strings - this is an error condition
        return Token(TokenType.ERROR, f"Unclosed string: {self.source_code[start_pos:self.position]}", self.line, start_col)

    def match_operator(self):
        # sort operators by length to match longest first
        for op in sorted(self.OPERATORS, key=len, reverse=True):
            if self.source_code[self.position:self.position + len(op)] == op:
                token = Token(TokenType.OPERATOR, op, self.line, self.column)
                self.position += len(op)
                self.column += len(op)
                return token
        return None
    
    def get_current_line(self):
        """Get the current line of code being processed (for error reporting)"""
        end = self.source_code.find('\n', self.current_line_start)
        if end == -1:
            end = len(self.source_code)
        return self.source_code[self.current_line_start:end]