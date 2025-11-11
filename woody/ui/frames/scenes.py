from .. import style
from ..widgets import CTkListbox
from ...tool.memory_store import store
from .operations.get_blends_docs import get_blends, get_blend_versions
from .operations.utils import sort_versions
from ...plugins.blender.blender_instance import BlenderInstance

import re
import customtkinter as ctk

class ScenesFrame:
    def __init__(self, parent):
        self.parent = parent
        self.create_frame()
        self.create_widgets()
        self.browser_selection = None
        
        self.open_blend_button.configure(state="disabled")
            
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
        self.blends_list_box.delete(0, "END")
        self.blend_version_list_box.delete(0, "END")
        self.open_blend_button.configure(state="disabled")
        
    def on_element_selected(self, selected):
        self.open_blend_button.configure(state="disabled")
        
        if selected:
            self.browser_selection = selected
            
            self.blends_list_box.delete(0, "END")
            
            def get_blends_list(selected, docs):
                if self.browser_selection != selected:
                    return
                
                names = [doc.get("name") for doc in docs if doc.get("name")]
                names.sort(key=str.lower)
                
                for name in names:
                    self.blends_list_box.insert("END", name)
                
            def populate_blends(docs):
                self.frame.after(0, get_blends_list, selected, docs)
                    
            get_blends(callback=populate_blends)
    
    def on_blend_selected(self, selected):
        self.open_blend_button.configure(state="disabled")
        
        def get_versions_list(docs):
            
            self.blend_version_list_box.delete(0, "END")
            
            if not docs or not docs.get("blend_files"):
                return
                
            versions = list(docs.get("blend_files").values())
            sorted_versions = sorted(versions, key=sort_versions)

            for version in sorted_versions:
                self.blend_version_list_box.insert("END", version)
        
        def populate_versions(docs):
            self.frame.after(0, get_versions_list, docs)
        
        get_blend_versions(selected, callback=populate_versions)
        
    def on_version_selected(self, selected):
        if selected:
            self.open_blend_button.configure(state="normal")
        else:
            self.open_blend_button.configure(state="disabled")
            
    def on_open_blend_file(self):
        
        blender = BlenderInstance()
        
        data = store.get_namespace("browser_selection")
        root = data.get("root")
        group = data.get("group")
        element = data.get("element")
        blend = self.blends_list_box.get()
        version = self.blend_version_list_box.get()
        
        if not version == "latest":
            v = "v"
        else:
            v = ""
        
        blender.open_file(
            root,
            group, 
            element,
            f"{blend}_{v}{version}.blend",
        ) 
        
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
        
        # Blends listbox
        self.blends_list_box = CTkListbox(
            self.frame,
            **style.LIST_BOX_STYLE,
            
            command=self.on_blend_selected
            )
        self.blends_list_box.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(3,5), padx=5)
        
        # Blend versions title
        self.blend_versions_title_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=30
        )
        self.blend_versions_title_frame.grid(row=2, padx=(7,3), pady=(0, 5), sticky="ew")
        self.blend_versions_title_frame.grid_propagate(False)
        
        self.blend_versions_title_label = ctk.CTkLabel(
            self.blend_versions_title_frame,
            text="Scene Versions:",
            **style.SUB_HEADER_LABEL
        )
        self.blend_versions_title_label.grid(row=0, padx=12, sticky="w")
        
        # Blend options title
        self.blend_options_title_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=30
        )
        self.blend_options_title_frame.grid(row=2, column=1, padx=(0,7), pady=(0, 5), sticky="ew")
        self.blend_options_title_frame.grid_propagate(False)
        
        self.blend_options_title_label = ctk.CTkLabel(
            self.blend_options_title_frame,
            text="Scene Options:",
            **style.SUB_HEADER_LABEL
        )
        self.blend_options_title_label.grid(row=0, padx=12, sticky="w")
        
        # Blend versions listbox
        self.blend_version_list_box = CTkListbox(
            self.frame,
            **style.LIST_BOX_STYLE,
            
            command=self.on_version_selected
            )
        self.blend_version_list_box.grid(row=3, column=0, sticky="nsew", pady=(0,5), padx=5)
        
        # Scene options frame
        self.blend_options_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            border_width=2,
            fg_color="transparent",
            height=30
        )
        self.blend_options_frame.grid(row=3, column=1, padx=(0,7), pady=(0, 5), sticky="nsew")
        self.blend_options_frame.grid_propagate(False)
        self.blend_options_frame.grid_columnconfigure(0, weight=1)
        
        # Open scene button
        self.open_blend_button = ctk.CTkButton(
            self.blend_options_frame,
            text="Open Scene",
            **style.BUTTON_STYLE,
            
            command=self.on_open_blend_file
        )
        self.open_blend_button.grid(row=0, padx=7, pady=8, sticky="ew")