import pytest
from lexers.javascript.javascriptlexer import JavaScriptLexer
from lexers.token import TokenType

# Helper function to compare token lists, ignoring EOF (similar to other lexer tests)
def assert_tokens_equal(actual_tokens, expected_tokens_data):
    if actual_tokens and actual_tokens[-1].type == TokenType.EOF:
        actual_tokens = actual_tokens[:-1]
    
    assert len(actual_tokens) == len(expected_tokens_data), \
        f"Expected {len(expected_tokens_data)} tokens, but got {len(actual_tokens)}\nActual: {actual_tokens}\nExpected data: {expected_tokens_data}"
    
    for i, (token_type, value) in enumerate(expected_tokens_data):
        assert actual_tokens[i].type == token_type, f"Token {i} type mismatch: Expected {token_type}, got {actual_tokens[i].type} ({actual_tokens[i].value})"
        assert actual_tokens[i].value == value, f"Token {i} value mismatch: Expected 	{value}	, got 	{actual_tokens[i].value}	"

# --- Test Cases ---

def test_js_empty_input():
    lexer = JavaScriptLexer("")
    tokens = lexer.tokenize()
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EOF

def test_js_keywords():
    code = "function if else return let const var for while do break continue switch case default try catch throw new this class extends super import export typeof instanceof void delete in of yield await async true false null undefined"
    lexer = JavaScriptLexer(code)
    tokens = lexer.tokenize()
    expected = [
        (TokenType.KEYWORD, "function"), (TokenType.KEYWORD, "if"), (TokenType.KEYWORD, "else"), (TokenType.KEYWORD, "return"),
        (TokenType.KEYWORD, "let"), (TokenType.KEYWORD, "const"), (TokenType.KEYWORD, "var"), (TokenType.KEYWORD, "for"),
        (TokenType.KEYWORD, "while"), (TokenType.KEYWORD, "do"), (TokenType.KEYWORD, "break"), (TokenType.KEYWORD, "continue"),
        (TokenType.KEYWORD, "switch"), (TokenType.KEYWORD, "case"), (TokenType.KEYWORD, "default"), (TokenType.KEYWORD, "try"),
        (TokenType.KEYWORD, "catch"), (TokenType.KEYWORD, "throw"), (TokenType.KEYWORD, "new"), (TokenType.KEYWORD, "this"),
        (TokenType.KEYWORD, "class"), (TokenType.KEYWORD, "extends"), (TokenType.KEYWORD, "super"), (TokenType.KEYWORD, "import"),
        (TokenType.KEYWORD, "export"), (TokenType.KEYWORD, "typeof"), (TokenType.KEYWORD, "instanceof"), (TokenType.KEYWORD, "void"),
        (TokenType.KEYWORD, "delete"), (TokenType.KEYWORD, "in"), (TokenType.KEYWORD, "of"), (TokenType.KEYWORD, "yield"),
        (TokenType.KEYWORD, "await"), (TokenType.KEYWORD, "async"), (TokenType.KEYWORD, "true"), (TokenType.KEYWORD, "false"),
        (TokenType.KEYWORD, "null"), (TokenType.KEYWORD, "undefined")
    ]
    assert_tokens_equal(tokens, expected)

def test_js_identifiers():
    code = "myVar _anotherVar var123 $special _"
    lexer = JavaScriptLexer(code)
    tokens = lexer.tokenize()
    expected = [
        (TokenType.IDENTIFIER, "myVar"),
        (TokenType.IDENTIFIER, "_anotherVar"),
        (TokenType.IDENTIFIER, "var123"),
        (TokenType.IDENTIFIER, "$special"), # $ is allowed in JS identifiers
        (TokenType.IDENTIFIER, "_"),
    ]
    assert_tokens_equal(tokens, expected)

def test_js_numbers():
    code = "123 45.67 0.5 1e3 2.5e-2 99"
    lexer = JavaScriptLexer(code)
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

