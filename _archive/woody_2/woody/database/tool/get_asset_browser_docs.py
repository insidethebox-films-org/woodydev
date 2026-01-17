from ...objects.memory_store import store
from ...objects import Database

import asyncio
import threading
    
async def get_groups_async():
    
    db = Database()
    
    data = store.get_namespace("browser_selection")
    root = data.get("root", "Assets")
    
    if root == "Assets":
        collection_name = "groups"
    else:
        collection_name = "sequences"
    
    docs = await db.get_docs(collection_name)
    
    return docs

def get_groups(callback):

    def run():
        docs = asyncio.run(get_groups_async())
        callback(docs)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    
async def get_elements_async():
    
    db = Database()
    
    data = store.get_namespace("browser_selection")
    root = data.get("root", "Assets")
    group = data.get("group")
    
    if not group:
        return []
    
    if root == "Assets":
        collection_name = "assets"
        parent_field = "group"
    else:
        collection_name = "shots"
        parent_field = "sequence"
    
    query = {parent_field: group}
    docs = await db.get_docs(collection_name, query)
    
    return docs

def get_elements(callback):

    def run():
        docs = asyncio.run(get_elements_async())
        callback(docs)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()