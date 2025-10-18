# woody_blender_addon/operators/publish.py
import re
import bpy
from pathlib import Path
from datetime import datetime, timezone

from ..utils.get_db_connection import get_database_connection

class WOODY_OT_publish(bpy.types.Operator):
    bl_idname = "woody.publish"
    bl_label = "Publish Asset"
    bl_description = "Publish selected collections as a reusable asset"

    # Properties for the publish dialog
    asset_name: bpy.props.StringProperty(
        name="Asset Name",
        description="Name for the published asset",
        default=""
    )#type: ignore
    
    collection_name: bpy.props.EnumProperty(
        name="Collection to Publish",
        description="Select which collection to publish",
        items=lambda self, context: [(col.name, col.name, "") for col in bpy.data.collections if col.name != "Collection"]
    )#type: ignore

    def invoke(self, context, event):
        # Auto-populate asset name from current blend file
        current_file = Path(bpy.data.filepath)
        if current_file.name:
            # Extract asset/shot name from path structure
            # Path structure: .../assets/CnB/cok/blendfile.blend
            # We want the folder name before the blend file (cok in this case)
            asset_name = current_file.parent.name  # Gets "cok" from the path
            self.asset_name = f"{asset_name}_published_latest"
        
        # Show dialog with properties
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "asset_name")
        layout.prop(self, "collection_name")

    def execute(self, context):
        try:
            # Get current file info to determine publish location
            current_path = Path(bpy.data.filepath)
            if not current_path.exists():
                self.report({'ERROR'}, "Save your blend file first!")
                return {'CANCELLED'}

            # Save the current file before publishing
            print("Saving current file before publishing...")
            bpy.ops.wm.save_mainfile()
            self.report({'INFO'}, "File saved before publishing")

            # Create publish directory structure
            publish_dir = current_path.parent / "_publish"
            publish_dir.mkdir(exist_ok=True)
            
            # Create the published blend file
            published_file = publish_dir / f"{self.asset_name}.blend"
            
            success = self.create_published_asset(self.collection_name, published_file)
            
            if success:
                # Update database with publish info
                self.update_publish_database(str(published_file))
                
                self.report({'INFO'}, f"Published: {self.asset_name}")
                return {'FINISHED'}
            else:
                self.report({'ERROR'}, "Failed to create published asset")
                return {'CANCELLED'}
                
        except Exception as e:
            self.report({'ERROR'}, f"Publish failed: {str(e)}")
            return {'CANCELLED'}

    def create_published_asset(self, collection_name: str, output_path: Path) -> bool:
        """Create a new blend file with just the specified collection"""
        try:
            collection = bpy.data.collections.get(collection_name)
            if not collection:
                print(f"❌ Collection '{collection_name}' not found")
                return False

            # Recursively gather all collections
            def gather_collections(col, seen=None):
                if seen is None:
                    seen = set()
                seen.add(col)
                for child in col.children:
                    if child not in seen:
                        gather_collections(child, seen)
                return seen

            collections = gather_collections(collection)
            
            # Gather all objects in all collections
            objects = set()
            for col in collections:
                for obj in col.objects:
                    objects.add(obj)

            # Gather meshes and materials used by objects
            meshes = {obj.data for obj in objects if obj.type == 'MESH' and obj.data}
            materials = {mat for obj in objects if obj.type == 'MESH' for mat in obj.data.materials if mat}

            # Include additional data that might be needed
            textures = set()
            node_groups = set()
            for mat in materials:
                if mat.node_tree:
                    for node in mat.node_tree.nodes:
                        if node.type == 'TEX_IMAGE' and node.image:
                            textures.add(node.image)
                        elif hasattr(node, 'node_tree') and node.node_tree:
                            node_groups.add(node.node_tree)

            # Combine all datablocks
            datablocks = collections | objects | meshes | materials | textures | node_groups

            # Write the blend file
            bpy.data.libraries.write(
                str(output_path),
                datablocks,
                fake_user=True,
                compress=True
            )
            
            print(f"✅ Published: '{collection_name}' with {len(objects)} objects, {len(meshes)} meshes, {len(materials)} materials")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create published asset: {e}")
            return False

    def update_publish_database(self, published_path: str):
        """Update database with publish information"""
        try:
            client, db, error = get_database_connection()
            if error or client is None or db is None:
                print(f"Could not update database: {error}")
                return

            # Get current blend file info for context
            current_path = Path(bpy.data.filepath)
            
            # Create a publish record
            publish_record = {
                "asset_name": self.asset_name,
                "collection_name": self.collection_name,
                "published_path": published_path,
                "source_file": str(current_path),
                "created_time": datetime.now(timezone.utc),
                "version": 1  # Could be incremented for republishing
            }

            # Insert into publishes collection
            db["publishes"].insert_one(publish_record)
            print(f"✅ Publish record added to database")
            
            client.close()

        except Exception as e:
            print(f"Failed to update database: {e}")