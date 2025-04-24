import os
import sys
import typer

# import commands
from cli.commands.translate import translate_command
from cli.commands.hello import hello_command
from cli.commands.version import version_command
from cli.commands.analyze import analyze_command
from cli.commands.export.export import export_command

# initialize typer
app = typer.Typer()

# add the current directory (cli) to the sys.path
sys.path.append('cli')

# get current directory, this is needed for it to work on other peoples computers via pip
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# select a file to save the current selected language
LANG_FILE = os.path.join(CURRENT_DIR, "lang.txt")

@app.command()
def translate():
    """
    Set the language for CLI messages.
    """
    translate_command(LANG_FILE)

@app.command()
def hello():
    """
    Welcome message.
    """
    hello_command(LANG_FILE)

@app.command()
def version():
    """
    Display the current version of the application.
    """
    version_command(LANG_FILE, CURRENT_DIR)

@app.command()
def analyze(
    file: str, 
    all: bool = typer.Option(False, "--all", help="Analyze all stats without selection menu"),
    json_output: bool = typer.Option(False, "--json", help="Output results in JSON format")
):
    """
    Analyze the given file.
    """
    analyze_command(file, all, json_output, LANG_FILE)

@app.command()
def export(
    file: str,
    format_type: str = typer.Option("json", "--format", "-f", help="Export format (json, csv, markdown, html)"),
    output: str = typer.Option(None, "--output", "-o", help="Output file path")
):
    """
    Analyze a file and export results to a file in the specified format.
    """
    export_command(file, format_type, output, LANG_FILE)

def main():
    app()  # run typer

if __name__ == "__main__":
    main()
