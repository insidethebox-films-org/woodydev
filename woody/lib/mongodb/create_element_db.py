from ...objects import Database
from ...templates.assets import assets_template
from ...templates.shots import shots_template
from ...tool.woody_id import create_woody_id

import asyncio
import threading
import copy
from datetime import datetime

async def create_element_db_async(root, group, elementName):

    db = Database()

    if root == 'Assets':
        collection_name = "assets"
        group_type = "groups"
        group_field = "group"
        template_type = assets_template

    else:
        collection_name = "shots"
        group_type = "sequences"
        group_field = "sequence"
        template_type = shots_template
        
    id = create_woody_id(root, group, elementName)
    parent_id = create_woody_id(root, group)

    existing = await db.connect[collection_name].find_one({"id": id})
    if existing:
        print(f"Document '{elementName}' already exists in collection '{collection_name}'.")
        return

    try:
        #Create document from template
        template = copy.deepcopy(template_type)
        template["id"] = id
        template["parent_id"] = parent_id
        template[group_field] = group
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

    except Exception as e:
        print(f"Error creating element document: {str(e)}")
        return False
    
    print(f"Document '{elementName}' added to '{group_type}' document '{group}'.")
    
def create_element_db(root, group, element_name):

    def run():
        asyncio.run(create_element_db_async(root, group, element_name))
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
