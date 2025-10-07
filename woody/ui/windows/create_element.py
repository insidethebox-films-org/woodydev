from .. import style
from ...lib.folder import create_element_fd
from ...lib.folder import create_group_sequence_fd
from ...lib.mongodb import create_group_sequence_db
from ...lib.mongodb import create_element_db
from ...lib.mongodb import get_group_sequence_names

import os
import time
import threading
import customtkinter as ctk

class CreateElementWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Create Element")
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
        
        threading.Thread(target=self.refresh_groups_name_comboBox, daemon=True).start()
        
        # Frame
        self.frame = ctk.CTkFrame(
            self.window,
            corner_radius=10,
            border_width=2,
            border_color="#4d8242"
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
    
    def create_element(self):
        create_group_sequence_fd(self.groupTypeComboBox.get(), self.groupsNameComboBox.get())
        create_group_sequence_db(self.groupTypeComboBox.get(), self.groupsNameComboBox.get())
        create_element_db(self.groupTypeComboBox.get(), self.groupsNameComboBox.get(), self.elementNameEntry.get())
        create_element_fd(self.groupTypeComboBox.get(), self.groupsNameComboBox.get(), self.elementNameEntry.get())
        
    def create_widgets(self):
         
        # Create element label
        self.projectLabel = ctk.CTkLabel(
            self.frame, 
            text="Create Element",
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
        
        # Create Element
        self.createGroupButton = ctk.CTkButton(
            self.frame,
            text="Create Element",
            **style.BUTTON_STYLE,
            
            command=self.create_element
        )
        self.createGroupButton.grid(row=8, sticky="nwe", padx=8, pady=8)
    
    def run(self):
        self.window.wait_window()