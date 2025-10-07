from ...tool import WoodyInstance

from pymongo import MongoClient

def get_projects_db():
    
    db = WoodyInstance().mongoDBAddress
    db = MongoClient(str(db))
    db_list = db.list_database_names()
    
    return [db for db in db_list if db not in ['admin', 'config', 'local']]

