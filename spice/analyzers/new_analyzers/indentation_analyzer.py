import re

def analyze_indentation_levels(code_content):
    lines = code_content.split("\n")
    indentation_levels_per_line = []

    for i, line_text in enumerate(lines):
        stripped_line = line_text.strip()
        is_empty_or_whitespace_only = not bool(stripped_line)

        leading_whitespace_match = re.match(r"^(\s*)", line_text)
        leading_whitespace = ""
        if leading_whitespace_match:
            leading_whitespace = leading_whitespace_match.group(1)
        
        indent_level = len(leading_whitespace) # Each char (space or tab) counts as 1

        indentation_levels_per_line.append({
            "original_line_number": i + 1,
            "line_content": line_text,
            "stripped_line_content": stripped_line,
            "indent_level": indent_level,
            "is_empty_or_whitespace_only": is_empty_or_whitespace_only
        })

    return indentation_levels_per_line

