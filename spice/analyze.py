import os
from typing import List, Dict, Optional, Union

from spice.analyzers.indentation import detect_indentation

def analyze_file(file_path: str, selected_stats: Optional[List[str]] = None) -> Dict[str, Union[int, str, List[int]]]:
    """
    Analyze a file and return only the requested stats.
    
    Args:
        file_path (str): Path to the file to analyze
        selected_stats (list, optional): List of stats to compute. If None, compute all stats.
            Valid stats are: "line_count", "function_count", "comment_line_count", 
            "inline_comment_count", "indentation_level"
    
    Returns:
        dict: Dictionary containing the requested stats and file information
    
    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If invalid stats are requested
        Exception: For other analysis errors
    """
    # Validate file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Validate file is a file (not a directory)
    if not os.path.isfile(file_path):
        raise ValueError(f"Path is not a file: {file_path}")
    
    # Validate file extension
    _, ext = os.path.splitext(file_path)
    if not ext:
        raise ValueError("File has no extension")
    
    # Define valid stats
    valid_stats = ["line_count", "function_count", "comment_line_count", "inline_comment_count", "indentation_level", "external_dependencies_count", "method_type_count", "comment_ratio"]
    
    # default to all stats if none specified
    if selected_stats is None:
        selected_stats = valid_stats
    else:
        # Validate requested stats
        invalid_stats = [stat for stat in selected_stats if stat not in valid_stats]
        if invalid_stats:
            raise ValueError(f"Invalid stats requested: {invalid_stats}. Valid stats are: {valid_stats}")

    # initialize results with the file information
    results = {
        "file_name": os.path.basename(file_path),
        "file_path": os.path.abspath(file_path),
        "file_size": os.path.getsize(file_path),
        "file_extension": ext
    }
    
    try:
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
            from utils.get_lexer import get_lexer_for_file
            LexerClass = get_lexer_for_file(file_path)
            lexer = LexerClass(source_code=code)  # Pass source_code explicitly
            results["comment_line_count"] = count_comment_lines(file_path)

        # inline comment count if requested
        if "inline_comment_count" in selected_stats:
            from spice.analyzers.count_inline_comments import count_inline_comments
            from utils.get_lexer import get_lexer_for_file
            LexerClass = get_lexer_for_file(file_path)
            lexer = LexerClass(source_code=code)  # Pass source_code explicitly
            results["inline_comment_count"] = count_inline_comments(file_path)

        # indentation analysis if requested
        if "indentation_level" in selected_stats:
            from spice.analyzers.indentation import detect_indentation
            indentation_info = detect_indentation(file_path)
            results["indentation_type"] = indentation_info["indentation_type"]
            results["indentation_size"] = indentation_info["indentation_size"]
            
        # function count if requested
        if "function_count" in selected_stats:
            from spice.analyzers.count_functions import count_functions
            results["function_count"] = count_functions(file_path)
        
        # external dependencies count if requested
        if "external_dependencies_count" in selected_stats:
            from spice.analyzers.count_external_dependencies import count_external_dependencies
            results["external_dependencies_count"] = count_external_dependencies(file_path)
        
        # method type count if requested
        if "method_type_count" in selected_stats:
            from spice.analyzers.count_method_type import count_method_type
            private_methods, public_methods = count_method_type(file_path)
            results["method_type_count"] = {
                "private": private_methods,
                "public": public_methods
            }

        # comment to code ratio if requested
        if "comment_ratio" in selected_stats:
            from spice.analyzers.count_comment_ratio import count_comment_ratio
            results["comment_ratio"] = count_comment_ratio(file_path)
        return results
        
    except Exception as e:
        # Add context to any errors that occur during analysis
        raise Exception(f"Error analyzing file {file_path}: {str(e)}")
