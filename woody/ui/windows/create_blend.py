from .. import style

from ...lib.mongodb import get_group_sequence_names
from ...lib.mongodb import create_blend_db

from ...plugins.blender.blender_instance import BlenderInstance

import re
import os
import threading
import time
import customtkinter as ctk

class CreateBlendWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Create Blender Scene")
        self.window.geometry("300x420")
        
        self.window.transient(parent) 
        self.window.grab_set()
        
        self.blender = BlenderInstance()
        
        # Set icon
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "icons",
            "woodyIcon.ico"
        )
        self.window.iconbitmap(icon_path)
        
        threading.Thread(target=self.refresh_groups_name_comboBox, daemon=True).start()
        
        # Frame
        self.frame = ctk.CTkFrame(
            self.window,
            corner_radius=10,
            border_width=2,
            border_color="#e97824"
        )
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.frame.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        
    def refresh_groups_name_comboBox(self):
        while True:
            try:
                current = self.groupsNameComboBox.get()
                new_values = get_group_sequence_names(self.groupTypeComboBox.get())
                
                if new_values != self.groupsNameComboBox.cget("values"):
                    self.groupsNameComboBox.configure(values=new_values)
                    if current in new_values:
                        self.groupsNameComboBox.set(current)
                
                time.sleep(1)
            except:
                time.sleep(1)
        
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
        
        # Append _latest to the blend name for file creation
        blend_name_with_latest = f"{blend_name}_latest"
        group_type = "assets" if self.groupTypeComboBox.get() == "Assets Group" else "shots"
        
        # Try to create the database entry first
        if create_blend_db(group_type, self.groupsNameComboBox.get(), self.elementNameEntry.get(), blend_name):
            # Only create the file if database entry was successful
            success = self.blender.create_file(
                group_type,
                self.groupsNameComboBox.get(),
                self.elementNameEntry.get(),
                blend_name_with_latest
            )
            
            if success:
                print(f"Blend file created successfully: {blend_name_with_latest}")
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
        
    def create_widgets(self):
        
        # Project label
        self.projectLabel = ctk.CTkLabel(
            self.frame, 
            text="Create Blender Scene",
            **style.HEADER_LABEL

        )
        self.projectLabel.grid(row= 0, column=0, sticky="nw", padx=8, pady=(8, 0))  
        
        separator = ctk.CTkFrame(self.frame, height=2, fg_color="#414141")
        separator.grid(row=1, column=0, sticky="ew", padx=5, pady=(2, 8), columnspan=2) 
        
                # Group type label
        self.groupTypeLabel = ctk.CTkLabel(
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
        
        self.groupTypeComboBox = ctk.CTkComboBox(
            self.frame,
            values=groupTypeValues,
            height=25,
            state="readonly"
        )
        self.groupTypeComboBox.set("Assets Group")
        self.groupTypeComboBox.grid(row=3, column=0, sticky="new", padx=8)
        
        # Group name label
        self.groupNameLabel = ctk.CTkLabel(
            self.frame, 
            text="Group Name",
            **style.BODY_LABEL
        )
        self.groupNameLabel.grid(row=4, column=0, sticky="nw", padx=8)
        
        # Group name combobox
        self.groupsNameComboBox = ctk.CTkComboBox(
            self.frame,
            values=get_group_sequence_names(self.groupTypeComboBox.get()),
            height=25
        )
        self.groupsNameComboBox.set("")
        self.groupsNameComboBox.grid(row=5, column=0, sticky="new", padx=8)
        
        # Element name label
        self.groupNameLabel = ctk.CTkLabel(
            self.frame, 
            text="Element Name",
            **style.BODY_LABEL
        )
        self.groupNameLabel.grid(row=6, column=0, sticky="nw", padx=8)
        
        # Element Name
        self.elementNameEntry = ctk.CTkEntry(
            self.frame,
            height=25    
        )
        self.elementNameEntry.grid(row=7, column=0, sticky="new", padx=8)

        # Blend name label
        self.groupNameLabel = ctk.CTkLabel(
            self.frame, 
            text="Blend FileName",
            **style.BODY_LABEL
        )
        self.groupNameLabel.grid(row=9, column=0, sticky="nw", padx=8, pady=3)
        
        # Blend Name
        self.blendNameEntry = ctk.CTkEntry(
            self.frame,
            height=25    
        )
        self.blendNameEntry.grid(row=10, column=0, sticky="new", padx=8, pady=3)

        # Add Blender buttons
        self.createBlendButton = ctk.CTkButton(
            self.frame,
            text="Create Blend File",
            **style.BUTTON_STYLE,
            command=self._create_blend_file
        )
        self.createBlendButton.grid(row=11, sticky="nwe", padx=8, pady=3)

        self.openBlendButton = ctk.CTkButton(
            self.frame,
            text="Open in Blender",
            **style.BUTTON_STYLE,
            command=self._open_blend_file
        )
        self.openBlendButton.grid(row=12, sticky="nwe", padx=8, pady=3)

    def run(self):
        self.window.wait_window()