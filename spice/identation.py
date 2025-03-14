import re

def detect_indentation(code):
    lines = code.split('\n')
    indentation_counts = {'tab': 0, 'space': 0}
    indentation_levels = []
    indent_sizes = {}

    for line in lines:
        if line.strip() == '':  # Skip empty lines
            continue
        
        leading_whitespace = re.match(r'^\s*', line).group()
        
        if '\t' in leading_whitespace:
            indentation_counts['tab'] += 1
        if ' ' in leading_whitespace:
            indentation_counts['space'] += 1
        if '\t' in leading_whitespace and ' ' in leading_whitespace:
            print(f"⚠ Identação mista detectada: {line}")

        indent_level = len(leading_whitespace)

        # Track indentation levels (ignoring zero indents)
        if indent_level > 0:
            indentation_levels.append((line.strip(), indent_level))
            indent_sizes[indent_level] = indent_sizes.get(indent_level, 0) + 1

    # Decide indentation type
    indent_type = 'tab' if indentation_counts['tab'] > indentation_counts['space'] else 'space'

    # Determine the most common indent size
    if indent_sizes:
        indent_size = max(indent_sizes, key=indent_sizes.get)
    else:
        indent_size = 4  # Default if no indentation found

    return {
        "indent_type": indent_type,
        "indent_size": indent_size,
        "levels": indentation_levels
    }
