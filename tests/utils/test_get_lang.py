import pytest
import os
from utils.get_lang import get_lexer_for_file

# Define test cases for supported file extensions
@pytest.mark.parametrize(
    "filename, expected_lang",
    [
        ("test.rb", "ruby"),
        ("test.py", "python"),
        ("test.js", "javascript"),
        ("test.go", "go"),
        ("/path/to/some/file.py", "python"),
        ("nodir.js", "javascript"),
    ],
)
def test_get_lexer_for_supported_files(filename, expected_lang):
    """Test get_lexer_for_file with supported file extensions."""
    assert get_lexer_for_file(filename) == expected_lang

# Define test cases for unsupported file extensions
@pytest.mark.parametrize(
    "filename",
    [
        "test.txt",
        "test.java",
        "test",
        "test.",
        ".bashrc",
        "/path/to/unsupported.ext",
    ],
)
def test_get_lexer_for_unsupported_files(filename):
    """Test get_lexer_for_file raises ValueError for unsupported extensions."""
    with pytest.raises(ValueError) as excinfo:
        get_lexer_for_file(filename)
    assert "Unsupported file extension:" in str(excinfo.value)

def test_get_lexer_for_file_no_extension():
    """Test get_lexer_for_file raises ValueError when there is no extension."""
    with pytest.raises(ValueError) as excinfo:
        get_lexer_for_file("file_without_extension")
    assert "Unsupported file extension:" in str(excinfo.value)

def test_get_lexer_for_file_hidden_file():
    """Test get_lexer_for_file with a hidden file (e.g., .gitignore)."""
    with pytest.raises(ValueError) as excinfo:
        get_lexer_for_file(".gitignore")
    # Assuming '.gitignore' is treated as having no extension or an unsupported one
    assert "Unsupported file extension:" in str(excinfo.value)


