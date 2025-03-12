import unittest
import os
import sys
from unittest.mock import patch, mock_open, MagicMock

# Add the parent directory to sys.path to import your module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import after adjusting the path
from cli.main import get_translation

# Get the LANG_FILE path directly from your module
from cli.main import LANG_FILE

class TestGetTranslation(unittest.TestCase):
    
    @patch('cli.main.os.path.exists')
    @patch('cli.main.open', new_callable=mock_open, read_data='en')
    @patch('cli.main.importlib.import_module')
    def test_get_translation_with_existing_file_en(self, mock_importlib, mock_file, mock_exists):
        # Setup mocks
        mock_exists.return_value = True
        mock_module = MagicMock()
        mock_module.messages = {"test": "English message"}
        mock_importlib.return_value = mock_module
        
        # Call the function
        result = get_translation()
        
        # Assertions
        mock_exists.assert_called_once_with(LANG_FILE)
        mock_file.assert_called_once_with(LANG_FILE, 'r')
        mock_importlib.assert_called_once_with('cli.translations.en')
        self.assertEqual(result, {"test": "English message"})
    
    @patch('cli.main.os.path.exists')
    @patch('cli.main.open', new_callable=mock_open, read_data='pt-br')
    @patch('cli.main.importlib.import_module')
    def test_get_translation_with_existing_file_pt_br(self, mock_importlib, mock_file, mock_exists):
        # Setup mocks
        mock_exists.return_value = True
        mock_module = MagicMock()
        mock_module.messages = {"test": "Portuguese message"}
        mock_importlib.return_value = mock_module
        
        # Call the function
        result = get_translation()
        
        # Assertions
        mock_exists.assert_called_once_with(LANG_FILE)
        mock_file.assert_called_once_with(LANG_FILE, 'r')
        mock_importlib.assert_called_once_with('cli.translations.pt-br')
        self.assertEqual(result, {"test": "Portuguese message"})
    
    @patch('cli.main.os.path.exists')
    @patch('cli.main.importlib.import_module')
    def test_get_translation_without_file(self, mock_importlib, mock_exists):
        # Setup mocks
        mock_exists.return_value = False
        mock_module = MagicMock()
        mock_module.messages = {"test": "Default English message"}
        mock_importlib.return_value = mock_module
        
        # Call the function
        result = get_translation()
        
        # Assertions
        mock_exists.assert_called_once_with(LANG_FILE)
        mock_importlib.assert_called_once_with('cli.translations.en')
        self.assertEqual(result, {"test": "Default English message"})
    
    @patch('cli.main.os.path.exists')
    @patch('cli.main.open', new_callable=mock_open, read_data='invalid_lang')
    @patch('cli.main.importlib.import_module')
    def test_get_translation_with_invalid_lang(self, mock_importlib, mock_file, mock_exists):
        # Setup mocks
        mock_exists.return_value = True
        
        def side_effect(module_name):
            if module_name == 'cli.translations.invalid_lang':
                raise ModuleNotFoundError("No module named 'cli.translations.invalid_lang'")
            mock_module = MagicMock()
            mock_module.messages = {"test": "Fallback English message"}
            return mock_module
        
        mock_importlib.side_effect = side_effect
        
        # Call the function
        result = get_translation()
        
        # Assertions
        mock_exists.assert_called_once_with(LANG_FILE)
        mock_file.assert_called_once_with(LANG_FILE, 'r')
        self.assertEqual(result, {"test": "Fallback English message"})

if __name__ == '__main__':
    unittest.main()