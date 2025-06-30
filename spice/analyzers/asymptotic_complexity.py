# spice/analyzers/asymptotic_complexity.py
import os
import re
from collections import defaultdict

def analyze_asymptotic_complexity(file_path):
    """Analyze the asymptotic complexity of functions in a file.
    
    Args:
        file_path (str): Path to the file to analyze
        
    Returns:
        dict: Contains complexity analysis results
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    _, ext = os.path.splitext(file_path)
    
    if ext == '.py':
        return _analyze_python_complexity(code)
    elif ext == '.js':
        return _analyze_javascript_complexity(code)
    elif ext == '.rb':
        return _analyze_ruby_complexity(code)
    elif ext == '.go':
        return _analyze_go_complexity(code)
    else:
        return {'average_complexity': 'O(1)', 'complexity_distribution': {}}

def _analyze_python_complexity(code):
    """Analyze complexity of Python functions."""
    lines = code.split('\n')
    functions = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('def ') and '(' in line:
            func_name = re.search(r'def\s+(\w+)', line).group(1)
            start_line = i
            func_indent = len(lines[i]) - len(lines[i].lstrip())
            
            # Find function end
            end_line = len(lines)
            for j in range(i + 1, len(lines)):
                if lines[j].strip() == '':
                    continue
                current_indent = len(lines[j]) - len(lines[j].lstrip())
                if current_indent <= func_indent and lines[j].strip():
                    end_line = j
                    break
            
            func_code = '\n'.join(lines[start_line:end_line])
            complexity = _calculate_complexity(func_code)
            functions.append({
                'name': func_name,
                'complexity': complexity,
                'start_line': start_line + 1,
                'end_line': end_line
            })
            i = end_line
        else:
            i += 1
    
    return _summarize_complexity(functions)

def _analyze_javascript_complexity(code):
    """Analyze complexity of JavaScript functions."""
    lines = code.split('\n')
    functions = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Traditional functions
        func_match = re.search(r'function\s+(\w+)\s*\(', line)
        if func_match:
            func_name = func_match.group(1)
            start_line = i
            brace_count = line.count('{') - line.count('}')
            
            j = i + 1
            while j < len(lines) and brace_count > 0:
                brace_count += lines[j].count('{') - lines[j].count('}')
                j += 1
            
            func_code = '\n'.join(lines[start_line:j])
            complexity = _calculate_complexity(func_code)
            functions.append({
                'name': func_name,
                'complexity': complexity,
                'start_line': start_line + 1,
                'end_line': j
            })
            i = j
        # Arrow functions
        elif '=>' in line:
            arrow_match = re.search(r'(\w+)\s*=.*=>', line)
            if arrow_match:
                func_name = arrow_match.group(1)
                start_line = i
                
                if '{' in line:
                    brace_count = line.count('{') - line.count('}')
                    j = i + 1
                    while j < len(lines) and brace_count > 0:
                        brace_count += lines[j].count('{') - lines[j].count('}')
                        j += 1
                    end_line = j
                else:
                    end_line = i + 1
                
                func_code = '\n'.join(lines[start_line:end_line])
                complexity = _calculate_complexity(func_code)
                functions.append({
                    'name': func_name,
                    'complexity': complexity,
                    'start_line': start_line + 1,
                    'end_line': end_line
                })
            i += 1
        else:
            i += 1
    
    return _summarize_complexity(functions)

def _analyze_ruby_complexity(code):
    """Analyze complexity of Ruby functions."""
    lines = code.split('\n')
    functions = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        func_match = re.search(r'def\s+(\w+)', line)
        
        if func_match:
            func_name = func_match.group(1)
            start_line = i
            end_keywords = 1
            j = i + 1
            
            while j < len(lines) and end_keywords > 0:
                current_line = lines[j].strip()
                if re.match(r'(def|class|module|if|unless|while|until|for|begin|case)\s', current_line):
                    end_keywords += 1
                elif current_line == 'end':
                    end_keywords -= 1
                j += 1
            
            func_code = '\n'.join(lines[start_line:j])
            complexity = _calculate_complexity(func_code)
            functions.append({
                'name': func_name,
                'complexity': complexity,
                'start_line': start_line + 1,
                'end_line': j
            })
            i = j
        else:
            i += 1
    
    return _summarize_complexity(functions)

def _analyze_go_complexity(code):
    """Analyze complexity of Go functions."""
    lines = code.split('\n')
    functions = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        func_match = re.search(r'func\s+(\w+)\s*\(', line)
        
        if func_match:
            func_name = func_match.group(1)
            start_line = i
            brace_count = line.count('{') - line.count('}')
            
            j = i + 1
            while j < len(lines) and brace_count > 0:
                brace_count += lines[j].count('{') - lines[j].count('}')
                j += 1
            
            func_code = '\n'.join(lines[start_line:j])
            complexity = _calculate_complexity(func_code)
            functions.append({
                'name': func_name,
                'complexity': complexity,
                'start_line': start_line + 1,
                'end_line': j
            })
            i = j
        else:
            i += 1
    
    return _summarize_complexity(functions)

def _calculate_complexity(code):
    """Calculate the asymptotic complexity of a code block."""
    complexity_score = 1  # Base complexity O(1)
    
    # Count nested loops and conditionals
    loop_patterns = [
        r'\bfor\b',      # for loops
        r'\bwhile\b',    # while loops
        r'\bforeach\b',  # foreach (Ruby)
        r'\.each\b',     # .each (Ruby)
        r'\.map\b',      # .map 
        r'\.filter\b',   # .filter
        r'\.reduce\b'    # .reduce
    ]
    
    conditional_patterns = [
        r'\bif\b',
        r'\belse\b',
        r'\belif\b',
        r'\bunless\b',   # Ruby
        r'\bcase\b',
        r'\bswitch\b'
    ]
    
    recursive_patterns = [
        r'\breturn\s+\w+\(',  # potential recursion
    ]
    
    # Count nesting levels
    nesting_level = 0
    max_nesting = 0
    lines = code.split('\n')
    
    for line in lines:
        stripped = line.strip()
        
        # Check for loop patterns
        for pattern in loop_patterns:
            if re.search(pattern, stripped):
                complexity_score *= 2  # Each loop adds a factor
                nesting_level += 1
                break
        
        # Check for conditional patterns (less impact than loops)
        for pattern in conditional_patterns:
            if re.search(pattern, stripped):
                complexity_score += 1
                break
        
        # Check for recursion
        for pattern in recursive_patterns:
            if re.search(pattern, stripped):
                complexity_score *= 3  # Recursion significantly increases complexity
                break
        
        # Track nesting (simplified)
        if any(char in stripped for char in ['{', 'do']):
            nesting_level += 1
        if any(char in stripped for char in ['}', 'end']):
            nesting_level = max(0, nesting_level - 1)
        
        max_nesting = max(max_nesting, nesting_level)
    
    # Apply nesting multiplier
    if max_nesting > 2:
        complexity_score *= max_nesting
    
    # Map score to Big O notation
    if complexity_score <= 1:
        return 'O(1)'
    elif complexity_score <= 3:
        return 'O(log n)'
    elif complexity_score <= 10:
        return 'O(n)'
    elif complexity_score <= 25:
        return 'O(n log n)'
    elif complexity_score <= 50:
        return 'O(n²)'
    elif complexity_score <= 100:
        return 'O(n³)'
    else:
        return 'O(2^n)'

def _summarize_complexity(functions):
    """Summarize complexity analysis results."""
    if not functions:
        return {
            'average_complexity': 'O(1)',
            'complexity_distribution': {},
            'total_functions': 0
        }
    
    # Count complexity distribution
    complexity_counts = defaultdict(int)
    for func in functions:
        complexity_counts[func['complexity']] += 1
    
    # Calculate "average" complexity (most common)
    most_common_complexity = max(complexity_counts.items(), key=lambda x: x[1])[0]
    
    return {
        'average_complexity': most_common_complexity,
        'complexity_distribution': dict(complexity_counts),
        'total_functions': len(functions),
        'function_details': functions
    }