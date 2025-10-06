import bpy
import os
import re
import shutil
import sys
from pathlib import Path

from ..prefs.load_woody_prefs import load_woody_preferences

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
            
            # Update database with new version info
            self.update_database(base_filename, str(new_file_path), str(new_latest_path), next_version)
            
            print(f"Created version: {new_file_path}")
            print(f"Working file: {new_latest_path}")
            self.report({'INFO'}, f"Version {next_version} created successfully")
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Version up failed: {str(e)}")
            return {'CANCELLED'}
        
    def update_database(self, blend_name: str, version_path: str, latest_path: str, version_number: int):
        """Update database with new version information"""
        try:
            # Import required libraries (now available thanks to install_blender_libraries)
            from pymongo import MongoClient
            from datetime import datetime, timezone
            
            # Load preferences directly from JSON
            prefs = load_woody_preferences()
            if not prefs:
                print("Could not load woody preferences")
                return
            
            # Get database connection info
            mongo_url = prefs.get("mongoDBAddress")
            project_name = prefs.get("projectName")
            
            if not mongo_url or not project_name:
                print("Warning: MongoDB address or project name not found in preferences")
                return
            
            print(f"Connecting to database: {project_name} at {mongo_url}")
            
            # Connect to MongoDB
            client = MongoClient(mongo_url)
            db = client[project_name]
            
            # Find the blend document
            blend_doc = db["blends"].find_one({"name": blend_name})
            
            if not blend_doc:
                print(f"Warning: Blend document '{blend_name}' not found in database")
                client.close()
                return
            
            # Get existing blend_files or create new dict
            blend_files = blend_doc.get("blend_files", {})
            
            # Remove old latest path if it exists and is different
            old_latest_key = None
            for key, value in blend_files.items():
                if value == "latest" and key != latest_path:
                    old_latest_key = key
                    break

            # Update blend_files dictionary
            blend_files[version_path] = version_number
            blend_files[latest_path] = "latest"
            
            # Remove old latest if found
            if old_latest_key:
                blend_files.pop(old_latest_key, None)
                    
            # Update the document with the complete blend_files object
            update_data = {
                "$set": {
                    "blend_files": blend_files,
                    "modified_time": datetime.now(timezone.utc),
                }
            }
            
            # Update the document
            result = db["blends"].update_one(
                {"_id": blend_doc["_id"]},
                update_data
            )
            
            if result.modified_count > 0:
                print(f"✓ Database updated for blend '{blend_name}' - Version {version_number}")
            else:
                print(f"⚠ No changes made to database for blend '{blend_name}'")
            
            # Close connection
            client.close()
            
        except ImportError as e:
            print(f"Database update failed - missing library: {str(e)}")
            print("Make sure pymongo is installed in Blender's Python environment")
        except Exception as e:
            print(f"Database update failed: {str(e)}")
            import traceback
            traceback.print_exc()
        