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
    
    cursor = collection.find({}, {"name": 1}).sort("name", 1)
    return [doc["name"] for doc in cursor]

def get_elements_names(group_name):
    woody = WoodyInstance()
    db = DB_instance(woody.projectName)
    db = db.connect
    
    if db["groups"].find_one({"name": group_name}):
        collection = db["assets"]
        query = {"group": group_name}
    else:
        collection = db["shots"]
        query = {"sequence": group_name}
    
    cursor = collection.find(query).sort("name", 1)
    return [doc["name"] for doc in cursor]