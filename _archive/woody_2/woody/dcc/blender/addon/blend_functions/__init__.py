from .save_bpy import save
from .set_frame_range_bpy import set_frame_range
from .set_render_settings_bpy import set_render_settings
from .usd_publish_bpy import usd_publish

OPERATIONS = {
    "save": save_bpy,
    "set_frame_range": set_frame_range_bpy,
    "set_render_settings": set_render_settings_bpy,
    "usd_publish": usd_publish_bpy,
}