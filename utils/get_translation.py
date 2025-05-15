import importlib
import os

# this will load the translations
def get_translation(key):
    """
    Get a translated message for the given key.
    
    Args:
        key (str): The message key to translate
        
    Returns:
        str: The translated message
    """
    # read the lang file to see what language was set by user
    LANG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cli", "lang.txt")
    
    if os.path.exists(LANG_FILE):
        # open the lang file
        with open(LANG_FILE, "r") as file:
            # read the lang file
            lang = file.read().strip()
            
            if not lang:
                lang = 'en'  # if file is empty, default to english
    else:
        lang = 'en'  # default to English if there is no file

    # this is actually import the translations
    try:
        messages = importlib.import_module(f"cli.translations.{lang}").messages
    except ModuleNotFoundError:
        messages = importlib.import_module("cli.translations.en").messages  # default to English if any errors

    # Return the specific message for the key, or the key itself if not found
    return messages.get(key, key)
