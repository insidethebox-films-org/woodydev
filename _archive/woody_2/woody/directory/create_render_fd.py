from ..objects import Directory
from ..utils.woody_id import explode_woody_id

def create_render_fd(woody_id, render_name):
    paths = explode_woody_id(woody_id)
    group_type = paths[1]
    group = paths[2]
    element = paths[3]

    dirInstance = Directory()
    base_path = dirInstance.root_path / group_type / group / element

    renders_path = base_path / "renders" / render_name
    renders_path.mkdir(parents=True, exist_ok=True)

    version = 1
    while True:
        version_folder = renders_path / f"v{version}"
        if not version_folder.exists():
            version_folder.mkdir()
            break
        version += 1

    return str(version_folder), int(version)