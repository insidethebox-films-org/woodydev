from ...objects.database import Database

import asyncio
import threading

async def get_frame_range_async(woody_id: str):
    try:
        db = Database()
        doc = await db.get_doc("shots", {"id": woody_id})
        
        frame_range = doc.get("frame_range") or {}
        start = frame_range.get("start_frame")
        end = frame_range.get("end_frame")
        
        return [start, end]
    
    except Exception as e:
        return {"error": f"Error getting frame range doc: {e}"}

def get_frame_range(callback, woody_id: str):
    def run():
        result = asyncio.run(get_frame_range_async(woody_id))
        callback(result)

    t = threading.Thread(target=run, daemon=True)
    t.start()