from ....tool.woody_id import get_browser_selection_id
from ....tool.memory_store import store
from ....objects import Database

import asyncio
import threading
    
async def get_asset_details_async():
    
    db = Database()
    data = store.get_namespace("browser_selection")
    root = data.get("root")
    id = get_browser_selection_id(element_id=True)
    
    if root == "Assets":
        collection_name = "assets"
    else:
        collection_name = "shots"
    
    docs = await db.get_doc(collection_name, {"id": id})
    
    return docs

def get_asset_details(callback):

    def run():
        docs = asyncio.run(get_asset_details_async())
        callback(docs)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()