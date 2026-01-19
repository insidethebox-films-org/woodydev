import bpy

def obj_publish(file_path):
    
    bpy.ops.wm.obj_export(
        'EXEC_DEFAULT',
        filepath=file_path,
        export_selected_objects=True,
        export_materials=False,
    )
    
def abc_publish(file_path):
    
    bpy.ops.wm.alembic_export(
        'EXEC_DEFAULT',
        filepath=file_path,
        selected=True,
    )