import bpy

def set_frame_range(range):
    try:
        start_frame = range[0]
        end_frame = range[1]
        
        scene = bpy.context.scene
        scene.frame_start = start_frame
        scene.frame_end = end_frame
            
        return f"[Blender] Frame range applied: Start[{start_frame}], End[{end_frame}]"
    
    except Exception as e:
        return f"[Blender] Error setting frame range: {e}"