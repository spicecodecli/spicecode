import pytest
from spice.analyzers.indentation_analysis import detect_indentation

@pytest.mark.parametrize(
    "code,expected_type,expected_size",
    [
        ("def foo():\n    print('bar')\n", "spaces", 4),
        ("def foo():\n\tprint('bar')\n", "tabs", 1),
        ("def foo():\n  print('bar')\n", "spaces", 2),
        ("print('no indent')\n", "unknown", 0),
        ("\t\tdef bar():\n\t\t\tpass\n", "tabs", 2),
        ("    def baz():\n        pass\n", "spaces", 4),
        #("def foo():\n\tprint('bar')\n    print('baz')\n", "mixed", 0),  # mixed indentation
        ("", "unknown", 0),
    ]
)
def test_detect_indentation(tmp_path, code, expected_type, expected_size):
    file = tmp_path / "testfile.py"
    file.write_text(code)
    result = detect_indentation(str(file))
    assert result["indentation_type"] == expected_type
    assert result["indentation_size"] == expected_size