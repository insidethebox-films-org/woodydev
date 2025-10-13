from ...tool import WoodyInstance
from ...database.db_instance import DB_instance
from ...ui.frames.asset_browser import AssetBrowserFrame

def get_element_details(element_selection):

    try:
        woody = WoodyInstance()
        db = DB_instance(woody.projectName)
        db = db.connect
        
        is_asset = element_selection['root'] == "Assets Group"
        collection = "assets" if is_asset else "shots"
        
        # Build query with both name and group/sequence
        query = {
            "name": element_selection['element'],
            "group" if is_asset else "sequence": element_selection['group']
        }
        element_details = db[collection].find_one(query)
        
        return element_details
        
    except Exception as e:
        print(f"Error getting element details: {e}")
        return None
    
    
    
    
    