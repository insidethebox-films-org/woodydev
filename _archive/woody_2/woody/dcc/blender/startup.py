import bpy
import sys
import os

blender_dir = os.path.dirname(__file__)
if blender_dir not in sys.path:
    sys.path.insert(0, blender_dir)

bpy.ops.preferences.addon_enable(module="addon")
print("[Woody] Addon enabled via startup script")