import os
import zipfile
from pathlib import Path

def update_zip_dev(addon_dir: str, addon_zip: str) -> bool:
    """Updates the addon zip file for development
    
    Args:
        addon_dir (str): Path to the addon source directory
        addon_zip (str): Path to the output zip file
    
    Returns:
        bool: True if zip file was created successfully
    """
    try:
        # Remove existing zip if it exists
        if os.path.exists(addon_zip):
            os.remove(addon_zip)
        
        # Create parent directory for zip if it doesn't exist
        os.makedirs(os.path.dirname(addon_zip), exist_ok=True)
        
        # Create zip file with correct structure
        addon_dir = Path(addon_dir)
        with zipfile.ZipFile(addon_zip, 'w', zipfile.ZIP_DEFLATED) as z:
            for file in addon_dir.rglob('*'):
                relative_path = os.path.join('woody_blender_addon', file.relative_to(addon_dir))
                z.write(file, relative_path)
        
        print(f"Dev update complete - addon zip created at: {addon_zip}")
        return True
        
    except Exception as e:
        print(f"Error during dev update: {str(e)}")
        return False