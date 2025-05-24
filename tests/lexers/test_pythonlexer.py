import pytest
from lexers.python.pythonlexer import PythonLexer
from lexers.token import TokenType

# Helper function to compare token lists, ignoring EOF
def assert_tokens_equal(actual_tokens, expected_tokens_data):
    # Remove EOF token if present
    if actual_tokens and actual_tokens[-1].type == TokenType.EOF:
        actual_tokens = actual_tokens[:-1]
    
    assert len(actual_tokens) == len(expected_tokens_data), \
        f"Expected {len(expected_tokens_data)} tokens, but got {len(actual_tokens)}\nActual: {actual_tokens}\nExpected data: {expected_tokens_data}"
    
    for i, (token_type, value) in enumerate(expected_tokens_data):
        assert actual_tokens[i].type == token_type, f"Token {i} type mismatch: Expected {token_type}, got {actual_tokens[i].type} ({actual_tokens[i].value})"
        assert actual_tokens[i].value == value, f"Token {i} value mismatch: Expected 	{value}	, got 	{actual_tokens[i].value}	"

# --- Test Cases ---

def test_empty_input():
    lexer = PythonLexer("")
    tokens = lexer.tokenize()
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EOF

def test_keywords():
    code = "def class return if else elif while for in break continue pass import from as try except finally raise with lambda and or not is None True False yield global nonlocal assert del async await"
    lexer = PythonLexer(code)
    tokens = lexer.tokenize()
    expected = [
        (TokenType.KEYWORD, "def"), (TokenType.KEYWORD, "class"), (TokenType.KEYWORD, "return"), 
        (TokenType.KEYWORD, "if"), (TokenType.KEYWORD, "else"), (TokenType.KEYWORD, "elif"), 
        (TokenType.KEYWORD, "while"), (TokenType.KEYWORD, "for"), (TokenType.KEYWORD, "in"), 
        (TokenType.KEYWORD, "break"), (TokenType.KEYWORD, "continue"), (TokenType.KEYWORD, "pass"), 
        (TokenType.KEYWORD, "import"), (TokenType.KEYWORD, "from"), (TokenType.KEYWORD, "as"), 
        (TokenType.KEYWORD, "try"), (TokenType.KEYWORD, "except"), (TokenType.KEYWORD, "finally"), 
        (TokenType.KEYWORD, "raise"), (TokenType.KEYWORD, "with"), (TokenType.KEYWORD, "lambda"), 
        (TokenType.KEYWORD, "and"), (TokenType.KEYWORD, "or"), (TokenType.KEYWORD, "not"), 
        (TokenType.KEYWORD, "is"), (TokenType.BOOLEAN, "None"), (TokenType.BOOLEAN, "True"), 
        (TokenType.BOOLEAN, "False"), (TokenType.KEYWORD, "yield"), (TokenType.KEYWORD, "global"), 
        (TokenType.KEYWORD, "nonlocal"), (TokenType.KEYWORD, "assert"), (TokenType.KEYWORD, "del"), 
        (TokenType.KEYWORD, "async"), (TokenType.KEYWORD, "await")
    ]
    assert_tokens_equal(tokens, expected)

def test_identifiers():
    code = "my_var _another_var var123 _1"
    lexer = PythonLexer(code)
    tokens = lexer.tokenize()
    expected = [
        (TokenType.IDENTIFIER, "my_var"),
        (TokenType.IDENTIFIER, "_another_var"),
        (TokenType.IDENTIFIER, "var123"),
        (TokenType.IDENTIFIER, "_1"),
    ]
    assert_tokens_equal(tokens, expected)

def test_numbers():
    code = "123 45.67 0.5 1e3 2.5e-2 99"
    lexer = PythonLexer(code)
    tokens = lexer.tokenize()
    expected = [
        (TokenType.NUMBER, "123"),
        (TokenType.NUMBER, "45.67"),
        (TokenType.NUMBER, "0.5"),
        (TokenType.NUMBER, "1e3"),
        (TokenType.NUMBER, "2.5e-2"),
        (TokenType.NUMBER, "99"),
    ]
    assert_tokens_equal(tokens, expected)

def test_strings():
    code = "'hello' \"world\" '''triple single''' \"\"\"triple double\"\"\" 'esc\"aped' \"esc'aped\""
    lexer = PythonLexer(code)
    tokens = lexer.tokenize()
    expected = [
        (TokenType.STRING, "'hello'"),
        (TokenType.STRING, '"world"'),
        (TokenType.STRING, "'''triple single'''"),
        (TokenType.STRING, '"""triple double"""'),
        (TokenType.STRING, "'esc\"aped'"),
        (TokenType.STRING, '"esc\'aped"'),
    ]
    assert_tokens_equal(tokens, expected)

