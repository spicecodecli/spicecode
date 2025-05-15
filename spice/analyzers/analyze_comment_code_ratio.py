import os
import json
import sys

def analyze_lines_for_comment_code_ratio(code_content):
    lines = code_content.splitlines()
    line_details = []
    
    num_code_lines = 0
    num_comment_only_lines = 0
    num_empty_or_whitespace_lines = 0

    for i, line_text in enumerate(lines):
        stripped_line = line_text.strip()
        line_type = ""

        if not stripped_line:
            line_type = "empty_or_whitespace"
            num_empty_or_whitespace_lines += 1
        elif stripped_line.startswith("#"): # Assuming Python style comments
            line_type = "comment_only"
            num_comment_only_lines += 1
        else:
            line_type = "code" # This includes lines with inline comments
            num_code_lines += 1
        
        line_details.append({
            "original_line_number": i + 1,
            "line_content": line_text,
            "stripped_line_content": stripped_line,
            "type": line_type
        })
    
    total_relevant_lines = num_code_lines + num_comment_only_lines
    ratio = 0
    if total_relevant_lines > 0:
        ratio = num_comment_only_lines / total_relevant_lines
    else: # Avoid division by zero if file has no code or comments (e.g. only empty lines)
        ratio = 0 # Or could be undefined/null, user might prefer 0 if no comments and no code.

    summary = {
        "total_lines_in_file": len(lines),
        "code_lines": num_code_lines,
        "comment_only_lines": num_comment_only_lines,
        "empty_or_whitespace_lines": num_empty_or_whitespace_lines,
        "comment_to_code_plus_comment_ratio": ratio
    }
    
    return {"line_by_line_analysis": line_details, "summary_stats": summary}

project_root = "/home/ubuntu/spicecode"
output_file_path = "/home/ubuntu/comment_code_ratio_analysis_results.json"
all_files_comment_code_data = {}

excluded_dirs = [".git", ".github", "venv", "__pycache__", "docs", "build", "dist", "node_modules", "tests/sample-code"]
excluded_files = ["setup.py"]

for root, dirs, files in os.walk(project_root, topdown=True):
    dirs[:] = [d for d in dirs if d not in excluded_dirs and not os.path.join(root, d).startswith(os.path.join(project_root, "tests/sample-code"))]
    for file_name in files:
        if file_name.endswith(".py") and file_name not in excluded_files:
            file_path = os.path.join(root, file_name)
            relative_file_path = os.path.relpath(file_path, project_root)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                analysis_result = analyze_lines_for_comment_code_ratio(content)
                all_files_comment_code_data[relative_file_path] = analysis_result
            except Exception as e:
                all_files_comment_code_data[relative_file_path] = {"error": str(e), "line_by_line_analysis": [], "summary_stats": {}}

with open(output_file_path, "w", encoding="utf-8") as outfile:
    json.dump(all_files_comment_code_data, outfile, indent=2)

print(f"Comment/Code ratio analysis complete. Results saved to {output_file_path}")

