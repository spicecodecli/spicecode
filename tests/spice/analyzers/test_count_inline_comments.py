import os
import re


def count_inline_comments(file_path):
    """
    Count inline comments in a source code file using regex patterns.
    
    An inline comment is a comment that appears on the same line as code,
    not on a line by itself.
    
    Args:
        file_path (str): Path to the source code file
        
    Returns:
        int: Number of inline comments found
        
    Raises:
        ValueError: If the file extension is not supported
        FileNotFoundError: If the file doesn't exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Get file extension
    _, ext = os.path.splitext(file_path)
    
    # Define comment patterns for different languages
    comment_patterns = {
        '.py': r'#',
        '.js': r'//',
        '.go': r'//',
        '.rb': r'#',
        '.java': r'//',
        '.cpp': r'//',
        '.c': r'//',
        '.cs': r'//',
        '.php': r'//',
        '.swift': r'//',
        '.kt': r'//',
        '.scala': r'//',
        '.rs': r'//',
        '.ts': r'//',
        '.jsx': r'//',
        '.tsx': r'//',
    }
    
    if ext not in comment_patterns:
        raise ValueError(f"Unsupported file extension: {ext}")
    
    comment_marker = comment_patterns[ext]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()
    
    if not content.strip():
        return 0
    
    lines = content.splitlines()
    inline_comment_count = 0
    
    for line in lines:
        if _has_inline_comment(line, comment_marker):
            inline_comment_count += 1
    
    return inline_comment_count


def _has_inline_comment(line, comment_marker):
    """
    Check if a line has an inline comment (comment on same line as code).
    
    Args:
        line (str): The line to check
        comment_marker (str): The comment marker for the language (e.g., '//', '#')
        
    Returns:
        bool: True if the line has an inline comment, False otherwise
    """
    # Remove leading/trailing whitespace
    line = line.strip()
    
    # Empty line or line with only whitespace
    if not line:
        return False
    
    # Line starts with comment marker (full-line comment)
    if line.startswith(comment_marker):
        return False
    
    # Find comment marker in the line
    comment_index = line.find(comment_marker)
    
    # No comment marker found
    if comment_index == -1:
        return False
    
    # Check if there's non-whitespace code before the comment
    code_before_comment = line[:comment_index].strip()
    
    # Handle string literals that might contain comment markers
    if _is_comment_in_string(line, comment_index):
        return False
    
    # If there's code before the comment, it's an inline comment
    return bool(code_before_comment)


def _is_comment_in_string(line, comment_index):
    """
    Check if the comment marker is inside a string literal.
    This is a simplified check that handles basic cases.
    
    Args:
        line (str): The line to check
        comment_index (int): Index of the comment marker
        
    Returns:
        bool: True if the comment marker is likely inside a string
    """
    # Count quotes before the comment marker
    line_before_comment = line[:comment_index]
    
    # Count single and double quotes (basic check)
    single_quotes = line_before_comment.count("'")
    double_quotes = line_before_comment.count('"')
    
    # Simple heuristic: if odd number of quotes, we're likely inside a string
    # This is not perfect but handles most common cases
    in_single_quote_string = single_quotes % 2 == 1
    in_double_quote_string = double_quotes % 2 == 1
    
    return in_single_quote_string or in_double_quote_string


# More robust string detection (optional, more complex)
def _is_comment_in_string_robust(line, comment_index):
    """
    More robust check for comment markers inside strings.
    Handles escaped quotes and mixed quote types.
    """
    i = 0
    in_single_string = False
    in_double_string = False
    
    while i < comment_index:
        char = line[i]
        
        if char == '"' and not in_single_string:
            # Check if it's escaped
            if i == 0 or line[i-1] != '\\':
                in_double_string = not in_double_string
        elif char == "'" and not in_double_string:
            # Check if it's escaped
            if i == 0 or line[i-1] != '\\':
                in_single_string = not in_single_string
        
        i += 1
    
    return in_single_string or in_double_string