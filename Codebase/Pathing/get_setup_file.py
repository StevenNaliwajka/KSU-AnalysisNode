from Codebase.Pathing.get_codebase_folder import get_codebase_folder


def get_setup_files_file():
    folder = get_codebase_folder()
    file = folder / "Setup" / "setup_files.py"
    return file