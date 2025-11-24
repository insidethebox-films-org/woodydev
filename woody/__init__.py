from .ui import *
from .ui.dcc.dcc_gui import DccGui

import customtkinter
import os
import threading
import socket
import json

# Control port allows external DCCs (like Blender) to show/raise DCC GUI windows.
CONTROL_PORT = 6001

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
        
        # Create ui
        self.setup_ui()

        # Start a simple control server to allow external apps to ask Woody
        # to show/raise its window. Run as a daemon thread so it doesn't block.
        try:
            t = threading.Thread(target=_control_server, args=(self,), daemon=True)
            t.start()
        except Exception:
            pass
    
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

    def run(self):
        self.mainWindow.mainloop()


def _show_or_create_dcc_gui(app):
    """Show existing DccGui or create a new one if none exist or all are closed."""
    try:
        # Clean up destroyed windows
        app.dcc_guis = [gui for gui in app.dcc_guis if gui.window.winfo_exists()]
        
        if app.dcc_guis:
            # Bring the first available DccGui to front
            gui = app.dcc_guis[0]
            gui.window.deiconify()
            gui.window.lift()
            try:
                gui.window.attributes("-topmost", True)
                gui.window.after(200, lambda: gui.window.attributes("-topmost", False))
            except Exception:
                pass
        else:
            # Create a new DccGui window
            new_gui = DccGui()
            app.dcc_guis.append(new_gui)
            # Bring the newly created window to front
            new_gui.window.deiconify()
            new_gui.window.lift()
            try:
                new_gui.window.attributes("-topmost", True)
                new_gui.window.after(200, lambda: new_gui.window.attributes("-topmost", False))
            except Exception:
                pass
    except Exception as e:
        print(f"Error in _show_or_create_dcc_gui: {e}")


def _control_server(app):
    """Simple JSON control server. Supported command:
    - {"command":"show_dcc_gui"} - show/raise or create DccGui window

    Runs in a daemon thread. Uses app.mainWindow.after to schedule UI calls on
    the main Tk event loop (thread-safe).
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(("127.0.0.1", CONTROL_PORT))
        s.listen(5)
    except Exception:
        try:
            s.close()
        except Exception:
            pass
        return

    while True:
        try:
            conn, addr = s.accept()
            data = conn.recv(4096)
            try:
                msg = json.loads(data.decode("utf8"))
            except Exception:
                conn.sendall(b'{"status":"error","message":"invalid json"}')
                conn.close()
                continue

            cmd = msg.get("command")
            if cmd == "show_dcc_gui":
                # schedule DccGui show/create on main thread
                app.mainWindow.after(0, lambda: _show_or_create_dcc_gui(app))
                conn.sendall(b'{"status":"ok"}')
            else:
                conn.sendall(b'{"status":"error","message":"unknown command"}')

            conn.close()
        except Exception:
            continue


__all__ = ['WoodyApp']