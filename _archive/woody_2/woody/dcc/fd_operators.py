from ..objects.directory import Directory

from ..directory.create_publish_fd import create_publish_fd
from ..directory.create_render_fd import create_render_fd

class FD_Operators(Directory):
    
    @staticmethod
    def create_publish_fd(woody_id):
        return create_publish_fd(woody_id)
    
    @staticmethod
    def create_render_fd(woody_id, render_name):
        return create_render_fd(woody_id, render_name)
    
    