from .. import style

from ...tool.memory_store import store
from ...lib.folder.create_group_sequence_fd import create_group_sequence_fd
from ...lib.mongodb.create_group_sequence_db import create_group_sequence_db

import os
import customtkinter as ctk

class CreateGroupWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Create Group")
        self.window.geometry("300x170")
        
        self.window.transient(parent) 
        self.window.grab_set()
        
        # Set icon
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "icons",
            "woodyIcon.ico"
        )
        self.window.after(201, lambda: self.window.iconbitmap(icon_path))
        
        # Frame
        self.frame = ctk.CTkFrame(
            self.window,
            corner_radius=10,
            border_width=2,
            border_color="#b34555"
        )
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.frame.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        
        self.check_browser_selection()
      
    def check_browser_selection(self):
        data = store.get_namespace("browser_selection")
        root = data.get("root")
     
        if root is None:
            self.groupNameEntry.delete(0, "end")
            self.groupNameEntry.insert(0, "Please select a root in browser")
            self.groupNameEntry.configure(
                state="disabled",
                **style.BODY_DANGER
            )
            self.createGroupButton.configure(state="disabled")   
        
    def create_group(self):
        
        data = store.get_namespace("browser_selection")
        root = data["root"]
        
        create_group_sequence_fd(root, self.groupNameEntry.get().strip())
        create_group_sequence_db(root, self.groupNameEntry.get().strip())
        
    def create_widgets(self):
         
        # Create element label
        self.projectLabel = ctk.CTkLabel(
            self.frame, 
            text="Create Group",
            **style.HEADER_LABEL

        )
        self.projectLabel.grid(row= 0, column=0, sticky="nw", padx=8, pady=(8, 0))  
        
        separator = ctk.CTkFrame(self.frame, height=2, fg_color="#414141")
        separator.grid(row=1, column=0, sticky="ew", padx=5, pady=(2, 8), columnspan=2)
        
        # Group name label
        self.groupNameLabel = ctk.CTkLabel(
            self.frame, 
            text="Group Name",
            **style.BODY_LABEL
        )
        self.groupNameLabel.grid(row=6, column=0, sticky="nw", padx=8)
        
        # Group Name
        self.groupNameEntry = ctk.CTkEntry(
            self.frame,
            height=25    
        )
        self.groupNameEntry.grid(row=7, column=0, sticky="new", padx=8)
        
        # Create Group button
        self.createGroupButton = ctk.CTkButton(
            self.frame,
            text="Create Group",
            **style.BUTTON_STYLE,
            
            command=self.create_group
        )
        self.createGroupButton.grid(row=8, sticky="nwe", padx=8, pady=8)
    
    def run(self):
        self.window.wait_window()