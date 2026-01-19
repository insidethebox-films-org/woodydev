def sort_versions(v):
    v = str(v)
    
    if v == "latest":
        return (0, 0)
    if v.isdigit():
        return (1, int(v))
    return (2, v)