from .. import style
from ..windows import SettingsWindow

import os
import customtkinter as ctk
from PIL import Image

class ToolsFrame:
    def __init__(self, parent):
        self.parent = parent
        self.create_frame()
        self.create_widgets()
            
    def create_frame(self):
        self.frame = ctk.CTkFrame(
            self.parent,
            corner_radius=8,        
            border_width=2,          
            border_color="#b59630",
            width=50
            )
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_propagate(False)

    def load_icon(self, path, size):
        image = Image.open(path)
        original_width, original_height = image.size
        
        if original_width > original_height:
            new_width = size
            new_height = int((original_height * size) / original_width)
        else:
            new_height = size
            new_width = int((original_width * size) / original_height)
        
        return ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=(new_width, new_height)
        )
        
    def open_settings(self):
        settings = SettingsWindow(self.parent.winfo_toplevel()) 
        settings.run()
    
    def create_widgets(self):
        
        # Create Project Button
        def create_project_input():
            input = ctk.CTkInputDialog(
                text="Project Name", 
                title="Create Project",
                **style.INPUT_DIALOG_STYLE
                )
            return input.get_input()

        create_project_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "icons", "tools", "create_project.png")
        create_project_icon = self.load_icon(create_project_icon_path, 22)

        self.createProjectButton = ctk.CTkButton(
            self.frame,
            image=create_project_icon,
            text="",
            width=40,
            height=40,
            border_width=2,
            border_color="#b59630",
            **style.BUTTON_STYLE,
            
            command=create_project_input
        )
        self.createProjectButton.grid(row=0, column=0, padx=0, pady=(5, 3))

        # Create Element Button
        create_element_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "icons", "tools", "create_element.png")
        create_element_icon = self.load_icon(create_element_icon_path, 25)

        self.createElementButton = ctk.CTkButton(
            self.frame,
            image=create_element_icon,
            text="",
            width=40,
            height=40,
            border_width=2,
            border_color="#4d8242",
            **style.BUTTON_STYLE,
            
            command=""
        )
        self.createElementButton.grid(row=1, column=0, padx=0, pady=(0, 3), sticky="n")
        
        # Create Blend Button
        create_blend_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "icons", "tools", "blender.png")
        create_blend_icon = self.load_icon(create_blend_icon_path, 23)

        self.createBlendButton = ctk.CTkButton(
            self.frame,
            image=create_blend_icon,
            text="",
            width=40,
            height=40,
            border_width=2,
            border_color="#e97824",
            **style.BUTTON_STYLE,
            
            command=""
        )
        self.createBlendButton.grid(row=2, column=0, padx=0, pady=(0, 5), sticky="n")
                
                
        # Settings Button
        settings_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "icons", "tools", "settings.png")
        settings_icon = self.load_icon(settings_icon_path, 23)

        self.settingsButton = ctk.CTkButton(
            self.frame,
            image=settings_icon,
            text="",
            width=40,
            height=40,
            border_width=2,
            border_color="#5a5a5a",
            **style.BUTTON_STYLE,
            
            command=self.open_settings
        )
        self.settingsButton.grid(row=3, column=0, padx=0, pady=5, sticky="s")

