from ..utils import load_preferences_json
 
from pathlib import Path

class WoodyInstance():
    def __init__(self):
        
        prefs = load_preferences_json() or {}
        
        self.projectName = prefs.get("projectName")
        self.projectDirectory = Path(prefs.get("projectDirectory"))
        self.mongoDBAddress = prefs.get("mongoDBAddress")
        self.blenderExecutable = prefs.get("blenderExecutable")
