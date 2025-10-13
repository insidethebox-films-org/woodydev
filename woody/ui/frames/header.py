from ...tool.woody_instance import WoodyInstance
from ...lib.mongodb.get_projects import get_projects_db
from ...utils.save_load_settings import save_settings_json

import os
import customtkinter as ctk
from PIL import Image

class HeaderFrame:
    def __init__(self, parent):
        self.parent = parent
        self.create_frame()
        self.create_widgets()

    def set_project_name_settings(self, project_name):
        # project_name contains the combobox selection
        save_settings_json(projectName=project_name)   

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
            height=frames_height
        )
        self.project_picker_frame.grid_columnconfigure(0, weight=1)
        self.project_picker_frame.grid_rowconfigure(0, weight=1)
        self.project_picker_frame.grid(row=0, column=1, sticky="nse", padx=0, pady=0)
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
        
        #Project picker combobox
        self.projectComboBox = ctk.CTkComboBox(
            self.project_picker_frame,
            values=get_projects_db(),
            height=25,
            state="readonly",

            command=self.set_project_name_settings
        )
        self.projectComboBox.set(WoodyInstance().projectName)
        self.projectComboBox.grid(row=0, column=0, sticky="we", padx=12)