from ...objects.database import Database
from ...templates.render import render_template
from ...utils.woody_id import explode_woody_id

import asyncio
import threading
import copy
from datetime import datetime
from pathlib import Path

async def render_db_async(name, woody_id, file_path, comment):
    db = Database()
    collection_name = "renders"
    id = f"{woody_id}|render:{name}"
    
    existing_doc = await db.get_doc(collection_name, {"id": id})
    id_parts = explode_woody_id(woody_id)
    filename = Path(file_path).name

    def build_relative_path(parts, render_name, version_folder, filename):
        return str(Path(*parts, "renders", render_name, version_folder, filename))

    if existing_doc:
        versions = existing_doc.get("versions", {})
        version_numbers = [
            int(k[1:]) for k in versions.keys()
            if k.startswith("v") and k[1:].isdigit()
        ]
        next_version = max(version_numbers, default=0) + 1
        version_key = f"v{next_version}"

        version_folder = version_key
        relative_path = build_relative_path(id_parts[1:], name, version_folder, filename)

        versions[version_key] = {
            "path": relative_path,
            "comment": comment
        }

        await db.update_document(
            collection_name,
            {"id": id},
            {"$set": {"versions": versions, "updated_time": datetime.now()}}
        )
        print(f"Added version {version_key} to '{name}'")
        return True
    else:
        try:
            version_key = "v1"
            render_name = name
            version_folder = version_key
            relative_path = build_relative_path(id_parts[1:], render_name, version_folder, filename)
            
            template = copy.deepcopy(render_template)
            template["id"] = id
            template["parent_id"] = woody_id
            template["name"] = name
            template["versions"] = {
                version_key: {
                    "path": relative_path,
                    "comment": comment
                }
            }
            template["created_time"] = datetime.now() 
            
            await db.add_document(collection_name, template)
            print(f"Render document created successfully for '{name}'")
            return True
        
        except Exception as e:
            print(f"Error creating render doc: {e}")
            return False
    
def render_db(name, woody_id, file_path, comment):
    def run():
        asyncio.run(render_db_async(name, woody_id, file_path, comment))

    t = threading.Thread(target=run, daemon=True)
    t.start()