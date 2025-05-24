# import pytest
# from lexers.golang.golexer import GoLexer
# from lexers.token import TokenType

# # Helper function to compare token lists, ignoring EOF
# def assert_tokens_equal(actual_tokens, expected_tokens_data):
#     if actual_tokens and actual_tokens[-1].type == TokenType.EOF:
#         actual_tokens = actual_tokens[:-1]
    
#     assert len(actual_tokens) == len(expected_tokens_data), \
#         f"Expected {len(expected_tokens_data)} tokens, but got {len(actual_tokens)}\nActual: {actual_tokens}\nExpected data: {expected_tokens_data}"
    
#     for i, (token_type, value) in enumerate(expected_tokens_data):
#         assert actual_tokens[i].type == token_type, f"Token {i} type mismatch: Expected {token_type}, got {actual_tokens[i].type} ({actual_tokens[i].value})"
#         assert actual_tokens[i].value == value, f"Token {i} value mismatch: Expected '{value}', got '{actual_tokens[i].value}'"

# # --- Test Cases ---

# def test_go_empty_input():
#     lexer = GoLexer("")
#     tokens = lexer.tokenize()
#     assert len(tokens) == 1
#     assert tokens[0].type == TokenType.EOF

# def test_go_keywords():
#     code = "package import func var const type struct interface if else for range switch case default return break continue goto fallthrough defer go select chan map make new len cap append copy delete panic recover true false nil"
#     lexer = GoLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.KEYWORD, "package"), (TokenType.KEYWORD, "import"), (TokenType.KEYWORD, "func"), (TokenType.KEYWORD, "var"),
#         (TokenType.KEYWORD, "const"), (TokenType.KEYWORD, "type"), (TokenType.KEYWORD, "struct"), (TokenType.KEYWORD, "interface"),
#         (TokenType.KEYWORD, "if"), (TokenType.KEYWORD, "else"), (TokenType.KEYWORD, "for"), (TokenType.KEYWORD, "range"),
#         (TokenType.KEYWORD, "switch"), (TokenType.KEYWORD, "case"), (TokenType.KEYWORD, "default"), (TokenType.KEYWORD, "return"),
#         (TokenType.KEYWORD, "break"), (TokenType.KEYWORD, "continue"), (TokenType.KEYWORD, "goto"), (TokenType.KEYWORD, "fallthrough"),
#         (TokenType.KEYWORD, "defer"), (TokenType.KEYWORD, "go"), (TokenType.KEYWORD, "select"), (TokenType.KEYWORD, "chan"),
#         (TokenType.KEYWORD, "map"), (TokenType.KEYWORD, "make"), (TokenType.KEYWORD, "new"), (TokenType.KEYWORD, "len"),
#         (TokenType.KEYWORD, "cap"), (TokenType.KEYWORD, "append"), (TokenType.KEYWORD, "copy"), (TokenType.KEYWORD, "delete"),
#         (TokenType.KEYWORD, "panic"), (TokenType.KEYWORD, "recover"), (TokenType.KEYWORD, "true"), (TokenType.KEYWORD, "false"),
#         (TokenType.KEYWORD, "nil")
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_go_identifiers():
#     code = "myVar _anotherVar var123 _"
#     lexer = GoLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.IDENTIFIER, "myVar"),
#         (TokenType.IDENTIFIER, "_anotherVar"),
#         (TokenType.IDENTIFIER, "var123"),
#         (TokenType.IDENTIFIER, "_"),
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_go_numbers():
#     code = "123 45.67 0.5 1e3 2.5e-2 99"
#     lexer = GoLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.NUMBER, "123"),
#         (TokenType.NUMBER, "45.67"),
#         (TokenType.NUMBER, "0.5"),
#         (TokenType.NUMBER, "1e3"),
#         (TokenType.NUMBER, "2.5e-2"),
#         (TokenType.NUMBER, "99"),
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_go_strings():
#     code = "\"hello\" `raw string\nwith newline` \"with \\\"escape\\\"\""
#     lexer = GoLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.STRING, "\"hello\""),
#         (TokenType.STRING, "`raw string\nwith newline`"),
#         (TokenType.STRING, "\"with \\\"escape\\\"\""),
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_go_operators():
#     code = "+ - * / % = == != < > <= >= && || ! & | ^ << >> &^ += -= *= /= %= &= |= ^= <<= >>= &^= ++ -- := ... -> <-"
#     lexer = GoLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.OPERATOR, "+"), (TokenType.OPERATOR, "-"), (TokenType.OPERATOR, "*"), (TokenType.OPERATOR, "/"), (TokenType.OPERATOR, "%"),
#         (TokenType.OPERATOR, "="), (TokenType.OPERATOR, "=="), (TokenType.OPERATOR, "!="), (TokenType.OPERATOR, "<"), (TokenType.OPERATOR, ">"),
#         (TokenType.OPERATOR, "<="), (TokenType.OPERATOR, ">="), (TokenType.OPERATOR, "&&"), (TokenType.OPERATOR, "||"), (TokenType.OPERATOR, "!"),
#         (TokenType.OPERATOR, "&"), (TokenType.OPERATOR, "|"), (TokenType.OPERATOR, "^"), (TokenType.OPERATOR, "<<"), (TokenType.OPERATOR, ">>"),
#         (TokenType.OPERATOR, "&^"), (TokenType.OPERATOR, "+="), (TokenType.OPERATOR, "-="), (TokenType.OPERATOR, "*="), (TokenType.OPERATOR, "/="),
#         (TokenType.OPERATOR, "%="), (TokenType.OPERATOR, "&="), (TokenType.OPERATOR, "|="), (TokenType.OPERATOR, "^="), (TokenType.OPERATOR, "<<="),
#         (TokenType.OPERATOR, ">>="), (TokenType.OPERATOR, "&^="), (TokenType.OPERATOR, "++"), (TokenType.OPERATOR, "--"), (TokenType.OPERATOR, ":="),
#         (TokenType.OPERATOR, "..."), (TokenType.OPERATOR, "->"), (TokenType.OPERATOR, "<-")
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_go_delimiters():
#     code = "( ) { } [ ] , ; . :"
#     lexer = GoLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.DELIMITER, "("), (TokenType.DELIMITER, ")"),
#         (TokenType.DELIMITER, "{"), (TokenType.DELIMITER, "}"),
#         (TokenType.DELIMITER, "["), (TokenType.DELIMITER, "]"),
#         (TokenType.DELIMITER, ","), (TokenType.DELIMITER, ";"),
#         (TokenType.DELIMITER, "."), (TokenType.DELIMITER, ":"),
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_go_comments():
#     code = "// Single line comment\nvar x = 1 // Another comment\n/* Multi-line\n comment */ y := 2"
#     lexer = GoLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.COMMENT, "// Single line comment"), (TokenType.NEWLINE, "\\n"),
#         (TokenType.KEYWORD, "var"), (TokenType.IDENTIFIER, "x"), (TokenType.OPERATOR, "="), (TokenType.NUMBER, "1"), (TokenType.COMMENT, "// Another comment"), (TokenType.NEWLINE, "\\n"),
#         (TokenType.COMMENT, "/* Multi-line\n comment */"),
#         (TokenType.IDENTIFIER, "y"), (TokenType.OPERATOR, ":="), (TokenType.NUMBER, "2"),
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_go_mixed_code():
#     code = """
# package main

