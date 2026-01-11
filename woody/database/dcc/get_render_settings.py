from ...objects.database import Database
import asyncio
import threading

async def get_render_settings_async():
    try:
        db = Database()
        docs = await db.get_docs("settings", {"render_settings": True})
        
        global_render_settings = next((item for item in docs if item.get("type") == "global"), None)
        blender_render_settings = next((item for item in docs if item.get("type") == "blender"), None)
        
        if global_render_settings:
            global_render_settings.pop("_id", None)
        
        if blender_render_settings:
            blender_render_settings.pop("_id", None)
        
        return {
            "global": global_render_settings,
            "blender": blender_render_settings
        }
    
    except Exception as e:
        print(f"Error getting render settings: {e}")
        return None

def get_render_settings(callback):
    def run():
        result = asyncio.run(get_render_settings_async())
        callback(result)

    t = threading.Thread(target=run, daemon=True)
    t.start()