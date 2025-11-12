from ...objects import Database
from ...tool.woody_id import create_woody_id
from ...templates.groups import groups_template
from ...templates.sequences import sequences_template

import asyncio
import threading
import copy
from datetime import datetime

async def create_group_sequence_db_async(root, name):
    
    db = Database()

    if root == 'Assets':
        collection_name = "groups"
        template_type = groups_template
        element_type = "assets"
    else:
        collection_name = "sequences"
        template_type = sequences_template
        element_type = "shots"
    
    id = create_woody_id(root, name)

    existing = await db.connect[collection_name].find_one({"id": id})
    if existing:
        print(f"Document '{name}' already exists in collection '{collection_name}'.")
        return
    
    try:
        template = copy.deepcopy(template_type)
        template["id"] = id
        template["name"] = name
        template[element_type] = {}
        template["created_time"] = datetime.now()  
        template["modified_time"] = datetime.now()
        

        await db.add_document(collection_name, template)
        print(f"Document '{name}' is set up in collection '{collection_name}'.")
        
    except Exception as e:
        print(f"Error creating group/sequence document: {str(e)}")
        return False

def create_group_sequence_db(root, name):

    def run():
        asyncio.run(create_group_sequence_db_async(root, name))
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()