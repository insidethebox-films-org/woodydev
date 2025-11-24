import bpy

class VIEW3D_PT_context(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_woody_context"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Woody Pipeline"
    bl_category = "Woody"

    def draw(self, context):
        layout = self.layout

        # Woody Tools Section
        rootBox = layout.box()
        rootBox.label(text="Woody", icon="OUTLINER")
        rootBox.scale_y = 0.75
        
        # Add Version Up button
        row = rootBox.row()
        row.operator("woody.launch_ui", text="Launch UI", icon="FILE_REFRESH")