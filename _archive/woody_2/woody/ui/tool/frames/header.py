from ... import style

from ....objects import Database
from ....utils.save_load_settings import save_settings_json, load_settings_json

import os
import asyncio
import threading
import customtkinter as ctk
from PIL import Image


class HeaderFrame:
    def __init__(self, parent, status_bar):
        self.parent = parent
        self.status_bar = status_bar
        self.asset_browser = None
        self.create_frame()
        
        default_logo_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "icons", "woodyHeader.png"
        )
        pil_image = Image.open(default_logo_path)
        self.header_image = ctk.CTkImage(
            light_image=pil_image,
            dark_image=pil_image,
            size=(332 / 3, 90 / 3)
        )
        
        self.create_widgets()
        self.populate_projects_list()
        self.set_project_from_prefs()

    def create_frame(self):
        frames_height=50
        
        # Main frame
        self.frame = ctk.CTkFrame(
            self.parent,
            fg_color="transparent",
            height=frames_height
        )
        self.frame.grid(row=0, column=0, sticky="ew", padx=3, pady=3)
        self.frame.grid_propagate(False)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Logo frame 
        self.logo_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=10,        
            border_width=2,          
            border_color="#b59630",
            fg_color="#222222",
            height=frames_height
        )
        self.logo_frame.grid_columnconfigure(0, weight=1)
        self.logo_frame.grid_rowconfigure(0, weight=1)
        self.logo_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 3), pady=0)
        self.logo_frame.grid_propagate(False) 
        
        # Project picker frame 
        self.project_picker_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=10,        
            border_width=2,          
            border_color="#77563c",
            fg_color="#222222",
            height=frames_height,
            width=235
        )
        self.project_picker_frame.grid_columnconfigure(0, weight=1)
        self.project_picker_frame.grid_rowconfigure(0, weight=1)
        self.project_picker_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.project_picker_frame.grid_propagate(False)
        
    def set_logo_image(self, image_path):
        image = Image.open(image_path)
        new_ctk_image = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=(332 / 3, 90 / 3)
        )
        self.headerImage.configure(image=new_ctk_image)
        self.header_image = new_ctk_image
        
    def set_project_from_prefs(self):
        settings = load_settings_json()
        project = settings.get("projectName")
        self.projectComboBox.set(project)
    
    def populate_projects_list(self):
        
        def run():
            async def fetch():
                db = Database()
                return await db.get_databases()
            
            projects = asyncio.run(fetch())
            self.parent.after(0, lambda: self.update_ui(projects))
        
        threading.Thread(target=run, daemon=True).start()
        
        self.parent.after(5000, self.populate_projects_list)
    
    def update_ui(self, projects):
        
        if not hasattr(self, 'projectComboBox'):
            return
        
        current = self.projectComboBox.get()
        
        if projects:
            self.projectComboBox.configure(values=projects)
            if current in projects:
                self.projectComboBox.set(current)
            elif not current or current == "Loading...":
                self.projectComboBox.set(projects[0])
        else:
            self.projectComboBox.configure(values=["No projects"])
            self.projectComboBox.set("No projects")
        
    def set_project_name_settings(self, selected):
        save_settings_json(projectName=selected)
        
        if self.asset_browser:
            self.asset_browser.group_list_box.delete(0, "END")
            self.asset_browser.element_list_box.delete(0, "END")
            self.asset_browser.root_list_box.deselect(0)
            
            from ....objects.memory_store import store
            store.set_value("browser_selection", "root", None)
            store.set_value("browser_selection", "group", None)
            store.set_value("browser_selection", "element", None)
    
    def create_widgets(self):
        
        self.headerImage = ctk.CTkLabel(
            self.logo_frame, 
            image=self.header_image, 
            text="",
            fg_color="transparent"
        )
        self.headerImage.grid(row=0, column=0, pady=(5, 2), padx=12, sticky="nsw")
        
        self.project_label = ctk.CTkLabel(
            self.project_picker_frame,
            text="Projects:",
            **style.SUB_HEADER_LABEL,
            text_color="#EBEBEB"
        )
        self.project_label.grid(row=0, column=0, sticky="we", padx=(12,0), pady=(0,1))
        
        #Project picker combobox
        self.projectComboBox = ctk.CTkComboBox(
            self.project_picker_frame,
            values="",
            **style.COMBO_BOX_STYLE,
            state="readonly",
            command=self.set_project_name_settings
        )
        self.projectComboBox.grid(row=0, column=1, sticky="we", padx=(6,12))