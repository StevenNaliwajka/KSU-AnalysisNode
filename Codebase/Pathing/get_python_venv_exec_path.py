from Codebase.Pathing.get_project_root import get_project_root


def get_python_venv_exec_path():
    root = get_project_root()
    file_path = root/ "venv" / "Scripts" / "python.exe"
    return file_path