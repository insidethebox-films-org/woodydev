import subprocess
import sys
from pathlib import Path

def install_blender_libraries(blender_executable_path: str) -> bool:
    """Install required libraries into Blender's Python environment"""
    try:
        # Get Blender's Python executable path
        blender_path = Path(blender_executable_path)
        
        if sys.platform == "win32":
            python_exe = blender_path / "4.2" / "python" / "bin" / "python.exe"
        else:
            python_exe = blender_path / "python" / "bin" / "python"
        
        if not python_exe.exists():
            print(f"Error: Blender Python executable not found at {python_exe}")
            return False
        
        print(f"Installing to Blender Python: {python_exe}")
        
        # Get the target site-packages directory
        site_packages_path = python_exe.parent.parent / "Lib" / "site-packages"  # Note: capital "Lib"
        print(f"Target site-packages: {site_packages_path}")
        
        # Install required libraries
        libraries = ["pymongo"]
        
        for library in libraries:
            print(f"Installing {library} directly to Blender's site-packages...")
            
            # Force installation to specific target directory
            result = subprocess.run([
                str(python_exe), "-m", "pip", "install", 
                "--target", str(site_packages_path),
                "--force-reinstall", 
                "--no-deps",  # Install without dependencies first
                library
            ], capture_output=True, text=True)
            
            print(f"Installation output: {result.stdout}")
            if result.stderr:
                print(f"Installation errors: {result.stderr}")
            
            # Now install with dependencies
            if result.returncode == 0:
                print(f"Installing {library} dependencies...")
                deps_result = subprocess.run([
                    str(python_exe), "-m", "pip", "install", 
                    "--target", str(site_packages_path),
                    "--force-reinstall",
                    library
                ], capture_output=True, text=True)
                
                print(f"Dependencies output: {deps_result.stdout}")
            
            # Verify installation in correct location
            verify_result = subprocess.run([
                str(python_exe), "-c", 
                f"""
import sys
sys.path.insert(0, r'{site_packages_path}')
import {library}
print('SUCCESS: {library} installed correctly')
print('Version:', {library}.version)
print('Location:', {library}.__file__)
"""
            ], capture_output=True, text=True)
            
            if verify_result.returncode == 0:
                print(f"✓ {library} successfully installed in Blender!")
                print(verify_result.stdout)
            else:
                print(f"✗ Verification failed: {verify_result.stderr}")
                return False
        
        print("All libraries successfully installed in Blender's Python!")
        return True
        
    except Exception as e:
        print(f"Error installing Blender libraries: {str(e)}")
        import traceback
        traceback.print_exc()
        return False