import typer
import json
import os
from rich.console import Console
from rich.table import Table
from spice.analyzers.new_analyzers.indentation_analyzer import analyze_indentation_levels
from utils.get_translation import get_translation

app = typer.Typer()
console = Console()

@app.command("indentation", help=get_translation("analyze_indentation_help"))
def indentation_stats(
    file_path: str = typer.Argument(..., help=get_translation("file_path_help")),
    output_format: str = typer.Option("console", "--format", "-f", help=get_translation("output_format_help")),
):
    """
    Analyzes and reports the indentation levels for each line in the given file.
    """
    if not os.path.exists(file_path):
        console.print(f"[bold red]{get_translation('error_file_not_found')}: {file_path}[/bold red]")
        raise typer.Exit(code=1)
    if not os.path.isfile(file_path):
        console.print(f"[bold red]{get_translation('error_not_a_file')}: {file_path}[/bold red]")
        raise typer.Exit(code=1)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        console.print(f"[bold red]{get_translation('error_reading_file')} {file_path}: {e}[/bold red]")
        raise typer.Exit(code=1)

    results = analyze_indentation_levels(content)

    if output_format == "json":
        console.print(json.dumps(results, indent=2))
    elif output_format == "console":
        console.print(f"\n[bold cyan]{get_translation('indentation_analysis_for')} [green]{file_path}[/green]:[/bold cyan]")
        
        table = Table(title=get_translation("indentation_details_per_line"))
        table.add_column(get_translation("line_num"), style="dim", width=6)
        table.add_column(get_translation("indent_level_col"), justify="right")
        table.add_column(get_translation("content_col"))

        for line_data in results:
            if not line_data["is_empty_or_whitespace_only"]:
                 table.add_row(
                    str(line_data["original_line_number"]),
                    str(line_data["indent_level"]),
                    line_data["stripped_line_content"] if len(line_data["stripped_line_content"]) < 70 else line_data["stripped_line_content"][:67] + "..."
                )
            else:
                table.add_row(
                    str(line_data["original_line_number"]),
                    "-",
                    f"[dim i]({get_translation('empty_line')})[/dim i]"
                )
        console.print(table)
    else:
        console.print(f"[bold red]{get_translation('error_invalid_format')}: {output_format}. {get_translation('valid_formats_are')} console, json.[/bold red]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()

