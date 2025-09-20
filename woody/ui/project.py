from . import style

from ..lib.folder import create_groups_sequences_fd
from ..lib.mongodb import create_groups_sequences_db

import customtkinter

class ProjectFrame:
    def __init__(self, parent):
        self.parent = parent
        self.create_frame()
        self.create_widgets()
            
    def create_frame(self):
        self.frame = customtkinter.CTkFrame(
            self.parent,
            corner_radius=10,        
            border_width=2,          
            border_color="#5c6935"
            )
        self.frame.grid_columnconfigure(0, weight=1)
        
    def create_group(self):
        create_groups_sequences_fd(self.groupTypeComboBox.get(), self.groupNameEntry.get())
        create_groups_sequences_db(self.groupTypeComboBox.get(), self.groupNameEntry.get())
    
    def create_widgets(self):
        
        # Project label
        self.projectLabel = customtkinter.CTkLabel(
            self.frame, 
            text="Project",
            **style.HEADER_LABEL

        )
        self.projectLabel.grid(row=0, column=0, sticky="nw", padx=8, pady=(8, 0))  
        
        separator = customtkinter.CTkFrame(self.frame, height=2, fg_color="#414141")
        separator.grid(row=1, column=0, sticky="ew", padx=5, pady=(2, 8), columnspan=2) 
        
        # Group name label
        self.grouptNameLabel = customtkinter.CTkLabel(
            self.frame, 
            text="Group Name",
            **style.BODY_LABEL
        )
        self.grouptNameLabel.grid(row=2, column=0, sticky="nw", padx=8)
        
        # Group name entry
        self.groupNameEntry = customtkinter.CTkEntry(
            self.frame,
            height=25
            )
        self.groupNameEntry.grid(row=3, column=0, sticky="new", padx=8)
                
        # Group type label
        self.grouptTypeLabel = customtkinter.CTkLabel(
            self.frame, 
            text="Group Type",
            **style.BODY_LABEL
        )
        self.grouptTypeLabel.grid(row=4, column=0, sticky="nw", padx=8)        
                
        # Group type combobox
        groupTypeValues = [
            "Assets Group",
            "Shots Sequence"
        ]
        
        self.groupTypeComboBox = customtkinter.CTkComboBox(
            self.frame,
            values=groupTypeValues,
            height=25
        )
        self.groupTypeComboBox.grid(row=5, column=0, sticky="new", padx=8)
        
        # Create group button
        self.createGroupButton = customtkinter.CTkButton(
            self.frame,
            text="Create Group",
            **style.BUTTON_STYLE,
            
            command=self.create_group
        )
        self.createGroupButton.grid(row=6, sticky="nwe", padx=8, pady=8)
