import bpy

def save():
    try:
        bpy.ops.wm.save_mainfile()
        blend_path = bpy.data.filepath
        return f"File Saved at: {blend_path}"
    except Exception as e:
        return f"Error Saving File: {e}"