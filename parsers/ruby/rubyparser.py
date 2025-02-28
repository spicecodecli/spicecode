import re

# Token specification for a subset of Ruby
token_specification = [
    ('NUMBER',   r'\d+(\.\d*)?'),     # Integer or decimal number
    ('DEF',      r'\bdef\b'),         # def keyword
    ('END',      r'\bend\b'),         # end keyword
    ('IF',       r'\bif\b'),          # if keyword
    ('ELSE',     r'\belse\b'),        # else keyword
    ('IDENT',    r'[A-Za-z_]\w*'),     # Identifiers
    ('LPAREN',   r'\('),              # Left parenthesis
    ('RPAREN',   r'\)'),              # Right parenthesis
    ('OP',       r'[+\-*/=]'),        # Operators: +, -, *, /, =
    ('NEWLINE',  r'\n'),              # Newline
    ('SKIP',     r'[ \t]+'),          # Skip spaces and tabs
    ('MISMATCH', r'.'),               # Any other character
]

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, col={self.column})"

class Lexer:
    def __init__(self, code):
        self.code = code
    def tokenize(self):
        tokens = []
        line_num = 1
        line_start = 0
        regex_parts = []
        for name, pattern in token_specification:
            regex_parts.append(f"(?P<{name}>{pattern})")
        regex = re.compile('|'.join(regex_parts))
        for mo in regex.finditer(self.code):
            kind = mo.lastgroup
            value = mo.group(kind)
            column = mo.start() - line_start
            if kind == 'NUMBER':
                # Convert numeric tokens into proper numbers
                value = float(value) if '.' in value else int(value)
                tokens.append(Token(kind, value, line_num, column))
            elif kind in ('DEF', 'END', 'IF', 'ELSE', 'IDENT', 'LPAREN', 'RPAREN', 'OP'):
                tokens.append(Token(kind, value, line_num, column))
            elif kind == 'NEWLINE':
                line_num += 1
                line_start = mo.end()
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Unexpected character {value!r} on line {line_num}')
        tokens.append(Token('EOF', '', line_num, 0))
        return tokens

# ---------------- AST Node Definitions ----------------

class ProgramNode:
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"Program({self.statements})"

class FunctionDefNode:
    def __init__(self, name, body):
        self.name = name
        self.body = body
    def __repr__(self):
        return f"FunctionDef(name={self.name}, body={self.body})"

class IfNode:
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body
    def __repr__(self):
        return f"If(condition={self.condition}, then={self.then_body}, else={self.else_body})"

class AssignmentNode:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
    def __repr__(self):
        return f"Assign({self.identifier} = {self.expression})"

class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"BinOp({self.left} {self.op} {self.right})"

class NumberNode:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Number({self.value})"

class IdentifierNode:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Identifier({self.name})"

# ---------------- Parser (Recursive Descent) ----------------

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[self.pos]
    
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.pos += 1
            self.current_token = self.tokens[self.pos]
        else:
            raise Exception(f"Unexpected token: expected {token_type}, got {self.current_token.type}")

    def peek(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        else:
            return Token('EOF', '', self.current_token.line, self.current_token.column)

    def parse(self):
        statements = []
        while self.current_token.type != 'EOF':
            stmt = self.statement()
            statements.append(stmt)
        return ProgramNode(statements)

    def statement(self):
        if self.current_token.type == 'DEF':
            return self.function_def()
        elif self.current_token.type == 'IF':
            return self.if_statement()
        # For this simple parser, an assignment is detected when an identifier is
        # followed by an '=' operator.
        elif self.current_token.type == 'IDENT' and self.peek().type == 'OP' and self.peek().value == '=':
            return self.assignment()
        else:
            return self.expression_statement()

    def function_def(self):
        self.eat('DEF')
        if self.current_token.type != 'IDENT':
            raise Exception("Expected function name after 'def'")
        func_name = self.current_token.value
        self.eat('IDENT')
        body = []
        while self.current_token.type != 'END' and self.current_token.type != 'EOF':
            body.append(self.statement())
        self.eat('END')
        return FunctionDefNode(func_name, body)

    def if_statement(self):
        self.eat('IF')
        condition = self.expression()
        then_body = []
        while self.current_token.type not in ('ELSE', 'END', 'EOF'):
            then_body.append(self.statement())
        else_body = None
        if self.current_token.type == 'ELSE':
            self.eat('ELSE')
            else_body = []
            while self.current_token.type not in ('END', 'EOF'):
                else_body.append(self.statement())
        self.eat('END')
        return IfNode(condition, then_body, else_body)

    def assignment(self):
        ident = IdentifierNode(self.current_token.value)
        self.eat('IDENT')
        if self.current_token.type == 'OP' and self.current_token.value == '=':
            self.eat('OP')
        else:
            raise Exception("Expected '=' in assignment")
        expr = self.expression()
        return AssignmentNode(ident, expr)

    def expression_statement(self):
        return self.expression()

    # Parsing arithmetic expressions (supports +, -, *, /)
    def expression(self):
        node = self.term()
        while self.current_token.type == 'OP' and self.current_token.value in ('+', '-'):
            op = self.current_token.value
            self.eat('OP')
            right = self.term()
            node = BinOpNode(node, op, right)
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type == 'OP' and self.current_token.value in ('*', '/'):
            op = self.current_token.value
            self.eat('OP')
            right = self.factor()
            node = BinOpNode(node, op, right)
        return node

    def factor(self):
        token = self.current_token
        if token.type == 'NUMBER':
            self.eat('NUMBER')