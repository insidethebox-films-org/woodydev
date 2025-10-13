import platform
from pathlib import Path

def normalise_directory_path(path_str):
    """
    Convert network path to platform-specific format and return as string.
    
    Args:
        path_str (str): The network path to convert
        
    Returns:
        str: Platform-specific network path as string
        - macOS: smb://server/path
        - Windows/Linux: //server/path
    """
    if not path_str:
        return None
    
    print(f"Normalizing path: {path_str}")

    # Convert path based on platform
    if platform.system() == "Darwin":  # macOS
        # Convert to smb://path format for macOS
        if path_str.startswith("smb://"):
            normalized_path = path_str
            print(f"Path is already in smb:// format: {normalized_path}")
        else:
            # Convert //server/path to smb://server/path for macOS
            if path_str.startswith("//"):
                normalized_path = "smb:" + path_str
                print(f"Converted // to smb://: {normalized_path}")
            else:
                normalized_path = "smb://" + path_str
                print(f"Added smb:// prefix: {normalized_path}")
    else:
        # For Windows/Linux, use UNC path format //server/path
        if path_str.startswith("smb://"):
            normalized_path = path_str.replace("smb://", "//")
        else:
            normalized_path = path_str
    
    return normalized_path