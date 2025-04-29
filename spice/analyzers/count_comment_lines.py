# this will count comment lines, since our AST/Parser doesn't include comment lines, this needs to be done in the tokenized output of the lexer
# not sure about that first line, im pretty sure like about 200% sure this is analyzing the raw code and not the tokenized code but ok
# COMMENT LINE IS A LINE THAT EXCLUSIVELY HAS A COMMENT
# so like: y = 5 #sets y to 5 IS NOT A COMMENT LINE!!!!!!!!
from utils.get_lexer import get_lexer_for_file
from lexers.token import TokenType
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
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Initialize lexer with source code
    lexer = Lexer(source_code=code)
    
    # Get all tokens
    tokens = lexer.tokenize()
    
    # Group tokens by line number
    tokens_by_line = {}
    for token in tokens:
        if token.line not in tokens_by_line:
            tokens_by_line[token.line] = []
        tokens_by_line[token.line].append(token)
    
    # Count lines that only have comment tokens (and possibly newlines)
    comment_count = 0
    for line_num, line_tokens in tokens_by_line.items():
        has_comment = False
        has_non_comment = False
        
        for token in line_tokens:
            if token.type == TokenType.COMMENT:
                has_comment = True
            elif token.type != TokenType.NEWLINE:
                has_non_comment = True
                break
        
        if has_comment and not has_non_comment:
            comment_count += 1
    
    return comment_count