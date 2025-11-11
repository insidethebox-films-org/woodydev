from ...database.async_db_instance import AsyncMongoDB
from ...database.templates.assets import assets_template
from ...database.templates.shots import shots_template
from ...tool.woody_id import create_woody_id

import asyncio
import threading
import copy
from datetime import datetime

async def create_element_db_async(root, group, elementName):

    db = AsyncMongoDB()

    if root == 'Assets':
        collection_name = "assets"
        group_type = "groups"
        group_feild = "group"
        template_type = assets_template

    else:
        collection_name = "shots"
        group_type = "sequences"
        group_feild = "sequence"
        template_type = shots_template
        
    id = create_woody_id(root, group, elementName)
    parent_id = create_woody_id(root, group)

    existing = await db.connect[collection_name].find_one({"id": id})
    if existing:
        print(f"Document '{elementName}' already exists in collection '{collection_name}'.")
        return

    #Create document from template
    template = copy.deepcopy(template_type)
    template["id"] = id
    template["parent_id"] = parent_id
    template[group_feild] = group
    template["name"] = elementName
    template["created_time"] = datetime.now()  
    template["modified_time"] = datetime.now()

    await db.add_document(collection_name, template)
    print(f"Document '{elementName}' is set up in collection '{collection_name}'.")

    # Update doc
    query = {"name": group}
    attribute = collection_name
    update = {"$set": {f"{attribute}.{elementName}": template["id"]}}
    await db.update_document(group_type, query, update)

    print(f"Document '{elementName}' added to '{group_type}' document '{group}'.")
    
def create_element_db(root, group, element_name):

    def run():
        asyncio.run(create_element_db_async(root, group, element_name))
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
