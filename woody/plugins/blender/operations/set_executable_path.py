import os

def set_executable_path(base_path: str) -> str:
    """Set the correct path to blender.exe
    
    Args:
        base_path (str): Base path to Blender executable or directory
    
    Returns:
        str: Full path to blender.exe, or None if base_path is empty
    """
    if not base_path:
        return None
        
    if os.path.isdir(base_path):
        return os.path.join(base_path, "blender.exe")
    elif not base_path.endswith('.exe'):
        return base_path + ".exe"
    return base_path