from ..utils import load_settings_json, load_recent_project_preferences_json

from pathlib import Path

class WoodyInstance():
    def __init__(self):
        settings = load_settings_json() or {}
        project_preferences = load_recent_project_preferences_json() or {}
        
        self.projectName = project_preferences.get("projectName")
        self.mongoDBAddress = settings.get("mongoDBAddress", "mongodb://localhost:27017")
        self.blenderExecutable = project_preferences.get("blenderExecutable")
        
        project_dir = project_preferences.get("projectDirectory")
        self.projectDirectory = Path(project_dir) if project_dir else None