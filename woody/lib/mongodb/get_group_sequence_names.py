from ...tool import WoodyInstance
from ...database.db_instance import DB_instance

def get_group_sequence_names(groupType):
    
    woody = WoodyInstance()
    db = DB_instance(woody.projectName)
    db = db.connect
    
    if groupType == "Assets Group":
        collection = db["groups"]
    else:
        collection = db["sequences"]
    
    
    return [doc["name"] for doc in collection.find({}, {"name": 1})]