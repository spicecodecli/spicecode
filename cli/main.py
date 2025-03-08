import typer
import importlib
import sys
from rich import print
from spice.analyze import analyze_file

app = typer.Typer()

# Add the current directory (cli) to the sys.path
sys.path.append('cli')

# this will load the translations, default is english
def get_translation(lang="en"):
    try:
        # Dynamically import translation using a relative import
        return importlib.import_module(f"cli.translations.{lang}").messages
    except ModuleNotFoundError:
        # Fallback to English if the specified language isn't found
        return importlib.import_module("cli.translations.en").messages  # Default to English
    

# you can set language here
LANG = "en"

# SPICE SET_LANG COMMAND
@app.command()
def set_lang(language: str):
    """
    Set the language for CLI messages.
    """
    global LANG
    LANG = language
    print(f"[green]Language set to:[/] {language}")


# SPICE ANALYZE COMMAND
@app.command()
def analyze(file: str):
    """
    Analyze the given file.
    """
    messages = get_translation(LANG)
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
    messages = get_translation(LANG)
    print(messages["welcome"])
    print(messages["description"])

def main():
    app()  # This will run your Typer app

if __name__ == "__main__":
    main()
