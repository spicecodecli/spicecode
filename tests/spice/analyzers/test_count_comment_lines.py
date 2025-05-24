import os
import re


def count_comment_lines(file_path):
    """
    Count full-line comments in a source code file using regex patterns.
    
    A full-line comment is a line that contains only a comment (and possibly whitespace),
    not a line that has both code and a comment.
    
    Args:
        file_path (str): Path to the source code file
        
    Returns:
        int: Number of full-line comments found
        
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
    comment_line_count = 0
    
    for line in lines:
        if _is_full_line_comment(line, comment_marker):
            comment_line_count += 1
    
    return comment_line_count


def _is_full_line_comment(line, comment_marker):
    """
    Check if a line is a full-line comment (contains only comment and whitespace).
    
    Args:
        line (str): The line to check
        comment_marker (str): The comment marker for the language (e.g., '//', '#')
        
    Returns:
        bool: True if the line is a full-line comment, False otherwise
    """
    # Strip whitespace from the line
    stripped_line = line.strip()
    
    # Empty line
    if not stripped_line:
        return False
    
    # Line starts with comment marker (this is a full-line comment)
    if stripped_line.startswith(comment_marker):
        return True
    
    return False


def _is_multiline_comment_start(line, language_ext):
    """
    Check if a line starts a multi-line comment block.
    Currently handles basic cases for languages that support multi-line comments.
    
    Args:
        line (str): The line to check
        language_ext (str): File extension to determine language
        
    Returns:
        bool: True if line starts a multi-line comment
    """
    stripped = line.strip()
    
    # Languages with /* */ style multi-line comments
    if language_ext in ['.js', '.go', '.java', '.cpp', '.c', '.cs', '.php', '.swift', '.kt', '.scala', '.rs', '.ts', '.jsx', '.tsx']:
        return stripped.startswith('/*')
    
    # Python has """ or ''' for docstrings/multi-line strings
    elif language_ext == '.py':
        return stripped.startswith('"""') or stripped.startswith("'''")
    
    return False


def _is_multiline_comment_end(line, language_ext):
    """
    Check if a line ends a multi-line comment block.
    
    Args:
        line (str): The line to check
        language_ext (str): File extension to determine language
        
    Returns:
        bool: True if line ends a multi-line comment
    """
    stripped = line.strip()
    
    # Languages with /* */ style multi-line comments
    if language_ext in ['.js', '.go', '.java', '.cpp', '.c', '.cs', '.php', '.swift', '.kt', '.scala', '.rs', '.ts', '.jsx', '.tsx']:
        return stripped.endswith('*/')
    
    # Python docstrings
    elif language_ext == '.py':
        return stripped.endswith('"""') or stripped.endswith("'''")
    
    return False


def count_comment_lines_with_multiline(file_path):
    """
    Enhanced version that also counts multi-line comment blocks.
    Each line within a multi-line comment block is counted as a comment line.
    
    Args:
        file_path (str): Path to the source code file
        
    Returns:
        int: Number of comment lines (including multi-line comments)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Get file extension
    _, ext = os.path.splitext(file_path)
    
    # Define single-line comment patterns
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
    comment_line_count = 0
    in_multiline_comment = False
    
    for line in lines:
        stripped_line = line.strip()
        
        # Skip empty lines
        if not stripped_line:
            continue
        
        # Check for multi-line comment start
        if not in_multiline_comment and _is_multiline_comment_start(line, ext):
            in_multiline_comment = True
            comment_line_count += 1
            # Check if it also ends on the same line
            if _is_multiline_comment_end(line, ext) and stripped_line != '/**/':
                in_multiline_comment = False
            continue
        
        # Check for multi-line comment end
        if in_multiline_comment:
            comment_line_count += 1
            if _is_multiline_comment_end(line, ext):
                in_multiline_comment = False
            continue
        
        # Check for single-line comments
        if _is_full_line_comment(line, comment_marker):
            comment_line_count += 1
    
    return comment_line_count