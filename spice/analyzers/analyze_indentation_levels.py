import os
import sys
import json
import re

def detect_indentation_from_spicecode(code_content):
    lines = code_content.split('\n')
    indentation_levels_per_line = []

    for i, line_text in enumerate(lines):
        stripped_line = line_text.strip()
        is_empty_or_whitespace_only = not bool(stripped_line)

        leading_whitespace_match = re.match(r'^(\s*)', line_text)
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

project_root = "/home/ubuntu/spicecode"
output_file_path = "/home/ubuntu/indentation_analysis_results.json"
all_files_indentation_data = {}

excluded_dirs = ['.git', '.github', 'venv', '__pycache__', 'docs', 'build', 'dist', 'node_modules', 'tests/sample-code']
excluded_files = ['setup.py'] 

for root, dirs, files in os.walk(project_root, topdown=True):
    dirs[:] = [d for d in dirs if d not in excluded_dirs and not os.path.join(root, d).startswith(os.path.join(project_root, 'tests/sample-code'))]
    for file_name in files:
        if file_name.endswith(".py") and file_name not in excluded_files:
            file_path = os.path.join(root, file_name)
            relative_file_path = os.path.relpath(file_path, project_root)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                line_indentation_details = detect_indentation_from_spicecode(content)
                all_files_indentation_data[relative_file_path] = line_indentation_details
            except Exception as e:
                all_files_indentation_data[relative_file_path] = {"error": str(e), "lines": []}

with open(output_file_path, "w", encoding="utf-8") as outfile:
    json.dump(all_files_indentation_data, outfile, indent=2)

print(f"Indentation analysis complete. Results saved to {output_file_path}")

