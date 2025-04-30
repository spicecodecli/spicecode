from InquirerPy import inquirer

from utils.get_translation import get_translation
from spice.analyze import analyze_file


def analyze_command(file, all, json_output, LANG_FILE):
    """
    Analyze the given file.
    """
    
    # load translations
    messages = get_translation(LANG_FILE)

    # define available stats
    available_stats = [
        "line_count",
        "function_count", 
        "comment_line_count",
        "inline_comment_count",
        "external_dependencies_count",
        "indentation_level"
    ]

    # dictionary for the stats
    stats_labels = {
        "line_count": messages.get("line_count_option", "Line Count"),
        "function_count": messages.get("function_count_option", "Function Count"),
        "comment_line_count": messages.get("comment_line_count_option", "Comment Line Count"),
        "inline_comment_count": messages.get("inline_comment_count_option", "Inline Comment Count"),
        "external_dependencies_count": messages.get("external_dependencies_count_option", "External Dependencies Count"),
        "indentation_level": messages.get("indentation_level_option", "Indentation Analysis")
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
            print(f"{messages.get('analyzing_file', 'Analyzing file')}: {file}")
        
        # get analysis results from analyze_file
        results = analyze_file(file, selected_stats=selected_stat_keys)
        
        # output in JSON format if flag
        if json_output:
            import json
            print(json.dumps(results, indent=2))
        else:
            # only print the selected stats in normal mode
            for stat in selected_stat_keys:
                if stat == "indentation_level" and "indentation_type" in results:
                    print(f"{messages.get('indentation_type', 'Indentation Type')}: {results['indentation_type']}")
                    print(f"{messages.get('indentation_size', 'Indentation Size')}: {results['indentation_size']}")
                elif stat in results:
                    print(messages.get(stat, f"{stat.replace('_', ' ').title()}: {{count}}").format(count=results[stat]))
        
    except Exception as e:
        if json_output:
            import json
            # Replace newlines with spaces or escape them properly
            error_msg = str(e).replace('\n', ' ')
            print(json.dumps({"error": error_msg}))
        else:
            print(f"{messages.get('error', 'Error')}: {e}")
