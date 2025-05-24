# import pytest
# import os
# from spice.analyzers.count_inline_comments import count_inline_comments

# # Define the path to the sample code directory relative to the test file
# SAMPLE_CODE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "sample-code")

# # Helper function to create a temporary file
# def create_temp_file(content, filename="temp_inline_test_file"):
#     file_path = os.path.join(SAMPLE_CODE_DIR, filename)
#     with open(file_path, "w", encoding="utf-8") as f:
#         f.write(content)
#     return file_path

# # Test cases for count_inline_comments
# @pytest.mark.parametrize(
#     "filename, expected_inline_comments",
#     [
#         # Based on the content of ratio_sample.* files
#         ("ratio_sample.py", 2), # `import sys # ...`, `y = 2 # ...`
#         ("ratio_sample.js", 2), # `const x = 1; // ...`, `let y = 2; // ...`
#         ("ratio_sample.go", 2), # `package main // ...`, `func main() { // ...`
#         ("ratio_sample.rb", 3), # `require ... # ...`, `x * 2 # ...`, `puts ... # ...`
#         # Based on func_sample.* files
#         ("func_sample.py", 0), # No inline comments in this specific sample
#         ("func_sample.js", 0), # No inline comments in this specific sample
#         ("func_sample.go", 0), # No inline comments in this specific sample
#         ("func_sample.rb", 0), # No inline comments in this specific sample
#         # Based on original example.* files
#         ("example.py", 1), # `print("Hello, Python!") # Output greeting`
#         ("example.js", 1), # `console.log("Hello, JavaScript!"); // Output greeting`
#         ("example.go", 1), # `fmt.Println("Hello, Go!") // Output greeting`
#         ("example.rb", 1), # `puts "Hello, Ruby!" # Output greeting`
#     ]
# )
# def test_count_inline_comments_sample_files(filename, expected_inline_comments):
#     """Test count_inline_comments with various sample files."""
#     file_path = os.path.join(SAMPLE_CODE_DIR, filename)
#     assert os.path.exists(file_path), f"Sample file not found: {file_path}"
#     assert count_inline_comments(file_path) == expected_inline_comments

# def test_count_inline_comments_empty_file():
#     """Test count_inline_comments with an empty file."""
#     empty_file_path = create_temp_file("", "empty_inline.tmp")
#     assert count_inline_comments(empty_file_path) == 0
#     os.remove(empty_file_path)

# def test_count_inline_comments_no_comments():
#     """Test count_inline_comments with a file containing no comments."""
#     no_comments_path = create_temp_file("print(\"Hello\")\nx = 1", "no_comments_inline.py")
#     assert count_inline_comments(no_comments_path) == 0
#     os.remove(no_comments_path)

# def test_count_inline_comments_only_full_line():
#     """Test count_inline_comments with only full-line comments."""
#     full_line_comments_path = create_temp_file("# line 1\n# line 2", "full_line_inline.py")
#     assert count_inline_comments(full_line_comments_path) == 0
#     os.remove(full_line_comments_path)

# def test_count_inline_comments_mixed():
#     """Test count_inline_comments with mixed comment types."""
#     mixed_path = create_temp_file("# full line\nx = 1 # inline\n# another full line\ny=2", "mixed_inline.py")
#     assert count_inline_comments(mixed_path) == 1
#     os.remove(mixed_path)

# def test_count_inline_comments_unsupported_extension():
#     """Test count_inline_comments with an unsupported file extension."""
#     unsupported_path = create_temp_file("code # inline comment", "unsupported_inline.txt")
#     # Should raise ValueError because lexer cannot be found
#     with pytest.raises(ValueError):
#         count_inline_comments(unsupported_path)
#     os.remove(unsupported_path)


