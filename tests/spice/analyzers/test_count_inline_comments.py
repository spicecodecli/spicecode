import os
import re
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.token import Token


def count_inline_comments(file_path):
    """
    Count inline comments in a source code file.
    
    An inline comment is a comment that appears on the same line as code,
    not on a line by itself.
    
    Args:
        file_path (str): Path to the source code file
        
    Returns:
        int: Number of inline comments found
        
    Raises:
        ValueError: If the file extension is not supported by Pygments
        FileNotFoundError: If the file doesn't exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        # Get the appropriate lexer for the file
        lexer = get_lexer_for_filename(file_path)
    except Exception:
        raise ValueError(f"Unsupported file extension: {file_path}")
    
    # Read the file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()
    
    if not content.strip():
        return 0
    
    # Tokenize the content
    tokens = list(lexer.get_tokens(content))
    
    # Group tokens by line
    lines = content.splitlines()
    line_tokens = {i + 1: [] for i in range(len(lines))}
    
    current_line = 1
    current_pos = 0
    
    for token_type, token_value in tokens:
        if token_value == '\n':
            current_line += 1
            current_pos = 0
        elif token_value:
            # Find which line this token belongs to
            token_lines = token_value.count('\n')
            if token_lines == 0:
                line_tokens[current_line].append((token_type, token_value))
            else:
                # Multi-line token
                parts = token_value.split('\n')
                for i, part in enumerate(parts):
                    if part:
                        line_tokens[current_line + i].append((token_type, part))
                current_line += token_lines
    
    inline_comment_count = 0
    
    # Check each line for inline comments
    for line_num, line_token_list in line_tokens.items():
        if not line_token_list:
            continue
            
        # Check if this line has both code and comments
        has_code = False
        has_comment = False
        
        for token_type, token_value in line_token_list:
            # Skip whitespace tokens
            if token_type in (Token.Text, Token.Text.Whitespace) and token_value.strip() == '':
                continue
            
            # Check if it's a comment token
            if token_type in Token.Comment:
                has_comment = True
            elif token_type not in (Token.Text, Token.Text.Whitespace):
                # Non-whitespace, non-comment token = code
                has_code = True
        
        # If the line has both code and comments, it contains an inline comment
        if has_code and has_comment:
            inline_comment_count += 1
    
    return inline_comment_count


# Alternative simpler implementation using regex patterns
def count_inline_comments_regex(file_path):
    """
    Alternative implementation using regex patterns for comment detection.
    This is simpler but less accurate than the Pygments-based approach.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Get file extension
    _, ext = os.path.splitext(file_path)
    
    # Define comment patterns for different languages
    comment_patterns = {
        '.py': r'#.*',
        '.js': r'//.*',
        '.go': r'//.*',
        '.rb': r'#.*',
        '.java': r'//.*',
        '.cpp': r'//.*',
        '.c': r'//.*',
        '.cs': r'//.*',
        '.php': r'//.*',
        '.swift': r'//.*',
        '.kt': r'//.*',
        '.scala': r'//.*',
    }
    
    if ext not in comment_patterns:
        raise ValueError(f"Unsupported file extension: {ext}")
    
    comment_pattern = comment_patterns[ext]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            lines = f.readlines()
    
    inline_comment_count = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Find comment in the line
        comment_match = re.search(comment_pattern, line)
        if comment_match:
            # Check if there's code before the comment
            code_before_comment = line[:comment_match.start()].strip()
            if code_before_comment:
                inline_comment_count += 1
    
    return inline_comment_count