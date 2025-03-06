from Codebase.Pathing.get_project_root import get_project_root
from pathlib import Path

def get_data_folder()-> Path:
    root = get_project_root()
    data_folder = root / "Data"
    return data_folder