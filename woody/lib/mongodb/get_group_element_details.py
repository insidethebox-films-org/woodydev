from ...tool import WoodyInstance
from ...database.db_instance import DB_instance

def get_group_element_details():
    
    woody = WoodyInstance()
    db = DB_instance(woody.projectName)
    db = db.connect
    
    group_selection = woody.browser_selection().get("group_type")
    group = woody.browser_selection().get("group")
    element = woody.browser_selection().get("element")
    
    if element:
        if group_selection == "Assets Group":
            collection_name = "assets"
        else:
            collection_name = "shots"
    else:
        if group_selection == "Assets Group":
            collection_name = "groups"
        else:
            collection_name = "sequences"
            
    collection = db[collection_name]
    
    if collection_name in ["groups", "sequences"]:
        doc = collection.find_one({"name": group})
    else:
        doc = collection.find_one({"name": element})
        
    return doc
    
        

    
    
    
    