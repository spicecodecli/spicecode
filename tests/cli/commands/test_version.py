import pytest
import os
from unittest.mock import patch, mock_open, MagicMock
from typer.testing import CliRunner

# Assuming cli.main is the entry point for typer app
# We need to adjust imports based on actual structure if main.py is elsewhere
# Let's assume main.py exists and imports version_command correctly
# We will test the command function directly for simplicity here, 
# avoiding the need for a full typer app setup in this unit test.
from cli.commands.version import version_command

# Dummy translation messages
DUMMY_MESSAGES = {
    "version_info": "SpiceCode Version:",
    "version_not_found": "Version information not found in setup.py",
    "setup_not_found": "Error: setup.py not found.",
    "error": "Error:",
}

# Mock CURRENT_DIR (assuming it's the 'cli' directory for the command)
TEST_CURRENT_DIR = "/home/ubuntu/spicecode/cli"
EXPECTED_SETUP_PATH = "/home/ubuntu/spicecode/setup.py"

@patch("cli.commands.version.get_translation")
@patch("os.path.exists")
def test_version_command_success(mock_exists, mock_get_translation, capsys):
    """Test version command when setup.py exists and contains version."""
    mock_get_translation.return_value = DUMMY_MESSAGES
    mock_exists.return_value = True
    
    # Create file content with version line
    file_content = 'name="spicecode",\nversion="1.2.3",\nauthor="test"\n'
    
    # Use mock_open with read_data parameter
    with patch("builtins.open", mock_open(read_data=file_content)) as mock_file:
        version_command(LANG_FILE="dummy_lang.txt", CURRENT_DIR=TEST_CURRENT_DIR)
        
        captured = capsys.readouterr()
        
        mock_exists.assert_called_once_with(EXPECTED_SETUP_PATH)
        mock_file.assert_called_once_with(EXPECTED_SETUP_PATH, "r")
        assert "SpiceCode Version: 1.2.3" in captured.out

@patch("cli.commands.version.get_translation")
@patch("os.path.exists")
def test_version_command_version_not_in_setup(mock_exists, mock_get_translation, capsys):
    """Test version command when setup.py exists but lacks version info."""
    mock_get_translation.return_value = DUMMY_MESSAGES
    mock_exists.return_value = True
    
    # Create file content without version line
    file_content = 'name="spicecode",\nauthor="test",\ndescription="A CLI tool"\n'
    
    with patch("builtins.open", mock_open(read_data=file_content)) as mock_file:
        version_command(LANG_FILE="dummy_lang.txt", CURRENT_DIR=TEST_CURRENT_DIR)
        
        captured = capsys.readouterr()
        
        mock_exists.assert_called_once_with(EXPECTED_SETUP_PATH)
        mock_file.assert_called_once_with(EXPECTED_SETUP_PATH, "r")
        assert "Version information not found in setup.py" in captured.out

@patch("cli.commands.version.get_translation")
@patch("os.path.exists")
def test_version_command_setup_not_found(mock_exists, mock_get_translation, capsys):
    """Test version command when setup.py does not exist."""
    mock_get_translation.return_value = DUMMY_MESSAGES
    mock_exists.return_value = False

    version_command(LANG_FILE="dummy_lang.txt", CURRENT_DIR=TEST_CURRENT_DIR)
    
    captured = capsys.readouterr()
    
    mock_exists.assert_called_once_with(EXPECTED_SETUP_PATH)
    assert "Error: setup.py not found." in captured.out

@patch("cli.commands.version.get_translation")
@patch("os.path.exists")
def test_version_command_read_error(mock_exists, mock_get_translation, capsys):
    """Test version command handles exceptions during file reading."""
    mock_get_translation.return_value = DUMMY_MESSAGES
    mock_exists.return_value = True

    with patch("builtins.open", side_effect=OSError("Permission denied")) as mock_file:
        version_command(LANG_FILE="dummy_lang.txt", CURRENT_DIR=TEST_CURRENT_DIR)
        
        captured = capsys.readouterr()
        
        mock_exists.assert_called_once_with(EXPECTED_SETUP_PATH)
        mock_file.assert_called_once_with(EXPECTED_SETUP_PATH, "r")
        assert "Error: Permission denied" in captured.out


        