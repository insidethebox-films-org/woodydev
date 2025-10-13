from ..widgets import CTkListbox
from .header import HeaderFrame
from ...lib.mongodb.get_groups_elements import get_group_sequence_names, get_elements_names

import customtkinter as ctk

class AssetBrowserFrame:
    def __init__(self, parent):
        self.parent = parent
        self.create_frame()
        self.create_widgets()
            
    def create_frame(self):
        self.frame = ctk.CTkFrame(
            self.parent,
            corner_radius=8,        
            border_width=2,          
            border_color="#5a5a5a",
            )
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=5)
        self.frame.grid_columnconfigure(2, weight=5)
        
        self.frame.grid_rowconfigure(0, weight=1)

    def on_root_select(self, selected):
        self.current_group_type = selected
        self.group_list_box.delete(0, "END")

        groups = get_group_sequence_names(selected)
        
        for i, group in enumerate(groups):
            self.group_list_box.insert(i, group)
        self.element_list_box.delete(0, "END")

            
    def on_group_select(self, selected):
        self.element_list_box.delete(0, "END")
        elements = get_elements_names(selected)
        
        for i, element in enumerate(elements):
            self.element_list_box.insert(i, element)
    
    def create_widgets(self):
        
        # Root list box
        self.root_list_box = CTkListbox(
            self.frame,
            highlight_color="#86753d",
            hover_color="#5a5a5a",
            border_width=2,
            command=self.on_root_select
            )
        self.root_list_box.grid(row=0, column=0, sticky="nsew", pady=5, padx=(5,0))
        self.root_list_box.insert(0, "Assets Group") 
        self.root_list_box.insert("END", "Shots Group")
        
        # Group list box
        self.group_list_box = CTkListbox(
            self.frame,
            highlight_color="#86753d",
            hover_color="#5a5a5a",
            border_width=2,
            command=self.on_group_select
        )
        self.group_list_box.grid(row=0, column=1, sticky="nsew", pady=5, padx=(5,0))
        
        # Element list box
        self.element_list_box = CTkListbox(
            self.frame,
            highlight_color="#86753d",
            hover_color="#5a5a5a",
            border_width=2
        )
        self.element_list_box.grid(row=0, column=2, sticky="nsew", pady=5, padx=5)