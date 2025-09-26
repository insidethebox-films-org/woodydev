import os

from ...tool import WoodyInstance
from .operations import *

class BlenderInstance:
    def __init__(self):
        self.woody = WoodyInstance()
        self.executable = set_executable_path(self.woody.blenderExecutable)

        self.addon_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../woody_blender_addon"))  #TODO hardcoded path
        self.addon_zip = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../woody_blender_addon.zip")) #TODO hardcoded path
        
    def create_file(self, group_type: str, group_name: str, element_name: str) -> bool:
        """Creates a new blend file"""
        if not self.executable or not os.path.exists(self.executable):
            print(f"Invalid Blender executable path: {self.executable}")
            return False

        blend_path = get_blend_path(
            str(self.woody.projectDirectory),
            str(self.woody.projectName),
            group_type,
            group_name,
            element_name
        )
        
        return create_blend_file(self.executable, blend_path)

    def open_file(self, group_type: str, group_name: str, element_name: str) -> bool:
        """Opens existing blend file with addon update check"""
        if not self.executable or not os.path.exists(self.executable):
            print(f"Invalid Blender executable path: {self.executable}")
            return False
        
        blend_path = get_blend_path(
            str(self.woody.projectDirectory),
            str(self.woody.projectName),
            group_type,
            group_name,
            element_name
        )
        
        return open_blend_file(self.executable, blend_path, self.addon_zip)
    
    def dev_update(self) -> bool:
        """Updates the addon zip file for development"""
        return update_zip_dev(self.addon_dir, self.addon_zip)