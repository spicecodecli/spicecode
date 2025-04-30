# this will count inline comments, which are lines that have both code and comments
# INLINE COMMENT LINE IS A LINE THAT HAS BOTH CODE AND A COMMENT
# so like: y = 5 #sets y to 5 IS AN INLINE COMMENT LINE!!!!!!!!
from utils.get_lexer import get_lexer_for_file
from lexers.token import TokenType
import os

def count_inline_comments(file_path):
    """Count lines that have both code and comments in a file.
    
    Args:
        file_path (str): Path to the file to analyze
        
    Returns:
        int: Number of lines that have both code and comments
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
    
    # Count lines that have both code and comment tokens
    inline_comment_count = 0
    for line_num, line_tokens in tokens_by_line.items():
        has_comment = False
        has_code = False
        
        for token in line_tokens:
            if token.type == TokenType.COMMENT:
                has_comment = True
            elif token.type not in [TokenType.NEWLINE, TokenType.COMMENT]:
                has_code = True
        
        if has_comment and has_code:
            inline_comment_count += 1
    
    return inline_comment_count
