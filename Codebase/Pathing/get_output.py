from Codebase.Pathing.get_project_root import get_project_root


def get_analysis_output():
    root = get_project_root()
    folder = root/"Output"
    return folder