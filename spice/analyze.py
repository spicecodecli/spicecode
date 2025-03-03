import os
from lexers.ruby.rubylexer import RubyLexer
from parser.parser import Parser as RubyParser
from lexers.ruby.token import TokenType

def get_analyzer_for_file(file_path):
    _, ext = os.path.splitext(file_path)
    if ext == ".rb":
        return RubyAnalyzer()
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

class RubyAnalyzer:
    def analyze(self, code):
        # Tokenize the code using our custom Ruby lexer
        lexer = RubyLexer(code)
        tokens = lexer.tokenize()
        
        # Parse the tokens using our custom Ruby parser
        parser = RubyParser(tokens)
        ast = parser.parse()
        
        # Analyze the code
        line_count = code.count("\n") + 1
        function_count = self._count_functions(tokens)
        comment_line_count = self._count_comment_lines(tokens)
        
        return {
            "line_count": line_count,
            "function_count": function_count,
            "comment_line_count": comment_line_count
        }
    
    def _count_functions(self, tokens):
        # Count function definitions by looking for 'def' keywords
        function_count = 0
        for i, token in enumerate(tokens):
            if (token.type == TokenType.KEYWORD and token.value == "def" and 
                i + 1 < len(tokens) and tokens[i + 1].type == TokenType.IDENTIFIER):
                function_count += 1
        return function_count
    
    def _count_comment_lines(self, tokens):
        # Count comment tokens
        comment_lines = 0
        for token in tokens:
            if token.type == TokenType.COMMENT:
                comment_lines += 1
        return comment_lines

def analyze_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()
    
    try:
        analyzer = get_analyzer_for_file(file_path)
        results = analyzer.analyze(code)
        
        print(f"Analyzing file: {os.path.basename(file_path)}")
        print(f"The file has {results['line_count']} lines.")
        print(f"The file has {results['function_count']} functions.")
        print(f"The file has {results['comment_line_count']} comment lines.")
    except ValueError as e:
        print(f"Error: {e}")