from ...database.async_db_instance import AsyncMongoDB
from ...tool.woody_id import create_woody_id
from ...database.templates.groups import groups_template
from ...database.templates.sequences import sequences_template

import asyncio
import threading
import copy
from datetime import datetime

async def create_group_sequence_db_async(root, name):
    
    db = AsyncMongoDB()

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

    template = copy.deepcopy(template_type)
    template["id"] = id
    template["name"] = name
    template[element_type] = {}
    template["created_time"] = datetime.now()  
    template["modified_time"] = datetime.now()
    

    await db.add_document(collection_name, template)
    print(f"Document '{name}' is set up in collection '{collection_name}'.")


def create_group_sequence_db(root, name):

    def run():
        asyncio.run(create_group_sequence_db_async(root, name))
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()