import bpy
from pathlib import Path
from ..utils.get_db_connection import get_database_connection

class WOODY_OT_load_publish(bpy.types.Operator):
    bl_idname = "woody.load_publish"
    bl_label = "Load Publish"
    bl_description = "Link a published asset using publish ID and version"

    def execute(self, context):
        # Get the publish ID and version from scene properties
        publish_id = getattr(context.scene, 'woody_publish_id', '').strip()
        version = getattr(context.scene, 'woody_publish_version', 'latest').strip()
        
        if not publish_id:
            self.report({'ERROR'}, "Please enter a publish ID first")
            return {'CANCELLED'}

        # Query database for publish information
        publish_info = self.get_publish_info(publish_id, version)
        if not publish_info:
            self.report({'ERROR'}, f"Could not find publish with ID: {publish_id}, version: {version}")
            return {'CANCELLED'}
        
        # Extract file path and metadata
        blend_path = Path(publish_info['file_path']).resolve()
        publish_type = publish_info['publish_type']
        custom_name = publish_info['custom_name']
        
        if not blend_path.exists():
            self.report({'ERROR'}, f"Published file not found: {blend_path}")
            return {'CANCELLED'}

        # Prevent linking from the current file
        current_path = Path(bpy.data.filepath).resolve() if bpy.data.filepath else None
        if current_path and current_path == blend_path:
            self.report({'ERROR'}, "Cannot link from the current file")
            return {'CANCELLED'}

        try:
            # Load based on publish type
            linked_items = self.load_by_type(str(blend_path), publish_type, context)
            
            if linked_items:
                items_str = ", ".join(linked_items)
                display_name = f"{publish_type.title()} - {custom_name} - {version}"
                self.report({'INFO'}, f"✅ Linked {publish_type}: {items_str}")
                
                # Clear the input fields after successful load
                context.scene.woody_publish_id = ""
                context.scene.woody_publish_version = "latest"
                
                # Refresh the loaded publishes list
                self.refresh_loaded_publishes(context)
                
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, f"Failed to link any {publish_type}s")
                return {'CANCELLED'}

        except Exception as e:
            self.report({'ERROR'}, f"Loading failed: {str(e)}")
            return {'CANCELLED'}

    def get_publish_info(self, publish_id: str, version: str):
        """Query database for publish information"""
        try:
            client, db, error = get_database_connection()
            if error or client is None or db is None:
                print(f"Database connection error: {error}")
                return None

            # Find the publish document by ID
            publish_doc = db["publishes"].find_one({"publish_id": publish_id})
            
            if not publish_doc:
                client.close()
                return None
            
            # Get the specific version
            published_versions = publish_doc.get("published_versions", {})
            
            if version not in published_versions:
                client.close()
                return None
            
            version_info = published_versions[version]
            
            # Return combined information
            result = {
                "file_path": version_info.get("published_path", ""),
                "publish_type": publish_doc.get("publish_type", ""),
                "custom_name": publish_doc.get("custom_name", ""),
                "source_asset": publish_doc.get("source_asset", ""),
                "version": version,
                "publish_id": publish_id
            }
            
            client.close()
            return result
            
        except Exception as e:
            print(f"Error querying publish info: {e}")
            return None

    def load_by_type(self, blend_path: str, publish_type: str, context):
        """Load assets based on their publish type"""
        linked_items = []
        
        if publish_type.upper() == "COLLECTION":
            linked_items = self.load_collections(blend_path, context)
        elif publish_type.upper() == "MATERIAL":
            linked_items = self.load_materials(blend_path, context)
        elif publish_type.upper() == "OBJECT":
            linked_items = self.load_objects(blend_path, context)
        elif publish_type.upper() == "MESH":
            linked_items = self.load_meshes(blend_path, context)
        else:
            # Fallback: try to load collections first, then other types
            linked_items = self.load_collections(blend_path, context)
            if not linked_items:
                linked_items = self.load_materials(blend_path, context)
            if not linked_items:
                linked_items = self.load_objects(blend_path, context)
        
        return linked_items

    def load_collections(self, blend_path: str, context):
        """Load collections from blend file"""
        linked_items = []
        
        with bpy.data.libraries.load(blend_path, link=True) as (data_from, data_to):
            if data_from.collections:
                data_to.collections = data_from.collections

        for col in data_to.collections:
            if col:
                context.scene.collection.children.link(col)
                linked_items.append(col.name)
        
        return linked_items

    def load_materials(self, blend_path: str, context):
        """Load materials from blend file"""
        linked_items = []
        
        with bpy.data.libraries.load(blend_path, link=True) as (data_from, data_to):
            if data_from.materials:
                data_to.materials = data_from.materials

        for mat in data_to.materials:
            if mat:
                linked_items.append(mat.name)
        
        return linked_items

    def load_objects(self, blend_path: str, context):
        """Load objects from blend file"""
        linked_items = []
        
        with bpy.data.libraries.load(blend_path, link=True) as (data_from, data_to):
            if data_from.objects:
                data_to.objects = data_from.objects

        for obj in data_to.objects:
            if obj:
                context.scene.collection.objects.link(obj)
                linked_items.append(obj.name)
        
        return linked_items

    def load_meshes(self, blend_path: str, context):
        """Load meshes from blend file"""
        linked_items = []
        
        with bpy.data.libraries.load(blend_path, link=True) as (data_from, data_to):
            if data_from.meshes:
                data_to.meshes = data_from.meshes

        for mesh in data_to.meshes:
            if mesh:
                linked_items.append(mesh.name)
        
        return linked_items

    def refresh_loaded_publishes(self, context):
        """Refresh the list of loaded publishes in the scene"""
        loaded_publishes = []
        
        # Check all linked data types
        linked_libraries = set()
        
        # Collections
        for collection in bpy.data.collections:
            if collection.library:
                linked_libraries.add(collection.library.filepath)
        
        # Materials  
        for material in bpy.data.materials:
            if material.library:
                linked_libraries.add(material.library.filepath)
        
        # Objects
        for obj in bpy.data.objects:
            if obj.library:
                linked_libraries.add(obj.library.filepath)
        
        # Meshes
        for mesh in bpy.data.meshes:
            if mesh.library:
                linked_libraries.add(mesh.library.filepath)
        
        # Get display info from database for each library
        for library_path in linked_libraries:
            display_name = self.get_display_name_from_db(library_path)
            
            loaded_publishes.append({
                'library_path': library_path,
                'display_name': display_name
            })
        
        # Store in scene for display
        context.scene.woody_loaded_publishes_count = len(loaded_publishes)
        
        # Create formatted display strings for UI
        display_strings = [pub['display_name'] for pub in loaded_publishes]
        context.scene.woody_loaded_publishes_display = "\n".join(display_strings) if display_strings else "No published assets loaded"
    
    def get_display_name_from_db(self, library_path: str):
        """Get display name from database instead of parsing filename"""
        try:
            client, db, error = get_database_connection()
            if error or client is None or db is None:
                # Fallback to filename if DB is unavailable
                return bpy.path.basename(library_path)

            # Search through all publish documents
            for publish_doc in db["publishes"].find():
                published_versions = publish_doc.get("published_versions", {})
                
                # Check each version to see if it matches our library path
                for version, version_info in published_versions.items():
                    if version_info.get("published_path") == library_path:
                        # Found a match! Build display name
                        publish_type = publish_doc.get("publish_type", "Unknown")
                        custom_name = publish_doc.get("custom_name", "Unknown")
                        
                        client.close()
                        return f"{publish_type.title()} - {custom_name} - {version}"
            
            client.close()
            # If not found in DB, fallback to filename
            return bpy.path.basename(library_path)
            
        except Exception as e:
            print(f"Error getting display name from DB: {e}")
            # Fallback to filename if error
            return bpy.path.basename(library_path)


