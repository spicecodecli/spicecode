import os


# this will read the file extension and return the correct lexer
def get_lexer_for_file(file_path):
    _, ext = os.path.splitext(file_path)

    if ext == ".rb":
        from lexers.ruby.rubylexer import RubyLexer
        return RubyLexer
    
    elif ext == ".py":
        from lexers.python.pythonlexer import PythonLexer
        return PythonLexer
    
    elif ext == ".js":
        from lexers.javascript.javascriptlexer import JavaScriptLexer
        return JavaScriptLexer
    
    elif ext == ".go":
        from lexers.golang.golexer import GoLexer
        return GoLexer
    
    else:
        raise ValueError(f"Unsupported file extension: {ext}")