from ..objects.database import Database
import threading

from ..database.dcc.publish_db import publish_db
from ..database.dcc.render_db import render_db
from ..database.dcc.get_frame_range import get_frame_range
from ..database.dcc.get_render_settings import get_render_settings

class DB_Operators(Database):
    
    def publish(self, name, publish_type, dcc, woody_id, file_path):
        publish_db(name, publish_type, dcc, woody_id, file_path)
        
    def render(self, name, woody_id, file_path, comment):
        render_db(name, woody_id, file_path, comment)
    
    def get_frame_range(self, woody_id):
        result = [None, None]
        event = threading.Event() 
        
        def handle_callback(data):
            if data and isinstance(data, list) and len(data) == 2:
                result[0] = data[0]
                result[1] = data[1]
            
            event.set() 
        
        get_frame_range(handle_callback, woody_id)
        event.wait()
        
        return result
    
    def get_render_settings(self):
        result = {}
        event = threading.Event() 
        
        def handle_callback(data):
            if data and isinstance(data, dict):                
                result.update(data)
            event.set() 
        
        get_render_settings(handle_callback)
        event.wait()
        
        return result