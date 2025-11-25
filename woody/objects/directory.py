from .database import Database
from .operations.mount_drive import mount_drive
from .operations.create_folders_subfolders import create_folders_subfolders
from .operations.get_dcc_executable import get_dcc_executable

import asyncio
import threading
import platform
from pathlib import Path

class Directory():

    def __init__(self, project_name=None):
        self.project_name = None
        self.host_address = None
        self.location = None
        
        self.get_settings(project_name)
        
        self.mount_local_drive(self.host_address, self.location)
        
        self.root_path = self.get_root_path(self.host_address, self.location,  self.project_name)
        
    async def get_settings_async(self, project_name):
    
        if project_name:
            docs = await Database(project_name).get_docs("settings")
            settings = docs[0]
        else:
            docs = await Database().get_docs("settings")
            settings = docs[0]
            
        self.project_name = settings.get("project_name")
        self.host_address = settings.get("host_address")
        self.location = settings.get("location")
        
    def get_settings(self, project_name):

        def run():
            asyncio.run(self.get_settings_async(project_name))
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        thread.join()

    def get_root_path(self, host_address, location, project_name):

        current_os = platform.system()

        if current_os == 'Darwin':
            return Path(f"/Volumes/{location}/{project_name}/".replace('\\', '/'))
        elif platform.system() == "Windows":
            return Path(f"\\\{host_address}\\{location}\\{project_name}\\")
        else:
            print("System not recognized")
            return None
        
    def construct_path(self, subfolders=[]):
    
        path = self.root_path
        
        for i in subfolders:
            path = path / i
        
        return path
    
    def mount_local_drive(self, host_address, location):
        return mount_drive(host_address, location) 

    def create_folders_subfolders(self, base_path, folders):
        return create_folders_subfolders(base_path, folders)
    
    def get_dcc_executable(self, dcc):
        return get_dcc_executable(dcc)

