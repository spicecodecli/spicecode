"""
Abstract Syntax Tree (AST) node definitions for a simple programming language parser.
"""


class ASTNode:
    """Base class for all AST nodes."""
    pass


class Identifier(ASTNode):
    """Represents an identifier/variable name."""
    
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return f"<Identifier:{self.name}>"


class Literal(ASTNode):
    """Represents a literal value (number, string, boolean, etc.)."""
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return f"<Literal:{self.value}>"


class Assignment(ASTNode):
    """Represents an assignment statement (variable = value)."""
    
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value
    
    def __str__(self):
        return f"<Assignment:{self.variable} = {self.value}>"


class BinaryOperation(ASTNode):
    """Represents a binary operation (left operator right)."""
    
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __str__(self):
        return f"<BinaryOp:{self.left} {self.operator} {self.right}>"


class FunctionDefinition(ASTNode):
    """Represents a function definition."""
    
    def __init__(self, name, parameters=None, body=None):
        self.name = name
        self.parameters = parameters if parameters is not None else []
        self.body = body if body is not None else []
    
    def __str__(self):
        # Format parameters
        if self.parameters:
            params_str = ", ".join(str(param) for param in self.parameters)
        else:
            params_str = ""
        
        # Start with function signature
        result = f"<FunctionDef:{self.name}({params_str})>\n"
        
        # Add body statements with indentation
        for statement in self.body:
            result += f"    {statement}\n"
        
        # Remove trailing newline if there are body statements
        if self.body:
            result = result.rstrip('\n')
        
        return result


class FunctionCall(ASTNode):
    """Represents a function call."""
    
    def __init__(self, function, arguments=None):
        self.function = function
        self.arguments = arguments if arguments is not None else []
    
    def __str__(self):
        # Format arguments
        if self.arguments:
            args_str = ", ".join(str(arg) for arg in self.arguments)
        else:
            args_str = ""
        
        return f"<FunctionCall:{self.function}({args_str})>"


class Program(ASTNode):
    """Represents the root of the AST - a program containing statements."""
    
    def __init__(self, statements):
        self.statements = statements
    
    def __str__(self):
        result = "<Program>\n"
        
        # Add each statement with indentation
        for statement in self.statements:
            result += f"  {statement}\n"
        
        # Remove trailing newline if there are statements
        if self.statements:
            result = result.rstrip('\n')
        
        return result


# Additional utility functions for working with AST nodes

def pretty_print_ast(node, indent=0):
    """
    Pretty print an AST node with proper indentation.
    This is an alternative to the __str__ methods for more detailed output.
    """
    indent_str = "  " * indent
    
    if isinstance(node, Program):
        print(f"{indent_str}Program:")
        for stmt in node.statements:
            pretty_print_ast(stmt, indent + 1)
    
    elif isinstance(node, FunctionDefinition):
        params = ", ".join(param.name for param in node.parameters)
        print(f"{indent_str}FunctionDef: {node.name.name}({params})")
        for stmt in node.body:
            pretty_print_ast(stmt, indent + 1)
    
    elif isinstance(node, Assignment):
        print(f"{indent_str}Assignment:")
        print(f"{indent_str}  Variable:")
        pretty_print_ast(node.variable, indent + 2)
        print(f"{indent_str}  Value:")
        pretty_print_ast(node.value, indent + 2)
    
    elif isinstance(node, BinaryOperation):
        print(f"{indent_str}BinaryOp: {node.operator}")
        print(f"{indent_str}  Left:")
        pretty_print_ast(node.left, indent + 2)
        print(f"{indent_str}  Right:")
        pretty_print_ast(node.right, indent + 2)
    
    elif isinstance(node, FunctionCall):
        print(f"{indent_str}FunctionCall:")
        print(f"{indent_str}  Function:")
        pretty_print_ast(node.function, indent + 2)
        if node.arguments:
            print(f"{indent_str}  Arguments:")
            for arg in node.arguments:
                pretty_print_ast(arg, indent + 2)
    
    elif isinstance(node, Identifier):
        print(f"{indent_str}Identifier: {node.name}")
    
    elif isinstance(node, Literal):
        print(f"{indent_str}Literal: {node.value}")
    
    else:
        print(f"{indent_str}Unknown node type: {type(node)}")


def traverse_ast(node, visitor_func):
    """
    Traverse an AST and apply a visitor function to each node.
    The visitor function should accept a single node parameter.
    """
    visitor_func(node)
    
    if isinstance(node, Program):
        for stmt in node.statements:
            traverse_ast(stmt, visitor_func)
    
    elif isinstance(node, FunctionDefinition):
        traverse_ast(node.name, visitor_func)
        for param in node.parameters:
            traverse_ast(param, visitor_func)
        for stmt in node.body:
            traverse_ast(stmt, visitor_func)
    
    elif isinstance(node, Assignment):
        traverse_ast(node.variable, visitor_func)
        traverse_ast(node.value, visitor_func)
    
    elif isinstance(node, BinaryOperation):
        traverse_ast(node.left, visitor_func)
        traverse_ast(node.right, visitor_func)
    
    elif isinstance(node, FunctionCall):
        traverse_ast(node.function, visitor_func)
        for arg in node.arguments:
            traverse_ast(arg, visitor_func)


def find_identifiers(node):
    """
    Find all identifier names used in an AST.
    Returns a set of identifier names.
    """
    identifiers = set()
    
    def collect_identifier(n):
        if isinstance(n, Identifier):
            identifiers.add(n.name)
    
    traverse_ast(node, collect_identifier)
    return identifiers


def count_nodes_by_type(node):
    """
    Count the number of nodes of each type in an AST.
    Returns a dictionary with node type names as keys and counts as values.
    """
    counts = {}
    
    def count_node(n):
        node_type = type(n).__name__
        counts[node_type] = counts.get(node_type, 0) + 1
    
    traverse_ast(node, count_node)
    return counts