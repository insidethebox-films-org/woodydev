from ...objects.directory import Directory
from ..get_free_port import get_free_port
from ..client_socket import run_server

from ..db_operators import DB_Operators
from ..fd_operators import FD_Operators

import subprocess
import os
import threading

class Blender():
    
    def __init__(self):
        self.db = DB_Operators()
        self.fd = FD_Operators()
    
    def open_file(self, root, group, element, blend_file, woody_id):
        directory = Directory()
        path = directory.construct_path([root, group, element, f"{blend_file}.blend"])
        print(f"Opening blend file: {path}")

        executable = directory.get_dcc_executable("blender")
        
        startup_script = os.path.join(os.path.dirname(__file__), "startup.py")
        
        cmd = [executable, path, "--python", startup_script]
        
        unique_port = get_free_port()

        t = threading.Thread(target=run_server, args=(unique_port, self), daemon=True)
        t.start()
        
        env = os.environ.copy()
        env["WOODY_CURRENT_ID"] = woody_id
        env["BLENDER_TOOL_PORT"] = str(unique_port)
        
        print(f"Opening Blender on Port: {unique_port}")
        
        subprocess.Popen(cmd, env=env)

        return True
        