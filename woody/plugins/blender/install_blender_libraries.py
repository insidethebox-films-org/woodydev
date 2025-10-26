import subprocess
import platform
from pathlib import Path

def get_python_path(blender_path):
    
    system = platform.system()
    
    if system == "Windows":
        python_exe = blender_path / "4.2" / "python" / "bin" / "python.exe"
        site_packages = python_exe.parent.parent / "Lib" / "site-packages"
        
    elif system == "Darwin": 
        if blender_path.name.endswith(".app"):
            blender_path = blender_path / "Contents" / "Resources"
        
        version_dir = next(blender_path.glob("*.*"), None)
        if not version_dir:
            return None, None
        
        python_bin = version_dir / "python" / "bin"
        python_exe = next(python_bin.glob("python3.*"), python_bin / "python3")
        
        result = subprocess.run([str(python_exe), "-c", 
            "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
            capture_output=True, text=True)
        
        py_version = result.stdout.strip() if result.returncode == 0 else "3.11"
        site_packages = python_exe.parent.parent / "lib" / f"python{py_version}" / "site-packages"
        
    else:
        version_dir = next(blender_path.glob("*.*"), None)
        if not version_dir:
            return None, None
        
        python_bin = version_dir / "python" / "bin"
        python_exe = next(python_bin.glob("python3.*"), python_bin / "python3")
        
        result = subprocess.run([str(python_exe), "-c", 
            "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
            capture_output=True, text=True)
        
        py_version = result.stdout.strip() if result.returncode == 0 else "3.11"
        site_packages = python_exe.parent.parent / "lib" / f"python{py_version}" / "site-packages"
    
    return python_exe, site_packages

def install_blender_libraries(blender_executable_path: str) -> bool:
    
    blender_path = Path(blender_executable_path)
    python_exe, site_packages = get_python_path(blender_path)
    
    if not python_exe or not python_exe.exists():
        print(f"Error: Blender Python not found at {python_exe}")
        return False
    
    print(f"Installing to: {python_exe}")
    print(f"Target: {site_packages}")
    
    libraries = ["pymongo"]
    
    for library in libraries:
        print(f"\nInstalling {library}...")
        
        result = subprocess.run([
            str(python_exe), "-m", "pip", "install",
            "--target", str(site_packages),
            "--force-reinstall",
            library
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        
        verify = subprocess.run([
            str(python_exe), "-c",
            f"import sys; sys.path.insert(0, r'{site_packages}'); "
            f"import {library}; print('SUCCESS')"
        ], capture_output=True, text=True)
        
        if verify.returncode == 0:
            print(f"✓ {library} installed successfully")
        else:
            print(f"✗ Verification failed: {verify.stderr}")
            return False
        
    return True