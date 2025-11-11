from ....tool.woody_id import get_browser_selection_id
from ....database.async_db_instance import AsyncMongoDB

import asyncio
import threading
    
async def get_blends_async():
    
    db = AsyncMongoDB()
    
    parent_id = get_browser_selection_id(element_id=True)
    
    docs = await db.get_docs("blends", {"parent_id": parent_id})
    
    return docs

def get_blends(callback):

    def run():
        docs = asyncio.run(get_blends_async())
        callback(docs)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    
async def get_blend_versions_async(selected):
    
    db = AsyncMongoDB()
    
    parent_id = get_browser_selection_id(element_id=True)
    id = f"{parent_id}|blend:{selected}"
    
    docs = await db.get_doc("blends", {"id": id})
    
    return docs

def get_blend_versions(selected, callback):

    def run():
        docs = asyncio.run(get_blend_versions_async(selected))
        callback(docs)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    