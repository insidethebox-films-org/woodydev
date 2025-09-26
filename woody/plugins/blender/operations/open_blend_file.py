import os
import subprocess
import time

from pathlib import Path

def open_blend_file(executable: str, blend_path: str, addon_zip: str) -> bool:
    """Opens existing blend file with addon update check
    
    Args:
        executable (str): Path to Blender executable
        blend_path (str): Path to the blend file to open
        addon_zip (str): Path to the addon zip file
        
    Returns:
        bool: True if blend file was opened successfully
    """
    try:
        blend_dir = os.path.dirname(blend_path)
        
        # Convert to Path object to handle network paths better
        blend_dir_path = Path(blend_dir)
        
        # Create all directories in path if they don't exist
        blend_dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create startup script in same directory as blend file
        startup_path = blend_dir_path / "_startup.py"

        # Create startup script
        startup_script = f"""
import bpy
import addon_utils
import os
import hashlib
import json

def get_zip_hash(zip_path):
    if not os.path.exists(zip_path):
        return ""
    with open(zip_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

addon_name = "woody_blender_addon"
zip_path = r"{addon_zip}"
current_hash = get_zip_hash(zip_path)

# Get stored hash if it exists
prefs_path = os.path.join(bpy.utils.user_resource('CONFIG'), "woody_addon_hash.json")
stored_hash = ""
if os.path.exists(prefs_path):
    with open(prefs_path, 'r') as f:
        stored_hash = json.load(f).get('hash', '')

# Only update if hash is different
if current_hash != stored_hash:
    print(f"Addon update detected, reinstalling {{addon_name}}...")
    
    # Safely disable addon if enabled
    if addon_name in bpy.context.preferences.addons:
        addon_utils.disable(addon_name)
    
    # Remove addon modules from sys.modules to force reload
    import sys
    for key in list(sys.modules.keys()):
        if key.startswith(addon_name):
            del sys.modules[key]
    
    # Install and enable addon
    bpy.ops.preferences.addon_install(overwrite=True, target='DEFAULT', filepath=zip_path)
    addon_utils.enable(addon_name, default_set=True, persistent=True)
    
    # Store new hash
    with open(prefs_path, 'w') as f:
        json.dump({{'hash': current_hash}}, f)
else:
    print(f"Addon {{addon_name}} is up to date")

# Save preferences
bpy.ops.wm.save_userpref()
"""
    
        print(f"Writing startup script to: {startup_path}")
        
        # Write startup script
        startup_path.write_text(startup_script)
        time.sleep(0.5)  # Give the filesystem time to complete the write
        
        if not startup_path.exists():
            print(f"Error: Failed to create startup script at {startup_path}")
            return False
            
        try:
            # Verify we can read the file
            test_read = startup_path.read_text()
            if not test_read:
                print("Error: Startup script exists but is empty")
                return False
        except Exception as e:
            print(f"Error: Cannot read startup script: {e}")
            return False

        print(f"Launching Blender with: {blend_path}")
        
        # Launch Blender
        subprocess.Popen([
            executable,
            str(blend_path),  # Convert Path to string
            "--python", str(startup_path)  # Convert Path to string
        ])
        
        # Give Blender time to read the startup script before we delete it
        time.sleep(2)

        return True
    
    except Exception as e:
        print(f"Error in open_blend_file: {str(e)}")
        return False
    finally:
        # Clean up startup script
        try:
            if startup_path.exists():
                startup_path.unlink()
                print(f"Cleaned up startup script: {startup_path}")
        except Exception as e:
            print(f"Error cleaning up startup script: {str(e)}")