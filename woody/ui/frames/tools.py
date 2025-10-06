import customtkinter as ctk

class ToolsFrame:
    def __init__(self, parent):
        self.parent = parent
        self.create_frame()
        self.create_widgets()
            
    def create_frame(self):
        self.frame = ctk.CTkFrame(
            self.parent,
            corner_radius=10,        
            border_width=2,          
            border_color="orange",
            width=50
            )
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_propagate(False)
    
    def create_widgets(self):
        return