import json
import os
from typer.testing import CliRunner
from cli.main import app

# Setup test runner
runner = CliRunner()

# Get the absolute path to the sample file
SAMPLE_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "sample-code", "example.rb")

def test_analyze_command_with_json_flag():
    """Test the analyze command with the --json flag for Ruby"""
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
    
    # Verify the values match expected results
    assert output["file_name"] == os.path.basename(SAMPLE_FILE_PATH)
    assert output["line_count"] == 226
    assert output["comment_line_count"] == 29
    assert output["function_count"] == 29

def test_analyze_command_with_all_and_json_flags():
    """Test the analyze command with both --all and --json flags for Ruby"""
    # Run the command with both flags
    result = runner.invoke(app, ["analyze", SAMPLE_FILE_PATH, "--all", "--json"])
    
    # Check if the command executed successfully
    assert result.exit_code == 0
    
    # Parse the JSON output
    output = json.loads(result.stdout)
    
    # Verify the values match expected results
    assert output["line_count"] == 226
    assert output["comment_line_count"] == 29
    assert output["function_count"] == 29

def test_analyze_command_with_nonexistent_file():
    """Test the analyze command with a nonexistent file"""
    # Run the command with a file that doesn't exist
    result = runner.invoke(app, ["analyze", "nonexistent_file.rb", "--json"])
    
    # Parse the JSON output (should contain an error)
    output = json.loads(result.stdout)
    
    # Check if the output contains an error message
    assert "error" in output
