# import pytest
# from lexers.ruby.rubylexer import RubyLexer
# from lexers.token import TokenType

# # Helper function to compare token lists, ignoring EOF (similar to Python lexer test)
# def assert_tokens_equal(actual_tokens, expected_tokens_data):
#     if actual_tokens and actual_tokens[-1].type == TokenType.EOF:
#         actual_tokens = actual_tokens[:-1]
    
#     assert len(actual_tokens) == len(expected_tokens_data), \
#         f"Expected {len(expected_tokens_data)} tokens, but got {len(actual_tokens)}\nActual: {actual_tokens}\nExpected data: {expected_tokens_data}"
    
#     for i, (token_type, value) in enumerate(expected_tokens_data):
#         assert actual_tokens[i].type == token_type, f"Token {i} type mismatch: Expected {token_type}, got {actual_tokens[i].type} ({actual_tokens[i].value})"
#         assert actual_tokens[i].value == value, f"Token {i} value mismatch: Expected '{value}', got '{actual_tokens[i].value}'"

# # --- Test Cases ---

# def test_ruby_empty_input():
#     lexer = RubyLexer("")
#     tokens = lexer.tokenize()
#     assert len(tokens) == 1
#     assert tokens[0].type == TokenType.EOF

# def test_ruby_keywords():
#     code = "def end if else elsif unless while until for do return break next class module begin rescue ensure yield self nil true false super then case when"
#     lexer = RubyLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.KEYWORD, "def"), (TokenType.KEYWORD, "end"), (TokenType.KEYWORD, "if"), (TokenType.KEYWORD, "else"), 
#         (TokenType.KEYWORD, "elsif"), (TokenType.KEYWORD, "unless"), (TokenType.KEYWORD, "while"), (TokenType.KEYWORD, "until"), 
#         (TokenType.KEYWORD, "for"), (TokenType.KEYWORD, "do"), (TokenType.KEYWORD, "return"), (TokenType.KEYWORD, "break"), 
#         (TokenType.KEYWORD, "next"), (TokenType.KEYWORD, "class"), (TokenType.KEYWORD, "module"), (TokenType.KEYWORD, "begin"), 
#         (TokenType.KEYWORD, "rescue"), (TokenType.KEYWORD, "ensure"), (TokenType.KEYWORD, "yield"), (TokenType.KEYWORD, "self"), 
#         (TokenType.BOOLEAN, "nil"), (TokenType.BOOLEAN, "true"), (TokenType.BOOLEAN, "false"), (TokenType.KEYWORD, "super"), 
#         (TokenType.KEYWORD, "then"), (TokenType.KEYWORD, "case"), (TokenType.KEYWORD, "when")
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_ruby_identifiers():
#     code = "my_var _another_var var123 method? ALL_CAPS"
#     lexer = RubyLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.IDENTIFIER, "my_var"),
#         (TokenType.IDENTIFIER, "_another_var"),
#         (TokenType.IDENTIFIER, "var123"),
#         (TokenType.IDENTIFIER, "method?"), # Note: ? is allowed in Ruby identifiers
#         (TokenType.IDENTIFIER, "ALL_CAPS"),
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_ruby_numbers():
#     code = "123 45.67 0.5 1e3 2.5e-2 99"
#     lexer = RubyLexer(code)
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

