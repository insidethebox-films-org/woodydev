from ....lib.folder.directory_instance import DirectoryInstance

import os
import subprocess

def create_blend_file(executable: str, blend_path: str) -> bool:
    """Creates a new blend file
    
    Args:
        executable (str): Path to Blender executable
        blend_path (str): Path to the blend file to create
    
    Returns:
        bool: True if blend file was created successfully
    """

    dir_instance = DirectoryInstance(blend_path)
    mounted_path = dir_instance.mount or blend_path

    os.makedirs(os.path.dirname(mounted_path), exist_ok=True)

    try:
        cmd = (
            f'"{executable}" --background '
            f'--python-expr "import bpy; bpy.ops.wm.save_as_mainfile(filepath=r\'{mounted_path}\')"'
        )
        subprocess.run(cmd, shell=True, check=True)

        if os.path.exists(mounted_path):
            print(f"Successfully created blend file at: {mounted_path}")
            return True
        print(f"File creation reported success but file not found at: {mounted_path}")
        return False

    except subprocess.CalledProcessError as e:
        print(f"Blender process error: {str(e)}")
        return False
    except Exception as e:
        print(f"Error creating blend file: {str(e)}")
        return False

