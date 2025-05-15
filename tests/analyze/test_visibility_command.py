from typer.testing import CliRunner
from cli.main import app
import json
import os

runner = CliRunner()

SAMPLE_CODE_DIR = os.path.join(os.path.dirname(__file__), "..", "sample-code")
PYTHON_SAMPLE_FILE = os.path.join(SAMPLE_CODE_DIR, "example.py") # example.py should have some functions and maybe a class

def test_visibility_command_console_output():
    result = runner.invoke(app, ["visibility", "visibility", PYTHON_SAMPLE_FILE, "--format", "console"])
    assert result.exit_code == 0
    assert "Visibility Analysis for" in result.stdout
    assert "example.py" in result.stdout
    assert "Visibility Summary" in result.stdout
    assert "Public Functions" in result.stdout
    assert "Private Functions" in result.stdout
    assert "Public Methods" in result.stdout
    assert "Private Methods" in result.stdout
    assert "Details by Element" in result.stdout # This table might or might not appear if no elements are found

def test_visibility_command_json_output():
    result = runner.invoke(app, ["visibility", "visibility", PYTHON_SAMPLE_FILE, "--format", "json"])
    assert result.exit_code == 0
    try:
        json_output = json.loads(result.stdout)
        assert "public_functions" in json_output
        assert "private_functions" in json_output
        assert "public_methods" in json_output
        assert "private_methods" in json_output
        assert "details" in json_output
        assert isinstance(json_output["details"], list)
        # If example.py has elements, check one
        # if json_output["details"]:
        #     first_detail = json_output["details"][0]
        #     assert "name" in first_detail
        #     assert "type" in first_detail
        #     assert "visibility" in first_detail
        #     assert "lineno" in first_detail
    except json.JSONDecodeError:
        assert False, "JSON output was not valid."

def test_visibility_command_file_not_found():
    result = runner.invoke(app, ["visibility", "visibility", "non_existent_file.py"])
    assert result.exit_code == 1
    assert "Error: File not found" in result.stdout # Or the translated equivalent

