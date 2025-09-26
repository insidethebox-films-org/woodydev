import os
import hashlib

def get_zip_hash(self) -> str:
        """Get hash of addon zip file
        
        Returns:
            str: MD5 hash of the addon zip file, or empty string if not found
        """
        if not os.path.exists(self.addon_zip):
            return ""
        with open(self.addon_zip, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()