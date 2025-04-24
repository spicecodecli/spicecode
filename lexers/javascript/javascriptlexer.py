import re
from ..token import Token, TokenType

class JavaScriptLexer:
    # palavras-chave do javascript
    KEYWORDS = {
        "function", "if", "else", "return", "let", "const", "var", "for", "while", 
        "do", "break", "continue", "switch", "case", "default", "try", "catch", 
        "throw", "new", "this", "class", "extends", "super", "import", "export", 
        "typeof", "instanceof", "void", "delete", "in", "of", "yield", "await", 
        "async", "true", "false", "null", "undefined"
    }
    
    # operadores do javascript
    OPERATORS = {
        "+", "-", "*", "/", "%", "=", "==", "===", "!=", "!==", ">", "<", ">=", 
        "<=", "&&", "||", "!", "&", "|", "^", "~", "<<", ">>", ">>>", "++", "--", 
        "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>=", ">>>=", 
        "=>", "?", ":", "."
    }
    
    # regex para números e identificadores
    NUMBER_PATTERN = re.compile(r"\d+(\.\d+)?([eE][+-]?\d+)?")
    IDENTIFIER_PATTERN = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")
    
    def __init__(self, source_code):
        self.source_code = source_code  # código fonte que vai ser tokenizado
        self.position = 0  # posição atual no código
        self.line = 1  # linha atual
        self.column = 1  # coluna atual
        self.current_line_start = 0  # início da linha atual

    def tokenize(self):
        tokens = []  # lista de tokens que vai ser retornada
        
        while self.position < len(self.source_code):
            char = self.source_code[self.position]  # caractere atual

            # ignora espaços em branco
            if char.isspace():
                if char == "\n":  # se for uma nova linha
                    tokens.append(Token(TokenType.NEWLINE, "\\n", self.line, self.column))
                    self.line += 1  # incrementa a linha
                    self.column = 1  # reseta a coluna
                    self.current_line_start = self.position + 1  # atualiza o início da linha
                else:
                    self.column += 1  # incrementa a coluna
                self.position += 1  # vai para o próximo caractere
                continue

            # se for um comentário (// ou /* ... */)
            if char == "/":
                if self.position + 1 < len(self.source_code):
                    next_char = self.source_code[self.position + 1]
                    if next_char == "/":  # comentário de linha única
                        comment_token = self.tokenize_single_line_comment()
                        tokens.append(comment_token)
                        continue
                    elif next_char == "*":  # comentário de múltiplas linhas
                        comment_token = self.tokenize_multi_line_comment()
                        tokens.append(comment_token)
                        continue

            # se for um número
            if char.isdigit():
                token = self.tokenize_number()  # tokeniza o número
                tokens.append(token)  # adiciona na lista de tokens
                continue

            # se for uma string (aspas simples ou duplas)
            if char in {'"', "'"}:
                token = self.tokenize_string()  # tokeniza a string
                tokens.append(token)  # adiciona na lista de tokens
                continue

            # se for um identificador (começa com letra ou _)
            if char.isalpha() or char == "_":
                token = self.tokenize_identifier()  # tokeniza o identificador
                tokens.append(token)  # adiciona na lista de tokens
                continue

            # se for um delimitador (colchetes, parênteses, etc.)
            if char in "()[]{},;:":
                tokens.append(Token(TokenType.DELIMITER, char, self.line, self.column))
                self.position += 1  # vai para o próximo caractere
                self.column += 1  # incrementa a coluna
                continue

            # se for um operador
            if match := self.match_operator():
                tokens.append(match)  # adiciona o operador na lista de tokens
                continue

            # se chegou aqui, é um caractere desconhecido (erro)
            error_char = self.source_code[self.position]
            tokens.append(Token(TokenType.ERROR, error_char, self.line, self.column))
            self.position += 1  # vai para o próximo caractere
            self.column += 1  # incrementa a coluna

        # adiciona o token de fim de arquivo (eof)
        tokens.append(Token(TokenType.EOF, "EOF", self.line, self.column))
        return tokens

    def tokenize_single_line_comment(self):
        """tokeniza um comentário de linha única (// ...)."""
        start_pos = self.position  # posição inicial do comentário
        start_col = self.column  # coluna inicial do comentário
        
        # avança até o fim da linha
        while self.position < len(self.source_code) and self.source_code[self.position] != "\n":
            self.position += 1
            self.column += 1
            
        comment = self.source_code[start_pos:self.position]  # pega o texto do comentário
        return Token(TokenType.COMMENT, comment, self.line, start_col)

    def tokenize_multi_line_comment(self):
        """tokeniza um comentário de múltiplas linhas (/* ... */)."""
        start_pos = self.position  # posição inicial do comentário
        start_col = self.column  # coluna inicial do comentário
        
        # avança até encontrar */
        while self.position + 1 < len(self.source_code):
            if self.source_code[self.position] == "*" and self.source_code[self.position + 1] == "/":
                self.position += 2  # avança os caracteres */
                self.column += 2
                break
            if self.source_code[self.position] == "\n":  # se tiver uma nova linha
                self.line += 1
                self.column = 1
                self.current_line_start = self.position + 1
            else:
                self.column += 1
            self.position += 1
        else:
            # se não encontrou o fechamento, é um erro
            return Token(TokenType.ERROR, "comentário não fechado", self.line, start_col)
        
        comment = self.source_code[start_pos:self.position]  # pega o texto do comentário
        return Token(TokenType.COMMENT, comment, self.line, start_col)

    def tokenize_number(self):
        """tokeniza um número (inteiro, decimal ou notação científica)."""
        start_pos = self.position  # posição inicial do número
        match = self.NUMBER_PATTERN.match(self.source_code[self.position:])  # tenta casar com o regex de número
        if match:
            number = match.group(0)  # pega o número
            self.position += len(number)  # avança a posição
            self.column += len(number)  # avança a coluna
            return Token(TokenType.NUMBER, number, self.line, self.column - len(number))
        
        # se não casou com o regex, faz a tokenização manual
        while self.position < len(self.source_code) and self.source_code[self.position].isdigit():
            self.position += 1
            self.column += 1
        
        # verifica se tem um ponto decimal
        if self.position < len(self.source_code) and self.source_code[self.position] == '.' and \
           self.position + 1 < len(self.source_code) and self.source_code[self.position + 1].isdigit():
            self.position += 1  # avança o ponto
            self.column += 1
            while self.position < len(self.source_code) and self.source_code[self.position].isdigit():
                self.position += 1
                self.column += 1
        
        return Token(TokenType.NUMBER, self.source_code[start_pos:self.position], self.line, self.column - (self.position - start_pos))

    def tokenize_identifier(self):
        """tokeniza um identificador (nomes de variáveis, funções, etc.)."""
        start_pos = self.position  # posição inicial do identificador
        start_col = self.column  # coluna inicial do identificador
        
        # Usa o padrão de regex para identificadores ou faz a tokenização manual
        match = self.IDENTIFIER_PATTERN.match(self.source_code[self.position:])
        if match:
            identifier = match.group(0)  # pega o identificador
            self.position += len(identifier)  # avança a posição
            self.column += len(identifier)  # avança a coluna
        else:
            # tokenização manual como fallback
            while self.position < len(self.source_code) and (self.source_code[self.position].isalnum() or self.source_code[self.position] == "_"):
                self.position += 1
                self.column += 1
            identifier = self.source_code[start_pos:self.position]  # pega o texto do identificador
        
        # verifica se é uma palavra-chave
        if identifier in self.KEYWORDS:
            return Token(TokenType.KEYWORD, identifier, self.line, start_col)
        else:
            return Token(TokenType.IDENTIFIER, identifier, self.line, start_col)

    def tokenize_string(self):
        """tokeniza uma string (aspas simples ou duplas)."""
        start_pos = self.position  # posição inicial da string
        start_col = self.column  # coluna inicial da string
        quote_char = self.source_code[self.position]  # tipo de aspas (' ou ")
        self.position += 1  # avança as aspas iniciais
        self.column += 1
        
        while self.position < len(self.source_code):
            char = self.source_code[self.position]
            if char == quote_char:  # fecha a string
                self.position += 1
                self.column += 1
                break
            elif char == "\\":  # escape de caracteres
                self.position += 1
                self.column += 1
                if self.position < len(self.source_code):
                    self.position += 1
                    self.column += 1
                continue
            elif char == "\n":  # se tiver uma nova linha dentro da string
                self.line += 1
                self.column = 1
                self.current_line_start = self.position + 1
            else:
                self.column += 1
            self.position += 1
        
        string_value = self.source_code[start_pos:self.position]  # pega o texto da string
        return Token(TokenType.STRING, string_value, self.line, start_col)

    def match_operator(self):
        """tenta casar com um operador."""
        for op in sorted(self.OPERATORS, key=len, reverse=True):  # verifica operadores mais longos primeiro
            if self.source_code.startswith(op, self.position):
                token = Token(TokenType.OPERATOR, op, self.line, self.column)
                self.position += len(op)
                self.column += len(op)
                return token
        return None
