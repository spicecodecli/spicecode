import os
import tree_sitter_python as tspython
import tree_sitter_ruby as tsruby
import tree_sitter_rust as tsrust
import tree_sitter_java as tsjava
import tree_sitter_javascript as tsjs
import tree_sitter_lua as tslua
from tree_sitter import Language, Parser

def get_language_for_file(file_path):
    _, ext = os.path.splitext(file_path)
    if ext == ".py":
        return Language(tspython.language())
    elif ext == ".rb":
        return Language(tsruby.language())
    elif ext == ".rs":
        return Language(tsrust.language())
    elif ext == ".java":
        return Language(tsjava.language())
    elif ext == ".js":
        return Language(tsjs.language())
    elif ext == ".lua":
        return Language(tslua.language())
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

def count_lines_from_tree(tree, code):
    last_node = tree.root_node
    last_byte = last_node.end_byte
    line_count = code[:last_byte].count("\n") + 1
    return line_count

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
