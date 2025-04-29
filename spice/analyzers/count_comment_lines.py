# this will count comment lines, since our AST/Parser doesn't include comment lines, this needs to be done in the tokenized output of the lexer
# not sure about that first line, im pretty sure like about 200% sure this is analyzing the raw code and not the tokenized code but ok
# COMMENT LINE IS A LINE THAT EXCLUSIVELY HAS A COMMENT
# so like: y = 5 #sets y to 5 IS NOT A COMMENT LINE!!!!!!!!
from utils.get_lexer import get_lexer_for_file
import os

def count_comment_lines(file_path):
    """Count lines that are exclusively comments in a file.
    
    Args:
        file_path (str): Path to the file to analyze
        
    Returns:
        int: Number of lines that are exclusively comments
    """
    # Get the appropriate lexer for the file
    Lexer = get_lexer_for_file(file_path)
    lexer = Lexer()
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Split into lines
    lines = code.splitlines()
    comment_count = 0
    
    for line in lines:
        # Remove leading/trailing whitespace
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            continue
            
        # Tokenize the line
        tokens = lexer.tokenize(stripped)
        
        # Check if the line consists only of comments
        is_comment_only = True
        for token in tokens:
            if token.type != 'Comment':
                is_comment_only = False
                break
                
        if is_comment_only:
            comment_count += 1
    
    return comment_count