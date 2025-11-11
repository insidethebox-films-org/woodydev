from .woody_instance import WoodyInstance
from .memory_store import store

prefix = "woodyID:"

def create_woody_id(root, group, element=None, blend=None):
    
    project = WoodyInstance().projectName
    root = str.lower(root)
    
    if element == None:
        woodyID = f"{prefix}{project}|{root}|{group}"    
    elif blend == None:
        woodyID = f"{prefix}{project}|{root}|{group}|{element}"
    else:
        woodyID = f"{prefix}{project}|{root}|{group}|{element}|blend:{blend}"
    
    print(f"Woody ID = {woodyID}")
    return woodyID

def get_browser_selection_id(group_id=False, element_id=False):
    
    project = WoodyInstance().projectName
    
    data = store.get_namespace("browser_selection")
    root = str.lower(data.get("root", ""))
    group = data.get("group", "")
    element = data.get("element", "")
    
    if group_id and element_id == True or group_id and element_id == False:
        print("Please select one return option")
        return None
    
    if group_id == True:
        if group != None:
            woody_id = f"{prefix}{project}|{root}|{group}"
            return woody_id
        else:
            print("No group selected in asset browser")
    
    if element_id == True:
        if element != None:
            woody_id = f"{prefix}{project}|{root}|{group}|{element}"
            return woody_id
        else:
            print("No element selected in asset browser")