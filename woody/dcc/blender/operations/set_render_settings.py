import bpy

def set_render_settings(render_settings):
    try:
        global_settings = render_settings["global"]
        blender_settings = render_settings["blender"]
        
        scene = bpy.context.scene
        render = scene.render
        view = scene.view_settings
        cycles = scene.cycles
        
        render.resolution_x = int(global_settings["resolution"]["x"])
        render.resolution_y = int(global_settings["resolution"]["y"])
        
        render.fps = int(global_settings["framerate"])
        
        #render.image_settings.file_format = global_settings["file_format"]
        
        #view.view_transform = global_settings["colour_space"]

        if blender_settings["render_engine"] == "Cycles":
            render.engine = 'CYCLES'

            cycles.samples = int(blender_settings["max_samples"])
            cycles.preview_samples = int(blender_settings["min_samples"])

            cycles.use_adaptive_sampling = True
            cycles.adaptive_threshold = float(blender_settings["noise_threshold"])

            cycles.time_limit = float(blender_settings["time_limit"])

            denoise = blender_settings["denoise"]
            cycles.use_denoising = bool(denoise) if isinstance(denoise, bool) else denoise.lower() == "true"

        motion_blur = blender_settings["motion_blur"]
        render.use_motion_blur = bool(motion_blur) if isinstance(motion_blur, bool) else motion_blur.lower() == "true"
        
        return "Render Settings Applied Successfully"
    
    except Exception as e:
        return f"Error setting render settings: {e}"