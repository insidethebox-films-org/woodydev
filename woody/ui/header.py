import os
import customtkinter as ctk
from PIL import Image

class HeaderFrame:
    def __init__(self, parent):
        self.parent = parent
        self.create_frame()
        self.create_widgets()
            
    def create_frame(self):
        self.frame = ctk.CTkFrame(
            self.parent,
            corner_radius=10,        
            border_width=2,          
            border_color="#b59630"
            )
        self.frame.grid_columnconfigure(0, weight=1)
    
    def create_widgets(self):
        
        image_path = os.path.join(os.path.dirname(__file__), "..", "icons", "woodyHeader.png")
        image = Image.open(image_path)
        
        ctk_image = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=(332 / 1.6, 90 / 1.6)
        )

        headerImage = ctk.CTkLabel(
            self.frame, 
            image=ctk_image, 
            text=""
        )
        headerImage.grid(row=0, column=0, columnspan=2, pady=20)