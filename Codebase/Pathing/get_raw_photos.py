from Codebase.Pathing.get_project_root import get_project_root


def get_raw_photos():
    root = get_project_root()
    folder = root / "Output" / "RawPhotos"
    return folder