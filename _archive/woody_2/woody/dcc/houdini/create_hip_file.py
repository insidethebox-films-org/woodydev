from ...objects.directory import Directory

import os
import subprocess

def create_houdini_file(hip_path: str) -> bool:

    executable = Directory().get_dcc_executable("houdini")
    
    if not executable or not os.path.exists(executable):
        print(f"Invalid Houdini executable path: {executable}")
        return False
    
    hython_exe = str(executable).replace("houdini.exe", "hython.exe").replace("houdinifx.exe", "hython.exe")
    
    if not os.path.exists(hython_exe):
        print(f"hython not found at: {hython_exe}")
        return False
    
    try:
        os.makedirs(os.path.dirname(hip_path), exist_ok=True)
        
        python_code = f"import hou; hou.hipFile.save(file_name=r'{hip_path}')"
        
        cmd = [
            hython_exe,
            "-c",
            python_code
        ]
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)

        if os.path.exists(hip_path):
            print(f"Successfully created hip file at: {hip_path}")
            return True
        print(f"File creation reported success but file not found at: {hip_path}")
        return False

    except subprocess.CalledProcessError as e:
        print(f"Houdini process error: {str(e)}")
        return False
    except Exception as e:
        print(f"Error creating hip file: {str(e)}")
        return False

def create_file(root: str, group: str, element: str, hip_name: str) -> bool:
    
    hip_path = Directory().construct_path([root, group, element, hip_name])
    
    return create_houdini_file(hip_path)