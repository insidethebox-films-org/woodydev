from .. import style
from ..widgets.ctk_list_box import CTkListbox
from ...tool.woody_id import get_dcc_woody_id
from ...objects.dcc import DCC

import os
import customtkinter as ctk

class DccGui:
    def __init__(self, dcc, port=5000):
        cls = DCC.registry.get(dcc.lower())
        if not cls:
            raise ValueError("Unknown DCC")
        
        self.dcc = cls()
        self.dcc_name = dcc
        self.port = port
        self.woody_id = os.environ.get("WOODY_CURRENT_ID")
        
        self.window = ctk.CTkToplevel()
        self.window.title(f"{dcc} Controller")
        self.window.geometry("300x500")
        
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
        self.frame.grid_columnconfigure(1, weight=1)
        
        self.create_widgets()
        
#==============================
# Button Operations
#==============================
        
    def save(self):
        self.dcc.save_file(self.port)
        
    def set_frame_range(self):
        self.dcc.set_frame_range(self.port, self.woody_id)
        
    def set_render_settings(self):
        self.dcc.set_render_settings(self.port)
        
#==============================
# UI
#==============================
        
    def create_widgets(self):
        
        self.dcc_label = ctk.CTkLabel(
            self.frame, 
            text=f"{self.dcc_name} (Port: {self.port})",
            **style.HEADER_LABEL
        )
        self.dcc_label.grid(row= 0, column=0, sticky="nw", padx=8, pady=(8, 0), columnspan=2)  
        
        separator = ctk.CTkFrame(self.frame, height=3, fg_color="#696969")
        separator.grid(row=1, column=0, sticky="ew", padx=8, pady=(2, 0), columnspan=2) 
        
        self.save_label = ctk.CTkLabel(
            self.frame, 
            text="Save",
            **style.SUB_HEADER_LABEL
        )
        self.save_label.grid(row= 2, column=0, sticky="nw", padx=8, pady=2)  
        
        self.save_button = ctk.CTkButton(
            self.frame,
            text="Save",
            **style.DCC_BUTTON_STYLE,
            command=self.save
        )
        self.save_button.grid(row=3, column=0, sticky="nwe", padx=(8,2), pady=2)
        
        self.version_up_button = ctk.CTkButton(
            self.frame,
            text="Version Up",
            **style.DCC_BUTTON_STYLE,
            command=""
        )
        self.version_up_button.grid(row=3, column=1, sticky="nwe", padx=(2,8), pady=2)
        
        self.publish_label = ctk.CTkLabel(
            self.frame, 
            text="Publish",
            **style.SUB_HEADER_LABEL
        )
        self.publish_label.grid(row= 4, column=0, sticky="nw", padx=8, pady=2)
        
        self.load_publish_button = ctk.CTkButton(
            self.frame,
            text="Load Publish",
            **style.DCC_BUTTON_STYLE,
            command=""
        )
        self.load_publish_button.grid(row=5, column=0, columnspan=2, sticky="nwe", padx=8, pady=2)
        
        self.group_list_box = CTkListbox(
            self.frame,
            height=120,
            **style.LIST_BOX_STYLE,
            
            command=""
        )
        self.group_list_box.grid(row=6, column=0, columnspan=2, sticky="new", pady=5, padx=8)
        
        self.publish_entry = ctk.CTkEntry(
            self.frame,
            placeholder_text="Publish Name",
            placeholder_text_color="grey"
        )
        self.publish_entry.grid(row=7, column=0, sticky="new", padx=(8,2), pady=2)

        self.publish_type_comboBox = ctk.CTkComboBox(
            self.frame,
            state="readonly",
            values=[".obj",".abc",".fbx"]
        )
        self.publish_type_comboBox.grid(row=7, column=1, sticky="new", padx=(2,8), pady=2)
        self.publish_type_comboBox.set(".obj")

        self.publish_button = ctk.CTkButton(
            self.frame,
            text="Publish",
            **style.DCC_BUTTON_STYLE,
            command=""
        )
        self.publish_button.grid(row=8, column=0, columnspan=2, sticky="nwe", padx=8, pady=4)

        self.settings_label = ctk.CTkLabel(
            self.frame, 
            text="Settings",
            **style.SUB_HEADER_LABEL
        )
        self.settings_label.grid(row= 9, column=0, sticky="nw", padx=8, pady=(0,2))  
        
        self.render_settings_button = ctk.CTkButton(
            self.frame,
            text="Render Settings",
            **style.DCC_BUTTON_STYLE,
            command=self.set_render_settings
        )
        self.render_settings_button.grid(row=10, column=0, sticky="nwe", padx=(8,2), pady=2)
        
        self.frame_range_button = ctk.CTkButton(
            self.frame,
            text="Frame Range",
            **style.DCC_BUTTON_STYLE,
            command=self.set_frame_range
        )
        self.frame_range_button.grid(row=10, column=1, sticky="nwe", padx=(2,8), pady=2)

    def run(self):
        self.window.wait_window()