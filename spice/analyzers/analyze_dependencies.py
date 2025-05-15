import os
import ast
import json
import sys

def get_std_lib_modules():
    # This is a simplified list. For a more comprehensive list, 
    # one might need to install a package like `stdlibs` or parse Python's documentation.
    # For this task, we'll use a common subset.
    # Alternatively, we can list ALL imports and let the user differentiate if needed.
    # Based on user's "tudo que é importado", I will list all.
    return set()

def find_imports_in_file(file_path):
    imports = set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        tree = ast.parse(content, filename=file_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0]) # Add the top-level module
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0]) # Add the top-level module
    except Exception as e:
        # print(f"Error parsing {file_path}: {e}", file=sys.stderr)
        return {"error": str(e), "imports": []}
    return list(imports)

project_root = "/home/ubuntu/spicecode"
output_file_path = "/home/ubuntu/dependency_analysis_results.json"
all_files_dependencies = {}

excluded_dirs = [".git", ".github", "venv", "__pycache__", "docs", "build", "dist", "node_modules", "tests/sample-code"]
excluded_files = ["setup.py"] # setup.py might list dependencies but doesn't import them for runtime usually

for root, dirs, files in os.walk(project_root, topdown=True):
    dirs[:] = [d for d in dirs if d not in excluded_dirs and not os.path.join(root, d).startswith(os.path.join(project_root, "tests/sample-code"))]
    for file_name in files:
        if file_name.endswith(".py") and file_name not in excluded_files:
            file_path = os.path.join(root, file_name)
            relative_file_path = os.path.relpath(file_path, project_root)
            file_imports = find_imports_in_file(file_path)
            if isinstance(file_imports, dict) and "error" in file_imports: # Handle parsing errors
                 all_files_dependencies[relative_file_path] = file_imports
            elif file_imports: # Only add if there are imports
                all_files_dependencies[relative_file_path] = file_imports

# Consolidate all unique dependencies across the project
project_wide_dependencies = set()
for file_path, imports in all_files_dependencies.items():
    if isinstance(imports, list):
        for imp in imports:
            project_wide_dependencies.add(imp)

final_output = {
    "project_wide_unique_dependencies": sorted(list(project_wide_dependencies)),
    "dependencies_by_file": all_files_dependencies
}

with open(output_file_path, "w", encoding="utf-8") as outfile:
    json.dump(final_output, outfile, indent=2)

print(f"Dependency analysis complete. Results saved to {output_file_path}")

