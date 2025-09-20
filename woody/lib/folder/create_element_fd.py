from .create_folders_subfolders import create_folders_subfolders
from ...tool import WoodyInstance

def create_element_fd(groupTypeCombo, groupName, elementName):
    
    woody = WoodyInstance()
    
    group_type = "assets" if groupTypeCombo == "Assets Group" else "shots"
    
    base_path = woody.projectDirectory / woody.projectName / group_type / groupName
    
    folders = {
       elementName: [],
    }
    
    create_folders_subfolders(folders, base_path)
    
    