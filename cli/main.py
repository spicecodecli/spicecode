import os
import sys
import typer
from rich import print
from InquirerPy import inquirer

# this is the analyzer
from spice.analyze import analyze_file

# here we import utilities
from cli.utils.get_translation import get_translation

# here we import the commands
from cli.commands.translate import translate_command
from cli.commands.hello import hello_command


# initialize typer
app = typer.Typer()

# add the current directory (cli) to the sys.path
sys.path.append('cli')

# get current directory, this is needed for it to work on other peoples computers via pip
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# select a file to save the current selected langague (if saved to memory it wont persist between commands)
LANG_FILE = os.path.join(CURRENT_DIR, "lang.txt")



# SPICE SET_LANG COMMAND
@app.command()
def translate():
    """
    Set the language for CLI messages.
    """

    translate_command(LANG_FILE)



# SPICE HELLO COMMAND
@app.command()
def hello():
    """
    Welcome message.
    """

    hello_command(LANG_FILE)


# SPICE VERSION COMMAND
@app.command()
def version():
    """
    Display the current version of the application.
    """
    
    # load translations
    messages = get_translation(LANG_FILE)
    
    try:
        # Get the path to setup.py in the parent directory
        setup_path = os.path.join(os.path.dirname(CURRENT_DIR), "setup.py")
        
        # Check if setup.py exists
        if not os.path.exists(setup_path):
            print(f"[red]{messages.get('setup_not_found', 'Error: setup.py not found.')}")
            return
            
        # Read setup.py to extract version
        version_info = None
        with open(setup_path, "r") as file:
            for line in file:
                if line.strip().startswith("version="):
                    # Extract version using string manipulation
                    version_line = line.strip()
                    version_info = version_line.split("=")[1].strip().strip('"').strip("'").strip(",")
                    break
        
        # Display version information
        if version_info:
            print(f"[green]{messages.get('version_info', 'Version:')}[/] {version_info}")
        else:
            print(f"[yellow]{messages.get('version_not_found', 'Version information not found in setup.py')}")
            
    except Exception as e:
        print(f"[red]{messages.get('error', 'Error:')}[/] {e}")


# SPICE ANALYZE COMMAND
@app.command()
def analyze(
    file: str, 
    all: bool = typer.Option(False, "--all", help="Analyze all stats without selection menu"),
    json_output: bool = typer.Option(False, "--json", help="Output results in JSON format")
):
    """
    Analyze the given file.
    """
    
    # load translations
    messages = get_translation(LANG_FILE)

    # define available stats UPDATE THIS WHEN NEEDED PLEASE !!!!!!!!
    available_stats = [
        "line_count",
        "function_count", 
        "comment_line_count"
    ]

    # dictionary for the stats UPDATE THIS WHEN NEEDED PLEASE !!!!!!!!
    stats_labels = {
        "line_count": messages.get("line_count_option", "Line Count"),
        "function_count": messages.get("function_count_option", "Function Count"),
        "comment_line_count": messages.get("comment_line_count_option", "Comment Line Count")
    }
    
    # If --all flag is used, skip the selection menu and use all stats
    if all:
        selected_stat_keys = available_stats
    else:
        # Don't show interactive menu in JSON mode (assumes all stats)
        if json_output:
            selected_stat_keys = available_stats
        else:
            # print checkbox menu to select which stats to show
            selected_stats = inquirer.checkbox(
                message=messages.get("select_stats", "Select stats to display:"),
                choices=[stats_labels[stat] for stat in available_stats],
                pointer="> ",
                default=[stats_labels[stat] for stat in available_stats],  # All selected by default
                instruction=messages.get("checkbox_hint", "(Use space to select, enter to confirm)")
            ).execute()

            # if no stats were selected
            if not selected_stats:
                if json_output:
                    import json
                    print(json.dumps({"error": messages.get("no_stats_selected", "No stats selected. Analysis cancelled.")}))
                else:
                    print(messages.get("no_stats_selected", "No stats selected. Analysis cancelled."))
                return

            # create a mapping from displayed labels back to stat keys
            reverse_mapping = {v: k for k, v in stats_labels.items()}
            
            # convert selected labels back to stat keys
            selected_stat_keys = [reverse_mapping[label] for label in selected_stats]

    # try to analyze and if error then print the error
    try:
        # show analyzing message if not in JSON mode
        if not json_output:
            print(f"{messages['analyzing_file']}: {file}")
        
        # get analysis results from analyze_file
        results = analyze_file(file, selected_stats=selected_stat_keys)
        
        # output in JSON format if flag
        if json_output:
            import json
            print(json.dumps(results, indent=2))
        else:
            # only print the selected stats in normal mode
            for stat in selected_stat_keys:
                if stat in results:
                    print(messages[stat].format(count=results[stat]))
        
    except Exception as e:
        if json_output:
            import json
            # Replace newlines with spaces or escape them properly
            error_msg = str(e).replace('\n', ' ')
            print(json.dumps({"error": error_msg}))
        else:
            print(f"[red]{messages['error']}[/] {e}")


def main():
    app()  # run typer

# whatever the fuck this is python makes no sense
if __name__ == "__main__":
    main()