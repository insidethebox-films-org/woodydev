
import bpy

class VIEW3D_PT_context(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_woody_context"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Hello"
    bl_category = "Woody"

    def draw(self, context):
        layout = self.layout

            
        rootBox = layout.box()
        rootBox.label(text=f"777", icon="OUTLINER")
        rootBox.scale_y = 0.75