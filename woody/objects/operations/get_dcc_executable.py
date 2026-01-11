from ..woody import Woody

import platform
from pathlib import Path

def get_dcc_executable(dcc):
    current_os = platform.system()
    woody = Woody()
    blender_path = woody.blenderExecutable
    houdini_path = woody.houdiniExecutable
    rv_path = woody.rvExecutable

    if dcc == "blender":
        if current_os == "Darwin":
            return Path(blender_path) / "Contents" / "MacOS" / "Blender"
        else:
            return Path(blender_path) / "blender.exe"
    elif dcc == "houdini":
        if current_os == "Darwin":
            return Path(houdini_path) / "Contents" / "MacOS" / "Houdini"
        else:
            return Path(houdini_path) / "houdini.exe"
    elif dcc == "rv":
        if current_os == "Darwin":
            return Path(rv_path) / "Contents" / "MacOS" / "RV"
        else:
            return Path(rv_path) / "rv.exe"