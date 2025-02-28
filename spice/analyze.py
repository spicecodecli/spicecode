import os
import tree_sitter_python as tspython
import tree_sitter_java as tsjava
import tree_sitter_javascript as tsjs
import tree_sitter_lua as tslua
from tree_sitter import Language, Parser

# Adjusted import for the custom Ruby parser
from parsers.ruby.rubyparser import Lexer, Parser as RubyParser, ProgramNode, FunctionDefNode

def get_language_for_file(file_path):
    _, ext = os.path.splitext(file_path)
    if ext == ".py":
        return Language(tspython.language())
    elif ext == ".java":
        return Language(tsjava.language())
    elif ext == ".js":
        return Language(tsjs.language())
    elif ext == ".lua":
        return Language(tslua.language())
    elif ext == ".rb":
        return "CUSTOM_RUBY"
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

def count_functions_from_ruby_ast(ast):
    """Counts function definitions in the custom Ruby AST."""
    return sum(1 for node in ast.statements if isinstance(node, FunctionDefNode))

def count_comment_lines_from_ruby_code(code):
    """Counts comment lines (lines starting with #) in Ruby code."""
    return sum(1 for line in code.split("\n") if line.strip().startswith("#"))

def analyze_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()
    
    language = get_language_for_file(file_path)

    if language == "CUSTOM_RUBY":
        # Use the custom Ruby parser
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = RubyParser(tokens)
        ast = parser.parse()
        
        line_count = code.count("\n") + 1
        function_count = count_functions_from_ruby_ast(ast)
        comment_line_count = count_comment_lines_from_ruby_code(code)

    else:
        # Use Tree-sitter for other languages
        parser = Parser(language)
        tree = parser.parse(bytes(code, "utf8"))
        
        line_count = code.count("\n") + 1
        function_count = count_functions_from_tree(tree)
        comment_line_count = count_comment_lines_from_tree(tree, code)
    
    print(f"Analyzing file: {os.path.basename(file_path)}")
    print(f"The file has {line_count} lines.")
    print(f"The file has {function_count} functions.")
    print(f"The file has {comment_line_count} comment lines.")

def count_functions_from_tree(tree):
    function_count = 0
    for node in tree.root_node.children:
        if node.type == "function_definition":
            function_count += 1
    return function_count

def count_comment_lines_from_tree(tree, code):
    comment_lines = 0
    for node in tree.root_node.children:
        if node.type == "comment":
            comment_text = code[node.start_byte:node.end_byte]
            comment_lines += comment_text.count("\n") + 1
    return comment_lines



def analyze_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()
    
    language = get_language_for_file(file_path)
    parser = Parser(language)
    tree = parser.parse(bytes(code, "utf8"))
    
    line_count = count_lines_from_tree(tree, code)
    function_count = count_functions_from_tree(tree)
    comment_line_count = count_comment_lines_from_tree(tree, code)
    
    print(f"Analyzing file: {os.path.basename(file_path)}")
    print(f"The file has {line_count} lines.")
    print(f"The file has {function_count} functions.")
    print(f"The file has {comment_line_count} comment lines.")
