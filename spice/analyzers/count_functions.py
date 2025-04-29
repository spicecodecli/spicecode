# this will count functions in the AST
from parser.ast import FunctionDefinition, Program, Node
from utils.get_lexer import get_lexer_for_file
import os

def count_functions(file_path):
    """Count function definitions in a file.
    
    Args:
        file_path (str): Path to the file to analyze
        
    Returns:
        int: Number of function definitions found
    """
    # Get the appropriate lexer for the file
    Lexer = get_lexer_for_file(file_path)
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Initialize lexer with source code
    lexer = Lexer(source_code=code)
    
    # Tokenize the code
    tokens = lexer.tokenize()
    
    # Parse the tokens into an AST
    from parser.parser import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    if not isinstance(ast, Program):
        return 0
    
    function_count = 0
    
    def search_node(node):
        nonlocal function_count
        
        # Check if this is a function definition
        if isinstance(node, FunctionDefinition):
            function_count += 1
        
        # Process child nodes based on their type
        if isinstance(node, Program):
            for statement in node.statements:
                search_node(statement)
        elif isinstance(node, FunctionDefinition):
            for statement in node.body:
                search_node(statement)
        elif hasattr(node, 'statements') and node.statements:
            for statement in node.statements:
                search_node(statement)
        elif hasattr(node, 'body') and node.body:
            for statement in node.body:
                search_node(statement)
        
        # Handle binary operations
        if hasattr(node, 'left'):
            search_node(node.left)
        if hasattr(node, 'right'):
            search_node(node.right)
        
        # Handle assignments
        if hasattr(node, 'value'):
            search_node(node.value)
            
        # Handle function call arguments
        if hasattr(node, 'arguments') and node.arguments:
            for arg in node.arguments:
                search_node(arg)
    
    # Start recursive search from the root Program node
    search_node(ast)
    
    return function_count