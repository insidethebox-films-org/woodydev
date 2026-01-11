from ..objects import Directory
from ..utils.woody_id import explode_woody_id

def create_publish_fd(woody_id):
    
    paths = explode_woody_id(woody_id)
      
    group_type = paths[1]
    group = paths[2]
    element = paths[3]

    dirInstance = Directory()
    base_path = dirInstance.root_path / group_type / group / element
    
    folders = {
       "publish": [],
    }
    dirInstance.create_folders_subfolders(base_path, folders)
    
    return str(base_path)
    