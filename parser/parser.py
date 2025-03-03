# parser/parser.py

from lexers.ruby.token import Token, TokenType
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
            # Skip newlines
            if self.tokens[self.position].type == TokenType.NEWLINE:
                self.position += 1
                continue
                
            # Check for EOF
            if self.tokens[self.position].type == TokenType.EOF:
                break
                
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
            else:
                # Important: advance position if no statement was parsed
                # to avoid infinite loop
                self.position += 1
        
        return Program(statements)

    def parse_statement(self):
        """Parse a statement."""
        if self.position >= len(self.tokens):
            return None

        token = self.tokens[self.position]

        # Handle function definitions
        if token.type == TokenType.KEYWORD and token.value == 'def':
            return self.parse_function_definition()

        # Handle assignments
        if token.type == TokenType.IDENTIFIER:
            # Check for function call
            if (self.position + 1 < len(self.tokens) and 
                self.tokens[self.position + 1].type != TokenType.OPERATOR):
                return self.parse_function_call()
                
            # Check for assignment
            if (self.position + 1 < len(self.tokens) and 
                self.tokens[self.position + 1].type == TokenType.OPERATOR and 
                self.tokens[self.position + 1].value == '='):
                return self.parse_assignment()
            
            # Just an identifier by itself
            identifier = Identifier(token.value)
            self.position += 1
            return identifier

        # Add more statement types as necessary (e.g., if, while, etc.)

        return None  # Return None if no valid statement is found

    def parse_function_definition(self):
        """Parse a function definition."""
        start_pos = self.position
        self.position += 1  # Skip 'def'
        
        # Expect function name identifier
        if self.position < len(self.tokens) and self.tokens[self.position].type == TokenType.IDENTIFIER:
            function_name = self.tokens[self.position].value
            self.position += 1
            
            # Parse parameters if any (not implemented yet)
            parameters = []
            
            # Parse function body
            body_statements = []
            
            # Skip newline after function declaration
            if self.position < len(self.tokens) and self.tokens[self.position].type == TokenType.NEWLINE:
                self.position += 1
            
            # Parse statements until 'end'
            while self.position < len(self.tokens):
                if (self.tokens[self.position].type == TokenType.KEYWORD and
                    self.tokens[self.position].value == 'end'):
                    self.position += 1  # Skip the 'end'
                    break
                
                # Skip newlines
                if self.tokens[self.position].type == TokenType.NEWLINE:
                    self.position += 1
                    continue
                
                statement = self.parse_statement()
                if statement:
                    body_statements.append(statement)
                else:
                    # If we can't parse a statement, advance to avoid infinite loop
                    self.position += 1
            
            return FunctionDefinition(function_name, parameters, body_statements)
        
        # Reset position if we couldn't parse a valid function definition
        self.position = start_pos
        return None

    def parse_function_call(self):
        """Parse a function call."""
        function_name = self.tokens[self.position].value
        self.position += 1  # move past the function name
        
        arguments = []
        
        # Parse arguments
        while self.position < len(self.tokens) and self.tokens[self.position].type != TokenType.NEWLINE:
            arg = self.parse_expression()
            if arg:
                arguments.append(arg)
            else:
                break
        
        # Skip newline
        if self.position < len(self.tokens) and self.tokens[self.position].type == TokenType.NEWLINE:
            self.position += 1
            
        return FunctionCall(function_name, arguments)

    def parse_assignment(self):
        """Parse an assignment statement."""
        variable_token = self.tokens[self.position]
        self.position += 1  # move past the identifier
        
        # Check if next token is '='
        if self.position < len(self.tokens) and self.tokens[self.position].type == TokenType.OPERATOR and self.tokens[self.position].value == '=':
            self.position += 1  # move past the '=' operator
            value = self.parse_expression()
            
            # Skip newline
            if self.position < len(self.tokens) and self.tokens[self.position].type == TokenType.NEWLINE:
                self.position += 1
                
            return Assignment(variable_token.value, value)
        
        # If no equals sign, go back
        self.position -= 1
        return None

    def parse_expression(self):
        """Parse an expression."""
        if self.position >= len(self.tokens):
            return None
            
        # Skip newlines
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
        
        # Skip newlines
        if token.type == TokenType.NEWLINE:
            self.position += 1
            return None
            
        if token.type == TokenType.NUMBER:
            self.position += 1
            try:
                # Try to convert to int first
                return Literal(int(token.value))
            except ValueError:
                # If it's not an int, try float
                return Literal(float(token.value))
        
        if token.type == TokenType.STRING:
            self.position += 1
            # Remove quotes if present
            value = token.value
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            return Literal(value)
        
        if token.type == TokenType.IDENTIFIER:
            self.position += 1
            # Handle Ruby boolean literals
            if token.value == 'true':
                return Literal(True)
            elif token.value == 'false':
                return Literal(False)
            elif token.value == 'nil':
                return Literal(None)
            return Identifier(token.value)
        
        if token.type == TokenType.SYMBOL:
            self.position += 1
            return Literal(token.value)  # Handle symbols as literals
        
        return None  # Return None for tokens we can't handle yet

    def expect(self, token_type, value=None):
        """Ensure the current token matches the expected type and value."""
        if self.position >= len(self.tokens):
            raise SyntaxError(f"Unexpected end of input, expected {token_type}")
            
        token = self.tokens[self.position]
        if token.type != token_type or (value is not None and token.value != value):
            raise SyntaxError(f"Expected {token_type} with value '{value}', but got {token}")