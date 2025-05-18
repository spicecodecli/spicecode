import os
import re

def count_comment_to_code_ratio(path):
    total_comments = 0
    total_lines = 0

    file_types = {
        '.py': {'single': [r'#'], 'multi': []},
        '.js': {'single': [r'//'], 'multi': [("/*", "*/")]},
        '.go': {'single': [r'//'], 'multi': [("/*", "*/")]},
        '.rb': {'single': [r'#'], 'multi': []},
    }

    def analyze_file(file_path, ext):
        nonlocal total_comments, total_lines
        single_comment_patterns = [re.compile(rf'{pat}') for pat in file_types[ext]['single']]
        multi_comment_delims = file_types[ext]['multi']
        in_multiline_comment = False

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                total_lines += 1
                stripped = line.strip()
                # Multi-line comment handling
                if multi_comment_delims:
                    if in_multiline_comment:
                        total_comments += 1
                        for _, end in multi_comment_delims:
                            if end in stripped:
                                in_multiline_comment = False
                        continue
                    for start, end in multi_comment_delims:
                        if start in stripped:
                            total_comments += 1
                            if end not in stripped:
                                in_multiline_comment = True
                            break
                    else:
                        # Single/inline comment
                        if any(pat.search(line) for pat in single_comment_patterns):
                            total_comments += 1
                else:
                    # Only single/inline comments
                    if any(pat.search(line) for pat in single_comment_patterns):
                        total_comments += 1

    if os.path.isfile(path):
        ext = os.path.splitext(path)[1]
        if ext in file_types:
            analyze_file(path, ext)
    else:
        for root, dirs, files in os.walk(path):
            for filename in files:
                ext = os.path.splitext(filename)[1]
                if ext in file_types:
                    analyze_file(os.path.join(root, filename), ext)

    if total_lines == 0:
        return "0%"

    percentage = (total_comments / total_lines) * 100
    return f"{percentage:.2f}%"

    return total_comments / total_lines