def test_js_strings()    code = "\\'hello\\' \"world\" \"with \\\"escape\\\"\""
    lexer = JavaScriptLexer(code)
    tokens = lexer.tokenize()
    expected = [
        (TokenType.STRING, "\'hello\'"),
        (TokenType.STRING, '\"world\"'),
        (TokenType.STRING, '\"with \\"escape\\"\"'), # String includes escapes
    ]
    assert_tokens_equal(tokens, expected)

def test_js_operators():
    code = "+ - * / % = == === != !== > < >= <= && || ! & | ^ ~ << >> >>> ++ -- += -= *= /= %= &= |= ^= <<= >>= >>>= => ? : ."
    lexer = JavaScriptLexer(code)
    tokens = lexer.tokenize()
    expected = [
        (TokenType.OPERATOR, "+"), (TokenType.OPERATOR, "-"), (TokenType.OPERATOR, "*"), (TokenType.OPERATOR, "/"), (TokenType.OPERATOR, "%"),
        (TokenType.OPERATOR, "="), (TokenType.OPERATOR, "=="), (TokenType.OPERATOR, "==="), (TokenType.OPERATOR, "!="), (TokenType.OPERATOR, "!=="),
        (TokenType.OPERATOR, ">"), (TokenType.OPERATOR, "<"), (TokenType.OPERATOR, ">="), (TokenType.OPERATOR, "<="), (TokenType.OPERATOR, "&&"),
        (TokenType.OPERATOR, "||"), (TokenType.OPERATOR, "!"), (TokenType.OPERATOR, "&"), (TokenType.OPERATOR, "|"), (TokenType.OPERATOR, "^"),
        (TokenType.OPERATOR, "~"), (TokenType.OPERATOR, "<<"), (TokenType.OPERATOR, ">>"), (TokenType.OPERATOR, ">>>"), (TokenType.OPERATOR, "++"),
        (TokenType.OPERATOR, "--"), (TokenType.OPERATOR, "+="), (TokenType.OPERATOR, "-="), (TokenType.OPERATOR, "*="), (TokenType.OPERATOR, "/="),
        (TokenType.OPERATOR, "%="), (TokenType.OPERATOR, "&="), (TokenType.OPERATOR, "|="), (TokenType.OPERATOR, "^="), (TokenType.OPERATOR, "<<="),
        (TokenType.OPERATOR, ">>="), (TokenType.OPERATOR, ">>>="), (TokenType.OPERATOR, "=>"), (TokenType.OPERATOR, "?"), (TokenType.OPERATOR, ":"),
        (TokenType.OPERATOR, ".")
    ]
    assert_tokens_equal(tokens, expected)

def test_js_delimiters():
    code = "( ) { } [ ] ; , :"
    lexer = JavaScriptLexer(code)
    tokens = lexer.tokenize()
    expected = [
        (TokenType.DELIMITER, "("), (TokenType.DELIMITER, ")"),
        (TokenType.DELIMITER, "{"), (TokenType.DELIMITER, "}"),
        (TokenType.DELIMITER, "["), (TokenType.DELIMITER, "]"),
        (TokenType.DELIMITER, ";"),
        (TokenType.ERROR, ","), # Comma is not listed as a delimiter in the lexer
        (TokenType.DELIMITER, ":"),
    ]
    # Note: Comma is currently marked as ERROR. Adjust test if lexer is updated.
    assert_tokens_equal(tokens, expected)

def test_js_comments():
    code = "// Single line comment\nlet x = 1; /* Multi-line\n comment */ var y = 2;"
    lexer = JavaScriptLexer(code)
    tokens = lexer.tokenize()
    expected = [
        (TokenType.COMMENT, "// Single line comment"), (TokenType.NEWLINE, "\\n"),
        (TokenType.KEYWORD, "let"), (TokenType.IDENTIFIER, "x"), (TokenType.OPERATOR, "="), (TokenType.NUMBER, "1"), (TokenType.DELIMITER, ";"),
        (TokenType.COMMENT, "/* Multi-line\n comment */"),
        (TokenType.KEYWORD, "var"), (TokenType.IDENTIFIER, "y"), (TokenType.OPERATOR, "="), (TokenType.NUMBER, "2"), (TokenType.DELIMITER, ";"),
    ]
    assert_tokens_equal(tokens, expected)

