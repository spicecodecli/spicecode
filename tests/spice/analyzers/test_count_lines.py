import pytest
from spice.analyzers.count_lines import count_lines

# Test cases for count_lines function
@pytest.mark.parametrize(
    "code, expected_lines",
    [
        ("", 0),  # Empty string
        ("one line", 1),
        ("two\nlines", 2), # Unix newline
        ("three\r\nlines\r\nnow", 3), # Windows newline
        ("old\rmac\rlines", 3), # Old Mac newline
        ("mixed\nendings\r\nokay?", 3),
        ("line with no ending", 1),
        ("\n", 1), # Single newline character
        ("\n\n", 2), # Multiple empty lines
        ("  leading whitespace\n trailing whitespace  \n", 2),
        ("line1\nline2\n", 2), # Trailing newline doesn't add a line
        ("line1\nline2", 2),
    ]
)
def test_count_lines(code, expected_lines):
    """Test count_lines with various inputs and line endings."""
    assert count_lines(code) == expected_lines


