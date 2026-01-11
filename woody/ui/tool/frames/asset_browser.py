from ... import style
from ..widgets import CTkListbox
from ....objects.memory_store import store
from ....database.tool.get_asset_browser_docs import get_groups, get_elements

import customtkinter as ctk

class AssetBrowserFrame:
    def __init__(self, parent, status_bar):
        self.parent = parent
        self.status_bar = status_bar

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
        self.frame.grid_columnconfigure(1, weight=10)
        self.frame.grid_columnconfigure(2, weight=10)
        
        self.frame.grid_rowconfigure(0, weight=1)
        
    def on_root_selection(self, selected):
        store.set_value("browser_selection", "root", selected)
        store.set_value("browser_selection", "group", None)
        store.set_value("browser_selection", "element", None)
        
        self.group_list_box.delete(0, "END")
        self.element_list_box.delete(0, "END")
        
        if hasattr(self, "scenes_frame"):
            self.scenes_frame.clear_scenes()
        if hasattr(self, "publishes_frame"):
            self.publishes_frame.clear_scenes()
        if hasattr(self, "renders_frame"):
            self.renders_frame.clear_scenes()
        if hasattr(self, "asset_details_frame"):
            # Only clear if in Element mode
            if self.asset_details_frame.mode_combo_box.get() == "Element":
                self.asset_details_frame.clear_mode_items()
        
        def populate_groups(docs):
            names = [doc.get("name") for doc in docs if doc.get("name")]
            names.sort(key=str.lower)
            
            for name in names:
                self.group_list_box.insert("END", name)
            
        get_groups(callback=populate_groups)
        
    def on_group_selection(self, selected):
        store.set_value("browser_selection", "group", selected)
        store.set_value("browser_selection", "element", None)
        
        self.element_list_box.delete(0, "END")
        
        if hasattr(self, "scenes_frame"):
            self.scenes_frame.clear_scenes()
        if hasattr(self, "publishes_frame"):
            self.publishes_frame.clear_scenes()
        if hasattr(self, "renders_frame"):
            self.renders_frame.clear_scenes()
        if hasattr(self, "asset_details_frame"):
            # Only clear if in Element mode
            if self.asset_details_frame.mode_combo_box.get() == "Element":
                self.asset_details_frame.clear_mode_items()
        
        def populate_elements(docs):
            names = [doc.get("name") for doc in docs if doc.get("name")]
            names.sort(key=str.lower)
            
            for name in names:
                self.element_list_box.insert("END", name)
            
        get_elements(callback=populate_elements)
        
    def on_element_selection(self, selected):
        store.set_value("browser_selection", "element", selected)
        
        if hasattr(self, "scenes_frame"):
            if selected:
                self.scenes_frame.clear_scenes()
                self.scenes_frame.on_element_selected(selected)
            else:
                self.scenes_frame.clear_scenes()
                
        if hasattr(self, "publishes_frame"):
            if selected:
                self.publishes_frame.clear_scenes()
                self.publishes_frame.on_element_selected(selected)
            else:
                self.publishes_frame.clear_scenes()
                
        if hasattr(self, "renders_frame"):
            if selected:
                self.renders_frame.clear_scenes()
                self.renders_frame.on_element_selected(selected)
            else:
                self.publishes_frame.clear_scenes()
                
        if hasattr(self, "asset_details_frame"):
            if selected:
                if self.asset_details_frame.mode_combo_box.get() == "Element":
                    self.asset_details_frame.clear_mode_items()
                self.asset_details_frame.update_mode_items(selected)
            else:
                if self.asset_details_frame.mode_combo_box.get() == "Element":
                    self.asset_details_frame.clear_mode_items()
    
            
    def create_widgets(self):
        
        # Root list box
        self.root_list_box = CTkListbox(
            self.frame,
            **style.LIST_BOX_STYLE,
            
            command=self.on_root_selection
            )
        self.root_list_box.grid(row=0, column=0, sticky="nsew", pady=5, padx=(5,0))
        self.root_list_box.insert(0, "Assets") 
        self.root_list_box.insert("END", "Shots")
        
        # Group list box
        self.group_list_box = CTkListbox(
            self.frame,
            **style.LIST_BOX_STYLE,
            
            command=self.on_group_selection
        )
        self.group_list_box.grid(row=0, column=1, sticky="nsew", pady=5, padx=(2,0))
        
        # Element list box
        self.element_list_box = CTkListbox(
            self.frame,
            **style.LIST_BOX_STYLE,
            
            command=self.on_element_selection
        )
        self.element_list_box.grid(row=0, column=2, sticky="nsew", pady=5, padx=(2,5))
        