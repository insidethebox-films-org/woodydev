import bpy
import os
import re
import shutil
import sys
from pathlib import Path

class WOODY_OT_version_up(bpy.types.Operator):
    bl_idname = "woody.version_up"
    bl_label = "Version Up"
    bl_description = "Save current scene and create a new version"
    
    def execute(self, context):
        try:
            # Check if scene has been saved
            if not bpy.data.filepath:
                self.report({'ERROR'}, "Scene has not been saved before. Save it first.")
                return {'CANCELLED'}
            
            # Save current scene first
            bpy.ops.wm.save_mainfile()
            
            # Get current file info
            current_path = Path(bpy.data.filepath)
            directory = current_path.parent
            extension = current_path.suffix
            filename = current_path.stem
            
            # Remove _latest suffix if it exists
            base_filename = filename.replace("_latest", "")
            
            print(f"Processing file: {base_filename}")
            
            # Find existing versions
            version_pattern = re.compile(rf"{re.escape(base_filename)}_v(\d+){re.escape(extension)}$")
            existing_versions = []
            
            for file in directory.iterdir():
                if file.is_file():
                    match = version_pattern.match(file.name)
                    if match:
                        existing_versions.append(int(match.group(1)))
            
            # Calculate next version
            next_version = max(existing_versions, default=0) + 1
            new_filename = f"{base_filename}_v{next_version}{extension}"
            new_file_path = directory / new_filename
            
            # Copy current file to new version
            shutil.copy2(current_path, new_file_path)

            # Create the new _latest filename
            new_latest_filename = f"{base_filename}_latest{extension}"
            new_latest_path = directory / new_latest_filename
            
            # Save current scene as _latest (this will rename the current file)
            bpy.ops.wm.save_as_mainfile(filepath=str(new_latest_path))

            # Remove the original file if it's different from the new _latest file
            if current_path != new_latest_path and current_path.exists():
                os.remove(current_path)
                # Remove Blender's automatic backup file (.blend1)
                backup_file = current_path.with_suffix(current_path.suffix + '1')
                if backup_file.exists():
                    os.remove(backup_file)
            
            print(f"Created version: {new_file_path}")
            print(f"Working file: {new_latest_path}")
            self.report({'INFO'}, f"Version {next_version} created successfully")
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Version up failed: {str(e)}")
            return {'CANCELLED'}
        