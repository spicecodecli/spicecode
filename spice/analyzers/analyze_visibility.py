import os
import ast
import json
import sys

def analyze_methods_functions_visibility(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        tree = ast.parse(content, filename=file_path)
    except Exception as e:
        return {"error": str(e), "public_functions": 0, "private_functions": 0, "public_methods": 0, "private_methods": 0, "details": []}

    public_functions = 0
    private_functions = 0
    public_methods = 0
    private_methods = 0
    details = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            is_method = False
            parent = getattr(node, "parent", None)
            while parent:
                if isinstance(parent, ast.ClassDef):
                    is_method = True
                    break
                parent = getattr(parent, "parent", None)
            
            # Assign parent nodes for easier traversal (ast doesn't do this by default)
            for child in ast.iter_child_nodes(node):
                child.parent = node

            # Check if it's a method by looking for a ClassDef ancestor
            is_within_class = False
            ancestor = node
            # Need to walk up the tree. A simple way is to check the first arg name for 'self' or 'cls' for methods,
            # but proper way is to check if FunctionDef is a direct child of ClassDef.
            # The ast.walk gives nodes in some order, but not necessarily with parent pointers.
            # For simplicity, I'll check if the function is a direct child of a ClassDef node during a separate pass or by checking node.name
            # A more robust way: iterate all ClassDefs, then their FunctionDef children.

            if node.name.startswith("__") and not node.name.endswith("__"): # Exclude dunder methods like __init__ unless they also start with _ClassName__
                # Python's name mangling for __var means it's private.
                # Dunder methods like __init__, __str__ are special, not typically considered 'private' in the same sense of hiding.
                # However, user asked for methods/functions. __init__ is a method.
                # Let's stick to the leading underscore convention for privacy.
                # If it starts with __ and is not a dunder, it's private.
                if is_method:
                    private_methods += 1
                    details.append({"name": node.name, "type": "method", "visibility": "private (name mangling)", "lineno": node.lineno})
                else:
                    private_functions += 1
                    details.append({"name": node.name, "type": "function", "visibility": "private (name mangling)", "lineno": node.lineno})
            elif node.name.startswith("_"):
                if is_method:
                    private_methods += 1
                    details.append({"name": node.name, "type": "method", "visibility": "private (convention)", "lineno": node.lineno})
                else:
                    private_functions += 1
                    details.append({"name": node.name, "type": "function", "visibility": "private (convention)", "lineno": node.lineno})
            else:
                if is_method:
                    public_methods += 1
                    details.append({"name": node.name, "type": "method", "visibility": "public", "lineno": node.lineno})
                else:
                    public_functions += 1
                    details.append({"name": node.name, "type": "function", "visibility": "public", "lineno": node.lineno})
    
    # Refined approach to distinguish methods from functions:
    # Iterate through ClassDef nodes first.
    public_functions = 0
    private_functions = 0
    public_methods = 0
    private_methods = 0
    details = []
    
    defined_in_class = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    defined_in_class.add(item.name)
                    if item.name.startswith("__") and not item.name.endswith("__"): 
                        private_methods +=1
                        details.append({"name": f"{node.name}.{item.name}", "type": "method", "visibility": "private (name mangling)", "lineno": item.lineno})
                    elif item.name.startswith("_"):
                        private_methods += 1
                        details.append({"name": f"{node.name}.{item.name}", "type": "method", "visibility": "private (convention)", "lineno": item.lineno})
                    else:
                        public_methods += 1
                        details.append({"name": f"{node.name}.{item.name}", "type": "method", "visibility": "public", "lineno": item.lineno})
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name not in defined_in_class: # It's a standalone function
                if node.name.startswith("__") and not node.name.endswith("__"): 
                    private_functions += 1
                    details.append({"name": node.name, "type": "function", "visibility": "private (name mangling)", "lineno": node.lineno})
                elif node.name.startswith("_"):
                    private_functions += 1
                    details.append({"name": node.name, "type": "function", "visibility": "private (convention)", "lineno": node.lineno})
                else:
                    public_functions += 1
                    details.append({"name": node.name, "type": "function", "visibility": "public", "lineno": node.lineno})

    return {
        "public_functions": public_functions,
        "private_functions": private_functions,
        "public_methods": public_methods,
        "private_methods": private_methods,
        "details": sorted(details, key=lambda x: x["lineno"])
    }

project_root = "/home/ubuntu/spicecode"
output_file_path = "/home/ubuntu/visibility_analysis_results.json"
all_files_visibility_data = {}

excluded_dirs = [".git", ".github", "venv", "__pycache__", "docs", "build", "dist", "node_modules", "tests/sample-code"]
excluded_files = ["setup.py"]

for root, dirs, files in os.walk(project_root, topdown=True):
    dirs[:] = [d for d in dirs if d not in excluded_dirs and not os.path.join(root, d).startswith(os.path.join(project_root, "tests/sample-code"))]
    for file_name in files:
        if file_name.endswith(".py") and file_name not in excluded_files:
            file_path = os.path.join(root, file_name)
            relative_file_path = os.path.relpath(file_path, project_root)
            analysis_result = analyze_methods_functions_visibility(file_path)
            all_files_visibility_data[relative_file_path] = analysis_result

with open(output_file_path, "w", encoding="utf-8") as outfile:
    json.dump(all_files_visibility_data, outfile, indent=2)

print(f"Method/Function visibility analysis complete. Results saved to {output_file_path}")

