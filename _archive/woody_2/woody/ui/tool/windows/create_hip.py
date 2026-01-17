from ... import style
from ....database.tool.create_scene_db import create_scene_db
from ....dcc.houdini.create_hip_file import create_file
from ....objects.memory_store import store

import re
import os
import customtkinter as ctk

class CreateHipWindow:
    def __init__(self, parent, status_bar):
        self.window = ctk.CTkToplevel(parent)
        self.status_bar = status_bar
        self.window.title("Create Houdini Scene")
        self.window.geometry("300x170")
        
        self.window.transient(parent) 
        self.window.grab_set()
        
        
        # Set icon
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "..",
            "icons",
            "woodyIcon.ico"
        )
        if os.path.exists(icon_path):
            self.window.after(201, lambda: self.window.iconbitmap(icon_path))
        
        # Frame
        self.frame = ctk.CTkFrame(
            self.window,
            corner_radius=10,
            border_width=2,
            border_color="#e94c24"
        )
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.frame.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        
        self.check_browser_selection()

    def check_browser_selection(self):
        data = store.get_namespace("browser_selection")
        element = data.get("element")
        
        if element is None:
            self.hipNameEntry.delete(0, "end")
            self.hipNameEntry.insert(0, "Please select an element in browser")
            self.hipNameEntry.configure(
                state="disabled",
                **style.BODY_DANGER
            )
            self.createHipButton.configure(state="disabled")      
    
    def create_hip_file(self):
        dcc = "houdini"
        data = store.get_namespace("browser_selection")
        root = str.lower(data["root"])
        group = data["group"]
        element = data["element"]
        
        scene_name = self.hipNameEntry.get().strip()
        if self._is_invalid_hip_name(scene_name):
            print(
                "Invalid Name", 
                "Hip name cannot contain '_latest' or version suffixes like '_v1', '_v2', etc.\n"
                "These suffixes are reserved for the versioning system."
            )
            return
        
        hip_name_with_latest = f"{scene_name}_latest.hip"
        
        if create_scene_db(root, group, element, scene_name, dcc):
            create_file(
                root,
                group,
                element,
                hip_name_with_latest
            )
            print(f"Hip file created successfully: {hip_name_with_latest}")
        else:
            print("Failed to create database entry - hip file not created")
       
    def _is_invalid_hip_name(self, name: str) -> bool:
        if "_latest" in name:
            return True
        if re.search(r"_v\d+", name):
            return True
        return False
        
    def create_widgets(self):
        
        # Project label
        self.projectLabel = ctk.CTkLabel(
            self.frame, 
            text="Create Houdini Scene",
            **style.HEADER_LABEL

        )
        self.projectLabel.grid(row= 0, column=0, sticky="nw", padx=8, pady=(8, 0))  
        
        separator = ctk.CTkFrame(self.frame, height=2, fg_color="#414141")
        separator.grid(row=1, column=0, sticky="ew", padx=5, pady=(2, 8), columnspan=2) 

        # Hip name label
        self.groupNameLabel = ctk.CTkLabel(
            self.frame, 
            text="Hip File Name",
            **style.BODY_LABEL
        )
        self.groupNameLabel.grid(row=2, column=0, sticky="nw", padx=8)
        
        # Hip Name
        self.hipNameEntry = ctk.CTkEntry(
            self.frame,
            height=25    
        )
        self.hipNameEntry.grid(row=3, column=0, sticky="new", padx=8)

        # Add Houdini button
        self.createHipButton = ctk.CTkButton(
            self.frame,
            text="Create Hip File",
            **style.BUTTON_STYLE,
            command=self.create_hip_file
        )
        self.createHipButton.grid(row=4, sticky="nwe", padx=8, pady=8)

    def run(self):
        self.window.wait_window()