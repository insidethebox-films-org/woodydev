from ...templates.settings import settings_template
from ...templates.render_settings import global_render_settings_template, blender_render_settings_template
from ...objects import Database

import asyncio
import threading
import copy
from datetime import datetime

async def create_project_db_async(name, host_address, directory):
    
    client = Database().client
    
    if name in await client.list_database_names():
        print(f"Database \"{name}\" already exists.")
        return False
    
    db = client[name]
    
    try:
        settings = copy.deepcopy(settings_template)
        settings["project_name"] = name
        settings["host_address"] = host_address
        settings["location"] = directory
        settings["created_time"] = datetime.now()
        
        render_settings = copy.deepcopy(global_render_settings_template)
        blender_render_settings = copy.deepcopy(blender_render_settings_template)
        
        collection = db["settings"]
        await collection.insert_many([settings, render_settings, blender_render_settings])
    
    except Exception as e:
        print(f"Error creating settings document: {str(e)}")
        return False

    print(f"Collection 'settings' is set up in database '{name}'.")
    
    return True


def create_project_db(name, host_address, directory):
    result = [None] 
    
    def run():
        result[0] = asyncio.run(create_project_db_async(name, host_address, directory))
        
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    thread.join()
    
    return result[0]