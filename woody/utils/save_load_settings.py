from pathlib import Path
import json

settings_path  = Path("prefs") / "prefs.json"
settings_path.parent.mkdir(parents=True, exist_ok=True)

def save_settings_json(mongoDBAddress):
    
    settings = {
        "mongoDBAddress": mongoDBAddress,
    }

    with settings_path.open("w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)
        
def load_settings_json():

    if not settings_path.exists():
        print(f"No preferences file found at {settings_path}")
        return None
    
    with settings_path.open("r", encoding="utf-8") as f:
        settings = json.load(f)
        
    return settings
    