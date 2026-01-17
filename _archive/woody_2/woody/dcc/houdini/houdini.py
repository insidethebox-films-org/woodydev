from ...objects.directory import Directory
from ..client_socket import run_server
from ..get_free_port import get_free_port
from ...utils.woody_id import woody_product_id_to_filepath
from ...utils.woody_id import explode_woody_id
from ...objects.ffmpeg import FFmpegBatch

from ..db_operators import DB_Operators
from ..fd_operators import FD_Operators

import subprocess
import threading
import os
from pathlib import Path

class Houdini():
    
    def __init__(self):
        self.db = DB_Operators()
        self.fd = FD_Operators()
        self.woody_id_to_filepath = woody_product_id_to_filepath
        self.explode_woody_id = explode_woody_id

    def open_file(self, root, group, element, hip_file, woody_id):
        directory = Directory()
        path = directory.construct_path([root, group, element, f"{hip_file}.hip"])
        
        current_dir = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
        hda_dir = os.path.join(current_dir, "hda").replace("\\", "/")
        scripts_dir = os.path.join(current_dir, "scripts").replace("\\", "/")
        bundled_ocio = str((Path(__file__).parent.parent.parent / "resources" / "cg-config-v2.2.0_aces-v1.3_ocio-v2.3.ocio").resolve())
        
        executable = directory.get_dcc_executable("houdini")
        unique_port = get_free_port()

        t = threading.Thread(target=run_server, args=(unique_port, self), daemon=True)
        t.start()

        env = os.environ.copy()
        
        env["WOODY_CURRENT_ID"] = woody_id
        env["HOUDINI_TOOL_PORT"] = str(unique_port)
        
        if os.path.exists(bundled_ocio):
            env["OCIO"] = bundled_ocio
        else:
            print(f"Warning: Bundled OCIO not found at {bundled_ocio}. Falling back to default.")
        
        sep = os.pathsep
        existing_pythonpath = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = f"{scripts_dir}{sep}{existing_pythonpath}" if existing_pythonpath else scripts_dir

        env["HOUDINI_OTLSCAN_PATH"] = f"{hda_dir}{sep}&"

        print(f"Launching Houdini on Port: {unique_port}")
        
        try:
            subprocess.Popen([executable, path], env=env)
        except Exception as e:
            print(f"Error launching Houdini: {e}")
            return False

        return True
        
    def publish(self, publish_name, woody_id):
        
        base_path = self.fd.create_publish_fd(woody_id)
        
        id_parts = self.explode_woody_id(woody_id)
        file_name = (
                f"{id_parts[1]}_{id_parts[2]}_{id_parts[3]}_"
                f"{publish_name}_latest.usd"
            )
        
        file_path = os.path.join(base_path, "publish", file_name)
        
        self.db.publish(
            name=publish_name,
            publish_type=".usd",
            dcc="houdini",
            woody_id=woody_id,
            file_path=file_path
        )
        
        return file_path
    
    def render(self, render_name, woody_id, comment):
        
        base_path, version = self.fd.create_render_fd(woody_id, render_name)
        
        id_parts = self.explode_woody_id(woody_id)
        
        file_name = (
                f"{id_parts[1]}_{id_parts[2]}_{id_parts[3]}_"
                f"{render_name}_v{version:03d}_<F4>.exr"
            )
        db_file_name = (
                f"{id_parts[1]}_{id_parts[2]}_{id_parts[3]}_"
                f"{render_name}_v{version:03d}_#.exr"
            )
        
        file_path = os.path.join(base_path, file_name)
        db_file_path = os.path.join(base_path, db_file_name)
        
        self.db.render(
            render_name, 
            woody_id, 
            db_file_path, 
            comment
        )
        
        return file_path
    
    def post_render_task(self, render_path):
        render_dir = os.path.dirname(render_path)
        ffmpeg = FFmpegBatch()
        ffmpeg.add_dir(render_dir)

        previews_dir = os.path.join(render_dir, "previews")
        os.makedirs(previews_dir, exist_ok=True)

        def on_previews_complete(success, msg):
            if success:
                print(f"Preview frames generated in: {msg}")
            else:
                print(f"Preview frame generation failed: {msg}")


        ffmpeg.generate_previews(
            preview_subfolder="previews",
            width=512,
            on_complete=on_previews_complete
        )

        return
    