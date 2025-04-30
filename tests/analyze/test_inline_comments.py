import os
from spice.analyzers.count_inline_comments import count_inline_comments

# Get path to the sample files
SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "sample-code")
PY_SAMPLE = os.path.join(SAMPLES_DIR, "example.py")
JS_SAMPLE = os.path.join(SAMPLES_DIR, "example.js")
GO_SAMPLE = os.path.join(SAMPLES_DIR, "example.go")
RB_SAMPLE = os.path.join(SAMPLES_DIR, "example.rb")

def test_count_inline_comments_python():
    """Test counting inline comments in Python code."""
    count = count_inline_comments(PY_SAMPLE)
    assert count == 2, f"Expected 2 inline comments in Python sample, got {count}"

def test_count_inline_comments_javascript():
    """Test counting inline comments in JavaScript code."""
    count = count_inline_comments(JS_SAMPLE)
    assert count == 2, f"Expected 2 inline comments in JavaScript sample, got {count}"

def test_count_inline_comments_go():
    """Test counting inline comments in Go code."""
    count = count_inline_comments(GO_SAMPLE)
    assert count == 1, f"Expected 1 inline comment in Go sample, got {count}"

def test_count_inline_comments_ruby():
    """Test counting inline comments in Ruby code."""
    count = count_inline_comments(RB_SAMPLE)
    assert count == 1, f"Expected 1 inline comment in Ruby sample, got {count}"

def test_count_inline_comments_nonexistent_file():
    """Test counting inline comments in a nonexistent file."""
    try:
        count_inline_comments("nonexistent_file.py")
        assert False, "Expected FileNotFoundError for nonexistent file"
    except FileNotFoundError:
        # Expected behavior
        pass

def test_count_inline_comments_empty_string():
    """Test counting inline comments in an empty file."""
    # Create a temporary empty file
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp:
        temp_name = temp.name
    
    try:
        count = count_inline_comments(temp_name)
        assert count == 0, f"Expected 0 inline comments in empty file, got {count}"
    finally:
        # Clean up the temporary file
        os.unlink(temp_name)
        
def test_count_inline_comments_with_only_inline_comments():
    """Test counting inline comments in a file with only inline comments."""
    # Create a temporary file with only inline comments
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp:
        temp.write(b"x = 5  # This is an inline comment\n")
        temp.write(b"y = 10  # This is another inline comment\n")
        temp.write(b"z = 15  # This is yet another inline comment\n")
        temp_name = temp.name
    
    try:
        count = count_inline_comments(temp_name)
        assert count == 3, f"Expected 3 inline comments in file with only inline comments, got {count}"
    finally:
        # Clean up the temporary file
        os.unlink(temp_name)
        
def test_count_inline_comments_with_mixed_comments():
    """Test counting inline comments in a file with both regular and inline comments."""
    # Create a temporary file with mixed comments
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp:
        temp.write(b"# This is a regular comment\n")
        temp.write(b"x = 5  # This is an inline comment\n")
        temp.write(b"# This is another regular comment\n")
        temp.write(b"y = 10  # This is another inline comment\n")
        temp_name = temp.name
    
    try:
        count = count_inline_comments(temp_name)
        assert count == 2, f"Expected 2 inline comments in file with mixed comments, got {count}"
    finally:
        # Clean up the temporary file
        os.unlink(temp_name) 