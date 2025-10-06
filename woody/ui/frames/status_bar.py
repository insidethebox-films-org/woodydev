import customtkinter as ctk

class StatusBarFrame:
    def __init__(self, parent):
        self.parent = parent
        self.create_frame()
        self.create_widgets()
            
    def create_frame(self):
        self.frame = ctk.CTkFrame(
            self.parent,
            corner_radius=8,        
            border_width=2,          
            border_color="green",
            height=30
            )
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_propagate(False)
    
    def create_widgets(self):
        return