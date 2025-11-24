import bpy

def create_cube():
    bpy.ops.mesh.primitive_cube_add(
        size=2.0, 
        location=(0.0, 0.0, 0.0), 
        rotation=(0.0, 0.0, 0.0), 
        scale=(1.0, 1.0, 1.0)
    )
    
    obj = bpy.context.view_layer.objects.active
    
    return {"name": obj.name, "type": obj.type}