from .. import style
from ...lib.folder.create_element_fd import create_element_fd
from ...lib.mongodb.create_element_db import create_element_db
from ...tool.memory_store import store

import os
import customtkinter as ctk

class CreateElementWindow:
    def __init__(self, parent):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Create Element")
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
            border_color="#4d8242"
        )
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.frame.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        
        self.check_browser_selection()
    
    def check_browser_selection(self):
        data = store.get_namespace("browser_selection")
        group = data.get("group")
     
        if group == None:
            self.elementNameEntry.delete(0, "end")
            self.elementNameEntry.insert(0, "Please select a group in browser")
            self.elementNameEntry.configure(
                state="disabled",
                **style.BODY_DANGER
            )
            self.createElementButton.configure(state="disabled")  
    
    def create_element(self):
        
        data = store.get_namespace("browser_selection")
        root = data["root"]
        group = data["group"]
        
        create_element_db(root, group, self.elementNameEntry.get())
        create_element_fd(root, group, self.elementNameEntry.get())
        
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
        self.createElementButton = ctk.CTkButton(
            self.frame,
            text="Create Element",
            **style.BUTTON_STYLE,
            
            command=self.create_element
        )
        self.createElementButton.grid(row=8, sticky="nwe", padx=8, pady=8)
    
    def run(self):
        self.window.wait_window()