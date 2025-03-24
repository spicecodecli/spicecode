import re
from ..token import Token, TokenType

class JavaScriptLexer:
    # Palavras-chave do JavaScript
    KEYWORDS = {
        "break", "case", "catch", "class", "const", "continue", "debugger", "default", 
        "delete", "do", "else", "export", "extends", "finally", "for", "function", 
        "if", "import", "in", "instanceof", "new", "return", "super", "switch", 
        "this", "throw", "try", "typeof", "var", "void", "while", "with", "yield",
        "true", "false", "null", "undefined"
    }
    
    # Operadores do JavaScript
    OPERATORS = {
        "+", "-", "*", "/", "%", "=", "==", "===", "!=", "!==", "<", ">", "<=", ">=", 
        "&&", "||", "!", "&", "|", "^", "<<", ">>", ">>>", "&=", "|=", "^=", "<<=", 
        ">>=", ">>>=", "+=", "-=", "*=", "/=", "%=", "++", "--", "?:", "=>", "**"
    }
    
    # Delimitadores do JavaScript
    DELIMITERS = {
        "(", ")", "{", "}", "[", "]", ",", ";", ".", ":"
    }
    
    # Regex para números e identificadores
    NUMBER_PATTERN = re.compile(r"0b[01]+|0o[0-7]+|0x[0-9a-fA-F]+|\d+(\.\d+)?([eE][+-]?\d+)?")
    IDENTIFIER_PATTERN = re.compile(r"[a-zA-Z_$][a-zA-Z0-9_$]*")
    
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

            # Ignora espaços em branco
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

            # Comentários
            if char == "/":
                if self.position + 1 < len(self.source_code):
                    next_char = self.source_code[self.position + 1]
                    if next_char == "/":  # Comentário de linha única
                        comment_token = self.tokenize_single_line_comment()
                        tokens.append(comment_token)
                        continue
                    elif next_char == "*":  # Comentário de múltiplas linhas
                        comment_token = self.tokenize_multi_line_comment()
                        tokens.append(comment_token)
                        continue

            # Números
            if char.isdigit() or (char == "0" and self.position + 1 < len(self.source_code) and 
                                  self.source_code[self.position + 1] in "bxo"):
                token = self.tokenize_number()
                tokens.append(token)
                continue

            # Strings
            if char in {'"', "'", "`"}:
                token = self.tokenize_string()
                tokens.append(token)
                continue

            # Identificadores
            if char.isalpha() or char in "_$":
                token = self.tokenize_identifier()
                tokens.append(token)
                continue

            # Delimitadores
            if char in self.DELIMITERS:
                tokens.append(Token(TokenType.DELIMITER, char, self.line, self.column))
                self.position += 1
                self.column += 1
                continue

            # Operadores
            if match := self.match_operator():
                tokens.append(match)
                continue

            # Caractere desconhecido
            error_char = self.source_code[self.position]
            tokens.append(Token(TokenType.ERROR, error_char, self.line, self.column))
            self.position += 1
            self.column += 1

        # Token de fim de arquivo
        tokens.append(Token(TokenType.EOF, "EOF", self.line, self.column))
        return tokens

    def tokenize_single_line_comment(self):
        """Tokeniza um comentário de linha única (// ...)."""
        start_pos = self.position
        start_col = self.column
        
        while self.position < len(self.source_code) and self.source_code[self.position] != "\n":
            self.position += 1
            self.column += 1
            
        comment = self.source_code[start_pos:self.position]
        return Token(TokenType.COMMENT, comment, self.line, start_col)

    def tokenize_multi_line_comment(self):
        """Tokeniza um comentário de múltiplas linhas (/* ... */)."""
        start_pos = self.position
        start_col = self.column
        
        while self.position + 1 < len(self.source_code):
            if self.source_code[self.position] == "*" and self.source_code[self.position + 1] == "/":
                self.position += 2
                self.column += 2
                break
            if self.source_code[self.position] == "\n":
                self.line += 1
                self.column = 1
                self.current_line_start = self.position + 1
            else:
                self.column += 1
            self.position += 1
        else:
            return Token(TokenType.ERROR, "comentário não fechado", self.line, start_col)
        
        comment = self.source_code[start_pos:self.position]
        return Token(TokenType.COMMENT, comment, self.line, start_col)

    def tokenize_number(self):
        """Tokeniza um número (decimal, binário, octal, hexadecimal)."""
        start_pos = self.position
        match = self.NUMBER_PATTERN.match(self.source_code[self.position:])
        if match:
            number = match.group(0)
            self.position += len(number)
            self.column += len(number)
            return Token(TokenType.NUMBER, number, self.line, self.column - len(number))
        
        # Fallback para tokenização manual
        while self.position < len(self.source_code) and self.source_code[self.position].isdigit():
            self.position += 1
            self.column += 1
        
        return Token(TokenType.NUMBER, self.source_code[start_pos:self.position], self.line, self.column - (self.position - start_pos))

    def tokenize_string(self):
        """Tokeniza uma string (aspas simples, duplas ou template)."""
        start_pos = self.position
        start_col = self.column
        quote_char = self.source_code[self.position]
        self.position += 1
        self.column += 1
        
        while self.position < len(self.source_code):
            char = self.source_code[self.position]
            if char == quote_char:  # Fecha a string
                self.position += 1
                self.column += 1
                break
            elif char == "\\":  # Escape de caracteres
                self.position += 2
                self.column += 2
            self.position += 1
            self.column += 1
        
        string_value = self.source_code[start_pos:self.position]
        return Token(TokenType.STRING, string_value, self.line, start_col)

    def tokenize_identifier(self):
        """Tokeniza um identificador."""
        start_pos = self.position
        start_col = self.column
        
        while self.position < len(self.source_code) and (self.source_code[self.position].isalnum() or self.source_code[self.position] in "_$"):
            self.position += 1
            self.column += 1
        
        identifier = self.source_code[start_pos:self.position]
        if identifier in self.KEYWORDS:
            return Token(TokenType.KEYWORD, identifier, self.line, start_col)
        else:
            return Token(TokenType.IDENTIFIER, identifier, self.line, start_col)

    def match_operator(self):
        """Tenta casar com um operador."""
        for op in sorted(self.OPERATORS, key=len, reverse=True):
            if self.source_code.startswith(op, self.position):
                token = Token(TokenType.OPERATOR, op, self.line, self.column)
                self.position += len(op)
                self.column += len(op)
                return token
        return None