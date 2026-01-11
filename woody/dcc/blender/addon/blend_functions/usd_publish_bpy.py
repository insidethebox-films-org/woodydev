import bpy
import os

try:
    from pxr import Usd, UsdGeom, UsdShade, Sdf, Kind
except ImportError:
    if hasattr(bpy.utils, "expose_bundled_modules"):
        bpy.utils.expose_bundled_modules()
    from pxr import Usd, UsdGeom, UsdShade, Sdf, Kind

def export_usd(filepath, selected_only=True):
    bpy.ops.wm.usd_export(
        filepath=filepath,
        selected_objects_only=selected_only,
        export_meshes=True,
        export_uvmaps=True,
        export_materials=False,
        export_textures=False,
        evaluation_mode='RENDER'
    )
    
def get_collection_hierarchy(bl_obj, parent_map):
    hierarchy = []
    if bl_obj.users_collection:
        curr = bl_obj.users_collection[0]
        while curr and curr.name != "Scene Collection":
            clean_col_name = curr.name.replace(".", "_").replace(" ", "_")
            hierarchy.insert(0, f"{clean_col_name}_grp")
            curr = parent_map.get(curr)
    return hierarchy

def rebuild_usd_stage(source_path, asset_name):
    source_stage = Usd.Stage.Open(source_path)
    clean_path = source_path.replace(".usd", "_clean.usd")
    clean_stage = Usd.Stage.CreateNew(clean_path)
    
    UsdGeom.SetStageUpAxis(clean_stage, UsdGeom.Tokens.z)
    
    root_path = f"/{asset_name}"
    geo_path = f"{root_path}/geo"
    mtl_path = f"{root_path}/mtl"
    
    root_xform = UsdGeom.Xform.Define(clean_stage, root_path)
    root_xform.AddRotateXOp().Set(-90)
    
    UsdGeom.Scope.Define(clean_stage, geo_path)
    UsdGeom.Scope.Define(clean_stage, mtl_path)
    
    root_prim = root_xform.GetPrim()
    Usd.ModelAPI(root_prim).SetKind(Kind.Tokens.component)

    parent_map = {}
    for col in bpy.data.collections:
        for child in col.children:
            parent_map[child] = col

    bl_map = {obj.name.replace(".", "_").replace(" ", "_"): obj for obj in bpy.data.objects}

    for prim in source_stage.Traverse():
        if prim.IsA(UsdGeom.Xform):
            usd_name = prim.GetName()
            bl_obj = bl_map.get(usd_name)
            
            if bl_obj and bl_obj.type == 'MESH':
                hierarchy = get_collection_hierarchy(bl_obj, parent_map)
                col_path = "/".join(hierarchy) if hierarchy else "scene_layout_grp"
                target_path = Sdf.Path(f"{geo_path}/{col_path}/{usd_name}")
                
                current_parent = geo_path
                for step in hierarchy:
                    current_parent += f"/{step}"
                    col_prim = UsdGeom.Xform.Define(clean_stage, current_parent).GetPrim()
                    Usd.ModelAPI(col_prim).SetKind(Kind.Tokens.subcomponent)

                Sdf.CopySpec(source_stage.GetRootLayer(), prim.GetPath(), 
                             clean_stage.GetRootLayer(), target_path)
                
                leaf_prim = clean_stage.GetPrimAtPath(target_path)
                Usd.ModelAPI(leaf_prim).SetKind(Kind.Tokens.subcomponent)

    clean_stage.GetRootLayer().Save()
    del source_stage
    del clean_stage
    os.replace(clean_path, source_path)

import tempfile
import shutil

def usd_publish(base_path, asset_name, publish_name=None):
    if not bpy.context.selected_objects:
        raise ValueError("No objects selected")
    
    if hasattr(base_path, '__fspath__'):
        base_path = str(base_path)
    
    publish_path = os.path.join(base_path, "publish")
    publish_file_name = f"{publish_name}_latest"
    
    if not publish_file_name:
        name = bpy.path.display_name_from_filepath(bpy.data.filepath)
        publish_file_name = name if name and name != "Untitled" else "asset"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        local_filepath = os.path.join(tmpdir, f"{asset_name}_{publish_name}_latest.usd")
        os.makedirs(publish_path, exist_ok=True)
        export_usd(local_filepath)
        rebuild_usd_stage(local_filepath, asset_name)
        
        network_filepath = os.path.join(publish_path, f"{asset_name}_{publish_name}_latest.usd")
        shutil.copy2(local_filepath, network_filepath)
    
    return network_filepath