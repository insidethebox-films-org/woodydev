bl_info = {
    "name": "Woody",
    "author": "Oscar Bartle",
    "version": (0, 0, 1),
    "blender": (4, 2, 5),
    "location": "3D Viewport > Sidebar > Woody",
    "description": "A pipeline tool",
    "category": "Development",
}

import bpy
import os

from .woody_socket import execute_operation
from .properties import Properties
from .panel import VIEW3D_PT_context
from .operators.save_ot import WOODY_OT_Save
from .operators.publish_ot import WOODY_OT_Publish
from .operators.set_frame_range_ot import WOODY_OT_Set_Frame_Range
from .operators.set_render_settings_ot import WOODY_OT_Set_Render_Settings

bpy.woody = execute_operation

print("[Woody] Addon initialized")
print(f"[Woody] Port: {os.environ.get('BLENDER_TOOL_PORT', 'NOT SET')}")
print(f"[Woody] ID: {os.environ.get('WOODY_CURRENT_ID', 'NOT SET')}")

classes = [
    Properties,
    VIEW3D_PT_context, 
    WOODY_OT_Save,
    WOODY_OT_Publish,
    WOODY_OT_Set_Frame_Range,
    WOODY_OT_Set_Render_Settings
    ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.woody = bpy.props.PointerProperty(type=Properties)
    
    print(f"[Woody] Registered {len(classes)} classes")

def unregister():
    del bpy.types.Scene.woody
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()