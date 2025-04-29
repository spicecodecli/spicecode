import os
import json
import csv
import typer
from rich.console import Console
from rich.table import Table

from utils.get_translation import get_translation

def export_results(results, format_type, output_file, messages):
    """
    Export analysis results to a file in the specified format.
    
    Args:
        results (dict): Analysis results to export
        format_type (str): Format to export (json, csv, html, markdown)
        output_file (str): Path to output file
        messages (dict): Translation messages
    
    Returns:
        bool: True if export was successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        
        if format_type == "json":
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
        
        elif format_type == "csv":
            with open(output_file, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                # Write header
                writer.writerow(["Metric", "Value"])
                # Write data
                for key, value in results.items():
                    if isinstance(value, (int, float, str)):
                        writer.writerow([key, value])
                    elif isinstance(value, list):
                        writer.writerow([key, json.dumps(value)])
        
        elif format_type == "markdown":
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"# {messages.get('analysis_results', 'Analysis Results')}\n\n")
                f.write(f"**{messages.get('file_name', 'File')}: {results.get('file_name', 'Unknown')}**\n\n")
                f.write("| Metric | Value |\n")
                f.write("|--------|-------|\n")
                for key, value in results.items():
                    if isinstance(value, (int, float, str)):
                        f.write(f"| {key.replace('_', ' ').title()} | {value} |\n")
                    elif isinstance(value, list) and key == "indentation_levels":
                        f.write(f"| {key.replace('_', ' ').title()} | {len(value)} levels |\n")
        
        elif format_type == "html":
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("<!DOCTYPE html>\n<html>\n<head>\n")
                f.write("<meta charset=\"utf-8\">\n")
                f.write("<title>SpiceCode Analysis Results</title>\n")
                f.write("<style>\n")
                f.write("body { font-family: Arial, sans-serif; margin: 20px; }\n")
                f.write("table { border-collapse: collapse; width: 100%; }\n")
                f.write("th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }\n")
                f.write("th { background-color: #f2f2f2; }\n")
                f.write("h1 { color: #333; }\n")
                f.write("</style>\n</head>\n<body>\n")
                f.write(f"<h1>{messages.get('analysis_results', 'Analysis Results')}</h1>\n")
                f.write(f"<p><strong>{messages.get('file_name', 'File')}: {results.get('file_name', 'Unknown')}</strong></p>\n")
                f.write("<table>\n<tr><th>Metric</th><th>Value</th></tr>\n")
                for key, value in results.items():
                    if isinstance(value, (int, float, str)):
                        f.write(f"<tr><td>{key.replace('_', ' ').title()}</td><td>{value}</td></tr>\n")
                    elif isinstance(value, list) and key == "indentation_levels":
                        f.write(f"<tr><td>{key.replace('_', ' ').title()}</td><td>{len(value)} levels</td></tr>\n")
                f.write("</table>\n</body>\n</html>")
        
        else:
            return False
        
        return True
    
    except Exception as e:
        print(f"{messages.get('export_error', 'Export error')}: {str(e)}")
        return False

def export_command(file, format_type, output, LANG_FILE):
    """
    Export analysis results to a file.
    """
    # Load translations
    messages = get_translation(LANG_FILE)
    console = Console()
    
    # Validate format type
    valid_formats = ["json", "csv", "markdown", "html"]
    if format_type not in valid_formats:
        console.print(f"[red]{messages.get('invalid_format', 'Invalid format')}[/] {format_type}")
        console.print(f"{messages.get('valid_formats', 'Valid formats')}: {', '.join(valid_formats)}")
        return
    
    try:
        # Analyze file
        from spice.analyze import analyze_file
        results = analyze_file(file)
        
        # Set default output file if not provided
        if not output:
            base_name = os.path.splitext(os.path.basename(file))[0]
            output = f"{base_name}_analysis.{format_type}"
        
        # Export results
        success = export_results(results, format_type, output, messages)
        
        if success:
            console.print(f"[green]{messages.get('export_success', 'Export successful')}[/]: {output}")
        else:
            console.print(f"[red]{messages.get('export_failed', 'Export failed')}[/]")
    
    except Exception as e:
        console.print(f"[red]{messages.get('error', 'Error')}[/]: {str(e)}")
