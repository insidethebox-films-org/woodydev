from .. import style
from ...dcc.blender.client_socket import execute_operation

import os
import customtkinter as ctk

class DccGui:
    def __init__(self, dcc, port=5000):
        self.dcc = dcc
        self.port = port
        self.window = ctk.CTkToplevel()
        self.window.title(f"Woody DCC UI (Port: {port})")
        self.window.geometry("375x170")
        
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "icons",
            "woodyIcon.ico"
        )
        self.window.after(201, lambda: self.window.iconbitmap(icon_path))
        
        self.frame = ctk.CTkFrame(
            self.window,
            corner_radius=10,
            border_width=2,
            border_color="#e97824"
        )
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.frame.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        
    def add_cube(self):
        def print_result(result):
            print(f"Object Added: {result}")
        execute_operation("create_cube", port=self.port, on_success=print_result)
        
    def create_widgets(self):
        
        self.dccLabel = ctk.CTkLabel(
            self.frame, 
            text=f"{self.dcc} Controller",
            **style.HEADER_LABEL
        )
        self.dccLabel.grid(row= 0, column=0, sticky="nw", padx=8, pady=(8, 0))  
        
        separator = ctk.CTkFrame(self.frame, height=2, fg_color="#414141")
        separator.grid(row=1, column=0, sticky="ew", padx=5, pady=(2, 8), columnspan=2) 

        self.createCubeButton = ctk.CTkButton(
            self.frame,
            text="Create Cube",
            **style.BUTTON_STYLE,
            command=self.add_cube
        )
        self.createCubeButton.grid(row=2, sticky="nwe", padx=8, pady=(0, 8))

    def run(self):
        self.window.wait_window()