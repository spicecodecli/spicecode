import os
from rich import print # this add colors to the printed text

from utils.get_translation import get_translation


def version_command(LANG_FILE, CURRENT_DIR):
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
            print(f"[green]{messages.get('version_info', 'SpiceCode Version:')}[/] {version_info}")
        else:
            print(f"[yellow]{messages.get('version_not_found', 'Version information not found in setup.py')}")
            
    except Exception as e:
        print(f"[red]{messages.get('error', 'Error:')}[/] {e}")