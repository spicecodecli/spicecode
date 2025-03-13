import os 
import re

def detect_indentation(code):
    lines = code.split('\n')
    indentation_counts = {'tab': 0, 'space': 0}
    indentation_levels = []

    for line in lines:
        if line.strip() == '':
            continue  # skip empty lines
        leading_whitespace = re.match(r'^\s*', line).group()
        #detect space, tab or new line within the function
        if '\t' in leading_whitespace:
            indentation_counts['tab'] += 1
        if ' ' in leading_whitespace:
            indentation_counts['space'] += 1
        if '\t' in leading_whitespace and ' ' in leading_whitespace:
            print(f"Identação mista detectada: {line}")
        indent_level = len(leading_whitespace)
        indentation_levels.append((line.strip(), indent_level))

    indent_type = 'tab' if indentation_counts['tab'] > indentation_counts['space'] else 'space'
    # qual estilo de identaçao for mais frequente será enviado para a variavel 
    indent_size = 4  # tipo um padrao de identacao

    return {
        "indent_type": indent_type,
        "indent_size": indent_size,
        "levels": indentation_levels
    }
