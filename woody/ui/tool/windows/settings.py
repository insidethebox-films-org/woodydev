from ... import style
from ....utils import save_settings_json, load_settings_json
from ....objects import Woody

import os
import customtkinter as ctk

class SettingsWindow:
    def __init__(self, parent, status_bar):
        self.window = ctk.CTkToplevel(parent)
        self.status_bar = status_bar
        self.window.title("Settings")
        self.window.geometry("500x325")
        
        self.window.transient(parent) 
        self.window.grab_set()
        
        
        # Set icon
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "..",
            "icons",
            "woodyIcon.ico"
        )
        self.window.after(201, lambda: self.window.iconbitmap(icon_path))
        
        # Frame
        self.frame = ctk.CTkFrame(
            self.window,
            corner_radius=10,
            border_width=2,
            border_color="#5a5a5a"
        )
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.frame.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        self.load_settings()
        
    def load_settings(self):
        preferences = load_settings_json()
        self.mongoDBAddressEntry.insert(0, preferences.get("mongoDBAddress", ""))
        self.blenderExecutableEntry.insert(1, preferences.get("blenderExecutable", ""))
        self.houdiniExecutableEntry.insert(1, preferences.get("houdiniExecutable", ""))
        self.rvExecutableEntry.insert(1, preferences.get("rvExecutable", ""))
    
    def save_settings(self):
        mongoDBAddress = self.mongoDBAddressEntry.get()
        blenderExecutable = self.blenderExecutableEntry.get()
        houdiniExecutable = self.houdiniExecutableEntry.get()
        rvExecutable = self.rvExecutableEntry.get()
        
        print(f"Saving settings:\nMongoDB Address: {mongoDBAddress}\nBlender Executable: {blenderExecutable}\nHoudini Executable: {houdiniExecutable}\nRV Executable: {rvExecutable}")
        save_settings_json(mongoDBAddress=mongoDBAddress, blenderExecutable=blenderExecutable, houdiniExecutable=houdiniExecutable, rvExecutable=rvExecutable)
        self.window.destroy()
    
    def create_widgets(self):
        # Settings Label
        self.settingsLabel = ctk.CTkLabel(
            self.frame,
            text="Settings",
            **style.HEADER_LABEL
        )
        self.settingsLabel.grid(row=0, column=0, sticky="nw", padx=8, pady=(8, 0))
        
        # Separator
        self.separator = ctk.CTkFrame(
            self.frame,
            height=2,
            fg_color="#414141"
        )
        self.separator.grid(row=1, column=0, sticky="ew", padx=5, pady=(2, 8))

        # MongoDB Address
        self.mongoDBAddressLabel = ctk.CTkLabel(
            self.frame,
            text="MongoDB Address",
            **style.BODY_LABEL
        )
        self.mongoDBAddressLabel.grid(row=2, column=0, sticky="nw", padx=8)
        
        self.mongoDBAddressEntry = ctk.CTkEntry(
            self.frame,
        )
        self.mongoDBAddressEntry.grid(row=3, column=0, sticky="ew", padx=8)

        # Blender executable label
        self.blenderExecutableLabel = ctk.CTkLabel(
            self.frame, 
            text="Blender Executable",
            **style.BODY_LABEL
        )
        self.blenderExecutableLabel.grid(row=4, column=0, sticky="nw", padx=8)

        # Blender executable entry
        self.blenderExecutableEntry = ctk.CTkEntry(
            self.frame,
            height=25
            )
        self.blenderExecutableEntry.grid(row=5, column=0, sticky="new", padx=8, columnspan=2)
        
        # Houdini executable label
        self.houdiniExecutableLabel = ctk.CTkLabel(
            self.frame, 
            text="Houdini Executable",
            **style.BODY_LABEL
        )
        self.houdiniExecutableLabel.grid(row=6, column=0, sticky="nw", padx=8)

        # Houdini executable entry
        self.houdiniExecutableEntry = ctk.CTkEntry(
            self.frame,
            height=25
            )
        self.houdiniExecutableEntry.grid(row=7, column=0, sticky="new", padx=8, columnspan=2)
        
        # RV executable label
        self.rvExecutableLabel = ctk.CTkLabel(
            self.frame, 
            text="RV Executable",
            **style.BODY_LABEL
        )
        self.rvExecutableLabel.grid(row=8, column=0, sticky="nw", padx=8)

        # RV executable entry
        self.rvExecutableEntry = ctk.CTkEntry(
            self.frame,
            height=25
            )
        self.rvExecutableEntry.grid(row=9, column=0, sticky="new", padx=8, columnspan=2)
        
        # Save settings button
        self.saveSettingsButton = ctk.CTkButton(
            self.frame,
            text="Save Settings",
            **style.BUTTON_STYLE,
            
            command=self.save_settings
        )
        self.saveSettingsButton.grid(row=10, column=0, sticky="nwe", padx=8, pady=8)
        
        separator = ctk.CTkFrame(self.frame, height=2, fg_color="#414141")
        separator.grid(row=11, column=0, sticky="ew", padx=5, pady=(2, 8), columnspan=2)
    
    def run(self):
        self.window.wait_window()