from ..objects import Woody
from ..objects import Directory
from ..objects.database import Database
from ..objects.memory_store import store

import asyncio
import json
from pathlib import Path

PREFIX = "woodyID:"

def create_woody_id(root, group, element=None, scene=None, publish=None):
    
    project = Woody().projectName
    root = str.lower(root)
    
    if element is None:
        woodyID = f"{PREFIX}{project}|{root}|{group}"    
    elif scene is None:
        woodyID = f"{PREFIX}{project}|{root}|{group}|{element}"
    elif publish is None:
        woodyID = f"{PREFIX}{project}|{root}|{group}|{element}|scene:{scene}"
    else:
        woodyID = f"{PREFIX}{project}|{root}|{group}|{element}|publish:{publish}"
    
    print(f"Woody ID = {woodyID}")
    return woodyID

def get_browser_selection_id(group_id=False, element_id=False):
    
    project = Woody().projectName
    
    data = store.get_namespace("browser_selection")
    root = str.lower(data.get("root", ""))
    group = data.get("group", "")
    element = data.get("element", "")
    
    if group_id == element_id:
        print("Please select one return option")
        return None
    
    if group_id:
        if group != None:
            woody_id = f"{PREFIX}{project}|{root}|{group}"
            return woody_id
        else:
            print("No group selected in asset browser")
    
    if element_id:
        if element != None:
            woody_id = f"{PREFIX}{project}|{root}|{group}|{element}"
            return woody_id
        else:
            print("No element selected in asset browser")
    else:
        woody_id = None
        return woody_id

def get_dcc_woody_id(port):
    
    file_path  = Path("prefs") / "dcc.json"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    with file_path.open("r", encoding="utf-8") as f:
        file = json.load(f)
        
    session = file.get(f"dcc_session ({port})")
    woody_id = session.get("woody_id")
    
    return woody_id

def explode_woody_id(id):  
    try:
        raw_id = id.replace(PREFIX, "")
        raw_id = raw_id.split("|")
        
        project = raw_id[0]
        group_type = raw_id[1]
        group = raw_id[2]
        
        if len(raw_id) > 3:
            element = raw_id[3]
        else:
            element = None
        
        if len(raw_id) > 4 and ":" in raw_id[4]:
            product_list = raw_id[4].split(":")
            product_type = product_list[0]
            product = product_list[1]
            
            id_sections = [project, group_type, group, element, product_type, product]
            return id_sections
        
        elif element:
            id_sections = [project, group_type, group, element]
            return id_sections
        
        else:
            id_sections = [project, group_type, group]
            return id_sections
    
    except Exception as e:
        return {"error": f"Error getting woody id: {e}"}
    
async def _woody_product_id_to_filepath_async(id):
    try:
        db = Database()
        doc = await db.get_doc("publishes", {"id": id})
        
        if doc:
            path = doc.get("versions", {}).get("latest")
            if path:
                return path
        
        doc = await db.get_doc("scenes", {"id": id})
        
        if doc:
            path = doc.get("versions", {}).get("latest")
            if path:
                return path
        
        return {"error": f"No document found with id: {id}"}
    
    except Exception as e:
        return {"error": f"Error retrieving path from database: {e}"}

def woody_product_id_to_filepath(id):
    directory = Directory()
    relative_path = asyncio.run(_woody_product_id_to_filepath_async(id))
    
    if isinstance(relative_path, dict) and "error" in relative_path:
        return relative_path
    
    path_parts = relative_path.replace('\\', '/').split('/')
    full_path = directory.construct_path(subfolders=path_parts)
    
    return str(full_path)
    