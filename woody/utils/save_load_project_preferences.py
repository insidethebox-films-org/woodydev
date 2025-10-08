from pathlib import Path
import json

def save_project_preferences_json(project_name, blenderExecutable, projectDirectory):
    project_preferences_path = Path("prefs") / f"{project_name}_proj_prefs.json"
    project_preferences_path.parent.mkdir(parents=True, exist_ok=True)
    
    project_preferences = {
        "projectName": project_name,
        "blenderExecutable": blenderExecutable,
        "projectDirectory": projectDirectory
    }

    with project_preferences_path.open("w", encoding="utf-8") as f:
        json.dump(project_preferences, f, indent=4, ensure_ascii=False)
    
    return project_name  # Return project name for use in other functions
        
        
def load_recent_project_preferences_json():
    """Load project preferences from last saved project"""
    try:
        # Get most recent project preferences file
        prefs_dir = Path("prefs")
        if not prefs_dir.exists():
            return None
            
        pref_files = list(prefs_dir.glob("*_proj_prefs.json"))
        if not pref_files:
            return None
            
        # Get most recently modified file
        latest_pref = max(pref_files, key=lambda x: x.stat().st_mtime)
        
        with latest_pref.open("r", encoding="utf-8") as f:
            project_preferences = json.load(f)
            
        return project_preferences
        
    except Exception as e:
        print(f"Error loading project preferences: {e}")
        return None