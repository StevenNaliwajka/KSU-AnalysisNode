from Codebase.Pathing.get_project_root import get_project_root


def get_codebase_folder():
    root = get_project_root()
    codebase_folder = root/"Codebase"
    return codebase_folder