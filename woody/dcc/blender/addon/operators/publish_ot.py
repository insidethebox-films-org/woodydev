from ..woody_socket import execute_operation
from utils.explode_woody_id import explode_woody_id
from ..blend_functions.usd_publish_bpy import usd_publish
from ..blend_functions.publish_bpy import obj_publish, abc_publish

import bpy
import os

class WOODY_OT_Publish(bpy.types.Operator):
    bl_idname = "woody.publish"
    bl_label = "Publish"
    bl_description = "Publish Selected"
    
    def execute(self, context):
        
        def on_success(result):
            publish_dir = result.get("base_path") if isinstance(result, dict) else result
            print(f"Folder created: {publish_dir}")
            self.create_publish(context, publish_dir)

        def on_error(error):
            self.report({'ERROR'}, f"Failed: {error}")
        
        execute_operation(
            "fd.create_publish_fd", 
            args={"woody_id": os.environ.get("WOODY_CURRENT_ID", "")},
            on_success=on_success,
            on_error=on_error
        )
        
        return {'FINISHED'}
        
    def create_publish(self, context, publish_dir):
        
        woody = context.scene.woody

        woody_id = os.environ.get("WOODY_CURRENT_ID", "")
        asset_parts = explode_woody_id(woody_id)
        asset_name = f"{asset_parts[1]}_{asset_parts[2]}_{asset_parts[3]}"

        publish_name = woody.publish_name
        publish_type = woody.publish_type

        ext_map = {
            'USD': '.usd',
            'BLEND': '.blend',
            'OBJ': '.obj',
            'ABC': '.abc',
        }
        ext = ext_map.get(publish_type, '.usd')

        filename = f"{asset_name}_{publish_name}_latest{ext}"
        file_path = os.path.join(publish_dir, "publish", filename)

        def on_success(result):
            if ext == ".usd":
                usd_publish(publish_dir, asset_name, publish_name)
                print("USD publish Created")
            elif ext ==".obj":
                obj_publish(file_path)
                print("OBJ publish Created")
            elif ext ==".abc":
                abc_publish(file_path)
                print("Alembic publish Created")
            else:
                print("Please select a valid publish type")

        def on_error(error):
            self.report({'ERROR'}, f"Failed: {error}")

        execute_operation(
            "db.publish",
            args={
                "name": publish_name,
                "publish_type": ext,
                "dcc": "blender",
                "woody_id": woody_id,
                "file_path": file_path
            },
            on_success=on_success,
            on_error=on_error
        )