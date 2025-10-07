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
    
    def create_widgets(self):
    
        listbox = CTkListbox(
            self.frame,
            highlight_color="#86753d",
            hover_color="#5a5a5a",
            border_width=2
            )
        listbox.pack(fill="both", expand=True, padx=5, pady=5)

        listbox.insert(0, "Option 0")
        listbox.insert(1, "Option 1")
        listbox.insert(2, "Option 2")
        listbox.insert(3, "Option 3")
        listbox.insert(4, "Option 4")
        listbox.insert(5, "Option 5")
        listbox.insert(6, "Option 6")
        listbox.insert(7, "Option 7")
        listbox.insert("END", "Option 8")