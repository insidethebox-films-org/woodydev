from ...tool import WoodyInstance
from ...database.db_instance import DB_instance

def get_blend_doc():
    
    woody = WoodyInstance()
    browser_selection = woody.browser_selection()
    
    if not browser_selection:
        return []
    
    root = browser_selection.get("group_type")
    element = browser_selection.get("element")
    
    try:
        db = DB_instance(woody.projectName).connect
    except Exception as e:
        print(f"Database connection error: {e}")
        return []
    
    if root == "Assets Group":
        collection_name = "assets"
        id_field = "asset_id"
    else:
        collection_name = "shots"
        id_field = "shot_id"
    
    try:
        element_doc = db[collection_name].find_one({"name": element})
        
        if not element_doc:
            return []
        
        element_id = element_doc.get(id_field)
        docs = db["blends"].find({"element_id": element_id})
          
        return list(docs)
    except Exception as e:
        print(f"Database query error: {e}")
        return []
    
def get_blend_versions(docs, blend_name):
    
    doc = next((d for d in docs if d["name"] == blend_name), None)
    blend_files = doc.get("blend_files")
    versions = list(blend_files.values())
    
    return versions