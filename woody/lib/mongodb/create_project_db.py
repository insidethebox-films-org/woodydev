from ...tool import WoodyInstance
from ...database.db_instance import DB_instance
from ...database.templates.settings import settings_template

import copy
from datetime import datetime, timezone

def create_project_db():
    
    woody = WoodyInstance()
    name = woody.projectName
    directory = str(woody.projectDirectory)

    db = DB_instance(name)
    
    collection_name = "settings"
    db.add_collection(collection_name)
    print(f"Collection '{collection_name}' is set up in database '{db.name}'.") #TODO
    
    settings = copy.deepcopy(settings_template)
    settings["project_name"] = db.name
    settings["location"] = directory
    settings["created_time"] = datetime.now(timezone.utc)
    db.add_document(collection_name, settings)
    
    



