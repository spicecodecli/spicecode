import os
import re


def count_comment_ratio(file_or_dir_path):
    """
    Calculate the comment ratio for a file or directory.
    
    The ratio is calculated as: (total comment lines / total non-empty lines) * 100
    
    For directories, analyzes all supported files and combines the counts.
    
    Args:
        file_or_dir_path (str): Path to a file or directory
        
    Returns:
        str: Comment ratio as a percentage string (e.g., "75.50%")
    """
    if os.path.isfile(file_or_dir_path):
        return _calculate_file_ratio(file_or_dir_path)
    elif os.path.isdir(file_or_dir_path):
        return _calculate_directory_ratio(file_or_dir_path)
    else:
        return "0.00%"


def _calculate_file_ratio(file_path):
    """Calculate comment ratio for a single file."""
    try:
        total_comments, total_lines = _count_comments_and_lines(file_path)
        
        if total_lines == 0:
            return "0.00%"
        
        ratio = (total_comments / total_lines) * 100
        return f"{ratio:.2f}%"
    
    except (ValueError, FileNotFoundError):
        # Unsupported file type or file doesn't exist
        return "0.00%"


def _calculate_directory_ratio(dir_path):
    """Calculate comment ratio for all supported files in a directory."""
    total_comments = 0
    total_lines = 0
    
    supported_extensions = {'.py', '.js', '.go', '.rb', '.java', '.cpp', '.c', '.cs', 
                          '.php', '.swift', '.kt', '.scala', '.rs', '.ts', '.jsx', '.tsx'}
    
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(filename)
            
            if ext in supported_extensions:
                try:
                    file_comments, file_lines = _count_comments_and_lines(file_path)
                    total_comments += file_comments
                    total_lines += file_lines
                except (ValueError, FileNotFoundError):
                    # Skip unsupported or problematic files
                    continue
    
    if total_lines == 0:
        return "0.00%"
    
    ratio = (total_comments / total_lines) * 100
    return f"{ratio:.2f}%"


def _count_comments_and_lines(file_path):
    """
    Count total comment lines and total non-empty lines in a file.
    
    Returns:
        tuple: (comment_lines, total_non_empty_lines)
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
        return 0, 0
    
    lines = content.splitlines()
    
    comment_lines = 0
    total_non_empty_lines = 0
    in_multiline_comment = False
    
    for line in lines:
        stripped_line = line.strip()
        
        # Skip completely empty lines
        if not stripped_line:
            continue
        
        total_non_empty_lines += 1
        
        # Handle multi-line comments for supported languages
        if _is_multiline_comment_start(line, ext):
            in_multiline_comment = True
            comment_lines += 1
            # Check if it also ends on the same line (e.g., /* comment */)
            if _is_multiline_comment_end(line, ext) and not _is_single_line_multiline_comment(line, ext):
                in_multiline_comment = False
            continue
        
        # If we're inside a multi-line comment
        if in_multiline_comment:
            comment_lines += 1
            if _is_multiline_comment_end(line, ext):
                in_multiline_comment = False
            continue
        
        # Check for full-line comments (lines that start with comment marker)
        if stripped_line.startswith(comment_marker):
            comment_lines += 1
            continue
        
        # Check for inline comments (lines with code AND comments)
        if _has_inline_comment(line, comment_marker):
            comment_lines += 1
            continue
    
    return comment_lines, total_non_empty_lines


def _is_multiline_comment_start(line, language_ext):
    """Check if a line starts a multi-line comment block."""
    stripped = line.strip()
    
    # Languages with /* */ style multi-line comments
    if language_ext in ['.js', '.go', '.java', '.cpp', '.c', '.cs', '.php', '.swift', '.kt', '.scala', '.rs', '.ts', '.jsx', '.tsx']:
        return stripped.startswith('/*')
    
    # Python has """ or ''' for docstrings/multi-line strings
    elif language_ext == '.py':
        return stripped.startswith('"""') or stripped.startswith("'''")
    
    return False


def _is_multiline_comment_end(line, language_ext):
    """Check if a line ends a multi-line comment block."""
    stripped = line.strip()
    
    # Languages with /* */ style multi-line comments
    if language_ext in ['.js', '.go', '.java', '.cpp', '.c', '.cs', '.php', '.swift', '.kt', '.scala', '.rs', '.ts', '.jsx', '.tsx']:
        return stripped.endswith('*/')
    
    # Python docstrings
    elif language_ext == '.py':
        return stripped.endswith('"""') or stripped.endswith("'''")
    
    return False


def _is_single_line_multiline_comment(line, language_ext):
    """Check if a line is a single-line multi-line comment (e.g., /* comment */)."""
    stripped = line.strip()
    
    if language_ext in ['.js', '.go', '.java', '.cpp', '.c', '.cs', '.php', '.swift', '.kt', '.scala', '.rs', '.ts', '.jsx', '.tsx']:
        return stripped.startswith('/*') and stripped.endswith('*/')
    
    elif language_ext == '.py':
        return ((stripped.startswith('"""') and stripped.endswith('"""') and len(stripped) > 6) or
                (stripped.startswith("'''") and stripped.endswith("'''") and len(stripped) > 6))
    
    return False


def _has_inline_comment(line, comment_marker):
    """Check if a line has an inline comment (comment on same line as code)."""
    stripped_line = line.strip()
    
    # Empty line or line with only whitespace
    if not stripped_line:
        return False
    
    # Line starts with comment marker (full-line comment, not inline)
    if stripped_line.startswith(comment_marker):
        return False
    
    # Find comment marker in the line
    comment_index = stripped_line.find(comment_marker)
    
    # No comment marker found
    if comment_index == -1:
        return False
    
    # Check if there's non-whitespace code before the comment
    code_before_comment = stripped_line[:comment_index].strip()
    
    # Handle string literals that might contain comment markers
    if _is_comment_in_string(stripped_line, comment_index):
        return False
    
    # If there's code before the comment, it's an inline comment
    return bool(code_before_comment)


def _is_comment_in_string(line, comment_index):
    """Check if the comment marker is inside a string literal."""
    line_before_comment = line[:comment_index]
    
    # Count single and double quotes (basic check)
    single_quotes = line_before_comment.count("'")
    double_quotes = line_before_comment.count('"')
    
    # Simple heuristic: if odd number of quotes, we're likely inside a string
    in_single_quote_string = single_quotes % 2 == 1
    in_double_quote_string = double_quotes % 2 == 1
    
    return in_single_quote_string or in_double_quote_string