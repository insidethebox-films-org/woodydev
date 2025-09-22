from .ui import *

import customtkinter
import os

class WoodyApp:
    def __init__(self):
        self.mainWindow = customtkinter.CTk()
        self.mainWindow.geometry("300x670")
        self.mainWindow.title("Woody")
        
        # Create icon
        icon_path = os.path.join(os.path.dirname(__file__), "icons", "woodyIcon.ico")
        self.mainWindow.iconbitmap(icon_path)
        
        # Create ui
        self.setup_ui()
    
    def setup_ui(self):
        
        self.mainWindow.grid_columnconfigure(0, weight=1)
        
        # Header
        self.header_frame = HeaderFrame(self.mainWindow)
        self.header_frame.frame.grid(row=0, column=0, sticky="nsew", padx=3, pady=3)
        
        #Preferences  
        self.preferences_frame = PreferencesFrame(self.mainWindow)
        self.preferences_frame.frame.grid(row=1, column=0, sticky="nsew", padx=3, pady=3)
        
        # Project
        self.project_frame = ProjectFrame(self.mainWindow)
        self.project_frame.frame.grid(row=2, column=0, sticky="nsew", padx=3, pady=3)
        
    def run(self):
        self.mainWindow.mainloop()
        
__all__ = ['WoodyApp']