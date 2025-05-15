import ast

def analyze_dependencies(code_content, file_name_for_error_reporting="<string>"):
    imports = set()
    try:
        tree = ast.parse(code_content, filename=file_name_for_error_reporting)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0]) # Add the top-level module
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split(".")[0]) # Add the top-level module
    except Exception as e:
        return {"error": str(e), "imports": []} # Return error and empty list for consistency
    return list(imports)

