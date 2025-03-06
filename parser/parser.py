
from lexers.token import Token, TokenType
from parser.ast import (
    Program, Assignment, Identifier, Literal, BinaryOperation,
    FunctionDefinition, FunctionCall
)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        statements = []
        while self.position < len(self.tokens):
            # skip new lines
            if self.tokens[self.position].type == TokenType.NEWLINE:
                self.position += 1
                continue
                
            # check for eof end of file
            if self.tokens[self.position].type == TokenType.EOF:
                break
                
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
            else:
                # advance position if no statement was parsed
                # to avoid infinite loop
                # dont ask me how i know
                # please.
                self.position += 1
        
        return Program(statements)

    def parse_statement(self):
        """Parse a statement."""
        if self.position >= len(self.tokens):
            return None

        token = self.tokens[self.position]

        # function definitions
        if token.type == TokenType.KEYWORD and token.value == 'def':
            return self.parse_function_definition()

        # assignments
        if token.type == TokenType.IDENTIFIER:
            # check for function call
            if (self.position + 1 < len(self.tokens) and 
                self.tokens[self.position + 1].type != TokenType.OPERATOR):
                return self.parse_function_call()
                
            # check for assignment
            if (self.position + 1 < len(self.tokens) and 
                self.tokens[self.position + 1].type == TokenType.OPERATOR and 
                self.tokens[self.position + 1].value == '='):
                return self.parse_assignment()
            
            # indendeitifier alone
            identifier = Identifier(token.value)
            self.position += 1
            return identifier

        # can add more stuff here (if, while, etc.)

        return None  # return none if no valid statement is found

    def parse_function_definition(self):
        """Parse a function definition."""
        start_pos = self.position
        self.position += 1  # skip 'def'
        
        # expecting function name identifier
        if self.position < len(self.tokens) and self.tokens[self.position].type == TokenType.IDENTIFIER:
            function_name = self.tokens[self.position].value
            self.position += 1
            
            # parse parameters if any (TODO NOT WORKING YET)
            parameters = []
            
            # parse function body
            body_statements = []
            
            # skip newline after function declaration
            if self.position < len(self.tokens) and self.tokens[self.position].type == TokenType.NEWLINE:
                self.position += 1
            
            # parase statements until 'end'
            while self.position < len(self.tokens):
                if (self.tokens[self.position].type == TokenType.KEYWORD and
                    self.tokens[self.position].value == 'end'):
                    self.position += 1  # Skip the 'end'
                    break
                
                # skip newlines
                if self.tokens[self.position].type == TokenType.NEWLINE:
                    self.position += 1
                    continue
                
                statement = self.parse_statement()
                if statement:
                    body_statements.append(statement)
                else:
                    # if can't parse statement, advance to avoid infinite loop
                    # again, PLEASE do not ask how i know this
                    self.position += 1
            
            return FunctionDefinition(function_name, parameters, body_statements)
        
        # reset position if  can t't parse a valid function definition
        self.position = start_pos
        return None

    def parse_function_call(self):
        """Parse a function call."""
        function_name = self.tokens[self.position].value
        self.position += 1  # move past function name
        
        arguments = []
        
        # parse arguments
        while self.position < len(self.tokens) and self.tokens[self.position].type != TokenType.NEWLINE:
            arg = self.parse_expression()
            if arg:
                arguments.append(arg)
            else:
                break
        
        # skup newline
        if self.position < len(self.tokens) and self.tokens[self.position].type == TokenType.NEWLINE:
            self.position += 1
            
        return FunctionCall(function_name, arguments)

    def parse_assignment(self):
        """Parse an assignment statement."""
        variable_token = self.tokens[self.position]
        self.position += 1  # move past the identifier
        
        # check if next token is '='
        if self.position < len(self.tokens) and self.tokens[self.position].type == TokenType.OPERATOR and self.tokens[self.position].value == '=':
            self.position += 1  # move past the '=' op
            value = self.parse_expression()
            
            # skip newline
            if self.position < len(self.tokens) and self.tokens[self.position].type == TokenType.NEWLINE:
                self.position += 1
                
            return Assignment(variable_token.value, value)
        
        # if no equals sign, go back
        self.position -= 1
        return None

    def parse_expression(self):
        """Parse an expression."""
        if self.position >= len(self.tokens):
            return None
            
        # skip newlines
        if self.tokens[self.position].type == TokenType.NEWLINE:
            self.position += 1
            return None
            
        left = self.parse_term()
        if not left:
            return None
        
        while (self.position < len(self.tokens) and 
               self.tokens[self.position].type == TokenType.OPERATOR and
               self.tokens[self.position].value in ['+', '-', '*', '/']):
            operator = self.tokens[self.position]
            self.position += 1  # move past operator
            right = self.parse_term()
            if not right:
                break
            left = BinaryOperation(left, operator.value, right)
        
        return left

    def parse_term(self):
        """Parse terms like literals or identifiers."""
        if self.position >= len(self.tokens):
            return None
            
        token = self.tokens[self.position]
        
        # skip newlines
        if token.type == TokenType.NEWLINE:
            self.position += 1
            return None
            
        if token.type == TokenType.NUMBER:
            self.position += 1
            try:
                # try to convert to int first
                return Literal(int(token.value))
            except ValueError:
                # if it's not an int, try float
                return Literal(float(token.value))
        
        if token.type == TokenType.STRING:
            self.position += 1
            # remove quotes if present
            value = token.value
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            return Literal(value)
        
        if token.type == TokenType.IDENTIFIER:
            self.position += 1
            # handle Ruby boolean literals
            if token.value == 'true':
                return Literal(True)
            elif token.value == 'false':
                return Literal(False)
            elif token.value == 'nil':
                return Literal(None)
            return Identifier(token.value)
        
        if token.type == TokenType.SYMBOL:
            self.position += 1
            return Literal(token.value)  # handle symbols as literals
        
        return None  # return None for tokens with no current support maybe i could like print this so i know what tokens need support? does that make senes? TODO

    def expect(self, token_type, value=None):
        """Ensure the current token matches the expected type and value."""
        if self.position >= len(self.tokens):
            raise SyntaxError(f"Unexpected end of input, expected {token_type}")
            
        token = self.tokens[self.position]
        if token.type != token_type or (value is not None and token.value != value):
            raise SyntaxError(f"Expected {token_type} with value '{value}', but got {token}")