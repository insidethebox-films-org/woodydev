from .create_folders_subfolders import create_folders_subfolders
from ...tool import WoodyInstance

def create_group_sequence_fd(type, folder_name):
    
    woody = WoodyInstance()
    
    group_type = "assets" if type == "Assets Group" else "shots"
    
    base_path = woody.projectDirectory / woody.projectName / group_type
    
    folders = {
       folder_name: [],
    }
    
    create_folders_subfolders(folders, base_path)
    
    