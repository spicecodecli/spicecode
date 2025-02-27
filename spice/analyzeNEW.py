
import os
from tree_sitter_language_pack import get_binding, get_language, get_parser

def get_language_name_for_file(file_path):
    _, ext = os.path.splitext(file_path)
    if ext == ".py":
        return 'python'
    elif ext == ".rb":
        return 'ruby'
    elif ext == ".java":
        return 'java'
    elif ext == ".js":
        return 'javascript'
    elif ext == ".lua":
        return 'lua'
    else:
        raise ValueError(f"Support coming soon for the file extension: {ext}")

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
    

    language_name = get_language_name_for_file(file_path)
    # binding = get_binding(language_name)
    # language = get_language(language_name)
    parser = get_parser('python')

    tree = parser.parse(bytes(code, "utf8"))
    
    line_count = count_lines_from_tree(tree, code)
    function_count = count_functions_from_tree(tree)
    comment_line_count = count_comment_lines_from_tree(tree, code)
    
    print(f"Analyzing file: {os.path.basename(file_path)}")
    print(f"The file has {line_count} lines.")
    print(f"The file has {function_count} functions.")
    print(f"The file has {comment_line_count} comment lines.")


# I WILL DELETE THIS FILE LATER IM JUST SAVING THIS VERSION HERE FOR NOW I DONT WANT TO USE GIT ITS TOO LATE AT NIGHT PEOPLE WILL THINK IM CRAZY