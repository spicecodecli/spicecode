import os
import re

def count_comment_ratio(path):
    total_comments = 0
    total_lines = 0

    file_types = {
        '.py': {'single': [r'#'], 'multi': []},
        '.js': {'single': [r'//'], 'multi': [('/*', '*/')]},
        '.go': {'single': [r'//'], 'multi': [('/*', '*/')]},
        '.rb': {'single': [r'#'], 'multi': []},
    }

    def analyze_file(file_path, ext):
        nonlocal total_comments, total_lines
        single_patterns = [re.compile(pat) for pat in file_types[ext]['single']]
        multi_delims = file_types[ext]['multi']
        in_multiline = False

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    stripped = line.strip()
                    if not stripped:
                        continue  # ignora linha em branco
                    total_lines += 1

                    # Dentro de comentário multilinha
                    if in_multiline:
                        total_comments += 1
                        for _, end in multi_delims:
                            if end in stripped:
                                in_multiline = False
                        continue

                    # Início de comentário multilinha
                    found_multiline = False
                    for start, end in multi_delims:
                        if start in stripped:
                            total_comments += 1
                            found_multiline = True
                            if end not in stripped:
                                in_multiline = True
                            break
                    if found_multiline:
                        continue

                    # Comentário de linha única (ou inline)
                    if any(pat.search(line) for pat in single_patterns):
                        total_comments += 1
        except Exception as e:
            print(f"Erro ao ler arquivo: {file_path}, erro: {e}")

    if os.path.isfile(path):
        ext = os.path.splitext(path)[1]
        if ext in file_types:
            analyze_file(path, ext)
    else:
        for root, _, files in os.walk(path):
            for filename in files:
                ext = os.path.splitext(filename)[1]
                if ext in file_types:
                    analyze_file(os.path.join(root, filename), ext)

    if total_lines == 0:
        return "0.00%"

    percentage = (total_comments / total_lines) * 100
    return f"{percentage:.2f}%"
