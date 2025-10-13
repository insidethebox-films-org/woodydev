from ..tool import WoodyInstance
from pymongo import MongoClient
from pathlib import Path


class DB_instance:
    def __init__(self, name=None):
        self.client = self.get_mongo_client()
        self.name = self.get_project_name() if name is None else name
        self.connect = self.client[self.name] if self.name else None
        self.collections = self.get_collections_from_db()  # Dictionary to store multiple collections
        self.projectDirectory = Path(self.get_project_directory()) if self.get_project_directory() else None
        
    def get_mongo_client(self):
        woody = WoodyInstance()
        return MongoClient(woody.mongoDBAddress)

    def get_project_name(self):
        return WoodyInstance().projectName
    
    def get_collections_from_db(self):
        if self.connect is not None:
            return {name: self.connect[name] for name in self.connect.list_collection_names()}
        else:
            return {}
        
    def get_project_directory(self):
        if self.connect is not None:
            settings = self.connect['settings'].find_one({})
            if settings and 'location' in settings:
                path_str = settings['location']
                return path_str
        return None
        
    def add_collection(self, collection_name):
        if self.connect is not None:
            self.collections[collection_name] = self.connect[collection_name]
        else:
            raise Exception("No database selected")

    def add_document(self, collection_name, doc):
        if collection_name in self.collections:
            result = self.collections[collection_name].insert_one(doc)
            return result.inserted_id
        else:
            raise Exception(f"Collection '{collection_name}' not found")  
    
    def update_document(self, collection_name, query, update):
        if collection_name in self.collections:
            result = self.collections[collection_name].update_one(query, update)
            return result.modified_count
        else:
            raise Exception(f"Collection '{collection_name}' not found")

    