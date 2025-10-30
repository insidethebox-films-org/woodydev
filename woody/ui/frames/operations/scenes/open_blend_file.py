from .....tool.woody_instance import WoodyInstance
from .....plugins.blender.blender_instance import BlenderInstance

def open_blend_file(self):
    
    woody = WoodyInstance().browser_selection()
    blender = BlenderInstance()
    group_type_selection = woody.get("group_type")
    group_selection = woody.get("group")
    element_selection = woody.get("element")
    blend_selection = self.blends_list_box.get()
    version_selection = self.blend_version_list_box.get()
    
    group_type = "assets" if group_type_selection == "Assets Group" else "shots"
    
    if version_selection == "latest":
        blender.open_file(
            group_type,
            group_selection, 
            element_selection,
            f"{blend_selection}_latest.blend",
        )   
    else:
        blender.open_file(
            group_type,
            group_selection, 
            element_selection,
            f"{blend_selection}_{version_selection}.blend",
        )