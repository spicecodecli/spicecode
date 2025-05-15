import typer
import json
import os
from rich.console import Console
from rich.table import Table
from spice.analyzers.new_analyzers.dependency_analyzer import analyze_dependencies
from utils.get_translation import get_translation

app = typer.Typer()
console = Console()

@app.command("dependencies", help=get_translation("analyze_dependencies_help"))
def dependency_stats(
    file_path: str = typer.Argument(..., help=get_translation("file_path_help")),
    output_format: str = typer.Option("console", "--format", "-f", help=get_translation("output_format_help")),
):
    """
    Analyzes and reports the external dependencies for the given file.
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

    results = analyze_dependencies(content, file_name_for_error_reporting=file_path)

    if output_format == "json":
        # The analyzer returns a list of imports or an error dict
        if isinstance(results, dict) and "error" in results:
            console.print(json.dumps({"error": results["error"]}, indent=2))
        else:
            console.print(json.dumps(sorted(results) if isinstance(results, list) else [], indent=2))
    elif output_format == "console":
        console.print(f"\n[bold cyan]{get_translation('dependency_analysis_for')} [green]{file_path}[/green]:[/bold cyan]")
        if isinstance(results, dict) and "error" in results:
            console.print(f"[bold red]{get_translation('error_analyzing_dependencies')}: {results['error']}[/bold red]")
        elif isinstance(results, list):
            if results:
                table = Table(title=get_translation('dependencies_found'))
                table.add_column(get_translation('dependency_name'), style="dim")
                for dep in sorted(results):
                    table.add_row(dep)
                console.print(table)
            else:
                console.print(get_translation("no_dependencies_found"))
        else:
            console.print(f"[bold red]{get_translation('error_unexpected_result')}[/bold red]")
    else:
        console.print(f"[bold red]{get_translation('error_invalid_format')}: {output_format}. {get_translation('valid_formats_are')} console, json.[/bold red]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()

