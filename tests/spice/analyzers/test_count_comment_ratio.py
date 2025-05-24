import pytest
import os
from spice.analyzers.count_comment_ratio import count_comment_ratio

# Define the path to the sample code directory relative to the test file
SAMPLE_CODE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "sample-code")

# Helper function to create a temporary file
def create_temp_file(content, filename="temp_test_file"):
    file_path = os.path.join(SAMPLE_CODE_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path

# Test cases for count_comment_ratio
@pytest.mark.parametrize(
    "filename, expected_ratio_str",
    [
        # Based on the content of sample files created earlier
        # ratio_sample.py: 5 comment lines (3 full, 2 inline) / 7 non-empty code lines = 71.43%
        ("ratio_sample.py", "71.43%"), 
        # ratio_sample.js: 5 comment lines (2 full, 2 multi, 1 inline) / 6 non-empty code lines = 83.33%
        ("ratio_sample.js", "83.33%"), 
        # ratio_sample.go: 5 comment lines (2 full, 2 multi, 1 inline) / 7 non-empty code lines = 71.43%
        ("ratio_sample.go", "71.43%"), 
        # ratio_sample.rb: 4 comment lines (3 full, 1 inline) / 6 non-empty code lines = 66.67% (Note: =begin/=end ignored by current analyzer)
        ("ratio_sample.rb", "66.67%"), 
    ]
)
def test_count_comment_ratio_sample_files(filename, expected_ratio_str):
    """Test count_comment_ratio with various sample files."""
    file_path = os.path.join(SAMPLE_CODE_DIR, filename)
    assert os.path.exists(file_path), f"Sample file not found: {file_path}"
    assert count_comment_ratio(file_path) == expected_ratio_str

def test_count_comment_ratio_empty_file():
    """Test count_comment_ratio with an empty file."""
    empty_file_path = create_temp_file("", "empty_ratio.tmp")
    assert count_comment_ratio(empty_file_path) == "0.00%"
    os.remove(empty_file_path)

def test_count_comment_ratio_no_comments():
    """Test count_comment_ratio with a file containing no comments."""
    no_comments_path = create_temp_file("print(\"Hello\")\nx = 1", "no_comments_ratio.py")
    assert count_comment_ratio(no_comments_path) == "0.00%"
    os.remove(no_comments_path)

def test_count_comment_ratio_all_comments():
    """Test count_comment_ratio with a file containing only comments."""
    all_comments_py = create_temp_file("# line 1\n# line 2", "all_comments_ratio.py")
    assert count_comment_ratio(all_comments_py) == "100.00%"
    os.remove(all_comments_py)
    
    all_comments_js = create_temp_file("// line 1\n/* line 2 */", "all_comments_ratio.js")
    assert count_comment_ratio(all_comments_js) == "100.00%"
    os.remove(all_comments_js)

def test_count_comment_ratio_unsupported_extension():
    """Test count_comment_ratio with an unsupported file extension."""
    unsupported_path = create_temp_file("# comment\ncode", "unsupported.txt")
    assert count_comment_ratio(unsupported_path) == "0.00%" # Should ignore the file
    os.remove(unsupported_path)

def test_count_comment_ratio_directory():
    """Test count_comment_ratio when given a directory path."""
    # It should analyze all supported files within the directory
    # Using SAMPLE_CODE_DIR which contains ratio_sample.* files
    # Total comments = 5(py) + 5(js) + 5(go) + 4(rb) = 19
    # Total lines = 7(py) + 6(js) + 7(go) + 6(rb) = 26
    # Ratio = (19 / 26) * 100 = 73.08%
    # Note: This depends on the exact content and assumes no other supported files exist there
    # We might need a dedicated test directory for more reliable results
    # For now, let's test based on the known sample files
    # Re-calculate based ONLY on the ratio_sample files created:
    # Py: 5 comments / 7 lines
    # JS: 5 comments / 6 lines
    # Go: 5 comments / 7 lines
    # Rb: 4 comments / 6 lines
    # Total comments = 19, Total lines = 26
    # Ratio = 19 / 26 * 100 = 73.076... => 73.08%
    assert count_comment_ratio(SAMPLE_CODE_DIR) == "73.08%"


