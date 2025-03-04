

class Node:
    """Base class for all AST nodes."""
    pass

class Program(Node):
    """Root node representing the entire program."""
    def __init__(self, statements):
        self.statements = statements
    
    def __str__(self):
        return f"<Program>\n" + "\n".join(f"  {str(statement)}" for statement in self.statements)

class Identifier(Node):
    """Node representing a variable or function name."""
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return f"<Identifier:{self.name}>"

class Literal(Node):
    """Node representing a literal value (number, string, boolean, etc.)."""
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return f"<Literal:{self.value}>"

class Assignment(Node):
    """Node representing a variable assignment."""
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value
    
    def __str__(self):
        return f"<Assignment:{self.variable} = {self.value}>"

class BinaryOperation(Node):
    """Node representing a binary operation (e.g., addition, subtraction)."""
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __str__(self):
        return f"<BinaryOp:{self.left} {self.operator} {self.right}>"

class FunctionDefinition(Node):
    """Node representing a function definition."""
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters or []
        self.body = body or []
    
    def __str__(self):
        params_str = ", ".join(self.parameters)
        body_str = "\n".join(f"    {str(stmt)}" for stmt in self.body)
        return f"<FunctionDef:{self.name}({params_str})>\n{body_str}"

class FunctionCall(Node):
    """Node representing a function call."""
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments or []
    
    def __str__(self):
        args_str = ", ".join(str(arg) for arg in self.arguments)
        return f"<FunctionCall:{self.function}({args_str})>"