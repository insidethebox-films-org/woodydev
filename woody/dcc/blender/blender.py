from ...objects.dcc import DCC
from ...objects.directory import Directory

import subprocess
import os
from pathlib import Path

@DCC.register("blender")
class Blender(DCC):
    
    def open_file(self, root, group, element, blend_file):
        directory = Directory()
        path = directory.construct_path([root, group, element, f"{blend_file}.blend"])
        print(f"Opening blend file: {path}")
    
        executable = directory.get_dcc_executable("blender")
        socket = os.path.join(os.path.dirname(__file__), "blender_socket.py")
        addon = os.path.join(os.path.dirname(__file__), "addon","__init__.py")
        
        cmd = [executable, path, "--python", socket, "--python", addon]
        
        subprocess.Popen(cmd)

        return True