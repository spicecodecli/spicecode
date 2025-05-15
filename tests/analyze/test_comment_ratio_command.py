from typer.testing import CliRunner
from cli.main import app
import json
import os

runner = CliRunner()

SAMPLE_CODE_DIR = os.path.join(os.path.dirname(__file__), "..", "sample-code")
PYTHON_SAMPLE_FILE = os.path.join(SAMPLE_CODE_DIR, "example.py")

def test_comment_ratio_command_console_output():
    result = runner.invoke(app, ["ratio", "ratio", PYTHON_SAMPLE_FILE, "--format", "console"])
    assert result.exit_code == 0
    assert "Comment/Code Ratio Analysis for" in result.stdout
    assert "example.py" in result.stdout
    assert "Summary Statistics" in result.stdout
    assert "Total Lines" in result.stdout
    assert "Code Lines" in result.stdout
    assert "Comment Lines" in result.stdout
    assert "Comment/Code Ratio" in result.stdout
    assert "Line-by-Line Classification" in result.stdout

def test_comment_ratio_command_json_output():
    result = runner.invoke(app, ["ratio", "ratio", PYTHON_SAMPLE_FILE, "--format", "json"])
    assert result.exit_code == 0
    try:
        json_output = json.loads(result.stdout)
        assert "line_by_line_analysis" in json_output
        assert "summary_stats" in json_output
        assert isinstance(json_output["line_by_line_analysis"], list)
        assert isinstance(json_output["summary_stats"], dict)
        assert "total_lines_in_file" in json_output["summary_stats"]
        assert "code_lines" in json_output["summary_stats"]
        assert "comment_only_lines" in json_output["summary_stats"]
        assert "comment_to_code_plus_comment_ratio" in json_output["summary_stats"]
    except json.JSONDecodeError:
        assert False, "JSON output was not valid."

def test_comment_ratio_command_file_not_found():
    result = runner.invoke(app, ["ratio", "ratio", "non_existent_file.py"])
    assert result.exit_code == 1
    assert "Error: File not found" in result.stdout # Or the translated equivalent

