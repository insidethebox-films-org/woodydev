from ..tool import WoodyInstance

from pymongo import MongoClient


class DB_instance:
    def __init__(self, name=None):
        self.client = self.get_mongo_client()
        self.name = name
        self.connect = self.client[name] if name else None
        self.collections = self.get_collections_from_db()  # Dictionary to store multiple collections
        
    def get_mongo_client(self):
        woody = WoodyInstance()
        return MongoClient(woody.mongoDBAddress)
    
    def get_collections_from_db(self):
        if self.connect is not None:
            return {name: self.connect[name] for name in self.connect.list_collection_names()}
        else:
            return {}
        
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
