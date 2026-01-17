import bpy

from ..blend_functions.save_bpy import save

class WOODY_OT_Save(bpy.types.Operator):
    bl_idname = "woody.save"
    bl_label = "Save"
    bl_description = "Save file"
    
    def execute(self, context):
        save()
        return {'FINISHED'}