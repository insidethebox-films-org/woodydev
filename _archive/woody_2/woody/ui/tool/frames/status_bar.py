import customtkinter as ctk

COLORS = {
    "success": "#72a343",
    "warning": "#e9883f",
    "error": "#d13b3b",
}

SUCCESS_TITLE = {
    "text": "Success:",
    "font": ("Arial", 13, "bold"),
    "text_color": COLORS["success"]
}

WARNING_TITLE = {
    "text": "Warning:",
    "font": ("Arial", 13, "bold"),
    "text_color": COLORS["warning"]
}

ERROR_TITLE = {
    "text": "Error:",
    "font": ("Arial", 13, "bold"),
    "text_color": COLORS["error"]
}

class StatusBarFrame:
    def __init__(self, parent):
        self.parent = parent
        self.clear_message_job = None
        self.create_frame()
        self.create_widgets()
            
    def create_frame(self):
        self.frame = ctk.CTkFrame(
            self.parent,
            corner_radius=8,        
            border_width=2,          
            border_color="#72a343",
            fg_color="#222222",
            height=30
            )
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_propagate(False)
        
    def set_message(self, message, msg_type="success"):
        if msg_type == "success":
            title_dict = SUCCESS_TITLE
            self.frame.configure(border_color=COLORS["success"])
        elif msg_type == "warning":
            title_dict = WARNING_TITLE
            self.frame.configure(border_color=COLORS["warning"])
        elif msg_type == "error":
            title_dict = ERROR_TITLE
            self.frame.configure(border_color=COLORS["error"])
        else:
            title_dict = SUCCESS_TITLE

        self.message_title_label.configure(
            text=title_dict["text"],
            font=title_dict["font"],
            text_color=title_dict["text_color"]
        )
        self.message_label.configure(text=message)

        if self.clear_message_job is not None:
            self.frame.after_cancel(self.clear_message_job)
        self.clear_message_job = self.frame.after(5000, self.clear_message)
        
    def clear_message(self):
        self.message_title_label.configure(text="")
        self.message_label.configure(text="")
        self.frame.configure(border_color=COLORS["success"])
        self.clear_message_job = None
    
    def create_widgets(self):
        column = 0

        self.message_title_label = ctk.CTkLabel(
            self.frame,
            height=10,
            text="",
            font=SUCCESS_TITLE["font"],
            text_color=SUCCESS_TITLE["text_color"]
        )
        self.message_title_label.grid(row=0, column=column, padx=(10,3), pady=(7,0), sticky="w")

        column += 1

        self.message_label = ctk.CTkLabel(
            self.frame,
            height=10,
            text=""
        )
        self.message_label.grid(row=0, column=column, padx=(0,10), pady=(7,0), sticky="w")

        column += 1

        self.version_label = ctk.CTkLabel(
            self.frame,
            height=10,
            text_color="#6B6B6B",
            text="Version: 0.1.0"
        )
        self.version_label.grid(row=0, column=column, padx=10, pady=(7,0), sticky="e")