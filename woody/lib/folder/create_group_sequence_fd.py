from .folder_instance import FolderInstance
from ...tool import WoodyInstance
from ...database.db_instance import DB_instance

def create_group_sequence_fd(type, folder_name):
    
    woody = WoodyInstance()
    db = DB_instance()
    
    group_type = "assets" if type == "Assets Group" else "shots"
    
    base_path = db.projectDirectory / woody.projectName / group_type
    
    folders = {
       folder_name: [],
    }
    print(base_path)
    FolderInstance(base_path, folders).create_folders_subfolders()
    
    