def test_operators():
    code = "+ - * / // % ** = == != < > <= >= and or not is in & | ^ ~ << >> := += -= *= /= %= **= //= &= |= ^= <<= >>="
    lexer = PythonLexer(code)
    tokens = lexer.tokenize()
    # Note: 'and', 'or', 'not', 'is', 'in' are keywords when standalone, but operators here due to context/lexer logic
    expected = [
        (TokenType.OPERATOR, "+"), (TokenType.OPERATOR, "-"), (TokenType.OPERATOR, "*"), (TokenType.OPERATOR, "/"),
        (TokenType.OPERATOR, "//"), (TokenType.OPERATOR, "%"), (TokenType.OPERATOR, "**"), (TokenType.OPERATOR, "="),
        (TokenType.OPERATOR, "=="), (TokenType.OPERATOR, "!="), (TokenType.OPERATOR, "<"), (TokenType.OPERATOR, ">"),
        (TokenType.OPERATOR, "<="), (TokenType.OPERATOR, ">="), (TokenType.KEYWORD, "and"), (TokenType.KEYWORD, "or"),
        (TokenType.KEYWORD, "not"), (TokenType.KEYWORD, "is"), (TokenType.KEYWORD, "in"), (TokenType.OPERATOR, "&"),
        (TokenType.OPERATOR, "|"), (TokenType.OPERATOR, "^"), (TokenType.OPERATOR, "~"), (TokenType.OPERATOR, "<<"),
        (TokenType.OPERATOR, ">>"), (TokenType.OPERATOR, ":="), (TokenType.OPERATOR, "+="), (TokenType.OPERATOR, "-="),
        (TokenType.OPERATOR, "*="), (TokenType.OPERATOR, "/="), (TokenType.OPERATOR, "%="), (TokenType.OPERATOR, "**="),
        (TokenType.OPERATOR, "//="), (TokenType.OPERATOR, "&="), (TokenType.OPERATOR, "|="), (TokenType.OPERATOR, "^="),
        (TokenType.OPERATOR, "<<="), (TokenType.OPERATOR, ">>=")
    ]
    assert_tokens_equal(tokens, expected)

def test_delimiters():
    code = "() [] {} , : . ; @"
    lexer = PythonLexer(code)
    tokens = lexer.tokenize()
    expected = [
        (TokenType.DELIMITER, "("), (TokenType.DELIMITER, ")"),
        (TokenType.DELIMITER, "["), (TokenType.DELIMITER, "]"),
        (TokenType.DELIMITER, "{"), (TokenType.DELIMITER, "}"),
        (TokenType.DELIMITER, ","), (TokenType.DELIMITER, ":"),
        (TokenType.DELIMITER, "."), (TokenType.DELIMITER, ";"),
        (TokenType.DELIMITER, "@"),
    ]
    assert_tokens_equal(tokens, expected)

def test_comments():
    code = "# This is a comment\nx = 1 # Another comment"
    lexer = PythonLexer(code)
    tokens = lexer.tokenize()
    expected = [
        (TokenType.COMMENT, "# This is a comment"),
        (TokenType.NEWLINE, "\\n"),
        (TokenType.IDENTIFIER, "x"),
        (TokenType.OPERATOR, "="),
        (TokenType.NUMBER, "1"),
        (TokenType.COMMENT, "# Another comment"),
    ]
    assert_tokens_equal(tokens, expected)

def test_newlines_and_whitespace():
    code = "x = 1\n  y = 2\n\nz = 3"
    lexer = PythonLexer(code)
    tokens = lexer.tokenize()
    expected = [
        (TokenType.IDENTIFIER, "x"), (TokenType.OPERATOR, "="), (TokenType.NUMBER, "1"), (TokenType.NEWLINE, "\\n"),
        (TokenType.IDENTIFIER, "y"), (TokenType.OPERATOR, "="), (TokenType.NUMBER, "2"), (TokenType.NEWLINE, "\\n"),
        (TokenType.NEWLINE, "\\n"),
        (TokenType.IDENTIFIER, "z"), (TokenType.OPERATOR, "="), (TokenType.NUMBER, "3"),
    ]
    assert_tokens_equal(tokens, expected)

def test_mixed_code():
    code = """
def greet(name):
    # Print a greeting
    print(f"Hello, {name}!") # Inline comment
    return name is not None and name != ''

greet("Spice")
"""
    lexer = PythonLexer(code)
    tokens = lexer.tokenize()
    expected = [
        (TokenType.KEYWORD, "def"), (TokenType.IDENTIFIER, "greet"), (TokenType.DELIMITER, "("), (TokenType.IDENTIFIER, "name"), (TokenType.DELIMITER, ")"), (TokenType.DELIMITER, ":"), (TokenType.NEWLINE, "\\n"),
        (TokenType.COMMENT, "# Print a greeting"), (TokenType.NEWLINE, "\\n"),
        (TokenType.IDENTIFIER, "print"), (TokenType.DELIMITER, "("), (TokenType.STRING, 'f"Hello, {name}!"'), (TokenType.DELIMITER, ")"), (TokenType.COMMENT, "# Inline comment"), (TokenType.NEWLINE, "\\n"),
        (TokenType.KEYWORD, "return"), (TokenType.IDENTIFIER, "name"), (TokenType.KEYWORD, "is"), (TokenType.KEYWORD, "not"), (TokenType.BOOLEAN, "None"), (TokenType.KEYWORD, "and"), (TokenType.IDENTIFIER, "name"), (TokenType.OPERATOR, "!="), (TokenType.STRING, "''"), (TokenType.NEWLINE, "\\n"),
        (TokenType.NEWLINE, "\\n"),
        (TokenType.IDENTIFIER, "greet"), (TokenType.DELIMITER, "("), (TokenType.STRING, '"Spice"'), (TokenType.DELIMITER, ")"), (TokenType.NEWLINE, "\\n"),
    ]
    assert_tokens_equal(tokens, expected)

def test_error_character():
    code = "x = $"
    lexer = PythonLexer(code)
    tokens = lexer.tokenize()
    expected = [
        (TokenType.IDENTIFIER, "x"),
        (TokenType.OPERATOR, "="),
        (TokenType.ERROR, "$"),
    ]
    assert_tokens_equal(tokens, expected)

def test_unterminated_string():
    code = "'unterminated"
    lexer = PythonLexer(code)
    tokens = lexer.tokenize()
    # The lexer currently returns an ERROR token for unterminated strings
    assert len(tokens) == 2 # ERROR token + EOF
    assert tokens[0].type == TokenType.ERROR
    assert "string não fechada" in tokens[0].value


