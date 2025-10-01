import os

def get_blend_path(project_dir: str, project_name: str, group_type: str, 
                   group_name: str, element_name: str, blend_name: str) -> str:
    """Constructs blend file path
    
    Args:
        project_dir (str): Base project directory
        project_name (str): Name of the project
        group_type (str): "assets" or "shots"
        group_name (str): Name of the asset or shot group
        element_name (str): Name of the specific asset or shot

    Returns:
        str: Full path to the blend file
    """
    path_components = [
        project_dir,
        project_name,
        group_type,
        group_name,
        element_name,
        f"{blend_name}.blend"
    ]
    
    if project_dir.startswith(r'\\'): 
        return os.path.join(*path_components)
    else:
        return os.path.normpath(os.path.join(*path_components))