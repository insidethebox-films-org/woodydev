from . import style

from ..lib.folder import create_group_sequence_fd
from ..lib.mongodb import create_group_sequence_db
from ..lib.mongodb import create_element_db
from ..lib.folder import create_element_fd

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
        
    def create_element(self):
        create_group_sequence_fd(self.groupTypeComboBox.get(), self.groupsNameComboBox.get())
        create_group_sequence_db(self.groupTypeComboBox.get(), self.groupsNameComboBox.get())
        create_element_db(self.groupTypeComboBox.get(), self.groupsNameComboBox.get(), self.elementNameEntry.get())
        create_element_fd(self.groupTypeComboBox.get(), self.groupsNameComboBox.get(), self.elementNameEntry.get())
    
    def create_widgets(self):        
        
        # Project label
        self.projectLabel = customtkinter.CTkLabel(
            self.frame, 
            text="Project",
            **style.HEADER_LABEL

        )
        self.projectLabel.grid(row= 0, column=0, sticky="nw", padx=8, pady=(8, 0))  
        
        separator = customtkinter.CTkFrame(self.frame, height=2, fg_color="#414141")
        separator.grid(row=1, column=0, sticky="ew", padx=5, pady=(2, 8), columnspan=2) 

        # Group type label
        self.groupTypeLabel = customtkinter.CTkLabel(
            self.frame, 
            text="Group Type",
            **style.BODY_LABEL
        )
        self.groupTypeLabel.grid(row=2, column=0, sticky="nw", padx=8)        
        
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
        self.groupTypeComboBox.grid(row=3, column=0, sticky="new", padx=8)
        
        # Group name label
        self.groupNameLabel = customtkinter.CTkLabel(
            self.frame, 
            text="Group Name",
            **style.BODY_LABEL
        )
        self.groupNameLabel.grid(row=4, column=0, sticky="nw", padx=8)
        
        # Group name combobox
        groupNameValues = []
        
        self.groupsNameComboBox = customtkinter.CTkComboBox(
            self.frame,
            values=groupNameValues,
            height=25
        )
        self.groupsNameComboBox.grid(row=5, column=0, sticky="new", padx=8)
        
        # Element name label
        self.groupNameLabel = customtkinter.CTkLabel(
            self.frame, 
            text="Element Name",
            **style.BODY_LABEL
        )
        self.groupNameLabel.grid(row=6, column=0, sticky="nw", padx=8)
        
        # Element Name
        self.elementNameEntry = customtkinter.CTkEntry(
            self.frame,
            height=25    
        )
        self.elementNameEntry.grid(row=7, column=0, sticky="new", padx=8)
        
        # Create Element
        self.createGroupButton = customtkinter.CTkButton(
            self.frame,
            text="Create Element",
            **style.BUTTON_STYLE,
            
            command=self.create_element
        )
        self.createGroupButton.grid(row=8, sticky="nwe", padx=8, pady=8)


