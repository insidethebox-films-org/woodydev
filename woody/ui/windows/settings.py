from .. import style
from ...utils import save_preferences_json, load_preferences_json

import os
import customtkinter as ctk

class SettingsWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Settings")
        self.window.geometry("500x290")
        
        self.window.transient(parent) 
        self.window.grab_set()
        
        # Set icon
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "icons",
            "woodyIcon.ico"
        )
        self.window.iconbitmap(icon_path)
        
        # Frame
        self.frame = ctk.CTkFrame(
            self.window,
            corner_radius=10,
            border_width=2,
            border_color="#5c6935"
        )
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.create_widgets()
        self.load_preferances()
        
    def create_widgets(self):
        # Project Settings Label
        self.projectLabel = ctk.CTkLabel(
            self.frame,
            text="Project Settings",
            **style.HEADER_LABEL
        )
        self.projectLabel.grid(row=0, column=0, sticky="nw", padx=8, pady=(8, 0))
        
        # Separator
        self.separator = ctk.CTkFrame(
            self.frame,
            height=2,
            fg_color="#414141"
        )
        self.separator.grid(row=1, column=0, sticky="ew", padx=5, pady=(2, 8))
        
        # Project Directory
        self.projectDirectoryLabel = ctk.CTkLabel(
            self.frame,
            text="Project Directory",
            **style.BODY_LABEL
        )
        self.projectDirectoryLabel.grid(row=4, column=0, sticky="nw", padx=8)
        
        self.projectDirectoryEntry = ctk.CTkEntry(
            self.frame,
        )
        self.projectDirectoryEntry.grid(row=5, column=0, sticky="ew", padx=8)
        
        # MongoDB Address
        self.mongoDBAddressLabel = ctk.CTkLabel(
            self.frame,
            text="MongoDB Address",
            **style.BODY_LABEL
        )
        self.mongoDBAddressLabel.grid(row=6, column=0, sticky="nw", padx=8)
        
        self.mongoDBAddressEntry = ctk.CTkEntry(
            self.frame,
        )
        self.mongoDBAddressEntry.grid(row=7, column=0, sticky="ew", padx=8)
        
        # Blender Executable
        self.blenderExecutableLabel = ctk.CTkLabel(
            self.frame,
            text="Blender Executable",
            **style.BODY_LABEL
        )
        self.blenderExecutableLabel.grid(row=8, column=0, sticky="nw", padx=8)
        
        self.blenderExecutableEntry = ctk.CTkEntry(
            self.frame,
        )
        self.blenderExecutableEntry.grid(row=9, column=0, sticky="ew", padx=8)
        
        # Save Button
        self.savePreferancesButton = ctk.CTkButton(
            self.frame,
            text="Save Preferences",
            command=self.save_preferances,
            **style.BUTTON_STYLE
        )
        self.savePreferancesButton.grid(row=10, column=0, sticky="ew", padx=8, pady=8)
        
        # Configure column weight
        self.frame.grid_columnconfigure(0, weight=1)
    
    def load_preferances(self):
        preferences = load_preferences_json()
        self.projectDirectoryEntry.insert(0, preferences.get("projectDirectory", ""))
        self.mongoDBAddressEntry.insert(0, preferences.get("mongoDBAddress", ""))
        self.blenderExecutableEntry.insert(0, preferences.get("blenderExecutable", ""))
    
    def save_preferances(self):
        projectDirectory = self.projectDirectoryEntry.get()
        mongoDBAddress = self.mongoDBAddressEntry.get()
        blenderExecutable = self.blenderExecutableEntry.get()
        
        save_preferences_json(projectDirectory, mongoDBAddress, blenderExecutable)
        self.window.destroy()
    
    def run(self):
        self.window.wait_window()