from .ui import *
from .ui.dcc.dcc_gui import DccGui
from .objects.control_socket import ControlSocket

import customtkinter
import os

class WoodyApp:
    def __init__(self):
        customtkinter.set_appearance_mode("dark")
        
        self.mainWindow = customtkinter.CTk()
        self.mainWindow.geometry("1300x800")
        self.mainWindow.title("Woody")
        self.mainWindow.configure
        
        # Create icon
        icon_path = os.path.join(os.path.dirname(__file__), "icons", "woodyIcon.ico")
        self.mainWindow.iconbitmap(icon_path)
        
        # Track DccGui instances (one per DCC/file)
        self.dcc_guis = []
        
        # Initialize socket handler
        self.socket = ControlSocket()
        
        # Create ui
        self.setup_ui()

        # Start control server
        self.socket.start_control_server(self)
    
    def setup_ui(self):
        
        self.mainWindow.grid_rowconfigure(0, weight=0)  
        self.mainWindow.grid_rowconfigure(1, weight=1)
        self.mainWindow.grid_rowconfigure(2, weight=3)
        self.mainWindow.grid_rowconfigure(3, weight=0)

        self.mainWindow.grid_columnconfigure(0, weight=0)
        self.mainWindow.grid_columnconfigure(1, weight=1)
        self.mainWindow.grid_columnconfigure(2, weight=3)
        self.mainWindow.grid_columnconfigure(3, weight=3)
        
        # Header
        self.header_frame = HeaderFrame(self.mainWindow)
        self.header_frame.frame.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=3, pady=(3, 1))
        
        # Tools
        self.tools_frame = ToolsFrame(self.mainWindow)
        self.tools_frame.frame.grid(row=1, column=0, rowspan=2, sticky="nswe", padx=(3, 1), pady=3)
        
        # Scenes
        self.scenes_frame = ScenesFrame(self.mainWindow)
        self.scenes_frame.frame.grid(row=2, column=2, sticky="nswe", padx=(3, 0), pady=(0, 3))
        
        # Asset Details
        self.asset_details_frame = AssetDetailsFrame(self.mainWindow)
        self.asset_details_frame.frame.grid(row=2, column=1, sticky="nswe", padx=(3, 0), pady=(0, 3))
        
        # Asset Browser
        self.asset_browser_frame = AssetBrowserFrame(self.mainWindow)
        self.asset_browser_frame.frame.grid(row=1, column=1, columnspan=3, sticky="nswe", padx=3, pady=3)
        self.header_frame.asset_browser = self.asset_browser_frame
        self.asset_browser_frame.scenes_frame = self.scenes_frame
        self.asset_browser_frame.asset_details_frame = self.asset_details_frame

        # Publishes
        self.publishes_frame = PublishesFrame(self.mainWindow)
        self.publishes_frame.frame.grid(row=2, column=3, sticky="nswe", padx=3, pady=(0, 3))

        # Status Bar
        self.status_bar_frame = StatusBarFrame(self.mainWindow)
        self.status_bar_frame.frame.grid(row=3, column=0, columnspan=4, sticky="nswe", padx=3, pady=(0, 3))

    def show_or_create_dcc_gui(self, dcc, port=5000):
        try:
            # Clean up closed windows
            self.dcc_guis = [gui for gui in self.dcc_guis if gui.window.winfo_exists()]
            
            # Find existing GUI for this port
            gui = None
            for g in self.dcc_guis:
                if g.port == port:
                    gui = g
                    break
            
            if gui:
                # Bring existing window to front
                gui.window.deiconify()
                gui.window.lift()
                try:
                    gui.window.attributes("-topmost", True)
                    gui.window.after(200, lambda: gui.window.attributes("-topmost", False))
                except Exception:
                    pass
            else:
                # Create new GUI for this port
                new_gui = DccGui(dcc, port)
                self.dcc_guis.append(new_gui)
                new_gui.window.deiconify()
                new_gui.window.lift()
                try:
                    new_gui.window.attributes("-topmost", True)
                    new_gui.window.after(200, lambda: new_gui.window.attributes("-topmost", False))
                except Exception:
                    print(f"Error setting topmost attribute for new_gui.window: {Exception}")
        except Exception as e:
            print(f"Error in show_or_create_dcc_gui: {e}")

    def run(self):
        self.mainWindow.mainloop()


__all__ = ['WoodyApp']