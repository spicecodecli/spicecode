import os
from rich import print # this add colors to the printed text

from utils.get_translation import get_translation


def version_command(LANG_FILE, CURRENT_DIR):
    """
    Display the current version of the application.
    """
    
    try:
        # Get the path to setup.py in the parent directory
        setup_path = os.path.join(os.path.dirname(CURRENT_DIR), "setup.py")
        
        # Check if setup.py exists
        if not os.path.exists(setup_path):
            print(f"[red]{get_translation('setup_not_found')}")
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
            print(f"[green]{get_translation('version_info')}[/] {version_info}")
        else:
            print(f"[yellow]{get_translation('version_not_found')}")
            
    except Exception as e:
        print(f"[red]{get_translation('error')}[/] {e}")