from pathlib import Path
import json

filepath  = Path("prefs") / "prefs.json"
filepath.parent.mkdir(parents=True, exist_ok=True)

def save_preferences_json(projectName, projectDirectory, mongoDBAddress, blenderExecutable):
    
    preferences = {
        "projectName": projectName,
        "projectDirectory": projectDirectory,
        "mongoDBAddress": mongoDBAddress,
        "blenderExecutable": blenderExecutable
    }

    with filepath.open("w", encoding="utf-8") as f:
        json.dump(preferences, f, indent=4, ensure_ascii=False)
        
def load_preferences_json():

    if not filepath.exists():
        print(f"No preferences file found at {filepath}")
        return None
    
    with filepath.open("r", encoding="utf-8") as f:
        preferances = json.load(f)
        
    return preferances
    