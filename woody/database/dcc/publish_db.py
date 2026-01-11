from ...objects.database import Database
from ...templates.publish import publish_template
from ...utils.woody_id import explode_woody_id

import asyncio
import threading
import copy
from datetime import datetime
from pathlib import Path

async def publish_db_async(name, publish_type, dcc, woody_id, file_path):
    db = Database()
    collection_name = "publishes"
    id = f"{woody_id}|publish:{name}"
    
    existing_doc = await db.get_doc(collection_name, {"id": id})
    
    if existing_doc:
        print("Publish already exists")
        return False
    else:
        try:
            id_parts = explode_woody_id(woody_id)
            filename = Path(file_path).name
            relative_path = "\\".join(id_parts[1:]) + "\\" + "publish\\" + filename
            
            template = copy.deepcopy(publish_template)
            template["id"] = id
            template["parent_id"] = woody_id
            template["name"] = name
            template["type"] = publish_type
            template["dcc"] = dcc
            template["versions"] = {"latest": relative_path}
            template["created_time"] = datetime.now() 
            
            await db.add_document(collection_name, template)
            print(f"Publish document created successfully for '{name}'")
            return True
        
        except Exception as e:
            print(f"Error creating publish doc: {e}")
            return False
    
def publish_db(name, publish_type, dcc, woody_id, file_path):
    def run():
        asyncio.run(publish_db_async(name, publish_type, dcc, woody_id, file_path))

    t = threading.Thread(target=run, daemon=True)
    t.start()