import os

# this is the universal token, used by all lexers to know what to output
from lexers.token import TokenType

# this are the individual lexers for all languagues we support
from lexers.ruby.rubylexer import RubyLexer
from lexers.python.pythonlexer import PythonLexer
from lexers.javascript.javascriptlexer import JavaScriptLexer
from lexers.golang.golexer import GoLexer


# this will read the file extension and return the correct lexer
def get_lexer_for_file(file_path):

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
    


# this is the analyze functions
def analyze_file(file_path: str):

    # import parser here to avoid error idk why but it fixed it
    from parser.parser import Parser
    
    # read the code file and save it to memory
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()
    

    # get the lexer for the code's language
    LexerClass = get_lexer_for_file(file_path)
    

    # put the code through the lexer
    lexer = LexerClass(code)
    tokens = lexer.tokenize()
    

    # parse the output of the lexer (tokens) through the parse to get an AST
    parser = Parser(tokens)
    ast = parser.parse()
    

    # analyze the AST
    results = {
        "file_name": os.path.basename(file_path),
        "line_count": count_lines(code),
        "function_count": count_functions(ast),
        "comment_line_count": count_comment_lines(tokens)
    }
    
    # return the results above, they will each call their own function to do what they need to do and get the stats they refer to
    return results



# this will count lines straight from the raw code
def count_lines(code):
    return code.count("\n") + 1



# this will count functions in the AST
def count_functions(ast):

    # import function definition from the parser's ast
    from parser.ast import FunctionDefinition, Program
    
    if not isinstance(ast, Program):
        return 0
    
    function_count = 0
    
    # recursive search for function definitions in the AST
    def search_node(node):
        nonlocal function_count
        
        if isinstance(node, FunctionDefinition):
            function_count += 1
        
        # process child nodes if they exist
        if hasattr(node, 'statements') and node.statements:
            for statement in node.statements:
                search_node(statement)
        
        if hasattr(node, 'body') and node.body:
            for body_statement in node.body:
                search_node(body_statement)
        
        # for binary operation, check both sides
        if hasattr(node, 'left'):
            search_node(node.left)
        if hasattr(node, 'right'):
            search_node(node.right)
        
        # check the value part of an assignment
        if hasattr(node, 'value'):
            search_node(node.value)
            
        # check function call arguments
        if hasattr(node, 'arguments') and node.arguments:
            for arg in node.arguments:
                search_node(arg)
    
    # start recursive search from the root Program node
    search_node(ast)
    
    return function_count



# this will count comment lines, since our AST/Parser doesn't include comment lines, this needs to be done in the tokenized output of the lexer
def count_comment_lines(tokens):

    comment_count = 0

    for token in tokens:
        if token.type == TokenType.COMMENT:
            comment_count += 1
    
    return comment_count