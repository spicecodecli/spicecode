import re
from .token import Token, TokenType

class RubyLexer:
    KEYWORDS = {"def", "end", "if", "else", "elsif", "while", "do", "return", "class"}
    OPERATORS = {"+", "-", "*", "/", "=", "==", "!=", "<", ">", "<=", ">=", "&&", "||", "+=", "-="}
    SYMBOL_PATTERN = re.compile(r":[a-zA-Z_][a-zA-Z0-9_]*")  # Matches symbols like `:my_symbol`
    
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.line = 1
        self.column = 1

    def tokenize(self):
        tokens = []
        
        while self.position < len(self.source_code):
            char = self.source_code[self.position]

            if char.isspace():
                if char == "\n":
                    tokens.append(Token(TokenType.NEWLINE, "\\n", self.line, self.column))
                    self.line += 1
                    self.column = 1
                self.position += 1
                continue

            if char == "#":  # Comment Handling
                self.skip_comment()
                continue

            if char.isdigit():
                token = self.tokenize_number()
                tokens.append(token)
                continue

            if char in {'"', "'"}:  # String Handling
                token = self.tokenize_string()
                tokens.append(token)
                continue

            if char.isalpha() or char == "_":
                token = self.tokenize_identifier()
                tokens.append(token)
                continue

            if self.match_operator():
                tokens.append(self.match_operator())
                continue

            if match := self.SYMBOL_PATTERN.match(self.source_code[self.position:]):
                tokens.append(Token(TokenType.SYMBOL, match.group(), self.line, self.column))
                self.position += len(match.group())
                self.column += len(match.group())
                continue

            # Unknown character (Error handling can be added here)
            self.position += 1
            self.column += 1

        tokens.append(Token(TokenType.EOF, "EOF", self.line, self.column))
        return tokens

    def tokenize_number(self):
        start_pos = self.position
        while self.position < len(self.source_code) and self.source_code[self.position].isdigit():
            self.position += 1
            self.column += 1
        return Token(TokenType.NUMBER, self.source_code[start_pos:self.position], self.line, self.column)

    def tokenize_identifier(self):
        start_pos = self.position
        while self.position < len(self.source_code) and (self.source_code[self.position].isalnum() or self.source_code[self.position] == "_"):
            self.position += 1
            self.column += 1
        word = self.source_code[start_pos:self.position]
        token_type = TokenType.KEYWORD if word in self.KEYWORDS else TokenType.IDENTIFIER
        return Token(token_type, word, self.line, self.column)

    def tokenize_string(self):
        quote_char = self.source_code[self.position]
        start_pos = self.position
        self.position += 1  # Skip opening quote
        self.column += 1

        while self.position < len(self.source_code):
            if self.source_code[self.position] == quote_char:
                self.position += 1  # Skip closing quote
                self.column += 1
                return Token(TokenType.STRING, self.source_code[start_pos:self.position], self.line, self.column)
            self.position += 1
            self.column += 1

        return Token(TokenType.STRING, self.source_code[start_pos:], self.line, self.column)  # Handle unclosed strings

    def match_operator(self):
        for op in sorted(self.OPERATORS, key=len, reverse=True):  # Longest match first
            if self.source_code[self.position:self.position + len(op)] == op:
                token = Token(TokenType.OPERATOR, op, self.line, self.column)
                self.position += len(op)
                self.column += len(op)
                return token
        return None

    def skip_comment(self):
        while self.position < len(self.source_code) and self.source_code[self.position] != "\n":
            self.position += 1
        # Newline will be handled in the main loop