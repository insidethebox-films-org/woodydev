import platform
import os
import subprocess

def mount_drive(path, normalised):
    
    current_os = platform.system()

    if normalised.startswith('//') and current_os == 'Darwin':
    
        parts = normalised[2:].split('/', 2)
        if len(parts) < 2:
            print(f"{normalised}: is not a valid smb path")
            return None
            
        server = parts[0]
        share = parts[1]
        
        # Mount point
        mount = f"/Volumes/{share}"
        
        if not os.path.ismount(mount):
            smb_url = f"smb://{server}/{share}"
            print(f"Mounting {smb_url} to {mount}...")

            result = subprocess.run(
                ['osascript', '-e', 
                    f'mount volume "{smb_url}"'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                print(f"Warning: Could not mount {smb_url}: {result.stderr}")
                return None

        # Verify mount
        if os.path.ismount(mount):
            if len(parts) >= 3:
                subdirectory = parts[2]
                full_path = os.path.join(mount, subdirectory)
                return full_path
            else:
                return mount
        else:
            print(f"Mount verification failed: {mount}")
            return None
    
    return path.replace("\\", "/")
