from ... import style
from ..windows import SettingsWindow
from ..windows import CreateProjectWindow
from ..windows import CreateElementWindow
from ..windows import CreateGroupWindow
from ..windows import CreateBlendWindow
from ..windows import CreateHipWindow
from ..utils.load_icon import load_icon

import os
import customtkinter as ctk
from PIL import Image

class ToolsFrame:
    def __init__(self, parent, app, status_bar):
        self.parent = parent  
        self.app = app      
        self.status_bar = status_bar  
        self.create_frame()
        self.create_widgets()
            
    def create_frame(self):
        self.frame = ctk.CTkFrame(
            self.parent,
            corner_radius=8,        
            border_width=2,          
            border_color="#b59630",
            width=50
            )
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(8, weight=1)
        self.frame.grid_propagate(False)
        
    def toggle_asset_view(self):
        self.asset_view_active = True
        self.assetViewButton.configure(fg_color="#796B2D")
        self.renderViewButton.configure(fg_color="#414141")
        self.frame.configure(border_color="#b59630")
        self.header_frame.logo_frame.configure(border_color="#b59630")
        self.header_frame.set_logo_image(os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "icons", "woodyHeader.png"
        ))
        self.header_frame.project_picker_frame.configure(border_color="#77563c")
        

        self.app.show_asset_view()

    def toggle_render_view(self):
        self.asset_view_active = False
        self.assetViewButton.configure(fg_color="#414141")
        self.renderViewButton.configure(fg_color="#2d5c83")
        self.frame.configure(border_color="#248ecb")
        self.header_frame.logo_frame.configure(border_color="#248ecb")
        self.header_frame.set_logo_image(os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "icons", "woodyHeaderBlue.png"
        ))
        self.header_frame.project_picker_frame.configure(border_color="#54498d")
        
        self.app.show_render_view()    
        
    def open_create_project(self):
        create_project = CreateProjectWindow(self.parent.winfo_toplevel(), self.status_bar)
        create_project.run()
        
    def open_create_group(self):
        create_group = CreateGroupWindow(self.parent.winfo_toplevel(), self.status_bar)
        create_group.run()
    
    def open_create_element(self):
        create_element = CreateElementWindow(self.parent.winfo_toplevel(), self.status_bar)
        create_element.run()
        
    def open_create_blend(self):
        create_blend = CreateBlendWindow(self.parent.winfo_toplevel(), self.status_bar)
        create_blend.run()
        
    def open_create_hip(self):
        create_blend = CreateHipWindow(self.parent.winfo_toplevel(), self.status_bar)
        create_blend.run()
    
    def open_settings(self):
        settings = SettingsWindow(self.parent.winfo_toplevel(), self.status_bar) 
        settings.run()
    
    def create_widgets(self):
        row = 0
        
        self.tools_label = ctk.CTkLabel(
            self.frame,
            text="View",
            text_color="#B3B3B3",
            **style.BODY_LABEL_BOLD
        )
        self.tools_label.grid(row=row, pady=(3, 1), padx=3, sticky="ew")
        
        row += 1
        
        # Asset View Button
        asset_view_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "icons", "tools", "asset_view.png")
        asset_view_icon = load_icon(asset_view_icon_path, 26)
        
        self.assetViewButton = ctk.CTkButton(
            self.frame,
            image=asset_view_icon,
            text="",
            width=40,
            height=40,
            border_width=2,
            border_color="#b59630",
            **style.BUTTON_STYLE,
            
            command=self.toggle_asset_view
        )
        self.assetViewButton.grid(row=row, column=0, padx=0, pady=(0, 3))
        
        row += 1
        
        # Render View Button
        render_view_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "icons", "tools", "render_view.png")
        render_view_icon = load_icon(render_view_icon_path, 24)
        
        self.renderViewButton = ctk.CTkButton(
            self.frame,
            image=render_view_icon,
            text="",
            width=40,
            height=40,
            border_width=2,
            border_color="#248ecb",
            **style.BUTTON_STYLE,
            
            command=self.toggle_render_view
        )
        self.renderViewButton.grid(row=row, column=0, padx=0, pady=(0, 1))
        
        row += 1
        
        self.tools_label = ctk.CTkLabel(
            self.frame,
            text="Tools",
            text_color="#B3B3B3",
            **style.BODY_LABEL_BOLD
        )
        self.tools_label.grid(row=row, pady=(0, 1), padx=3, sticky="ew")
        
        row += 1
        
        # Create Project Button
        create_project_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "icons", "tools", "create_project.png")
        create_project_icon = load_icon(create_project_icon_path, 22)
        
        self.createProjectButton = ctk.CTkButton(
            self.frame,
            image=create_project_icon,
            text="",
            width=40,
            height=40,
            border_width=2,
            border_color="#b59630",
            **style.BUTTON_STYLE,
            
            command=self.open_create_project
        )
        self.createProjectButton.grid(row=row, column=0, padx=0, pady=(0, 3))
        
        row += 1
        
        # Create Group Button
        create_group_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "icons", "tools", "create_group.png")
        create_group_icon = load_icon(create_group_icon_path, 28)

        self.createGroupButton = ctk.CTkButton(
            self.frame,
            image=create_group_icon,
            text="",
            width=40,
            height=40,
            border_width=2,
            border_color="#b34555",
            **style.BUTTON_STYLE,
            
            command=self.open_create_group
        )
        self.createGroupButton.grid(row=row, column=0, padx=0, pady=(0, 3), sticky="n")
        
        row += 1

        # Create Element Button
        create_element_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "icons", "tools", "create_element.png")
        create_element_icon = load_icon(create_element_icon_path, 25)

        self.createElementButton = ctk.CTkButton(
            self.frame,
            image=create_element_icon,
            text="",
            width=40,
            height=40,
            border_width=2,
            border_color="#4d8242",
            **style.BUTTON_STYLE,
            
            command=self.open_create_element
        )
        self.createElementButton.grid(row=row, column=0, padx=0, pady=(0, 3), sticky="n")
        
        row += 1
        
        # Create Blend Button
        create_blend_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "icons", "tools", "blender.png")
        create_blend_icon = load_icon(create_blend_icon_path, 23)

        self.createBlendButton = ctk.CTkButton(
            self.frame,
            image=create_blend_icon,
            text="",
            width=40,
            height=40,
            border_width=2,
            border_color="#e97824",
            **style.BUTTON_STYLE,
            
            command=self.open_create_blend
        )
        self.createBlendButton.grid(row=row, column=0, padx=0, pady=(0, 3), sticky="n")
        
        row += 1
        
        # Create Houdini Button
        create_hip_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "icons", "tools", "houdini.png")
        create_hip_icon = load_icon(create_hip_icon_path, 21)

        self.createHipButton = ctk.CTkButton(
            self.frame,
            image=create_hip_icon,
            text="",
            width=40,
            height=40,
            border_width=2,
            border_color="#e94c24",
            **style.BUTTON_STYLE,
            
            command=self.open_create_hip
        )
        self.createHipButton.grid(row=row, column=0, padx=0, pady=(0, 5), sticky="n")
        
        row += 1
                
        # Settings Button
        settings_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "icons", "tools", "settings.png")
        settings_icon = load_icon(settings_icon_path, 23)

        self.settingsButton = ctk.CTkButton(
            self.frame,
            image=settings_icon,
            text="",
            width=40,
            height=40,
            border_width=2,
            border_color="#5a5a5a",
            **style.BUTTON_STYLE,
            
            command=self.open_settings
        )
        self.settingsButton.grid(row=row, column=0, padx=0, pady=5, sticky="s")