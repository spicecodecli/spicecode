import re
from ..token import Token, TokenType

class PythonLexer:
    # palavras-chave do python
    KEYWORDS = {
        "def", "class", "return", "if", "else", "elif", "while", "for", "in", "break", 
        "continue", "pass", "import", "from", "as", "try", "except", "finally", "raise", 
        "with", "lambda", "and", "or", "not", "is", "None", "True", "False", "yield", 
        "global", "nonlocal", "assert", "del", "async", "await"
    }
    
    # operadores do python
    OPERATORS = {
        "+", "-", "*", "/", "//", "%", "**", "=", "==", "!=", "<", ">", "<=", ">=", 
        "and", "or", "not", "is", "in", "&", "|", "^", "~", "<<", ">>", ":=", "+=", 
        "-=", "*=", "/=", "%=", "**=", "//=", "&=", "|=", "^=", "<<=", ">>="
    }
    
    # regex pra pegar números e identificadores
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
                self.position += 1  # vai pro próximo caractere
                continue

            # se for um comentário (começa com #)
            if char == "#":
                comment_token = self.tokenize_comment()  # tokeniza o comentário
                tokens.append(comment_token)  # adiciona na lista de tokens
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
            if char in "()[]{},:.;@":
                tokens.append(Token(TokenType.DELIMITER, char, self.line, self.column))
                self.position += 1  # vai pro próximo caractere
                self.column += 1  # incrementa a coluna
                continue

            # se for um operador
            if match := self.match_operator():
                tokens.append(match)  # adiciona o operador na lista de tokens
                continue

            # se chegou aqui, é um caractere desconhecido (erro)
            error_char = self.source_code[self.position]
            tokens.append(Token(TokenType.ERROR, error_char, self.line, self.column))
            self.position += 1  # vai pro próximo caractere
            self.column += 1  # incrementa a coluna

        # adiciona o token de fim de arquivo (EOF)
        tokens.append(Token(TokenType.EOF, "EOF", self.line, self.column))
        return tokens

    def tokenize_comment(self):
        """tokeniza um comentário (tudo depois de # até o fim da linha)."""
        start_pos = self.position  # posição inicial do comentário
        start_col = self.column  # coluna inicial do comentário
        
        # avança até o fim da linha
        while self.position < len(self.source_code) and self.source_code[self.position] != "\n":
            self.position += 1
            self.column += 1
            
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
        """tokeniza um identificador (nome de variável, função, etc.) ou palavra-chave."""
        start_pos = self.position  # posição inicial do identificador
        start_col = self.column  # coluna inicial do identificador
        
        # avança enquanto for letra, número ou _
        while self.position < len(self.source_code) and (self.source_code[self.position].isalnum() or self.source_code[self.position] == "_"):
            self.position += 1
            self.column += 1
            
        word = self.source_code[start_pos:self.position]  # pega o texto do identificador
        
        # verifica se é uma palavra-chave ou um valor booleano/nulo
        if word in self.KEYWORDS:
            token_type = TokenType.KEYWORD
        elif word in ["True", "False", "None"]:
            token_type = TokenType.BOOLEAN
        else:
            token_type = TokenType.IDENTIFIER
            
        return Token(token_type, word, self.line, start_col)

    def tokenize_string(self):
        """tokeniza uma string (aspas simples, duplas ou triplas)."""
        quote_char = self.source_code[self.position]  # pega o tipo de aspas
        start_pos = self.position  # posição inicial da string
        start_col = self.column  # coluna inicial da string
        self.position += 1  # avança as aspas iniciais
        self.column += 1
        
        # verifica se é uma string com aspas triplas
        if self.position + 1 < len(self.source_code) and self.source_code[self.position] == quote_char and self.source_code[self.position + 1] == quote_char:
            self.position += 2  # avança as próximas duas aspas
            self.column += 2
            quote_char *= 3  # marca como aspas triplas
        
        while self.position < len(self.source_code):
            char = self.source_code[self.position]
            
            # se tiver uma barra invertida (escape), ignora o próximo caractere
            if char == '\\' and self.position + 1 < len(self.source_code):
                self.position += 2
                self.column += 2
                continue
                
            # se encontrar as aspas de fechamento, termina a string
            if char == quote_char:
                self.position += 1
                self.column += 1
                return Token(TokenType.STRING, self.source_code[start_pos:self.position], self.line, start_col)
                
            # se tiver uma nova linha, atualiza a linha e a coluna
            if char == '\n':
                self.line += 1
                self.column = 1
                self.current_line_start = self.position + 1
            else:
                self.column += 1
                
            self.position += 1

        # se não encontrou as aspas de fechamento, é um erro
        return Token(TokenType.ERROR, f"string não fechada: {self.source_code[start_pos:self.position]}", self.line, start_col)

    def match_operator(self):
        """tenta casar com um operador (e.g., +, -, ==, etc.)."""
        # ordena os operadores pelo tamanho pra pegar os maiores primeiro
        for op in sorted(self.OPERATORS, key=len, reverse=True):
            if self.source_code[self.position:self.position + len(op)] == op:
                token = Token(TokenType.OPERATOR, op, self.line, self.column)
                self.position += len(op)
                self.column += len(op)
                return token
        return None
    
    def get_current_line(self):
        """pega a linha atual do código (útil pra mensagens de erro)."""
        end = self.source_code.find('\n', self.current_line_start)
        if end == -1:
            end = len(self.source_code)
        return self.source_code[self.current_line_start:end]