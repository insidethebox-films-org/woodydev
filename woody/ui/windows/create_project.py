from .. import style
from ...utils import save_project_preferences_json
from ...lib.folder import create_project_fd
from ...lib.mongodb import create_project_db
from ...plugins.blender.install_blender_libraries import install_blender_libraries
from ...plugins.blender.operations.copy_prefs_to_addon import copy_prefs_to_addon

import os
import customtkinter as ctk

class CreateProjectWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Create Project")
        self.window.geometry("300x275")
        
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
            border_color="#b59630"
        )
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.frame.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        
    def create_project(self):
        # Save project preferences and get project name
        project_name = save_project_preferences_json(
            self.projectNameEntry.get(),
            self.blenderExecutableEntry.get(), 
            self.projectDirectoryEntry.get()
        )
        
        # Create project folders and database
        create_project_fd()
        create_project_db()

        # Install Blender libraries
        blender_executable_path = self.blenderExecutableEntry.get().strip()
        if blender_executable_path:
            print("Installing required libraries into Blender...")
            if install_blender_libraries(blender_executable_path):
                print("Blender libraries installed successfully!")
            else:
                print("Warning: Library installation failed")
        
        # Copy prefs to addon
        copy_prefs_to_addon()
        
        print(f"Project '{project_name}' created successfully!")
        self.window.destroy()
    
    def create_widgets(self):
        
        # Preferences label
        self.preferancesLabel = ctk.CTkLabel(
            self.frame, 
            text="Create Project",
            **style.HEADER_LABEL
        )
        self.preferancesLabel.grid(row=0, column=0, sticky="nw", padx=8, pady=(8, 0))  
        
        separator = ctk.CTkFrame(self.frame, height=2, fg_color="#414141")
        separator.grid(row=1, column=0, sticky="ew", padx=5, pady=(2, 8), columnspan=2) 
        

        # Project name label
        self.projectNameLabel = ctk.CTkLabel(
            self.frame, 
            text="Project Name",
            **style.BODY_LABEL
        )
        self.projectNameLabel.grid(row=2, column=0, sticky="nw", padx=8)

        # Project name entry
        self.projectNameEntry = ctk.CTkEntry(
            self.frame,
            height=25
            )
        self.projectNameEntry.grid(row=3, column=0, sticky="new", padx=8, columnspan=2)
        
        # Project directory label
        self.projectDirectoryLabel = ctk.CTkLabel(
            self.frame, 
            text="Project Directory",
            **style.BODY_LABEL
        )
        self.projectDirectoryLabel.grid(row=4, column=0, sticky="nw", padx=8)

        # Project name entry
        self.projectDirectoryEntry = ctk.CTkEntry(
            self.frame,
            height=25
            )
        self.projectDirectoryEntry.grid(row=5, column=0, sticky="new", padx=8, columnspan=2)
        
        # Blender executable label
        self.blenderExecutableLabel = ctk.CTkLabel(
            self.frame, 
            text="Blender Executable",
            **style.BODY_LABEL
        )
        self.blenderExecutableLabel.grid(row=8, column=0, sticky="nw", padx=8)

        # Blender executable entry
        self.blenderExecutableEntry = ctk.CTkEntry(
            self.frame,
            height=25
            )
        self.blenderExecutableEntry.grid(row=9, column=0, sticky="new", padx=8, columnspan=2)
        
        # Create project button
        self.createProjectButton = ctk.CTkButton(
            self.frame,
            text="Create Project",
            **style.BUTTON_STYLE,
            
            command=self.create_project
        )
        self.createProjectButton.grid(row=10, column=0, sticky="nwe", padx=8, pady=8)
    
    def run(self):
        self.window.wait_window()