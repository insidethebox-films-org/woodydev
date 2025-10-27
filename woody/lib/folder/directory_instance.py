from .operations import create_folders_subfolders
from .operations import mount_drive
from .operations import normalise_path

from pathlib import Path

class DirectoryInstance():
    """
    This class abstracts the process of:
      - Normalizing paths across platforms.
      - Mounting remote SMB network drives on macOS.
      - Creating nested folder structures on a mounted or local path.

    Attributes
    ----------
    path : str
        The original input path provided during initialization.
    normalised : str
        The normalized version of the path (with consistent separators and SMB handling).
    mount : str or None
        The mounted drive path if applicable, otherwise the normalized local path.
    folders : dict or None
        A dictionary defining the folder structure to create, where keys are folder names
        and values can be lists or nested dicts of subfolders.
    """

    def __init__(self, path, folders=None):

        if isinstance(path, Path):
            self.path = str(path)
        else:
            self.path = path
            
        self.normalised = self.normalise_path(self.path)
        self.mount = self.mount_drive(self.normalised)
        self.folders = folders

    def normalise_path(self, path):
        return normalise_path(path)

    def mount_drive(self, normalised_path):
        return mount_drive(normalised_path, normalised_path) 

    def create_folders_subfolders(self):
        create_folders_subfolders(self.mount, self.folders)
