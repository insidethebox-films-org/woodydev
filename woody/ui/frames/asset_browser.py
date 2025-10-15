from ..widgets import CTkListbox
from ...tool.woody_instance import WoodyInstance
from ...tool.event_bus import event_bus
from ...lib.mongodb.get_groups_elements import get_group_sequence_names, get_elements_names
from ...lib.mongodb.get_group_element_details import get_group_element_details


import customtkinter as ctk

class AssetBrowserFrame:
    def __init__(self, parent):
        self.parent = parent
        self.asset_browser_selection = None
        self.current_group = None
        
        event_bus.subscribe('project_selection_changed', self.on_project_change)
        
        self.create_frame()
        self.create_widgets()
            
    def create_frame(self):
        self.frame = ctk.CTkFrame(
            self.parent,
            corner_radius=8,        
            border_width=2,          
            border_color="#5a5a5a",
            )
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=5)
        self.frame.grid_columnconfigure(2, weight=5)
        
        self.frame.grid_rowconfigure(0, weight=1)
        
    def on_project_change(self, project_name):
        print(f"Asset browser refreshing for project: {project_name}")
        self.group_list_box.delete(0, "END")
        self.element_list_box.delete(0, "END")
        self.root_list_box.activate(0)
        self.group_list_box.activate(0)
        
    def on_root_select(self, selected):
        self.current_group_type = selected
        self.group_list_box.delete(0, "END")

        groups = get_group_sequence_names(selected)
        
        for i, group in enumerate(groups):
            self.group_list_box.insert(i, group)
        self.element_list_box.delete(0, "END")
            
    def on_group_select(self, selected):
        self.current_group = selected
        self.element_list_box.delete(0, "END")
        elements = get_elements_names(selected)
        
        for i, element in enumerate(elements):
            self.element_list_box.insert(i, element)
        
        self.asset_browser_selection = {'group_type': self.current_group_type, 'group': selected}
        
        if hasattr(self, 'selection_callback_func') and self.selection_callback_func:
            self.selection_callback_func(self.asset_browser_selection)
            
        WoodyInstance.browser_selection(self.asset_browser_selection)
        WoodyInstance.asset_details(get_group_element_details())
        
        event_bus.publish('browser_selection_changed', self.asset_browser_selection)

    def on_element_select(self, selected):
        self.asset_browser_selection = {'group_type': self.current_group_type,'group': self.current_group, 'element': selected}
        
        if hasattr(self, 'selection_callback_func') and self.selection_callback_func:
            self.selection_callback_func(self.asset_browser_selection)
            
        WoodyInstance.browser_selection(self.asset_browser_selection)
        WoodyInstance.asset_details(get_group_element_details())
        
        event_bus.publish('browser_selection_changed', self.asset_browser_selection)
            
        
    def create_widgets(self):
        
        # Root list box
        self.root_list_box = CTkListbox(
            self.frame,
            highlight_color="#86753d",
            hover_color="#5a5a5a",
            border_width=2,
            command=self.on_root_select
            )
        self.root_list_box.grid(row=0, column=0, sticky="nsew", pady=5, padx=(5,0))
        self.root_list_box.insert(0, "Assets Group") 
        self.root_list_box.insert("END", "Shots Group")
        
        # Group list box
        self.group_list_box = CTkListbox(
            self.frame,
            highlight_color="#86753d",
            hover_color="#5a5a5a",
            border_width=2,
            command=self.on_group_select
        )
        self.group_list_box.grid(row=0, column=1, sticky="nsew", pady=5, padx=(5,0))
        
        # Element list box
        self.element_list_box = CTkListbox(
            self.frame,
            highlight_color="#86753d",
            hover_color="#5a5a5a",
            border_width=2,
            
            command=self.on_element_select
        )
        self.element_list_box.grid(row=0, column=2, sticky="nsew", pady=5, padx=5)