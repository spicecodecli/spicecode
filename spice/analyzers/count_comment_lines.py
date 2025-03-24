# this will count comment lines, since our AST/Parser doesn't include comment lines, this needs to be done in the tokenized output of the lexer
# not sure about that first line, im pretty sure like about 200% sure this is analyzing the raw code and not the tokenized code but ok
# COMMENT LINE IS A LINE THAT EXCLUSIVELY HAS A COMMENT
# so like: y = 5 #sets y to 5 IS NOT A COMMENT LINE!!!!!!!!
def count_comment_lines(code):
    """Count lines that are exclusively comments (no code on the same line)"""
    # split the code into lines
    lines = code.splitlines()
    comment_count = 0
    
    for line in lines:
        # Remove leading whitespace
        stripped = line.strip()
        # Check if this line consists only of a comment
        if stripped and stripped.startswith('#'):
            comment_count += 1
    
    return comment_count