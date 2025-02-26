

import typer
from rich import print

from spice.analyze import analyze_file

app = typer.Typer()

@app.command()
def analyze(file: str):
    """
    Analyze the given file.
    """
    try:
        analyze_file(file)
    except Exception as e:
        print(f"[red]Error:[/] {e}")

@app.command()
def hello():
    """
    welcome message.
    """
    print("🌶️   Welcome to [bold red]SpiceCode[/]! 🌶️")
    print("🔥 The [yellow]CLI tool[/] that makes your code [yellow]spicier[/] 🥵")

if __name__ == "__main__":
    app()
