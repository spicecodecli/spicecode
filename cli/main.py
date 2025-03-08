import os
import sys
import importlib
import typer
from rich import print
from spice.analyze import analyze_file


# initialize typer
app = typer.Typer()

# add the current directory (cli) to the sys.path
sys.path.append('cli')

# select a file to save the current selected langague (if saved to memory it wont persist between commands)
LANG_FILE = "cli/lang.txt"

# this will load the translations
def get_translation():
    
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

    


# SPICE SET_LANG COMMAND
@app.command()
def set_lang(language: str):
    """
    Set the language for CLI messages.
    """

    # will write the new language to the langague file (to save it to HD instead of memory) (so its persistant between commands)
    with open(LANG_FILE, "w") as file:
        file.write(language)

    print(f"[green]Language set to:[/] {language}")



# SPICE ANALYZE COMMAND
@app.command()
def analyze(file: str):
    """
    Analyze the given file.
    """
    
    # load translations
    messages = get_translation()

    # try to analyze if error then print the error
    try:
        analyze_file(file)
    except Exception as e:
        print(f"[red]{messages['error']}[/] {e}")


# SPICE HELLO COMMAND
@app.command()
def hello():
    """
    Welcome message.
    """

    # load translations
    messages = get_translation()

    # print the hello message
    print(messages["welcome"])
    print(messages["description"])


def main():
    app()  # run typer

# whatever the fuck this is python makes no sense
if __name__ == "__main__":
    main()
