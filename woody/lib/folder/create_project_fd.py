from pathlib import Path
from .folder_instance import FolderInstance

def create_project_fd(project_name, base_path):
    
    # woody = WoodyInstance()
    # project_name = woody.projectName
    # base_path = woody.projectDirectory
    
    folders = {
        "assets": [],
        "shots": [],
    }
    
    # Handle path joining manually for scheme-based paths (smb://, etc.)
    if base_path.startswith(('smb://', 'http://', 'https://', 'ftp://')):
        # For URL-like paths, use string concatenation with proper separator
        project_root = base_path.rstrip('/') + '/' + project_name
    else:
        # For regular paths, use Path object
        project_root = Path(base_path) / project_name
    
    print(f"******** Creating project folder at: {project_root}")
    FolderInstance(project_root, folders).create_folders_subfolders()
