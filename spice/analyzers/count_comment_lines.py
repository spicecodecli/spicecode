# this will count comment lines for Python, JavaScript, Ruby, and Go
# COMMENT LINE IS A LINE THAT EXCLUSIVELY HAS A COMMENT
def count_comment_lines(code, lang):
    # split the code into lines
    lines = code.splitlines()
    comment_count = 0
    
    # Set language-specific comment markers
    if lang.lower() == "python":
        single_comment = "#"
        multi_start = '"""'
        alt_multi_start = "'''"
    elif lang.lower() == "javascript" or lang.lower() == "go":
        single_comment = "//"
        multi_start = "/*"
    elif lang.lower() == "ruby":
        single_comment = "#"
        multi_start = "=begin"
    else:
        raise ValueError(f"Unsupported language: {lang}")
    
    # Track if we're inside a multi-line comment
    in_multi_comment = False
    
    for line in lines:
        # Remove leading whitespace
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            continue
            
        # Handle multi-line comment blocks
        if in_multi_comment:
            comment_count += 1
            # Check for end of multi-line comment
            if lang == "python" and (stripped.endswith('"""') or stripped.endswith("'''")):
                in_multi_comment = False
            elif (lang == "javascript" or lang == "go") and "*/" in stripped:
                in_multi_comment = False
            elif lang == "ruby" and stripped == "=end":
                in_multi_comment = False
            continue
        
        # Check for start of multi-line comment
        if lang == "python" and (stripped.startswith('"""') or stripped.startswith("'''")):
            in_multi_comment = True
            comment_count += 1
            continue
        elif (lang == "javascript" or lang == "go") and stripped.startswith("/*"):
            in_multi_comment = True
            comment_count += 1
            continue
        elif lang == "ruby" and stripped == "=begin":
            in_multi_comment = True
            comment_count += 1
            continue
        
        # Check for single-line comments
        if stripped.startswith(single_comment):
            comment_count += 1
    
    return comment_count