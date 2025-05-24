import pytest
import os
from unittest.mock import patch, mock_open, MagicMock
from utils.get_translation import get_translation

# Define a dummy LANG_FILE path for tests
TEST_LANG_FILE = "/tmp/test_lang.txt"

# Dummy translation messages for mocking
DUMMY_EN_MESSAGES = {"greeting": "Hello"}
DUMMY_PT_BR_MESSAGES = {"greeting": "Ola"}
DUMMY_FREMEN_MESSAGES = {"greeting": "Usul"}

@pytest.fixture(autouse=True)
def cleanup_lang_file():
    """Ensure the dummy lang file is removed after each test."""
    yield
    if os.path.exists(TEST_LANG_FILE):
        os.remove(TEST_LANG_FILE)

@patch("importlib.import_module")
@patch("os.path.exists")
def test_get_translation_valid_lang_file(mock_exists, mock_import):
    """Test get_translation when LANG_FILE exists and contains a valid language."""
    mock_exists.return_value = True
    # Mock the import based on language
    def side_effect(module_name):
        mock_module = MagicMock()
        if module_name == "cli.translations.pt-br":
            mock_module.messages = DUMMY_PT_BR_MESSAGES
        elif module_name == "cli.translations.fremen":
            mock_module.messages = DUMMY_FREMEN_MESSAGES
        else: # Default or fallback to 'en'
            mock_module.messages = DUMMY_EN_MESSAGES
        return mock_module
    mock_import.side_effect = side_effect

    # Test pt-br
    with patch("builtins.open", mock_open(read_data="pt-br")):
        messages = get_translation(TEST_LANG_FILE)
        assert messages == DUMMY_PT_BR_MESSAGES
        mock_import.assert_called_with("cli.translations.pt-br")

    # Test fremen
    with patch("builtins.open", mock_open(read_data="fremen\n")):
        messages = get_translation(TEST_LANG_FILE)
        assert messages == DUMMY_FREMEN_MESSAGES
        mock_import.assert_called_with("cli.translations.fremen")

@patch("importlib.import_module")
@patch("os.path.exists")
def test_get_translation_empty_lang_file(mock_exists, mock_import):
    """Test get_translation when LANG_FILE exists but is empty (defaults to en)."""
    mock_exists.return_value = True
    mock_en_module = MagicMock()
    mock_en_module.messages = DUMMY_EN_MESSAGES
    mock_import.return_value = mock_en_module

    with patch("builtins.open", mock_open(read_data="")):
        messages = get_translation(TEST_LANG_FILE)
        assert messages == DUMMY_EN_MESSAGES
        mock_import.assert_called_with("cli.translations.en")

@patch("importlib.import_module")
@patch("os.path.exists")
def test_get_translation_nonexistent_lang_file(mock_exists, mock_import):
    """Test get_translation when LANG_FILE does not exist (defaults to en)."""
    mock_exists.return_value = False
    mock_en_module = MagicMock()
    mock_en_module.messages = DUMMY_EN_MESSAGES
    mock_import.return_value = mock_en_module

    messages = get_translation(TEST_LANG_FILE)
    assert messages == DUMMY_EN_MESSAGES
    mock_import.assert_called_with("cli.translations.en")

@patch("importlib.import_module")
@patch("os.path.exists")
def test_get_translation_invalid_lang_code(mock_exists, mock_import):
    """Test get_translation when LANG_FILE contains an invalid language code (defaults to en)."""
    mock_exists.return_value = True
    mock_en_module = MagicMock()
    mock_en_module.messages = DUMMY_EN_MESSAGES
    # Simulate ModuleNotFoundError for the invalid lang, then return 'en' module
    mock_import.side_effect = [ModuleNotFoundError, mock_en_module]

    with patch("builtins.open", mock_open(read_data="invalid-lang")):
        messages = get_translation(TEST_LANG_FILE)
        assert messages == DUMMY_EN_MESSAGES
        # Check it tried invalid-lang first, then fell back to en
        assert mock_import.call_count == 2
        mock_import.assert_any_call("cli.translations.invalid-lang")
        mock_import.assert_called_with("cli.translations.en")


