from ...objects import Database
from ...templates.scene import scene_template
from ...utils.woody_id import create_woody_id

import copy
import asyncio
import threading
from datetime import datetime

async def create_scene_db_async(root, group, element_name, scene_name, dcc):
    db = Database()
    
    element = await db.connect[root].find_one({"name": element_name})
    
    if not element:
        print(f"Error: Element '{element_name}' not found in {root} collection")
        return False

    if dcc == "blender":
        prefix = ".blend"
    elif dcc == "houdini":
        prefix = ".hip"
    else:
        return print("No vaild dcc selected")
    
    scene_name_with_latest = f"{scene_name}_latest{prefix}"
    scene_path = f"{root}\{group}\{element_name}\{scene_name_with_latest}"
    collection_name = "scenes"

    woody_id = create_woody_id(root, group, element_name, scene_name)
    parent_id = create_woody_id(root, group, element_name)
    
    if await db.connect[collection_name].find_one({"name": scene_name, "id": woody_id}):
        print(f"Document '{scene_name}' already exists in collection '{collection_name}'.")
        return False
    
    try:
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