from ...tool import WoodyInstance
from ...database.db_instance import DB_instance

def get_publish_doc():
    
    woody = WoodyInstance()
    browser_selection = woody.browser_selection()
    
    if not browser_selection:
        return []
    
    element = browser_selection.get("element")
    
    try:
        db = DB_instance(woody.projectName).connect
    except Exception as e:
        print(f"Database connection error: {e}")
        return []
    
    try:
        publish_doc = db["publishes"].find_one({"source_asset": element})
        
        if not publish_doc:
            return []
        
        source_asset = publish_doc.get("source_asset")
        docs = db["publishes"].find({"source_asset": source_asset})
          
        return list(docs)
    except Exception as e:
        print(f"Database query error: {e}")
        return []
    
def get_publish_versions(docs, publish_name, publish_version=None):
    
    doc = next((d for d in docs if d["custom_name"] == publish_name), None)
    publish_versions = doc.get("published_versions")
    versions = list(publish_versions)
    
    versions_data = doc.get("published_versions", {})
    version_data = versions_data.get(publish_version)
    
    return versions, version_data