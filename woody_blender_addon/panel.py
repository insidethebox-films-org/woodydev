
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
        rootBox.label(text="Woody Tools", icon="OUTLINER")
        rootBox.scale_y = 0.75
        
        # Add Version Up button
        row = rootBox.row()
        row.operator("woody.version_up", text="Version Up", icon="FILE_REFRESH")
        #Add Publish button
        row = rootBox.row()
        row.operator("woody.publish", text="Publish", icon="FILE_REFRESH")
        
        # Load Publishes Section
        layout.separator()
        loadBox = layout.box()
        loadBox.label(text="Load Publishes", icon="LINK_BLEND")
        
        # Publish ID input field
        row = loadBox.row()
        row.prop(context.scene, "woody_publish_id", text="Publish ID")
        
        # Version input field
        row = loadBox.row()
        row.prop(context.scene, "woody_publish_version", text="Version")
        
        # Load button
        row = loadBox.row()
        row.operator("woody.load_publish", text="Load Publish", icon="LIBRARY_DATA_DIRECT")
        
        # Loaded publishes info
        layout.separator()
        infoBox = layout.box()
        infoBox.label(text="Scene Publishes", icon="OUTLINER_COLLECTION")
        
        # Show count of loaded publishes
        loaded_count = getattr(context.scene, 'woody_loaded_publishes_count', 0)
        row = infoBox.row()
        row.label(text=f"Loaded: {loaded_count} published assets")
        
        # Show list of loaded publishes
        display_text = getattr(context.scene, 'woody_loaded_publishes_display', "No published assets loaded")
        if loaded_count > 0:
            # Split by lines and display each one
            for line in display_text.split('\n'):
                if line.strip():
                    row = infoBox.row()
                    row.label(text=f"  • {line}", icon="LINKED")
        
        # Refresh button
        row = infoBox.row()
        row.operator("woody.refresh_loaded_publishes", text="Refresh List", icon="FILE_REFRESH")