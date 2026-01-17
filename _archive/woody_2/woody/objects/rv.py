import subprocess
import os
from pathlib import Path
import copy
import tempfile

from .directory import Directory

class RVPlayer:
    def __init__(self):
        self.directory = Directory()
        self.rv_exe = self.directory.get_dcc_executable("rv")
        self.ocio_path = self._find_ocio_config()

    def _find_ocio_config(self):
        resources_dir = Path(__file__).parent.parent / "resources"
        for ocio_file in resources_dir.glob("*.ocio"):
            return ocio_file
        return None

    def play(self, frame_path):
        if Path(frame_path).is_dir():
            print("Warning: Provide a directory-like path; please provide a file or sequence pattern.")
            return

        env = copy.deepcopy(os.environ)
        if self.ocio_path:
            env["OCIO"] = str(self.ocio_path)
            env["RV_OCIO_SOURCE_SETUP"] = "1"
            env["RV_OCIO_DISPLAY_SETUP"] = "1"

        cmd = [
            self.rv_exe,
            str(frame_path)
        ]

        try:
            subprocess.Popen(cmd, env=env)
            print(f"OpenRV: Launching {frame_path}")
            print(f"OCIO Config: {self.ocio_path}")
        except Exception as e:
            print(f"Failed to launch RV: {e}")