import os

from lexers.ruby.rubylexer import RubyLexer
from parser.parser import Parser as RubyParser
from lexers.token import TokenType

from lexers.python.pythonlexer import PythonLexer
from parser.parser import Parser as PythonParser

from lexers.javascript.javascriptlexer import JavaScriptLexer  
from parser.parser import Parser as JavaScriptParser

def get_analyzer_for_file(file_path):
    _, ext = os.path.splitext(file_path)
    if ext == ".rb":
        return RubyAnalyzer()
    elif ext == ".py":
        return PythonAnalyzer()
    elif ext == ".js":  
        return JavaScriptAnalyzer()
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

class RubyAnalyzer:
    def analyze(self, code):
        # tokenize the code using our in house custom SPICY RUBY LEXER
        lexer = RubyLexer(code)
        tokens = lexer.tokenize()
        
        # parse the tokens using our in house custom SPICY PARSER
        parser = RubyParser(tokens)
        ast = parser.parse()
        
        # analyze the code
        line_count = code.count("\n") + 1
        function_count = self._count_functions(tokens)
        comment_line_count = self._count_comment_lines(tokens)
        
        return {
            "line_count": line_count,
            "function_count": function_count,
            "comment_line_count": comment_line_count
        }
    
    def _count_functions(self, tokens):
        # count function definitions by looking for 'def' keywords
        function_count = 0
        for i, token in enumerate(tokens):
            if (token.type == TokenType.KEYWORD and token.value == "def" and 
                i + 1 < len(tokens) and tokens[i + 1].type == TokenType.IDENTIFIER):
                function_count += 1
        return function_count
    
    def _count_comment_lines(self, tokens):
        # count comment tokens
        comment_lines = 0
        for token in tokens:
            if token.type == TokenType.COMMENT:
                comment_lines += 1
        return comment_lines

class PythonAnalyzer:
    def analyze(self, code):
        # tokeniza o código usando o lexer de python
        lexer = PythonLexer(code)
        tokens = lexer.tokenize()
        
        # parseia os tokens usando o parser de python
        parser = PythonParser(tokens)
        ast = parser.parse()
        
        # analisa o código
        line_count = code.count("\n") + 1
        function_count = self._count_functions(tokens)
        comment_line_count = self._count_comment_lines(tokens)
        
        return {
            "line_count": line_count,
            "function_count": function_count,
            "comment_line_count": comment_line_count
        }
    
    def _count_functions(self, tokens):
        # conta definições de função procurando por 'def'
        function_count = 0
        for i, token in enumerate(tokens):
            if (token.type == TokenType.KEYWORD and token.value == "def" and 
                i + 1 < len(tokens) and tokens[i + 1].type == TokenType.IDENTIFIER):
                function_count += 1
        return function_count
    
    def _count_comment_lines(self, tokens):
        # conta linhas de comentário
        comment_lines = 0
        for token in tokens:
            if token.type == TokenType.COMMENT:
                comment_lines += 1
        return comment_lines

class JavaScriptAnalyzer:
    def analyze(self, code):
        # tokeniza o código usando o lexer de javascript
        lexer = JavaScriptLexer(code)
        tokens = lexer.tokenize()
        
        # parseia os tokens usando o parser de javascript
        parser = JavaScriptParser(tokens)
        ast = parser.parse()
        
        # analisa o código
        line_count = code.count("\n") + 1
        function_count = self._count_functions(tokens)
        comment_line_count = self._count_comment_lines(tokens)
        
        return {
            "line_count": line_count,
            "function_count": function_count,
            "comment_line_count": comment_line_count
        }
    
    def _count_functions(self, tokens):
        # conta definições de função procurando por 'function'
        function_count = 0
        for i, token in enumerate(tokens):
            if (token.type == TokenType.KEYWORD and token.value == "function" and 
                i + 1 < len(tokens) and tokens[i + 1].type == TokenType.IDENTIFIER):
                function_count += 1
        return function_count
    
    def _count_comment_lines(self, tokens):
        # conta linhas de comentário
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