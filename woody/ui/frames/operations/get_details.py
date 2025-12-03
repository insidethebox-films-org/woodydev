from ... import style
from ....tool.woody_id import get_browser_selection_id
from ....utils.format_date import format_date
from ....tool.memory_store import store
from ....objects import Database

import customtkinter as ctk
import asyncio
import threading

#=========================
# DB Operations
#=========================
    
async def get_asset_details_async():
    
    db = Database()
    data = store.get_namespace("browser_selection")
    root = data.get("root")
    id = get_browser_selection_id(element_id=True)
    
    if root == "Assets":
        collection_name = "assets"
    else:
        collection_name = "shots"
    
    docs = await db.get_doc(collection_name, {"id": id})
    
    return docs

def get_asset_details(callback):

    def run():
        docs = asyncio.run(get_asset_details_async())
        callback(docs)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    
async def get_render_settings_async():
    
    db = Database()
    docs = await db.get_docs("settings", {"render_settings": True})
    
    return docs

def get_render_settings(callback):

    def run():
        docs = asyncio.run(get_render_settings_async())
        callback(docs)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()

async def update_asset_details_async(updates):
    db = Database()
    data = store.get_namespace("browser_selection")
    root = data.get("root")
    id = get_browser_selection_id(element_id=True)
    
    if root == "Assets":
        collection_name = "assets"
    else:
        collection_name = "shots"
    
    current_doc = await db.get_doc(collection_name, {"id": id})
    
    set_updates = {}
    for key, value in updates.items():
        if key in current_doc:
            set_updates[key] = value
        else:
            for parent_key, parent_value in current_doc.items():
                if isinstance(parent_value, dict) and key in parent_value:
                    set_updates[f"{parent_key}.{key}"] = value
                    break
    
    result = await db.update_document(
        collection_name,
        {"id": id},
        {"$set": set_updates}
    )
    
    return result

def update_asset_details(updates, callback):

    def run():
        result = asyncio.run(update_asset_details_async(updates))
        callback(result)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()

async def update_render_settings_async(updates, render_type):
    db = Database()
    
    # Get the specific document by type
    current_doc = await db.get_doc("settings", {"type": render_type, "render_settings": True})
    
    if not current_doc:
        raise Exception(f"No render settings found for type: {render_type}")
    
    # Build $set updates with nested paths
    set_updates = {}
    for key, value in updates.items():
        # Check if it's a nested key (contains a dot)
        if "." in key:
            # It's already in dot notation from create_editable_field
            set_updates[key] = value
        elif key in current_doc:
            set_updates[key] = value
        else:
            # Check nested dicts for the key
            for parent_key, parent_value in current_doc.items():
                if isinstance(parent_value, dict) and key in parent_value:
                    set_updates[f"{parent_key}.{key}"] = value
                    break
    
    result = await db.update_document(
        "settings",
        {"type": render_type, "render_settings": True},
        {"$set": set_updates}
    )
    
    return result

def update_render_settings(updates, render_type, callback):

    def run():
        result = asyncio.run(update_render_settings_async(updates, render_type))
        callback(result)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    
#=========================
# UI Helpers
#=========================
    
def make_label_text(key: str) -> str:
    return f"{key.replace('_', ' ').title()}:"

def create_readonly_field(parent, row, key, value):
    """
    Create a single readonly field row.
    
    Args:
        parent: Parent frame to add to
        row: Grid row position
        key: Field key (used for label)
        value: Field value to display
    """
    frame = ctk.CTkFrame(
        parent,
        corner_radius=5,
        fg_color="#252525",
        height=40,
    )
    frame.grid(row=row, pady=(0, 3), sticky="ew")
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_propagate(False)

    label = ctk.CTkLabel(
        frame,
        text=make_label_text(key),
        width=120,
        anchor="w",
        **style.BODY_LABEL,
    )
    label.grid(row=0, column=0, padx=(12, 5), sticky="w")

    if isinstance(value, dict) and "$date" in value:
        value = value["$date"]

    display_value = format_date(key, value)

    entry = ctk.CTkEntry(
        frame,
        placeholder_text=display_value if display_value else "None",
        fg_color="#1F1F1F",
        border_width=0,
    )
    if display_value:
        entry.insert(0, display_value)
    entry.grid(row=0, column=1, padx=(5, 12), sticky="ew")
    entry.configure(state="readonly")

def create_editable_field(parent, row, label_text, field_path, value, value_type=str):
    """
    Create an editable field row with Edit/Lock button.
    
    Args:
        parent: Parent frame to add to
        row: Grid row position
        label_text: Display label text
        field_path: MongoDB field path for updates
        value: Initial value
        value_type: Type to cast value to (int, str, float, etc.)
        
    Returns:
        dict: {"entry": entry_widget, "type": value_type, "path": field_path}
    """
    frame = ctk.CTkFrame(
        parent,
        corner_radius=5,
        fg_color="#252525",
        height=40,
    )
    frame.grid(row=row, pady=(0, 3), sticky="ew")
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, minsize=60)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_propagate(False)

    label = ctk.CTkLabel(
        frame,
        text=label_text,
        width=120,
        anchor="w",
        **style.BODY_LABEL,
    )
    label.grid(row=0, column=0, padx=(12, 5), sticky="w")

    entry = ctk.CTkEntry(
        frame,
        fg_color="#1F1F1F",
        border_width=0,
    )
    if value not in (None, ""):
        entry.insert(0, str(value))
    entry.grid(row=0, column=1, padx=(5, 4), sticky="ew")
    entry.configure(state="readonly")

    def toggle_edit():
        if entry.cget("state") == "readonly":
            entry.configure(state="normal")
            button.configure(text="Lock")
            button.configure(**style.WARNING_BUTTON_STYLE)
        else:
            entry.configure(state="readonly")
            button.configure(text="Edit")
            button.configure(**style.BUTTON_STYLE)

    button = ctk.CTkButton(
        frame,
        text="Edit",
        width=50,
        command=toggle_edit,
        **style.BUTTON_STYLE,
    )
    button.grid(row=0, column=2, padx=(0, 12), sticky="e")

    return {
        "entry": entry,
        "type": value_type,
        "path": field_path
    }
    
def get_editable_values(entries):
    values = {}
    for field_path, entry_data in entries:
        entry_widget = entry_data["entry"]
        field_type = entry_data["type"]
        
        raw_value = entry_widget.get()
        
        try:
            if field_type == int:
                values[field_path] = int(raw_value)
            elif field_type == float:
                values[field_path] = float(raw_value)
            else:
                values[field_path] = raw_value
        except (ValueError, TypeError):
            print(f"Failed to convert {field_path}: {raw_value}")
            values[field_path] = raw_value  # Store raw value as fallback
    
    return values