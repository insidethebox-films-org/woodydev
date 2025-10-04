from . import style

from ..utils import save_preferences_json, load_preferences_json
from ..lib.folder import create_project_fd
from ..lib.mongodb import create_project_db
from ..plugins.blender.install_blender_libraries import install_blender_libraries

import customtkinter

class PreferencesFrame:
    def __init__(self, parent):
        self.parent = parent
        self.create_frame()
        self.create_widgets()
        self.load_preferances()
            
    def create_frame(self):
        self.frame = customtkinter.CTkFrame(
            self.parent,
            corner_radius=10,        
            border_width=2,          
            border_color="#77553c"
            )
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
    
    def save_preferances(self):
        
        projectName = self.projectNameEntry.get()
        projectDirectory = self.projectDirectoryEntry.get()
        mongoDBAddress = self.mongoDBAddressEntry.get()
        blenderExecutable = self.blenderExecutableEntry.get()
        
        save_preferences_json(projectName, projectDirectory, mongoDBAddress, blenderExecutable)
        
    def load_preferances(self):
        
        preferences = load_preferences_json()
        
        if preferences:
            self.projectNameEntry.insert(0, preferences.get("projectName", ""))
            self.projectDirectoryEntry.insert(0, preferences.get("projectDirectory", ""))
            self.mongoDBAddressEntry.insert(0, preferences.get("mongoDBAddress", ""))
            self.blenderExecutableEntry.insert(0, preferences.get("blenderExecutable", ""))
    
    def create_project(self):
        self.save_preferances()
        
        # Get the Blender executable path
        blender_executable_path = self.blenderExecutableEntry.get().strip()
        if not blender_executable_path:
            print("Blender executable path is required to install libraries.")
            return
        
        create_project_fd()
        create_project_db()

        # Install required libraries into Blender
        print("Installing required libraries into Blender...")
        if install_blender_libraries(blender_executable_path):
            print("Project creation completed successfully!")
        else:
            print("Warning: Project created but library installation failed")
    
    def create_widgets(self):
        
        # Preferences label
        self.preferancesLabel = customtkinter.CTkLabel(
            self.frame, 
            text="Preferences",
            **style.HEADER_LABEL
        )
        self.preferancesLabel.grid(row=0, column=0, sticky="nw", padx=8, pady=(8, 0))  
        
        separator = customtkinter.CTkFrame(self.frame, height=2, fg_color="#414141")
        separator.grid(row=1, column=0, sticky="ew", padx=5, pady=(2, 8), columnspan=2) 
        

        # Project name label
        self.projectNameLabel = customtkinter.CTkLabel(
            self.frame, 
            text="Project Name",
            **style.BODY_LABEL
        )
        self.projectNameLabel.grid(row=2, column=0, sticky="nw", padx=8)

        # Project name entry
        self.projectNameEntry = customtkinter.CTkEntry(
            self.frame,
            height=25
            )
        self.projectNameEntry.grid(row=3, column=0, sticky="new", padx=8, columnspan=2)
        
        # Project directory label
        self.projectDirectoryLabel = customtkinter.CTkLabel(
            self.frame, 
            text="Project Directory",
            **style.BODY_LABEL
        )
        self.projectDirectoryLabel.grid(row=4, column=0, sticky="nw", padx=8)

        # Project name entry
        self.projectDirectoryEntry = customtkinter.CTkEntry(
            self.frame,
            height=25
            )
        self.projectDirectoryEntry.grid(row=5, column=0, sticky="new", padx=8, columnspan=2)
        
        # Mongodb address label
        self.mongoDBAddressLabel = customtkinter.CTkLabel(
            self.frame, 
            text="MongoDB Address",
            **style.BODY_LABEL
        )
        self.mongoDBAddressLabel.grid(row=6, column=0, sticky="nw", padx=8)

        # Mongodb address entry
        self.mongoDBAddressEntry = customtkinter.CTkEntry(
            self.frame,
            height=25
            )
        self.mongoDBAddressEntry.grid(row=7, column=0, sticky="new", padx=8, columnspan=2)
        
        # Blender executable label
        self.blenderExecutableLabel = customtkinter.CTkLabel(
            self.frame, 
            text="Blender Executable",
            **style.BODY_LABEL
        )
        self.blenderExecutableLabel.grid(row=8, column=0, sticky="nw", padx=8)

        # Blender executable entry
        self.blenderExecutableEntry = customtkinter.CTkEntry(
            self.frame,
            height=25
            )
        self.blenderExecutableEntry.grid(row=9, column=0, sticky="new", padx=8, columnspan=2)
        
        # Create project button
        self.createProjectButton = customtkinter.CTkButton(
            self.frame,
            text="Create Project",
            **style.BUTTON_STYLE,
            
            command=self.create_project
        )
        self.createProjectButton.grid(row=10, column=0, sticky="nwe", padx=8, pady=8)
        
        # Save preferances button
        self.savePreferancesButton = customtkinter.CTkButton(
            self.frame,
            text="Save Preferences",
            **style.BUTTON_STYLE,
            
            command=self.save_preferances
        )
        self.savePreferancesButton.grid(row=10, column=1, sticky="nwe", padx=8, pady=8)
        