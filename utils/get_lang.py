import os


# this will read the file extension and return the correct langague
def get_lexer_for_file(file_path):
    _, ext = os.path.splitext(file_path)

    if ext == ".rb":
        return "ruby"
    
    elif ext == ".py":
        from lexers.python.pythonlexer import PythonLexer
        return "python"
    
    elif ext == ".js":
        return "javascript"
    
    elif ext == ".go":
        return "go"
    
    else:
        raise ValueError(f"Unsupported file extension: {ext}")