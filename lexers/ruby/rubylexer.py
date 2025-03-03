import re
from .token import Token, TokenType

class RubyLexer:
    KEYWORDS = {"def", "end", "if", "else", "elsif", "while", "do", "return"}
    OPERATORS = {"+", "-", "*", "/", "=", "=="}

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

            if char.isdigit():
                token = self.tokenize_number()
                tokens.append(token)
                continue

            if char.isalpha() or char == "_":
                token = self.tokenize_identifier()
                tokens.append(token)
                continue

            if char in self.OPERATORS:
                tokens.append(Token(TokenType.OPERATOR, char, self.line, self.column))
                self.position += 1
                self.column += 1
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
