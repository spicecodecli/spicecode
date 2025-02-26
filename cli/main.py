

import typer
from rich import print


def main():
    print("🌶️   Welcome to [bold red]SpiceCode[/]! 🌶️")
    print("🔥 The [yellow]CLI tool[/] that makes your code [yellow]spicier[/] 🥵")


if __name__ == "__main__":
    typer.run(main)