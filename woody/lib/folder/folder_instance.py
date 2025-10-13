from urllib.parse import urlparse
import platform
import os
import subprocess
from pathlib import Path

class FolderInstance():
    """
    A utility class for creating and managing folder structures on local and network drives.
    
    Handles cross-platform directory creation with support for SMB network shares on macOS.
    Automatically mounts SMB drives when needed and creates nested folder structures.
    """
    
    def __init__(self, path, folders=None):
        """
        Initialize a FolderInstance for directory operations.
        
        Attributes:
            path (str): The original path converted to string format
            normalised (str): Path normalized for the current platform (e.g., UNC format)
            mount (str): Local mount point for network drives, or original path for local drives
            folders (dict): The folder structure to be created
        """
        if isinstance(path, Path):
            self.path = str(path)
        else:
            self.path = path
            
        self.normalised = self.normalise_path(self.path)
        self.mount = self.mount_drive(self.normalised)
        self.folders = folders

    def normalise_path(self, path):
        path = str(path)
        
        if path.startswith("smb://"):
            parsed = urlparse(path)
            result = f"//{parsed.netloc}{parsed.path}"
            return result
        
        if path.startswith('//'):
            return path.replace('\\', '/')
        
        return path

    def mount_drive(self, path):
        
        normalised = self.normalise_path(path)
        current_os = platform.system()

        if normalised.startswith('//') and current_os == 'Darwin':
        
            parts = normalised[2:].split('/', 2)
            if len(parts) < 2:
                print(f"{normalised}: is not a valid smb path")
                return None
                
            server = parts[0]
            share = parts[1]
            
            # Mount point
            mount = f"/Volumes/{share}"
            
            if not os.path.ismount(mount):
                smb_url = f"smb://{server}/{share}"

                result = subprocess.run(
                    ['osascript', '-e', 
                        f'mount volume "{smb_url}"'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode != 0:
                    print(f"Warning: Could not mount {smb_url}: {result.stderr}")
                    return None

            # Return the mount
            if len(parts) >= 3:
                subdirectory = parts[2]
                return os.path.join(mount, subdirectory)
            else:
                return mount
        
        # For non-SMB paths, return the original path
        return path

    def create_folders_subfolders(self):
        # Use the mounted path instead of the normalized path
        base_path = self.mount
        
        if base_path is None:
            print("Error: Could not mount the drive. Cannot create directories.")
            return
        
        print(f"Using base path: {base_path}")
        
        # Use the mounted local path for directory creation
        for main_folder, subfolders in self.folders.items():
            main_path = os.path.join(base_path, main_folder)
            try:
                print(f"Creating directory: {main_path}")
                os.makedirs(main_path, exist_ok=True)
            except OSError as e:
                print(f"Could not create directory {main_path}: {e}")
                continue

            if isinstance(subfolders, dict):
                # For nested dictionaries, recursively create subdirectories
                for subfolder_name, nested_content in subfolders.items():
                    subfolder_path = os.path.join(main_path, subfolder_name)
                    try:
                        print(f"Creating directory: {subfolder_path}")
                        os.makedirs(subfolder_path, exist_ok=True)
                    except OSError as e:
                        print(f"Could not create directory {subfolder_path}: {e}")
                        
            elif isinstance(subfolders, list): 
                for subfolder in subfolders:
                    subfolder_path = os.path.join(main_path, subfolder)
                    try:
                        print(f"Creating directory: {subfolder_path}")
                        os.makedirs(subfolder_path, exist_ok=True)
                    except OSError as e:
                        print(f"Could not create directory {subfolder_path}: {e}")