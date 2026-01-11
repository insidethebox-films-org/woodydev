from ...utils.woody_id import get_browser_selection_id
from ...objects import Database

import asyncio
import threading
    
async def get_renders_async():
    
    db = Database()
    
    parent_id = get_browser_selection_id(element_id=True)
    
    docs = await db.get_docs("renders", {"parent_id": parent_id})
    
    return docs

def get_renders(callback):

    def run():
        docs = asyncio.run(get_renders_async())
        callback(docs)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    
async def get_renders_versions_async(selected):
    
    db = Database()
    
    parent_id = get_browser_selection_id(element_id=True)
    id = f"{parent_id}|render:{selected}"
    
    docs = await db.get_doc("renders", {"id": id})
    
    return docs

def get_renders_versions(selected, callback):

    def run():
        docs = asyncio.run(get_renders_versions_async(selected))
        callback(docs)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    