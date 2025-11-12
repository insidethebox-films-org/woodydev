from .. import style
from ..widgets import CTkListbox

import customtkinter as ctk

class PublishesFrame:
    def __init__(self, parent):
        self.parent = parent
        self.create_frame()
        self.create_widgets()
        
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
        self.header_label.grid(row=0, pady=7, padx=12, sticky="w")
        
        # Publishes listbox
        self.publishes_list_box = CTkListbox(
            self.frame,
            **style.LIST_BOX_STYLE,
            
            command=""
            )
        self.publishes_list_box.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(3,5), padx=5)
        
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
        
        self.blend_options_title_label = ctk.CTkLabel(
            self.publish_options_title_frame,
            text="Publish Options:",
            **style.SUB_HEADER_LABEL
        )
        self.blend_options_title_label.grid(row=0, padx=12, sticky="w")
        
        # Publish versions listbox
        self.publish_version_list_box = CTkListbox(
            self.frame,
            **style.LIST_BOX_STYLE,
            
            command=""
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
            
            command=""
        )
        self.get_publish_button.grid(row=0, padx=7, pady=8, sticky="ew")