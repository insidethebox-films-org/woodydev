import os
from pathlib import Path

def create_folders_subfolders(folders, base_path):
    # Convert base_path to Path object if it's a string
    # Handle special cases for URL schemes like smb://
    if isinstance(base_path, str):       
        # For URL schemes, use os.makedirs with string paths
        for main_folder, subfolders in folders.items():
            main_path = base_path.rstrip('/') + '/' + main_folder
            try:
                print(f"Creating directory: {main_path}")
                os.makedirs(main_path, exist_ok=True)
            except OSError as e:
                print(f"Could not create directory {main_path}: {e}")
                continue

            if isinstance(subfolders, dict):
                create_folders_subfolders(subfolders, main_path)
            elif isinstance(subfolders, list): 
                for subfolder in subfolders:
                    subfolder_path = main_path.rstrip('/') + '/' + subfolder
                    try:
                        print(f"Creating directory: {subfolder_path}")
                        os.makedirs(subfolder_path, exist_ok=True)
                    except OSError as e:
                        print(f"Could not create directory {subfolder_path}: {e}")
        return
    
    # Handle Path objects (original logic)
    for main_folder, subfolders in folders.items():
        main_path = base_path / main_folder
        main_path.mkdir(parents=True, exist_ok=True)

        if isinstance(subfolders, dict):
            create_folders_subfolders(subfolders, main_path)
        elif isinstance(subfolders, list): 
            for subfolder in subfolders:
                (main_path / subfolder).mkdir(parents=True, exist_ok=True)