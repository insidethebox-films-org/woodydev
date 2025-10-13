from ..utils import load_settings_json

class WoodyInstance():
    def __init__(self):
        settings = load_settings_json() or {}
        
        self.projectName = settings.get("projectName")
        self.mongoDBAddress = settings.get("mongoDBAddress")
        self.blenderExecutable = settings.get("blenderExecutable")
