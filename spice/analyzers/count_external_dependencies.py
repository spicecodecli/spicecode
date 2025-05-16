import os 
import re 

def count_external_dependencies(path):
    """Contar o número de dependências externas em um arquivo de exemplo."""
    _, ext = os.path.splitext(path)
    with open(path, 'r') as file:
        code = file.read()

    if ext == '.py':
        # Contar o número de importações
        pattern = r'^\s*(import\s+\w+|from\s+\w+\s+import\s+.+)'
        matches = re.findall(pattern, code, flags=re.MULTILINE)
        return len(matches)
    elif ext == '.js':
        # Contar o número de importações
        require_pattern = r'require\s*\(\s*[\'"][^\'"]+[\'"]\s*\)'
        import_pattern = r'^\s*import\s+.*from\s+[\'"][^\'"]+[\'"]'
        matches = re.findall(require_pattern, code)
        matches += re.findall(import_pattern, code, flags=re.MULTILINE)
        return len(matches)
    elif ext == ".rb":
        pattern = r'^\s*require(_relative)?\s+[\'"][^\'"]+[\'"]'
        matches = re.findall(pattern, code, flags=re.MULTILINE)
        return len(matches)
    elif ext == ".go":
        import_block_pattern = r'import\s*\((.*?)\)'
        single_import_pattern = r'^\s*import\s+[\'"][^\'"]+[\'"]'
        block = re.findall(import_block_pattern, code, flags=re.DOTALL)
        count = 0
        for b in block:
            count += len(re.findall(r'[\'"][^\'"]+[\'"]', b))
        count += len(re.findall(single_import_pattern, code, flags=re.MULTILINE))
        return count
    else:
        return 0