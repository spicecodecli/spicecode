from typer.testing import CliRunner
from cli.main import app
import json
import os

runner = CliRunner()

SAMPLE_CODE_DIR = os.path.join(os.path.dirname(__file__), "..", "sample-code")
PYTHON_SAMPLE_FILE = os.path.join(SAMPLE_CODE_DIR, "example.py")

def test_dependencies_command_console_output():
    result = runner.invoke(app, ["dependencies", "dependencies", PYTHON_SAMPLE_FILE, "--format", "console"])
    assert result.exit_code == 0
    assert "Dependency Analysis for" in result.stdout
    assert "example.py" in result.stdout
    assert "Dependencies Found" in result.stdout
    # example.py imports os, sys, json, re, math
    assert "os" in result.stdout
    assert "sys" in result.stdout
    assert "json" in result.stdout
    assert "re" in result.stdout
    assert "math" in result.stdout

def test_dependencies_command_json_output():
    result = runner.invoke(app, ["dependencies", "dependencies", PYTHON_SAMPLE_FILE, "--format", "json"])
    assert result.exit_code == 0
    try:
        json_output = json.loads(result.stdout)
        assert isinstance(json_output, list) # The dependency analyzer returns a list of imports
        assert "os" in json_output
        assert "sys" in json_output
        assert "json" in json_output
        assert "re" in json_output
        assert "math" in json_output
    except json.JSONDecodeError:
        assert False, "JSON output was not valid."

def test_dependencies_command_file_not_found():
    result = runner.invoke(app, ["dependencies", "dependencies", "non_existent_file.py"])
    assert result.exit_code == 1
    assert "Error: File not found" in result.stdout # Or the translated equivalent

