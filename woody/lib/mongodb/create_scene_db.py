from ...objects import Database
from ...templates.scene import scene_template
from ...tool.woody_id import create_woody_id

import copy
import asyncio
import threading
from datetime import datetime

async def create_scene_db_async(root, group, element_name, scene_name, dcc):
    """
    Creates a new blend document in the MongoDB 'scenes' collection for a specified element.
    Args:
        root (str): The type of group the element belongs to ('assets' or 'shots').
        group (str): The name of the group (e.g., asset or shot group).
        element_name (str): The name of the element (e.g., asset or shot name).
        blend_name (str): The name to assign to the new blend document.
    Returns:
        bool: True if the blend document was created successfully, False otherwise.
    """
    
    db = Database()
    
    # Find the element document to get its ID
    element = await db.connect[root].find_one({"name": element_name})
    
    if not element:
        print(f"Error: Element '{element_name}' not found in {root} collection")
        return False

    scene_name_with_latest = f"{scene_name}_latest.blend"
    scene_path = f"{root}\{group}\{element_name}\{scene_name_with_latest}"
    collection_name = "scenes"

    woody_id = create_woody_id(root, group, element_name, scene_name)
    parent_id = create_woody_id(root, group, element_name)
    
    # Check if document with the same name and element id already exists
    if await db.connect[collection_name].find_one({"name": scene_name, "id": woody_id}):
        print(f"Document '{scene_name}' already exists in collection '{collection_name}'.")
        return False
    
    try:
        # Create document from template
        template = copy.deepcopy(scene_template)
        template["id"] = woody_id
        template["parent_id"] = parent_id
        template["dcc"] = dcc
        template["name"] = scene_name
        template["files"] = {scene_path: "latest"}
        template["created_time"] = datetime.now()  
        template["modified_time"] = datetime.now()
        
        await db.add_document(collection_name, template)
        print(f"Document '{scene_name}' is set up in collection '{collection_name}'.")
    
    except Exception as e:
        print(f"Error creating blend document: {str(e)}")
        return False
    
    return True
    
def create_scene_db(root, group, element_name, scene_name, dcc):
    
    result = {"success": False}

    def run():
        try:
            success = asyncio.run(create_scene_db_async(root, group, element_name, scene_name, dcc))
            result["success"] = success
        except Exception as e:
            print(f"Error creating blend document: {str(e)}")
            result["success"] = False
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    thread.join()
    
    return result["success"]