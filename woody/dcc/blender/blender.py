from ...objects.dcc import DCC
from ...objects.woody import Woody
from ...ui.dcc.dcc_gui import DccGui
import subprocess

import os

@DCC.register("blender")
class Blender(DCC):
    
    def open_file(self):
        executable = Woody().blenderExecutable + "blender.exe"
        socket = os.path.join(os.path.dirname(__file__), "blender_socket.py")
        addon = os.path.join(os.path.dirname(__file__), "addon","__init__.py")
        
        subprocess.Popen([
            executable,
            "--python", socket, "--python", addon
        ]) 
        
        #DccGui()
    
        return True
        