from .. import style

import os

import customtkinter as ctk
from PIL import Image


class HeaderFrame:
    def __init__(self, parent):
        self.parent = parent
        self.create_frame()
        self.create_widgets()

    def create_frame(self):
        frames_height=50
        
        # Main frame
        self.frame = ctk.CTkFrame(
            self.parent,
            fg_color="transparent",
            height=frames_height
        )
        self.frame.pack(fill="x", padx=3, pady=3)
        self.frame.pack_propagate(False) 
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Logo frame 
        self.logo_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=10,        
            border_width=2,          
            border_color="#b59630",
            fg_color="#222222",
            height=frames_height
        )
        self.logo_frame.grid_columnconfigure(0, weight=1)
        self.logo_frame.grid_rowconfigure(0, weight=1)
        self.logo_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 3), pady=0)
        self.logo_frame.grid_propagate(False) 
        
        # Project picker frame 
        self.project_picker_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=10,        
            border_width=2,          
            border_color="#77563c",
            fg_color="#222222",
            height=frames_height,
            width=235
        )
        self.project_picker_frame.grid_columnconfigure(0, weight=1)
        self.project_picker_frame.grid_rowconfigure(0, weight=1)
        self.project_picker_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.project_picker_frame.grid_propagate(False)
    
    def create_widgets(self):
        
        image_path = os.path.join(os.path.dirname(__file__), "..", "..", "icons", "woodyHeader.png")
        image = Image.open(image_path)
        
        header_image = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=(332 / 3, 90 / 3)
        )

        headerImage = ctk.CTkLabel(
            self.logo_frame, 
            image=header_image, 
            text="",
            fg_color="transparent"
        )
        headerImage.grid(row=0, column=0, pady=(5, 2), padx=12, sticky="nsw")
        
        self.project_label = ctk.CTkLabel(
            self.project_picker_frame,
            text="Projects:",
            **style.SUB_HEADER_LABEL,
            text_color="#EBEBEB"
        )
        self.project_label.grid(row=0, column=0, sticky="we", padx=(12,0), pady=(0,1))
        
        #Project picker combobox
        self.projectComboBox = ctk.CTkComboBox(
            self.project_picker_frame,
            values="",
            height=25,
            state="readonly",
            command=""
        )
        self.projectComboBox.grid(row=0, column=1, sticky="we", padx=(6,12))