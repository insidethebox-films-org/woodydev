import bpy

class Properties(bpy.types.PropertyGroup):
    publish_name: bpy.props.StringProperty(
        name="Publish Name",
        description="Name for the publish",
        default=""
    ) # type: ignore
    
    publish_type: bpy.props.EnumProperty(
        name="Publish Type",
        description="Type of publish",
        items=[
            ('USD', '.usd', 'Export as USD'),
            ('BLEND', '.blend', 'Export as Blend'),
            ("OBJ", '.obj', 'Export as obj'),
            ("ABC", '.abc', 'Export as alembic')
        ],
        default='BLEND'
    ) # type: ignore