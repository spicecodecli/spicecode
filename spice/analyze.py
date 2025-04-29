import os

from spice.analyzers.identation import detect_indentation

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
        selected_stats = ["line_count", "function_count", "comment_line_count", "indentation_level"]

    # initialize results with the file name
    results = {
        "file_name": os.path.basename(file_path)
    }
    
    # read the code file only once and load it into memory
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()
    
    # line count if requested
    if "line_count" in selected_stats:
        from spice.analyzers.count_lines import count_lines
        results["line_count"] = count_lines(code)

    # comment line count if requested
    if "comment_line_count" in selected_stats:
        from spice.analyzers.count_comment_lines import count_comment_lines
        results["comment_line_count"] = count_comment_lines(code)

    # indentation analysis if requested
    if "indentation_level" in selected_stats:
        indentation_info = detect_indentation(code)
        results["indentation_type"] = indentation_info["indent_type"]
        results["indentation_size"] = indentation_info["indent_size"]
        results["indentation_levels"] = indentation_info["levels"]
    
    # only put the code through the lexer and proceed with tokenization if needed
    if any(stat in selected_stats for stat in ["function_count"]):
        # get the lexer for the code's language
        from utils.get_lexer import get_lexer_for_file
        LexerClass = get_lexer_for_file(file_path)
        
        # tokenize the code via lexer
        lexer = LexerClass(code)
        tokens = lexer.tokenize()
        
        # only put the code through the parser and proceed with parsing if needed
        if "function_count" in selected_stats:
            # import parser here to avoid circular import issues
            from parser.parser import Parser
            
            # parse tokens into AST
            parser = Parser(tokens)
            ast = parser.parse()
            
            # count functions
            from spice.analyzers.count_functions import count_functions
            results["function_count"] = count_functions(ast)
    
    return results
