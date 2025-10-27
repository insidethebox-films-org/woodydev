from urllib.parse import urlparse
import platform

def normalise_path(path):
    
    path = str(path)
    
    if path.startswith("smb://"):
        parsed = urlparse(path)
        if platform.system() == "Windows":
            result = f"\\\\{parsed.netloc}{parsed.path}".replace('/', '\\')
        else:
            result = f"//{parsed.netloc}{parsed.path}"
        return result
    
    if path.startswith('\\\\') or path.startswith('//'):
        if platform.system() == "Windows":
            normalized = path.replace('/', '\\')
            if not normalized.startswith('\\\\'):
                normalized = '\\\\' + normalized.lstrip('\\')
        else:
            normalized = path.replace('\\', '/')
            if not normalized.startswith('//'):
                normalized = '//' + normalized.lstrip('/')
        return normalized
    
    return path