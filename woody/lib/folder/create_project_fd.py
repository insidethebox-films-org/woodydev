from pathlib import Path
from .create_folders_subfolders import create_folders_subfolders
from ...utils.normalise_directory_path import normalise_directory_path

def create_project_fd(project_name, base_path):
    
    # woody = WoodyInstance()
    # project_name = woody.projectName
    # base_path = woody.projectDirectory
    
    folders = {
        "assets": [],
        "shots": [],
    }
    
    normal_path = str(normalise_directory_path(base_path)) # ==  smb://100.113.50.90/projects/PUD/dev
    print(f"******** Normalized base path: {normal_path}")
    
    # Handle path joining manually for scheme-based paths (smb://, etc.)
    if normal_path.startswith(('smb://', 'http://', 'https://', 'ftp://')):
        # For URL-like paths, use string concatenation with proper separator
        project_root = normal_path.rstrip('/') + '/' + project_name
    else:
        # For regular paths, use Path object
        project_root = Path(normal_path) / project_name
    
    print(f"******** Creating project folder at: {project_root}")
    create_folders_subfolders(folders, project_root)