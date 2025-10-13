from .folder_instance import FolderInstance
from ...tool import WoodyInstance
from ...database.db_instance import DB_instance

def create_element_fd(groupTypeCombo, groupName, elementName):
    
    woody = WoodyInstance()
    db = DB_instance() 
    
    group_type = "assets" if groupTypeCombo == "Assets Group" else "shots"
    
    base_path = db.projectDirectory / woody.projectName / group_type / groupName
    
    folders = {
       elementName: [],
    }
    
    FolderInstance(base_path, folders).create_folders_subfolders()
    
    