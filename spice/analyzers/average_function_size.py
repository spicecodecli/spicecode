# spice/analyzers/average_function_size.py
import os
import re
from utils.get_lexer import get_lexer_for_file

def calculate_average_function_size(file_path):
    """Calculate the average size (in lines) of functions in a file.
    
    Args:
        file_path (str): Path to the file to analyze
        
    Returns:
        float: Average number of lines per function, or 0 if no functions found
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    _, ext = os.path.splitext(file_path)
    
    if ext == '.py':
        return _analyze_python_functions(code)
    elif ext == '.js':
        return _analyze_javascript_functions(code)
    elif ext == '.rb':
        return _analyze_ruby_functions(code)
    elif ext == '.go':
        return _analyze_go_functions(code)
    else:
        return 0.0

def _analyze_python_functions(code):
    """Analyze Python functions and calculate average size."""
    lines = code.split('\n')
    functions = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Find function definitions
        if stripped.startswith('def ') and '(' in line:
            start_line = i
            # Find the indentation level of the function
            func_indent = len(line) - len(line.lstrip())
            
            # Find the end of the function
            end_line = len(lines)
            for j in range(i + 1, len(lines)):
                current_line = lines[j]
                if current_line.strip() == '':
                    continue
                current_indent = len(current_line) - len(current_line.lstrip())
                # Function ends when we find a line with same or less indentation
                if current_indent <= func_indent and current_line.strip():
                    end_line = j
                    break
            
            function_size = end_line - start_line
            functions.append(function_size)
    
    return sum(functions) / len(functions) if functions else 0.0

def _analyze_javascript_functions(code):
    """Analyze JavaScript functions and calculate average size."""
    lines = code.split('\n')
    functions = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Traditional function declarations
        if re.match(r'function\s+\w+\s*\(', line) or re.match(r'function\s*\(', line):
            start_line = i
            brace_count = line.count('{') - line.count('}')
            
            # Find the closing brace
            j = i + 1
            while j < len(lines) and brace_count > 0:
                brace_count += lines[j].count('{') - lines[j].count('}')
                j += 1
            
            function_size = j - start_line
            functions.append(function_size)
            i = j
        # Arrow functions
        elif '=>' in line:
            start_line = i
            if '{' in line:
                brace_count = line.count('{') - line.count('}')
                j = i + 1
                while j < len(lines) and brace_count > 0:
                    brace_count += lines[j].count('{') - lines[j].count('}')
                    j += 1
                function_size = j - start_line
            else:
                function_size = 1  # Single line arrow function
            functions.append(function_size)
            i += 1
        else:
            i += 1
    
    return sum(functions) / len(functions) if functions else 0.0

def _analyze_ruby_functions(code):
    """Analyze Ruby functions and calculate average size."""
    lines = code.split('\n')
    functions = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Method definitions
        if re.match(r'def\s+\w+', line):
            start_line = i
            # Find the corresponding 'end'
            end_keywords = 1
            j = i + 1
            
            while j < len(lines) and end_keywords > 0:
                current_line = lines[j].strip()
                # Count def, class, module, if, while, etc. that need 'end'
                if re.match(r'(def|class|module|if|unless|while|until|for|begin|case)\s', current_line):
                    end_keywords += 1
                elif current_line == 'end':
                    end_keywords -= 1
                j += 1
            
            function_size = j - start_line
            functions.append(function_size)
            i = j
        else:
            i += 1
    
    return sum(functions) / len(functions) if functions else 0.0

def _analyze_go_functions(code):
    """Analyze Go functions and calculate average size."""
    lines = code.split('\n')
    functions = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Function declarations
        if re.match(r'func\s+(\w+\s*)?\(', line) or re.match(r'func\s*\([^)]*\)\s*\w+\s*\(', line):
            start_line = i
            brace_count = line.count('{') - line.count('}')
            
            # Find the closing brace
            j = i + 1
            while j < len(lines) and brace_count > 0:
                brace_count += lines[j].count('{') - lines[j].count('}')
                j += 1
            
            function_size = j - start_line
            functions.append(function_size)
            i = j
        else:
            i += 1
    
    return sum(functions) / len(functions) if functions else 0.0