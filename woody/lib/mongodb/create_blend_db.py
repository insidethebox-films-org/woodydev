from ...plugins.blender.blender_instance import BlenderInstance
from ...tool.woody_instance import WoodyInstance
from ...database.db_instance import DB_instance
from ...database.templates.blend import blend_template

import copy
from datetime import datetime, timezone

def create_blend_db(group_type, group_name, element_name, blend_name):
    woody = WoodyInstance()
    db = DB_instance(woody.projectName)
    blend = BlenderInstance()
    
    # Find the element document to get its ID
    element = db.connect[group_type].find_one({"name": element_name})
    
    if not element:
        print(f"Error: Element '{element_name}' not found in {group_type} collection")
        return False
    
    # Determine which collection the element is in and get its ID
    if group_type == "assets":
        element_id = element["asset_id"]
        print(f"Found element '{element_name}' in assets collection")
    elif group_type == "shots":
        element_id = element["shot_id"]
        print(f"Found element '{element_name}' in shots collection")
    else:
        print(f"Error: Invalid group_type '{group_type}'")
        return False

    blend_path = blend.get_blend_path(group_type, group_name, element_name, blend_name)
    collection_name = "blends"
    
    # Check if document with the same name already exists
    if db.connect[collection_name].find_one({"name": blend_name}):
        print(f"Document '{blend_name}' already exists in collection '{collection_name}'.")
        return False

    try:
        # Create collection if it doesn't exist
        db.add_collection(collection_name)
        
        # Create document from template
        template = copy.deepcopy(blend_template)
        template["name"] = blend_name
        template["element_id"] = element_id
        template["blend_files"] = {blend_path: 1}
        template["created_time"] = datetime.now(timezone.utc)  
        template["modified_time"] = datetime.now(timezone.utc)
        
        db.add_document(collection_name, template)
        print(f"Document '{blend_name}' is set up in collection '{collection_name}'.")
        return True
        
    except Exception as e:
        print(f"Error creating blend document: {str(e)}")
        return False