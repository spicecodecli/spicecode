# import pytest
# import os
# from spice.analyzers.count_comment_lines import count_comment_lines

# # Define the path to the sample code directory relative to the test file
# SAMPLE_CODE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "sample-code")

# # Test cases for count_comment_lines
# @pytest.mark.parametrize(
#     "filename, expected_comment_lines",
#     [
#         ("sample_comments.py", 4), # Based on the content of sample_comments.py
#         ("example.py", 1), # Based on the content of example.py (assuming it has one full comment line)
#         ("example.js", 2), # Based on the content of example.js (assuming two full comment lines)
#         ("example.go", 2), # Based on the content of example.go (assuming two full comment lines)
#         ("example.rb", 1), # Based on the content of example.rb (assuming one full comment line)
#     ]
# )
# def test_count_comment_lines_python(filename, expected_comment_lines):
#     """Test count_comment_lines with various sample files."""
#     file_path = os.path.join(SAMPLE_CODE_DIR, filename)
#     # Ensure the sample file exists before running the test
#     assert os.path.exists(file_path), f"Sample file not found: {file_path}"
#     assert count_comment_lines(file_path) == expected_comment_lines

# def test_count_comment_lines_empty_file():
#     """Test count_comment_lines with an empty file."""
#     empty_file_path = os.path.join(SAMPLE_CODE_DIR, "empty_test_file.py")
#     with open(empty_file_path, "w") as f:
#         f.write("")
#     assert count_comment_lines(empty_file_path) == 0
#     os.remove(empty_file_path) # Clean up the empty file

# def test_count_comment_lines_no_comments():
#     """Test count_comment_lines with a file containing no comments."""
#     no_comments_path = os.path.join(SAMPLE_CODE_DIR, "no_comments_test_file.py")
#     with open(no_comments_path, "w") as f:
#         f.write("print(\"Hello\")\nx = 1")
#     assert count_comment_lines(no_comments_path) == 0
#     os.remove(no_comments_path) # Clean up

# def test_count_comment_lines_only_inline():
#     """Test count_comment_lines with only inline comments."""
#     inline_comments_path = os.path.join(SAMPLE_CODE_DIR, "inline_comments_test_file.py")
#     with open(inline_comments_path, "w") as f:
#         f.write("x = 1 # inline\ny = 2 # another inline")
#     assert count_comment_lines(inline_comments_path) == 0
#     os.remove(inline_comments_path) # Clean up


