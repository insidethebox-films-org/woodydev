from .. import style
from ...tool.event_bus import event_bus
from ...database.db_instance import DB_instance
from ...tool.woody_instance import WoodyInstance
from ..widgets import CTkListbox

import os
import customtkinter as ctk
import subprocess
import platform
from PIL import Image

class PublishesFrame:
    def __init__(self, parent):
        self.parent = parent
        self.create_frame()
        self.create_widgets()
        
        self.get_publish_button.configure(state="disabled")
        
        event_bus.subscribe('browser_selection_changed', self.get_publishes)
            
    def create_frame(self):
        self.frame = ctk.CTkFrame(
            self.parent,
            corner_radius=8,        
            border_width=2,          
            border_color="#5a5a5a",
            height=200
            )
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(3, weight=2)
        self.frame.grid_propagate(False)
        
    def load_icon(self, path, size):
        image = Image.open(path)
        original_width, original_height = image.size
        
        if original_width > original_height:
            new_width = size
            new_height = int((original_height * size) / original_width)
        else:
            new_height = size
            new_width = int((original_width * size) / original_height)
        
        return image.resize((new_width, new_height), Image.LANCZOS)
    
    def get_publishes(self, new_browser_selection):

        self.publishes_list_box.delete(0, "END")
        self.publish_version_list_box.delete(0, "END")
        
        self.get_publish_button.configure(state="disabled")
        
        if len(new_browser_selection) < 3:
            return
        
        if not new_browser_selection.get("element"):
            return
        
        publishes_docs = DB_instance().get_docs(
            collection="publishes", 
            key=["source_asset"],
            value=[new_browser_selection.get("element")]
        )
        
        
        if not publishes_docs:
            self.publishes_list_box.insert("END", "No publishes found")
            self.publishes_list_box.configure(state="disabled")
            return
        
        self.publishes_list_box.configure(state="normal")
        
        for doc in publishes_docs:
                publish_name = doc.get("custom_name", "Unknown")
                publish_type = doc.get("publish_type", "OBJECT")
            
                icon_map = {
                    "COLLECTION": "collection",
                    "MATERIAL": "material",
                    "NODE_GROUP": "node_group",
                    "OBJECT": "object"
                }
                
                image_type = icon_map.get(publish_type, "object")
                
                image_path = os.path.join(os.path.dirname(__file__), "..", "..", "icons", "publishes", image_type + ".png")
                
                if os.path.exists(image_path):
                    pil_image = self.load_icon(image_path, 20)
                    icon = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=pil_image.size)
                else:
                    icon = None
                
                self.publishes_list_box.insert("END", publish_name, icon=icon)
    
    def get_publish_versions(self, selected):
        
        versions = DB_instance().get_nested_keys(
            collection="publishes",
            key="custom_name",
            value=selected,
            field_name="published_versions"
        )
        
        self.publish_version_list_box.delete(0, "END")
        
        self.get_publish_button.configure(state="disabled")

        if not versions:
            return
        
        def sort_versions(v):
            if v == "latest":
                return (0, 0) 
            else:
                try:
                    num = int(v) 
                    return (1, -num)
                except ValueError:
                    return (2, v)
                
        versions_sorted = sorted(versions, key=sort_versions)
            
        for i, version in enumerate(versions_sorted):
            self.publish_version_list_box.insert(i, version)
     
    def on_version_selected(self, selected):
        
        if selected:
            self.get_publish_button.configure(state="normal")
        else:
            self.get_publish_button.configure(state="disabled")
        
    def copy_publish_id(self):
        
        browser_selection = WoodyInstance().browser_selection().get("element")
        
        publish_id = DB_instance().get_docs(
            collection="publishes",
            key=["custom_name", "source_asset"],
            value=[self.publishes_list_box.get(), browser_selection],
            key_filter="publish_id",
            find_one=True
        )
  
        version = self.publish_version_list_box.get()
        
        text = f"{publish_id}#ver:{version}"
    
        system = platform.system()

        if system == "Darwin":  # macOS
            subprocess.run("pbcopy", text=True, input=text)
        elif system == "Windows":
            subprocess.run("clip", text=True, input=text)
        else:  # Linux
            subprocess.run("xclip -selection clipboard", shell=True, text=True, input=text)
            
        print("Publish id copied to clipboard!")
            
    def create_widgets(self):
    
        # Header
        self.header_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=40
        )
        self.header_frame.grid(row=0, columnspan=2, pady=(7, 3), padx=7, sticky="ew")
        self.header_frame.grid_propagate(False)
        
        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text="Publishes:",
            **style.HEADER_LABEL
        )
        self.header_label.grid(row=0, pady=7, padx=12, sticky="w")
        
        # Publishes listbox
        self.publishes_list_box = CTkListbox(
            self.frame,
            highlight_color="#86753d",
            hover_color="#5a5a5a",
            border_width=2,
            
            command=self.get_publish_versions
            )
        self.publishes_list_box.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(3,5), padx=5)
        
        # Publish versions title
        self.publish_versions_title_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=30
        )
        self.publish_versions_title_frame.grid(row=2, padx=(7,3), pady=(0, 5), sticky="ew")
        self.publish_versions_title_frame.grid_propagate(False)
        
        self.publish_versions_title_label = ctk.CTkLabel(
            self.publish_versions_title_frame,
            text="Publish Versions:",
            **style.SUB_HEADER_LABEL
        )
        self.publish_versions_title_label.grid(row=0, padx=12, sticky="w")
        
        # Publish options title
        self.publish_options_title_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=30
        )
        self.publish_options_title_frame.grid(row=2, column=1, padx=(0,7), pady=(0, 5), sticky="ew")
        self.publish_options_title_frame.grid_propagate(False)
        
        self.blend_options_title_label = ctk.CTkLabel(
            self.publish_options_title_frame,
            text="Publish Options:",
            **style.SUB_HEADER_LABEL
        )
        self.blend_options_title_label.grid(row=0, padx=12, sticky="w")
        
        # Publish versions listbox
        self.publish_version_list_box = CTkListbox(
            self.frame,
            highlight_color="#86753d",
            hover_color="#5a5a5a",
            border_width=2,
            
            command=self.on_version_selected
            )
        self.publish_version_list_box.grid(row=3, column=0, sticky="nsew", pady=(0,5), padx=5)
        
        # Publish options frame
        self.publish_options_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            border_width=2,
            fg_color="transparent",
            height=30
        )
        self.publish_options_frame.grid(row=3, column=1, padx=(0,7), pady=(0, 5), sticky="nsew")
        self.publish_options_frame.grid_propagate(False)
        self.publish_options_frame.grid_columnconfigure(0, weight=1)
        
        # Get publish button
        self.get_publish_button = ctk.CTkButton(
            self.publish_options_frame,
            text="Copy Publish ID",
            **style.BUTTON_STYLE,
            
            command=self.copy_publish_id
        )
        self.get_publish_button.grid(row=0, padx=7, pady=8, sticky="ew")