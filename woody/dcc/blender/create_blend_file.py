from ...objects.directory import Directory

import os
import subprocess

def create_blend_file(blend_path: str) -> bool:
    executable = Directory().get_dcc_executable("blender")
    
    if not executable or not os.path.exists(executable):
        print(f"Invalid Blender executable path: {executable}")
        return False
    
    try:
        cmd = (
            f'"{executable}" --background '
            f'--python-expr "import bpy; bpy.ops.wm.save_as_mainfile(filepath=r\'{blend_path}\')"'
        )
        subprocess.run(cmd, shell=True, check=True)

        if os.path.exists(blend_path):
            print(f"Successfully created blend file at: {blend_path}")
            return True
        print(f"File creation reported success but file not found at: {blend_path}")
        return False

    except subprocess.CalledProcessError as e:
        print(f"Blender process error: {str(e)}")
        return False
    except Exception as e:
        print(f"Error creating blend file: {str(e)}")
        return False

def create_file(root: str, group: str, element: str, blend_name: str) -> bool:
    """Creates a new blend file using path components"""
    
    blend_path = Directory().construct_path([root, group, element, blend_name])
    
    return create_blend_file(blend_path)