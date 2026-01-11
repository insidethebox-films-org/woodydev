import bpy
import os

from ..woody_socket import execute_operation
from ..blend_functions.set_frame_range_bpy import set_frame_range

class WOODY_OT_Set_Frame_Range(bpy.types.Operator):
    bl_idname = "woody.set_frame_range"
    bl_label = "Set Frame Range"
    bl_description = "Set frame range from database"
    
    def execute(self, context):
        woody_id = os.environ.get("WOODY_CURRENT_ID", "")
        
        def on_success(result):
            frame_range = set_frame_range(result)
            print(frame_range)

        def on_error(error):
            self.report({'ERROR'}, f"Failed: {error}")
        
        execute_operation("db.get_frame_range", 
            args={"woody_id": woody_id},
            on_success=on_success,
            on_error=on_error)
        
        return {'FINISHED'}