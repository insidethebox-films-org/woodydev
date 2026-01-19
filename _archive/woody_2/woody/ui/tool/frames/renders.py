from ... import style
from ..widgets import CTkListbox
from ....database.tool.get_renders_docs import get_renders, get_renders_versions
from ....utils.sort_versions import sort_versions
from ....objects.directory import Directory

from ....dcc.blender.blender import Blender
from ....dcc.houdini.houdini import Houdini
from ....objects.preview_player import PreviewPlayer
from ....objects.rv import RVPlayer

import threading
from pathlib import Path
import customtkinter as ctk
from PIL import Image

class RendersFrame:
    def __init__(self, parent, status_bar):
        self.parent = parent
        self.status_bar = status_bar
        self.create_frame()
        self.create_widgets()
        self.browser_selection = None
        self.dir = Directory()
        self.blender = Blender()
        self.houdini = Houdini()
        self.rv = RVPlayer()
        self.default_preview_img = self.load_default_preview_image()
        
        self.render_doc = None
        self.render_path = None
        self.preview_path = None
        self.render_comment = None
        
        self.preview_label.configure(image=self.default_preview_img)
        self.preview_label.image = self.default_preview_img
            
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
    
    def load_default_preview_image(self):
        img_path = Path(__file__).parent.parent.parent.parent / "icons" / "renders" / "no_media.png"
        img = Image.open(img_path).convert("RGBA")
        bg = Image.new("RGBA", img.size, "#222222") 
        img = Image.alpha_composite(bg, img)
        return ctk.CTkImage(light_image=img, size=(128, 128))
        
    def stop_preview_thread(self):
        if hasattr(self, "preview_player") and self.preview_player:
            self.preview_player.stop()
            self.preview_player = None
        if hasattr(self, "_preview_thread") and self._preview_thread:
            self._preview_thread.join(timeout=0.5)
            self._preview_thread = None
    
    def clear_scenes(self):
        self.stop_preview_thread()
        self.browser_selection = None
        self.renders_list_box.delete(0, "end")
        self.render_version_list_box.delete(0, "end")
        self.preview_label.configure(image=self.default_preview_img)
        self.preview_label.image = self.default_preview_img
        
        self.render_comment_text_box.configure(state="normal")
        self.render_comment_text_box.delete(0.0, "end")
        self.render_comment_text_box.configure(state="disabled")

        self.render_path_entry.configure(state="normal")
        self.render_path_entry.delete(0, "end")
        self.render_path_entry.configure(state="readonly")
        
    def on_element_selected(self, selected):
        self.stop_preview_thread()
        
        if selected:
            self.browser_selection = selected
            
            self.renders_list_box.delete(0, "END")
            
            def get_renders_list(selected, docs):
                if self.browser_selection != selected:
                    return
                items = [doc.get("name") for doc in docs if doc.get("name")]
                items.sort(key=lambda x: x[0].lower())
                
                for name in items:
                    self.renders_list_box.insert("END", name)
                
            def populate_scenes(docs):
                self.frame.after(0, get_renders_list, selected, docs)
                    
            get_renders(callback=populate_scenes)
    
    def on_render_selected(self, selected):
        self.stop_preview_thread()
        def get_versions_list(docs):
            
            self.render_version_list_box.delete(0, "END")
            
            self.render_doc = docs
                
            versions_dict = docs.get("versions", {})
            version_keys = sorted(versions_dict.keys(), key=sort_versions, reverse=True)

            for version in version_keys:
                self.render_version_list_box.insert("END", version)
        
        def populate_versions(docs):
            self.frame.after(0, get_versions_list, docs)
        
        get_renders_versions(selected, callback=populate_versions)
        
    def on_version_selected(self, selected):
        self.stop_preview_thread()
        versions_dict = self.render_doc.get("versions", {})
        version_doc = versions_dict.get(selected, {})
        
        self.render_path = self.dir.root_path / version_doc.get("path")
        self.preview_path = str(Path(self.render_path).parent / "previews")
        self.render_comment = version_doc.get("comment")
        
        self.render_comment_text_box.configure(state="normal")
        self.render_comment_text_box.delete(0.0, "end")
        self.render_comment_text_box.insert(0.0, self.render_comment)
        self.render_comment_text_box.configure(state="disabled")

        self.render_path_entry.configure(state="normal")
        self.render_path_entry.delete(0, "end")
        self.render_path_entry.insert(0, self.render_path)
        self.render_path_entry.configure(state="readonly")

        preview_folder = Path(self.preview_path)
        if not preview_folder.exists() or not preview_folder.is_dir():
            self.preview_label.configure(image=self.default_preview_img)
            self.preview_label.image = self.default_preview_img
            return
        
        image_files = list(preview_folder.glob("*.[pP][nN][gG]")) + \
                     list(preview_folder.glob("*.[jJ][pP][gG]")) + \
                     list(preview_folder.glob("*.[jJ][pP][eE][gG]"))
        
        if not image_files:
            self.preview_label.configure(image=self.default_preview_img)
            self.preview_label.image = self.default_preview_img
            return

        def show_frame(img):
            img = img.copy().convert("RGB")
            frame_w = self.render_preview_frame.winfo_width()
            frame_h = self.render_preview_frame.winfo_height()
            img_w, img_h = img.size
            
            frame_ratio = frame_w / frame_h
            img_ratio = img_w / img_h

            if img_ratio > frame_ratio:
                new_w = frame_w
                new_h = int(frame_w / img_ratio)
            else:
                new_h = frame_h
                new_w = int(frame_h * img_ratio)

            img = img.resize((new_w, new_h), Image.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=img, size=(new_w, new_h))
            self.preview_label.configure(image=ctk_img)
            self.preview_label.image = ctk_img

        if hasattr(self, "preview_player") and self.preview_player:
            self.preview_player.stop()

        self.preview_player = PreviewPlayer(self.preview_path, fps=5)

        def play_in_thread():
            def safe_show_frame(img):
                self.frame.after(0, show_frame, img)
            self.preview_player.play(safe_show_frame, loop=True)

        self._preview_thread = threading.Thread(target=play_in_thread, daemon=True)
        self._preview_thread.start()
            
    def on_play_rv(self):
        self.rv.play(self.render_path)
        self.status_bar.set_message("Playing with RV", msg_type="success")
        
    def on_generate_previews(self):
        self.houdini.post_render_task(self.render_path)
        self.status_bar.set_message("Generating Previews", msg_type="success")
            
    def create_widgets(self):
        # Header
        self.header_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=40
        )
        self.header_frame.grid(row=0, pady=(7, 3), padx=(5,3), sticky="ew")
        self.header_frame.grid_propagate(False)
        
        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text="Renders:",
            **style.HEADER_LABEL
        )
        self.header_label.grid(row=0, padx=12, pady=5, sticky="w")
        
        # Renders listbox
        self.renders_list_box = CTkListbox(
            self.frame,
            **style.LIST_BOX_STYLE,
            
            command=self.on_render_selected
            )
        self.renders_list_box.grid(row=1, column=0, sticky="nsew", pady=(0,5), padx=(5,3))
        
        # Render versions title
        self.render_versions_title_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=30
        )
        self.render_versions_title_frame.grid(row=2, padx=(7,3), pady=(0, 5), sticky="ew")
        self.render_versions_title_frame.grid_propagate(False)
        
        self.scene_versions_title_label = ctk.CTkLabel(
            self.render_versions_title_frame,
            text="Render Versions:",
            **style.SUB_HEADER_LABEL
        )
        self.scene_versions_title_label.grid(row=0, padx=12, sticky="w")
        
        # Render versions listbox
        self.render_version_list_box = CTkListbox(
            self.frame,
            **style.LIST_BOX_STYLE,
            
            command=self.on_version_selected
            )
        self.render_version_list_box.grid(row=3, column=0, sticky="nsew", pady=(0,5), padx=(5,3))
        
        # Render options title
        self.render_options_title_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            fg_color="#222222",
            height=40
        )
        self.render_options_title_frame.grid(row=0, column=1, padx=(0,7), pady=(7,3), sticky="ew")
        self.render_options_title_frame.grid_propagate(False)
        
        self.render_options_title_label = ctk.CTkLabel(
            self.render_options_title_frame,
            text="Render Options:",
            **style.HEADER_LABEL
        )
        self.render_options_title_label.grid(row=0, padx=12, pady=5, sticky="w")
        
        # Render options frame
        self.render_options_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=5,
            border_width=2,
            fg_color="transparent",
        )
        self.render_options_frame.grid(row=1, rowspan=3, column=1, padx=(0,7), pady=(0, 5), sticky="nsew")
        self.render_options_frame.grid_propagate(False)
        self.render_options_frame.grid_columnconfigure(0, weight=1)
        
        # Render Preview
        self.render_preview_frame = ctk.CTkFrame(
            self.render_options_frame,
            corner_radius=5,
            border_width=2,
            fg_color="#222222", 
            height=200 
        )
        self.render_preview_frame.grid(row=0, column=0, padx=10, pady=(10,0), sticky="ew")
        self.render_preview_frame.grid_columnconfigure(0, weight=1)
        self.render_preview_frame.grid_rowconfigure(0, weight=1)
        self.render_preview_frame.grid_propagate(False)
        
        self.preview_label = ctk.CTkLabel(self.render_preview_frame, text="")
        self.preview_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # Render options widgets
        
        self.play_rv_button = ctk.CTkButton(
            self.render_options_frame,
            text="Play with RV",
            **style.BUTTON_STYLE,
            
            command=self.on_play_rv
        )
        self.play_rv_button.grid(row=1, padx=10, pady=(4,4), sticky="ew")
        
        self.render_comment_label = ctk.CTkLabel(
            self.render_options_frame,
            text="Comment:",
            
            **style.SUB_HEADER_LABEL
        )
        self.render_comment_label.grid(row=2, padx=10, pady=(0,3), sticky="w")
        
        self.render_comment_text_box = ctk.CTkTextbox(
            self.render_options_frame,
            height=50,
            corner_radius=5,
            border_width=2,
            fg_color="#222222",
            state="disabled"
        )
        self.render_comment_text_box.grid(row=3, padx=10, pady=(0,3), sticky="ew")
        
        self.render_path_label = ctk.CTkLabel(
            self.render_options_frame,
            text="Render Path:",
            
            **style.SUB_HEADER_LABEL
        )
        self.render_path_label.grid(row=4, padx=10, pady=(0,3), sticky="w")
        
        self.render_path_entry = ctk.CTkEntry(
            self.render_options_frame,
            corner_radius=5,
            border_width=2,
            fg_color="#222222",
            state="readonly"
        )
        self.render_path_entry.grid(row=5, padx=10, pady=(0,3), sticky="ew")
        
        self.generate_previews = ctk.CTkButton(
            self.render_options_frame,
            text="Generate Previews",
            **style.BUTTON_STYLE,
            
            command=self.on_generate_previews
        )    
        self.generate_previews.grid(row=6, padx=10, pady=(0,3), sticky="ew")
        
    
        
        
        