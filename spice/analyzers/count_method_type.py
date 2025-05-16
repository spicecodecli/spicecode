import os 
import re

def count_method_type(path):
    """Count the number of private and public methods in a sample file."""
    _, ext = os.path.splitext(path)
    with open(path, 'r') as file:
        code = file.read()

    if ext == '.py':
        # Count the number of private and public methods
        pattern = r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(.*?\)\s*:\s*(?:#.*)?$'
        matches = re.findall(pattern, code, flags=re.MULTILINE)
        private_methods = [m for m in matches if m.startswith('_')]
        public_methods = [m for m in matches if not m.startswith('_')]
        return len(private_methods), len(public_methods)
    elif ext == '.js':
        # Count the number of private and public methods
        pattern = r'^\s*function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(.*?\)\s*{'
        matches = re.findall(pattern, code, flags=re.MULTILINE)
        private_methods = [m for m in matches if m.startswith('_')]
        public_methods = [m for m in matches if not m.startswith('_')]
        return len(private_methods), len(public_methods)
    elif ext == ".rb":
        # Count the number of private and public methods
        pattern = r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:#.*)?$'
        matches = re.findall(pattern, code, flags=re.MULTILINE)
        private_methods = [m for m in matches if m.startswith('_')]
        public_methods = [m for m in matches if not m.startswith('_')]
        return len(private_methods), len(public_methods)
    elif ext == ".go":
        # Count the number of private and public methods
        pattern = r'^\s*func\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(.*?\)\s*{'
        matches = re.findall(pattern, code, flags=re.MULTILINE)
        private_methods = [m for m in matches if m[0].islower()]
        public_methods = [m for m in matches if m[0].isupper()]
        return len(private_methods), len(public_methods)
    else:
        return 0, 0