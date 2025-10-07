from ...tool import WoodyInstance
from ...database.db_instance import DB_instance

woody = WoodyInstance()
db = DB_instance(woody.projectName)
db = db.connect

def get_group_sequence_names(groupType):
    
    if groupType == "Assets Group":
        collection = db["groups"]
    else:
        collection = db["sequences"]
    
    return [doc["name"] for doc in collection.find({}, {"name": 1})]

def get_elements_names(group_name):

    if db["groups"].find_one({"name": group_name}):
        collection = db["assets"]
        query = {"group": group_name}
    else:
        collection = db["shots"]
        query = {"sequence": group_name}
        
    return [doc["name"] for doc in collection.find(query)]

    