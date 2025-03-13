import importlib
import os

# this will load the translations
def get_translation(LANG_FILE):
    
    # read the lang file to see what langague was set by user
    if os.path.exists(LANG_FILE):

        # open the lang file
        with open(LANG_FILE, "r") as file:
                
                # read the lang file
                lang = file.read().strip()

              
                if not lang:
                    lang = 'en' # if file is empty, default to english
        
    else:
        lang = 'en'  # default to English if there is not file but there will always be a file this is just in case ALSO THIS IS SO @icrcode DOESNT COMPLAIN ABOUT MY CODE NOT BEING CLEAN AND WHATEVER

    # this is actually import the translations
    try:
        return importlib.import_module(f"cli.translations.{lang}").messages
    except ModuleNotFoundError:
        return importlib.import_module("cli.translations.en").messages  # default to English if any errors
