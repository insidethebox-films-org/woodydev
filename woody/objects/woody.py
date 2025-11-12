from ..utils import load_settings_json

class Woody():
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Woody, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        settings = load_settings_json() or {}
        
        self.projectName = settings.get("projectName")
        self.mongoDBAddress = settings.get("mongoDBAddress")
        self.blenderExecutable = settings.get("blenderExecutable")