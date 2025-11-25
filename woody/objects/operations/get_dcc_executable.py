from ..woody import Woody

import platform
from pathlib import Path

def get_dcc_executable(dcc):
    current_os = platform.system()
    blender_path = Woody().blenderExecutable

    if dcc == "blender":
        if current_os == "Darwin":
            return Path(blender_path) / "Contents" / "MacOS" / "Blender"
        else:
            return Path(blender_path) / "blender.exe"