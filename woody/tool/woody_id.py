from ..objects import Woody
from .memory_store import store

import json
from pathlib import Path

prefix = "woodyID:"

def create_woody_id(root, group, element=None, scene=None):
    
    project = Woody().projectName
    root = str.lower(root)
    
    if element is None:
        woodyID = f"{prefix}{project}|{root}|{group}"    
    elif scene is None:
        woodyID = f"{prefix}{project}|{root}|{group}|{element}"
    else:
        woodyID = f"{prefix}{project}|{root}|{group}|{element}|scene:{scene}"
    
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
            woody_id = f"{prefix}{project}|{root}|{group}"
            return woody_id
        else:
            print("No group selected in asset browser")
    
    if element_id:
        if element != None:
            woody_id = f"{prefix}{project}|{root}|{group}|{element}"
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