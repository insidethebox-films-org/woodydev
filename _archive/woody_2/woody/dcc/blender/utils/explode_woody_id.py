def explode_woody_id(id):  
    try:
        raw_id = id.replace("woodyID:", "")
        raw_id = raw_id.split("|")
        
        project = raw_id[0]
        group_type = raw_id[1]
        group = raw_id[2]
        
        if len(raw_id) > 3:
            element = raw_id[3]
        else:
            element = None
        
        if len(raw_id) > 4 and ":" in raw_id[4]:
            product_list = raw_id[4].split(":")
            product_type = product_list[0]
            product = product_list[1]
            
            id_sections = [project, group_type, group, element, product_type, product]
            return id_sections
        
        elif element:
            id_sections = [project, group_type, group, element]
            return id_sections
        
        else:
            id_sections = [project, group_type, group]
            return id_sections
    
    except Exception as e:
        return {"error": f"Error getting woody id: {e}"}