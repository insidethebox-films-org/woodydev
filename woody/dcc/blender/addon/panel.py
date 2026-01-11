import bpy
import os

class VIEW3D_PT_context(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_woody_context"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Woody Pipeline"
    bl_category = "Woody"

    def draw(self, context):
        layout = self.layout
        port = os.environ.get('BLENDER_TOOL_PORT', 'NOT SET')

        rootBox = layout.box()
        rootBox.label(text=f"(Port: {port})", icon="OUTLINER")
        rootBox.scale_y = 0.75
        
        # File Section
        file_box = rootBox.box()
        file_header = file_box.row()
        file_header.label(text="File", icon="FILE")
        file_header.scale_y = 1.2
        
        save_row = file_box.row()
        save_row.operator("woody.save", text="Save", icon="FILE_BLEND")
        save_row.scale_y = 1.2
        
        # Publishing Section
        publish_outer_box = rootBox.box()
        publish_header = publish_outer_box.row()
        publish_header.label(text="Publishing", icon="ASSET_MANAGER")
        publish_header.scale_y = 1.2
        
        publish_outer_box.prop(context.scene.woody, "publish_name", text="Name")
        publish_outer_box.prop(context.scene.woody, "publish_type", text="Type")
        
        publish_row = publish_outer_box.row()
        publish_row.operator("woody.publish", text="Publish", icon="SHADING_RENDERED")
        publish_row.scale_y = 1.2
        
        # Metadata Section
        metadata_box = rootBox.box()
        metadata_header = metadata_box.row()
        metadata_header.label(text="Metadata", icon="PROPERTIES")
        metadata_header.scale_y = 1.2
        
        metadata_row = metadata_box.row()
        metadata_row.operator("woody.set_frame_range", text="Frame Range", icon="NEXT_KEYFRAME")
        metadata_row.operator("woody.set_render_settings", text="Render Settings", icon="RENDER_RESULT")
        metadata_row.scale_y = 1.2