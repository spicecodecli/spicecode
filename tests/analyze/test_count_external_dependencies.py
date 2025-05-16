from spice.analyzers.count_external_dependencies import count_external_dependencies

def test_python_imports():
    code = "import os\nfrom sys import argv\n"
    with open("temp_test.py", "w") as f:
        f.write(code)
    assert count_external_dependencies("temp_test.py") == 2

def test_js_imports():
    code = "const fs = require('fs');\nimport x from 'y';\n"
    with open("temp_test.js", "w") as f:
        f.write(code)
    assert count_external_dependencies("temp_test.js") == 2

def test_js_imports_zero():
    code = ""
    with open("temp_test.js", "w") as f:
        f.write(code)
    assert count_external_dependencies("temp_test.js") == 0