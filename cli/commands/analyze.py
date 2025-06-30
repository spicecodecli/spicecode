from InquirerPy import inquirer
import requests
import json
import hashlib
import os
import sys

from utils.get_translation import get_translation
from spice.analyze import analyze_file

# Add this at the top - server configuration
SERVER_URL = "http://localhost:3000/api/submit"

def get_file_hash(file_path):
    """Generate a hash for the file based on content and modification time"""
    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # Include file modification time to detect changes
        mod_time = os.path.getmtime(file_path)
        hash_input = file_content + str(mod_time).encode()
        
        return hashlib.md5(hash_input).hexdigest()
    except Exception as e:
        print(f"Error generating hash: {e}")
        return None

def send_to_server(data):
    """Send analysis data to the server"""
    try:
        response = requests.post(SERVER_URL, json=data, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('isDuplicate'):
                print("✓ Data updated on server (file was modified)")
            else:
                print("✓ New analysis sent to server")
            return True
        else:
            # print(f"⚠ Server responded with status {response.status_code}", file=sys.stderr)
            return False
            
    except requests.exceptions.ConnectionError:
        # print("⚠ Could not connect to server - make sure it's running on localhost:3000", file=sys.stderr)
        return False
    except requests.exceptions.Timeout:
        # print("⚠ Server request timed out", file=sys.stderr)
        return False
    except Exception as e:
        # Linha para debugar erros, descomente se precisar:
        # print(f"⚠ Error sending to server: {e}", file=sys.stderr)
        return False



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
        "indentation_level",
        "external_dependencies_count",
        "method_type_count",
        "comment_ratio",
    ]

    # dictionary for the stats
    stats_labels = {
        "line_count": messages.get("line_count_option", "Line Count"),
        "function_count": messages.get("function_count_option", "Function Count"),
        "comment_line_count": messages.get("comment_line_count_option", "Comment Line Count"),
        "inline_comment_count": messages.get("inline_comment_count_option", "Inline Comment Count"),
        "indentation_level": messages.get("indentation_level_option", "Indentation Analysis"),
        "external_dependencies_count": messages.get("external_dependencies_count_option", "External Dependencies Count"),
        "method_type_count": messages.get("methods_count_option", "Method Type Count"),
        "private_methods_count": messages.get("private_methods_count_option", "Private Methods Count"),
        "public_methods_count": messages.get("public_methods_count_option", "Public Methods Count"),
        "comment_ratio": messages.get("comment_ratio_option", "Comment to Code Ratio"),
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
        
        # Prepare data for server
        server_data = {
            "file_name": results.get("file_name"),
            "file_path": results.get("file_path"),
            "file_size": results.get("file_size"),
            "file_extension": results.get("file_extension"),
            **{k: v for k, v in results.items() if k not in ["file_name", "file_path", "file_size", "file_extension"]}
        }
        
        # Send to server (always attempt this, regardless of output mode)
        send_to_server(server_data)
        
        # output in JSON format if flag
        if json_output:
            import json
            print(json.dumps(results, indent=2))
        else:
            # only print the selected stats in normal mode
            for stat in selected_stat_keys:
                #print(stat) #debug
                if stat == "method_type_count" and "method_type_count" in results:
                    mtc = results["method_type_count"]
                    print(f"{messages.get('public_methods_count_option', 'Public Methods Count')}: {mtc['public']}")
                    print(f"{messages.get('private_methods_count_option', 'Private Methods Count')}: {mtc['private']}")
                    continue

                if stat == "indentation_level" and "indentation_type" in results:
                    print(f"{messages.get('indentation_type', 'Indentation Type')}: {results.get('indentation_type', 'N/A')}")
                    print(f"{messages.get('indentation_size', 'Indentation Size')}: {results.get('indentation_size', 'N/A')}")
                    continue
                    
                elif stat in results:
                    print(f"{stats_labels[stat]}: {results[stat]}")
    except Exception as e:
        if json_output:
            import json
            # Replace newlines with spaces or escape them properly
            error_msg = str(e).replace('\n', ' ')
            print(json.dumps({"error": error_msg}))
        else:
            print(f"{messages.get('error', 'Error')}: {e}")