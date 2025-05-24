import pytest
from lexers.token import Token, TokenType

# Test cases for Token initialization and attributes
@pytest.mark.parametrize(
    "token_type, value, line, column",
    [
        (TokenType.IDENTIFIER, "my_var", 1, 5),
        (TokenType.NUMBER, "123", 2, 10),
        (TokenType.STRING, '"hello"', 3, 1),
        (TokenType.OPERATOR, "+", 4, 15),
        (TokenType.COMMENT, "# a comment", 5, 0),
        (TokenType.NEWLINE, "\n", 6, 0),
        (TokenType.EOF, "", 7, 0),
    ],
)
def test_token_initialization(token_type, value, line, column):
    """Test that Token objects are initialized correctly with given attributes."""
    token = Token(token_type, value, line, column)
    assert token.type == token_type
    assert token.value == value
    assert token.line == line
    assert token.column == column

# Test cases for Token representation
@pytest.mark.parametrize(
    "token_type, value, line, column, expected_repr",
    [
        (
            TokenType.IDENTIFIER,
            "my_var",
            1,
            5,
            "Token(TokenType.IDENTIFIER, 'my_var', 1:5)",
        ),
        (TokenType.NUMBER, "123", 2, 10, "Token(TokenType.NUMBER, '123', 2:10)"),
        (
            TokenType.STRING,
            '"hello"',
            3,
            1,
            "Token(TokenType.STRING, '\"hello\"', 3:1)",
        ),
        (TokenType.OPERATOR, "+", 4, 15, "Token(TokenType.OPERATOR, '+', 4:15)"),
        (
            TokenType.COMMENT,
            "# a comment",
            5,
            0,
            "Token(TokenType.COMMENT, '# a comment', 5:0)",
        ),
        (TokenType.NEWLINE, "\n", 6, 0, "Token(TokenType.NEWLINE, '\\n', 6:0)"),
        (TokenType.EOF, "", 7, 0, "Token(TokenType.EOF, '', 7:0)"),
    ],
)
def test_token_repr(token_type, value, line, column, expected_repr):
    """Test the __repr__ method of the Token class."""
    token = Token(token_type, value, line, column)
    assert repr(token) == expected_repr


