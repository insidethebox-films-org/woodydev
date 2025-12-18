from .. import style
from ..widgets import CTkListbox
from ...tool.memory_store import store
from .operations.get_scenes_docs import get_scenes, get_scene_versions
from .operations.utils import sort_versions
from ...tool.woody_id import get_browser_selection_id
from ..utils.load_icon import load_icon

from ...objects.dcc import DCC

import os
import customtkinter as ctk

class ScenesFrame:
    def __init__(self, parent):
        self.parent = parent
        self.create_frame()
        self.create_widgets()
        self.browser_selection = None
        
        self.open_scene_button.configure(state="disabled")
            
    def create_frame(self):
        self.frame = ctk.CTkFrame(
            self.parent,
            corner_radius=8,        
            border_width=2,          
            border_color="#5a5a5a",
            height=200
            )
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(3, weight=2)
        self.frame.grid_propagate(False)
        
    def clear_scenes(self):
        self.browser_selection = None
        self.scenes_list_box.delete(0, "END")
        self.scene_version_list_box.delete(0, "END")
        self.open_scene_button.configure(state="disabled")
        
    def on_element_selected(self, selected):
        self.open_scene_button.configure(state="disabled")
        
        if selected:
            self.browser_selection = selected
            
            self.scenes_list_box.delete(0, "END")
            
            def get_scenes_list(selected, docs):
                if self.browser_selection != selected:
                    return
                
                current_dir = os.path.dirname(os.path.abspath(__file__))
                icons_dir = os.path.join(current_dir, "..", "..", "icons", "scenes")
                
                items = [(doc.get("name"), doc.get("dcc", "unknown")) for doc in docs if doc.get("name")]
                items.sort(key=lambda x: x[0].lower())
                
                for name, dcc in items:
                    icon = None
                    try:
                        icon_path = os.path.join(icons_dir, f"{dcc.lower()}.png")
                        if os.path.exists(icon_path):
                            icon = load_icon(icon_path, 18)
                    except Exception as e:
                        print(f"Error loading icon for {dcc}: {e}")
                    
                    self.scenes_list_box.insert("END", name, icon=icon)
                
            def populate_scenes(docs):
                self.frame.after(0, get_scenes_list, selected, docs)
                    
            get_scenes(callback=populate_scenes)
    
    def on_scene_selected(self, selected):
        self.open_scene_button.configure(state="disabled")
        
        def get_versions_list(docs):
            
            self.scene_version_list_box.delete(0, "END")
            
            if not docs or not docs.get("files"):
                return
                
            versions = list(docs.get("files").values())
            sorted_versions = sorted(versions, key=sort_versions)

            for version in sorted_versions:
                self.scene_version_list_box.insert("END", version)
        
        def populate_versions(docs):
            self.frame.after(0, get_versions_list, docs)
        
        get_scene_versions(selected, callback=populate_versions)
        
    def on_version_selected(self, selected):
        if selected:
            self.open_scene_button.configure(state="normal")
        else:
            self.open_scene_button.configure(state="disabled")
            
    def on_open_scene_file(self):
        print("Opening scene file...")
        dcc = "blender"
        
        woody_id = get_browser_selection_id(element_id=True)
        
        data = store.get_namespace("browser_selection")
        root = data.get("root", "").lower()
        group = data.get("group", "")
        element = data.get("element", "")
        scene = f"{self.scenes_list_box.get()}_{self.scene_version_list_box.get()}"

        
        cls = DCC.registry.get(dcc.lower())
        if not cls:
            raise ValueError("Unknown DCC")
        cls().open_file(root, group, element, scene, woody_id)
        
        
    def create_widgets(self):
    
        # Header
        self.header_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=40
        )
        self.header_frame.grid(row=0, columnspan=2, pady=(7, 3), padx=7, sticky="ew")
        self.header_frame.grid_propagate(False)
        
        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text="Scenes:",
            **style.HEADER_LABEL
        )
        self.header_label.grid(row=0, pady=7, padx=12, sticky="w")
        
        # scenes listbox
        self.scenes_list_box = CTkListbox(
            self.frame,
            **style.LIST_BOX_STYLE,
            
            command=self.on_scene_selected
            )
        self.scenes_list_box.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(3,5), padx=5)
        
        # scene versions title
        self.scene_versions_title_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=30
        )
        self.scene_versions_title_frame.grid(row=2, padx=(7,3), pady=(0, 5), sticky="ew")
        self.scene_versions_title_frame.grid_propagate(False)
        
        self.scene_versions_title_label = ctk.CTkLabel(
            self.scene_versions_title_frame,
            text="Scene Versions:",
            **style.SUB_HEADER_LABEL
        )
        self.scene_versions_title_label.grid(row=0, padx=12, sticky="w")
        
        # scene options title
        self.scene_options_title_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=30
        )
        self.scene_options_title_frame.grid(row=2, column=1, padx=(0,7), pady=(0, 5), sticky="ew")
        self.scene_options_title_frame.grid_propagate(False)
        
        self.scene_options_title_label = ctk.CTkLabel(
            self.scene_options_title_frame,
            text="Scene Options:",
            **style.SUB_HEADER_LABEL
        )
        self.scene_options_title_label.grid(row=0, padx=12, sticky="w")
        
        # scene versions listbox
        self.scene_version_list_box = CTkListbox(
            self.frame,
            **style.LIST_BOX_STYLE,
            
            command=self.on_version_selected
            )
        self.scene_version_list_box.grid(row=3, column=0, sticky="nsew", pady=(0,5), padx=5)
        
        # Scene options frame
        self.scene_options_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            border_width=2,
            fg_color="transparent",
            height=30
        )
        self.scene_options_frame.grid(row=3, column=1, padx=(0,7), pady=(0, 5), sticky="nsew")
        self.scene_options_frame.grid_propagate(False)
        self.scene_options_frame.grid_columnconfigure(0, weight=1)
        
        # Open scene button
        self.open_scene_button = ctk.CTkButton(
            self.scene_options_frame,
            text="Open Scene",
            **style.BUTTON_STYLE,
            
            command=self.on_open_scene_file
        )
        self.open_scene_button.grid(row=0, padx=7, pady=8, sticky="ew")