# ast.py

class Node:
    """Base class for all AST nodes."""
    def __repr__(self):
        return f"<{self.__class__.__name__}>"

class Program(Node):
    """Represents a whole Ruby program (top-level node)."""
    def __init__(self, statements):
        self.statements = statements  # List of statements in the program

class Statement(Node):
    """Represents a single statement in the program."""
    pass

class Expression(Node):
    """Represents a single expression."""
    pass

class Assignment(Statement):
    """Represents an assignment (e.g., variable = value)."""
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

class Identifier(Expression):
    """Represents an identifier (variable name)."""
    def __init__(self, name):
        self.name = name

class Literal(Expression):
    """Represents a literal value (number, string, etc.)."""
    def __init__(self, value):
        self.value = value

class BinaryOperation(Expression):
    """Represents a binary operation (e.g., a + b)."""
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
