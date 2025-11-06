from .. import style

import customtkinter as ctk

class AssetDetailsFrame: 
    def __init__(self, parent):
        self.parent = parent
        self.detail_widgets = []
        
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

    def create_widgets(self):
        
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
        
        # Title
        self.title_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=30
        )
        self.title_frame.grid(row=1, padx=7, pady=(0, 3), sticky="ew")
        self.title_frame.grid_propagate(False)
        
        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="Select an item",
            **style.SUB_HEADER_LABEL
        )
        self.title_label.grid(row=0, padx=12, sticky="w")
        
        # Dynamic asset details frame
        self.asset_details_frame = ctk.CTkScrollableFrame(
            self.frame,
            corner_radius=5,
            fg_color="transparent",      
            border_width=2,
            
        )
        self.asset_details_frame.grid(row=2, padx=7, pady=(3,7), sticky="nsew")
        self.asset_details_frame.grid_columnconfigure(0, weight=1)
        self.asset_details_frame._scrollbar.grid(padx=(0, 3), pady=3)