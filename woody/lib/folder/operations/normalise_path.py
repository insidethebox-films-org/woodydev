from urllib.parse import urlparse

def normalise_path(path):
    
    path = str(path)
    
    if path.startswith("smb://"):
        parsed = urlparse(path)
        result = f"//{parsed.netloc}{parsed.path}"
        return result
    
    if path.startswith('\\\\') or path.startswith('//'):
        # Convert all backslashes to forward slashes
        normalized = path.replace('\\', '/')
        if not normalized.startswith('//'):
            normalized = '//' + normalized.lstrip('/')
        return normalized
    
    return path