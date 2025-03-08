import os
from lexers.token import TokenType


from lexers.ruby.rubylexer import RubyLexer
from lexers.python.pythonlexer import PythonLexer
from lexers.javascript.javascriptlexer import JavaScriptLexer
from lexers.golang.golexer import GoLexer


def get_lexer_for_file(file_path):
    """Returns the appropriate lexer class based on file extension."""
    _, ext = os.path.splitext(file_path)
    if ext == ".rb":
        return RubyLexer
    elif ext == ".py":
        return PythonLexer
    elif ext == ".js":
        return JavaScriptLexer
    elif ext == ".go":
        return GoLexer
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

def analyze_file(file_path: str):
    """
    Analyzes a file and returns the analysis results.
    """
    # Import here to avoid circular imports
    from parser.parser import Parser
    from parser.ast import FunctionDefinition, Program
    
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()
    
    # Get the appropriate lexer for this file type
    LexerClass = get_lexer_for_file(file_path)
    
    # Tokenize the code
    lexer = LexerClass(code)
    tokens = lexer.tokenize()
    
    # Parse the tokens to get the AST
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Analyze the AST
    results = {
        "file_name": os.path.basename(file_path),
        "line_count": code.count("\n") + 1,
        "function_count": count_functions(ast),
        "comment_line_count": count_comment_lines(tokens)
    }
    
    return results

def count_functions(ast):
    """Count function definitions in the AST."""
    # Import here to avoid circular imports
    from parser.ast import FunctionDefinition, Program
    
    if not isinstance(ast, Program):
        return 0
    
    function_count = 0
    
    # Recursively search for function definitions in the AST
    def search_node(node):
        nonlocal function_count
        
        if isinstance(node, FunctionDefinition):
            function_count += 1
        
        # Process child nodes if they exist
        if hasattr(node, 'statements') and node.statements:
            for statement in node.statements:
                search_node(statement)
        
        if hasattr(node, 'body') and node.body:
            for body_statement in node.body:
                search_node(body_statement)
        
        # For BinaryOperation, check both sides
        if hasattr(node, 'left'):
            search_node(node.left)
        if hasattr(node, 'right'):
            search_node(node.right)
        
        # Check the value part of an assignment
        if hasattr(node, 'value'):
            search_node(node.value)
            
        # Check function call arguments
        if hasattr(node, 'arguments') and node.arguments:
            for arg in node.arguments:
                search_node(arg)
    
    # Start the recursive search from the root Program node
    search_node(ast)
    
    return function_count

def count_comment_lines(tokens):
    """Count comment lines directly from tokens."""
    comment_count = 0
    for token in tokens:
        if token.type == TokenType.COMMENT:
            comment_count += 1
    
    return comment_count