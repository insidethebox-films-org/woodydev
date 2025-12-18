from .. import style
from .operations.get_details import (
    get_asset_details,
    create_readonly_field,
    create_editable_field,
    get_editable_values,
    update_asset_details,
    update_render_settings,
    get_render_settings,
    make_label_text
)

import customtkinter as ctk


class AssetDetailsFrame: 
    def __init__(self, parent):
        self.parent = parent
        self.browser_selection = None
        
        self._current_doc = None
        self._render_settings_docs = None
        self._editable_entries = {}
        
        self.create_frame()
        self.create_widgets()
            
    def create_frame(self):
        self.frame = ctk.CTkFrame(
            self.parent,
            corner_radius=8,        
            border_width=2,          
            border_color="#5a5a5a",
        )
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        
    def create_asset_details(self, docs):
        """Build details UI from document one field at a time."""
        if not docs:
            self._show_no_data_message()
            return
        
        self._current_doc = docs
        self._editable_entries = {}
        row = 0
        
        readonly_fields = ["id", "parent_id", "sequence", "name"]
        for field in readonly_fields:
            if field in docs:
                create_readonly_field(self.asset_details_frame, row, field, docs[field])
                row += 1
        
        fr = docs.get("frame_range", {})
        if "start_frame" in fr:
            entry_data = create_editable_field(
                self.asset_details_frame,
                row,
                "Start Frame:",
                "start_frame",
                fr["start_frame"],
                int
            )
            self._editable_entries["start_frame"] = entry_data
            row += 1
            
        if "end_frame" in fr:
            entry_data = create_editable_field(
                self.asset_details_frame,
                row,
                "End Frame:",
                "end_frame",
                fr["end_frame"],
                int
            )
            self._editable_entries["end_frame"] = entry_data
            row += 1
        
        timestamp_fields = ["created_time", "modified_time"]
        for field in timestamp_fields:
            if field in docs:
                create_readonly_field(self.asset_details_frame, row, field, docs[field])
                row += 1

    def create_render_settings(self, docs):
        """Build render settings UI with type selector."""
        if not docs:
            self._show_no_data_message()
            return
        
        self._render_settings_docs = docs
        self._editable_entries = {}
        
        self._create_render_settings_type_selector()
        
        self._render_render_settings_fields()
    
    def _create_render_settings_type_selector(self):
        type_frame = ctk.CTkFrame(
            self.asset_details_frame,
            corner_radius=5,
            fg_color="#252525",
            height=40,
        )
        type_frame.grid(row=0, column=0, pady=(0, 3), sticky="ew")
        type_frame.grid_rowconfigure(0, weight=1)
        type_frame.grid_propagate(False)
        
        self.render_settings_type_combo = ctk.CTkComboBox(
            type_frame,
            **style.COMBO_BOX_STYLE,
            values=["Global", "Blender"],
            state="readonly",
            command=self._on_render_settings_type_change
        )
        self.render_settings_type_combo.grid(row=0, column=0, padx=8, pady=5)
        self.render_settings_type_combo.set("Global")
    
    def _on_render_settings_type_change(self, selected_type):
        """Handle render settings type change."""
        children = list(self.asset_details_frame.winfo_children())
        for widget in children[1:]:
            try:
                if widget.winfo_exists():
                    widget.destroy()
            except Exception:
                pass
        
        self._render_render_settings_fields()
    
    def _render_render_settings_fields(self):
        if not self._render_settings_docs:
            return
        
        selected_type = self.render_settings_type_combo.get().lower()
        render_settings_doc = next(
            (item for item in self._render_settings_docs if item.get("type") == selected_type),
            None
        )
        
        if not render_settings_doc:
            self._show_no_data_message(row=1)
            return
        
        self._current_doc = render_settings_doc
        self._editable_entries = {}
        row = 1
        
        skip_fields = ["_id", "type", "id", "render_settings"]
        
        for key, value in render_settings_doc.items():
            if key in skip_fields or key.startswith("_"):
                continue
            
            if isinstance(value, dict):
                for nested_key, nested_value in value.items():
                    value_type = type(nested_value) if nested_value is not None else str
                    label = f"{make_label_text(key).rstrip(':')} - {make_label_text(nested_key)}"
                    
                    entry_data = create_editable_field(
                        self.asset_details_frame,
                        row,
                        label,
                        f"{key}.{nested_key}",
                        nested_value,
                        value_type
                    )
                    self._editable_entries[f"{key}.{nested_key}"] = entry_data
                    row += 1
            else:
                value_type = type(value) if value is not None else str
                
                entry_data = create_editable_field(
                    self.asset_details_frame,
                    row,
                    make_label_text(key),
                    key,
                    value,
                    value_type
                )
                self._editable_entries[key] = entry_data
                row += 1
    
    def _show_no_data_message(self, row=0):
        no_data_label = ctk.CTkLabel(
            self.asset_details_frame,
            text="No details available",
            **style.BODY_LABEL
        )
        no_data_label.grid(row=row, column=0, padx=12, pady=12)
    
    def update_mode_items(self, selected):
        if selected:
            self.browser_selection = selected
            
            if hasattr(self, 'mode_combo_box') and self.mode_combo_box.get() == "Element":
                def populate_details(docs):
                    self.clear_mode_items()
                    self.frame.after(0, self.create_asset_details, docs)
                get_asset_details(callback=populate_details)
                
            elif hasattr(self, 'mode_combo_box') and self.mode_combo_box.get() == "Render Settings":
                def populate_details(docs):
                    self.clear_mode_items()
                    self.frame.after(0, self.create_render_settings, docs)
                get_render_settings(callback=populate_details)
        else:
            self.browser_selection = None
            self.frame.after(0, self.clear_mode_items)
    
    def clear_mode_items(self):
        """Clear all detail widgets."""
        self._editable_entries = {}
        self._current_doc = None
        self._render_settings_docs = None
        
        def destroy_widgets():
            for widget in list(self.asset_details_frame.winfo_children()):
                try:
                    if widget.winfo_exists():
                        widget.destroy()
                except Exception:
                    pass
                
        self.frame.after(0, destroy_widgets)

    def on_update_details(self):
        updates = get_editable_values(self._editable_entries.items())
        
        def on_complete(result):
            print("Update complete:", result)
            if self.mode_combo_box.get() == "Element" and self.browser_selection:
                self.update_mode_items(self.browser_selection)
                
        if not hasattr(self, 'mode_combo_box'): return
        
        if self.mode_combo_box.get() == "Render Settings":
            render_type = self.render_settings_type_combo.get().lower()
            update_render_settings(updates, render_type, on_complete)
        else:
            update_asset_details(updates, on_complete)

    def create_widgets(self):
        """Create the main UI widgets."""
        # Header
        self.header_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=40
        )
        self.header_frame.grid(row=0, pady=(7, 3), padx=7, sticky="ew")
        self.header_frame.grid_propagate(False)
        
        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text="Details:",
            **style.HEADER_LABEL
        )
        self.header_label.grid(row=0, pady=7, padx=12, sticky="w")
        
        # Mode selector
        self.mode_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=40,
        )
        self.mode_frame.grid(row=1, padx=7, pady=(0, 3), sticky="ew")
        self.mode_frame.grid_propagate(False)
        self.mode_frame.grid_rowconfigure(0, weight=1)
        
        self.mode_combo_box = ctk.CTkComboBox(
            self.mode_frame,
            **style.COMBO_BOX_STYLE,
            state="readonly",
            values=["Element", "Render Settings"],
            command=self.update_mode_items
        )
        self.mode_combo_box.grid(row=0, padx=8, pady=(7, 5))
        self.mode_combo_box.set("Element")

        # Scrollable details frame
        self.asset_details_frame = ctk.CTkScrollableFrame(
            self.frame,
            corner_radius=5,
            fg_color="transparent",      
            border_width=2,
        )
        self.asset_details_frame.grid(row=2, padx=7, pady=(3, 5), sticky="nsew")
        self.asset_details_frame.grid_columnconfigure(0, weight=1)
        self.asset_details_frame._scrollbar.grid(padx=(0, 3), pady=3)
        
        # Save button
        self.update_button = ctk.CTkButton(
            self.frame,
            text="Save Changes",
            **style.DCC_BUTTON_STYLE,
            command=self.on_update_details,
        )
        self.update_button.grid(row=3, padx=7, pady=(0, 7), sticky="ew")