# def test_ruby_strings():
#     code = "'hello' \"world\" \"with \\\"escape\\\"\" \"interp #{var} end\""
#     lexer = RubyLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.STRING, "'hello'"),
#         (TokenType.STRING, '"world"'),
#         (TokenType.STRING, '"with \\"escape\\""'), # String includes escapes
#         (TokenType.STRING, '"interp #{var} end"'), # String with interpolation (treated as single string token)
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_ruby_operators():
#     # Excluding and, or, not as they are handled differently
#     code = "+ - * / % = == != < > <= >= && || += -= *= /= %= ** **= & | ^ ~ << >> => .. ... !~ =~"
#     lexer = RubyLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.OPERATOR, "+"), (TokenType.OPERATOR, "-"), (TokenType.OPERATOR, "*"), (TokenType.OPERATOR, "/"), 
#         (TokenType.OPERATOR, "%"), (TokenType.OPERATOR, "="), (TokenType.OPERATOR, "=="), (TokenType.OPERATOR, "!="), 
#         (TokenType.OPERATOR, "<"), (TokenType.OPERATOR, ">"), (TokenType.OPERATOR, "<="), (TokenType.OPERATOR, ">="), 
#         (TokenType.OPERATOR, "&&"), (TokenType.OPERATOR, "||"), (TokenType.OPERATOR, "+="), (TokenType.OPERATOR, "-="), 
#         (TokenType.OPERATOR, "*="), (TokenType.OPERATOR, "/="), (TokenType.OPERATOR, "%="), (TokenType.OPERATOR, "**"), 
#         (TokenType.OPERATOR, "**="), (TokenType.OPERATOR, "&"), (TokenType.OPERATOR, "|"), (TokenType.OPERATOR, "^"), 
#         (TokenType.OPERATOR, "~"), (TokenType.OPERATOR, "<<"), (TokenType.OPERATOR, ">>"), (TokenType.OPERATOR, "=>"), 
#         (TokenType.OPERATOR, ".."), (TokenType.OPERATOR, "..."), (TokenType.OPERATOR, "!~"), (TokenType.OPERATOR, "=~")
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_ruby_delimiters():
#     code = "( ) { } [ ]"
#     lexer = RubyLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.DELIMITER, "("), (TokenType.DELIMITER, ")"),
#         (TokenType.DELIMITER, "{"), (TokenType.DELIMITER, "}"),
#         (TokenType.DELIMITER, "["), (TokenType.DELIMITER, "]"),
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_ruby_comments():
#     code = "# This is a comment\nx = 1 # Another comment"
#     lexer = RubyLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.COMMENT, "# This is a comment"),
#         (TokenType.NEWLINE, "\\n"),
#         (TokenType.IDENTIFIER, "x"),
#         (TokenType.OPERATOR, "="),
#         (TokenType.NUMBER, "1"),
#         (TokenType.COMMENT, "# Another comment"),
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_ruby_symbols():
#     code = ":symbol :another_symbol :+ :[] :[]= :<<"
#     lexer = RubyLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.SYMBOL, ":symbol"),
#         (TokenType.SYMBOL, ":another_symbol"),
#         (TokenType.SYMBOL, ":+"),
#         (TokenType.SYMBOL, ":[]"),
#         (TokenType.SYMBOL, ":[]="),
#         (TokenType.SYMBOL, ":<<"),
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_ruby_instance_class_variables():
#     code = "@instance @@class_var @another"
#     lexer = RubyLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.INSTANCE_VAR, "@instance"),
#         (TokenType.INSTANCE_VAR, "@@class_var"), # Lexer currently identifies @@var as INSTANCE_VAR
#         (TokenType.INSTANCE_VAR, "@another"),
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_ruby_global_variables():
#     code = "$global $! $LOAD_PATH"
#     lexer = RubyLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.GLOBAL_VAR, "$global"),
#         (TokenType.GLOBAL_VAR, "$!"), # Special global var
#         (TokenType.GLOBAL_VAR, "$LOAD_PATH"),
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_ruby_mixed_code():
#     code = """
# def calculate(x, y)
#   # Calculate sum
#   sum = x + y
#   puts "Result: #{sum}" if $DEBUG
#   return sum > 10 ? :large : :small
# end

# calculate(5, 7)
# """
#     lexer = RubyLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.NEWLINE, "\\n"),
#         (TokenType.KEYWORD, "def"), (TokenType.IDENTIFIER, "calculate"), (TokenType.DELIMITER, "("), (TokenType.IDENTIFIER, "x"), (TokenType.OPERATOR, ","), (TokenType.IDENTIFIER, "y"), (TokenType.DELIMITER, ")"), (TokenType.NEWLINE, "\\n"),
#         (TokenType.COMMENT, "# Calculate sum"), (TokenType.NEWLINE, "\\n"),
#         (TokenType.IDENTIFIER, "sum"), (TokenType.OPERATOR, "="), (TokenType.IDENTIFIER, "x"), (TokenType.OPERATOR, "+"), (TokenType.IDENTIFIER, "y"), (TokenType.NEWLINE, "\\n"),
#         (TokenType.IDENTIFIER, "puts"), (TokenType.STRING, '"Result: #{sum}"'), (TokenType.KEYWORD, "if"), (TokenType.GLOBAL_VAR, "$DEBUG"), (TokenType.NEWLINE, "\\n"),
#         (TokenType.KEYWORD, "return"), (TokenType.IDENTIFIER, "sum"), (TokenType.OPERATOR, ">"), (TokenType.NUMBER, "10"), (TokenType.OPERATOR, "?"), (TokenType.SYMBOL, ":large"), (TokenType.OPERATOR, ":"), (TokenType.SYMBOL, ":small"), (TokenType.NEWLINE, "\\n"),
#         (TokenType.KEYWORD, "end"), (TokenType.NEWLINE, "\\n"),
#         (TokenType.NEWLINE, "\\n"),
#         (TokenType.IDENTIFIER, "calculate"), (TokenType.DELIMITER, "("), (TokenType.NUMBER, "5"), (TokenType.OPERATOR, ","), (TokenType.NUMBER, "7"), (TokenType.DELIMITER, ")"), (TokenType.NEWLINE, "\\n"),
#     ]
#     # Note: The expected tokens assume the lexer handles commas and ternary operators correctly
#     # Adjust these expectations based on your actual lexer implementation
#     assert_tokens_equal(tokens, expected)

# def test_ruby_error_character():
#     code = "x = `backtick`"
#     lexer = RubyLexer(code)
#     tokens = lexer.tokenize()
#     expected = [
#         (TokenType.IDENTIFIER, "x"),
#         (TokenType.OPERATOR, "="),
#         (TokenType.ERROR, "`"), # Backtick is not explicitly handled
#         (TokenType.IDENTIFIER, "backtick"),
#         (TokenType.ERROR, "`"),
#     ]
#     assert_tokens_equal(tokens, expected)

# def test_ruby_unterminated_string():
#     code = '"unterminated string'
#     lexer = RubyLexer(code)
#     tokens = lexer.tokenize()
#     assert len(tokens) == 2 # ERROR token + EOF
#     assert tokens[0].type == TokenType.ERROR
#     assert "Unclosed string" in tokens[0].value