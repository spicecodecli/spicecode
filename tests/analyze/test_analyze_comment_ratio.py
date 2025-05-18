from spice.analyzers.count_comment_ratio import count_comment_ratio
import os

def test_count_comment_ratio():
    # python
    py_code = """
        # This is a comment
        def foo():
            pass  # Inline comment
    """
    with open("temp_test.py", "w") as f:
        f.write(py_code)
    assert count_comment_ratio("temp_test.py") == "66.67%"
    os.remove("temp_test.py")

    # javascript
    js_code = """
        // This is a comment
        function foo() {
            return 42; // Inline comment
        }
        /*
        Multi-line
        comment
        */
    """
    with open("temp_test.js", "w") as f:
        f.write(js_code)
    assert count_comment_ratio("temp_test.js") == "75.00%"
    os.remove("temp_test.js")

    # go
    go_code = """
        // This is a comment
        func foo() int {
            return 42 // Inline comment
        }
        /*
        Multi-line
        comment
        */
    """
    with open("temp_test.go", "w") as f:
        f.write(go_code)
    assert count_comment_ratio("temp_test.go") == "75.00%"
    os.remove("temp_test.go")

    # ruby
    rb_code = """
        # This is a comment
        def foo
        42 # Inline comment
        end
    """
    with open("temp_test.rb", "w") as f:
        f.write(rb_code)
    assert count_comment_ratio("temp_test.rb") == "50.00%"
    os.remove("temp_test.rb")