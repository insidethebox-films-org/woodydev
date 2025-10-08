import customtkinter as ctk

class AssetDetailsFrame:
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
    
        test_label = ctk.CTkLabel(
            self.frame,
            text="Asset Details",
            font=("Arial", 16)
        )
        test_label.grid(row=0, column=0, pady=20)