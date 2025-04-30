import json
import os
from typer.testing import CliRunner
from cli.main import app
from cli.commands.analyze import analyze_to_json

# Setup test runner
runner = CliRunner()

# Get the absolute path to the sample file
SAMPLE_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "sample-code", "example.py")

# Get path to the sample files
SAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "sample-code")
PY_SAMPLE = os.path.join(SAMPLES_DIR, "example.py")

def test_analyze_command_with_json_flag():
    """Test the analyze command with the --json flag for Python"""
    # Run the command with --json flag
    result = runner.invoke(app, ["analyze", SAMPLE_FILE_PATH, "--json"])
    
    # Check if the command executed successfully
    assert result.exit_code == 0
    
    # Parse the JSON output
    output = json.loads(result.stdout)
    
    # Check if all expected stats are in the output
    assert "file_name" in output
    assert "line_count" in output
    assert "comment_line_count" in output
    assert "function_count" in output
    assert "inline_comment_count" in output
    
    # Verify the values match expected results
    assert output["file_name"] == os.path.basename(SAMPLE_FILE_PATH)
    assert output["line_count"] == 161
    assert output["comment_line_count"] == 25
    assert output["function_count"] == 17
    assert output["inline_comment_count"] == 2

def test_analyze_command_with_all_and_json_flags():
    """Test the analyze command with both --all and --json flags for Python"""
    # Run the command with both flags
    result = runner.invoke(app, ["analyze", SAMPLE_FILE_PATH, "--all", "--json"])
    
    # Check if the command executed successfully
    assert result.exit_code == 0
    
    # Parse the JSON output
    output = json.loads(result.stdout)
    
    # Verify the values match expected results
    assert output["line_count"] == 161
    assert output["comment_line_count"] == 25
    assert output["function_count"] == 17
    assert output["inline_comment_count"] == 2

def test_analyze_command_with_nonexistent_file():
    """Test the analyze command with a nonexistent file"""
    # Run the command with a file that doesn't exist
    result = runner.invoke(app, ["analyze", "nonexistent_file.py", "--json"])
    
    # Parse the JSON output (should contain an error)
    output = json.loads(result.stdout)
    
    # Check if the output contains an error message
    assert "error" in output

def test_analyze_json_python():
    result = analyze_to_json(PY_SAMPLE, ["line_count", "function_count", "comment_line_count", "blank_line_count", "inline_comment_count", "external_dependencies_count"])
    
    json_obj = json.loads(result)
    assert isinstance(json_obj, dict)
    assert PY_SAMPLE in json_obj
    
    stats = json_obj[PY_SAMPLE]
    assert isinstance(stats, dict)
    assert "line_count" in stats
    assert "function_count" in stats
    assert "comment_line_count" in stats
    assert "blank_line_count" in stats
    assert "inline_comment_count" in stats
    assert "external_dependencies_count" in stats
    
    assert isinstance(stats["line_count"], int)
    assert isinstance(stats["function_count"], int)
    assert isinstance(stats["comment_line_count"], int)
    assert isinstance(stats["blank_line_count"], int)
    assert isinstance(stats["inline_comment_count"], int)
    assert isinstance(stats["external_dependencies_count"], int)
    
    assert stats["line_count"] > 0
    assert stats["function_count"] >= 0
    assert stats["comment_line_count"] >= 0
    assert stats["blank_line_count"] >= 0
    assert stats["inline_comment_count"] == 2
    # This assertion depends on the content of example.py
    # If the sample file has external dependencies, this should be adjusted accordingly
    assert isinstance(stats["external_dependencies_count"], int)
