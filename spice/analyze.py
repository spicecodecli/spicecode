import os

# import our in-house token
from lexers.token import TokenType

# import all of our in-house lexers
from lexers.ruby.rubylexer import RubyLexer
from lexers.python.pythonlexer import PythonLexer
from lexers.javascript.javascriptlexer import JavaScriptLexer
from lexers.brainfuck.brainfucklexer import BrainfuckLexer

# import our in-house parser
from parser.parser import Parser


class CodeAnalyzer:
    """Base class for all language analyzers"""
    
    def __init__(self):
        self.lexer_class = None
        self.parser_class = None
        self.function_keyword = None
    
    def analyze(self, code):
        """Analyze code and return metrics"""
        # Tokenize the code
        lexer = self.lexer_class(code)
        tokens = lexer.tokenize()
        
        # Parse the tokens
        parser = self.parser_class(tokens)
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
        """Count function definitions by looking for function keywords"""
        function_count = 0
        for i, token in enumerate(tokens):
            if (token.type == TokenType.KEYWORD and 
                token.value == self.function_keyword and 
                i + 1 < len(tokens) and 
                tokens[i + 1].type == TokenType.IDENTIFIER):
                function_count += 1
        return function_count
    
    def _count_comment_lines(self, tokens):
        """Count comment tokens"""
        comment_lines = 0
        for token in tokens:
            if token.type == TokenType.COMMENT:
                comment_lines += 1
        return comment_lines


class RubyAnalyzer(CodeAnalyzer):
    def __init__(self):
        super().__init__()
        self.lexer_class = RubyLexer
        self.parser_class = Parser
        self.function_keyword = "def"


class PythonAnalyzer(CodeAnalyzer):
    def __init__(self):
        super().__init__()
        self.lexer_class = PythonLexer
        self.parser_class = Parser
        self.function_keyword = "def"


class JavaScriptAnalyzer(CodeAnalyzer):
    def __init__(self):
        super().__init__()
        self.lexer_class = JavaScriptLexer
        self.parser_class = Parser
        self.function_keyword = "function"


class BrainfuckAnalyzer(CodeAnalyzer):
    def __init__(self):
        super().__init__()
        self.lexer_class = BrainfuckLexer
        self.parser_class = Parser
        self.function_keyword = None  # Brainfuck doesn't have functions
    
    def _count_functions(self, tokens):
        """Override: Brainfuck doesn't have functions"""
        return 0
    
    def analyze(self, code):
        """Override analyze method for Brainfuck-specific metrics"""
        # Tokenize the code
        lexer = self.lexer_class(code)
        tokens = lexer.tokenize()
        
        # Parse the tokens (likely minimal for Brainfuck)
        parser = self.parser_class(tokens)
        ast = parser.parse()
        
        # Count lines and comments
        line_count = code.count("\n") + 1
        comment_line_count = self._count_comment_lines(tokens)
        
        # Count Brainfuck operations
        operation_counts = {
            ">": 0,  # Increment pointer
            "<": 0,  # Decrement pointer
            "+": 0,  # Increment value
            "-": 0,  # Decrement value
            ".": 0,  # Output
            ",": 0,  # Input
            "[": 0,  # Jump forward
            "]": 0   # Jump backward
        }
        
        for token in tokens:
            if token.type == TokenType.OPERATOR and token.value in operation_counts:
                operation_counts[token.value] += 1
        
        # Count loops (pairs of [ and ])
        loop_count = operation_counts["["]  # Should be equal to operation_counts["]"]
        
        return {
            "line_count": line_count,
            "function_count": 0,  # No functions in Brainfuck
            "comment_line_count": comment_line_count,
            "operation_counts": operation_counts,
            "loop_count": loop_count,
            "io_operations": operation_counts["."] + operation_counts[","]
        }


# dicionario tipo aurelio
LANGUAGE_ANALYZERS = {
    ".rb": RubyAnalyzer,
    ".py": PythonAnalyzer,
    ".js": JavaScriptAnalyzer,
    ".bf": BrainfuckAnalyzer,
    ".b": BrainfuckAnalyzer
}


def get_analyzer_for_file(file_path):
    """Factory function to get the appropriate analyzer for a file"""
    _, ext = os.path.splitext(file_path)
    analyzer_class = LANGUAGE_ANALYZERS.get(ext)
    
    if analyzer_class:
        return analyzer_class()
    else:
        raise ValueError(f"Unsupported file extension: {ext}")


def analyze_file(file_path):
    """Analyze a file and print the results"""
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()
    
    try:
        analyzer = get_analyzer_for_file(file_path)
        results = analyzer.analyze(code)
        
        print(f"Analyzing file: {os.path.basename(file_path)}")
        print(f"The file has {results['line_count']} lines.")
        
        # For most languages
        if isinstance(analyzer, (RubyAnalyzer, PythonAnalyzer, JavaScriptAnalyzer)):
            print(f"The file has {results['function_count']} functions.")
            print(f"The file has {results['comment_line_count']} comment lines.")
        
        # Brainfuck-specific output
        elif isinstance(analyzer, BrainfuckAnalyzer):
            ops = results['operation_counts']
            print(f"The file has {results['comment_line_count']} comment lines.")
            print(f"Brainfuck Operations:")
            print(f"  > (inc ptr): {ops['>']} operations")
            print(f"  < (dec ptr): {ops['<']} operations")
            print(f"  + (inc val): {ops['+']} operations")
            print(f"  - (dec val): {ops['-']} operations")
            print(f"  . (output): {ops['.']} operations")
            print(f"  , (input): {ops[',']} operations")
            print(f"  [ (loop start): {ops['[']} operations")
            print(f"  ] (loop end): {ops[']']} operations")
            print(f"Total loops: {results['loop_count']}")
            print(f"I/O operations: {results['io_operations']}")
    except ValueError as e:
        print(f"Error: {e}")