from ...tool import WoodyInstance
from ...database.db_instance import DB_instance
from ...database.templates.groups import groups_template
from ...database.templates.sequences import sequences_template

import copy
from datetime import datetime, timezone

def create_groups_sequences_db(type, name):

    woody = WoodyInstance()

    db = DB_instance(woody.projectName)

    if type == 'Assets Group':
        collection_name = "groups"
        template_type = groups_template
        element_type = "assets"

    else:
        collection_name = "sequences"
        template_type = sequences_template
        element_type = "shots"
    
    db.add_collection(collection_name)
    
    template = copy.deepcopy(template_type)
    template["name"] = name
    template[element_type] = None
    template["created_time"] = datetime.now(timezone.utc)  
    template["modified_time"] = datetime.now(timezone.utc)
    
    db.add_document(collection_name, template)
    print(f"Document '{name}' is set up in collection '{collection_name}'.") #TODO
    
    


    
    