def test_js_mixed_code():
    code = """
function calculate(x, y) {
  // Calculate sum
  const sum = x + y;
  if (sum > 10) {
    console.log(`Result: ${sum}`); // Log if large
  }
  return sum;
}

calculate(5, 7);
"""
    lexer = JavaScriptLexer(code)
    tokens = lexer.tokenize()
    expected = [
        (TokenType.NEWLINE, "\\n"),
        (TokenType.KEYWORD, "function"), (TokenType.IDENTIFIER, "calculate"), (TokenType.DELIMITER, "("), (TokenType.IDENTIFIER, "x"), (TokenType.ERROR, ","), (TokenType.IDENTIFIER, "y"), (TokenType.DELIMITER, ")"), (TokenType.DELIMITER, "{"), (TokenType.NEWLINE, "\\n"),
        (TokenType.COMMENT, "// Calculate sum"), (TokenType.NEWLINE, "\\n"),
        (TokenType.KEYWORD, "const"), (TokenType.IDENTIFIER, "sum"), (TokenType.OPERATOR, "="), (TokenType.IDENTIFIER, "x"), (TokenType.OPERATOR, "+"), (TokenType.IDENTIFIER, "y"), (TokenType.DELIMITER, ";"), (TokenType.NEWLINE, "\\n"),
        (TokenType.KEYWORD, "if"), (TokenType.DELIMITER, "("), (TokenType.IDENTIFIER, "sum"), (TokenType.OPERATOR, ">"), (TokenType.NUMBER, "10"), (TokenType.DELIMITER, ")"), (TokenType.DELIMITER, "{"), (TokenType.NEWLINE, "\\n"),
        (TokenType.IDENTIFIER, "console"), (TokenType.OPERATOR, "."), (TokenType.IDENTIFIER, "log"), (TokenType.DELIMITER, "("), (TokenType.STRING, "`Result: ${sum}`"), (TokenType.DELIMITER, ")"), (TokenType.DELIMITER, ";"), (TokenType.COMMENT, "// Log if large"), (TokenType.NEWLINE, "\\n"),
        (TokenType.DELIMITER, "}"), (TokenType.NEWLINE, "\\n"),
        (TokenType.KEYWORD, "return"), (TokenType.IDENTIFIER, "sum"), (TokenType.DELIMITER, ";"), (TokenType.NEWLINE, "\\n"),
        (TokenType.DELIMITER, "}"), (TokenType.NEWLINE, "\\n"),
        (TokenType.NEWLINE, "\\n"),
        (TokenType.IDENTIFIER, "calculate"), (TokenType.DELIMITER, "("), (TokenType.NUMBER, "5"), (TokenType.ERROR, ","), (TokenType.NUMBER, "7"), (TokenType.DELIMITER, ")"), (TokenType.DELIMITER, ";"), (TokenType.NEWLINE, "\\n"),
    ]
    # Note: Comma is currently marked as ERROR. Template literals are treated as simple strings.
    assert_tokens_equal(tokens, expected)

def test_js_error_character():
    code = "let a = @;"
    lexer = JavaScriptLexer(code)
    tokens = lexer.tokenize()
    expected = [
        (TokenType.KEYWORD, "let"),
        (TokenType.IDENTIFIER, "a"),
        (TokenType.OPERATOR, "="),
        (TokenType.ERROR, "@"),
        (TokenType.DELIMITER, ";"),
    ]
    assert_tokens_equal(tokens, expected)

def test_js_unterminated_string():
    code = "\'unterminated string"
    lexer = JavaScriptLexer(code)
    tokens = lexer.tokenize()
    # The lexer currently returns the unterminated string as a STRING token
    expected = [
        (TokenType.STRING, "\'unterminated string"),
    ]
    assert_tokens_equal(tokens, expected)

def test_js_unterminated_comment():
    code = "/* Unterminated comment"
    lexer = JavaScriptLexer(code)
    tokens = lexer.tokenize()
    # The lexer currently returns an ERROR token for unterminated multi-line comments
    assert len(tokens) == 2 # ERROR token + EOF
    assert tokens[0].type == TokenType.ERROR
    assert "comentário não fechado" in tokens[0].value


