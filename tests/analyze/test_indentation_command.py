from typer.testing import CliRunner
from cli.main import app # Assuming 'app' is your Typer application instance in main.py
import json
import os

runner = CliRunner()

# Define the path to the sample code directory relative to this test file or use absolute paths
SAMPLE_CODE_DIR = os.path.join(os.path.dirname(__file__), "..", "sample-code")
PYTHON_SAMPLE_FILE = os.path.join(SAMPLE_CODE_DIR, "example.py")

def test_indentation_command_console_output():
    result = runner.invoke(app, ["indentation", "indentation", PYTHON_SAMPLE_FILE, "--format", "console"])
    assert result.exit_code == 0
    # Check for some expected keywords in console output
    assert "Indentation Analysis for" in result.stdout
    assert "example.py" in result.stdout
    assert "Indentation Details Per Line" in result.stdout
    assert "Line No." in result.stdout
    assert "Indent Level" in result.stdout
    assert "Content" in result.stdout
    # Check a specific line from example.py (assuming its content and indentation)
    # This requires knowing the content of example.py
    # For example, if line 1 of example.py is "import os" with 0 indent:
    # assert "1" in result.stdout and "0" in result.stdout and "import os" in result.stdout

def test_indentation_command_json_output():
    result = runner.invoke(app, ["indentation", "indentation", PYTHON_SAMPLE_FILE, "--format", "json"])
    assert result.exit_code == 0
    try:
        json_output = json.loads(result.stdout)
        assert isinstance(json_output, list) # The indentation analyzer returns a list of line details
        assert len(json_output) > 0 # Assuming example.py is not empty
        first_line_detail = json_output[0]
        assert "original_line_number" in first_line_detail
        assert "line_content" in first_line_detail
        assert "stripped_line_content" in first_line_detail
        assert "indent_level" in first_line_detail
        assert "is_empty_or_whitespace_only" in first_line_detail
    except json.JSONDecodeError:
        assert False, "JSON output was not valid."

def test_indentation_command_file_not_found():
    result = runner.invoke(app, ["indentation", "indentation", "non_existent_file.py"])
    assert result.exit_code == 1
    assert "Error: File not found" in result.stdout # Or the translated equivalent

# To run these tests, you would typically use pytest from the root of your project.
# Ensure that PYTHONPATH is set up correctly if you run pytest from a different directory.