# import "fmt"

# func main() {
# 	// Declare and initialize
# 	message := "Hello, Go!"
# 	fmt.Println(message) // Print message
# 	num := 10 + 5
# 	if num > 10 {
# 		return
# 	}
# }
# """
#     lexer = GoLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.NEWLINE, "\\n"),
#         (TokenType.KEYWORD, "package"), (TokenType.IDENTIFIER, "main"), (TokenType.NEWLINE, "\\n"),
#         (TokenType.NEWLINE, "\\n"),
#         (TokenType.KEYWORD, "import"), (TokenType.STRING, "\"fmt\""), (TokenType.NEWLINE, "\\n"),
#         (TokenType.NEWLINE, "\\n"),
#         (TokenType.KEYWORD, "func"), (TokenType.IDENTIFIER, "main"), (TokenType.DELIMITER, "("), (TokenType.DELIMITER, ")"), (TokenType.DELIMITER, "{"), (TokenType.NEWLINE, "\\n"),
#         (TokenType.COMMENT, "// Declare and initialize"), (TokenType.NEWLINE, "\\n"),
#         (TokenType.IDENTIFIER, "message"), (TokenType.OPERATOR, ":="), (TokenType.STRING, "\"Hello, Go!\""), (TokenType.NEWLINE, "\\n"),
#         (TokenType.IDENTIFIER, "fmt"), (TokenType.DELIMITER, "."), (TokenType.IDENTIFIER, "Println"), (TokenType.DELIMITER, "("), (TokenType.IDENTIFIER, "message"), (TokenType.DELIMITER, ")"), (TokenType.COMMENT, "// Print message"), (TokenType.NEWLINE, "\\n"),
#         (TokenType.IDENTIFIER, "num"), (TokenType.OPERATOR, ":="), (TokenType.NUMBER, "10"), (TokenType.OPERATOR, "+"), (TokenType.NUMBER, "5"), (TokenType.NEWLINE, "\\n"),
#         (TokenType.KEYWORD, "if"), (TokenType.IDENTIFIER, "num"), (TokenType.OPERATOR, ">"), (TokenType.NUMBER, "10"), (TokenType.DELIMITER, "{"), (TokenType.NEWLINE, "\\n"),
#         (TokenType.KEYWORD, "return"), (TokenType.NEWLINE, "\\n"),
#         (TokenType.DELIMITER, "}"), (TokenType.NEWLINE, "\\n"),
#         (TokenType.DELIMITER, "}"), (TokenType.NEWLINE, "\\n"),
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_go_error_character():
#     code = "var a = @;"
#     lexer = GoLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.KEYWORD, "var"),
#         (TokenType.IDENTIFIER, "a"),
#         (TokenType.OPERATOR, "="),
#         (TokenType.ERROR, "@"),
#         (TokenType.DELIMITER, ";"),
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_go_unterminated_string():
#     code = "\"unterminated string"
#     lexer = GoLexer(code)
#     tokens = lexer.tokenize()
#     # Go lexer should return the unterminated string as a STRING token
#     expected = [
#         (TokenType.STRING, "\"unterminated string"),
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_go_unterminated_raw_string():
#     code = "`unterminated raw string"
#     lexer = GoLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.STRING, "`unterminated raw string"),
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_go_unterminated_comment():
#     code = "/* Unterminated comment"
#     lexer = GoLexer(code)
#     tokens = lexer.tokenize()
#     # Go lexer returns an ERROR token for unterminated multi-line comments
#     assert len(tokens) == 2 # ERROR token + EOF
#     assert tokens[0].type == TokenType.ERROR
#     assert "unterminated comment" in tokens[0].value.lower()