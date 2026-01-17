from ... import style
from ..widgets import CTkListbox
from ....utils.sort_versions import sort_versions
from ....utils.copy_to_clipboard import copy_to_clipboard
from ....database.tool.get_publishes_docs import get_publishes, get_publishes_versions
from ..utils.load_icon import load_icon

from ....dcc.blender.blender import Blender
from ....dcc.houdini.houdini import Houdini

import os
import customtkinter as ctk

class PublishesFrame:
    def __init__(self, parent, status_bar):
        self.parent = parent
        self.status_bar = status_bar
        self.create_frame()
        self.create_widgets()
        self.browser_selection = None
        self.publish_doc = None
        self.blender = Blender()
        self.houdini = Houdini()
        
        self.get_publish_button.configure(state="disabled")
            
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
        self.publishes_list_box.delete(0, "END")
        self.publish_version_list_box.delete(0, "END")
        self.get_publish_button.configure(state="disabled")
        
    def on_element_selected(self, selected):
        self.get_publish_button.configure(state="disabled")
        
        if selected:
            self.browser_selection = selected
            
            self.publishes_list_box.delete(0, "END")
            
            def get_publishes_list(selected, docs):
                if self.browser_selection != selected:
                    return
                
                current_dir = os.path.dirname(os.path.abspath(__file__))
                icons_dir = os.path.join(current_dir, "..", "..", "..", "icons", "publishes")
                
                items = [(doc.get("name"), doc.get("type", "unknown")) for doc in docs if doc.get("name")]
                items.sort(key=lambda x: x[0].lower())
                
                for name, dcc in items:
                    icon = None
                    try:
                        icon_path = os.path.join(icons_dir, f"{dcc.lower()}.png")
                        if os.path.exists(icon_path):
                            icon = load_icon(icon_path, 18)
                    except Exception as e:
                        print(f"Error loading icon for {dcc}: {e}")
                    
                    self.publishes_list_box.insert("END", name, icon=icon)
                
            def populate_scenes(docs):
                self.frame.after(0, get_publishes_list, selected, docs)
                    
            get_publishes(callback=populate_scenes)  
            
    def on_publish_selected(self, selected):
        self.get_publish_button.configure(state="disabled")
        
        def get_versions_list(docs):
            
            self.publish_version_list_box.delete(0, "END")
            
            self.publish_doc = docs
            
            if not docs or not docs.get("versions"):
                return
                
            versions = list(docs.get("versions").keys())
            sorted_versions = sorted(versions, key=sort_versions)

            for version in sorted_versions:
                self.publish_version_list_box.insert("END", version)
        
        def populate_versions(docs):
            self.frame.after(0, get_versions_list, docs)
        
        get_publishes_versions(selected, callback=populate_versions)
        
    def on_version_selected(self, selected):
        if selected:
            self.get_publish_button.configure(state="normal")
        else:
           self.get_publish_button.configure(state="disabled")
           
    def copy_publish_id(self):
        woody_id = str(self.publish_doc.get("id"))
        print(f"Woody ID added to clipboard: {woody_id}")
        copy_to_clipboard(woody_id)
    
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
            text="Publishes:",
            **style.HEADER_LABEL
        )
        self.header_label.grid(row=0, pady=5, padx=12, sticky="w")
        
        # Publishes listbox
        self.publishes_list_box = CTkListbox(
            self.frame,
            **style.LIST_BOX_STYLE,
            
            command=self.on_publish_selected
            )
        self.publishes_list_box.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0,5), padx=5)
        
        # Publish versions title
        self.publish_versions_title_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=30
        )
        self.publish_versions_title_frame.grid(row=2, padx=(7,3), pady=(0, 5), sticky="ew")
        self.publish_versions_title_frame.grid_propagate(False)
        
        self.publish_versions_title_label = ctk.CTkLabel(
            self.publish_versions_title_frame,
            text="Publish Versions:",
            **style.SUB_HEADER_LABEL
        )
        self.publish_versions_title_label.grid(row=0, padx=12, sticky="w")
        
        # Publish options title
        self.publish_options_title_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=30
        )
        self.publish_options_title_frame.grid(row=2, column=1, padx=(0,7), pady=(0, 5), sticky="ew")
        self.publish_options_title_frame.grid_propagate(False)
        
        self.publish_options_title_label = ctk.CTkLabel(
            self.publish_options_title_frame,
            text="Publish Options:",
            **style.SUB_HEADER_LABEL
        )
        self.publish_options_title_label.grid(row=0, padx=12, sticky="w")
        
        # Publish versions listbox
        self.publish_version_list_box = CTkListbox(
            self.frame,
            **style.LIST_BOX_STYLE,
            
            command=self.on_version_selected
            )
        self.publish_version_list_box.grid(row=3, column=0, sticky="nsew", pady=(0,5), padx=5)
        
        # Publish options frame
        self.publish_options_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            border_width=2,
            fg_color="transparent",
            height=30
        )
        self.publish_options_frame.grid(row=3, column=1, padx=(0,7), pady=(0, 5), sticky="nsew")
        self.publish_options_frame.grid_propagate(False)
        self.publish_options_frame.grid_columnconfigure(0, weight=1)
        
        # Get publish button
        self.get_publish_button = ctk.CTkButton(
            self.publish_options_frame,
            text="Copy Publish ID",
            **style.BUTTON_STYLE,
            
            command=self.copy_publish_id
        )
        self.get_publish_button.grid(row=0, padx=7, pady=8, sticky="ew")