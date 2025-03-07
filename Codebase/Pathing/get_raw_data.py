from Codebase.Pathing.get_project_root import get_project_root


def get_raw_data():
    root = get_project_root()
    folder = root / "RawData"
    return folder