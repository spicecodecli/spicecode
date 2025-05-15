import ast

def analyze_visibility(code_content, file_name_for_error_reporting="<string>"):
    try:
        tree = ast.parse(code_content, filename=file_name_for_error_reporting)
    except Exception as e:
        return {
            "error": str(e), 
            "public_functions": 0, "private_functions": 0, 
            "public_methods": 0, "private_methods": 0, 
            "details": []
        }

    public_functions = 0
    private_functions = 0
    public_methods = 0
    private_methods = 0
    details = []
    
    # Identify all function/method names defined within classes first
    defined_in_class = set()
    class_definitions = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_definitions[node.name] = node
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    # Record the method name with its class context to avoid ambiguity if needed later
                    # For now, just the name is enough for the set
                    defined_in_class.add(item.name) 
                    
                    method_full_name = f"{node.name}.{item.name}"
                    if item.name.startswith("__") and not item.name.endswith("__"): 
                        private_methods +=1
                        details.append({"name": method_full_name, "type": "method", "visibility": "private (name mangling)", "lineno": item.lineno})
                    elif item.name.startswith("_"):
                        private_methods += 1
                        details.append({"name": method_full_name, "type": "method", "visibility": "private (convention)", "lineno": item.lineno})
                    else:
                        public_methods += 1
                        details.append({"name": method_full_name, "type": "method", "visibility": "public", "lineno": item.lineno})
    
    # Identify standalone functions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Check if this function definition is directly under the module (i.e., not inside a class or another function)
            # A simple check is if its name is NOT in `defined_in_class`
            # More robust: check its parent node type if ast provided parent pointers (it doesn't by default)
            # For this script, we assume functions at the top level of the `ast.walk` that are FunctionDef
            # and not in `defined_in_class` are standalone functions.
            
            is_standalone_function = True
            # Check if it's nested inside another function (not directly supported by this simplified check)
            # For now, if it's not a method, it's a function.
            if item.name in defined_in_class:
                 is_standalone_function = False # It's a method, already processed

            if is_standalone_function:
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

