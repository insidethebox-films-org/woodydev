from .create_folders_subfolders import create_folders_subfolders
from ...tool import WoodyInstance

def create_project_fd():
    
    woody = WoodyInstance()
    project_name = woody.projectName
    base_path = woody.projectDirectory
    
    folders = {
        "assets": [],
        "shots": [],
    }
    
    project_root = base_path / project_name
    create_folders_subfolders(folders, project_root)