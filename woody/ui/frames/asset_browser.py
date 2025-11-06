from .. import style
from ..widgets import CTkListbox

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
        self.frame.grid_columnconfigure(1, weight=10)
        self.frame.grid_columnconfigure(2, weight=10)
        
        self.frame.grid_rowconfigure(0, weight=1)
            
    def create_widgets(self):
        
        # Root list box
        self.root_list_box = CTkListbox(
            self.frame,
            **style.LIST_BOX_STYLE,
            
            command=""
            )
        self.root_list_box.grid(row=0, column=0, sticky="nsew", pady=5, padx=(5,0))
        self.root_list_box.insert(0, "Assets") 
        self.root_list_box.insert("END", "Shots")
        
        # Group list box
        self.group_list_box = CTkListbox(
            self.frame,
            **style.LIST_BOX_STYLE,
            
            command=""
        )
        self.group_list_box.grid(row=0, column=1, sticky="nsew", pady=5, padx=(5,0))
        
        # Element list box
        self.element_list_box = CTkListbox(
            self.frame,
            **style.LIST_BOX_STYLE,
            
            command=""
        )
        self.element_list_box.grid(row=0, column=2, sticky="nsew", pady=5, padx=5)