from . import style

from ..lib.folder import create_element_fd
from ..lib.folder import create_group_sequence_fd
from ..lib.mongodb import create_group_sequence_db
from ..lib.mongodb import create_element_db
from ..lib.mongodb import get_group_sequence_names
from ..lib.mongodb import create_blend_db

from ..plugins.blender.blender_instance import BlenderInstance

import customtkinter
import re
import threading
import time

class ProjectFrame:
    def __init__(self, parent):
        self.parent = parent
        self.create_frame()
        self.create_widgets()

        self.blender = BlenderInstance()
        
        threading.Thread(target=self.refresh_groups_name_comboBox, daemon=True).start()
            
    def create_frame(self):
        self.frame = customtkinter.CTkFrame(
            self.parent,
            corner_radius=10,        
            border_width=2,          
            border_color="#5c6935"
            )
        self.frame.grid_columnconfigure(0, weight=1)
        
    def refresh_groups_name_comboBox(self):
        while True:
            try:
                current = self.groupsNameComboBox.get()
                new_values = get_group_sequence_names(self.groupTypeComboBox.get())
                
                if new_values != self.groupsNameComboBox.cget("values"):
                    self.groupsNameComboBox.configure(values=new_values)
                    if current in new_values:
                        self.groupsNameComboBox.set(current)
                
                time.sleep(2)
            except:
                time.sleep(2)
    
    def create_element(self):
        create_group_sequence_fd(self.groupTypeComboBox.get(), self.groupsNameComboBox.get())
        create_group_sequence_db(self.groupTypeComboBox.get(), self.groupsNameComboBox.get())
        create_element_db(self.groupTypeComboBox.get(), self.groupsNameComboBox.get(), self.elementNameEntry.get())
        create_element_fd(self.groupTypeComboBox.get(), self.groupsNameComboBox.get(), self.elementNameEntry.get())


    def _create_blend_file(self):
        blend_name = self.blendNameEntry.get().strip()
        # Validate blend name - prevent _latest and _v* patterns
        if self._is_invalid_blend_name(blend_name):
            print(
                "Invalid Name", 
                "Blend name cannot contain '_latest' or version suffixes like '_v1', '_v2', etc.\n"
                "These suffixes are reserved for the versioning system."
            )
            return
        group_type = "assets" if self.groupTypeComboBox.get() == "Assets Group" else "shots"
        
        # Try to create the database entry first
        if create_blend_db(group_type, self.groupsNameComboBox.get(), self.elementNameEntry.get(), self.blendNameEntry.get()):
            # Only create the file if database entry was successful
            success = self.blender.create_file(
                group_type,
                self.groupsNameComboBox.get(),
                self.elementNameEntry.get(),
                self.blendNameEntry.get()
            )
            
            if success:
                print("Blend file created successfully!")
            else:
                print("Failed to create blend file")
        else:
            print("Failed to create database entry - blend file not created")
       
    def _is_invalid_blend_name(self, name: str) -> bool:
        """Check if blend name contains reserved suffixes"""
        if "_latest" in name:
            return True
        if re.search(r"_v\d+", name):
            return True
        return False

    def _open_blend_file(self):
        group_type = "assets" if self.groupTypeComboBox.get() == "Assets Group" else "shots"
        self.blender.open_file(
            group_type,
            self.groupsNameComboBox.get(), 
            self.elementNameEntry.get(),
            self.blendNameEntry.get()
        )

    def _dev_update(self):
        if self.blender.dev_update():
            print("Dev Update Complete", "Addon zip has been recreated successfully!")
        else:
            print("Dev Update Failed", "Failed to recreate addon zip. Check the console for details.")
    
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
            height=25,
            state="readonly"
        )
        self.groupTypeComboBox.set("Assets Group")
        self.groupTypeComboBox.grid(row=3, column=0, sticky="new", padx=8)
        
        # Group name label
        self.groupNameLabel = customtkinter.CTkLabel(
            self.frame, 
            text="Group Name",
            **style.BODY_LABEL
        )
        self.groupNameLabel.grid(row=4, column=0, sticky="nw", padx=8)
        
        # Group name combobox
        self.groupsNameComboBox = customtkinter.CTkComboBox(
            self.frame,
            values=get_group_sequence_names(self.groupTypeComboBox.get()),
            height=25
        )
        self.groupsNameComboBox.set("")
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

        # Blend name label
        self.groupNameLabel = customtkinter.CTkLabel(
            self.frame, 
            text="Blend FileName",
            **style.BODY_LABEL
        )
        self.groupNameLabel.grid(row=9, column=0, sticky="nw", padx=8)
        
        # Blend Name
        self.blendNameEntry = customtkinter.CTkEntry(
            self.frame,
            height=25    
        )
        self.blendNameEntry.grid(row=10, column=0, sticky="new", padx=8)

        # Add Blender buttons
        self.createBlendButton = customtkinter.CTkButton(
            self.frame,
            text="Create Blend File",
            **style.BUTTON_STYLE,
            command=self._create_blend_file
        )
        self.createBlendButton.grid(row=11, sticky="nwe", padx=8, pady=(0,4))

        self.openBlendButton = customtkinter.CTkButton(
            self.frame,
            text="Open in Blender",
            **style.BUTTON_STYLE,
            command=self._open_blend_file
        )
        self.openBlendButton.grid(row=12, sticky="nwe", padx=8, pady=(0,8))

        self.devUpdateButton = customtkinter.CTkButton(
        self.frame,
        text="Dev Update",
        **style.BUTTON_STYLE,
        command=self._dev_update
        )
        self.devUpdateButton.grid(row=13, sticky="nwe", padx=8, pady=(0,8))


