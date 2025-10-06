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
            border_color="red",
            )
        self.frame.grid_columnconfigure(0, weight=1)
    
    def create_widgets(self):
    
        test_label = ctk.CTkLabel(
            self.frame,
            text="Asset Browser",
            font=("Arial", 16)
        )
        test_label.grid(row=0, column=0, pady=20)