import typer
import json
import os
from rich.console import Console
from rich.table import Table
from spice.analyzers.new_analyzers.visibility_analyzer import analyze_visibility
from utils.get_translation import get_translation

app = typer.Typer()
console = Console()

@app.command("visibility", help=get_translation("analyze_visibility_help"))
def visibility_stats(
    file_path: str = typer.Argument(..., help=get_translation("file_path_help")),
    output_format: str = typer.Option("console", "--format", "-f", help=get_translation("output_format_help")),
):
    """
    Analyzes and reports the visibility of functions and methods (public/private) in the given file.
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

    results = analyze_visibility(content, file_name_for_error_reporting=file_path)

    if output_format == "json":
        console.print(json.dumps(results, indent=2))
    elif output_format == "console":
        console.print(f"\n[bold cyan]{get_translation('visibility_analysis_for')} [green]{file_path}[/green]:[/bold cyan]")
        
        if isinstance(results, dict) and "error" in results:
            console.print(f"[bold red]{get_translation('error_analyzing_visibility')}: {results['error']}[/bold red]")
            raise typer.Exit(code=1)

        summary_table = Table(title=get_translation('visibility_summary'))
        summary_table.add_column(get_translation('category'), style="dim")
        summary_table.add_column(get_translation('count'), justify="right")
        summary_table.add_row(get_translation('public_functions'), str(results.get("public_functions", 0)))
        summary_table.add_row(get_translation('private_functions'), str(results.get("private_functions", 0)))
        summary_table.add_row(get_translation('public_methods'), str(results.get("public_methods", 0)))
        summary_table.add_row(get_translation('private_methods'), str(results.get("private_methods", 0)))
        console.print(summary_table)

        details = results.get("details", [])
        if details:
            details_table = Table(title=get_translation('details_by_element'))
            details_table.add_column(get_translation('name'), style="dim")
            details_table.add_column(get_translation('type'))
            details_table.add_column(get_translation('visibility'))
            details_table.add_column(get_translation('line_num'), justify="right")
            for detail in details:
                if isinstance(detail, dict):
                    details_table.add_row(
                        detail.get("name", ""), 
                        get_translation(detail.get("type", "")),
                        get_translation(detail.get("visibility", "")),
                        str(detail.get("lineno", ""))
                    )
            console.print(details_table)
        else:
            console.print(get_translation("no_elements_found_for_visibility"))
            
    else:
        console.print(f"[bold red]{get_translation('error_invalid_format')}: {output_format}. {get_translation('valid_formats_are')} console, json.[/bold red]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()

