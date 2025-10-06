from ...database.db_instance import DB_instance

def get_projects_db():
    
    db = DB_instance().client
    db_list = db.list_database_names()
    
    return [db for db in db_list if db not in ['admin', 'config', 'local']]

