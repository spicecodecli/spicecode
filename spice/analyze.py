import os

# import utils
from spice.utils.get_lexer import get_lexer_for_file

# import analyzer functions from analyzers folder
from spice.analyzers.count_lines import count_lines
from spice.analyzers.count_comment_lines import count_comment_lines

# gustavo testando alguma coisa 
from spice.analyzers.identation import detect_indentation

    

# this is the analyze function
def analyze_file(file_path: str, selected_stats=None):
    """
    Analyze a file and return only the requested stats.
    
    Args:
        file_path (str): Path to the file to analyze
        selected_stats (list, optional): List of stats to compute. If None, compute all stats.
    
    Returns:
        dict: Dictionary containing the requested stats
    """
    # default to all stats if none specified
    if selected_stats is None:
        selected_stats = ["line_count", "function_count", "comment_line_count", "identation_level"]

    # initialize results with the file name (dont change this please)
    results = {
        "file_name": os.path.basename(file_path)
    }
    
    # read the code file only once and load it into memory
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()
    
    # line count if requested
    if "line_count" in selected_stats:
        results["line_count"] = count_lines(code)
    
    # only put the code through the lexer and proceed with tokenization if we need function count or comment count (UPDATE THIS WHEN  NEEDED PLEASE !!!!!!!!)
    if "function_count" in selected_stats or "comment_line_count" in selected_stats:
        # get the lexer for the code's language
        LexerClass = get_lexer_for_file(file_path)
        
        # tokenize the code via lexer
        lexer = LexerClass(code)
        tokens = lexer.tokenize()
        
        # process comment line count if requested
        if "comment_line_count" in selected_stats:
            results["comment_line_count"] = count_comment_lines(code)
        
        # only put the code through the parser and proceed with parsing if we need function count (UPDATE THIS WHEN  NEEDED PLEASE !!!!!!!!)
        if "function_count" in selected_stats:

            # import parser here to avoid error i still dont know why but it works
            from parser.parser import Parser
            
            # prase tokens into AST
            parser = Parser(tokens)
            ast = parser.parse()
            
            # count functions
            results["function_count"] = count_functions(ast)
        if "identation_level" in selected_stats:
            analyze_code_structure(code)
    
    return results



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


def analyze_code_structure(code):
    indentation_info = detect_indentation(code)

    print(f"Detected Indentation Type: {indentation_info['indent_type']}")
    print(f"Detected Indentation Size: {indentation_info['indent_size']}")
    for line, level in indentation_info["levels"]:
        # print(f"Indentation Level {level}: {line}")
        print(f"Detected Indentation Type: {indentation_info['indent_type']}")
        print(f"Detected Indentation Size: {indentation_info['indent_size']}")