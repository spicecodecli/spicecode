import typer
import json
import os
from rich.console import Console
from rich.table import Table
from spice.analyzers.new_analyzers.comment_code_ratio_analyzer import analyze_comment_code_ratio
from utils.get_translation import get_translation

app = typer.Typer()
console = Console()

@app.command("ratio", help=get_translation("analyze_comment_code_ratio_help"))
def comment_code_ratio_stats(
    file_path: str = typer.Argument(..., help=get_translation("file_path_help")),
    output_format: str = typer.Option("console", "--format", "-f", help=get_translation("output_format_help")),
):
    """
    Analyzes and reports the comment to code ratio for the given file.
    """
    if not os.path.exists(file_path):
        console.print(f"[bold red]{get_translation("error_file_not_found")}: {file_path}[/bold red]")
        raise typer.Exit(code=1)
    if not os.path.isfile(file_path):
        console.print(f"[bold red]{get_translation("error_not_a_file")}: {file_path}[/bold red]")
        raise typer.Exit(code=1)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        console.print(f"[bold red]{get_translation("error_reading_file")} {file_path}: {e}[/bold red]")
        raise typer.Exit(code=1)

    results = analyze_comment_code_ratio(content)

    if output_format == "json":
        console.print(json.dumps(results, indent=2))
    elif output_format == "console":
        console.print(f"\n[bold cyan]{get_translation("comment_code_ratio_analysis_for")} [green]{file_path}[/green]:[/bold cyan]")
        summary = results.get("summary_stats", {})
        
        table_summary = Table(title=get_translation("summary_statistics"))
        table_summary.add_column(get_translation("metric"), style="dim")
        table_summary.add_column(get_translation("value"), justify="right")
        table_summary.add_row(get_translation("total_lines"), str(summary.get("total_lines_in_file", 0)))
        table_summary.add_row(get_translation("code_lines"), str(summary.get("code_lines", 0)))
        table_summary.add_row(get_translation("comment_lines"), str(summary.get("comment_only_lines", 0)))
        table_summary.add_row(get_translation("empty_lines"), str(summary.get("empty_or_whitespace_lines", 0)))
        table_summary.add_row(get_translation("comment_code_ratio"), f"{summary.get("comment_to_code_plus_comment_ratio", 0):.2%}")
        console.print(table_summary)

        line_details = results.get("line_by_line_analysis", [])
        if line_details:
            table_details = Table(title=get_translation("line_by_line_classification"))
            table_details.add_column(get_translation("line_num"), style="dim", width=6)
            table_details.add_column(get_translation("line_type"), style="dim")
            table_details.add_column(get_translation("content_col"))
            for line_data in line_details:
                table_details.add_row(
                    str(line_data["original_line_number"]),
                    get_translation(line_data["type"]),
                    line_data["line_content"] if len(line_data["line_content"]) < 70 else line_data["line_content"][:67] + "..."
                )
            console.print(table_details)
    else:
        console.print(f"[bold red]{get_translation("error_invalid_format")}: {output_format}. {get_translation("valid_formats_are")} console, json.[/bold red]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()

