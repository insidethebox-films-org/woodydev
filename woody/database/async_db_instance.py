from ..tool import WoodyInstance
from pymongo import AsyncMongoClient

class AsyncMongoDB:

    def __init__(self):
        woody = WoodyInstance()
        self.uri = woody.mongoDBAddress
        self.project = woody.projectName
        
        self.client = AsyncMongoClient(self.uri)
        self.connect = self.client[self.project]
        
    async def get_databases(self):
        databases = await self.client.list_database_names()
        user_databases = [db for db in databases if db not in ("admin", "config", "local")]
        
        return user_databases

    async def get_docs(self, collection_name, query=None):
        if query is None:
            query = {}
        collection = self.connect[collection_name]
        cursor = collection.find(query)
        results = []
        async for doc in cursor:
            results.append(doc)
        return results
    
    async def get_doc(self, collection_name, query):
        collection = self.connect[collection_name]
        doc = await collection.find_one(query)
        return doc
    
    async def add_document(self, collection_name, doc):
        try:
            collection = self.connect[collection_name]
            result = await collection.insert_one(doc)
            return result.inserted_id
        except Exception as e:
            raise Exception(f"Failed to insert document into '{collection_name}': {e}")
        
    async def update_document(self, collection_name, query, update):
        try:
            collection = self.connect[collection_name]
            result = await collection.update_one(query, update)
            return result.modified_count
        except Exception as e:
            raise Exception(f"Failed to update document in '{collection_name}': {e}")
        