class WOODY_OT_refresh_loaded_publishes(bpy.types.Operator):
    bl_idname = "woody.refresh_loaded_publishes"
    bl_label = "Refresh Loaded Publishes"
    bl_description = "Refresh the list of loaded published assets"

    def execute(self, context):
        # Duplicate the refresh logic here to avoid instantiation issues
        loaded_publishes = []
        
        # Check all linked data types
        linked_libraries = set()
        
        # Collections
        for collection in bpy.data.collections:
            if collection.library:
                linked_libraries.add(collection.library.filepath)
        
        # Materials  
        for material in bpy.data.materials:
            if material.library:
                linked_libraries.add(material.library.filepath)
        
        # Objects
        for obj in bpy.data.objects:
            if obj.library:
                linked_libraries.add(obj.library.filepath)
        
        # Meshes
        for mesh in bpy.data.meshes:
            if mesh.library:
                linked_libraries.add(mesh.library.filepath)
        
        # Get display info from database for each library
        for library_path in linked_libraries:
            display_name = self.get_display_name_from_db(library_path)
            
            loaded_publishes.append({
                'library_path': library_path,
                'display_name': display_name
            })
        
        # Store in scene for display
        context.scene.woody_loaded_publishes_count = len(loaded_publishes)
        
        # Create formatted display strings for UI
        display_strings = [pub['display_name'] for pub in loaded_publishes]
        context.scene.woody_loaded_publishes_display = "\n".join(display_strings) if display_strings else "No published assets loaded"
        
        loaded_count = len(loaded_publishes)
        if loaded_count > 0:
            self.report({'INFO'}, f"Refreshed: Found {loaded_count} loaded publishes")
        else:
            self.report({'INFO'}, "No linked publishes found in scene")
        
        return {'FINISHED'}
    
    def get_display_name_from_db(self, library_path: str):
        """Get display name from database instead of parsing filename"""
        try:
            client, db, error = get_database_connection()
            if error or client is None or db is None:
                # Fallback to filename if DB is unavailable
                return bpy.path.basename(library_path)

            # Search through all publish documents
            for publish_doc in db["publishes"].find():
                published_versions = publish_doc.get("published_versions", {})
                
                # Check each version to see if it matches our library path
                for version, version_info in published_versions.items():
                    if version_info.get("published_path") == library_path:
                        # Found a match! Build display name
                        publish_type = publish_doc.get("publish_type", "Unknown")
                        custom_name = publish_doc.get("custom_name", "Unknown")
                        
                        client.close()
                        return f"{publish_type.title()} - {custom_name} - {version}"
            
            client.close()
            # If not found in DB, fallback to filename
            return bpy.path.basename(library_path)
            
        except Exception as e:
            print(f"Error getting display name from DB: {e}")
            # Fallback to filename if error
            return bpy.path.basename(library_path)


# Scene properties for storing data
def register_properties():
    bpy.types.Scene.woody_publish_id = bpy.props.StringProperty(
        name="Publish ID",
        description="ID of the published asset to load",
        default=""
    )
    
    bpy.types.Scene.woody_publish_version = bpy.props.StringProperty(
        name="Version",
        description="Version of the published asset to load (latest, v001, v002, etc.)",
        default="latest"
    )
    
    bpy.types.Scene.woody_loaded_publishes_count = bpy.props.IntProperty(
        name="Loaded Publishes Count",
        description="Number of loaded published assets in scene",
        default=0
    )
    
    bpy.types.Scene.woody_loaded_publishes_display = bpy.props.StringProperty(
        name="Loaded Publishes Display",
        description="Formatted display of loaded published assets",
        default="No published assets loaded"
    )

def unregister_properties():
    del bpy.types.Scene.woody_publish_id
    del bpy.types.Scene.woody_publish_version
    del bpy.types.Scene.woody_loaded_publishes_count
    del bpy.types.Scene.woody_loaded_publishes_display