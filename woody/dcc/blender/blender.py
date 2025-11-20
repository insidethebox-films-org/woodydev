from ...objects.dcc import DCC
from ...objects.woody import Woody
import subprocess

@DCC.register("blender")
class Blender(DCC):
    
    def open_file(self):
        executable = Woody().blenderExecutable + "blender.exe"
        subprocess.Popen([
            executable
        ])  
        
        return True
        