from ...objects.dcc import DCC
from ...objects.directory import Directory

import subprocess
import os

@DCC.register("blender")
class Blender(DCC):
    
    def open_file(self):
        executable = Directory().get_dcc_executable("blender")
        socket = os.path.join(os.path.dirname(__file__), "blender_socket.py")
        addon = os.path.join(os.path.dirname(__file__), "addon","__init__.py")
        
        subprocess.Popen([
            executable,
            "--python", socket, "--python", addon
        ])

        return True
         