from ...objects.dcc import DCC
from ...objects.directory import Directory
from ...dcc.blender.client_socket import execute_operation
from ...dcc.database.get_frame_range import get_frame_range
from ...dcc.database.get_render_settings import get_render_settings

import subprocess
import os
@DCC.register("blender")
class Blender(DCC):
    
    def open_file(self, root, group, element, blend_file, woody_id):
        directory = Directory()
        path = directory.construct_path([root, group, element, f"{blend_file}.blend"])
        print(f"Opening blend file: {path}")
    
        executable = directory.get_dcc_executable("blender")
        socket = os.path.join(os.path.dirname(__file__), "blender_socket.py")
        addon = os.path.join(os.path.dirname(__file__), "addon","__init__.py")
        
        cmd = [executable, path, "--python", socket, "--python", addon]
        
        env = os.environ.copy()
        env["WOODY_CURRENT_ID"] = woody_id
        
        subprocess.Popen(cmd, env=env)

        return True
    
    def save_file(self, port):
        def print_result(result):
            print(result)
        execute_operation("save", port=port, on_success=print_result)
        
    def set_frame_range(self, port, woody_id):
        def handle_query(range):
            if not range:
                print(f"[Woody] No doc found for woody_id {woody_id}")
                return
            
            def print_result(result):
                print(result)

            execute_operation(
                "set_frame_range",
                port=port,
                args={"range": range},
                on_success=print_result,
            )

        get_frame_range(handle_query, woody_id)
        
    def set_render_settings(self, port):
        def handle_query(render_settings):
            if not render_settings:
                print(f"[Woody] No render settings found.")
                return
            
            def print_result(result):
                print(result)

            execute_operation(
                "set_render_settings",
                port=port,
                args={"render_settings": render_settings},
                on_success=print_result,
                on_error=print_result
            )

        get_render_settings(handle_query)
        