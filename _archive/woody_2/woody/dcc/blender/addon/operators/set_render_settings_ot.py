import bpy
import os

from ..woody_socket import execute_operation
from ..blend_functions.set_render_settings_bpy import set_render_settings

class WOODY_OT_Set_Render_Settings(bpy.types.Operator):
    bl_idname = "woody.set_render_settings"
    bl_label = "Set Render Settigns"
    bl_description = "Set render settings from database"
    
    def execute(self, context):
        
        def on_success(result):
            render_settings = set_render_settings(result)
            print(render_settings)

        def on_error(error):
            self.report({'ERROR'}, f"Failed: {error}")
        
        execute_operation("db.get_render_settings",
            on_success=on_success,
            on_error=on_error)
        
        return {'FINISHED'}