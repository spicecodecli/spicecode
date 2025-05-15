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

    results = analyze_comment_code_ratio(content)

    if output_format == "json":
        # Clean the results to ensure valid JSON
        cleaned_results = {
            "summary_stats": {
                "total_lines_in_file": results.get("summary_stats", {}).get("total_lines_in_file", 0),
                "code_lines": results.get("summary_stats", {}).get("code_lines", 0),
                "comment_only_lines": results.get("summary_stats", {}).get("comment_only_lines", 0),
                "empty_or_whitespace_lines": results.get("summary_stats", {}).get("empty_or_whitespace_lines", 0),
                "comment_to_code_plus_comment_ratio": results.get("summary_stats", {}).get("comment_to_code_plus_comment_ratio", 0)
            },
            "line_by_line_analysis": [
                {
                    "original_line_number": line.get("original_line_number", 0),
                    "type": line.get("type", ""),
                    "line_content": line.get("line_content", "").replace("\n", " ").replace("\r", "").replace("\t", " ")
                }
                for line in results.get("line_by_line_analysis", [])
            ]
        }
        print(json.dumps(cleaned_results, indent=2))
    elif output_format == "console":
        console.print(f"\n[bold cyan]{get_translation('comment_code_ratio_analysis_for')} [green]{file_path}[/green]:[/bold cyan]")
        summary = results.get("summary_stats", {})
        
        table_summary = Table(title="Summary Statistics")
        table_summary.add_column("Metric", style="dim")
        table_summary.add_column("Value", justify="right")
        table_summary.add_row("Total Lines", str(summary.get("total_lines_in_file", 0)))
        table_summary.add_row("Code Lines", str(summary.get("code_lines", 0)))
        table_summary.add_row("Comment Lines", str(summary.get("comment_only_lines", 0)))
        table_summary.add_row("Empty Lines", str(summary.get("empty_or_whitespace_lines", 0)))
        table_summary.add_row("Comment/Code Ratio", f"{summary.get('comment_to_code_plus_comment_ratio', 0):.2%}")
        console.print(table_summary)

        line_details = results.get("line_by_line_analysis", [])
        if line_details:
            table_details = Table(title="Line-by-Line Classification")
            table_details.add_column("Line No.", style="dim", width=6)
            table_details.add_column("Line Type", style="dim")
            table_details.add_column("Content")
            for line_data in line_details:
                if isinstance(line_data, dict):
                    content = line_data.get("line_content", "")
                    if len(content) > 70:
                        content = content[:67] + "..."
                    table_details.add_row(
                        str(line_data.get("original_line_number", "")),
                        get_translation(line_data.get("type", "")),
                        content
                    )
            console.print(table_details)
    else:
        console.print(f"[bold red]{get_translation('error_invalid_format')}: {output_format}. {get_translation('valid_formats_are')} console, json.[/bold red]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()

